# -*- coding: utf-8 -*-
import json
import logging
import time
import base64
from urllib import request

import config as nvda_config

from ...utils.media_capture import get_proxy_opener

log = logging.getLogger(__name__)


class MinimaxHandler:
	@staticmethod
	def get_voices():
		from ..core import AIHandler

		try:
			cache = nvda_config.conf["VisionAssistant"].get("minimax_voices_cache", "")
			cache_time_raw = nvda_config.conf["VisionAssistant"].get("minimax_voices_cache_time", 0)
			try:
				cache_time = float(cache_time_raw)
			except (TypeError, ValueError):
				cache_time = 0
			if cache and (time.time() - cache_time < 86400):
				voices = []
				for entry in cache.split(","):
					if "|" in entry:
						vid, vname = entry.split("|", 1)
						voices.append((vid, vname))
				if voices:
					log.debug(f"Using cached MiniMax voices ({len(voices)} entries)")
					return voices

			base = AIHandler.get_base_url("minimax")
			url = f"{base.rstrip('/')}/get_voice"
			keys = AIHandler.get_keys("minimax")
			if not keys:
				return []
			key = keys[0]
			payload = json.dumps({"voice_type": "system"}).encode("utf-8")
			req = request.Request(
				url,
				data=payload,
				headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
			)
			with get_proxy_opener(url).open(req, timeout=30) as r:
				resp = json.loads(r.read().decode("utf-8"))
				system_voices = resp.get("system_voice", [])
				if not system_voices:
					log.warning("MiniMax /get_voice returned no system_voice list")
					return []
				voices = []
				storage_parts = []
				for v in system_voices:
					vid = v.get("voice_id", "")
					vname = v.get("voice_name", vid)
					if vid:
						voices.append((vid, vname))
						storage_parts.append(f"{vid}|{vname}")
				if voices:
					nvda_config.conf["VisionAssistant"]["minimax_voices_cache"] = ",".join(storage_parts)
					nvda_config.conf["VisionAssistant"]["minimax_voices_cache_time"] = int(time.time())
					log.debug(f"Fetched and cached {len(voices)} MiniMax voices")
					return voices
				return []
		except Exception as e:
			log.warning(f"Failed to fetch MiniMax voices: {e}")
			return []

	@staticmethod
	def generate_speech(text, voice_name, model_override=None):
		from ..core import AIHandler

		keys = AIHandler.get_keys("minimax")
		if not keys:
			return "ERROR: No API Keys configured.", False

		minimax_base = AIHandler.get_base_url("minimax").rstrip("/") or "https://api.minimax.io/v1"
		minimax_tts_url = f"{minimax_base}/t2a_v2"
		model = (
			nvda_config.conf["VisionAssistant"].get("minimax_tts_model", "speech-2.8-hd").strip()
			or "speech-2.8-hd"
		)
		minimax_voice = (
			voice_name
			if voice_name
			else nvda_config.conf["VisionAssistant"]["minimax_tts_voice"].strip()
			or "English_expressive_narrator"
		)
		minimax_payload = {
			"model": model,
			"text": text,
			"voice_setting": {"voice_id": minimax_voice, "speed": 1.0, "vol": 1.0, "pitch": 0},
			"audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
		}
		for key in keys:
			try:
				headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
				if key and key.strip():
					headers["Authorization"] = f"Bearer {key}"
				req = request.Request(
					minimax_tts_url,
					data=json.dumps(minimax_payload).encode(),
					headers=headers,
				)
				with get_proxy_opener(minimax_tts_url).open(req, timeout=600) as r:
					resp_json = json.loads(r.read().decode("utf-8"))
					hex_audio = resp_json.get("data", {}).get("audio", "")
					if not hex_audio:
						return "ERROR: MiniMax TTS returned no audio data.", False
					audio_bytes = bytes.fromhex(hex_audio)
					return base64.b64encode(audio_bytes).decode("utf-8"), False
			except Exception as e:
				if key == keys[-1]:
					return f"ERROR: {str(e)}", False
				continue
