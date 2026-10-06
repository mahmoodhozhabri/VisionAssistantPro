# -*- coding: utf-8 -*-
import json
import logging
import re
from functools import wraps

import addonHandler
import config as nvda_config

from . import vision_config

log = logging.getLogger(__name__)

addonHandler.initTranslation()


def _normalize_required_markers(markers):
	if not isinstance(markers, (list, tuple)):
		return []
	normalized = []
	for marker in markers:
		if not isinstance(marker, str):
			continue
		marker = marker.strip()
		if marker and marker not in normalized:
			normalized.append(marker)
	return normalized


def _normalize_required_regex_checks(regex_checks):
	if not isinstance(regex_checks, (list, tuple)):
		return []
	normalized = []
	seen = set()
	for regex_item in regex_checks:
		if isinstance(regex_item, dict):
			pattern = regex_item.get("pattern")
			description = regex_item.get("description")
		else:
			pattern = regex_item
			description = ""
		if not isinstance(pattern, str):
			continue
		pattern = pattern.strip()
		if not pattern or pattern in seen:
			continue
		seen.add(pattern)
		if not isinstance(description, str):
			description = ""
		description = description.strip() or pattern
		normalized.append({"pattern": pattern, "description": description})
	return normalized


def get_builtin_default_prompts():
	builtins = []
	for item in vision_config.DEFAULT_SYSTEM_PROMPTS:
		p = str(item["prompt"]).strip()
		guarded = bool(item.get("guarded"))
		builtins.append(
			{
				"key": item["key"],
				"section": item["section"],
				"label": item["label"],
				"display_label": f"{item['section']} - {item['label']}",
				"internal": bool(item.get("internal")),
				"guarded": guarded,
				"guardedFeatureLabel": str(item.get("guardedFeatureLabel", item["label"])).strip()
				if guarded
				else "",
				"requiredMarkers": _normalize_required_markers(item.get("requiredMarkers")),
				"requiredRegex": _normalize_required_regex_checks(item.get("requiredRegex")),
				"prompt": p,
				"default": p,
			},
		)
	return builtins


def get_builtin_default_prompt_map():
	return {item["key"]: item for item in get_builtin_default_prompts()}


_HOTKEY_MODIFIER_ALIASES = {"ctrl": "control", "win": "windows", "insert": "nvda"}
_HOTKEY_ALLOWED_MODIFIERS = frozenset({"alt", "shift", "control", "nvda", "windows"})
_HOTKEY_MODIFIER_DISPLAY = {
	"control": "Ctrl",
	"shift": "Shift",
	"alt": "Alt",
	"nvda": "NVDA",
	"windows": "Win",
	"leftcontrol": "Left Ctrl",
	"rightcontrol": "Right Ctrl",
	"leftshift": "Left Shift",
	"rightshift": "Right Shift",
	"leftalt": "Left Alt",
	"rightalt": "Right Alt",
	"leftwindows": "Left Win",
	"rightwindows": "Right Win",
}
_HOTKEY_MODIFIER_DISPLAY_TO_SPEC = {v.lower(): k for k, v in _HOTKEY_MODIFIER_DISPLAY.items()}


def _normalize_hotkey(value):
	if not isinstance(value, str):
		return ""
	spec = value.strip().lower()
	if not spec:
		return ""
	parts = spec.split("+")
	if not parts:
		return ""
	key = parts[-1]
	if not re.fullmatch(r"[a-z0-9]|f(?:1[0-2]|[1-9])", key):
		return ""
	modifiers = []
	for token in parts[:-1]:
		token = _HOTKEY_MODIFIER_ALIASES.get(token, token)
		if token not in _HOTKEY_ALLOWED_MODIFIERS:
			return ""
		if token not in modifiers:
			modifiers.append(token)
	if not modifiers:
		return key
	modifiers.sort()
	return "+".join(modifiers) + "+" + key


def _format_hotkey_display(hotkey):
	if not hotkey:
		return ""
	parts = hotkey.split("+")
	key = parts[-1].upper()
	display_parts = [_HOTKEY_MODIFIER_DISPLAY.get(token, token.title()) for token in parts[:-1]]
	return "+".join(display_parts + [key])


_HOTKEY_MODIFIER_VKS = {
	"control": 0x11,
	"shift": 0x10,
	"alt": 0x12,
	"windows": 0x5B,
	"leftcontrol": 0xA2,
	"rightcontrol": 0xA3,
	"leftshift": 0xA0,
	"rightshift": 0xA1,
	"leftalt": 0xA4,
	"rightalt": 0xA5,
	"leftwindows": 0x5B,
	"rightwindows": 0x5C,
}
_NVDA_VK_CANDIDATES = (0x2D, 0x14)


def normalize_ptt_key(value):
	if not isinstance(value, str):
		return ""
	spec = _normalize_hotkey(value)
	if spec:
		return spec
	token = value.strip().lower()
	token = _HOTKEY_MODIFIER_DISPLAY_TO_SPEC.get(token, token)
	token = _HOTKEY_MODIFIER_ALIASES.get(token, token)
	if token in _HOTKEY_MODIFIER_VKS:
		return token
	return ""


def ptt_key_display(value):
	spec = normalize_ptt_key(value)
	if not spec:
		return ""
	if spec in _HOTKEY_MODIFIER_VKS:
		return _HOTKEY_MODIFIER_DISPLAY.get(spec, spec.title())
	return _format_hotkey_display(spec)


def hotkey_spec_to_vks(value):
	spec = normalize_ptt_key(value)
	if not spec:
		return None
	parts = spec.split("+")
	key = parts[-1]
	if key in _HOTKEY_MODIFIER_VKS:
		return (None, [_HOTKEY_MODIFIER_VKS[key]], False)
	if key.startswith("f") and len(key) > 1:
		main_vk = 0x6F + int(key[1:])
	else:
		main_vk = ord(key.upper())
	mods = []
	needs_nvda = False
	for token in parts[:-1]:
		if token == "nvda":
			needs_nvda = True
		elif token in _HOTKEY_MODIFIER_VKS:
			vk = _HOTKEY_MODIFIER_VKS[token]
			if vk not in mods:
				mods.append(vk)
	return (main_vk, mods, needs_nvda)


_VALID_FEEDBACK_BEHAVIORS = frozenset(
	{
		"global",
		"clipboard",
		"direct_output",
		"ui_message",
		"clipboard_and_direct_output",
		"clipboard_and_ui_message",
		"chat",
	}
)


def _normalize_feedback_behavior(value):
	if not isinstance(value, str):
		return "global"
	val = value.strip().lower()
	if val == "ui_message":
		return "direct_output"
	if val == "clipboard_and_ui_message":
		return "clipboard_and_direct_output"
	return val if val in _VALID_FEEDBACK_BEHAVIORS else "global"


def get_feedback_behavior_options():
	return [
		# Translators: Option to use the global feedback setting for a custom prompt.
		("global", _("Use global setting (default)")),
		# Translators: Option to copy prompt result to clipboard.
		("clipboard", _("Copy AI responses to clipboard")),
		# Translators: Option to output prompt result directly without opening a chat window.
		("direct_output", _("Direct Output (No Chat Window)")),
		# Translators: Option to copy prompt result to clipboard and output directly without a chat window.
		("clipboard_and_direct_output", _("Copy AI responses to clipboard and Direct Output")),
		# Translators: Option to display prompt results in a chat window with follow-up questions.
		("chat", _("Chat Window (Ask questions)")),
	]


def _normalize_custom_prompt_items(items):
	normalized = []
	if not isinstance(items, list):
		return normalized

	for item in items:
		if not isinstance(item, dict):
			continue
		name = item.get("name")
		content = item.get("content")
		if not isinstance(name, str) or not isinstance(content, str):
			continue
		name = name.strip()
		content = content.strip()
		if name and content:
			normalized.append(
				{
					"name": name,
					"content": content,
					"hotkey": _normalize_hotkey(item.get("hotkey")),
					"feedback_behavior": _normalize_feedback_behavior(item.get("feedback_behavior")),
				},
			)
	return normalized


def parse_custom_prompts_v2(raw_value):
	if not isinstance(raw_value, str) or not raw_value.strip():
		return None
	try:
		data = json.loads(raw_value)
	except Exception as e:
		log.warning(f"Invalid custom_prompts_v2 config, falling back to legacy format: {e}")
		return None
	return _normalize_custom_prompt_items(data)


def serialize_custom_prompts_v2(items):
	normalized = _normalize_custom_prompt_items(items)
	if not normalized:
		return ""
	return json.dumps(normalized, ensure_ascii=False)


def load_configured_custom_prompts():
	try:
		raw_v2 = nvda_config.conf["VisionAssistant"]["custom_prompts_v2"]
	except Exception:
		raw_v2 = ""
	items_v2 = parse_custom_prompts_v2(raw_v2)
	if items_v2 is not None:
		return items_v2
	return []


def _sanitize_default_prompt_overrides(data):
	if not isinstance(data, dict):
		return {}, False

	changed = False
	valid_keys = set(get_builtin_default_prompt_map().keys())
	sanitized = {}
	for key, value in data.items():
		if key not in valid_keys or not isinstance(value, str):
			changed = True
			continue
		prompt_text = value.strip()
		if not prompt_text:
			changed = True
			continue
		if prompt_text != value:
			changed = True
		sanitized[key] = prompt_text
	return sanitized, changed


def load_default_prompt_overrides():
	try:
		raw = nvda_config.conf["VisionAssistant"]["default_refine_prompts"]
	except Exception:
		raw = ""
	if not isinstance(raw, str) or not raw.strip():
		return {}

	try:
		data = json.loads(raw)
	except Exception as e:
		log.warning(f"Invalid default_refine_prompts config, using built-ins: {e}")
		return {}

	overrides, _dummy = _sanitize_default_prompt_overrides(data)
	return overrides


def get_configured_default_prompt_map():
	prompt_map = get_builtin_default_prompt_map()
	overrides = load_default_prompt_overrides()
	for key, override in overrides.items():
		if key not in prompt_map:
			continue
		prompt_map[key]["prompt"] = override
	return prompt_map


def get_configured_default_prompts():
	prompt_map = get_configured_default_prompt_map()
	items = []
	for item in vision_config.DEFAULT_SYSTEM_PROMPTS:
		if item.get("internal"):
			continue
		key = item["key"]
		if key in prompt_map:
			items.append(dict(prompt_map[key]))
	items.sort(key=lambda item: item.get("display_label", "").casefold())
	return items


def get_prompt_text(prompt_key):
	prompt_map = get_configured_default_prompt_map()
	item = prompt_map.get(prompt_key)
	if item:
		return item["prompt"]
	return ""


def serialize_default_prompt_overrides(items):
	if not items:
		return ""

	base_map = {item["key"]: item["prompt"] for item in get_builtin_default_prompts()}
	overrides = {}
	for item in items:
		key = item.get("key")
		prompt_text = item.get("prompt", "")
		if key not in base_map:
			continue
		if not isinstance(prompt_text, str):
			continue
		prompt_text = prompt_text.strip()
		if prompt_text and prompt_text != base_map[key]:
			overrides[key] = prompt_text

	if not overrides:
		return ""
	return json.dumps(overrides, ensure_ascii=False)


def get_refine_menu_options():
	options = []
	prompt_map = get_configured_default_prompt_map()
	for key in vision_config.REFINE_PROMPT_KEYS:
		item = prompt_map.get(key)
		if item:
			options.append((item["label"], item["prompt"], "global"))

	for item in load_configured_custom_prompts():
		options.append((item["name"], item["content"], item.get("feedback_behavior", "global")))
	return options


def apply_prompt_template(template, replacements):
	if not isinstance(template, str):
		return ""

	text = template
	for key, value in replacements:
		text = text.replace("{" + key + "}", str(value))

	if "{image_desc_instruction}" in text:
		if nvda_config.conf["VisionAssistant"].get("describe_images_ocr", True):
			lang = nvda_config.conf["VisionAssistant"]["ai_response_language"]
			desc_text = get_prompt_text("ocr_image_desc_instruction")
			desc_text = desc_text.replace("{response_lang}", lang)
			text = text.replace("{image_desc_instruction}", desc_text)
		else:
			text = text.replace("{image_desc_instruction}", "")

	return text.strip()


def finally_(func, final):
	@wraps(func)
	def new(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		finally:
			final()

	return new


_ = vision_config._ if hasattr(vision_config, "_") else (lambda x: x)

STATIC_CAPTURE_VARS = (
	"[screen_full]",
	"[screen_obj]",
	"[screen_fg_obj]",
	"[clipboard_image]",
	"[file_ocr]",
	"[file_read]",
	"[file_audio]",
)

AMBIENT_MODE_VARS = (
	"[ambient_screen]",
	"[ambient_webcam]",
	"[ambient_audio]",
)


def is_ambient_prompt(prompt_text):
	if not isinstance(prompt_text, str):
		return False
	return any(m in prompt_text for m in AMBIENT_MODE_VARS)


def validate_custom_prompt_content(prompt_text):
	if not isinstance(prompt_text, str):
		# Translators: Validation error for empty prompt text.
		return False, _("Prompt text cannot be empty.")
	raw = prompt_text.strip()
	if not raw:
		# Translators: Validation error for empty prompt text.
		return False, _("Prompt text cannot be empty.")

	modes = [m for m in AMBIENT_MODE_VARS if m in raw]
	if len(modes) > 1:
		return False, _(
			# Translators: Validation error when multiple ambient observer modes are used in a single prompt.
			"Cannot combine multiple ambient observer modes ({modes}) in the same prompt."
		).format(
			modes=", ".join(modes),
		)

	statics = [s for s in STATIC_CAPTURE_VARS if s in raw]
	if modes and statics:
		return False, _(
			# Translators: Validation error when static capture variables are combined with an ambient observer mode.
			"Cannot combine static capture variables ({vars}) with ambient observer ({mode}).",
		).format(vars=", ".join(statics), mode=modes[0])

	has_loopback = "[loopback]" in raw
	has_mic = "[mic]" in raw
	if has_loopback and has_mic:
		# Translators: Validation error when both loopback and mic audio sources are specified.
		return False, _("Cannot combine both [loopback] and [mic] audio sources.")

	if has_loopback and "[ambient_audio]" not in raw:
		# Translators: Validation error when [loopback] is used without [ambient_audio].
		return False, _("[loopback] can only be used with [ambient_audio].")

	if has_mic and not ("[ambient_audio]" in raw or "[ambient_webcam]" in raw):
		# Translators: Validation error when [mic] is used without [ambient_audio] or [ambient_webcam].
		return False, _("[mic] can only be used with [ambient_audio] or [ambient_webcam].")

	has_brief = "[brief]" in raw
	has_detailed = "[detailed]" in raw
	if has_brief and has_detailed:
		# Translators: Validation error when both brief and detailed reporting styles are specified.
		return False, _("Cannot combine both [brief] and [detailed] reporting styles.")

	if has_brief or has_detailed:
		if "[ambient_audio]" in raw:
			# Translators: Validation error when reporting styles are used with [ambient_audio].
			return False, _("Reporting styles ([brief], [detailed]) cannot be used with [ambient_audio].")
		if not ("[ambient_screen]" in raw or "[ambient_webcam]" in raw):
			return False, _(
				# Translators: Validation error when reporting styles are used without an ambient visual observer.
				"Reporting styles ([brief], [detailed]) can only be used with [ambient_screen] or [ambient_webcam]."
			)

	lang_tags = re.findall(r"\[lang:[^\]]*\]", raw)
	for tag in lang_tags:
		if not re.match(r"^\[lang:[a-zA-Z\-_]+\]$", tag):
			return False, _(
				# Translators: Validation error when a [lang:code] tag is malformed.
				"Invalid language tag '{tag}'. Use [lang:code], for example [lang:fa] or [lang:en]."
			).format(tag=tag)

	if len(lang_tags) > 1:
		# Translators: Validation error when multiple [lang:code] tags are present in the same prompt.
		return False, _("Only one [lang:code] tag can be used in a prompt.")

	if lang_tags and not modes:
		# Translators: Validation error when [lang:code] is used without an ambient mode.
		return False, _("[lang:code] can only be used with ambient observer modes.")

	if "[ambient_audio]" in raw:
		stripped = raw
		for tag in ("[ambient_audio]", "[loopback]", "[mic]"):
			stripped = stripped.replace(tag, "")
		stripped = re.sub(r"\[lang:[a-zA-Z\-_]+\]", "", stripped).strip()
		if stripped:
			return False, _(
				# Translators: Validation error when non-variable text instructions are included in [ambient_audio].
				"Audio Observer does not accept instructional text prompts. Only audio source and [lang:code] are supported.",
			)

	return True, ""


def parse_ambient_prompt(prompt_text):
	raw = str(prompt_text or "")
	mode = None
	if "[ambient_screen]" in raw:
		mode = "screen"
	elif "[ambient_webcam]" in raw:
		mode = "webcam"
	elif "[ambient_audio]" in raw:
		mode = "audio"

	audio_source = None
	if "[loopback]" in raw:
		audio_source = "system"
	elif "[mic]" in raw:
		audio_source = "mic"
	elif mode == "audio":
		try:
			audio_source = nvda_config.conf["VisionAssistant"].get("ambient_audio_source", "system")
		except Exception:
			audio_source = "system"
	elif mode == "webcam":
		audio_source = "mic"

	target_code = None
	lang_match = re.search(r"\[lang:([a-zA-Z\-_]+)\]", raw)
	if lang_match:
		target_code = lang_match.group(1).lower()
	elif mode == "audio":
		try:
			target_code = nvda_config.conf["VisionAssistant"].get("ambient_audio_lang", "en")
		except Exception:
			target_code = "en"

	style = None
	if "[brief]" in raw:
		style = "brief"
	elif "[detailed]" in raw:
		style = "detailed"
	elif mode in ("screen", "webcam"):
		style = "custom"

	use_ptt = None
	if mode == "webcam":
		try:
			use_ptt = bool(nvda_config.conf["VisionAssistant"].get("live_push_to_talk", False))
		except Exception:
			use_ptt = False

	context = ""
	if mode in ("screen", "webcam"):
		clean = raw
		for tag in (
			"[ambient_screen]",
			"[ambient_webcam]",
			"[ambient_audio]",
			"[loopback]",
			"[mic]",
			"[brief]",
			"[detailed]",
		):
			clean = clean.replace(tag, "")
		clean = re.sub(r"\[lang:[a-zA-Z\-_]+\]", "", clean)
		context = clean.strip()
		if context:
			try:
				target_lang = vision_config.get_lang_name("target_language")
				source_lang = vision_config.get_lang_name("source_language")
				resp_lang = vision_config.get_lang_name("ai_response_language")
				context = apply_prompt_template(
					context,
					[
						("target_lang", target_lang),
						("source_lang", source_lang),
						("response_lang", resp_lang),
					],
				)
			except Exception:
				pass

	return {
		"mode": mode,
		"audio_source": audio_source,
		"target_code": target_code,
		"style": style,
		"context": context,
		"use_ptt": use_ptt,
	}
