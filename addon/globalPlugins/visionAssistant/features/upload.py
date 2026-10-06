# -*- coding: utf-8 -*-
import os
import json
import logging
import wx
from uuid import uuid4
from urllib import request
import config as nvda_config
import addonHandler

from ..ai.core import AIHandler
from ..ai.providers.gemini import GeminiHandler
from ..utils.media_capture import get_proxy_opener
from ..utils.system import show_error_dialog

log = logging.getLogger(__name__)

addonHandler.initTranslation()


class UploadMixin:
	def _upload_file_to_gemini(self, file_path, mime_type, silent=False, abort_checker=None, api_key=None):
		p = nvda_config.conf["VisionAssistant"]["active_provider"]
		keys = AIHandler.get_keys(p)
		if not keys:
			return None

		if not AIHandler.is_gemini():
			url = AIHandler.get_endpoint("upload")
			boundary = "Boundary-" + uuid4().hex
			with open(file_path, "rb") as f:
				data = f.read()
			body = []
			body.append(f"--{boundary}".encode())
			body.append('Content-Disposition: form-data; name="purpose"'.encode())
			body.append(b"")
			body.append(b"ocr")
			body.append(f"--{boundary}".encode())
			body.append(
				f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(file_path)}"'.encode(),
			)
			body.append(f"Content-Type: {mime_type}".encode())
			body.append(b"")
			body.append(data)
			body.append(f"--{boundary}--".encode())
			body.append(b"")

			for key in keys:
				if abort_checker and abort_checker():
					return None
				try:
					req = request.Request(
						url,
						data=b"\r\n".join(body),
						headers={
							"Authorization": f"Bearer {key}",
							"Content-Type": f"multipart/form-data; boundary={boundary}",
						},
						method="POST",
					)
					with get_proxy_opener().open(req, timeout=3600) as r:
						res = json.loads(r.read().decode())
						return res.get("id") or res.get("name")
				except Exception as e:
					log.warning(f"Upload to mistral/openai failed: {e}")
					continue
			return None

		if not api_key:
			g_keys = GeminiHandler._get_api_keys()
			if not g_keys:
				return None
			api_key = g_keys[GeminiHandler._working_key_idx % len(g_keys)]

		try:
			uri, _dur = GeminiHandler._upload_file_common(
				file_path,
				mime_type,
				api_key,
				abort_checker=abort_checker,
			)
			return uri
		except Exception as e:
			if abort_checker and abort_checker():
				log.debug("File upload aborted by user")
				return None
			err_msg = GeminiHandler._handle_error(e) if hasattr(GeminiHandler, "_handle_error") else str(e)
			# Translators: Message of a dialog which may pop up while performing an AI call
			msg = _("File Upload Error: {error}").format(error=err_msg)
			self.report_status(msg)
			if not silent:
				wx.CallAfter(show_error_dialog, msg)
			return None

	def _get_gemini_file_uri(self, file_path, mime_type, api_key=None):
		if not api_key:
			g_keys = GeminiHandler._get_api_keys()
			if not g_keys:
				return None
			api_key = g_keys[GeminiHandler._working_key_idx % len(g_keys)]
		cache = getattr(self, "_gemini_file_cache", None)
		if cache is None:
			from .. import vision_config
			from ..utils.storage import GeminiFileCache

			cache = self._gemini_file_cache = GeminiFileCache(vision_config.GEMINI_FILE_CACHE_FILE)
		uri = cache.get(file_path, api_key)
		if uri:
			return uri
		uri = self._upload_file_to_gemini(file_path, mime_type, api_key=api_key)
		if uri and "files/" in uri:
			cache.put(file_path, api_key, uri)
		return uri
