# -*- coding: utf-8 -*-
import array
import base64
import collections
import ctypes
import json
import logging
import re
import threading
import time
from urllib.parse import urlparse

import wx
import nvwave
import tones
import config as nvda_config

from .. import plugin_state
from .. import vision_config
from ..utils import logging_utils, error_contract
from ..utils.media_capture import (
	_MicCapture,
	_MinimalWebSocket,
	live_resumption_supported,
	live_thinking_level,
	live_thinking_supported,
	resolve_live_model,
)

log = logging.getLogger(__name__)

_ = vision_config._ if hasattr(vision_config, "_") else (lambda x: x)


class LiveSession:
	HOST = vision_config.DEFAULT_API_URLS["gemini"].replace("https://", "")
	REPLY_TIMEOUT = 60.0
	PLAYBACK_GRACE = 3.0
	SILENCE_KEEPALIVE_MS = 1000
	_TOOL_CALL_LIMIT = 1024

	def __init__(
		self,
		on_text,
		on_status,
		on_closed,
		on_stream=None,
		on_user_speech=None,
		prompt_key="live_assistant_system",
		greet=True,
		audio_source="mic",
		model="",
		reporting_style="",
		barge_in=True,
		voice_enabled=True,
		translation_config=None,
		push_to_talk=None,
		context="",
		resume_handle="",
		welcome_prompt="",
		announce_start=True,
		tools=None,
		tool_instruction="",
		on_tool_call=None,
		on_tool_cancel=None,
		output_device=None,
	):
		self.on_text = on_text
		self.on_status = on_status
		self.on_closed = on_closed
		self.on_stream = on_stream
		self.on_user_speech = on_user_speech
		self.prompt_key = prompt_key
		self.greet = greet
		self.audio_source = audio_source
		self.model_override = model
		self.reporting_style = reporting_style
		self.barge_in = barge_in
		self.voice_enabled = voice_enabled
		self.translation_config = translation_config
		self.push_to_talk = push_to_talk
		self.context = context
		self.welcome_prompt = welcome_prompt
		self.announce_start = announce_start
		self.tools = tools
		self.tool_instruction = tool_instruction
		self.on_tool_call = on_tool_call
		self.on_tool_cancel = on_tool_cancel
		self.output_device = output_device
		self._tool_lock = threading.RLock()
		self._pending_tool_calls = {}
		self._seen_tool_ids = set()
		self._tool_names = set()
		if isinstance(tools, list):
			for tool in tools:
				if not isinstance(tool, dict):
					continue
				declarations = tool.get("functionDeclarations", [])
				if not isinstance(declarations, list):
					continue
				for declaration in declarations:
					if isinstance(declaration, dict):
						name = declaration.get("name")
						if isinstance(name, str) and name:
							self._tool_names.add(name)
		self.ws = None
		self.mic = None
		self.player = None
		self._running = False
		self._recv_thread = None
		self._stream_speaker = None
		self._interrupted = False
		self._player_lock = threading.Lock()
		self._ptt_enabled = False
		self._ptt_vks = None
		self._ptt_was_held = False
		self._ptt_thread = None
		self._welcome_in_progress = False
		self._welcome_deadline = 0.0
		self.ready = False
		self._resume_handle = resume_handle or ""
		self.resumption_handle = ""
		self.resumable = False
		self._audio_queue = collections.deque(maxlen=10)
		self._audio_drops = 0
		self._audio_sender = None
		self._model_replying = False
		self._reply_deadline = 0.0
		self._audio_pending = 0
		self._audio_generation = 0
		self._player_on_done = True
		self._ai_stream_buf = ""
		self._turn_is_silent = False
		self._stopped = False

	def _get_player(self):
		with self._player_lock:
			if getattr(self, "_stopped", False) or self._interrupted:
				return None
			if self.player is None:
				try:
					device = self.output_device
					if device is None:
						try:
							device = nvda_config.conf["VisionAssistant"].get("live_output_device", "")
						except Exception:
							device = ""
					if not device:
						try:
							device = nvda_config.conf["audio"]["outputDevice"]
						except (KeyError, IndexError):
							try:
								device = nvda_config.conf["speech"]["outputDevice"]
							except (KeyError, IndexError):
								device = "default"
					self.player = nvwave.WavePlayer(
						channels=1, samplesPerSec=24000, bitsPerSample=16, outputDevice=device or "default"
					)
				except Exception as e:
					log.warning(
						f"Live: WavePlayer with configured device failed ({e}); using default device."
					)
					self.player = nvwave.WavePlayer(channels=1, samplesPerSec=24000, bitsPerSample=16)
			return self.player

	def set_output_device(self, device):
		with self._player_lock:
			if self.output_device == device:
				return
			self.output_device = device
			if self.player:
				try:
					self.player.stop()
					self.player.close()
				except Exception as e:
					log.debug(f"Live: WavePlayer close on device change failed: {e}")
				self.player = None

	def _stop_player(self):
		with self._player_lock:
			self._interrupted = True
			self._speaking_until = 0
			self._audio_generation += 1
			self._audio_pending = 0
			if self.player:
				try:
					self.player.stop()
					self.player.close()
				except Exception as e:
					log.debug(f"Wave player stop failed: {e}")
				self.player = None

	def flush_playback(self):
		self._stop_player()
		self._interrupted = False

	def is_speaking(self):
		return time.time() < getattr(self, "_speaking_until", 0)

	def model_busy(self):
		if self._model_replying and time.time() < self._reply_deadline:
			return True
		if self._audio_playing():
			return True
		return time.time() < getattr(self, "_speaking_until", 0) + 0.4

	def _audio_playing(self):
		if not self._player_on_done:
			return time.time() < getattr(self, "_speaking_until", 0)
		if self._audio_pending <= 0:
			return False
		return time.time() < getattr(self, "_speaking_until", 0) + self.PLAYBACK_GRACE

	def _feed_player(self, player, data):
		with self._player_lock:
			if getattr(self, "_stopped", False) or self._interrupted:
				return
			generation = self._audio_generation
			self._audio_pending += 1
		try:
			player.feed(data, onDone=lambda *args, **kwargs: self._on_chunk_played(generation))
		except TypeError as e:
			log.debug(f"Live: the wave player has no playback callback: {e}")
			self._player_on_done = False
			self._on_chunk_played(generation)
			player.feed(data)
		except Exception:
			self._on_chunk_played(generation)
			raise

	def _on_chunk_played(self, generation):
		with self._player_lock:
			if generation != self._audio_generation:
				return
			if self._audio_pending > 0:
				self._audio_pending -= 1

	def _mark_reply_pending(self):
		self._model_replying = True
		self._reply_deadline = time.time() + self.REPLY_TIMEOUT

	def _clear_reply(self):
		self._model_replying = False
		self._reply_deadline = 0.0

	def _resolve_model(self):
		return resolve_live_model()

	def _resolve_target(self):
		from ..ai.core import AIHandler

		try:
			base = AIHandler.get_base_url(nvda_config.conf["VisionAssistant"]["active_provider"])
			parsed = urlparse(base)
			if parsed.hostname:
				port = parsed.port or (443 if parsed.scheme == "https" else 80)
				is_ssl = parsed.scheme == "https"
				return parsed.hostname, port, is_ssl
		except Exception:
			pass
		return self.HOST, 443, True

	def start(self):
		from ..ai.core import AIHandler
		from ..ai.providers.gemini import GeminiHandler
		from ..prompt_utils import get_prompt_text, apply_prompt_template
		from ..vision_config import get_lang_name

		keys = AIHandler.get_keys(nvda_config.conf["VisionAssistant"]["active_provider"])
		if not keys:
			# Translators: Error message when TTS is not supported by the provider
			self.on_status("ERROR:" + _("No API Keys configured."))
			return False
		model = self.model_override.strip() or self._resolve_model()
		send_voice = self.voice_enabled and "translate" not in model.lower()
		voice = ""
		thinking_level = ""
		plugin = plugin_state.plugin_instance
		if plugin and getattr(plugin, "live_dlg", None) and plugin.live_dlg:
			try:
				dlg = plugin.live_dlg
				if hasattr(dlg, "voice_sel") and dlg.voice_sel:
					sel = dlg.voice_sel.GetSelection()
					if sel != wx.NOT_FOUND:
						voice = vision_config.GEMINI_VOICES[sel][0]
				if hasattr(dlg, "thinking_sel") and dlg.thinking_sel:
					t_sel = dlg.thinking_sel.GetSelection()
					if t_sel != wx.NOT_FOUND:
						thinking_level = dlg.thinking_choices[t_sel][1]
			except Exception:
				pass
		if send_voice and not voice:
			voice = nvda_config.conf["VisionAssistant"].get("tts_voice", "Puck").strip() or "Puck"
		if not thinking_level:
			thinking_level = (
				nvda_config.conf["VisionAssistant"].get("live_thinking_level", "medium").strip() or "medium"
			)
		host, port, is_ssl = self._resolve_target()

		self.ws = None
		num_keys = len(keys)
		start_idx = getattr(GeminiHandler, "_working_key_idx", 0)

		last_error = None
		for i in range(num_keys):
			idx = (start_idx + i) % num_keys
			api_key = keys[idx]
			ws_version = "v1alpha" if self.translation_config else "v1beta"
			path = (
				f"/ws/google.ai.generativelanguage.{ws_version}.GenerativeService.BidiGenerateContent?key={api_key}"
			)

			max_retries = getattr(GeminiHandler, "_max_retries", 3)
			attempt = 0
			while attempt < max_retries:
				if getattr(self, "_stopped", False):
					return False
				try:
					ws_candidate = _MinimalWebSocket(host, path, port=port, is_ssl=is_ssl)
					ws_candidate.connect()
					if getattr(self, "_stopped", False):
						try:
							ws_candidate.close()
						except Exception:
							pass
						return False
					self.ws = ws_candidate
					GeminiHandler._working_key_idx = idx
					break
				except Exception as e:
					last_error = str(e)
					err_str = last_error.lower()
					is_retryable = False
					delay = 1.0 * (attempt + 1)

					if "500" in err_str or "502" in err_str or "503" in err_str or "504" in err_str:
						is_retryable = True
					elif (
						"429" in err_str
						or "high demand" in err_str
						or "exhausted" in err_str
						or "quota" in err_str
					):
						if any(
							x in err_str for x in ["daily", "per day", "per_day", "perday", "requestsperday"]
						):
							is_retryable = False
						else:
							is_retryable = True
							if "high demand" in err_str:
								max_retries = max(max_retries, 10)
							else:
								max_retries = max(max_retries, 5)

					if is_retryable and ("429" in err_str or "quota" in err_str or "exhausted" in err_str):
						match = re.search(r"retry in ([\d\.]+)s", err_str)
						if match:
							try:
								delay = float(match.group(1)) + 0.5
							except Exception as e:
								log.debug(f"Retry delay parse failed: {e}")

					if not is_retryable:
						log.error(f"LiveSession: WebSocket connection failed (Key {idx}): {e}")
						if (
							"403" in err_str
							or "401" in err_str
							or "forbidden" in err_str
							or "unauthorized" in err_str
						):
							break
						break

					if attempt < max_retries - 1:
						log.warning(
							f"LiveSession: Retryable error (Key {idx}, Attempt {attempt + 1}/{max_retries}). Retrying in {delay}s..."
						)
						sleep_end = time.time() + delay
						while time.time() < sleep_end:
							if getattr(self, "_stopped", False):
								return False
							time.sleep(0.1)
						attempt += 1
						continue
					else:
						break
			if getattr(self, "_stopped", False):
				return False
			if self.ws:
				break
			if last_error and error_contract.is_server_busy_error(last_error):
				break

		if not self.ws:
			err_str = last_error if last_error else "Unknown error"

			if "403" in err_str or "forbidden" in err_str.lower():
				# Translators: Error message displayed when access to the Live voice service is blocked or forbidden (HTTP 403 Forbidden).
				err_msg = _("Access denied (HTTP 403 Forbidden). Please check your Proxy/VPN or API key.")
			elif error_contract.is_server_busy_error(err_str):
				# Translators: Error message displayed when the Gemini Live service is temporarily overloaded or experiencing high demand.
				err_msg = _("The AI service is currently busy. Please try again in a moment.")
			else:
				if "b'HTTP" in err_str:
					try:
						status_part = err_str.split("HTTP/1.1 ")[1].split("\\r")[0]
						err_str = f"HTTP {status_part}"
					except Exception:
						pass
				# Translators: Error message announced when connecting to the Live service fails. {error} is replaced with the technical connection error details.
				err_msg = _("Could not connect to the Live service: {error}").format(error=err_str)

			self.on_status("ERROR:" + err_msg)
			return False

		lang = get_lang_name("ai_response_language")
		self.response_lang = lang
		realtime_config = None
		if self.translation_config:
			setup = {
				"setup": {
					"model": f"models/{model}",
					"generationConfig": {
						"responseModalities": ["AUDIO"],
						"translationConfig": dict(self.translation_config),
					},
				}
			}
		else:
			live_instruction = apply_prompt_template(
				get_prompt_text(self.prompt_key),
				[
					("response_lang", lang),
					("reporting_style", self.reporting_style),
					("context", self.context),
				],
			)
			if self.tool_instruction:
				live_instruction += "\n\n" + apply_prompt_template(
					self.tool_instruction,
					[("response_lang", lang), ("reporting_style", self.reporting_style), ("context", self.context)],
				)
			generation_config = {"responseModalities": ["AUDIO"]}
			if live_thinking_supported(model):
				generation_config["thinkingConfig"] = {
					"thinkingLevel": live_thinking_level(model, thinking_level)
				}
			if send_voice and voice:
				generation_config["speechConfig"] = {
					"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}
				}
			realtime_config = {"automaticActivityDetection": {"disabled": False}}
			setup = {
				"setup": {
					"model": f"models/{model}",
					"generationConfig": generation_config,
					"realtimeInputConfig": realtime_config,
					"systemInstruction": {"parts": [{"text": live_instruction}]},
					"outputAudioTranscription": {},
					"inputAudioTranscription": {},
				}
			}
			if self.tools is not None:
				setup["setup"]["tools"] = self.tools
			if live_resumption_supported(model):
				resumption = {}
				if self._resume_handle:
					resumption["handle"] = self._resume_handle
				setup["setup"]["sessionResumption"] = resumption
		if getattr(self, "_stopped", False) or not self.ws:
			if self.ws:
				try:
					self.ws.close()
				except Exception:
					pass
				self.ws = None
			return False
		try:
			self.ws.send_text(json.dumps(setup))
			log.debug("Live setup sent: model=%s realtime=%s", model, json.dumps(realtime_config) if realtime_config else "-")
		except Exception as e:
			log.error(f"Live: Failed to send setup payload: {e}")
			self.stop()
			return False

		self._running = True
		if getattr(self, "_stopped", False):
			self.stop()
			return False
		self._recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
		self._recv_thread.start()
		self._start_audio_sender()
		if self.push_to_talk is None:
			self.set_push_to_talk(bool(nvda_config.conf["VisionAssistant"].get("live_push_to_talk", False)))
		else:
			self.set_push_to_talk(bool(self.push_to_talk))
		try:
			if self.audio_source in ("system", "silence"):
				from ..utils.loopback import create_capture

				self.mic = create_capture(
					self.audio_source,
					self._on_mic_data,
					silence_interval_s=self.SILENCE_KEEPALIVE_MS / 1000.0,
				)
				if self.audio_source == "silence":
					log.debug(
						f"Live: no audio is watched; a silent keepalive is sent every {self.SILENCE_KEEPALIVE_MS} ms."
					)
			elif self.audio_source != "none":
				self.mic = _MicCapture(self._on_mic_data, block_ms=100)
			if self.mic:
				self.mic.start()
		except Exception as e:
			log.error(f"Audio capture failed: {e}", exc_info=True)
			if self.audio_source == "system":
				# Translators: Error shown when the system audio (loopback) cannot be captured for the live session.
				self.on_status("ERROR:" + _("Could not capture the system audio."))
			else:
				# Translators: Error shown when the microphone cannot be opened for the live session.
				self.on_status("ERROR:" + _("Could not open the microphone."))
			self.stop()
			return False
		return True

	def _start_audio_sender(self):
		if self._audio_sender and self._audio_sender.is_alive():
			return
		self._audio_sender = threading.Thread(target=self._audio_sender_loop, daemon=True)
		self._audio_sender.start()

	def _audio_sender_loop(self):
		while self._running and not getattr(self, "_stopped", False):
			if not self._audio_queue:
				time.sleep(0.01)
				continue
			text = self._audio_queue.popleft()
			if not self.ws or self.ws.closed or getattr(self, "_stopped", False):
				self._audio_queue.clear()
				continue
			try:
				self.ws.send_text(text)
			except Exception as e:
				log.debug(f"Live audio send failed: {e}")

	def _queue_audio(self, text):
		if len(self._audio_queue) >= self._audio_queue.maxlen:
			self._audio_drops += 1
			if self._audio_drops == 1 or self._audio_drops % 100 == 0:
				log.warning(
					f"Live: the audio uplink cannot keep up; dropped audio blocks: {self._audio_drops}."
				)
		self._audio_queue.append(text)

	def user_speaking(self):
		return self._ptt_enabled and not self._ptt_gate_open()

	def set_push_to_talk(self, enabled):
		self._ptt_enabled = bool(enabled)
		self._ptt_was_held = False
		self._ptt_vks = None
		if self._ptt_enabled:
			from ..prompt_utils import hotkey_spec_to_vks

			self._ptt_vks = hotkey_spec_to_vks(nvda_config.conf["VisionAssistant"].get("live_ptt_key", ""))
			if not self._ptt_vks:
				log.warning(
					"Live: Push to Talk is enabled but no valid key is configured; the microphone stays open."
				)
		self._start_ptt_monitor()

	def _start_ptt_monitor(self):
		if not self._ptt_enabled or not self._ptt_vks:
			return
		thread = self._ptt_thread
		if thread and thread.is_alive():
			return
		self._ptt_thread = threading.Thread(target=self._ptt_loop, daemon=True)
		self._ptt_thread.start()

	def _ptt_loop(self):
		while self._running and self._ptt_enabled and self._ptt_vks:
			held = self._is_ptt_held()
			if held != self._ptt_was_held:
				self._ptt_was_held = held
				if held:
					wx.CallAfter(tones.beep, 880, 40)
					self._stop_player()
					self._welcome_in_progress = False
					self._notify_user_speech()
				else:
					wx.CallAfter(tones.beep, 440, 40)
					self._send_audio_stream_end()
			time.sleep(0.02)

	def _is_ptt_held(self):
		if not self._ptt_enabled:
			return True
		vks = self._ptt_vks
		if not vks:
			return True
		main_vk, mods, needs_nvda = vks
		get = ctypes.windll.user32.GetAsyncKeyState
		for vk in mods:
			if not (get(vk) & 0x8000):
				return False
		if needs_nvda:
			if not ((get(0x2D) & 0x8000) or (get(0x14) & 0x8000)):
				return False
		if main_vk is None:
			return True
		return bool(get(main_vk) & 0x8000)

	def _ptt_gate_open(self):
		return not self._ptt_enabled or not self._ptt_vks or self._ptt_was_held

	def _on_mic_data(self, pcm_bytes):
		if not self._running or not self.ws or self.ws.closed:
			return

		if self._welcome_in_progress and time.time() > self._welcome_deadline:
			self._welcome_in_progress = False

		if self._ptt_enabled and not self._ptt_gate_open():
			pcm_bytes = bytes(len(pcm_bytes))

		try:
			samples = array.array("h", pcm_bytes)
			peak = max(abs(s) for s in samples)
			if self.barge_in and peak > 3000:
				self._stop_player()
		except Exception as e:
			log.debug(f"Live audio send failed: {e}")

		encoded = base64.b64encode(pcm_bytes).decode()
		if self.translation_config:
			self._tx_blocks = getattr(self, "_tx_blocks", 0) + 1
			if self._tx_blocks % 50 == 1:
				logging_utils.log_addon(
					logging.INFO,
					f"Ambient translate: sending audio to the server (block {self._tx_blocks})",
				)
			msg = {
				"realtimeInput": {
					"mediaChunks": [{"mimeType": "audio/pcm;rate=16000", "data": encoded}]
				}
			}
		else:
			msg = {"realtimeInput": {"audio": {"mimeType": "audio/pcm;rate=16000", "data": encoded}}}
		self._queue_audio(json.dumps(msg))

	def _send_audio_stream_end(self):
		if not self._running or not self.ws or self.ws.closed:
			return
		self._queue_audio(json.dumps({"realtimeInput": {"audioStreamEnd": True}}))

	def send_client_text(self, text):
		if not text or not self._running or not self.ready or not self.ws or self.ws.closed:
			return False
		msg = {
			"clientContent": {
				"turns": [{"role": "user", "parts": [{"text": text}]}],
				"turnComplete": True,
			}
		}
		try:
			self.ws.send_text(json.dumps(msg))
			self._interrupted = False
			self._mark_reply_pending()
			return True
		except Exception as e:
			log.debug(f"Live text turn send failed: {e}")
			return False

	def send_video_frame(self, jpeg_b64):
		if not self._running or not self.ws or self.ws.closed or not jpeg_b64:
			return False
		if getattr(self, "_sending_video", False):
			return False
		self._sending_video = True
		try:
			msg = {"realtimeInput": {"video": {"mimeType": "image/jpeg", "data": jpeg_b64}}}
			self.ws.send_text(json.dumps(msg))
			return True
		except Exception as e:
			log.debug(f"Live message send failed: {e}")
			return False
		finally:
			self._sending_video = False

	def send_image_turn(self, jpeg_b64, text):
		if not self._running or not self.ready or not self.ws or self.ws.closed or not jpeg_b64:
			return False
		parts = [{"inlineData": {"mimeType": "image/jpeg", "data": jpeg_b64}}]
		if text:
			parts.append({"text": text})
		msg = {
			"clientContent": {
				"turns": [{"role": "user", "parts": parts}],
				"turnComplete": True,
			}
		}
		try:
			self.ws.send_text(json.dumps(msg))
			self._interrupted = False
			self._mark_reply_pending()
			return True
		except Exception as e:
			log.debug(f"Live image turn send failed: {e}")
			return False

	def send_tool_response(self, call, response_dict):
		if not isinstance(call, dict) or not isinstance(response_dict, dict):
			return False
		call_id = call.get("id")
		name = call.get("name")
		if not isinstance(call_id, str) or not isinstance(name, str):
			return False
		with self._tool_lock:
			pending = self._pending_tool_calls.get(call_id)
			if pending is None or pending["name"] != name:
				return False
			if not self._running or not self.ready or not self.ws or self.ws.closed:
				return False
			self._pending_tool_calls.pop(call_id)
			try:
				msg = {
					"toolResponse": {
						"functionResponses": [{"id": call_id, "name": name, "response": response_dict}]
					}
				}
				self.ws.send_text(json.dumps(msg))
				return True
			except Exception as e:
				log.debug(f"Live tool response send failed: {e}")
				return False

	def _handle_tool_call(self, call):
		if not isinstance(call, dict):
			return
		call_id = call.get("id")
		name = call.get("name")
		if not isinstance(call_id, str) or not call_id or not isinstance(name, str) or not name:
			log.warning("Live: invalid tool call identity.")
			return
		with self._tool_lock:
			if not self._running or not self.ready or not self.ws or self.ws.closed:
				return
			if call_id in self._seen_tool_ids:
				return
			error = None
			if len(self._seen_tool_ids) >= self._TOOL_CALL_LIMIT:
				error = {"code": "tool_call_limit", "message": "Session tool call limit reached."}
			else:
				self._seen_tool_ids.add(call_id)
			call = dict(call)
			self._pending_tool_calls[call_id] = dict(call)
			if error is None:
				if not isinstance(call.get("args"), dict):
					error = {"code": "invalid_arguments", "message": "Tool arguments must be an object."}
				elif self.translation_config or not self.tools or not callable(self.on_tool_call):
					error = {"code": "tools_unavailable", "message": "Tool calls are not configured."}
				elif name not in self._tool_names:
					error = {"code": "unknown_tool", "message": "Tool is not declared for this session."}
			if error is not None:
				self.send_tool_response(call, {"error": error})
				self._pending_tool_calls.pop(call_id, None)
				return
			try:
				if self.on_tool_call(self, call) is not False:
					return
			except Exception as e:
				log.debug(f"Live tool call dispatch failed: {e}")
			self.send_tool_response(self._pending_tool_calls.get(call_id, {}), {
				"error": {"code": "dispatch_failed", "message": "Tool call could not be dispatched."}
			})

	def _cancel_tool_calls(self, ids=None):
		if ids is not None and (not isinstance(ids, list) or any(not isinstance(i, str) for i in ids)):
			return
		with self._tool_lock:
			if ids is None:
				self._pending_tool_calls.clear()
			else:
				for call_id in ids:
					self._pending_tool_calls.pop(call_id, None)
			if callable(self.on_tool_cancel):
				try:
					self.on_tool_cancel(self, ids)
				except Exception as e:
					log.debug(f"Live tool cancellation dispatch failed: {e}")

	def _recv_loop(self):
		while self._running and not getattr(self, "_stopped", False):
			opcode, payload = self.ws.recv()
			if opcode is None:
				if self._running and not getattr(self, "_stopped", False):
					reason = self.ws.close_reason

					# Translators: Fallback close reason when the Live connection terminates without a specific server code.
					unknown_reason = _("unknown")
					# Translators: Message displayed in the Live Assistant dialog when the server unexpectedly closes the connection. {reason} is the server disconnect reason.
					self.on_text(_("[Connection closed: {reason}]").format(reason=reason or unknown_reason))
				break
			if opcode == 0x9:
				try:
					self.ws._send_frame(0xA, payload or b"")
				except Exception as e:
					log.debug(f"WebSocket ping reply failed: {e}")
				continue
			if opcode != 0x1 and opcode != 0x2:
				continue
			try:
				data = json.loads(payload.decode("utf-8", "replace"))
				self._handle_message(data)
			except Exception as e:
				log.error(f"Live: Failed to decode received payload: {e}")
		if self._running:
			self.stop()

	def _handle_message(self, data):
		if getattr(self, "_stopped", False):
			return
		if "setupComplete" in data:
			with self._tool_lock:
				if not self._running:
					return
				self.ready = True
			if not self.greet:
				self._welcome_in_progress = False
				return
			self._welcome_in_progress = True
			self._welcome_deadline = time.time() + 8.0
			if self.announce_start:
				# Translators: Message announced by NVDA when the live voice conversation starts.
				self.on_status("STATUS:" + _("Live conversation started. You can speak now."))
			lang = getattr(self, "response_lang", "English")
			if self.welcome_prompt:
				trigger_prompt = self.welcome_prompt.format(lang=lang)
			else:
				trigger_prompt = (
					f"Please greet the user warmly, introduce yourself exactly as 'Vision Assistant Pro' (DO NOT translate this name, keep it in English), "
					f"and ask how you can help them today. Speak strictly in {lang}."
				)

			msg = {
				"clientContent": {
					"turns": [{"role": "user", "parts": [{"text": trigger_prompt}]}],
					"turnComplete": True,
				}
			}
			try:
				self.ws.send_text(json.dumps(msg))
				self._mark_reply_pending()
			except Exception as e:
				log.error(f"Live: Failed to send dynamic welcome trigger: {e}")
			return
		if "error" in data:
			err = data.get("error", {})
			err_msg = err.get("message") if isinstance(err, dict) else str(err)
			log.error(f"Live: Server returned error: {err_msg}")
			self.on_status("ERROR:" + str(err_msg))
			return

		resumption = data.get("sessionResumptionUpdate") or data.get("session_resumption_update")
		if resumption:
			new_handle = resumption.get("newHandle") or resumption.get("new_handle") or ""
			if new_handle:
				self.resumption_handle = new_handle
			self.resumable = bool(resumption.get("resumable", True))
			log.debug(f"Live: session resumption update (resumable={self.resumable}).")

		tool_call = data.get("toolCall")
		if isinstance(tool_call, dict):
			calls = tool_call.get("functionCalls")
			if isinstance(calls, list):
				for call in calls:
					self._handle_tool_call(call)
		cancellation = data.get("toolCallCancellation")
		if isinstance(cancellation, dict):
			self._cancel_tool_calls(cancellation.get("ids"))

		server_content = data.get("serverContent")
		if not server_content:
			return
		if getattr(self, "_rx_logged", 0) < 5:
			self._rx_logged = getattr(self, "_rx_logged", 0) + 1
			logging_utils.log_addon(
				logging.INFO,
				f"Live server message: {list(data.keys())} -> serverContent keys: {list(server_content.keys())}",
			)

		if server_content.get("interrupted"):
			log.debug("Live: previous turn was interrupted by a new request")
			self._ai_stream_buf = ""
			self._turn_is_silent = False
			if not self.translation_config:
				self.flush_playback()
			self._clear_reply()
			self._end_stream_line()

		if "inputTranscription" in server_content or "input_transcription" in server_content:
			self._interrupted = False
			in_tx = (
				server_content.get("inputTranscription") or server_content.get("input_transcription") or {}
			)
			if in_tx.get("text"):
				# Translators: Prefix for the user's transcribed speech line in the Live Assistant history.
				self._stream("user", _("You: "), in_tx["text"])
				self._notify_user_speech()

		out_tx = server_content.get("outputTranscription") or server_content.get("output_transcription")
		if out_tx and out_tx.get("text"):
			raw_tx = out_tx["text"]
			if self._is_silence_artifact(raw_tx):
				self._turn_is_silent = True
			clean_text = self._sanitize_ai_chunk(raw_tx)
			if clean_text.strip():
				if self._is_silence_artifact(clean_text):
					self._turn_is_silent = True
				else:
					self._turn_is_silent = False
					self._stream("ai", _("AI: "), clean_text)

		model_turn = server_content.get("modelTurn") or server_content.get("model_turn") or {}
		for part in model_turn.get("parts", []):
			inline = part.get("inlineData") or part.get("inline_data")
			if inline and inline.get("data") and not self._turn_is_silent:
				if self.translation_config:
					self._interrupted = False
				if not self._interrupted:
					try:
						p = self._get_player()
						data = base64.b64decode(inline["data"])
						if p:
							self._feed_player(p, data)
							duration = len(data) / 2 / 24000.0
							self._speaking_until = max(
								time.time(), getattr(self, "_speaking_until", 0)
							) + duration
					except Exception as e:
						log.error(f"Live playback failed: {e}")
			text = part.get("text")
			if text:
				if self._is_silence_artifact(text):
					self._turn_is_silent = True
				clean_part = self._sanitize_ai_chunk(text)
				if clean_part.strip():
					if self._is_silence_artifact(clean_part):
						self._turn_is_silent = True
					else:
						self._turn_is_silent = False
						# Translators: Prefix for an AI message line in the Live Assistant history.
						self._stream("ai", _("AI: "), clean_part)

		if server_content.get("turnComplete") or server_content.get("turn_complete"):
			remaining = self._flush_ai_stream_buf()
			if remaining and not self._is_silence_artifact(remaining):
				self._stream("ai", _("AI: "), remaining)
			self._turn_is_silent = False
			self._welcome_in_progress = False
			self._interrupted = False
			self._clear_reply()
			self._end_stream_line()

	@staticmethod
	def _is_silence_artifact(text):
		if not text:
			return True
		t = text.strip()
		if not t:
			return True
		untagged = re.sub(
			r"<[^>]+>|\{[^}]+\}|\[[^\]]+\]|\(\s*(?:silence|silenzio|silencio|stille|no[\s_-]*speech|pause)\s*\)",
			"",
			t,
			flags=re.IGNORECASE,
		).strip()
		if not untagged:
			return True
		if not any(c.isalnum() for c in untagged):
			return True
		if re.match(r"^[\(\[\{<]\s*pause\s*[\)\]\}>]$", t, re.IGNORECASE):
			return True
		core = re.sub(r"^[\s\(\[\{<\-_.\*…—–~'\"`]+|[\s\)\]\}>\-_.\*…—–~'\"`]+$", "", untagged).lower()
		return core in {
			"silenzio", "silence", "silencio", "silêncio", "stille",
			"no speech", "nospeech", "no_speech", "no-speech",
			"no sound", "nosound", "no_sound", "no-sound",
		}

	def _sanitize_ai_chunk(self, text):
		if not text:
			return ""
		self._ai_stream_buf += text
		last_open_angle = self._ai_stream_buf.rfind("<")
		last_close_angle = self._ai_stream_buf.rfind(">")
		last_open_brace = self._ai_stream_buf.rfind("{")
		last_close_brace = self._ai_stream_buf.rfind("}")
		last_open_bracket = self._ai_stream_buf.rfind("[")
		last_close_bracket = self._ai_stream_buf.rfind("]")

		split_pos = len(self._ai_stream_buf)
		for open_idx, close_idx in [
			(last_open_angle, last_close_angle),
			(last_open_brace, last_close_brace),
			(last_open_bracket, last_close_bracket),
		]:
			if open_idx > close_idx:
				split_pos = min(split_pos, open_idx)

		ready = self._ai_stream_buf[:split_pos]
		self._ai_stream_buf = self._ai_stream_buf[split_pos:]
		cleaned = re.sub(
			r"<[^>]+>|\{[^}]+\}|\[[^\]]+\]|\(\s*(?:silence|silenzio|silencio|stille|no[\s_-]*speech|pause)\s*\)",
			"",
			ready,
			flags=re.IGNORECASE,
		)
		return cleaned

	def _flush_ai_stream_buf(self):
		cleaned = re.sub(
			r"<[^>]+>|\{[^}]+\}|\[[^\]]+\]|\(\s*(?:silence|silenzio|silencio|stille|no[\s_-]*speech|pause)\s*\)",
			"",
			self._ai_stream_buf,
			flags=re.IGNORECASE,
		)
		self._ai_stream_buf = ""
		return cleaned

	def _notify_user_speech(self):
		if not self.on_user_speech:
			return
		try:
			self.on_user_speech()
		except Exception as e:
			log.debug(f"Live user speech callback failed: {e}")

	def _stream(self, speaker, prefix, text):
		if getattr(self, "_stopped", False):
			return
		log.debug("Live %s said: %s", speaker, text)
		if self._stream_speaker != speaker:
			if self._stream_speaker is not None and self.on_stream:
				self.on_stream("\n")
			if self.on_stream:
				self.on_stream(prefix)
			self._stream_speaker = speaker
		if self.on_stream:
			self.on_stream(text)

	def _end_stream_line(self):
		if self._stream_speaker is not None and self.on_stream:
			self.on_stream("\n")
		self._stream_speaker = None

	def stop(self):
		self._stopped = True
		with self._tool_lock:
			self.ready = False
			inactive = not self._running and self.ws is None
			self._running = False
			if not inactive or self._pending_tool_calls:
				self._cancel_tool_calls()
			if inactive:
				return
		self._ptt_enabled = False
		if self.mic:
			try:
				self.mic.stop()
			except Exception as e:
				log.debug(f"Mic stop failed: {e}")
			self.mic = None
		if self.ws:
			try:
				self.ws.close()
			except Exception as e:
				log.debug(f"WebSocket close failed: {e}")
			self.ws = None
		self._stop_player()
		if self.on_closed:
			try:
				self.on_closed()
			except Exception as e:
				log.debug(f"on_closed callback failed: {e}")
