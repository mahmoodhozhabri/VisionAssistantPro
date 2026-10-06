# -*- coding: utf-8 -*-
import json
import logging
import base64
from urllib import request
from uuid import uuid4
from .. import vision_config
from ..utils.media_capture import get_proxy_opener

log = logging.getLogger(__name__)


class ChromeOCREngine:
	@staticmethod
	def recognize(image_bytes):
		key = vision_config.CHROME_OCR_KEYS[0]
		url = "https://ckintersect-pa.googleapis.com/v1/intersect/pixels"
		headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0", "x-goog-api-key": key}
		payload = {
			"imageRequests": [
				{
					"engineParameters": [{"ocrParameters": {}}],
					"imageBytes": base64.b64encode(image_bytes).decode("utf-8"),
					"imageId": str(uuid4()),
				},
			],
		}
		try:
			req = request.Request(
				url,
				data=json.dumps(payload).encode("utf-8"),
				headers=headers,
				method="POST",
			)
			opener = get_proxy_opener()
			with opener.open(req, timeout=120) as response:
				if response.status == 200:
					data = json.loads(response.read().decode("utf-8"))
					regions = data["results"][0]["engineResults"][0]["ocrEngine"].get("ocrRegions", [])
					lines = []
					for reg in regions:
						line_text = " ".join([w.get("detectedText", "") for w in reg.get("words", [])])
						if line_text.strip():
							lines.append(line_text)
					return "\n".join(lines)
		except Exception as e:
			log.error(f"Chrome OCR Failed: {e}", exc_info=True)
			return None
		return None
