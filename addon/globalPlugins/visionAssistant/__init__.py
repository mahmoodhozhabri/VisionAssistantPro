# -*- coding: utf-8 -*-
import sys
import os
import json
import threading
import logging
import base64
import io
import ctypes
import re
import tempfile
import time
import wave
import gc
import wx
from urllib import request, error, parse
from urllib.parse import quote, urlparse, urlencode
from http import cookiejar
from functools import wraps
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor

lib_dir = os.path.join(os.path.dirname(__file__), "lib")
if lib_dir not in sys.path:
    sys.path.append(lib_dir)

try:
    import markdown as markdown_lib
except ImportError:
    markdown_lib = None

try:
    import fitz
except ImportError:
    fitz = None

import addonHandler
import globalPluginHandler
import config
import gui
import ui
import api
import textInfos
import tones
import NVDAObjects.behaviors
import scriptHandler
from .prompt_manager_dialog import PromptManagerDialog

log = logging.getLogger(__name__)
addonHandler.initTranslation()

_vision_assistant_instance = None

ADDON_NAME = addonHandler.getCodeAddon().manifest["summary"]
GITHUB_REPO = "mahmoodhozhabri/VisionAssistantPro"

# --- Constants & Config ---

CHROME_OCR_KEYS = [
    "AIzaSyA2KlwBX3mkFo30om9LUFYQhpqLoa_BNhE",
    "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
]

MODELS = [
    # --- 1. Recommended (Auto-Updating) ---
    # Translators: AI Model info. [Auto] = Automatic updates. (Latest) = Newest version.
    (_("[Auto]") + " Gemini Flash " + _("(Latest)"), "gemini-flash-latest"),
    (_("[Auto]") + " Gemini Flash Lite " + _("(Latest)"), "gemini-flash-lite-latest"),

    # --- 2. Current Standard (Free & Fast) ---
    # Translators: AI Model info. [Free] = Generous usage limits. (Preview) = Experimental or early-access version.
    (_("[Free]") + " Gemini 3.0 Flash " + _("(Preview)"), "gemini-3-flash-preview"),
    (_("[Free]") + " Gemini 2.5 Flash", "gemini-2.5-flash"),
    (_("[Free]") + " Gemini 2.5 Flash Lite", "gemini-2.5-flash-lite"),

    # --- 3. High Intelligence (Paid/Pro/Preview) ---
    # Translators: AI Model info. [Pro] = High intelligence/Paid tier. (Preview) = Experimental version.
    (_("[Pro]") + " Gemini 3.0 Pro " + _("(Preview)"), "gemini-3-pro-preview"),
    (_("[Pro]") + " Gemini 2.5 Pro", "gemini-2.5-pro"),
]

GEMINI_VOICES = [
    # Translators: Voice style description (e.g., Bright, Calm, Formal).
    ("Zephyr", _("Bright")), 
    ("Puck", _("Upbeat")), 
    ("Charon", _("Informative")), 
    ("Kore", _("Firm")), 
    ("Fenrir", _("Excitable")), 
    ("Leda", _("Youthful")), 
    ("Orus", _("Firm")), 
    ("Aoede", _("Breezy")), 
    ("Callirrhoe", _("Easy-going")), 
    ("Autonoe", _("Bright")), 
    ("Enceladus", _("Breathy")), 
    ("Iapetus", _("Clear")), 
    ("Umbriel", _("Easy-going")), 
    ("Algieba", _("Smooth")), 
    ("Despina", _("Smooth")), 
    ("Erinome", _("Clear")), 
    ("Algenib", _("Gravelly")), 
    ("Rasalgethi", _("Informative")), 
    ("Laomedeia", _("Upbeat")), 
    ("Achernar", _("Soft")), 
    ("Alnilam", _("Firm")), 
    ("Schedar", _("Even")), 
    ("Gacrux", _("Mature")), 
    ("Pulcherrima", _("Forward")), 
    ("Achird", _("Friendly")), 
    ("Zubenelgenubi", _("Casual")), 
    ("Vindemiatrix", _("Gentle")), 
    ("Sadachbia", _("Lively")), 
    ("Sadaltager", _("Knowledgeable")), 
    ("Sulafat", _("Warm"))
]

BASE_LANGUAGES = [
    ("Arabic", "ar"), ("Bulgarian", "bg"), ("Chinese", "zh"), ("Czech", "cs"), ("Danish", "da"),
    ("Dutch", "nl"), ("English", "en"), ("Finnish", "fi"), ("French", "fr"),
    ("German", "de"), ("Greek", "el"), ("Hebrew", "he"), ("Hindi", "hi"),
    ("Hungarian", "hu"), ("Indonesian", "id"), ("Italian", "it"), ("Japanese", "ja"),
    ("Korean", "ko"), ("Nepali", "ne"), ("Norwegian", "no"), ("Persian", "fa"), ("Polish", "pl"),
    ("Portuguese", "pt"), ("Romanian", "ro"), ("Russian", "ru"), ("Spanish", "es"),
    ("Swedish", "sv"), ("Thai", "th"), ("Turkish", "tr"), ("Ukrainian", "uk"),
    ("Vietnamese", "vi")
]
SOURCE_LIST = [("Auto-detect", "auto")] + BASE_LANGUAGES
SOURCE_NAMES = [x[0] for x in SOURCE_LIST]
TARGET_LIST = BASE_LANGUAGES
TARGET_NAMES = [x[0] for x in TARGET_LIST]
TARGET_CODES = {x[0]: x[1] for x in BASE_LANGUAGES}

OCR_ENGINES = [
    # Translators: OCR Engine option (Fast but less formatted)
    (_("Chrome (Fast)"), "chrome"),
    # Translators: OCR Engine option (Slower but better formatting)
    (_("Gemini (Formatted)"), "gemini")
]

confspec = {
    "proxy_url": "string(default='')",
    "api_key": "string(default='')",
    "model_name": "string(default='gemini-flash-lite-latest')",
    "target_language": "string(default='English')",
    "source_language": "string(default='Auto-detect')",
    "ai_response_language": "string(default='English')",
    "smart_swap": "boolean(default=True)",
    "captcha_mode": "string(default='navigator')",
    "custom_prompts": "string(default='')",
    "custom_prompts_v2": "string(default='')",
    "default_refine_prompts": "string(default='')",
    "check_update_startup": "boolean(default=False)",
    "clean_markdown_chat": "boolean(default=True)",
    "copy_to_clipboard": "boolean(default=False)",
    "skip_chat_dialog": "boolean(default=False)",
    "ocr_engine": "string(default='chrome')",
    "tts_voice": "string(default='Puck')"
}

config.conf.spec["VisionAssistant"] = confspec

PROMPT_TRANSLATE = """
Task: Translate the text below to "{target_lang}".

Configuration:
- Target Language: "{target_lang}"
- Swap Language: "{swap_target}"
- Smart Swap: {smart_swap}

Rules:
1. DEFAULT: Translate the input strictly to "{target_lang}".
2. MIXED CONTENT: If the text contains mixed languages (e.g., Arabic content with English UI terms like 'Reply', 'From', 'Forwarded'), translate EVERYTHING to "{target_lang}".
3. EXCEPTION: If (and ONLY if) the input is already completely in "{target_lang}" AND "Smart Swap" is True, then translate to "{swap_target}".

Constraints:
- Output ONLY the translation.
- Do NOT translate actual programming code (Python, C++, etc.) or URLs.
- Translate ALL UI elements, menus, and interface labels.

Input Text:
{text_content}
"""

PROMPT_UI_LOCATOR = "Analyze UI (Size: {width}x{height}). Request: '{query}'. Output JSON: {{\"x\": int, \"y\": int, \"found\": bool}}."

REFINE_PROMPT_KEYS = ("summarize", "fix_grammar", "fix_translate", "explain")

LEGACY_REFINER_TOKENS = {
    "summarize": "[summarize]",
    "fix_grammar": "[fix_grammar]",
    "fix_translate": "[fix_translate]",
    "explain": "[explain]",
}

DEFAULT_SYSTEM_PROMPTS = (
    {
        "key": "summarize",
        "section": _("Refine"),
        "label": _("Summarize"),
        "prompt": "Summarize the text below in {response_lang}.",
    },
    {
        "key": "fix_grammar",
        "section": _("Refine"),
        "label": _("Fix Grammar"),
        "prompt": "Fix grammar in the text below. Output ONLY the fixed text.",
    },
    {
        "key": "fix_translate",
        "section": _("Refine"),
        "label": _("Fix Grammar & Translate"),
        "prompt": "Fix grammar and translate to {target_lang}.{swap_instruction} Output ONLY the result.",
    },
    {
        "key": "explain",
        "section": _("Refine"),
        "label": _("Explain"),
        "prompt": "Explain the text below in {response_lang}.",
    },
    {
        "key": "translate_main",
        "section": _("Translation"),
        "label": _("Smart Translation"),
        "prompt": PROMPT_TRANSLATE.strip(),
    },
    {
        "key": "translate_quick",
        "section": _("Translation"),
        "label": _("Quick Translation"),
        "prompt": "Translate to {target_lang}. Output ONLY translation.",
    },
    {
        "key": "document_chat_system",
        "section": _("Document"),
        "label": _("Document Chat Context"),
        "prompt": "STRICTLY Respond in {response_lang}. Use Markdown formatting. Analyze the attached content to answer.",
    },
    {
        "key": "document_chat_ack",
        "section": _("Advanced"),
        "label": _("Document Chat Bootstrap Reply"),
        "internal": True,
        "prompt": "Context received. Ready for questions.",
    },
    {
        "key": "vision_navigator_object",
        "section": _("Vision"),
        "label": _("Navigator Object Analysis"),
        "prompt": (
            "Analyze this image. Describe the layout, visible text, and UI elements. "
            "Use Markdown formatting (headings, lists) to organize the description. "
            "Language: {response_lang}. Ensure the response is strictly in {response_lang}. "
            "IMPORTANT: Start directly with the description content. Do not add introductory "
            "sentences like 'Here is the analysis' or 'The image shows'."
        ),
    },
    {
        "key": "vision_fullscreen",
        "section": _("Vision"),
        "label": _("Full Screen Analysis"),
        "prompt": (
            "Analyze this image. Describe the layout, visible text, and UI elements. "
            "Use Markdown formatting (headings, lists) to organize the description. "
            "Language: {response_lang}. Ensure the response is strictly in {response_lang}. "
            "IMPORTANT: Start directly with the description content. Do not add introductory "
            "sentences like 'Here is the analysis' or 'The image shows'."
        ),
    },
    {
        "key": "vision_followup_context",
        "section": _("Advanced"),
        "label": _("Vision Follow-up Context"),
        "internal": True,
        "prompt": "Image Context. Target Language: {response_lang}",
    },
    {
        "key": "vision_followup_suffix",
        "section": _("Advanced"),
        "label": _("Vision Follow-up Answer Rule"),
        "internal": True,
        "prompt": "Answer strictly in {response_lang}",
    },
    {
        "key": "video_analysis",
        "section": _("Video"),
        "label": _("Video Analysis"),
        "prompt": (
            "Analyze this video. Provide a detailed description of the visual content and a "
            "summary of the audio. IMPORTANT: Write the entire response STRICTLY in "
            "{response_lang} language."
        ),
    },
    {
        "key": "audio_transcription",
        "section": _("Audio"),
        "label": _("Audio Transcription"),
        "prompt": "Transcribe this audio in {response_lang}.",
    },
    {
        "key": "dictation_transcribe",
        "section": _("Audio"),
        "label": _("Smart Dictation"),
        "prompt": (
            "Transcribe speech. Use native script. Fix stutters. If there is no speech, silence, "
            "or background noise only, write exactly: [[[NOSPEECH]]]"
        ),
    },
    {
        "key": "ocr_image_extract",
        "section": _("OCR"),
        "label": _("OCR Image Extraction"),
        "prompt": (
            "Extract all visible text from this image. Strictly preserve original formatting "
            "(headings, lists, tables) using Markdown. Do not output any system messages or "
            "code block backticks (```). Output ONLY the raw content."
        ),
    },
    {
        "key": "ocr_document_extract",
        "section": _("OCR"),
        "label": _("OCR Document Extraction"),
        "prompt": (
            "Extract all visible text from this document. Strictly preserve original formatting "
            "(headings, lists, tables) using Markdown. You MUST insert the exact delimiter "
            "'[[[PAGE_SEP]]]' immediately after the content of every single page. Do not output "
            "any system messages or code block backticks (```). Output ONLY the raw content."
        ),
    },
    {
        "key": "ocr_document_translate",
        "section": _("Document"),
        "label": _("Document OCR + Translate"),
        "prompt": (
            "Extract all text from this document. Preserve formatting (Markdown). Then translate "
            "the content to {target_lang}. Output ONLY the translated content. Do not add "
            "explanations."
        ),
    },
    {
        "key": "captcha_solver_base",
        "section": _("CAPTCHA"),
        "label": _("CAPTCHA Solver"),
        "internal": True,
        "prompt": (
            "Blind user. Return CAPTCHA code only. If NO CAPTCHA is detected in the image, "
            "strictly return: [[[NO_CAPTCHA]]].{captcha_extra}"
        ),
    },
    {
        "key": "refine_files_only",
        "section": _("Advanced"),
        "label": _("Refine Files-Only Fallback"),
        "internal": True,
        "prompt": "Analyze these files.",
    },
)

PROMPT_VARIABLES_GUIDE = (
    ("[selection]", _("Currently selected text"), _("Text")),
    ("[clipboard]", _("Clipboard content"), _("Text")),
    ("[screen_obj]", _("Screenshot of the navigator object"), _("Image")),
    ("[screen_full]", _("Screenshot of the entire screen"), _("Image")),
    ("[file_ocr]", _("Select image/PDF/TIFF for text extraction"), _("Image, PDF, TIFF")),
    ("[file_read]", _("Select document for reading"), _("TXT, Code, PDF")),
    ("[file_audio]", _("Select audio file for analysis"), _("MP3, WAV, OGG")),
)

# --- Helpers ---

def get_builtin_default_prompts():
    builtins = []
    for item in DEFAULT_SYSTEM_PROMPTS:
        p = str(item["prompt"]).strip()
        builtins.append({
            "key": item["key"],
            "section": item["section"],
            "label": item["label"],
            "display_label": f"{item['section']} - {item['label']}",
            "internal": bool(item.get("internal")),
            "prompt": p,
            "default": p,
        })
    return builtins

def get_builtin_default_prompt_map():
    return {item["key"]: item for item in get_builtin_default_prompts()}

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
            normalized.append({"name": name, "content": content})
    return normalized

def parse_custom_prompts_legacy(raw_value):
    items = []
    if not raw_value:
        return items

    normalized = raw_value.replace("\r\n", "\n").replace("\r", "\n")
    for line in normalized.split("\n"):
        for segment in line.split("|"):
            segment = segment.strip()
            if not segment or ":" not in segment:
                continue
            name, content = segment.split(":", 1)
            name = name.strip()
            content = content.strip()
            if name and content:
                items.append({"name": name, "content": content})
    return items

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
        raw_v2 = config.conf["VisionAssistant"]["custom_prompts_v2"]
    except Exception:
        raw_v2 = ""
    items_v2 = parse_custom_prompts_v2(raw_v2)
    if items_v2 is not None:
        return items_v2
    return parse_custom_prompts_legacy(config.conf["VisionAssistant"]["custom_prompts"])

def _sanitize_default_prompt_overrides(data):
    if not isinstance(data, dict):
        return {}, False

    changed = False
    mutable = dict(data)
    # Migrate old key used in previous versions.
    legacy_vision = mutable.pop("vision_image_analysis", None)
    if legacy_vision is not None:
        changed = True
    if isinstance(legacy_vision, str) and legacy_vision.strip():
        legacy_text = legacy_vision.strip()
        nav_value = mutable.get("vision_navigator_object")
        if not isinstance(nav_value, str) or not nav_value.strip():
            mutable["vision_navigator_object"] = legacy_text
            changed = True
        full_value = mutable.get("vision_fullscreen")
        if not isinstance(full_value, str) or not full_value.strip():
            mutable["vision_fullscreen"] = legacy_text
            changed = True

    valid_keys = set(get_builtin_default_prompt_map().keys())
    sanitized = {}
    for key, value in mutable.items():
        if key not in valid_keys or not isinstance(value, str):
            changed = True
            continue
        prompt_text = value.strip()
        if not prompt_text:
            changed = True
            continue
        if key in LEGACY_REFINER_TOKENS and prompt_text == LEGACY_REFINER_TOKENS[key]:
            # Drop old token-only overrides and fallback to current built-ins.
            changed = True
            continue
        if prompt_text != value:
            changed = True
        sanitized[key] = prompt_text
    return sanitized, changed

def migrate_prompt_config_if_needed():
    changed = False

    try:
        raw_v2 = config.conf["VisionAssistant"]["custom_prompts_v2"]
    except Exception:
        raw_v2 = ""
    raw_legacy = config.conf["VisionAssistant"]["custom_prompts"]

    v2_items = parse_custom_prompts_v2(raw_v2)
    if v2_items is None:
        target_items = parse_custom_prompts_legacy(raw_legacy)
    else:
        target_items = v2_items

    serialized_v2 = serialize_custom_prompts_v2(target_items)
    if serialized_v2 != (raw_v2 or ""):
        config.conf["VisionAssistant"]["custom_prompts_v2"] = serialized_v2
        changed = True

    # Legacy mirror is disabled. Clear old storage to prevent stale fallback data.
    if raw_legacy:
        config.conf["VisionAssistant"]["custom_prompts"] = ""
        changed = True

    try:
        raw_defaults = config.conf["VisionAssistant"]["default_refine_prompts"]
    except Exception:
        raw_defaults = ""
    if isinstance(raw_defaults, str) and raw_defaults.strip():
        try:
            defaults_data = json.loads(raw_defaults)
        except Exception:
            defaults_data = None
        if isinstance(defaults_data, dict):
            sanitized, migrated = _sanitize_default_prompt_overrides(defaults_data)
            if migrated:
                config.conf["VisionAssistant"]["default_refine_prompts"] = (
                    json.dumps(sanitized, ensure_ascii=False) if sanitized else ""
                )
                changed = True

    return changed

def load_default_prompt_overrides():
    try:
        raw = config.conf["VisionAssistant"]["default_refine_prompts"]
    except Exception:
        raw = ""
    if not isinstance(raw, str) or not raw.strip():
        return {}

    try:
        data = json.loads(raw)
    except Exception as e:
        log.warning(f"Invalid default_refine_prompts config, using built-ins: {e}")
        return {}

    overrides, _ = _sanitize_default_prompt_overrides(data)
    return overrides

def get_configured_default_prompt_map():
    prompt_map = get_builtin_default_prompt_map()
    overrides = load_default_prompt_overrides()
    for key, override in overrides.items():
        if key not in prompt_map:
            continue
        if key in LEGACY_REFINER_TOKENS and override == LEGACY_REFINER_TOKENS[key]:
            continue
        prompt_map[key]["prompt"] = override
    return prompt_map

def get_configured_default_prompts():
    prompt_map = get_configured_default_prompt_map()
    items = []
    for item in DEFAULT_SYSTEM_PROMPTS:
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
    for key in REFINE_PROMPT_KEYS:
        item = prompt_map.get(key)
        if item:
            options.append((item["label"], item["prompt"]))

    for item in load_configured_custom_prompts():
        # Translators: Prefix for custom prompts in the Refine menu
        options.append((_("Custom: ") + item["name"], item["content"]))
    return options

def apply_prompt_template(template, replacements):
    if not isinstance(template, str):
        return ""

    text = template
    for key, value in replacements:
        text = text.replace("{" + key + "}", str(value))

    return text.strip()

def finally_(func, final):
    @wraps(func)
    def new(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            final()
    return new

def clean_markdown(text):
    if not text: return ""
    text = re.sub(r'\*\*|__|[*_]', '', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'```', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'^\s*-\s+', '', text, flags=re.MULTILINE)
    return text.strip()

def markdown_to_html(text, full_page=False):
    if not text: return ""
    
    html = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html)
    html = re.sub(r'__(.*?)__', r'<i>\1</i>', html)
    html = re.sub(r'^### (.*)', r'<h3>\1</h3>', html, flags=re.M)
    html = re.sub(r'^## (.*)', r'<h2>\1</h2>', html, flags=re.M)
    html = re.sub(r'^# (.*)', r'<h1>\1</h1>', html, flags=re.M)
    
    lines = html.split('\n')
    in_table = False
    new_lines = []
    table_style = 'border="1" style="border-collapse: collapse; width: 100%; margin-bottom: 10px;"'
    td_style = 'style="padding: 5px; border: 1px solid #ccc;"'
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') or (stripped.count('|') > 1 and len(stripped) > 5):
            if not in_table:
                new_lines.append(f'<table {table_style}>')
                in_table = True
            if '---' in stripped: continue
            row_content = stripped.strip('|').split('|')
            cells = "".join([f'<td {td_style}>{c.strip()}</td>' for c in row_content])
            new_lines.append(f'<tr>{cells}</tr>')
        else:
            if in_table:
                new_lines.append('</table>')
                in_table = False
            if stripped: new_lines.append(line + "<br>")
            else: new_lines.append("<br>")
    if in_table: new_lines.append('</table>')
    html_body = "".join(new_lines)

    if not full_page: return html_body
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>body{{font-family:"Segoe UI",Arial,sans-serif;line-height:1.6;padding:20px;color:#333;max-width:800px;margin:0 auto}}h1,h2,h3{{color:#2c3e50;border-bottom:1px solid #eee;padding-bottom:5px}}pre{{background-color:#f4f4f4;padding:10px;border-radius:5px;overflow-x:auto;font-family:Consolas,monospace}}code{{background-color:#f4f4f4;padding:2px 5px;border-radius:3px;font-family:Consolas,monospace}}table{{border-collapse:collapse;width:100%;margin-bottom:10px}}td,th{{border:1px solid #ccc;padding:8px;text-align:left}}strong,b{{color:#000;font-weight:bold}}li{{margin-bottom:5px}}</style></head><body>{html_body}</body></html>"""

def get_mime_type(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf': return 'application/pdf'
    if ext in ['.jpg', '.jpeg']: return 'image/jpeg'
    if ext == '.png': return 'image/png'
    if ext == '.webp': return 'image/webp'
    if ext in ['.tif', '.tiff']: return 'image/jpeg'
    if ext == '.mp3': return 'audio/mpeg'
    if ext == '.wav': return 'audio/wav'
    if ext == '.ogg': return 'audio/ogg'
    if ext == '.mp4': return 'video/mp4'
    return 'application/octet-stream'

def show_error_dialog(message):
    # Translators: Title of the error dialog box
    title = _("{name} Error").format(name=ADDON_NAME)
    wx.CallAfter(gui.messageBox, message, title, wx.OK | wx.ICON_ERROR)

def send_ctrl_v():
    try:
        user32 = ctypes.windll.user32
        VK_CONTROL = 0x11; VK_V = 0x56; KEYEVENTF_KEYUP = 0x0002
        user32.keybd_event(VK_CONTROL, 0, 0, 0)
        user32.keybd_event(VK_V, 0, 0, 0)
        user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
        user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
    except: pass

def get_proxy_opener():
    proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
    if proxy_url:
        if "127.0.0.1" in proxy_url or "localhost" in proxy_url or ":" in proxy_url.split("/")[-1]:
             handler = request.ProxyHandler({'http': proxy_url, 'https': proxy_url})
             return request.build_opener(handler)
    return request.build_opener()

def get_twitter_download_link(tweet_url):
    cj = cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    base_url = "https://savetwitter.net/en4"
    api_url = "https://savetwitter.net/api/ajaxSearch"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36', 'X-Requested-With': 'XMLHttpRequest', 'Referer': base_url}
    try:
        req_init = request.Request(base_url, headers=headers)
        opener.open(req_init)
        params = {'q': tweet_url, 'lang': 'en', 'cftoken': ''}
        data = urlencode(params).encode('utf-8')
        req_post = request.Request(api_url, data=data, headers=headers, method='POST')
        with opener.open(req_post) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            if res_data.get('status') == 'ok':
                html = res_data.get('data', '')
                match = re.search(r'href="(https?://dl\.snapcdn\.app/[^"]+)"', html)
                if match: return match.group(1)
    except: pass
    return None

def get_instagram_download_link(insta_url):
    cj = cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://anon-viewer.com/',
        'Accept': '*/*'
    }
    opener.addheaders = list(headers.items())
    try:
        opener.open("https://anon-viewer.com/", timeout=30)
        
        if "/stories/" in insta_url:
            parts = insta_url.split("/")
            username = parts[parts.index("stories") + 1]
            api_url = f"https://anon-viewer.com/content.php?url={username}&method=allstories"
        else:
            encoded_url = quote(insta_url, safe='')
            api_url = f"https://anon-viewer.com/content.php?url={encoded_url}"

        response = opener.open(api_url, timeout=60)
        if response.getcode() == 200:
            res_content = response.read().decode('utf-8')
            data = json.loads(res_content)
            html_text = data.get('html', '')
            
            match = re.search(r'href="([^"]+anon-viewer\.com/media\.php\?media=[^"]+)"', html_text)
            if match:
                return match.group(1).replace('&amp;', '&')
            
            source_match = re.search(r'<source src="([^"]+)"', html_text)
            if source_match:
                return source_match.group(1).replace('&amp;', '&')
    except: pass
    return None

def get_tiktok_download_link(tiktok_url):
    api_url = "https://www.tikwm.com/api/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        params = {'url': tiktok_url, 'hd': '1'}
        data = urlencode(params).encode('utf-8')
        req = request.Request(api_url, data=data, headers=headers, method='POST')
        opener = get_proxy_opener()
        with opener.open(req, timeout=30) as response:
            res = json.loads(response.read().decode('utf-8'))
            if res.get('code') == 0:
                play_url = res['data']['play']
                return play_url if play_url.startswith('http') else "https://www.tikwm.com" + play_url
    except: pass
    return None

def _download_temp_video(url):
    try:
        req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with request.urlopen(req, timeout=60) as response:
            fd, path = tempfile.mkstemp(suffix=".mp4")
            os.close(fd)
            with open(path, 'wb') as f:
                while True:
                    chunk = response.read(8192)
                    if not chunk: break
                    f.write(chunk)
            return path
    except: pass
    return None

def get_file_path(title, wildcard, mode="open", multiple=False):
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST if mode == "open" else wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
    if multiple: style |= wx.FD_MULTIPLE
    with wx.FileDialog(gui.mainFrame, title, wildcard=wildcard, style=style) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            return dlg.GetPaths() if multiple else dlg.GetPath()
    return None

class VirtualDocument:
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.page_map = [] 
        self.total_pages = 0
        self.is_single_pdf = (len(file_paths) == 1 and file_paths[0].lower().endswith('.pdf'))
        self.single_pdf_path = file_paths[0] if self.is_single_pdf else None

    def scan(self):
        if not fitz: return
        for path in self.file_paths:
            try:
                doc = fitz.open(path)
                count = len(doc)
                for i in range(count):
                    self.page_map.append((path, i))
                doc.close()
            except Exception as e:
                log.error(f"Error scanning file {path}: {e}", exc_info=True)
        self.total_pages = len(self.page_map)

    def get_page_info(self, global_page_index):
        if 0 <= global_page_index < self.total_pages:
            return self.page_map[global_page_index]
        return None, None

    def create_merged_pdf(self, start_page, end_page):
        if not fitz: return None
        try:
            out_doc = fitz.open()
            for i in range(start_page, end_page + 1):
                f_path, f_idx = self.get_page_info(i)
                src_doc = fitz.open(f_path)
                if src_doc.is_pdf:
                    out_doc.insert_pdf(src_doc, from_page=f_idx, to_page=f_idx)
                else:
                    pdf_bytes = src_doc.convert_to_pdf(from_page=f_idx, to_page=f_idx)
                    img_pdf = fitz.open("pdf", pdf_bytes)
                    out_doc.insert_pdf(img_pdf)
                src_doc.close()
            
            fd, temp_path = tempfile.mkstemp(suffix=".pdf")
            os.close(fd)
            out_doc.save(temp_path)
            out_doc.close()
            return temp_path
        except Exception as e:
            log.error(f"Error merging PDF: {e}", exc_info=True)
            return None

class ChromeOCREngine:
    @staticmethod
    def recognize(image_bytes):
        key = CHROME_OCR_KEYS[0]
        url = "https://ckintersect-pa.googleapis.com/v1/intersect/pixels"
        headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0", "x-goog-api-key": key}
        payload = {"imageRequests": [{"engineParameters": [{"ocrParameters": {}}], "imageBytes": base64.b64encode(image_bytes).decode('utf-8'), "imageId": str(uuid4())}]}
        try:
            req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
            opener = get_proxy_opener()
            with opener.open(req, timeout=30) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    regions = data['results'][0]['engineResults'][0]['ocrEngine'].get('ocrRegions', [])
                    lines = []
                    for reg in regions:
                        line_text = " ".join([w.get('detectedText', '') for w in reg.get('words', [])])
                        if line_text.strip(): lines.append(line_text)
                    return "\n".join(lines)
        except Exception as e:
            log.error(f"Chrome OCR Failed: {e}", exc_info=True)
            return None
        return None

class SmartProgrammersOCREngine:
    @staticmethod
    def recognize(image_bytes):
        url = "https://ubsa.in/smartprogrammers/SP%20Reader/extract.php"
        boundary = uuid4().hex.encode('utf-8')
        body = []
        body.append(b'--' + boundary)
        body.append(f'Content-Disposition: form-data; name="file"; filename="p.jpg"'.encode('utf-8'))
        body.append(b'Content-Type: image/jpeg')
        body.append(b'')
        body.append(image_bytes)
        body.append(b'--' + boundary + b'--')
        body.append(b'')
        try:
            req = request.Request(url, data=b'\r\n'.join(body), headers={'Content-Type': f"multipart/form-data; boundary={boundary.decode('utf-8')}"}, method="POST")
            opener = get_proxy_opener()
            with opener.open(req, timeout=40) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    text = data.get("text", "").replace("\\n", "\n")
                    return text if text.strip() else None
        except Exception as e:
            log.error(f"SmartProgrammers OCR Failed: {e}", exc_info=True)
            return None
        return None

class GoogleTranslator:
    @staticmethod
    def translate(text, target_lang):
        try:
            target_code = TARGET_CODES.get(target_lang, 'en')
            base_url = "https://translate.googleapis.com/translate_a/single"
            params = {"client": "gtx", "sl": "auto", "tl": target_code, "dt": "t", "q": text}
            url = f"{base_url}?{parse.urlencode(params)}"
            req = request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            opener = get_proxy_opener()
            with opener.open(req, timeout=30) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    if data and isinstance(data, list) and len(data) > 0:
                        result_parts = [x[0] for x in data[0] if x[0]]
                        return "".join(result_parts)
        except Exception as e:
            log.error(f"Google Translate Failed: {e}", exc_info=True)
            return text 
        return text

class GeminiHandler:
    _working_key_idx = 0 
    _file_uri_keys = {}
    _max_retries = 5

    @staticmethod
    def _get_api_keys():
        raw = config.conf["VisionAssistant"]["api_key"]
        clean_raw = raw.replace('\r\n', ',').replace('\n', ',')
        return [k.strip() for k in clean_raw.split(',') if k.strip()]

    @staticmethod
    def _get_opener():
        return get_proxy_opener()

    @staticmethod
    def _handle_error(e):
        if hasattr(e, 'code'):
            # Translators: Error message for Bad Request (400)
            if e.code == 400: return _("Error 400: Bad Request (Check API Key)")
            # Translators: Error message for Forbidden (403)
            if e.code == 403: return _("Error 403: Forbidden (Check Region)")
            if e.code == 429: return "QUOTA_EXCEEDED"
            if e.code >= 500: return "SERVER_ERROR"
        return str(e)

    @staticmethod
    def _call_with_retry(func_logic, key, *args):
        last_exc = None
        for attempt in range(GeminiHandler._max_retries):
            try:
                return func_logic(key, *args)
            except error.HTTPError as e:
                err_msg = GeminiHandler._handle_error(e)
                if err_msg not in ["QUOTA_EXCEEDED", "SERVER_ERROR"]:
                    raise
                last_exc = e
            except error.URLError as e:
                last_exc = e
            if attempt < GeminiHandler._max_retries - 1:
                time.sleep(0.5 * (attempt + 1))
        raise last_exc

    @staticmethod
    def _register_file_uri(uri, key):
        if uri and key:
            GeminiHandler._file_uri_keys[uri] = key
            while len(GeminiHandler._file_uri_keys) > 200:
                GeminiHandler._file_uri_keys.pop(next(iter(GeminiHandler._file_uri_keys)))

    @staticmethod
    def _get_registered_key(uri):
        if not uri:
            return None
        return GeminiHandler._file_uri_keys.get(uri)

    @staticmethod
    def _call_with_key(func_logic, key, *args):
        try:
            return GeminiHandler._call_with_retry(func_logic, key, *args)
        except error.HTTPError as e:
            err_msg = GeminiHandler._handle_error(e)
            if err_msg == "QUOTA_EXCEEDED":
                # Translators: Message of a dialog which may pop up while performing an AI call
                err_msg = _("Error 429: Quota Exceeded (Try later)")
            elif err_msg == "SERVER_ERROR":
                # Translators: Message of a dialog which may pop up while performing an AI call
                err_msg = _("Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
            return "ERROR:" + err_msg
        except Exception as e:
            return "ERROR:" + str(e)

    @staticmethod
    def _call_with_rotation(func_logic, *args):
        keys = GeminiHandler._get_api_keys()
        if not keys: 
            # Translators: Error when no API keys are found in settings
            return "ERROR:" + _("No API Keys configured.")
        
        num_keys = len(keys)
        for i in range(num_keys):
            idx = (GeminiHandler._working_key_idx + i) % num_keys
            key = keys[idx]
            try:
                res = GeminiHandler._call_with_retry(func_logic, key, *args)
                GeminiHandler._working_key_idx = idx 
                return res
            except error.HTTPError as e:
                err_msg = GeminiHandler._handle_error(e)
                if err_msg in ["QUOTA_EXCEEDED", "SERVER_ERROR"]:
                    if i < num_keys - 1: continue
                    # Translators: Error when all available API keys fail
                    return "ERROR:" + _("All API Keys failed (Quota/Server).")
                return "ERROR:" + err_msg
            except Exception as e:
                return "ERROR:" + str(e)
        return "ERROR:" + _("Unknown error occurred.")

    @staticmethod
    def translate(text, target_lang):
        def _logic(key, txt, lang):
            model = config.conf["VisionAssistant"]["model_name"]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            quick_template = get_prompt_text("translate_quick") or "Translate to {target_lang}. Output ONLY translation."
            quick_prompt = apply_prompt_template(quick_template, [("target_lang", lang)])
            payload = {"contents": [{"parts": [{"text": quick_prompt}, {"text": txt}]}]}
            req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json", "x-goog-api-key": key})
            with GeminiHandler._get_opener().open(req, timeout=90) as r:
                return json.loads(r.read().decode())['candidates'][0]['content']['parts'][0]['text']
        return GeminiHandler._call_with_rotation(_logic, text, target_lang)

    @staticmethod
    def ocr_page(image_bytes):
        def _logic(key, img_data):
            model = config.conf["VisionAssistant"]["model_name"]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
            ocr_image_prompt = get_prompt_text("ocr_image_extract")
            payload = {"contents": [{"parts": [{"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(img_data).decode('utf-8')}}, {"text": ocr_image_prompt}]}]}
            req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json", "x-goog-api-key": key})
            with GeminiHandler._get_opener().open(req, timeout=90) as r:
                return json.loads(r.read().decode())['candidates'][0]['content']['parts'][0]['text']
        return GeminiHandler._call_with_rotation(_logic, image_bytes)

    @staticmethod
    def upload_and_process_batch(file_path, mime_type, page_count):
        keys = GeminiHandler._get_api_keys()
        if not keys: 
            # Translators: Error message for missing API Keys
            return [ "ERROR:" + _("No API Keys.") ]
        model = config.conf["VisionAssistant"]["model_name"]
        
        opener = GeminiHandler._get_opener()
        proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
        base_url = proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"
        
        for i, key in enumerate(keys):
            try:
                f_size = os.path.getsize(file_path)
                init_url = f"{base_url}/upload/v1beta/files"
                headers = {"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start", "X-Goog-Upload-Header-Content-Length": str(f_size), "X-Goog-Upload-Header-Content-Type": mime_type, "Content-Type": "application/json", "x-goog-api-key": key}
                
                req = request.Request(init_url, data=json.dumps({"file": {"display_name": "batch"}}).encode(), headers=headers, method="POST")
                with opener.open(req, timeout=60) as r: upload_url = r.headers.get("x-goog-upload-url")
                
                with open(file_path, 'rb') as f: f_data = f.read()
                req_up = request.Request(upload_url, data=f_data, headers={"Content-Length": str(f_size), "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"}, method="POST")
                with opener.open(req_up, timeout=180) as r:
                    res = json.loads(r.read().decode())
                    uri, name = res['file']['uri'], res['file']['name']
                
                active = False
                for _ in range(30):
                    req_check = request.Request(f"{base_url}/v1beta/{name}", headers={"x-goog-api-key": key})
                    with opener.open(req_check, timeout=30) as r:
                        state = json.loads(r.read().decode()).get('state')
                        if state == "ACTIVE":
                            active = True
                            break
                        if state == "FAILED":
                            break
                    time.sleep(2)

                if not active:
                    if i < len(keys) - 1:
                        continue
                    return [ "ERROR:" + _("Upload failed.") ]

                GeminiHandler._register_file_uri(uri, key)
                
                url = f"{base_url}/v1beta/models/{model}:generateContent"
                prompt = get_prompt_text("ocr_document_extract")
                contents = [{"parts": [{"file_data": {"mime_type": mime_type, "file_uri": uri}}, {"text": prompt}]}]
                
                req_gen = request.Request(url, data=json.dumps({"contents": contents}).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
                with opener.open(req_gen, timeout=180) as r:
                    res = json.loads(r.read().decode())
                    text = res['candidates'][0]['content']['parts'][0]['text']
                    return text.split('[[[PAGE_SEP]]]')
                    
            except error.HTTPError as e:
                err_code = GeminiHandler._handle_error(e)
                if err_code in ["QUOTA_EXCEEDED", "SERVER_ERROR"] and i < len(keys) - 1:
                    continue
                if err_code == "QUOTA_EXCEEDED":
                    # Translators: Message of a dialog which may pop up while performing an AI call
                    err_msg = _("Error 429: Quota Exceeded (Try later)")
                elif err_code == "SERVER_ERROR":
                    # Translators: Message of a dialog which may pop up while performing an AI call
                    err_msg = _("Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
                else:
                    err_msg = err_code
                return ["ERROR:" + err_msg]
            except Exception as e:
                return ["ERROR:" + str(e)]
        return ["ERROR:" + _("All keys failed.")]

    @staticmethod
    def chat(history, new_msg, file_uri, mime_type):
        def _logic(key, hist, msg, uri, mime):
            model = config.conf["VisionAssistant"]["model_name"]
            proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
            base_url = proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"
            url = f"{base_url}/v1beta/models/{model}:generateContent"
            
            contents = list(hist)
            if uri: 
                user_parts = [{"file_data": {"mime_type": mime, "file_uri": uri}}]
            else:
                user_parts = []
            user_parts.append({"text": msg})
            contents.append({"role": "user", "parts": user_parts})
            
            req = request.Request(url, data=json.dumps({"contents": contents}).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": key})
            with GeminiHandler._get_opener().open(req, timeout=90) as r:
                return json.loads(r.read().decode())['candidates'][0]['content']['parts'][0]['text']
        forced_key = GeminiHandler._get_registered_key(file_uri) if file_uri else None
        if forced_key:
            return GeminiHandler._call_with_key(_logic, forced_key, history, new_msg, file_uri, mime_type)
        return GeminiHandler._call_with_rotation(_logic, history, new_msg, file_uri, mime_type)

    @staticmethod
    def upload_for_chat(file_path, mime_type):
        keys = GeminiHandler._get_api_keys()
        if not keys: return None
        opener = GeminiHandler._get_opener()
        proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
        base_url = proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"
        
        for key in keys:
            try:
                f_size = os.path.getsize(file_path)
                init_url = f"{base_url}/upload/v1beta/files"
                headers = {"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start", "X-Goog-Upload-Header-Content-Length": str(f_size), "X-Goog-Upload-Header-Content-Type": mime_type, "Content-Type": "application/json", "x-goog-api-key": key}
                req = request.Request(init_url, data=json.dumps({"file": {"display_name": os.path.basename(file_path)}}).encode(), headers=headers, method="POST")
                with opener.open(req, timeout=60) as r: upload_url = r.headers.get("x-goog-upload-url")
                with open(file_path, 'rb') as f: f_data = f.read()
                req_up = request.Request(upload_url, data=f_data, headers={"Content-Length": str(f_size), "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"}, method="POST")
                with opener.open(req_up, timeout=180) as r:
                    res = json.loads(r.read().decode())
                    uri, name = res['file']['uri'], res['file']['name']
                for _ in range(30):
                    req_check = request.Request(f"{base_url}/v1beta/{name}", headers={"x-goog-api-key": key})
                    with opener.open(req_check, timeout=30) as r:
                        state = json.loads(r.read().decode()).get('state')
                        if state == "ACTIVE":
                            GeminiHandler._register_file_uri(uri, key)
                            return uri
                    time.sleep(2)
                return None 
            except: continue 
        return None

    @staticmethod
    def generate_speech(text, voice_name):
        def _logic(key, txt, voice):
            main_model = config.conf["VisionAssistant"]["model_name"]
            if "pro" in main_model.lower():
                tts_model = "gemini-2.5-pro-preview-tts"
            else:
                tts_model = "gemini-2.5-flash-preview-tts"

            proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
            base_url = proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"
            url = f"{base_url}/v1beta/models/{tts_model}:generateContent"
            
            payload = {
                "contents": [{"parts": [{"text": txt}]}],
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}
                }
            }
            req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json", "x-goog-api-key": key})
            with GeminiHandler._get_opener().open(req, timeout=600) as r:
                res = json.loads(r.read().decode())
                candidates = res.get('candidates', [])
                if not candidates: raise Exception("No candidates returned")
                content = candidates[0].get('content', {})
                parts = content.get('parts', [])
                if not parts: raise Exception("No parts in response")
                part = parts[0]
                if 'inlineData' in part: return part['inlineData']['data']
                if 'inline_data' in part: return part['inline_data']['data']
                if 'text' in part: raise Exception(f"Model refused audio: {part['text']}")
                raise Exception("Unknown response format")
        return GeminiHandler._call_with_rotation(_logic, text, voice_name)

# --- Update Manager ---
class UpdateDialog(wx.Dialog):
    def __init__(self, parent, version, name, changes):
        # Translators: Title of update confirmation dialog
        super().__init__(parent, title=_("Update Available"), size=(500, 450))
        self.Centre()
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Translators: Message asking user to update. {version} is version number.
        msg = _("A new version ({version}) of {name} is available.").format(version=version, name=name)
        header = wx.StaticText(panel, label=msg)
        vbox.Add(header, 0, wx.ALL, 15)
        
        # Translators: Label for the changes text box
        change_lbl = wx.StaticText(panel, label=_("Changes:"))
        vbox.Add(change_lbl, 0, wx.LEFT | wx.RIGHT, 15)
        
        self.changes_ctrl = wx.TextCtrl(panel, value=changes, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        vbox.Add(self.changes_ctrl, 1, wx.EXPAND | wx.ALL, 15)
        
        # Translators: Question to download and install
        question = wx.StaticText(panel, label=_("Download and Install?"))
        vbox.Add(question, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Button to accept update
        self.yes_btn = wx.Button(panel, wx.ID_YES, label=_("&Yes"))
        # Translators: Button to reject update
        self.no_btn = wx.Button(panel, wx.ID_NO, label=_("&No"))
        
        btn_sizer.Add(self.yes_btn, 0, wx.RIGHT, 10)
        btn_sizer.Add(self.no_btn, 0)
        vbox.Add(btn_sizer, 0, wx.ALIGN_RIGHT | wx.ALL, 15)
        
        panel.SetSizer(vbox)
        self.yes_btn.SetDefault()
        self.yes_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_YES))
        self.no_btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_NO))

class UpdateManager:
    def __init__(self, repo_name):
        self.repo_name = repo_name
        self.current_version = addonHandler.getCodeAddon().manifest['version']

    def check_for_updates(self, silent=True):
        threading.Thread(target=self._check_thread, args=(silent,), daemon=True).start()

    def _check_thread(self, silent):
        try:
            url = f"https://api.github.com/repos/{self.repo_name}/releases/latest"
            req = request.Request(url, headers={"User-Agent": "NVDA-Addon"})
            with request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    latest_tag = data.get("tag_name", "").lstrip("v")
                    if self._compare_versions(latest_tag, self.current_version) > 0:
                        download_url = None
                        for asset in data.get("assets", []):
                            if asset["name"].endswith(".nvda-addon"):
                                download_url = asset["browser_download_url"]
                                break
                        if download_url:
                            raw_changes = data.get("body", "")
                            
                            clean_changes = re.split(r'SHA256|Checklist|---', raw_changes, flags=re.I)[0].strip()
                            clean_changes = clean_markdown(clean_changes)
                            
                            wx.CallAfter(self._prompt_update, latest_tag, download_url, clean_changes)
                        elif not silent:
                            msg = _("Update found but no .nvda-addon file in release.")
                            show_error_dialog(msg)
                    elif not silent:
                        msg = _("You have the latest version.")
                        wx.CallAfter(ui.message, msg)
        except Exception as e:
            if not silent:
                msg = _("Update check failed: {error}").format(error=e)
                show_error_dialog(msg)

    def _compare_versions(self, v1, v2):
        try:
            parts1 = [int(x) for x in v1.split('.')]
            parts2 = [int(x) for x in v2.split('.')]
            return (parts1 > parts2) - (parts1 < parts2)
        except: return 0 if v1 == v2 else 1

    def _prompt_update(self, version, url, changes):
        dlg = UpdateDialog(gui.mainFrame, version, ADDON_NAME, changes)
        if dlg.ShowModal() == wx.ID_YES:
            threading.Thread(target=self._download_install_worker, args=(url,), daemon=True).start()
        dlg.Destroy()

    def _download_install_worker(self, url):
        try:
            # Translators: Message shown while downloading update
            msg = _("Downloading update...")
            wx.CallAfter(ui.message, msg)
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, "VisionAssistant_Update.nvda-addon")
            with request.urlopen(url) as response, open(file_path, 'wb') as out_file:
                out_file.write(response.read())
            wx.CallAfter(os.startfile, file_path)
        except Exception as e:
            # Translators: Error message for download failure
            msg = _("Download failed: {error}").format(error=e)
            show_error_dialog(msg)

# --- UI Classes ---


class VisionQADialog(wx.Dialog):
    def __init__(self, parent, title, initial_text, context_data, callback_fn, extra_info=None, raw_content=None, status_callback=None, announce_on_open=True, allow_questions=True):
        super(VisionQADialog, self).__init__(parent, title=title, size=(550, 500), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.context_data = context_data 
        self.callback_fn = callback_fn
        self.extra_info = extra_info
        self.chat_history = [] 
        self.raw_content = raw_content
        self.status_callback = status_callback
        self.announce_on_open = announce_on_open
        self.allow_questions = allow_questions
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: Label for the AI response text area in a chat dialog
        lbl_text = _("AI Response:")
        lbl = wx.StaticText(self, label=lbl_text)
        mainSizer.Add(lbl, 0, wx.ALL, 5)
        self.outputArea = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        mainSizer.Add(self.outputArea, 1, wx.EXPAND | wx.ALL, 5)
        
        self.should_clean = config.conf["VisionAssistant"]["clean_markdown_chat"]
        display_text = clean_markdown(initial_text) if self.should_clean else initial_text
        if display_text:
            # Translators: Format for displaying AI message in a chat dialog
            init_msg = _("AI: {text}\n").format(text=display_text)
            self.outputArea.AppendText(init_msg)
            if config.conf["VisionAssistant"]["copy_to_clipboard"]:
                api.copyToClip(raw_content if raw_content else display_text)
        
        if not (extra_info and extra_info.get('skip_init_history')):
             self.chat_history.append({"role": "model", "parts": [{"text": initial_text}]})

        self.inputArea = None
        if allow_questions:
            # Translators: Label for user input field in a chat dialog
            ask_text = _("Ask:")
            inputLbl = wx.StaticText(self, label=ask_text)
            mainSizer.Add(inputLbl, 0, wx.ALL, 5)
            self.inputArea = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(-1, 30))
            mainSizer.Add(self.inputArea, 0, wx.EXPAND | wx.ALL, 5)
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.askBtn = None
        if allow_questions:
            # Translators: Button to send message in a chat dialog
            self.askBtn = wx.Button(self, label=_("Send"))
        # Translators: Button to view the content in a formatted HTML window
        self.viewBtn = wx.Button(self, label=_("View Formatted"))
        self.viewBtn.Bind(wx.EVT_BUTTON, self.onView)
        # Translators: Button to save only the result content without chat history
        self.saveContentBtn = wx.Button(self, label=_("Save Content"))
        self.saveContentBtn.Bind(wx.EVT_BUTTON, self.onSaveContent)
        # Translators: Button to save chat in a chat dialog
        self.saveBtn = wx.Button(self, label=_("Save Chat"))
        # Translators: Button to close chat dialog
        self.closeBtn = wx.Button(self, wx.ID_CANCEL, label=_("Close"))
        
        self.saveBtn.Enable(bool(initial_text.strip()))
        self.viewBtn.Enable(bool(self.raw_content))
        self.saveContentBtn.Enable(bool(self.raw_content))

        if self.askBtn:
            btnSizer.Add(self.askBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.viewBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.saveContentBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.saveBtn, 0, wx.ALL, 5)
        btnSizer.Add(self.closeBtn, 0, wx.ALL, 5)
        mainSizer.Add(btnSizer, 0, wx.ALIGN_RIGHT)
        
        self.SetSizer(mainSizer)
        if self.inputArea:
            self.inputArea.SetFocus()
        else:
            self.outputArea.SetFocus()
        if self.askBtn:
            self.askBtn.Bind(wx.EVT_BUTTON, self.onAsk)
        self.saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
        if self.inputArea:
            self.inputArea.Bind(wx.EVT_TEXT_ENTER, self.onAsk)
        if display_text and self.announce_on_open:
            wx.CallLater(300, ui.message, display_text)

    def onAsk(self, event):
        if not self.inputArea:
            return
        question = self.inputArea.Value
        if not question.strip(): return
        # Translators: Format for displaying User message in a chat dialog
        user_msg = _("\nYou: {text}\n").format(text=question)
        self.outputArea.AppendText(user_msg)
        self.inputArea.Clear()
        # Translators: Message shown while processing in a chat dialog
        msg = _("Thinking...")
        ui.message(msg)
        threading.Thread(target=self.process_question, args=(question,), daemon=True).start()

    def process_question(self, question):
        result_tuple = self.callback_fn(self.context_data, question, self.chat_history, self.extra_info)
        response_text, _ = result_tuple
        if response_text:
            if not (self.extra_info and self.extra_info.get('file_context')):
                 self.chat_history.append({"role": "user", "parts": [{"text": question}]})
                 self.chat_history.append({"role": "model", "parts": [{"text": response_text}]})
            final_text = clean_markdown(response_text) if self.should_clean else response_text
            wx.CallAfter(self.update_response, final_text, response_text)

    def update_response(self, display_text, raw_text=None):
        if raw_text:
            self.raw_content = raw_text
            self.viewBtn.Enable(True)
            self.saveContentBtn.Enable(True)
        # Translators: Format for displaying AI message in a chat dialog
        ai_msg = _("AI: {text}\n").format(text=display_text)
        self.outputArea.AppendText(ai_msg)
        self.saveBtn.Enable(True)
        if config.conf["VisionAssistant"]["copy_to_clipboard"]:
            api.copyToClip(raw_text if raw_text else display_text)
        self.outputArea.ShowPosition(self.outputArea.GetLastPosition())
        ui.message(display_text)

    def report_save(self, msg):
        if self.status_callback: self.status_callback(msg)
        else: ui.message(msg)

    def onView(self, event):
        full_html = ""
        # Translators: Format for displaying User message in a chat dialog
        user_label = _("\nYou: {text}\n").format(text="").strip()
        # Translators: Format for displaying AI message in a chat dialog
        ai_label = _("AI: {text}\n").format(text="").strip()
        
        if self.chat_history:
            for item in self.chat_history:
                role = item.get("role", "")
                text = item.get("parts", [{}])[0].get("text", "")
                if role == "user":
                    safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    full_html += f"<h2>{user_label}</h2><p>{safe_text}</p>"
                elif role == "model":
                    formatted_text = markdown_to_html(text, full_page=False)
                    full_html += f"<h2>{ai_label}</h2>{formatted_text}<hr>"
        
        if not full_html and self.raw_content:
             formatted_text = markdown_to_html(self.raw_content, full_page=False)
             full_html += f"<h2>{ai_label}</h2>{formatted_text}"

        if not full_html: return
        try:
            # Translators: Title of the formatted result window
            ui.browseableMessage(full_html, _("Formatted Conversation"), isHtml=True)
        except Exception as e:
            # Translators: Error message if viewing fails
            msg = _("Error displaying content: {error}").format(error=e)
            show_error_dialog(msg)

    def onSave(self, event):
        # Translators: Save dialog title
        path = get_file_path(_("Save Chat Log"), "Text files (*.txt)|*.txt", mode="save")
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f: f.write(self.outputArea.GetValue())
                # Translators: Message on successful save
                self.report_save(_("Saved."))
            except Exception as e:
                # Translators: Message in the error dialog when saving fails.
                msg = _("Save failed: {error}").format(error=e)
                show_error_dialog(msg)

    def onSaveContent(self, event):
        # Translators: Save dialog title
        path = get_file_path(_("Save Result"), "HTML files (*.html)|*.html", mode="save")
        if path:
            try:
                full_html = markdown_to_html(self.raw_content, full_page=True)
                with open(path, "w", encoding="utf-8") as f: f.write(full_html)
                # Translators: Message on successful save
                self.report_save(_("Saved."))
            except Exception as e:
                # Translators: Message in the error dialog when saving fails.
                msg = _("Save failed: {error}").format(error=e)
                show_error_dialog(msg)

class SettingsPanel(gui.settingsDialogs.SettingsPanel):
    title = ADDON_NAME
    def makeSettings(self, settingsSizer):
        # --- Connection Group ---
        # Translators: Title of the settings group for connection and updates
        groupLabel = _("Connection")
        self.connectionBox = wx.StaticBox(self, label=groupLabel)
        connectionSizer = wx.StaticBoxSizer(self.connectionBox, wx.VERTICAL)
        cHelper = gui.guiHelper.BoxSizerHelper(self.connectionBox, sizer=connectionSizer)

        # Translators: Label for API Key input
        apiLabel = wx.StaticText(self.connectionBox, label=_("Gemini API Key (Separate multiple keys with comma or newline):"))
        cHelper.addItem(apiLabel)
        
        api_value = config.conf["VisionAssistant"]["api_key"]
        
        self.apiKeyCtrl_hidden = wx.TextCtrl(self.connectionBox, value=api_value, style=wx.TE_PASSWORD, size=(-1, -1))
        
        self.apiKeyCtrl_visible = wx.TextCtrl(self.connectionBox, value=api_value, style=wx.TE_MULTILINE | wx.TE_DONTWRAP, size=(-1, 60))
        self.apiKeyCtrl_visible.Hide()
        
        cHelper.addItem(self.apiKeyCtrl_hidden)
        cHelper.addItem(self.apiKeyCtrl_visible)
        
        # Translators: Checkbox to toggle API Key visibility
        self.showApiCheck = wx.CheckBox(self.connectionBox, label=_("Show API Key"))
        self.showApiCheck.Bind(wx.EVT_CHECKBOX, self.onToggleApiVisibility)
        cHelper.addItem(self.showApiCheck)
        
        model_display_names = [opt[0] for opt in MODELS]
        # Translators: Label for Model selection
        self.model = cHelper.addLabeledControl(_("AI Model:"), wx.Choice, choices=model_display_names)
        current_id = config.conf["VisionAssistant"]["model_name"]
        try:
            index = next(i for i, v in enumerate(MODELS) if v[1] == current_id)
            self.model.SetSelection(index)
        except StopIteration: self.model.SetSelection(0)

        # Translators: Label for Proxy URL input
        self.proxyUrl = cHelper.addLabeledControl(_("Proxy URL:"), wx.TextCtrl)
        self.proxyUrl.Value = config.conf["VisionAssistant"]["proxy_url"]

        # Translators: Checkbox to enable/disable automatic update checks on NVDA startup
        self.checkUpdateStartup = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Check for updates on startup")))
        self.checkUpdateStartup.Value = config.conf["VisionAssistant"]["check_update_startup"]
        # Translators: Checkbox to toggle markdown cleaning in chat windows
        self.cleanMarkdown = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Clean Markdown in Chat")))
        self.cleanMarkdown.Value = config.conf["VisionAssistant"]["clean_markdown_chat"]
        # Translators: Checkbox to enable copying AI responses to clipboard
        self.copyToClipboard = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Copy AI responses to clipboard")))
        self.copyToClipboard.Value = config.conf["VisionAssistant"]["copy_to_clipboard"]
        # Translators: Checkbox to skip chat window and only speak AI responses
        self.skipChatDialog = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Direct Output (No Chat Window)")))
        self.skipChatDialog.Value = config.conf["VisionAssistant"]["skip_chat_dialog"]
        settingsSizer.Add(connectionSizer, 0, wx.EXPAND | wx.ALL, 5)

        # --- Translation Languages Group ---
        # Translators: Title of the settings group for translation languages configuration
        groupLabel = _("Translation Languages")
        langBox = wx.StaticBox(self, label=groupLabel)
        langSizer = wx.StaticBoxSizer(langBox, wx.VERTICAL)
        lHelper = gui.guiHelper.BoxSizerHelper(langBox, sizer=langSizer)

        # Translators: Label for Source Language selection
        self.sourceLang = lHelper.addLabeledControl(_("Source:"), wx.Choice, choices=SOURCE_NAMES)
        try: self.sourceLang.SetSelection(SOURCE_NAMES.index(config.conf["VisionAssistant"]["source_language"]))
        except: self.sourceLang.SetSelection(0)
        
        # Translators: Label for Target Language selection
        self.targetLang = lHelper.addLabeledControl(_("Target:"), wx.Choice, choices=TARGET_NAMES)
        try: self.targetLang.SetSelection(TARGET_NAMES.index(config.conf["VisionAssistant"]["target_language"]))
        except: self.targetLang.SetSelection(0)
        
        # Translators: Label for AI Response Language selection
        self.aiResponseLang = lHelper.addLabeledControl(_("AI Response:"), wx.Choice, choices=TARGET_NAMES)
        try: self.aiResponseLang.SetSelection(TARGET_NAMES.index(config.conf["VisionAssistant"]["ai_response_language"]))
        except: self.aiResponseLang.SetSelection(0)

        # Translators: Checkbox for Smart Swap feature
        self.smartSwap = lHelper.addItem(wx.CheckBox(langBox, label=_("Smart Swap")))
        self.smartSwap.Value = config.conf["VisionAssistant"]["smart_swap"]
        settingsSizer.Add(langSizer, 0, wx.EXPAND | wx.ALL, 5)

        # --- Document Reader Settings ---
        # Translators: Title of settings group for Document Reader features
        groupLabel = _("Document Reader")
        docBox = wx.StaticBox(self, label=groupLabel)
        docSizer = wx.StaticBoxSizer(docBox, wx.VERTICAL)
        dHelper = gui.guiHelper.BoxSizerHelper(docBox, sizer=docSizer)

        # Translators: Label for OCR Engine selection
        self.ocr_sel = dHelper.addLabeledControl(_("OCR Engine:"), wx.Choice, choices=[x[0] for x in OCR_ENGINES])
        curr_ocr = config.conf["VisionAssistant"]["ocr_engine"]
        try:
            o_idx = next(i for i, v in enumerate(OCR_ENGINES) if v[1] == curr_ocr)
            self.ocr_sel.SetSelection(o_idx)
        except: self.ocr_sel.SetSelection(0)

        voice_choices = [f"{v[0]} - {v[1]}" for v in GEMINI_VOICES]
        # Translators: Label for TTS Voice selection
        self.voice_sel = dHelper.addLabeledControl(_("TTS Voice:"), wx.Choice, choices=voice_choices)
        curr_voice = config.conf["VisionAssistant"]["tts_voice"]
        try:
            v_idx = next(i for i, v in enumerate(GEMINI_VOICES) if v[0] == curr_voice)
            self.voice_sel.SetSelection(v_idx)
        except: self.voice_sel.SetSelection(1)
        settingsSizer.Add(docSizer, 0, wx.EXPAND | wx.ALL, 5)

        # --- CAPTCHA Group ---
        # Translators: Title of the settings group for CAPTCHA options
        groupLabel = _("CAPTCHA")
        capBox = wx.StaticBox(self, label=groupLabel)
        capSizer = wx.StaticBoxSizer(capBox, wx.VERTICAL)
        capHelper = gui.guiHelper.BoxSizerHelper(capBox, sizer=capSizer)
        # Translators: Label for CAPTCHA capture method selection
        self.captchaMode = capHelper.addLabeledControl(_("Capture Method:"), wx.Choice, choices=[
            # Translators: A choice for capture method. Captures only the specific object under the NVDA navigator cursor.
            _("Navigator Object"),
            # Translators: A choice for capture method. Captures the entire visible screen area.
            _("Full Screen")
        ])
        self.captchaMode.SetSelection(0 if config.conf["VisionAssistant"]["captcha_mode"] == 'navigator' else 1)
        settingsSizer.Add(capSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.defaultPromptItems = get_configured_default_prompts()
        self.customPromptItems = load_configured_custom_prompts()

        # --- Prompt Manager Group ---
        # Translators: Title of the settings group for prompt management
        groupLabel = _("Prompts")
        promptsBox = wx.StaticBox(self, label=groupLabel)
        promptsSizer = wx.StaticBoxSizer(promptsBox, wx.VERTICAL)
        pHelper = gui.guiHelper.BoxSizerHelper(promptsBox, sizer=promptsSizer)
        # Translators: Description for the prompt manager button.
        pHelper.addItem(wx.StaticText(promptsBox, label=_("Manage default system prompts and custom refine prompts.")))
        # Translators: Button label to open prompt manager dialog.
        self.managePromptsBtn = wx.Button(promptsBox, label=_("Manage Prompts..."))
        self.managePromptsBtn.Bind(wx.EVT_BUTTON, self.onManagePrompts)
        pHelper.addItem(self.managePromptsBtn)
        self.promptsSummary = wx.StaticText(promptsBox)
        pHelper.addItem(self.promptsSummary)
        self._refreshPromptSummary()
        settingsSizer.Add(promptsSizer, 0, wx.EXPAND | wx.ALL, 5)

    def _refreshPromptSummary(self):
        # Translators: Summary text for prompt counts in settings.
        summary = _("Default prompts: {defaultCount}, Custom prompts: {customCount}").format(
            defaultCount=len(self.defaultPromptItems),
            customCount=len(self.customPromptItems),
        )
        self.promptsSummary.SetLabel(summary)

    def onManagePrompts(self, event):
        top = wx.GetTopLevelParent(self)
        dlg = PromptManagerDialog(
            self,
            self.defaultPromptItems,
            self.customPromptItems,
            PROMPT_VARIABLES_GUIDE,
        )
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.defaultPromptItems = dlg.get_default_items()
                self.customPromptItems = dlg.get_custom_items()
                self._refreshPromptSummary()
        finally:
            dlg.Destroy()
            if top:
                top.Enable(True)
                top.SetFocus()

    def onToggleApiVisibility(self, event):
        if self.showApiCheck.IsChecked():
            self.apiKeyCtrl_visible.SetValue(self.apiKeyCtrl_hidden.GetValue())
            self.apiKeyCtrl_hidden.Hide()
            self.apiKeyCtrl_visible.Show()
        else:
            self.apiKeyCtrl_hidden.SetValue(self.apiKeyCtrl_visible.GetValue())
            self.apiKeyCtrl_visible.Hide()
            self.apiKeyCtrl_hidden.Show()
        
        self.connectionBox.GetParent().Layout()

    def onSave(self):
        val = self.apiKeyCtrl_visible.GetValue() if self.showApiCheck.IsChecked() else self.apiKeyCtrl_hidden.GetValue()
        config.conf["VisionAssistant"]["api_key"] = val.strip()
        config.conf["VisionAssistant"]["model_name"] = MODELS[self.model.GetSelection()][1]
        config.conf["VisionAssistant"]["proxy_url"] = self.proxyUrl.Value.strip()
        config.conf["VisionAssistant"]["source_language"] = SOURCE_NAMES[self.sourceLang.GetSelection()]
        config.conf["VisionAssistant"]["target_language"] = TARGET_NAMES[self.targetLang.GetSelection()]
        config.conf["VisionAssistant"]["ai_response_language"] = TARGET_NAMES[self.aiResponseLang.GetSelection()]
        config.conf["VisionAssistant"]["smart_swap"] = self.smartSwap.Value
        config.conf["VisionAssistant"]["check_update_startup"] = self.checkUpdateStartup.Value
        config.conf["VisionAssistant"]["clean_markdown_chat"] = self.cleanMarkdown.Value
        config.conf["VisionAssistant"]["copy_to_clipboard"] = self.copyToClipboard.Value
        config.conf["VisionAssistant"]["skip_chat_dialog"] = self.skipChatDialog.Value
        config.conf["VisionAssistant"]["captcha_mode"] = 'navigator' if self.captchaMode.GetSelection() == 0 else 'fullscreen'
        config.conf["VisionAssistant"]["custom_prompts_v2"] = serialize_custom_prompts_v2(self.customPromptItems)
        config.conf["VisionAssistant"]["custom_prompts"] = ""
        config.conf["VisionAssistant"]["default_refine_prompts"] = serialize_default_prompt_overrides(self.defaultPromptItems)
        config.conf["VisionAssistant"]["ocr_engine"] = OCR_ENGINES[self.ocr_sel.GetSelection()][1]
        config.conf["VisionAssistant"]["tts_voice"] = GEMINI_VOICES[self.voice_sel.GetSelection()][0]

class RangeDialog(wx.Dialog):
    def __init__(self, parent, total_pages):
        # Translators: Title of the PDF options dialog
        super().__init__(parent, title=_("Options"), size=(350, 320))
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: Label showing total pages found
        sizer.Add(wx.StaticText(self, label=_("Total Pages (All Files): {count}").format(count=total_pages)), 0, wx.ALL, 10)
        
        # Translators: Box title for page range selection
        box_range = wx.StaticBoxSizer(wx.VERTICAL, self, _("Range"))
        g_sizer = wx.FlexGridSizer(2, 2, 10, 10)
        # Translators: Label for start page
        g_sizer.Add(wx.StaticText(self, label=_("From:")), 0, wx.ALIGN_CENTER_VERTICAL)
        self.spin_from = wx.SpinCtrl(self, min=1, max=total_pages, initial=1)
        g_sizer.Add(self.spin_from, 1, wx.EXPAND)
        # Translators: Label for end page
        g_sizer.Add(wx.StaticText(self, label=_("To:")), 0, wx.ALIGN_CENTER_VERTICAL)
        self.spin_to = wx.SpinCtrl(self, min=1, max=total_pages, initial=total_pages)
        g_sizer.Add(self.spin_to, 1, wx.EXPAND)
        box_range.Add(g_sizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(box_range, 0, wx.EXPAND | wx.ALL, 10)

        # Translators: Box title for translation options
        box_trans = wx.StaticBoxSizer(wx.VERTICAL, self, _("Translation"))
        # Translators: Checkbox to enable translation
        self.chk_trans = wx.CheckBox(self, label=_("Translate Output"))
        box_trans.Add(self.chk_trans, 0, wx.ALL, 5)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Label for target language
        h_sizer.Add(wx.StaticText(self, label=_("Target:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.cmb_lang = wx.Choice(self, choices=TARGET_NAMES)
        self.cmb_lang.SetSelection(0)
        h_sizer.Add(self.cmb_lang, 1)
        box_trans.Add(h_sizer, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(box_trans, 0, wx.EXPAND | wx.ALL, 10)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Button to start processing
        btn_ok = wx.Button(self, wx.ID_OK, label=_("Start"))
        btn_ok.SetDefault()
        # Translators: Button to cancel
        btn_cancel = wx.Button(self, wx.ID_CANCEL, label=_("Cancel"))
        btn_sizer.Add(btn_ok, 0, wx.RIGHT, 10)
        btn_sizer.Add(btn_cancel, 0)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)

        self.chk_trans.Bind(wx.EVT_CHECKBOX, self.on_check)
        self.cmb_lang.Disable()

    def on_check(self, event):
        self.cmb_lang.Enable(self.chk_trans.IsChecked())

    def get_settings(self):
        return {
            'start': self.spin_from.GetValue() - 1,
            'end': self.spin_to.GetValue() - 1,
            'translate': self.chk_trans.IsChecked(),
            'lang': TARGET_NAMES[self.cmb_lang.GetSelection()]
        }

class ChatDialog(wx.Dialog):
    instance = None

    def __init__(self, parent, file_path):
        # Translators: Title of the chat dialog
        super().__init__(parent, title=_("Ask about Document"), size=(600, 500), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        ChatDialog.instance = self
        self.file_path = file_path
        self.file_uri = None
        self.mime_type = get_mime_type(file_path)
        self.history = []
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: Label showing the analyzed file name
        lbl_info = wx.StaticText(self, label=_("File: {name}").format(name=os.path.basename(file_path)))
        sizer.Add(lbl_info, 0, wx.ALL, 5)
        self.display = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        sizer.Add(self.display, 1, wx.EXPAND | wx.ALL, 10)
        # Translators: Status message while uploading
        self.display.SetValue(_("Uploading to Gemini...\n"))
        
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Label for the chat input field
        input_sizer.Add(wx.StaticText(self, label=_("Your Question:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(-1, 30))
        self.input.Bind(wx.EVT_TEXT_ENTER, self.on_send)
        input_sizer.Add(self.input, 1, wx.EXPAND | wx.RIGHT, 5)
        
        # Translators: Button to send message
        self.btn_send = wx.Button(self, label=_("Send"))
        self.btn_send.Bind(wx.EVT_BUTTON, self.on_send)
        self.btn_send.Disable()
        input_sizer.Add(self.btn_send, 0)
        sizer.Add(input_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        threading.Thread(target=self.init_upload, daemon=True).start()

    def on_close(self, event):
        ChatDialog.instance = None
        self.Destroy()

    def init_upload(self):
        uri = GeminiHandler.upload_for_chat(self.file_path, self.mime_type)
        if uri and not str(uri).startswith("ERROR:"):
            self.file_uri = uri
            wx.CallAfter(self.on_ready)
        else:
            err_msg = str(uri)[6:] if uri else _("Upload failed.")
            wx.CallAfter(show_error_dialog, err_msg)
            wx.CallAfter(self.Close)

    def on_ready(self):
        # Translators: Message when ready to chat
        self.display.AppendText(_("Ready! Ask your questions.\n"))
        self.btn_send.Enable()
        self.input.SetFocus()

    def on_send(self, event):
        msg = self.input.GetValue().strip()
        if not msg: return
        self.input.Clear()
        self.display.AppendText(f"You: {msg}\n")
        # Translators: Message showing AI is thinking
        ui.message(_("Thinking..."))
        threading.Thread(target=self.do_chat, args=(msg,), daemon=True).start()

    def do_chat(self, msg):
        resp = GeminiHandler.chat(self.history, msg, self.file_uri, self.mime_type)
        
        if str(resp).startswith("ERROR:"):
            show_error_dialog(resp[6:])
            if _vision_assistant_instance:
                # Translators: Initial status when the add-on is doing nothing
                _vision_assistant_instance.current_status = _("Idle")
            return

        self.history.append({"role": "user", "parts": [{"text": msg}]})
        self.history.append({"role": "model", "parts": [{"text": resp}]})
        wx.CallAfter(self.display.AppendText, f"AI: {resp}\n\n")
        # Translators: Spoken prefix for AI response
        wx.CallAfter(ui.message, _("AI: ") + resp)

class DocumentViewerDialog(wx.Dialog):
    def __init__(self, parent, virtual_doc, settings):
        super().__init__(parent, title=ADDON_NAME, size=(800, 600), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        self.v_doc = virtual_doc
        self.start_page = settings['start']
        self.end_page = settings['end']
        self.do_translate = settings['translate']
        self.target_lang = settings['lang']
        self.range_count = self.end_page - self.start_page + 1
        self.page_cache = {}
        self.current_page = self.start_page
        self.thread_pool = ThreadPoolExecutor(max_workers=5)
        
        self.init_ui()
        self.Centre()
        threading.Thread(target=self.start_auto_processing, daemon=True).start()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        # Translators: Initial status message
        self.lbl_status = wx.StaticText(panel, label=_("Initializing..."))
        vbox.Add(self.lbl_status, 0, wx.ALL, 5)
        self.txt_content = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        vbox.Add(self.txt_content, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        hbox_nav = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Button to go to previous page
        self.btn_prev = wx.Button(panel, label=_("Previous (Ctrl+PageUp)"))
        self.btn_prev.Bind(wx.EVT_BUTTON, self.on_prev)
        hbox_nav.Add(self.btn_prev, 0, wx.RIGHT, 5)
        # Translators: Button to go to next page
        self.btn_next = wx.Button(panel, label=_("Next (Ctrl+PageDown)"))
        self.btn_next.Bind(wx.EVT_BUTTON, self.on_next)
        hbox_nav.Add(self.btn_next, 0, wx.RIGHT, 15)
        # Translators: Label for Go To Page
        hbox_nav.Add(wx.StaticText(panel, label=_("Go to:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        choices = [str(i+1) for i in range(self.start_page, self.end_page + 1)]
        self.cmb_pages = wx.Choice(panel, choices=choices)
        self.cmb_pages.Bind(wx.EVT_CHOICE, self.on_page_select)
        hbox_nav.Add(self.cmb_pages, 0, wx.RIGHT, 15)
        vbox.Add(hbox_nav, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        hbox_actions = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Button to Ask questions about the document
        self.btn_ask = wx.Button(panel, label=_("Ask AI (Alt+A)"))
        self.btn_ask.Bind(wx.EVT_BUTTON, self.on_ask)
        hbox_actions.Add(self.btn_ask, 0, wx.RIGHT, 5)
        
        # Translators: Button to force re-scan
        self.btn_gemini = wx.Button(panel, label=_("Re-scan with Gemini (Alt+R)"))
        self.btn_gemini.Bind(wx.EVT_BUTTON, self.on_gemini_scan)
        hbox_actions.Add(self.btn_gemini, 0, wx.RIGHT, 5)
        
        # Translators: Button to generate audio
        self.btn_tts = wx.Button(panel, label=_("Generate Audio (Alt+G)"))
        self.btn_tts.Bind(wx.EVT_BUTTON, self.on_tts)
        hbox_actions.Add(self.btn_tts, 0, wx.RIGHT, 5)

        # Translators: Button to view formatted content
        self.btn_view = wx.Button(panel, label=_("View Formatted"))
        self.btn_view.Bind(wx.EVT_BUTTON, self.on_view)
        hbox_actions.Add(self.btn_view, 0, wx.RIGHT, 5)

        # Translators: Button to save text
        self.btn_save = wx.Button(panel, label=_("Save (Alt+S)"))
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save_all)
        hbox_actions.Add(self.btn_save, 0)
        
        vbox.Add(hbox_actions, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        btn_close = wx.Button(panel, wx.ID_CLOSE, label=_("Close"))
        btn_close.Bind(wx.EVT_BUTTON, lambda e: self.Destroy())
        vbox.Add(btn_close, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        panel.SetSizer(vbox)
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_CTRL, wx.WXK_PAGEDOWN, self.btn_next.GetId()),
            (wx.ACCEL_CTRL, wx.WXK_PAGEUP, self.btn_prev.GetId()),
            (wx.ACCEL_CTRL, ord('S'), self.btn_save.GetId()),
            (wx.ACCEL_ALT, ord('S'), self.btn_save.GetId()),
            (wx.ACCEL_ALT, ord('A'), self.btn_ask.GetId()),
            (wx.ACCEL_ALT, ord('R'), self.btn_gemini.GetId()),
            (wx.ACCEL_ALT, ord('G'), self.btn_tts.GetId())
        ])
        self.SetAcceleratorTable(accel_tbl)
        self.cmb_pages.SetSelection(0)
        self.update_view()
        self.txt_content.SetFocus()

    def start_auto_processing(self):
        engine = config.conf["VisionAssistant"]["ocr_engine"]
        
        if engine == 'gemini':
            threading.Thread(target=self.gemini_scan_batch_thread, daemon=True).start()
        else:
            for i in range(self.start_page, self.end_page + 1):
                self.thread_pool.submit(self.process_page_worker, i)

    def process_page_worker(self, page_num):
        if page_num in self.page_cache: return
        text = self._get_page_text_logic(page_num)
        self.page_cache[page_num] = text
        if page_num == self.current_page:
            wx.CallAfter(self.update_view)
            # Translators: Spoken message when the current page is ready
            wx.CallAfter(ui.message, _("Page {num} ready").format(num=page_num + 1))

    def _get_page_text_logic(self, page_num):
        file_path, page_idx = self.v_doc.get_page_info(page_num)
        if not file_path: return ""
        try:
            doc = fitz.open(file_path)
            page = doc.load_page(page_idx)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img_bytes = pix.tobytes("jpg")
            doc.close()
            engine = config.conf["VisionAssistant"]["ocr_engine"]
            text = None
            if engine == 'gemini':
                try: text = GeminiHandler.ocr_page(img_bytes)
                except: text = None
            if not text or not text.strip() or engine == 'chrome':
                text = ChromeOCREngine.recognize(img_bytes)
                if not text or not text.strip():
                    text = SmartProgrammersOCREngine.recognize(img_bytes)
            if not text or not text.strip():
                # Translators: Placeholder text when OCR fails
                text = _("[OCR failed. Try Gemini Re-scan.]")
            if self.do_translate and text and "[OCR failed" not in text:
                if engine == 'gemini':
                    text = GeminiHandler.translate(text, self.target_lang)
                else:
                    text = GoogleTranslator.translate(text, self.target_lang)
            return text
        except: 
            # Translators: Error message for page processing failure
            return _("Error processing page.")

    def update_view(self):
        rel_page = self.current_page - self.start_page + 1
        # Translators: Status label format
        self.lbl_status.SetLabel(_("Page {current} of {total}").format(current=rel_page, total=self.range_count))
        if self.current_page in self.page_cache:
            self.txt_content.SetValue(self.page_cache[self.current_page])
            self.txt_content.SetInsertionPoint(0)
            self.txt_content.SetFocus()
        else:
            # Translators: Status when page is loading
            self.txt_content.SetValue(_("Processing in background..."))
            self.txt_content.SetInsertionPoint(0)
            self.txt_content.SetFocus()
        self.btn_prev.Enable(self.current_page > self.start_page)
        self.btn_next.Enable(self.current_page < self.end_page)

    def load_page(self, page_num):
        if page_num < self.start_page or page_num > self.end_page: return
        self.current_page = page_num
        self.cmb_pages.SetSelection(page_num - self.start_page)
        # Translators: Spoken message when switching pages
        ui.message(_("Page {num}").format(num=page_num + 1))
        self.update_view()

    def on_prev(self, event):
        if self.current_page > self.start_page: self.load_page(self.current_page - 1)

    def on_next(self, event):
        if self.current_page < self.end_page: self.load_page(self.current_page + 1)

    def on_page_select(self, event):
        self.load_page(self.start_page + self.cmb_pages.GetSelection())

    def on_view(self, event):
        full_html = []
        for i in range(self.start_page, self.end_page + 1):
            if i in self.page_cache:
                page_text = self.page_cache[i]
                page_content = markdown_to_html(page_text, full_page=False)
                # Translators: Heading for each page in the formatted content view.
                page_label = _("Page {num}").format(num=i+1)
                full_html.append(f"<h2>{page_label}</h2>")
                full_html.append(page_content)
                full_html.append("<hr>")
        
        if not full_html:
            text = self.txt_content.GetValue()
            if not text: return
            full_html.append(markdown_to_html(text, full_page=False))
        
        combined_html = "".join(full_html)
        try:
            # Translators: Title of the formatted result window
            ui.browseableMessage(combined_html, _("Formatted Content"), isHtml=True)
        except Exception as e:
            show_error_dialog(str(e))

    def on_gemini_scan(self, event):
        if not config.conf["VisionAssistant"]["api_key"]:
            wx.MessageBox(_("Please configure Gemini API Key."), _("Error"), wx.ICON_ERROR)
            return
        menu = wx.Menu()
        # Translators: Menu option for current page
        item_curr = menu.Append(wx.ID_ANY, _("Current Page"))
        # Translators: Menu option for all pages
        item_all = menu.Append(wx.ID_ANY, _("All Pages (In Range)"))
        self.Bind(wx.EVT_MENU, self.do_rescan_current, item_curr)
        self.Bind(wx.EVT_MENU, self.do_rescan_all, item_all)
        self.PopupMenu(menu)
        menu.Destroy()

    def do_rescan_current(self, event):
        if self.current_page in self.page_cache: del self.page_cache[self.current_page]
        self.update_view()
        # Translators: Message during manual scan
        ui.message(_("Scanning with Gemini..."))
        threading.Thread(target=self.gemini_scan_single_thread, args=(self.current_page,), daemon=True).start()

    def gemini_scan_single_thread(self, page_num):
        try:
            file_path, page_idx = self.v_doc.get_page_info(page_num)
            doc = fitz.open(file_path)
            page = doc.load_page(page_idx)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            text = GeminiHandler.ocr_page(pix.tobytes("jpg"))
            doc.close()
            if self.do_translate: text = GeminiHandler.translate(text, self.target_lang)
            self.page_cache[page_num] = text
            if self.current_page == page_num: 
                wx.CallAfter(self.update_view)
                # Translators: Message when scan is complete
                wx.CallAfter(ui.message, _("Scan complete"))
        except: pass

    def do_rescan_all(self, event):
        threading.Thread(target=self.gemini_scan_batch_thread, daemon=True).start()

    def gemini_scan_batch_thread(self):
        # Translators: Message when batch scan starts
        msg = _("Batch Processing Started")
        if _vision_assistant_instance: _vision_assistant_instance.current_status = msg
        wx.CallAfter(ui.message, msg)
        
        for i in range(self.start_page, self.end_page + 1):
            if i in self.page_cache: del self.page_cache[i]
        wx.CallAfter(self.update_view)
        
        upload_path = self.v_doc.create_merged_pdf(self.start_page, self.end_page)
        if not upload_path:
            # Translators: Error message if PDF creation fails
            wx.CallAfter(self.lbl_status.SetLabel, _("Error creating temporary PDF."))
            return

        try:
            count = (self.end_page - self.start_page) + 1
            results = GeminiHandler.upload_and_process_batch(upload_path, "application/pdf", count)
            
            if not results or (len(results) == 1 and str(results[0]).startswith("ERROR:")):
                err_msg = results[0][6:] if results else _("Unknown error")
                wx.CallAfter(ui.message, _("Scan failed: {err}").format(err=err_msg))
                return

            for i, text_part in enumerate(results):
                if i >= count: break
                idx = self.start_page + i
                clean = text_part.strip()
                if self.do_translate:
                    clean = GeminiHandler.translate(clean, self.target_lang)
                self.page_cache[idx] = clean

            wx.CallAfter(self.update_view)
            # Translators: Message when batch scan is complete
            final_msg = _("Batch Scan Complete")
            if _vision_assistant_instance: 
                # Translators: Initial status when the add-on is doing nothing
                _vision_assistant_instance.current_status = _("Idle")
            wx.CallAfter(ui.message, final_msg)
        finally:
            if upload_path and os.path.exists(upload_path):
                try: os.remove(upload_path)
                except: pass

    def on_tts(self, event):
        if not config.conf["VisionAssistant"]["api_key"]:
            wx.MessageBox(_("Please configure Gemini API Key."), _("Error"), wx.ICON_ERROR)
            return
        menu = wx.Menu()
        # Translators: Menu option for TTS current page
        item_curr = menu.Append(wx.ID_ANY, _("Generate for Current Page"))
        # Translators: Menu option for TTS all pages
        item_all = menu.Append(wx.ID_ANY, _("Generate for All Pages (In Range)"))
        self.Bind(wx.EVT_MENU, self.do_tts_current, item_curr)
        self.Bind(wx.EVT_MENU, self.do_tts_all, item_all)
        self.PopupMenu(menu)
        menu.Destroy()

    def do_tts_current(self, event):
        text = self.txt_content.GetValue().strip()
        if not text: 
            # Translators: Error message when text field is empty
            wx.MessageBox(_("No text to read."), "Error")
            return
        self._save_tts(text)

    def do_tts_all(self, event):
        threading.Thread(target=self.tts_batch_thread, daemon=True).start()

    def tts_batch_thread(self):
        full_text = []
        # Translators: Message while gathering text
        wx.CallAfter(ui.message, _("Gathering text for audio..."))
        for i in range(self.start_page, self.end_page + 1):
            while i not in self.page_cache: time.sleep(0.1)
            full_text.append(self.page_cache[i])
        final_text = "\n".join(full_text).strip()
        if not final_text: return
        wx.CallAfter(self._save_tts, final_text)

    def _save_tts(self, text):
        # Translators: File dialog title for saving audio
        path = get_file_path(_("Save Audio"), "MP3 Files (*.mp3)|*.mp3|WAV Files (*.wav)|*.wav", mode="save")
        if path:
            voice = config.conf["VisionAssistant"]["tts_voice"]
            threading.Thread(target=self.tts_worker, args=(text, voice, path), daemon=True).start()

    def tts_worker(self, text, voice, path):
        # Translators: Message while generating audio
        msg = _("Generating Audio...")
        if _vision_assistant_instance: _vision_assistant_instance.current_status = msg
        wx.CallAfter(ui.message, msg)
        try:
            audio_b64 = GeminiHandler.generate_speech(text, voice)
            if not audio_b64 or len(audio_b64) < 100:
                 wx.CallAfter(wx.MessageBox, f"TTS Error: {audio_b64}", "Error", wx.ICON_ERROR)
                 return
            missing_padding = len(audio_b64) % 4
            if missing_padding: audio_b64 += '=' * (4 - missing_padding)
            pcm_data = base64.b64decode(audio_b64)

            if path.lower().endswith(".mp3"):
                import subprocess
                lame_path = os.path.join(os.path.dirname(__file__), "lib", "lame.exe")
                if not os.path.exists(lame_path):
                    wx.CallAfter(wx.MessageBox, _("lame.exe not found in lib folder."), "Error", wx.ICON_ERROR)
                    return
                
                process = subprocess.Popen(
                    [lame_path, "-r", "-s", "24", "-m", "m", "-b", "128", "--bitwidth", "16", "--resample", "24", "-q", "0", "-", path],
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
                )

                process.communicate(input=pcm_data)
            else:
                with wave.open(path, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(24000)
                    wf.writeframes(pcm_data)

            # Translators: Spoken message when audio is saved
            res_msg = _("Audio Saved")
            if _vision_assistant_instance: _vision_assistant_instance.current_status = _("Idle")
            wx.CallAfter(ui.message, res_msg)
            wx.CallAfter(wx.MessageBox, _("Audio file generated and saved successfully."), _("Success"), wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            if _vision_assistant_instance: _vision_assistant_instance.current_status = _("Idle")
            wx.CallAfter(wx.MessageBox, f"TTS Error: {e}", "Error", wx.ICON_ERROR)

    def on_ask(self, event):
        if not config.conf["VisionAssistant"]["api_key"]:
            wx.MessageBox(_("Please configure Gemini API Key."), _("Error"), wx.ICON_ERROR)
            return
        if ChatDialog.instance:
            ChatDialog.instance.Raise()
            ChatDialog.instance.SetFocus()
            return
        file_path, _ = self.v_doc.get_page_info(self.current_page)
        if file_path: 
            dlg = ChatDialog(self, file_path)
            dlg.Show()

    def on_save_all(self, event):
        # Translators: File dialog filter for saving text/html
        wildcard = "Text File (*.txt)|*.txt|HTML File (*.html)|*.html"
        # Translators: File dialog title for saving
        path = get_file_path(_("Save"), wildcard, mode="save")
        if path:
            is_html = path.lower().endswith('.html')
            self.btn_save.Disable()
            threading.Thread(target=self.save_thread, args=(path, is_html), daemon=True).start()

    def save_thread(self, path, is_html):
        full_content = []
        try:
            for i in range(self.start_page, self.end_page + 1):
                # Translators: Message showing save progress
                wx.CallAfter(self.lbl_status.SetLabel, _("Saving Page {num}...").format(num=i+1))
                while i not in self.page_cache: time.sleep(0.1)
                txt = self.page_cache[i]
                if is_html:
                    h = markdown_to_html(txt)
                    if "<body>" in h: h = h.split("<body>")[1].split("</body>")[0]
                    full_content.append(f"<hr><h2>Page {i+1}</h2>{h}")
                else:
                    full_content.append(f"--- Page {i+1} ---\n{txt}\n")
            with open(path, "w", encoding="utf-8") as f:
                if is_html: f.write(f"<html><body>{''.join(full_content)}</body></html>")
                else: f.write("\n".join(full_content))
            # Translators: Status label when save is complete
            wx.CallAfter(self.lbl_status.SetLabel, _("Saved"))
            # Translators: Message box content for successful save
            wx.CallAfter(wx.MessageBox, _("File saved successfully."), _("Success"), wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.CallAfter(wx.MessageBox, f"Save Error: {e}", "Error", wx.ICON_ERROR)
        finally: wx.CallAfter(self.btn_save.Enable)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = ADDON_NAME
    
    last_translation = "" 
    is_recording = False
    temp_audio_file = os.path.join(tempfile.gettempdir(), "vision_dictate.wav")
    
    translation_cache = {}
    _last_source_text = None
    _last_params = None
    update_timer = None
    
    # Translators: Initial status when the add-on is doing nothing
    current_status = _("Idle")

    def __init__(self):
        super(GlobalPlugin, self).__init__()
        global _vision_assistant_instance
        _vision_assistant_instance = self
        try:
            migrate_prompt_config_if_needed()
        except Exception as e:
            log.warning(f"Prompt config migration failed: {e}")
        gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SettingsPanel)
        
        self.updater = UpdateManager(GITHUB_REPO)
        
        self.va_menu = wx.Menu()
        
        # Translators: Menu item for Document Reader
        item_doc = self.va_menu.Append(wx.ID_ANY, _("&Document Reader..."))
        self.va_menu.Bind(wx.EVT_MENU, lambda e: wx.CallAfter(self._open_document_reader), item_doc)
        
        # Translators: Menu item for Audio Transcription
        item_audio = self.va_menu.Append(wx.ID_ANY, _("Transcribe &Audio File..."))
        self.va_menu.Bind(wx.EVT_MENU, lambda e: wx.CallAfter(self._open_audio), item_audio)
        
        # Translators: Menu item for Video Analysis
        item_video = self.va_menu.Append(wx.ID_ANY, _("Analyze &Video URL..."))
        self.va_menu.Bind(wx.EVT_MENU, lambda e: wx.CallAfter(self._open_video_dialog), item_video)
        
        self.va_menu.AppendSeparator()
        
        # Translators: Menu item to open settings
        item_settings = self.va_menu.Append(wx.ID_ANY, _("&Settings..."))
        self.va_menu.Bind(wx.EVT_MENU, self.on_settings_click, item_settings)
        
        # Translators: Menu item to check for updates
        item_update = self.va_menu.Append(wx.ID_ANY, _("Check for &Update"))
        self.va_menu.Bind(wx.EVT_MENU, lambda e: self.updater.check_for_updates(silent=False), item_update)
        
        # Translators: Menu item to open documentation
        item_help = self.va_menu.Append(wx.ID_ANY, _("Docu&mentation"))
        self.va_menu.Bind(wx.EVT_MENU, self.on_help_click, item_help)
        
        # Translators: Menu item for donations
        item_donate = self.va_menu.Append(wx.ID_ANY, _("D&onate"))
        self.va_menu.Bind(wx.EVT_MENU, self.on_donate_click, item_donate)
        
        self.tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
        self.va_submenu_item = self.tools_menu.AppendSubMenu(self.va_menu, _("Vision Assistant"))
        
        self.refine_dlg = None
        self.refine_menu_dlg = None
        self.vision_dlg = None
        self.doc_dlg = None
        self.translation_dlg = None
        self.toggling = False
        
        if config.conf["VisionAssistant"]["check_update_startup"]:
            self.update_timer = wx.CallLater(10000, self.updater.check_for_updates, True)

    def _browse_and_run(self, worker_fn, wildcard, multiple=False):
        # Translators: Standard title for opening a file
        title = _("Open")
        path = get_file_path(title, wildcard, multiple=multiple)
        if path:
            threading.Thread(target=worker_fn, args=(path,), daemon=True).start()


    def _open_document_reader(self):
        # Translators: File dialog filter for supported files
        wc = _("Supported Files") + "|*.pdf;*.jpg;*.jpeg;*.png;*.tif;*.tiff"
        self._browse_and_run(self._scan_and_open, wc, multiple=True)

    def _scan_and_open(self, paths):
        try:
            if not fitz:
                # Translators: Error when PyMuPDF is missing
                wx.CallAfter(wx.MessageBox, _("PyMuPDF library is missing."), "Error", wx.ICON_ERROR)
                return
            v_doc = VirtualDocument(paths)
            v_doc.scan() 
            if v_doc.total_pages == 0:
                 # Translators: Error when no pages found
                 wx.CallAfter(wx.MessageBox, _("No readable pages found."), "Error", wx.ICON_ERROR)
                 return
            if v_doc.total_pages == 1:
                settings = {'start': 0, 'end': 0, 'translate': False, 'lang': TARGET_NAMES[0]}
                wx.CallAfter(lambda: DocumentViewerDialog(gui.mainFrame, v_doc, settings).Show())
            else:
                wx.CallAfter(self._show_range_dialog, v_doc)
        except Exception as e:
            log.error(f"Error opening files: {e}", exc_info=True)

    def _show_range_dialog(self, v_doc):
        range_dlg = RangeDialog(gui.mainFrame, v_doc.total_pages)
        if range_dlg.ShowModal() == wx.ID_OK:
            wx.CallAfter(lambda: DocumentViewerDialog(gui.mainFrame, v_doc, range_dlg.get_settings()).Show())
        range_dlg.Destroy()

    def getScript(self, gesture):
        if not self.toggling:
            return super(GlobalPlugin, self).getScript(gesture)
        
        script = super(GlobalPlugin, self).getScript(gesture)
        if not script:
            script = finally_(self.script_error, self.finish)
        return finally_(script, self.finish)

    def finish(self):
        self.toggling = False
        self.clearGestureBindings()
        self.bindGestures(self.__gestures)

    def script_error(self, gesture):
        tones.beep(120, 100)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Activates the Command Layer for quick access to all features."))
    def script_activateLayer(self, gesture):
        if self.toggling:
            self.script_error(gesture)
            return
        
        self.bindGestures(self.__VisionGestures)
        self.toggling = True
        tones.beep(500, 100)

    def terminate(self):
        global _vision_assistant_instance
        try:
            if hasattr(self, 'va_submenu_item') and self.va_submenu_item:
                self.tools_menu.Remove(self.va_submenu_item.GetId())
            
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SettingsPanel)
            
            if LauncherDialog.instance:
                LauncherDialog.instance.Destroy()
        except: pass
        
        if hasattr(self, 'update_timer') and self.update_timer and self.update_timer.IsRunning():
            self.update_timer.Stop()
        
        for dlg in [self.refine_dlg, self.refine_menu_dlg, self.vision_dlg, self.doc_dlg, self.translation_dlg]:
            if dlg:
                try: dlg.Destroy()
                except: pass
        
        if self.is_recording:
            try:
                ctypes.windll.winmm.mciSendStringW('close all', None, 0, 0)
            except: pass
        
        self.translation_cache = {}
        self._last_source_text = None
        _vision_assistant_instance = None
        gc.collect()

    def report_status(self, msg):
        self.current_status = msg
        ui.message(msg)

    def _handle_direct_output(self, text, raw_text=None):
        if not config.conf["VisionAssistant"]["skip_chat_dialog"]:
            return False
            
        if config.conf["VisionAssistant"]["copy_to_clipboard"]:
            api.copyToClip(raw_text if raw_text else text)
            
        cleaned = clean_markdown(text)
        ui.message(cleaned)
        return True

    def script_showHelp(self, gesture):
        if self.toggling: self.finish()
        help_msg = (
            "T: " + _("Translates the selected text or navigator object.") + "\n" + \
            "Shift+T: " + _("Translates the text currently in the clipboard.") + "\n" + \
            "R: " + _("Opens a menu to Explain, Summarize, or Fix the selected text.") + "\n" + \
            "O: " + _("Performs OCR and description on the entire screen.") + "\n" + \
            "V: " + _("Describes the current object (Navigator Object).") + "\n" + \
            "D: " + _("Opens the Document Reader for detailed page-by-page analysis (PDF/Images).") + "\n" + \
            "F: " + _("Recognizes text from a selected image or PDF file.") + "\n" + \
            "A: " + _("Transcribes a selected audio file.") + "\n" + \
            "Shift+V: " + _("Analyzes a YouTube, Instagram, Twitter or TikTok video URL.") + "\n" + \
            "C: " + _("Attempts to solve a CAPTCHA on the screen or navigator object.") + "\n" + \
            "S: " + _("Records voice, transcribes it using AI, and types the result.") + "\n" + \
            "L: " + _("Announces the current status of the add-on.") + "\n" + \
            "U: " + _("Checks for updates manually.") + "\n" + \
            "H: " + _("Shows a list of available commands in the layer.")
)
        # Translators: Title of the help dialog
        ui.browseableMessage(help_msg, _("{name} Help").format(name=ADDON_NAME))

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Announces the current status of the add-on."))
    def script_announceStatus(self, gesture):
        if self.toggling: self.finish()
        # Translators: Status message when the add-on is doing nothing
        idle_msg = _("Idle")
        msg = self.current_status if self.current_status else idle_msg
        ui.message(msg)

    def _browse_file(self, wildcard):
        # Translators: Standard title for opening a file
        return get_file_path(_("Open"), wildcard)

    def _upload_file_to_gemini(self, file_path, mime_type):
        api_key = config.conf["VisionAssistant"]["api_key"].strip()
        keys = GeminiHandler._get_api_keys()
        if not keys: return None
        key_idx = GeminiHandler._working_key_idx % len(keys)
        api_key = keys[key_idx]

        proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
        base_url = proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"
        
        try:
            file_size = os.path.getsize(file_path)
            filename = os.path.basename(file_path)
            
            initial_url = f"{base_url}/upload/v1beta/files"
            headers_init = {
                "X-Goog-Upload-Protocol": "resumable",
                "X-Goog-Upload-Command": "start",
                "X-Goog-Upload-Header-Content-Length": str(file_size),
                "X-Goog-Upload-Header-Content-Type": mime_type,
                "Content-Type": "application/json",
                "x-goog-api-key": api_key
            }
            metadata = {"file": {"display_name": filename}}
            req_init = request.Request(initial_url, data=json.dumps(metadata).encode('utf-8'), headers=headers_init, method="POST")
            
            with get_proxy_opener().open(req_init, timeout=30) as response:
                upload_url = response.headers.get("x-goog-upload-url")
                
            if not upload_url: return None

            with open(file_path, "rb") as f:
                file_data = f.read()
                
            headers_upload = {
                "Content-Length": str(file_size),
                "X-Goog-Upload-Offset": "0",
                "X-Goog-Upload-Command": "upload, finalize"
            }
            req_upload = request.Request(upload_url, data=file_data, headers=headers_upload, method="POST")
            
            file_name_id = None
            with get_proxy_opener().open(req_upload, timeout=300) as response:
                if response.status == 200:
                    res_json = json.loads(response.read().decode('utf-8'))
                    file = res_json.get('file', {})
                    file_name_id = file.get('name')
                    
            if not file_name_id: return None

            check_url = f"{base_url}/v1beta/{file_name_id}"
            for _ in range(30):
                try:
                    req_check = request.Request(check_url, headers={"x-goog-api-key": api_key})
                    with get_proxy_opener().open(req_check, timeout=10) as response:
                        state_data = json.loads(response.read().decode('utf-8'))
                        state = state_data.get('state')
                        if state == "ACTIVE":
                            file_uri = state_data.get('uri')
                            GeminiHandler._register_file_uri(file_uri, api_key)
                            return file_uri
                        elif state == "FAILED":
                            return None
                except: pass
                time.sleep(2)
                
            return None 

        except error.URLError as e:
            # Translators: Message of a dialog which may pop up while trying to upload a file
            msg = _("Upload Connection Error: {reason}").format(reason=e.reason)
            self.report_status(msg)
            show_error_dialog(msg)
            return None
        except error.HTTPError as e:
            # Translators: Message of a dialog which may pop up while trying to upload a file
            msg = _("Upload Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
            self.report_status(msg)
            show_error_dialog(msg)
            return None
        except Exception as e:
            # Translators: Message of a dialog which may pop up while trying to upload a file
            msg = _("File Upload Error: {error}").format(error=e)
            self.report_status(msg)
            show_error_dialog(msg)
            return None



    def _call_gemini_safe(self, prompt_or_contents, attachments=[], json_mode=False):
        def _has_parts(contents):
            for item in contents:
                if not isinstance(item, dict):
                    continue
                parts = item.get("parts", [])
                for part in parts:
                    if isinstance(part, dict) and part:
                        return True
            return False

        if isinstance(prompt_or_contents, list):
            if not _has_parts(prompt_or_contents):
                # Translators: Error message when there's no content to send
                err_msg = _("Nothing to send.")
                self.report_status(_("Error"))
                show_error_dialog(err_msg)
                return None
        else:
            if not prompt_or_contents and not attachments:
                # Translators: Error message when there's no content to send
                err_msg = _("Nothing to send.")
                self.report_status(_("Error"))
                show_error_dialog(err_msg)
                return None

        def _logic(key, p_or_c, atts, j_mode):
            model = config.conf["VisionAssistant"]["model_name"]
            proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
            base_url = proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"
            url = f"{base_url}/v1beta/models/{model}:generateContent"
            headers = {"Content-Type": "application/json; charset=UTF-8", "x-goog-api-key": key}
            
            contents = []
            if isinstance(p_or_c, list):
                contents = p_or_c
            else:
                parts = []
                for att in atts:
                    if 'file_uri' in att:
                        parts.append({"file_data": {"mime_type": att['mime_type'], "file_uri": att['file_uri']}})
                    else:
                        parts.append({"inline_data": {"mime_type": att['mime_type'], "data": att['data']}})
                if p_or_c:
                    parts.append({"text": p_or_c})
                contents = [{"parts": parts}]
                
            data = {
                "contents": contents,
                "generationConfig": {"temperature": 0.0, "topK": 40},
                "safetySettings": [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            }
            if j_mode: data["generationConfig"]["response_mime_type"] = "application/json"

            req = request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
            with get_proxy_opener().open(req, timeout=600) as response:
                if response.status == 200:
                    res = json.loads(response.read().decode('utf-8'))
                    if not res.get('candidates'): return None
                    candidate = res['candidates'][0]
                    if candidate.get('finishReason') == 'SAFETY':
                        # Translators: Error message when AI refuses to answer due to safety guidelines
                        return "ERROR:" + _("Error: Response blocked by AI safety filters.")
                    content = candidate.get('content', {})
                    parts = content.get('parts', [])
                    if parts and 'text' in parts[0]:
                        return parts[0]['text'].strip()
                    return None

        forced_key = None
        if attachments:
            for att in attachments:
                file_uri = att.get("file_uri") if isinstance(att, dict) else None
                registered_key = GeminiHandler._get_registered_key(file_uri)
                if registered_key:
                    forced_key = registered_key
                    break

        if forced_key:
            res = GeminiHandler._call_with_key(_logic, forced_key, prompt_or_contents, attachments, json_mode)
        else:
            res = GeminiHandler._call_with_rotation(_logic, prompt_or_contents, attachments, json_mode)
        
        if isinstance(res, str) and res.startswith("ERROR:"):
            err_msg = res[6:]
            # Translators: Status reported when an error occurs
            self.report_status(_("Error"))
            show_error_dialog(err_msg)
            return None
            
        return res

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Records voice, transcribes it using AI, and types the result."))
    def script_smartDictation(self, gesture):
        if self.toggling: self.finish()
        if not self.is_recording:
            self.is_recording = True
            tones.beep(800, 100)
            try:
                ctypes.windll.winmm.mciSendStringW('open new type waveaudio alias myaudio', None, 0, 0)
                ctypes.windll.winmm.mciSendStringW('record myaudio', None, 0, 0)
                # Translators: Message reported when dictation starts
                msg = _("Listening...")
                self.report_status(msg)
            except Exception as e:
                # Translators: Message in an error dialog which can pop up while trying dictation.
                msg = _("Audio Hardware Error: {error}").format(error=e)
                show_error_dialog(msg)
                self.is_recording = False
        else:
            self.is_recording = False
            tones.beep(500, 100)
            try:
                ctypes.windll.winmm.mciSendStringW(f'save myaudio "{self.temp_audio_file}"', None, 0, 0)
                ctypes.windll.winmm.mciSendStringW('close myaudio', None, 0, 0)
                # Translators: Message reported when processing dictation
                msg = _("Typing...")
                self.report_status(msg)
                threading.Thread(target=self._thread_dictation, daemon=True).start()
            except Exception as e:
                # Translators: Message in an error dialog which can pop up while trying dictation.
                msg = _("Save Recording Error: {error}").format(error=e)
                show_error_dialog(msg)

    def _thread_dictation(self):
        try:
            if not os.path.exists(self.temp_audio_file): return
            
            try:
                with wave.open(self.temp_audio_file, "rb") as wave_file:
                    frame_rate = wave_file.getframerate()
                    n_frames = wave_file.getnframes()
                    duration = n_frames / float(frame_rate)
                
                if duration < 1.0:
                    # Translators: Message reported when the AI detects silence or empty speech
                    msg = _("No speech detected.")
                    wx.CallAfter(self.report_status, msg)
                    try: os.remove(self.temp_audio_file)
                    except: pass
                    return
            except Exception:
                pass

            with open(self.temp_audio_file, "rb") as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            dictation_template = get_prompt_text("dictation_transcribe") or (
                "Transcribe speech. Use native script. Fix stutters. If there is no speech, "
                "silence, or background noise only, write exactly: [[[NOSPEECH]]]"
            )
            p = apply_prompt_template(dictation_template, [("response_lang", config.conf["VisionAssistant"]["ai_response_language"])])
            
            res = self._call_gemini_safe(p, attachments=[{'mime_type': 'audio/wav', 'data': audio_data}])
            
            if res:
                clean_res = res.strip()
                if "[[[NOSPEECH]]]" in clean_res:
                    # Translators: Message reported when the AI detects silence or empty speech
                    msg = _("No speech detected.")
                    wx.CallAfter(self.report_status, msg)
                else:
                    cleaned_text = clean_markdown(res)
                    wx.CallAfter(self._paste_text, cleaned_text)
            else: 
                # Translators: Message reported while trying dictation.
                msg = _("No speech recognized or Error.")
                wx.CallAfter(self.report_status, msg)
            
            try: os.remove(self.temp_audio_file)
            except: pass
        except: pass

    def _paste_text(self, text):
        api.copyToClip(text)
        send_ctrl_v()
        wx.CallLater(300, self._announce_paste, text)

    def _announce_paste(self, text):
        preview = text[:100]
        # Translators: Message reported when dictation is complete
        msg = _("Typed: {text}").format(text=preview)
        self.report_status(msg)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Translates the selected text or navigator object."))
    def script_translateSmart(self, gesture):
        if self.toggling: self.finish()
        text = self._get_text_smart()
        
        if not text:
            # Translators: Message reported when calling translation command
            msg = _("No text found.")
            self.report_status(msg)
            return
            
        # Translators: Message reported when calling translation command
        msg = _("Translating...")
        self.report_status(msg)
        threading.Thread(target=self._thread_translate, args=(text,), daemon=True).start()

    def _thread_translate(self, text):
        s = config.conf["VisionAssistant"]["source_language"]
        t = config.conf["VisionAssistant"]["target_language"]
        swap = config.conf["VisionAssistant"]["smart_swap"]
        fallback = "English" if s == "Auto-detect" else s
        
        current_params = f"{t}|{swap}"
        if text == self._last_source_text and current_params == self._last_params and self.last_translation:
            wx.CallAfter(self._announce_translation, self.last_translation)
            return

        translation_template = get_prompt_text("translate_main")
        p = apply_prompt_template(translation_template, [
            ("target_lang", t),
            ("swap_target", fallback),
            ("smart_swap", str(swap)),
            ("text_content", text),
        ])
        res = self._call_gemini_safe(p)
        if res:
            clean_res = clean_markdown(res)
            self._last_source_text = text
            self._last_params = current_params
            self.last_translation = clean_res
            wx.CallAfter(self._announce_translation, clean_res)

    def _announce_translation(self, text):
        if config.conf["VisionAssistant"]["copy_to_clipboard"] and not config.conf["VisionAssistant"]["skip_chat_dialog"]:
            api.copyToClip(text)
        # Translators: Message reported when calling translation command
        msg = _("Translated: {text}").format(text=text)
        self.report_status(msg)
        if self._handle_direct_output(text):
            return
        wx.CallAfter(self._open_translation_dialog, text)

    def _open_translation_dialog(self, text):
        if self.translation_dlg:
            try: self.translation_dlg.Destroy()
            except: pass
            self.translation_dlg = None

        def noop_callback(ctx, q, history, extra):
            return None, None

        # Translators: Dialog title for Translation results
        self.translation_dlg = VisionQADialog(
            gui.mainFrame, 
            _("{name} - Translation").format(name=ADDON_NAME), 
            text, 
            None, 
            noop_callback, 
            extra_info={'skip_init_history': True},
            raw_content=text,
            status_callback=self.report_status,
            announce_on_open=False,
            allow_questions=False
        )
        self.translation_dlg.Show()
        self.translation_dlg.Raise()

    def _get_text_smart(self):
        focus_obj = api.getFocusObject()
        if not focus_obj: return None

        if hasattr(focus_obj, "treeInterceptor") and focus_obj.treeInterceptor:
            try:
                info = focus_obj.treeInterceptor.makeTextInfo(textInfos.POSITION_SELECTION)
                if info and info.text and not info.text.isspace():
                    return info.text
            except: pass

        try:
            info = focus_obj.makeTextInfo(textInfos.POSITION_SELECTION)
            if info and info.text and not info.text.isspace():
                return info.text
        except: pass

        if isinstance(focus_obj, NVDAObjects.behaviors.EditableText):
            try:
                info = focus_obj.makeTextInfo(textInfos.POSITION_ALL)
                if info and info.text and not info.text.isspace():
                    return info.text
            except: pass
        
        if isinstance(focus_obj, NVDAObjects.behaviors.Terminal):
            try:
                info = focus_obj.makeTextInfo(textInfos.POSITION_ALL)
                return info.text
            except: pass

        try:
            obj = api.getNavigatorObject()
            if not obj: return None
            
            content = []
            if getattr(obj, 'name', None): content.append(obj.name)
            if getattr(obj, 'value', None): content.append(obj.value)
            if getattr(obj, 'description', None): content.append(obj.description)
            
            if hasattr(obj, 'makeTextInfo'):
                try: 
                    ti = obj.makeTextInfo(textInfos.POSITION_ALL)
                    if ti.text and len(ti.text) < 2000: 
                        content.append(ti.text)
                except: pass
                
            final_text = " ".join(list(dict.fromkeys([c for c in content if c and not c.isspace()])))
            return final_text if final_text else None
        except Exception: 
            return None

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Opens a menu to Explain, Summarize, or Fix the selected text."))
    def script_refineText(self, gesture):
        if self.toggling: self.finish()
        if self.refine_menu_dlg:
            self.refine_menu_dlg.Raise()
            self.refine_menu_dlg.SetFocus()
            return
        
        captured_text = self._get_text_smart()
        if not captured_text: captured_text = "" 
        
        wx.CallLater(100, self._open_refine_dialog, captured_text)

    def _open_refine_dialog(self, captured_text):
        options = get_refine_menu_options()
        if not options:
            prompt_map = get_builtin_default_prompt_map()
            for key in REFINE_PROMPT_KEYS:
                if key in prompt_map:
                    item = prompt_map[key]
                    options.append((item["label"], item["prompt"]))
        
        display_choices = [opt[0] for opt in options]
        
        self.refine_menu_dlg = wx.SingleChoiceDialog(
            gui.mainFrame,
            # Translators: Title of the Refine dialog
            _("Choose action:"),
            # Translators: main message of the Refine dialog
            _("Refine"),
            display_choices,
        )
        
        self.refine_menu_dlg.Raise()
        self.refine_menu_dlg.SetFocus()
        
        if self.refine_menu_dlg.ShowModal() == wx.ID_OK:
            selection_index = self.refine_menu_dlg.GetSelection()
            custom_content = options[selection_index][1]

            file_paths = []
            needs_file = False
            wc = "Files|*.*"
            
            if "[file_ocr]" in custom_content:
                needs_file = True
                wc = "Images/PDF/TIFF|*.png;*.jpg;*.webp;*.pdf;*.tif;*.tiff"
            elif "[file_read]" in custom_content:
                needs_file = True
                wc = "Documents|*.txt;*.py;*.md;*.html;*.pdf;*.tif;*.tiff"
            elif "[file_audio]" in custom_content:
                needs_file = True
                wc = "Audio|*.mp3;*.wav;*.ogg"
            
            if needs_file:
                # Translators: Standard title for opening a file
                dlg = wx.FileDialog(gui.mainFrame, _("Open"), wildcard=wc, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
                if dlg.ShowModal() == wx.ID_OK:
                    file_paths = dlg.GetPaths()
                    file_paths.sort()
                    wx.CallLater(200, lambda: threading.Thread(target=self._thread_refine, args=(captured_text, custom_content, file_paths), daemon=True).start())
                dlg.Destroy()
            else:
                # Translators: Message while processing request of the refine text command
                msg = _("Processing...")
                self.report_status(msg)
                threading.Thread(target=self._thread_refine, args=(captured_text, custom_content, None), daemon=True).start()
        
        self.refine_menu_dlg.Destroy()
        self.refine_menu_dlg = None

    def _thread_refine(self, captured_text, custom_content, file_paths=None):
        target_lang = config.conf["VisionAssistant"]["target_language"]
        source_lang = config.conf["VisionAssistant"]["source_language"]
        smart_swap = config.conf["VisionAssistant"]["smart_swap"]
        resp_lang = config.conf["VisionAssistant"]["ai_response_language"]
        
        if file_paths and isinstance(file_paths, str):
            file_paths = [file_paths]
        elif not file_paths:
            file_paths = []

        prompt_text = custom_content
        attachments = []
        fallback = "English" if source_lang == "Auto-detect" else source_lang
        swap_instr = f" If text is in {target_lang}, translate to {fallback}." if smart_swap else ""
        prompt_text = apply_prompt_template(prompt_text, [
            ("target_lang", target_lang),
            ("source_lang", source_lang),
            ("response_lang", resp_lang),
            ("swap_target", fallback),
            ("swap_instruction", swap_instr),
        ])
        
        if "[fix_translate]" in prompt_text:
            prompt_text = prompt_text.replace("[fix_translate]", 
                f"Fix grammar and translate to {target_lang}.{swap_instr} Output ONLY the result.")
        
        prompt_text = prompt_text.replace("[summarize]", f"Summarize the text below in {resp_lang}.")
        prompt_text = prompt_text.replace("[fix_grammar]", "Fix grammar in the text below. Output ONLY the fixed text.")
        prompt_text = prompt_text.replace("[explain]", f"Explain the text below in {resp_lang}.")
        
        used_selection = False
        if "[selection]" in prompt_text: 
            prompt_text = prompt_text.replace("[selection]", captured_text)
            used_selection = True
            
        if "[clipboard]" in prompt_text: 
            prompt_text = prompt_text.replace("[clipboard]", api.getClipData())
        
        if "[screen_obj]" in prompt_text:
            d, w, h = self._capture_navigator()
            if d: attachments.append({'mime_type': 'image/png', 'data': d})
            prompt_text = prompt_text.replace("[screen_obj]", "")
            
        if "[screen_full]" in prompt_text:
            d, w, h = self._capture_fullscreen()
            if d: attachments.append({'mime_type': 'image/png', 'data': d})
            prompt_text = prompt_text.replace("[screen_full]", "")
            
        if file_paths:
            # Translators: Message reported when executing the refine command
            msg = _("Uploading file...")
            wx.CallAfter(self.report_status, msg)
            
            for f_path in file_paths:
                try:
                    mime_type = get_mime_type(f_path)
                    ext = os.path.splitext(f_path)[1].lower()
                    
                    if "[file_ocr]" in prompt_text:
                        if ext in ['.pdf', '.tif', '.tiff'] and fitz:
                            try:
                                doc = fitz.open(f_path)
                                for i in range(len(doc)):
                                    page = doc.load_page(i)
                                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                                    data = base64.b64encode(pix.tobytes("jpg")).decode('utf-8')
                                    attachments.append({'mime_type': 'image/jpeg', 'data': data})
                                doc.close()
                            except: pass
                        else:
                            file_uri = self._upload_file_to_gemini(f_path, mime_type)
                            if file_uri:
                                 attachments.append({'mime_type': mime_type, 'file_uri': file_uri})
                    
                    elif "[file_read]" in prompt_text:
                        file_uri = self._upload_file_to_gemini(f_path, mime_type)
                        if file_uri:
                            attachments.append({'mime_type': mime_type, 'file_uri': file_uri})
                        else:
                             try:
                                with open(f_path, "rb") as f: raw = f.read()
                                txt = raw.decode('utf-8')
                                prompt_text += f"\n\nFile Content ({os.path.basename(f_path)}):\n{txt}\n"
                             except: pass

                    elif "[file_audio]" in prompt_text:
                        file_uri = self._upload_file_to_gemini(f_path, mime_type)
                        if file_uri:
                            attachments.append({'mime_type': mime_type, 'file_uri': file_uri})
                except: pass

            prompt_text = prompt_text.replace("[file_ocr]", "").replace("[file_read]", "").replace("[file_audio]", "")
            
            if not prompt_text.strip() and attachments:
                 prompt_text = get_prompt_text("refine_files_only") or "Analyze these files."
            
        if captured_text and not used_selection and not file_paths:
            prompt_text += f"\n\n---\nInput Text:\n{captured_text}\n---\n"
            
        # Translators: Message reported when executing the refine command
        msg = _("Analyzing...")
        wx.CallAfter(self.report_status, msg)
        res = self._call_gemini_safe(prompt_text, attachments=attachments)
        
        if res:
             self.current_status = _("Idle")
             if not self._handle_direct_output(res):
                 wx.CallAfter(self._open_refine_result_dialog, res, attachments, captured_text, prompt_text)

    def _open_refine_result_dialog(self, result_text, attachments, original_text, initial_prompt):
        if self.refine_dlg:
            try: self.refine_dlg.Destroy()
            except: pass

        def refine_callback(ctx, q, history, extra):
            atts, orig, first_p = ctx
            parts = [{"text": q}]
            current_user_msg = {"role": "user", "parts": parts}
            
            messages = []
            
            if len(history) <= 1: 
                sys_parts = [{"text": first_p}]
                for att in atts:
                    if 'file_uri' in att:
                        sys_parts.append({"file_data": {"mime_type": att['mime_type'], "file_uri": att['file_uri']}})
                    elif 'data' in att:
                        sys_parts.append({"inline_data": {"mime_type": att['mime_type'], "data": att['data']}})
                
                messages.append({"role": "user", "parts": sys_parts})
                if history: messages.append(history[0])
            else:
                messages.extend(history)
            
            messages.append(current_user_msg)
            return self._call_gemini_safe(messages), None

        context = (attachments, original_text, initial_prompt)
        has_file_context = any('file_uri' in a for a in attachments)
        # Translators: Title of Refine Result dialog
        self.refine_dlg = VisionQADialog(
            gui.mainFrame, 
            _("{name} - Refine Result").format(name=ADDON_NAME), 
            result_text, 
            context, 
            refine_callback, 
            extra_info={'file_context': has_file_context, 'skip_init_history': False},
            raw_content=result_text,
            status_callback=self.report_status
        )
        self.refine_dlg.Show()
        self.refine_dlg.Raise()

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Recognizes text from a selected image or PDF file."))
    def script_fileOCR(self, gesture):
        if self.toggling: self.finish()
        wx.CallLater(100, self._open_file_ocr_dialog)

    def _open_file_ocr_dialog(self):
        wc = "Files|*.pdf;*.jpg;*.jpeg;*.png;*.webp;*.tif;*.tiff"
        self._browse_and_run(self._pre_process_ocr, wc, multiple=True)

    def _pre_process_ocr(self, paths):
        try:
            if not fitz:
                # Translators: Error when PyMuPDF is missing
                wx.CallAfter(wx.MessageBox, _("PyMuPDF library is missing."), "Error", wx.ICON_ERROR)
                return
            v_doc = VirtualDocument(paths)
            v_doc.scan()
            if v_doc.total_pages == 0:
                # Translators: Error when no pages found
                wx.CallAfter(wx.MessageBox, _("No readable pages found."), "Error", wx.ICON_ERROR)
                return
            if v_doc.total_pages == 1:
                threading.Thread(target=self._process_file_ocr, args=(v_doc, 0, 0), daemon=True).start()
            else:
                wx.CallAfter(self._show_ocr_range_dialog, v_doc)
        except Exception as e:
            log.error(f"Error preparing OCR: {e}")

    def _show_ocr_range_dialog(self, v_doc):
        range_dlg = RangeDialog(gui.mainFrame, v_doc.total_pages)
        if range_dlg.ShowModal() == wx.ID_OK:
            settings = range_dlg.get_settings()
            threading.Thread(target=self._process_file_ocr, args=(v_doc, settings['start'], settings['end']), daemon=True).start()
        range_dlg.Destroy()

    def _process_file_ocr(self, v_doc, start_page, end_page):
        engine = config.conf["VisionAssistant"]["ocr_engine"]
        target_lang = config.conf["VisionAssistant"]["target_language"]
        
        # Translators: Message reported when calling the OCR file recognition command
        msg = _("Uploading & Extracting...")
        wx.CallAfter(self.report_status, msg)
        
        if engine == 'chrome':
            def chrome_page_worker(page_idx):
                try:
                    file_path, internal_idx = v_doc.get_page_info(page_idx)
                    doc = fitz.open(file_path)
                    page = doc.load_page(internal_idx)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_bytes = pix.tobytes("jpg")
                    doc.close()
                    
                    txt = ChromeOCREngine.recognize(img_bytes)
                    if not txt: return ""
                    
                    if target_lang != "English":
                        txt = GoogleTranslator.translate(txt, target_lang)
                    return f"--- Page {page_idx + 1} ---\n{txt}\n"
                except Exception as e:
                    return f"Error on page {page_idx + 1}: {e}\n"

            with ThreadPoolExecutor(max_workers=5) as executor:
                results_gen = executor.map(chrome_page_worker, range(start_page, end_page + 1))
                full_text = "\n".join(results_gen).strip()

            if not full_text:
                self.current_status = _("Idle")
                # Translators: Error shown when OCR finds no text in the selected files
                wx.CallAfter(show_error_dialog, _("No text detected in the selected file(s)."))
                return
            
            self.current_status = _("Idle")
            if not self._handle_direct_output(full_text):
                wx.CallAfter(self._open_doc_chat_dialog, full_text, [], full_text, full_text)
                
        else: # Gemini Engine
            upload_path = v_doc.create_merged_pdf(start_page, end_page)
            if not upload_path:
                # Translators: Error message if PDF creation fails
                wx.CallAfter(self.report_status, _("Error creating PDF."))
                return

            mime_type = "application/pdf"
            file_uri = self._upload_file_to_gemini(upload_path, mime_type)
            if not file_uri:
                try: os.remove(upload_path)
                except: pass
                self.current_status = _("Idle")
                wx.CallAfter(self.report_status, _("Upload failed."))
                return
            attachments = [{'mime_type': mime_type, 'file_uri': file_uri}]
            
            ocr_translate_template = get_prompt_text("ocr_document_translate")
            p = apply_prompt_template(ocr_translate_template, [("target_lang", target_lang)])
            res = self._call_gemini_safe(p, attachments=attachments)
            
            try: os.remove(upload_path)
            except: pass

            if isinstance(res, str) and not res.strip():
                self.current_status = _("Idle")
                # Translators: Error shown when OCR finds no text in the selected files
                wx.CallAfter(show_error_dialog, _("No text detected in the selected file(s)."))
                return

            if res:
                if not self._handle_direct_output(res):
                    wx.CallAfter(self._open_doc_chat_dialog, res, attachments, res, res)
            else:
                self.current_status = _("Idle")

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Opens the Document Reader for detailed page-by-page analysis (PDF/Images)."))
    def script_analyzeDocument(self, gesture):
        if self.toggling: self.finish()
        wx.CallAfter(self._open_document_reader)

    def _open_doc_chat_dialog(self, init_msg, initial_attachments, doc_text, raw_text_for_save=None):
        if self.doc_dlg:
            try: 
                self.doc_dlg.Destroy()
            except: pass
            self.doc_dlg = None

        def doc_callback(ctx_atts, q, history, dum2):
            lang = config.conf["VisionAssistant"]["ai_response_language"]
            system_template = get_prompt_text("document_chat_system")
            system_instr = apply_prompt_template(system_template, [("response_lang", lang)])
            context_parts = []
            if ctx_atts:
                for att in ctx_atts:
                    if 'file_uri' in att:
                        context_parts.append({"file_data": {"mime_type": att['mime_type'], "file_uri": att['file_uri']}})
                    elif 'data' in att:
                        context_parts.append({"inline_data": {"mime_type": att['mime_type'], "data": att['data']}})
            elif doc_text and not history:
                context_parts.append({"text": f"Document OCR text:\n{doc_text}"})
            context_parts.append({"text": f"Context: {system_instr}"})
            messages = []
            messages.append({"role": "user", "parts": context_parts})
            ack_text = get_prompt_text("document_chat_ack") or "Context received. Ready for questions."
            messages.append({"role": "model", "parts": [{"text": ack_text}]})
            if history: messages.extend(history)
            messages.append({"role": "user", "parts": [{"text": q}]})
            return self._call_gemini_safe(messages), None
            
        # Translators: Dialog title for a Chat dialog
        self.doc_dlg = VisionQADialog(
            gui.mainFrame, 
            _("{name} - Chat").format(name=ADDON_NAME), 
            init_msg, 
            initial_attachments, 
            doc_callback, 
            extra_info={'skip_init_history': True},
            raw_content=raw_text_for_save,
            status_callback=self.report_status
        )
        self.doc_dlg.Show()
        self.doc_dlg.Raise()

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Performs OCR and description on the entire screen."))
    def script_ocrFullScreen(self, gesture):
        if self.toggling: self.finish()
        self._start_vision(True)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Describes the current object (Navigator Object)."))
    def script_describeObject(self, gesture):
        if self.toggling: self.finish()
        self._start_vision(False)

    def _start_vision(self, full):
        if full: d, w, h = self._capture_fullscreen()
        else: d, w, h = self._capture_navigator()
        if d:
            # Translators: Message reported when calling an image analysis command
            msg = _("Scanning...")
            self.report_status(msg)
            wx.CallLater(100, lambda: threading.Thread(target=self._thread_vision, args=(d, w, h, full), daemon=True).start())
        else: 
            # Translators: Message reported when calling an image analysis command
            msg = _("Capture failed.")
            self.report_status(msg)

    def _thread_vision(self, img, w, h, full=False):
        lang = config.conf["VisionAssistant"]["ai_response_language"]
        vision_key = "vision_fullscreen" if full else "vision_navigator_object"
        vision_template = get_prompt_text(vision_key)
        p = apply_prompt_template(vision_template, [
            ("response_lang", lang),
            ("width", w),
            ("height", h),
        ])
        att = [{'mime_type': 'image/png', 'data': img}]
        res = self._call_gemini_safe(p, attachments=att)
        if res:
            self.current_status = _("Idle")
            if not self._handle_direct_output(res):
                wx.CallAfter(self._open_vision_dialog, res, att, None)
        else:
            self.current_status = _("Idle")
        
    def _open_vision_dialog(self, text, atts, size):
        if self.vision_dlg:
            try: self.vision_dlg.Destroy()
            except: pass

        def cb(atts, q, history, sz):
            lang = config.conf["VisionAssistant"]["ai_response_language"]
            followup_suffix_template = get_prompt_text("vision_followup_suffix") or "Answer strictly in {response_lang}"
            followup_suffix = apply_prompt_template(followup_suffix_template, [("response_lang", lang)])
            current_user_msg = {"role": "user", "parts": [{"text": f"{q} ({followup_suffix})"}]}
            messages = []
            initial_history = (not history) or (len(history) == 1 and history[0].get("role") == "model")
            if initial_history:
                parts = []
                for att in atts:
                    parts.append({"inline_data": {"mime_type": att['mime_type'], "data": att['data']}})
                followup_context_template = get_prompt_text("vision_followup_context") or "Image Context. Target Language: {response_lang}"
                followup_context = apply_prompt_template(followup_context_template, [("response_lang", lang)])
                parts.append({"text": followup_context})
                messages.append({"role": "user", "parts": parts})
                if history and history[0].get("role") == "model":
                    messages.append(history[0])
                else:
                    messages.append({"role": "model", "parts": [{"text": text}]})
            else:
                messages.extend(history)
            messages.append(current_user_msg)
            return self._call_gemini_safe(messages), None
            
        # Translators: Dialog title for Image Analysis
        self.vision_dlg = VisionQADialog(
            gui.mainFrame, 
            _("{name} - Image Analysis").format(name=ADDON_NAME), 
            text, 
            atts, 
            cb, 
            None,
            raw_content=text,
            status_callback=self.report_status
        )
        self.vision_dlg.Show()
        self.vision_dlg.Raise()

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Transcribes a selected audio file."))
    def script_transcribeAudio(self, gesture):
        if self.toggling: self.finish()
        wx.CallLater(100, self._open_audio)

    def _open_audio(self):
        wc = "Audio|*.mp3;*.wav;*.ogg"
        self._browse_and_run(self._thread_audio, wc)

    def _thread_audio(self, path):
        try:
            # Translators: Message reported when calling the audio transcription command
            msg = _("Uploading...")
            wx.CallAfter(self.report_status, msg)
            mime_type = get_mime_type(path)
            
            file_uri = self._upload_file_to_gemini(path, mime_type)
            if not file_uri: 
                self.current_status = _("Idle")
                return

            # Translators: Message reported when calling the audio transcription command
            msg = _("Analyzing...")
            wx.CallAfter(self.report_status, msg)
            lang = config.conf["VisionAssistant"]["ai_response_language"]
            audio_template = get_prompt_text("audio_transcription")
            p = apply_prompt_template(audio_template, [("response_lang", lang)])
            
            att = [{'mime_type': mime_type, 'file_uri': file_uri}]
            res = self._call_gemini_safe(p, attachments=att)
            
            if res:
                self.current_status = _("Idle")
                if not self._handle_direct_output(res):
                    wx.CallAfter(self._open_doc_chat_dialog, res, att, res, res)
            else:
                self.current_status = _("Idle")
        except: 
            # Translators: Generic error message when audio processing fails
            msg = _("Error processing audio.")
            wx.CallAfter(self.report_status, msg)
            self.current_status = _("Idle")

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Analyzes a YouTube, Instagram, Twitter or TikTok video URL."))
    def script_analyzeOnlineVideo(self, gesture):
        if self.toggling: self.finish()
        wx.CallLater(100, self._open_video_dialog)

    def _open_video_dialog(self):
        # Translators: Title for the video URL entry dialog
        title = _("YouTube / Instagram / Twitter / TikTok Analysis")
        # Translators: Label for the text entry in video dialog
        msg = _("Enter Video URL (YouTube/Instagram/Twitter/TikTok):")
        dlg = wx.TextEntryDialog(gui.mainFrame, msg, title)
        dlg.Raise()
        if dlg.ShowModal() == wx.ID_OK:
            url = dlg.GetValue()
            if url.strip():
                threading.Thread(target=self._thread_video, args=(url,), daemon=True).start()
        dlg.Destroy()

    def _thread_video(self, url):
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.lower()
            if not domain:
                # Translators: Error message when the URL is invalid
                wx.CallAfter(self.report_status, _("Error: Invalid URL."))
                return
        except:
            wx.CallAfter(self.report_status, _("Error: Invalid URL."))
            return

        is_youtube = any(d in domain for d in ["youtube.com", "youtu.be"])
        is_insta = "instagram.com" in domain
        is_twitter = any(d in domain for d in ["twitter.com", "x.com"])
        is_tiktok = "tiktok.com" in domain

        if not (is_youtube or is_insta or is_twitter or is_tiktok):
            # Translators: Error message when the platform is not supported
            wx.CallAfter(self.report_status, _("Error: Unsupported platform. Only YouTube, Instagram, Twitter, and TikTok are supported."))
            return

        # Translators: Message reported when processing video link
        wx.CallAfter(self.report_status, _("Processing Video..."))
        
        lang = config.conf["VisionAssistant"]["ai_response_language"]
        video_template = get_prompt_text("video_analysis")
        p = apply_prompt_template(video_template, [("response_lang", lang)])

        chat_attachments = []

        if is_insta or is_twitter or is_tiktok:
            if is_insta:
                direct_link = get_instagram_download_link(url)
                err_msg = _("Error: Could not extract Instagram video.")
            elif is_twitter:
                direct_link = get_twitter_download_link(url)
                err_msg = _("Error: Could not extract Twitter video.")
            else:
                direct_link = get_tiktok_download_link(url)
                err_msg = _("Error: Could not extract TikTok video.")

            if not direct_link:
                wx.CallAfter(self.report_status, err_msg)
                return
            
            # Translators: Message reported when downloading video
            wx.CallAfter(self.report_status, _("Downloading Video..."))
            temp_path = _download_temp_video(direct_link)
            
            if not temp_path:
                # Translators: Error message when video download fails
                wx.CallAfter(self.report_status, _("Error: Download failed."))
                return

            # Translators: Message reported when uploading video to AI
            wx.CallAfter(self.report_status, _("Uploading to AI..."))
            try:
                file_uri = self._upload_file_to_gemini(temp_path, "video/mp4")
                if file_uri:
                    chat_attachments = [{'mime_type': 'video/mp4', 'file_uri': file_uri}]
                    # Translators: Message reported when AI is analyzing the video
                    wx.CallAfter(self.report_status, _("Analyzing..."))
                    res = self._call_gemini_safe(p, attachments=chat_attachments)
                    if res:
                        self.current_status = _("Idle")
                        if not self._handle_direct_output(res):
                            wx.CallAfter(self._open_doc_chat_dialog, res, chat_attachments, res, res)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        elif is_youtube:
            # Translators: Message reported when analyzing YouTube video
            wx.CallAfter(self.report_status, _("Analyzing YouTube..."))
            chat_attachments = [{'mime_type': 'video/mp4', 'file_uri': url}]
            res = self._call_gemini_safe(p, attachments=chat_attachments)
            if res:
                self.current_status = _("Idle")
                if not self._handle_direct_output(res):
                    wx.CallAfter(self._open_doc_chat_dialog, res, chat_attachments, res, res)
            else:
                self.current_status = _("Idle")

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Attempts to solve a CAPTCHA on the screen or navigator object."))
    def script_solveCaptcha(self, gesture):
        if self.toggling: self.finish()
        mode = config.conf["VisionAssistant"]["captcha_mode"]
        if mode == 'fullscreen': d, w, h = self._capture_fullscreen()
        else: d, w, h = self._capture_navigator()
        
        is_gov = False
        try:
            if api.getForegroundObject() and "پنجره ملی خدمات دولت هوشمند" in api.getForegroundObject().name: 
                is_gov = True
        except: pass

        if d:
            # Translators: Message reported when calling the CAPTCHA solving command
            msg = _("Solving...")
            self.report_status(msg)
            threading.Thread(target=self._thread_cap, args=(d, is_gov), daemon=True).start()
        else: 
            # Translators: Message reported when calling the CAPTCHA solving command
            msg = _("Capture failed.")
            self.report_status(msg)
        
    def _thread_cap(self, d, is_gov):
        cap_template = get_prompt_text("captcha_solver_base") or (
            "Blind user. Return CAPTCHA code only. If NO CAPTCHA is detected in the image, "
            "strictly return: [[[NO_CAPTCHA]]].{captcha_extra}"
        )
        cap_extra = " Read 5 Persian digits, convert to English." if is_gov else " Convert to English digits."
        p = apply_prompt_template(cap_template, [("captcha_extra", cap_extra)])
        
        r = self._call_gemini_safe(p, attachments=[{'mime_type': 'image/png', 'data': d}])
        if r:
            self.current_status = _("Idle")
            if "[[[NO_CAPTCHA]]]" in r:
                # Translators: Message reported when AI cannot find any CAPTCHA in the image
                wx.CallAfter(self.report_status, _("No CAPTCHA detected."))
            else:
                wx.CallAfter(self._finish_captcha, r)
        else: 
            # Translators: Message reported when calling the CAPTCHA solving command
            msg = _("Failed.")
            wx.CallAfter(self.report_status, msg)
            self.current_status = _("Idle")

    def _finish_captcha(self, text):
        if config.conf["VisionAssistant"]["copy_to_clipboard"]:
            api.copyToClip(text)
        send_ctrl_v()
        # Translators: Message reported when calling the CAPTCHA solving command
        msg = _("Captcha: {text}").format(text=text)
        wx.CallLater(200, self.report_status, msg)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Checks for updates manually."))
    def script_checkUpdate(self, gesture):
        if self.toggling: self.finish()
        # Translators: Message reported when calling the update command
        msg = _("Checking for updates...")
        self.report_status(msg)
        self.updater.check_for_updates(silent=False)

    def _capture_navigator(self):
        try:
            obj = api.getNavigatorObject()
            if not obj or not obj.location: return None,0,0
            x,y,w,h = obj.location
            if w<1 or h<1: return None,0,0
            bmp = wx.Bitmap(w,h)
            wx.MemoryDC(bmp).Blit(0,0,w,h,wx.ScreenDC(),x,y)
            s = io.BytesIO()
            bmp.ConvertToImage().SaveFile(s, wx.BITMAP_TYPE_PNG)
            return base64.b64encode(s.getvalue()).decode('utf-8'),w,h
        except: return None,0,0
    def _capture_fullscreen(self):
        try:
            w,h = wx.GetDisplaySize()
            bmp = wx.Bitmap(w,h)
            wx.MemoryDC(bmp).Blit(0,0,w,h,wx.ScreenDC(),0,0)
            s = io.BytesIO()
            bmp.ConvertToImage().SaveFile(s, wx.BITMAP_TYPE_PNG)
            return base64.b64encode(s.getvalue()).decode('utf-8'),w,h
        except: return None,0,0
    
    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Translates the text currently in the clipboard."))
    def script_translateClipboard(self, gesture):
        if self.toggling: self.finish()
        t = api.getClipData()
        if t: 
            # Translators: Message when calling the command to translate from clipboard
            msg = _("Translating Clipboard...")
            self.report_status(msg)
            threading.Thread(target=self._thread_translate, args=(t,), daemon=True).start()
        else:
            # Translators: Message when calling the command to translate from clipboard
            msg = _("Clipboard empty.")
            self.report_status(msg)

    def on_settings_click(self, event):
        instance = getattr(gui.settingsDialogs.NVDASettingsDialog, "instance", None)
        if instance:
            try:
                instance.Enable(True)
                instance.Raise()
                instance.SetFocus()
                # Translators: Message shown when settings dialog is already open
                ui.message(_("Settings dialog is already open."))
                return
            except:
                gui.settingsDialogs.NVDASettingsDialog.instance = None

        def _open():
            try:
                gui.settingsDialogs.NVDASettingsDialog(gui.mainFrame, SettingsPanel)
            except Exception:
                # Translators: Message shown when settings dialog is already open
                ui.message(_("Settings dialog is already open."))
        
        wx.CallAfter(_open)

    def on_help_click(self, event):
        # Translators: Message when opening documentation
        self.report_status(_("Opening documentation..."))
        addon = addonHandler.getCodeAddon()
        doc_path = addon.getDocFilePath("readme.html")
        if doc_path:
            try:
                os.startfile(doc_path)
            except Exception as e:
                show_error_dialog(str(e))
        else:
            # Translators: Error when help file is missing
            show_error_dialog(_("Documentation file not found."))

    def on_donate_click(self, event):
        try:
            curr_dir = os.path.dirname(__file__)
            if curr_dir not in sys.path:
                sys.path.append(curr_dir)
            import donate_dialog
            wx.CallAfter(donate_dialog.requestDonations, gui.mainFrame)
        except Exception as e:
            show_error_dialog(str(e))

    __gestures = {
        "kb:NVDA+shift+v": "activateLayer",
    }
    
    __VisionGestures = {
        "kb:t": "translateSmart",
        "kb:r": "refineText",
        "kb:o": "ocrFullScreen",
        "kb:v": "describeObject",
        "kb:d": "analyzeDocument",
        "kb:f": "fileOCR",
        "kb:a": "transcribeAudio",
        "kb:c": "solveCaptcha",
        "kb:l": "announceStatus",
        "kb:s": "smartDictation",
        "kb:u": "checkUpdate",
        "kb:shift+t": "translateClipboard",
        "kb:shift+v": "analyzeOnlineVideo",
        "kb:h": "showHelp",
    }
