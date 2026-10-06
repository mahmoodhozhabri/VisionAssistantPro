# -*- coding: utf-8 -*-
import json
import logging
import base64
import uuid
from urllib import request, error

import config as nvda_config
import addonHandler

from ...utils import error_contract
from ...utils.media_capture import get_proxy_opener
from ...utils.system import strip_thinking_tags

log = logging.getLogger(__name__)

addonHandler.initTranslation()


class OpenAIHandler:
	@staticmethod
	def call(prompt, attachments=None, json_mode=False, task="chat"):
		from ..core import AIHandler

		p = nvda_config.conf["VisionAssistant"]["active_provider"]
		keys = AIHandler.get_keys(p)
		if not keys and p != "custom":
			# Translators: Error message when TTS is not supported by the provider
			return "ERROR:" + _("No API Keys configured.")
		if not keys:
			keys = [""]

		is_audio = (
			any(a.get("mime_type", "").startswith("audio/") for a in attachments) if attachments else False
		)
		is_image = (
			any(a.get("mime_type", "").startswith("image/") for a in attachments) if attachments else False
		)

		custom_audio_chat = (
			p == "custom"
			and is_audio
			and not (
				nvda_config.conf["VisionAssistant"].get("use_advanced_endpoints", False)
				and nvda_config.conf["VisionAssistant"].get("custom_stt_url", "").strip()
			)
		)

		if is_audio and not custom_audio_chat:
			audio_att = next(a for a in attachments if a.get("mime_type", "").startswith("audio/"))
			url = AIHandler.get_endpoint("stt")
			model = "whisper-1"
			if p == "groq":
				model = "whisper-large-v3-turbo"
			elif p == "mistral":
				model = "voxtral-mini-latest"
			elif p == "minimax":
				model = nvda_config.conf["VisionAssistant"]["minimax_stt_model"].strip() or "asr-01"
			if p == "custom":
				model = (
					nvda_config.conf["VisionAssistant"]["custom_stt_model"].strip()
					or nvda_config.conf["VisionAssistant"]["custom_model_name"].strip()
					or model
				)
			elif nvda_config.conf["VisionAssistant"].get("advanced_model_routing", False):
				adv_stt = nvda_config.conf["VisionAssistant"].get(f"{p}_stt_model", "").strip()
				if adv_stt:
					model = adv_stt

			for key in keys:
				res = AIHandler._transcribe_helper(key, audio_att, url, model)
				if not error_contract.is_ai_error(res):
					return res
			return res

		for key in keys:
			try:
				current_task = "vision" if is_image and task == "chat" else task
				url = AIHandler.get_endpoint(current_task)

				if p == "custom":
					model = nvda_config.conf["VisionAssistant"]["custom_model_name"].strip()
					if current_task in ["vision", "ocr"]:
						model = nvda_config.conf["VisionAssistant"]["custom_ocr_model"].strip()
					if not model:
						model = nvda_config.conf["VisionAssistant"]["custom_model_name"].strip()
				else:
					m_key = f"{p}_model_name"
					model = nvda_config.conf["VisionAssistant"].get(m_key, "")
					if nvda_config.conf["VisionAssistant"].get("advanced_model_routing", False):
						adv_model = (
							nvda_config.conf["VisionAssistant"].get(f"{p}_{current_task}_model", "").strip()
						)
						if adv_model:
							model = adv_model

				if not model:
					return "ERROR: Model name is empty."

				if isinstance(prompt, str):
					if attachments:
						contents = []
						if prompt:
							contents.append({"type": "text", "text": prompt})
						for att in attachments:
							if "data" in att and att.get("mime_type", "").startswith("image/"):
								contents.append(
									{
										"type": "image_url",
										"image_url": {"url": f"data:{att['mime_type']};base64,{att['data']}"},
									},
								)
							elif (
								custom_audio_chat
								and "data" in att
								and att.get("mime_type", "").startswith("audio/")
							):
								audio_format = att["mime_type"].split("/", 1)[-1].replace("mpeg", "mp3")
								contents.append(
									{
										"type": "input_audio",
										"input_audio": {
											"data": att["data"],
											"format": audio_format,
										},
									},
								)
							elif "file_uri" in att:
								uri_val = att["file_uri"]
								mime_str = att.get("mime_type", "")
								if uri_val.startswith(("http://", "https://")):
									if mime_str.startswith("image/"):
										contents.append({"type": "image_url", "image_url": {"url": uri_val}})
									else:
										contents.append({"type": "file_url", "file_url": {"url": uri_val}})
								else:
									contents.append({"type": "file_id", "file_id": uri_val})
						messages = [{"role": "user", "content": contents}]
					else:
						messages = [{"role": "user", "content": prompt}]
				else:
					messages = prompt

				temp = nvda_config.conf["VisionAssistant"].get("ai_temperature", 0.7)
				payload = {"model": model, "messages": messages, "temperature": temp, "stream": False}
				if json_mode:
					payload["response_format"] = {"type": "json_object"}

				headers = {
					"Content-Type": "application/json",
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
				}
				if key and key.strip():
					headers["Authorization"] = f"Bearer {key}"

				req = request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
				with get_proxy_opener(url).open(req, timeout=180) as r:
					res = json.loads(r.read().decode("utf-8"))
					if isinstance(res, dict):
						if "choices" in res and res["choices"]:
							content = res["choices"][0]["message"]["content"]
							if content:
								content = strip_thinking_tags(content)
							return content
						elif "error" in res:
							err_val = res["error"]
							err_msg = err_val.get("message") if isinstance(err_val, dict) else str(err_val)
							return f"ERROR: {err_msg}"
						elif "message" in res:
							return f"ERROR: {res['message']}"
						elif "detail" in res:
							return f"ERROR: {res['detail']}"
						elif "msg" in res:
							return f"ERROR: {res['msg']}"
						elif "error_message" in res:
							return f"ERROR: {res['error_message']}"
						elif "choices" in res and not res["choices"]:
							# Translators: Error prefix shown when the AI response is blocked by safety filters.
							return "ERROR: " + _("Blocked by AI Safety Filters: ")
					# Translators: Error message shown when the AI returns an unknown error
					return "ERROR: " + _("AI Error") + f" (Response: {res})"
			except error.HTTPError as e:
				try:
					raw_err = e.read().decode("utf-8")
					err_json = json.loads(raw_err)
					err_val = err_json.get("error")
					if isinstance(err_val, dict):
						server_msg = err_val.get("message")
					else:
						server_msg = err_val or err_json.get("message")
					if server_msg:
						if key == keys[-1]:
							return f"ERROR: {server_msg}"
						continue
				except Exception as ex:
					log.warning(f"Error parsing raw error JSON: {ex}")
				if key == keys[-1]:
					return f"ERROR: {str(e)}"
				continue
			except Exception as e:
				if key == keys[-1]:
					return f"ERROR: {str(e)}"
				continue

	@staticmethod
	def _transcribe_helper(key, audio_att, url, model_name):
		try:
			boundary = f"Boundary-{uuid.uuid4()}"
			body = []
			body.append(f"--{boundary}".encode())
			body.append(b'Content-Disposition: form-data; name="file"; filename="audio.wav"')
			body.append(f"Content-Type: {audio_att['mime_type']}".encode())
			body.append(b"")
			body.append(base64.b64decode(audio_att["data"]))
			body.append(f"--{boundary}".encode())
			body.append(b'Content-Disposition: form-data; name="model"')
			body.append(b"")
			body.append(model_name.encode())
			body.append(f"--{boundary}--".encode())
			body.append(b"")
			headers = {
				"Content-Type": f"multipart/form-data; boundary={boundary}",
				"User-Agent": "Mozilla/5.0",
			}
			if key and key.strip():
				headers["Authorization"] = f"Bearer {key}"
			req = request.Request(url, data=b"\r\n".join(body), headers=headers)
			with get_proxy_opener(url).open(req, timeout=60) as r:
				return json.loads(r.read().decode())["text"]
		except Exception as e:
			log.error(f"Transcription helper failed: {e}")
			# Translators: Error message when speech-to-text fails.
			return "ERROR: " + _("Transcription Failed") + f" ({str(e)})"

	@staticmethod
	def generate_speech(text, voice_name, model_override=None):
		from ..core import AIHandler

		p = nvda_config.conf["VisionAssistant"]["active_provider"]
		keys = AIHandler.get_keys(p)
		if not keys and p != "custom":
			return "ERROR:" + _("No API Keys configured."), False
		if not keys:
			keys = [""]
		url = AIHandler.get_endpoint("tts")
		m_key = "model_name" if p == "gemini" else f"{p}_model_name"
		model = model_override or nvda_config.conf["VisionAssistant"].get(m_key, "")

		if p == "custom":
			model = nvda_config.conf["VisionAssistant"]["custom_tts_model"].strip() or "tts-1"
		elif nvda_config.conf["VisionAssistant"].get("advanced_model_routing", False):
			adv_tts = nvda_config.conf["VisionAssistant"].get(f"{p}_tts_model", "").strip()
			if adv_tts:
				model = adv_tts
			elif p == "openai":
				model = "tts-1"
		elif p == "openai":
			model = "tts-1"

		payload = {"model": model, "input": text, "voice": voice_name.lower(), "response_format": "mp3"}
		for key in keys:
			try:
				headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
				if key and key.strip():
					headers["Authorization"] = f"Bearer {key}"
				req = request.Request(url, data=json.dumps(payload).encode(), headers=headers)
				with get_proxy_opener(url).open(req, timeout=600) as r:
					return base64.b64encode(r.read()).decode("utf-8"), False
			except Exception as e:
				if key == keys[-1]:
					return f"ERROR: {str(e)}", False
				continue
