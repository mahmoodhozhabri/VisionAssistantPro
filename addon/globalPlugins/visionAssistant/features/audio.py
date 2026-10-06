# -*- coding: utf-8 -*-
import wx
import os
import wave
import base64
import threading
import ctypes
import logging
import re
import subprocess
import time
import json
import tempfile

import ui
import core
import api
import tones
import scriptHandler
import gui
import config as nvda_config
import addonHandler

from .. import vision_config
from ..vision_config import ADDON_NAME
from ..prompt_utils import apply_prompt_template, get_prompt_text
from ..ai.core import AIHandler, is_ai_error, ai_error_message
from ..utils.system import (
	clean_markdown,
	show_error_dialog,
	get_mime_type,
	get_focused_explorer_files,
)
from ..utils.mouse_keyboard import send_ctrl_v
from ..utils.media_capture import ensure_ffmpeg
from ..utils import error_contract


log = logging.getLogger(__name__)

addonHandler.initTranslation()


class AudioMixin:
	@scriptHandler.script(
		# Translators: Script description for 'Records voice, transcribes it using AI, and types the result.' in Input Gestures dialog.
		description=_("Records voice, transcribes it using AI, and types the result."),
		category=ADDON_NAME,
	)
	def script_smartDictation(self, gesture):
		self._toggle_voice_capture("transcribe")

	@scriptHandler.script(
		# Translators: Script description for 'Shows a list of available commands in the layer.' in Input Gestures dialog.
		description=_("Records voice, transcribes and translates it using AI, and types the result."),
		category=ADDON_NAME,
	)
	def script_voiceTranslation(self, gesture):
		self._toggle_voice_capture("translate")

	def _toggle_voice_capture(self, mode):
		if getattr(self, "toggling", False):
			self.finish()
		flag = "is_recording" if mode == "transcribe" else "is_translation_recording"
		alias = "myaudio" if mode == "transcribe" else "myaudiotrans"
		if not getattr(self, flag, False):
			setattr(self, flag, True)
			tones.beep(800, 100)
			try:
				ret_open = ctypes.windll.winmm.mciSendStringW(
					f"open new type waveaudio alias {alias}",
					None,
					0,
					0,
				)
				if ret_open != 0:
					setattr(self, flag, False)
					# Translators: Message in an error dialog which can pop up while trying dictation.
					msg = _("Audio Hardware Error: {error}").format(error=f"MCI_OPEN_ERR_{ret_open}")
					show_error_dialog(msg)
					return

				ret_rec = ctypes.windll.winmm.mciSendStringW(f"record {alias}", None, 0, 0)
				if ret_rec != 0:
					setattr(self, flag, False)
					ctypes.windll.winmm.mciSendStringW("close all", None, 0, 0)
					msg = _("Audio Hardware Error: {error}").format(error=f"MCI_RECORD_ERR_{ret_rec}")
					show_error_dialog(msg)
					return

				# Translators: Message reported when dictation or voice translation recording starts.
				msg = _("Listening...")
				self.report_status(msg)
			except Exception as e:
				msg = _("Audio Hardware Error: {error}").format(error=e)
				show_error_dialog(msg)
				setattr(self, flag, False)
		else:
			setattr(self, flag, False)
			tones.beep(500, 100)
			try:
				ctypes.windll.winmm.mciSendStringW(f'save {alias} "{self.temp_audio_file}"', None, 0, 0)
				ctypes.windll.winmm.mciSendStringW(f"close {alias}", None, 0, 0)
				threading.Thread(target=self._thread_dictation, args=(mode,), daemon=True).start()
			except Exception as e:
				# Translators: Message in an error dialog which can pop up while trying dictation.
				msg = _("Save Recording Error: {error}").format(error=e)
				show_error_dialog(msg)

	def _thread_dictation(self, mode="transcribe"):
		try:
			if not os.path.exists(self.temp_audio_file):
				return

			try:
				with wave.open(self.temp_audio_file, "rb") as wave_file:
					frame_rate = wave_file.getframerate()
					n_frames = wave_file.getnframes()
					duration = n_frames / float(frame_rate)

				if duration < 1.0:
					# Translators: Message reported when the AI detects silence or empty speech
					msg = _("No speech detected.")
					core.callLater(0, self.report_status, msg)
					if os.path.exists(self.temp_audio_file):
						try:
							os.remove(self.temp_audio_file)
						except Exception as e:
							log.warning(f"Temp file removal failed: {e}")
					return
			except Exception as e:
				log.warning(f"Dictation duration check failed: {e}")

			if mode == "transcribe":
				# Translators: Message reported when processing dictation
				core.callLater(0, self.report_status, _("Typing..."))
			else:
				# Translators: Message reported when calling translation command
				core.callLater(0, self.report_status, _("Translating..."))

			with open(self.temp_audio_file, "rb") as f:
				audio_data = base64.b64encode(f.read()).decode("utf-8")

			if mode == "transcribe":
				dictation_template = get_prompt_text("dictation_transcribe")
				p = apply_prompt_template(
					dictation_template,
					[("response_lang", vision_config.get_lang_name("ai_response_language"))],
				)
			else:
				translation_template = get_prompt_text("dictation_translate")

				s = vision_config.get_lang_name("source_language")
				t = vision_config.get_lang_name("target_language")
				swap = nvda_config.conf["VisionAssistant"]["smart_swap"]
				fallback = "English" if vision_config.is_auto_language("source_language") else s

				p = apply_prompt_template(
					translation_template,
					[
						("source_lang", s),
						("target_lang", t),
						("swap_target", fallback),
						("smart_swap", str(swap)),
					],
				)

			res = AIHandler.call(p, attachments=[{"mime_type": "audio/wav", "data": audio_data}])

			if res:
				if is_ai_error(res):
					log.error(
						f"{'Dictation' if mode == 'transcribe' else 'Voice Translation'} AI call error: {res}",
					)
					wx.CallAfter(show_error_dialog, ai_error_message(res))
				elif "NOSPEECH" in res.upper():
					msg = _("No speech detected.")
					core.callLater(0, self.report_status, msg)
				else:
					cleaned_text = clean_markdown(res)
					core.callLater(0, self._paste_text, cleaned_text)
			else:
				log.error(
					f"{'Dictation' if mode == 'transcribe' else 'Voice Translation'}: AI returned empty response",
				)
				# Translators: Message reported while trying dictation.
				msg = _("No speech recognized or Error.")
				core.callLater(0, self.report_status, msg)

			if os.path.exists(self.temp_audio_file):
				try:
					os.remove(self.temp_audio_file)
				except Exception as e:
					log.warning(f"Temp file removal failed: {e}")
		except Exception as e:
			log.error(
				f"{'Dictation' if mode == 'transcribe' else 'Voice Translation'} thread failed: {e}",
				exc_info=True,
			)
		finally:
			# Translators: Error message shown when uploading a video file fails.
			self.current_status = _("Idle")
			flag = "is_recording" if mode == "transcribe" else "is_translation_recording"
			setattr(self, flag, False)

	def _paste_text(self, text):
		api.copyToClip(text)
		send_ctrl_v()
		wx.CallLater(300, self._announce_paste, text)

	def _announce_paste(self, text):
		preview = text[:100]
		# Translators: Message reported when dictation is complete
		msg = _("Typed: {text}").format(text=preview)
		tones.beep(1000, 100)
		self.report_status(msg)

	@scriptHandler.script(description=_("Transcribes or dubs a selected media file."), category=ADDON_NAME)
	def script_mediaTranscriber(self, gesture):
		if getattr(self, "toggling", False):
			self.finish()
		if getattr(self, "_dialog_open", False):
			return
		focused_paths = get_focused_explorer_files()
		valid_exts = (".mp3", ".wav", ".ogg", ".m4a", ".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv")
		valid_paths = [p for p in focused_paths if p.lower().endswith(valid_exts)]
		if valid_paths:
			wx.CallAfter(self._ask_audio_action, valid_paths[0])
			return
		wx.CallLater(100, self._open_audio)

	def _open_audio(self):
		self._dialog_open = True
		wc = "Audio/Video|*.mp3;*.wav;*.ogg;*.m4a;*.mp4;*.mkv;*.avi;*.mov;*.flv;*.wmv"
		self._browse_and_run(self._ask_audio_action_from_browse, wc, multiple=False)
		self._dialog_open = False

	def _ask_audio_action_from_browse(self, path):
		if path:
			wx.CallAfter(self._ask_audio_action, path)

	def _ask_audio_action(self, path):
		# Translators: Option in media action menu to transcribe audio in its original language
		opt_transcribe = _("Transcribe (Original Language)")
		# Translators: Option in media action menu to transcribe and translate audio to the target language
		opt_transcribe_translate = _("Transcribe and Translate (Target Language)")
		choices = [opt_transcribe, opt_transcribe_translate]
		if AIHandler.is_gemini():
			# Translators: Option in media action menu to live translate/dub audio
			opt_dub = _("Dub and Translate (Target Language)")
			choices.append(opt_dub)

		gui.mainFrame.prePopup()
		try:
			# Translators: Prompt message asking user to choose an action for the media file
			prompt_msg = _("Choose action:")
			# Translators: Title of the media file action selection dialog
			dlg_title = _("Media File")
			dlg = wx.SingleChoiceDialog(gui.mainFrame, prompt_msg, dlg_title, choices)
			dlg.Raise()
			if dlg.ShowModal() == wx.ID_OK:
				selection = dlg.GetSelection()
				if selection == 0:
					threading.Thread(
						target=self._thread_audio,
						args=(path, "transcribe"),
						daemon=True,
					).start()
				elif selection == 1:
					dlg.Destroy()
					from ..dialogs.media import DubbingDialog

					dub_dlg = DubbingDialog(gui.mainFrame, is_dubbing=False)
					dub_dlg.Raise()
					if dub_dlg.ShowModal() == wx.ID_OK:
						s_lang, t_lang = dub_dlg.get_settings()
						threading.Thread(
							target=self._thread_audio,
							args=(path, "translate", s_lang, t_lang),
							daemon=True,
						).start()
					dub_dlg.Destroy()
					return
				elif selection == 2:
					dlg.Destroy()
					from ..dialogs.media import DubbingDialog

					dub_dlg = DubbingDialog(gui.mainFrame, is_dubbing=True)
					dub_dlg.Raise()
					if dub_dlg.ShowModal() == wx.ID_OK:
						s_lang, t_lang = dub_dlg.get_settings()
						threading.Thread(
							target=self._thread_live_translate_audio,
							args=(path, s_lang, t_lang),
							daemon=True,
						).start()
					dub_dlg.Destroy()
					return
			dlg.Destroy()
		except Exception as e:
			log.warning(f"Audio action dialog failed: {e}")
		finally:
			gui.mainFrame.postPopup()
			self._dialog_open = False

	def _thread_audio(self, path, action_type, s_lang=None, t_lang=None):
		log.info(f"Media processing started: path={path}, action={action_type}")
		try:
			# Translators: Message reported when calling the audio transcription command
			msg = _("Uploading...")
			core.callLater(0, self.report_status, msg)
			mime_type = get_mime_type(path)
			lang = vision_config.get_lang_name("ai_response_language")
			if action_type == "transcribe":
				audio_template = get_prompt_text("audio_transcription")
				p = apply_prompt_template(audio_template, [("response_lang", lang)])
			else:
				audio_template = get_prompt_text("audio_translation")
				target_lang = t_lang if t_lang else vision_config.get_lang_name("target_language")
				source_lang = s_lang if s_lang else vision_config.get_lang_name("source_language")
				p = apply_prompt_template(
					audio_template,
					[("target_lang", target_lang), ("source_lang", source_lang)],
				)

			if AIHandler.is_gemini():
				file_uri = self._upload_file_to_gemini(path, mime_type)
				if not file_uri:
					return
				att = [{"mime_type": mime_type, "file_uri": file_uri}]
			else:
				with open(path, "rb") as f:
					audio_data = base64.b64encode(f.read()).decode("utf-8")
				att = [{"mime_type": mime_type, "data": audio_data}]

			# Translators: Progress message spoken when the add-on starts taking a screenshot of the current focused object.
			msg = _("Analyzing...")
			core.callLater(0, self.report_status, msg)
			res = AIHandler.call(p, attachments=att)

			if res:
				if is_ai_error(res):
					wx.CallAfter(show_error_dialog, ai_error_message(res))
					return
				wx.CallAfter(self._open_doc_chat_dialog, res, att, res, res)
		except Exception as e:
			log.error(f"Audio analysis thread failed: {e}", exc_info=True)
		finally:
			self.current_status = _("Idle")

	def _thread_live_translate_audio(self, path, s_lang, t_lang):
		try:
			# Translators: Status message when extracting audio and connecting to Gemini for dubbing
			core.callLater(0, self.report_status, _("Extracting audio and connecting to Gemini..."))

			ffmpeg_path = ensure_ffmpeg()
			if not ffmpeg_path:
				return

			log.info(f"Live dubbing started: path={path}, source={s_lang}, target={t_lang}")
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			startupinfo.wShowWindow = 0
			CREATE_NO_WINDOW = 0x08000000

			duration_sec = 0
			try:
				proc = subprocess.run(
					[ffmpeg_path, "-i", path],
					stderr=subprocess.PIPE,
					text=True,
					startupinfo=startupinfo,
					creationflags=CREATE_NO_WINDOW,
				)
				m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", proc.stderr)
				if m:
					duration_sec = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
			except Exception as e:
				log.debug(f"Duration probe failed: {e}")
			log.debug(f"Live dubbing duration: {duration_sec:.1f}s")

			model = "gemini-3.5-live-translate-preview"
			api_keys = AIHandler.get_keys("gemini")
			if not api_keys:
				# Translators: Error message when TTS is not supported by the provider
				wx.CallAfter(show_error_dialog, _("No API Keys configured."))
				return

			ws = None
			num_keys = len(api_keys)
			from ..ai.providers.gemini import GeminiHandler

			start_idx = getattr(GeminiHandler, "_working_key_idx", 0)
			from ..utils.media_capture import _MinimalWebSocket

			for i in range(num_keys):
				idx = (start_idx + i) % num_keys
				api_key = api_keys[idx]

				base_host = vision_config.DEFAULT_API_URLS["gemini"].replace("https://", "")
				base_port = 443
				is_ssl = True
				try:
					import urllib.parse

					base = AIHandler.get_base_url("gemini")
					p_base = urllib.parse.urlparse(base)
					if p_base.hostname:
						base_host = p_base.hostname
						base_port = p_base.port or (443 if p_base.scheme == "https" else 80)
						is_ssl = p_base.scheme != "http"
				except Exception as e:
					log.debug(f"Gemini base URL parse failed: {e}")

				ws_path = f"/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={api_key}"

				max_retries = getattr(GeminiHandler, "_max_retries", 3)
				attempt = 0
				while attempt < max_retries:
					ws_candidate = _MinimalWebSocket(base_host, ws_path, port=base_port, is_ssl=is_ssl)
					try:
						ws_candidate.connect()
						ws = ws_candidate
						GeminiHandler._working_key_idx = idx
						break
					except Exception as e:
						err_str = str(e).lower()
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
								x in err_str
								for x in ["daily", "per day", "per_day", "perday", "requestsperday"]
							):
								is_retryable = False
							else:
								is_retryable = True
								if "high demand" in err_str:
									max_retries = max(max_retries, 10)
								else:
									max_retries = max(max_retries, 5)

						if is_retryable and (
							"429" in err_str or "quota" in err_str or "exhausted" in err_str
						):
							match = re.search(r"retry in ([\d\.]+)s", err_str)
							if match:
								try:
									delay = float(match.group(1)) + 0.5
								except Exception as e:
									log.debug(f"Retry delay parse failed: {e}")

						if not is_retryable:
							log.error(f"Live Translate: WebSocket connection failed (Key {idx}): {e}")
							break

						if attempt < max_retries - 1:
							log.warning(
								f"Live Translate: Retryable error (Key {idx}, Attempt {attempt + 1}/{max_retries}). Retrying in {delay}s...",
							)
							time.sleep(delay)
							attempt += 1
							continue
						else:
							break
				if ws:
					break
				if error_contract.is_server_busy_error(err_str):
					break

			if not ws:
				if error_contract.is_server_busy_error(err_str):
					# Translators: Error message shown when Live Translate cannot connect due to server overload or high demand.
					msg = _("The AI service is currently busy. Please try again in a moment.")
				else:
					# Translators: Error message shown when Live Translate cannot connect to the server.
					msg = _("WebSocket connection failed for all available API keys.")
				wx.CallAfter(show_error_dialog, msg)
				return

			target_code = vision_config.TARGET_CODES.get(t_lang, "en")
			swap = nvda_config.conf["VisionAssistant"]["smart_swap"]

			setup_msg = {
				"setup": {
					"model": f"models/{model}",
					"generationConfig": {
						"responseModalities": ["AUDIO"],
						"translationConfig": {
							"targetLanguageCode": target_code,
							"echoTargetLanguage": True if swap else False,
						},
					},
				},
			}
			ws.send_text(json.dumps(setup_msg))

			setup_success = False
			for step in range(5):
				opcode, payload = ws.recv()
				if not payload:
					break
				err_msg = payload.decode("utf-8", "replace")
				if "setupComplete" in err_msg or "setup_complete" in err_msg:
					setup_success = True
					break

			if not setup_success:
				# Translators: Error message shown when the Live translation setup fails.
				msg = _("Failed to setup Live translation session. Error: {error}").format(
					error=err_msg if "err_msg" in locals() else "Unknown",
				)
				wx.CallAfter(show_error_dialog, msg)
				ws.close()
				return

			log.info(f"Live dubbing session ready: model={model}, target_code={target_code}")
			duration_str = ""
			import datetime

			if duration_sec > 0:
				mins = int(duration_sec // 60)
				secs = int(duration_sec % 60)
				finish_time = datetime.datetime.now() + datetime.timedelta(seconds=duration_sec)
				time_str = finish_time.strftime("%I:%M %p")
				if mins > 0:
					# Translators: Status message part showing estimated time remaining and completion time.
					duration_str = _(" (approx. {mins} min {secs} sec, finishing around {time})").format(
						mins=mins,
						secs=secs,
						time=time_str,
					)
				else:
					# Translators: Status message part showing estimated seconds remaining and completion time.
					duration_str = _(" (approx. {secs} sec, finishing around {time})").format(
						secs=secs,
						time=time_str,
					)

			# Translators: Status message when live dubbing is actively streaming
			core.callLater(0, self.report_status, _("Dubbing in progress...") + duration_str)

			ffmpeg_proc = subprocess.Popen(
				[
					ffmpeg_path,
					"-i",
					path,
					"-f",
					"s16le",
					"-acodec",
					"pcm_s16le",
					"-ar",
					"16000",
					"-ac",
					"1",
					"pipe:1",
				],
				stdout=subprocess.PIPE,
				stderr=subprocess.DEVNULL,
				startupinfo=startupinfo,
				creationflags=CREATE_NO_WINDOW,
			)

			def send_audio():
				try:
					start_time = time.time()
					total_bytes = 0
					bytes_per_sec = 32000.0
					while True:
						data = ffmpeg_proc.stdout.read(3200)
						if not data:
							break
						total_bytes += len(data)
						b64_data = base64.b64encode(data).decode("utf-8")
						realtime_msg = {
							"realtimeInput": {
								"mediaChunks": [{"mimeType": "audio/pcm;rate=16000", "data": b64_data}],
							},
						}
						ws.send_text(json.dumps(realtime_msg))

						expected_time = total_bytes / bytes_per_sec
						elapsed = time.time() - start_time
						if expected_time > elapsed:
							time.sleep(expected_time - elapsed)

					time.sleep(2)
					end_msg = {"clientContent": {"turnComplete": True}}
					ws.send_text(json.dumps(end_msg))
				except Exception as e:
					log.error(f"Live Translate Send Audio failed: {e}")
				finally:
					try:
						ffmpeg_proc.terminate()
						ffmpeg_proc.wait(timeout=2)
					except Exception as e:
						log.debug(f"ffmpeg terminate failed: {e}")

			sender_thread = threading.Thread(target=send_audio, daemon=True)
			sender_thread.start()

			base, _ext = os.path.splitext(path)
			bname = os.path.basename(base)
			temp_dir = tempfile.gettempdir()
			out_pcm = os.path.join(temp_dir, bname + "_dubbed.pcm")
			if not hasattr(self, "_temp_files_to_cleanup"):
				self._temp_files_to_cleanup = []
			self._temp_files_to_cleanup.append(out_pcm)

			with open(out_pcm, "wb") as f:
				while True:
					opcode, payload = ws.recv()
					if opcode is None:
						reason = str(ws.close_reason)
						if "1007" not in reason and "1000" not in reason:
							log.error(f"Live Translate: WebSocket closed unexpectedly. Reason: {reason}")
						break
					if opcode == 0x9:
						try:
							ws._send_frame(0xA, payload or b"")
						except Exception as e:
							log.debug(f"WebSocket ping reply failed: {e}")
						continue
					if opcode != 0x1 and opcode != 0x2:
						continue
					try:
						data = json.loads(payload.decode("utf-8", "replace"))
						srv = data.get("serverContent") or data.get("server_content")
						if srv:
							turn = srv.get("modelTurn") or srv.get("model_turn")
							if turn:
								for part in turn.get("parts", []):
									inline = part.get("inlineData") or part.get("inline_data")
									if inline and "data" in inline:
										chunk = base64.b64decode(inline["data"])
										f.write(chunk)

							is_complete = srv.get("turnComplete") or srv.get("turn_complete")
							if is_complete and not sender_thread.is_alive():
								break
					except Exception as e:
						log.debug(f"Live translate payload parse failed: {e}")

			ws.close()
			sender_thread.join(timeout=2)
			try:
				ffmpeg_proc.kill()
			except Exception as e:
				log.debug(f"ffmpeg kill failed: {e}")

			if os.path.getsize(out_pcm) == 0:
				# Translators: Error message shown when live dubbing fails to return any audio
				err_msg = _("Dubbing failed. No audio returned. Check NVDA log for details.")
				wx.CallAfter(
					show_error_dialog,
					err_msg,
				)
				try:
					os.remove(out_pcm)
				except Exception as e:
					log.debug(f"Temp PCM removal failed: {e}")
				return

			temp_mp3 = os.path.join(temp_dir, bname + "_dubbed_temp.mp3")
			self._temp_files_to_cleanup.append(temp_mp3)

			filter_complex = "[0:a]volume=0.35[bg];[bg][1:a]amix=inputs=2:duration=longest:normalize=0"
			proc = subprocess.run(
				[
					ffmpeg_path,
					"-y",
					"-i",
					path,
					"-f",
					"s16le",
					"-ar",
					"24000",
					"-ac",
					"1",
					"-i",
					out_pcm,
					"-filter_complex",
					filter_complex,
					"-ac",
					"2",
					temp_mp3,
				],
				stdout=subprocess.DEVNULL,
				stderr=subprocess.PIPE,
				startupinfo=startupinfo,
				creationflags=CREATE_NO_WINDOW,
			)

			if proc.returncode != 0 or not os.path.exists(temp_mp3):
				err = proc.stderr.decode("utf-8", "ignore") if proc.stderr else "None"
				log.error(
					f"Live Translate mixing failed (Return code: {proc.returncode}). Fallback to simple dubbing. ffmpeg stderr: {err}",
				)
				subprocess.run(
					[ffmpeg_path, "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", out_pcm, "-y", temp_mp3],
					stdout=subprocess.DEVNULL,
					stderr=subprocess.DEVNULL,
					startupinfo=startupinfo,
					creationflags=CREATE_NO_WINDOW,
				)

			try:
				os.remove(out_pcm)
			except Exception as e:
				log.debug(f"Temp PCM removal failed: {e}")

			def _save_file():
				import gui

				default_file = os.path.basename(base) + "_dubbed.mp3"
				# Translators: Dialog title when saving a dubbed media file
				save_msg = _("Save dubbed audio as")
				save_dlg = wx.FileDialog(
					gui.mainFrame,
					message=save_msg,
					defaultDir=os.path.dirname(path),
					defaultFile=default_file,
					wildcard="MP3 Audio (*.mp3)|*.mp3",
					style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
				)
				save_dlg.Raise()
				if save_dlg.ShowModal() == wx.ID_OK:
					import shutil

					out_path = save_dlg.GetPath()
					shutil.move(temp_mp3, out_path)
					# Translators: Message reported when dubbed file is successfully saved
					core.callLater(0, ui.message, _("Dubbed file saved: {path}").format(path=out_path))
				else:
					try:
						os.remove(temp_mp3)
					except Exception as e:
						log.debug(f"Temp MP3 removal failed: {e}")
				save_dlg.Destroy()

			wx.CallAfter(_save_file)
			# Translators: Status message when dubbing process finishes
			core.callLater(0, self.report_status, _("Dubbing finished."))
			log.info("Live dubbing finished")

		except Exception as e:
			log.error(f"Live translate failed: {e}", exc_info=True)
			# Translators: Error message when live translate fails
			core.callLater(0, self.report_status, _("Dubbing failed."))
			wx.CallAfter(show_error_dialog, str(e))
		finally:
			self.current_status = _("Idle")
