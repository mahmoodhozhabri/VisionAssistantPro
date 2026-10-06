# -*- coding: utf-8 -*-
import json
import logging
from urllib import request
from urllib.parse import quote
from ..utils.media_capture import get_proxy_opener

log = logging.getLogger(__name__)


class GoogleTranslator:
	@staticmethod
	def translate(text, target_lang):
		try:
			url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={quote(text)}"
			opener = get_proxy_opener()
			req = request.Request(url)
			with opener.open(req, timeout=15) as r:
				res = json.loads(r.read().decode("utf-8"))
				if res and isinstance(res, list) and res[0]:
					translated_parts = [sentence[0] for sentence in res[0] if sentence[0]]
					return "".join(translated_parts).strip()
		except Exception as e:
			log.error(f"GoogleTranslator failed, falling back to original text: {e}")
		return text
