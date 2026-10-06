# -*- coding: utf-8 -*-
import os
import json
import logging
import base64
from urllib import request, error
from uuid import uuid4

import addonHandler

addonHandler.initTranslation()

import config as nvda_config
from ...utils.media_capture import get_proxy_opener

log = logging.getLogger(__name__)


def _build_file_upload(file_bytes, filename, mime_type, key):
	boundary = f"Boundary-{uuid4()}"
	body = []
	body.append(f"--{boundary}".encode())
	body.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode())
	body.append(f"Content-Type: {mime_type}".encode())
	body.append(b"")
	body.append(file_bytes)
	body.append(f"--{boundary}".encode())
	body.append(b'Content-Disposition: form-data; name="purpose"')
	body.append(b"")
	body.append(b"ocr")
	body.append(f"--{boundary}--".encode())
	body.append(b"")

	upload_headers = {
		"Content-Type": f"multipart/form-data; boundary={boundary}",
		"Authorization": f"Bearer {key}",
		"User-Agent": "Mozilla/5.0",
	}
	return b"\r\n".join(body), upload_headers


class MistralHandler:
	@staticmethod
	def ocr(img_or_pdf_base64, mime_type):
		from ..core import AIHandler

		keys = AIHandler.get_keys("mistral")
		# Translators: Error when no API keys are found in settings
		if not keys:
			return "ERROR:" + _("No API Keys configured.")

		is_pdf = "pdf" in mime_type.lower()
		base_url = AIHandler.get_base_url("mistral").rstrip("/")
		v1_base = base_url if "/v1" in base_url.lower() else f"{base_url}/v1"

		upload_url = f"{v1_base}/files"
		ocr_url = f"{v1_base}/ocr"

		model = nvda_config.conf["VisionAssistant"].get("mistral_ocr_model", "").strip()
		if not model:
			model = "mistral-ocr-latest"

		is_file = False
		try:
			if isinstance(img_or_pdf_base64, str) and os.path.exists(img_or_pdf_base64):
				is_file = True
		except Exception:
			pass

		for key in keys:
			try:
				if is_file:
					with open(img_or_pdf_base64, "rb") as f:
						file_bytes = f.read()
				else:
					file_bytes = base64.b64decode(img_or_pdf_base64)

				upload_data, upload_headers = _build_file_upload(
					file_bytes,
					"document.pdf" if is_pdf else "image.jpg",
					mime_type,
					key,
				)
				req_upload = request.Request(
					upload_url,
					data=upload_data,
					headers=upload_headers,
					method="POST",
				)
				with get_proxy_opener(upload_url).open(req_upload, timeout=120) as r:
					upload_res = json.loads(r.read().decode())
					file_id = upload_res.get("id")

				if not file_id:
					raise ValueError("File upload failed to return an ID")

				payload = {"model": model, "document": {"type": "file", "file_id": file_id}}

				ocr_headers = {
					"Authorization": f"Bearer {key}",
					"Content-Type": "application/json",
					"User-Agent": "Mozilla/5.0",
				}

				req_ocr = request.Request(
					ocr_url,
					data=json.dumps(payload).encode(),
					headers=ocr_headers,
					method="POST",
				)
				with get_proxy_opener(ocr_url).open(req_ocr, timeout=120) as r:
					res = json.loads(r.read().decode())

					try:
						delete_url = f"{v1_base}/files/{file_id}"
						req_del = request.Request(
							delete_url,
							headers={"Authorization": f"Bearer {key}"},
							method="DELETE",
						)
						with get_proxy_opener(delete_url).open(req_del, timeout=10):
							pass
					except Exception as e:
						log.warning(f"Mistral delete file failed: {e}")

					return "[[[PAGE_SEP]]]".join([pg.get("markdown", "") for pg in res.get("pages", [])])

			except error.HTTPError as e:
				if (e.code == 429 or e.code >= 500) and key != keys[-1]:
					continue
				return f"ERROR: {e.code}"
			except Exception as e:
				if key == keys[-1]:
					return f"ERROR: {str(e)}"
				continue

	@staticmethod
	def upload_to_mistral_for_chat(file_path):
		from ..core import AIHandler

		keys = AIHandler.get_keys("mistral")
		# Translators: Error message when TTS is not supported by the provider
		if not keys:
			return None, "ERROR:" + _("No API Keys configured.")

		base_url = AIHandler.get_base_url("mistral").rstrip("/")
		v1_base = base_url if "/v1" in base_url.lower() else f"{base_url}/v1"
		upload_url = f"{v1_base}/files"

		for key in keys:
			try:
				with open(file_path, "rb") as f:
					file_bytes = f.read()

				upload_data, upload_headers = _build_file_upload(
					file_bytes,
					os.path.basename(file_path),
					"application/pdf",
					key,
				)
				req_upload = request.Request(
					upload_url,
					data=upload_data,
					headers=upload_headers,
					method="POST",
				)
				opener = get_proxy_opener(upload_url)
				with opener.open(req_upload, timeout=3600) as r:
					upload_res = json.loads(r.read().decode())
					file_id = upload_res.get("id")

				if not file_id:
					continue

				signed_url_endpoint = f"{v1_base}/files/{file_id}/url?expiry=24"
				req_signed = request.Request(
					signed_url_endpoint,
					headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
				)
				with opener.open(req_signed, timeout=30) as r:
					signed_res = json.loads(r.read().decode())
					signed_url = signed_res.get("url")

				if signed_url:
					return file_id, signed_url

			except Exception as e:
				log.error(f"Mistral upload failed: {e}")
				continue

		# Translators: Error message shown when uploading a video file fails.
		return None, "ERROR:" + _("Upload failed.")

	@staticmethod
	def delete_mistral_file(file_id):
		from ..core import AIHandler

		keys = AIHandler.get_keys("mistral")
		if not keys or not file_id:
			return
		base_url = AIHandler.get_base_url("mistral").rstrip("/")
		v1_base = base_url if "/v1" in base_url.lower() else f"{base_url}/v1"
		delete_url = f"{v1_base}/files/{file_id}"

		for key in keys:
			try:
				req_del = request.Request(
					delete_url,
					headers={"Authorization": f"Bearer {key}"},
					method="DELETE",
				)
				with get_proxy_opener(delete_url).open(req_del, timeout=10):
					break
			except Exception as e:
				log.warning(f"Mistral delete failed: {e}")
