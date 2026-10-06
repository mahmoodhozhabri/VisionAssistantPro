# -*- coding: utf-8 -*-
import json
import logging
import core
import ui
import addonHandler
import config as nvda_config

from .. import vision_config
from ..ai.core import AIHandler, PROVIDERS, provider_key_name, provider_model_name

addonHandler.initTranslation()
log = logging.getLogger(__name__)

_TOGGLE_SETTINGS = {
	"Live Direct Output (No Window)": ("live_direct_output", False),
	"Visual CAPTCHA Solver": ("enable_visual_captcha_solver", True),
	"Image Description in OCR": ("describe_images_ocr", True),
	"Document Export Page Numbers": ("document_export_page_numbers", True),
	"Copy AI responses to clipboard": ("copy_to_clipboard", False),
	"Direct Output (No Chat Window)": ("skip_chat_dialog", False),
	"Clean Markdown in Chat": ("clean_markdown_chat", True),
	"Save Chats to History": ("save_chat_history", True),
	"Save Documents to History": ("save_document_history", True),
	"Smart Swap": ("smart_swap", True),
}

_LANGUAGE_SETTINGS = {
	"Source Language": ("source_language", vision_config.SOURCE_LIST),
	"Target Language": ("target_language", vision_config.TARGET_LIST),
	"AI Response Language": ("ai_response_language", vision_config.TARGET_LIST),
}


def _quick_settings_categories():
	return [
		"AI Provider",
		"AI Model",
		"TTS Voice",
		"OCR Model",
		"STT Model",
		"TTS Model",
		"Operator / CAPTCHA Model",
		"Video Model",
		"Live Model",
		"Live Direct Output (No Window)",
		"Gemini Live Audio Output Device",
		"Source Language",
		"Target Language",
		"AI Response Language",
		"Visual CAPTCHA Solver",
		"Text CAPTCHA Method",
		"OCR Engine",
		"Image Description in OCR",
		"Document Export Page Numbers",
		"Copy AI responses to clipboard",
		"Direct Output (No Chat Window)",
		"Clean Markdown in Chat",
		"Save Chats to History",
		"Save Documents to History",
		"Smart Swap",
	]


_MODEL_CATEGORY_TASKS = {
	"AI Model": "main",
	"OCR Model": "ocr",
	"STT Model": "stt",
	"TTS Model": "tts",
	"Operator / CAPTCHA Model": "operator",
	"Video Model": "video",
	"Live Model": "live",
}


def _model_conf_key(category, provider):
	if category == "AI Model":
		return provider_model_name(provider)
	return f"{provider}_{category.split(' ')[0].lower()}_model"


def _parse_models_list(raw):
	if not raw:
		return None
	try:
		return [m["id"] for m in json.loads(raw)]
	except Exception:
		return [part.split("|")[0] for part in raw.split(",") if "|" in part]


class QuickSettingsMixin:
	def _get_models_for_provider(self, p):
		conf = nvda_config.conf["VisionAssistant"]
		if p == "gemini":
			models = _parse_models_list(conf.get("gemini_models_list", ""))
			return models if models is not None else [m[1] for m in vision_config.MODELS]
		elif p in ("openai", "mistral", "groq", "custom"):
			models = _parse_models_list(conf.get(f"{p}_models_list", ""))
			return models if models is not None else []
		elif p == "minimax":
			return ["MiniMax-M3"]
		return []

	def _get_quick_setting_value(self, c):
		conf = nvda_config.conf["VisionAssistant"]
		if c == "AI Provider":
			return conf["active_provider"].capitalize()
		elif c == "OCR Engine":
			cur = conf["ocr_engine"]
			for name, val in vision_config.OCR_ENGINES:
				if val == cur:
					return name
			return cur
		elif c == "TTS Voice":
			return conf["tts_voice"]
		elif c in _LANGUAGE_SETTINGS:
			return vision_config.get_lang_name(_LANGUAGE_SETTINGS[c][0])
		elif c in _TOGGLE_SETTINGS:
			key, default = _TOGGLE_SETTINGS[c]
			if conf.get(key, default):
				# Translators: Value representing the ON state for a toggle setting (e.g., in quick settings).
				return _("On")
			# Translators: Value representing the OFF state for a toggle setting (e.g., in quick settings).
			return _("Off")
		elif c == "Text CAPTCHA Method":
			return (
				_("Full Screen")
				if conf.get("captcha_mode", "navigator") == "fullscreen"
				else _("Navigator Object")
			)
		elif c == "Gemini Live Audio Output Device":
			cur_id = conf.get("live_output_device", "")
			devs = vision_config.get_audio_output_devices()
			for d_id, d_name in devs:
				if d_id == cur_id:
					return d_name
			return devs[0][1] if devs else _("Default")

		p = conf["active_provider"]
		return conf.get(_model_conf_key(c, p), "")

	def _announce_current_quick_setting(self, value_only=False):
		cats = _quick_settings_categories()
		idx = getattr(self, "_quick_settings_idx", 0)
		c = cats[idx]
		# Translators: Value announced in quick settings when the setting has no value selected yet.
		val = self._get_quick_setting_value(c) or _("Default")
		if value_only:
			core.callLater(0, ui.message, val)
		else:
			# Translators: Announced when navigating to AI Model quick settings
			msg = _("{setting}, Current: {val}. Use left and right arrows to change.").format(
				setting=c,
				val=val,
			)
			core.callLater(0, ui.message, msg)

	def _change_quick_setting(self, direction):
		conf = nvda_config.conf["VisionAssistant"]
		cats = _quick_settings_categories()
		idx = getattr(self, "_quick_settings_idx", 0)
		c = cats[idx]

		if c == "AI Provider":
			providers = PROVIDERS
			cur = conf["active_provider"]
			try:
				i = providers.index(cur)
			except Exception:
				i = 0
			for _i in range(len(providers)):
				i = (i + direction) % len(providers)
				p = providers[i]
				if p == "custom":
					break
				k = provider_key_name(p)
				if conf.get(k, "").strip():
					break
			conf["active_provider"] = providers[i]
		elif c in _LANGUAGE_SETTINGS:
			key, lang_list = _LANGUAGE_SETTINGS[c]
			opts = [x[1] for x in lang_list]
			cur = conf[key]
			try:
				i = opts.index(cur)
			except Exception:
				i = 0
			i = (i + direction) % len(opts)
			conf[key] = opts[i]
		elif c == "OCR Engine":
			opts = [val for name, val in vision_config.OCR_ENGINES]
			cur = conf["ocr_engine"]
			try:
				i = opts.index(cur)
			except Exception:
				i = 0
			i = (i + direction) % len(opts)
			conf["ocr_engine"] = opts[i]
		elif c == "TTS Voice":
			opts = [v[0] for v in vision_config.GEMINI_VOICES] + [v[0] for v in vision_config.OPENAI_VOICES]
			unique_opts = list(dict.fromkeys(opts))
			cur = conf["tts_voice"]
			try:
				i = unique_opts.index(cur)
			except Exception:
				i = 0
			i = (i + direction) % len(unique_opts)
			conf["tts_voice"] = unique_opts[i]
		elif c in _TOGGLE_SETTINGS:
			key, default = _TOGGLE_SETTINGS[c]
			conf[key] = not conf.get(key, default)
		elif c == "Text CAPTCHA Method":
			mode = conf.get("captcha_mode", "navigator")
			conf["captcha_mode"] = "fullscreen" if mode == "navigator" else "navigator"
		elif c == "Gemini Live Audio Output Device":
			devs = vision_config.get_audio_output_devices()
			if devs:
				opts = [d[0] for d in devs]
				cur = conf.get("live_output_device", "")
				try:
					i = opts.index(cur)
				except Exception:
					i = 0
				i = (i + direction) % len(opts)
				new_dev = opts[i]
				conf["live_output_device"] = new_dev
				if getattr(self, "live_session", None):
					try:
						self.live_session.set_output_device(new_dev)
					except Exception as e:
						log.debug(f"Live device change via quick settings failed: {e}")
		else:
			p = conf["active_provider"]
			raw_models = self._get_models_for_provider(p)
			task = _MODEL_CATEGORY_TASKS.get(c, "main")
			filtered = AIHandler.filter_models(p, [(m, m) for m in raw_models], task=task)
			models = [m[0] for m in filtered]
			if not models and not raw_models:
				core.callLater(
					0,
					ui.message,
					# Translators: Warning when models list is not fetched
					_("No models fetched for {provider}. Please update models list from settings.").format(
						provider=p.capitalize(),
					),
				)
				return
			if c != "AI Model":
				models.insert(0, "")
				conf["advanced_model_routing"] = True
			k = _model_conf_key(c, p)
			cur = conf.get(k, "")
			try:
				i = models.index(cur)
			except Exception:
				i = 0
			i = (i + direction) % len(models)
			conf[k] = models[i]

		self._announce_current_quick_setting(value_only=True)

	def script_layerDown(self, gesture):
		self._quick_settings_idx = (getattr(self, "_quick_settings_idx", 0) + 1) % len(
			_quick_settings_categories(),
		)
		self._announce_current_quick_setting()

	script_layerDown.keep_layer_alive = True

	def script_layerUp(self, gesture):
		self._quick_settings_idx = (getattr(self, "_quick_settings_idx", 0) - 1) % len(
			_quick_settings_categories(),
		)
		self._announce_current_quick_setting()

	script_layerUp.keep_layer_alive = True

	def script_layerRight(self, gesture):
		self._change_quick_setting(1)

	script_layerRight.keep_layer_alive = True

	def script_layerLeft(self, gesture):
		self._change_quick_setting(-1)

	script_layerLeft.keep_layer_alive = True
