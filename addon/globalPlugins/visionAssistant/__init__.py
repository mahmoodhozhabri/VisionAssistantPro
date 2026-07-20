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
import shutil
import zipfile
import wave
import gc
import wx
from urllib import request, error
from urllib.parse import quote, urlparse, urlencode
from http import cookiejar
from functools import wraps
import uuid
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor, as_completed
import ssl
import socket
import struct
import subprocess
import array

lib_dir = os.path.join(os.path.dirname(__file__), "lib")
if lib_dir not in sys.path:
    sys.path.append(lib_dir)

arch_lib_dir = os.path.join(lib_dir, "x64" if sys.maxsize > 2**32 else "x86")
if arch_lib_dir not in sys.path:
    sys.path.insert(0, arch_lib_dir)

try:
    import markdown as markdown_lib
except ImportError:
    markdown_lib = None

try:
    import fitz
except ImportError:
    fitz = None

import addonHandler
import languageHandler
import globalPluginHandler
import globalVars
import config
import gui
import ui
import api
import textInfos
import tones
import NVDAObjects.behaviors
import scriptHandler
import mouseHandler
import keyboardHandler
import winUser
import controlTypes
import comtypes.client
import nvwave
import synthDriverHandler

from .prompt_manager_dialog import PromptManagerDialog
from . import donate_dialog

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
    (_("[Free]") + " Gemini 3.5 Flash", "gemini-3.5-flash"),
    (_("[Free]") + " Gemini 3.1 Flash Lite", "gemini-3.1-flash-lite"),
    (_("[Free]") + " Gemini 2.5 Flash", "gemini-2.5-flash"),
    (_("[Free]") + " Gemini 2.5 Flash Lite", "gemini-2.5-flash-lite"),

    # --- 3. High Intelligence (Paid/Pro/Preview) ---
    # Translators: AI Model info. [Pro] = High intelligence/Paid tier. (Preview) = Experimental version.
    (_("[Pro]") + " Gemini 3.1 Pro " + _("(Preview)"), "gemini-3.1-pro-preview"),
    (_("[Pro]") + " Gemini 2.5 Pro", "gemini-2.5-pro"),
]

GEMINI_VOICES = [
    # Translators: Adjective describing a bright AI voice style.
    ("Zephyr", _("Bright")), 
    # Translators: Adjective describing an upbeat AI voice style.
    ("Puck", _("Upbeat")), 
    # Translators: Adjective describing an informative AI voice style.
    ("Charon", _("Informative")), 
    # Translators: Adjective describing a firm AI voice style.
    ("Kore", _("Firm")), 
    # Translators: Adjective describing an excitable AI voice style.
    ("Fenrir", _("Excitable")), 
    # Translators: Adjective describing a youthful AI voice style.
    ("Leda", _("Youthful")), 
    # Translators: Adjective describing a firm AI voice style.
    ("Orus", _("Firm")), 
    # Translators: Adjective describing a breezy AI voice style.
    ("Aoede", _("Breezy")), 
    # Translators: Adjective describing an easy-going AI voice style.
    ("Callirrhoe", _("Easy-going")), 
    # Translators: Adjective describing a bright AI voice style.
    ("Autonoe", _("Bright")), 
    # Translators: Adjective describing a breathy AI voice style.
    ("Enceladus", _("Breathy")), 
    # Translators: Adjective describing a clear AI voice style.
    ("Iapetus", _("Clear")), 
    # Translators: Adjective describing an easy-going AI voice style.
    ("Umbriel", _("Easy-going")), 
    # Translators: Adjective describing a smooth AI voice style.
    ("Algieba", _("Smooth")), 
    # Translators: Adjective describing a smooth AI voice style.
    ("Despina", _("Smooth")), 
    # Translators: Adjective describing a clear AI voice style.
    ("Erinome", _("Clear")), 
    # Translators: Adjective describing a gravelly AI voice style.
    ("Algenib", _("Gravelly")), 
    # Translators: Adjective describing an informative AI voice style.
    ("Rasalgethi", _("Informative")), 
    # Translators: Adjective describing an upbeat AI voice style.
    ("Laomedeia", _("Upbeat")), 
    # Translators: Adjective describing a soft AI voice style.
    ("Achernar", _("Soft")), 
    # Translators: Adjective describing a firm AI voice style.
    ("Alnilam", _("Firm")), 
    # Translators: Adjective describing an even AI voice style.
    ("Schedar", _("Even")), 
    # Translators: Adjective describing a mature AI voice style.
    ("Gacrux", _("Mature")), 
    # Translators: Adjective describing a forward AI voice style.
    ("Pulcherrima", _("Forward")), 
    # Translators: Adjective describing a friendly AI voice style.
    ("Achird", _("Friendly")), 
    # Translators: Adjective describing a casual AI voice style.
    ("Zubenelgenubi", _("Casual")), 
    # Translators: Adjective describing a gentle AI voice style.
    ("Vindemiatrix", _("Gentle")), 
    # Translators: Adjective describing a lively AI voice style.
    ("Sadachbia", _("Lively")), 
    # Translators: Adjective describing a knowledgeable AI voice style.
    ("Sadaltager", _("Knowledgeable")), 
    # Translators: Adjective describing a warm AI voice style.
    ("Sulafat", _("Warm"))
]
OPENAI_VOICES = [
    # Translators: Adjective describing a neutral AI voice style.
    ("Alloy", _("Neutral")),
    # Translators: Adjective describing a quirky AI voice style.
    ("Ash", _("Quirky")),
    # Translators: Adjective describing a professional AI voice style.
    ("Ballad", _("Professional")),
    # Translators: Adjective describing a cheerful AI voice style.
    ("Coral", _("Cheerful")),
    # Translators: Adjective describing a confident AI voice style.
    ("Echo", _("Confident")),
    # Translators: Adjective describing a British AI voice style.
    ("Fable", _("British")),
    # Translators: Adjective describing a pleasant AI voice style.
    ("Nova", _("Pleasant")),
    # Translators: Adjective describing a deep AI voice style.
    ("Onyx", _("Deep")),
    # Translators: Adjective describing a gentle AI voice style.
    ("Sage", _("Gentle")),
    # Translators: Adjective describing a clear AI voice style.
    ("Shimmer", _("Clear")),
    # Translators: Adjective describing an expressive AI voice style.
    ("Verse", _("Expressive")),
    # Translators: Adjective describing a reliable AI voice style.
    ("Marin", _("Reliable")),
    # Translators: Adjective describing an energetic AI voice style.
    ("Cedar", _("Energetic"))
]

LABELS_FILE = os.path.join(globalVars.appArgs.configPath, f"{ADDON_NAME}_labels.json")

OCR_PROGRESS_FILE = os.path.join(globalVars.appArgs.configPath, f"{ADDON_NAME}_ocr_progress.json")


class OCRProgressStore:
    _lock = threading.Lock()

    @staticmethod
    def _read_all():
        if not os.path.exists(OCR_PROGRESS_FILE):
            return {}
        try:
            with open(OCR_PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def _write_all(data):
        try:
            tmp = OCR_PROGRESS_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            os.replace(tmp, OCR_PROGRESS_FILE)
        except Exception as e:
            log.error(f"Failed to write OCR progress: {e}")

    @staticmethod
    def save(key, record):
        with OCRProgressStore._lock:
            data = OCRProgressStore._read_all()
            data[key] = record
            OCRProgressStore._write_all(data)

    @staticmethod
    def load(key):
        with OCRProgressStore._lock:
            return OCRProgressStore._read_all().get(key)

    @staticmethod
    def clear(key):
        with OCRProgressStore._lock:
            data = OCRProgressStore._read_all()
            if key in data:
                del data[key]
                OCRProgressStore._write_all(data)


def _is_failed_ocr_page(text):
    if not text:
        return True
    stripped = text.strip()
    return stripped.startswith("[") or stripped.startswith("ERROR:")


_LANG_CODES = [
    "af", "ar", "bg", "bn", "bs", "ca", "cs", "da", "de", "el", 
    "en", "es", "et", "fa", "fi", "fr", "gu", "he", "hi", "hr", 
    "hu", "id", "is", "it", "ja", "kn", "ko", "lv", "lt", "ml", 
    "mr", "ms", "ne", "nl", "no", "pa", "pl", "pt", "ro", "ru", "sk", 
    "sl", "sr", "sv", "ta", "te", "th", "tr", "uk", "ur", "vi", "zh_CN", "zh_TW"
]

def get_localized_languages():
    lang_list = []
    for code in _LANG_CODES:
        name = languageHandler.getLanguageDescription(code)
        if name:
            lang_list.append((name, code))
    
    lang_list.sort(key=lambda x: x[0])
    return lang_list

BASE_LANGUAGES = get_localized_languages()
# Translators: Option in the language list to automatically detect the source language.
SOURCE_LIST = [(_("Auto-detect"), "auto")] + BASE_LANGUAGES
SOURCE_NAMES = [x[0] for x in SOURCE_LIST]
TARGET_LIST = BASE_LANGUAGES
TARGET_NAMES = [x[0] for x in TARGET_LIST]
TARGET_CODES = {x[0]: x[1] for x in BASE_LANGUAGES}

def get_lang_name(conf_key):
    code = config.conf["VisionAssistant"][conf_key]
    if code == "auto":
        return "Auto-detect"
    return languageHandler.getLanguageDescription(code) or "English"

OCR_ENGINES = [
    # Translators: OCR Engine option (Fast but less formatted)
    (_("Chrome (Fast)"), "chrome"),
    # Translators: OCR Engine option (Slower but better formatting/AI-driven)
    (_("AI (Advanced)"), "gemini"),
    # Translators: OCR Engine option for searchable PDFs (extracts text without OCR)
    (_("None (Extract Text Layer)"), "none")
]

confspec = {
    "active_provider": "string(default='gemini')",
    "api_key": "string(default='')",
    "openai_api_key": "string(default='')",
    "mistral_api_key": "string(default='')",
    "groq_api_key": "string(default='')",
    "minimax_api_key": "string(default='')",
    "minimax_api_host": "string(default='https://api.minimax.io/v1')",
    "minimax_model_name": "string(default='MiniMax-M3')",
    "minimax_vision_model": "string(default='MiniMax-M3')",
    "minimax_ocr_model": "string(default='MiniMax-M3')",
    "minimax_stt_model": "string(default='asr-01')",
    "minimax_tts_model": "string(default='speech-2.8-hd')",
    "minimax_tts_voice": "string(default='English_expressive_narrator')",
    "minimax_voices_cache": "string(default='')",
    "minimax_voices_cache_time": "integer(default=0)",
    "banned_gemini_keys": "string(default='{}')",
    "custom_api_key": "string(default='')",
    "custom_api_url": "string(default='')",
    "custom_api_type": "string(default='openai')",
    "custom_model_name": "string(default='')",
    "custom_upload_support": "boolean(default=False)",
    "use_advanced_endpoints": "boolean(default=False)",
    "custom_models_url": "string(default='')",
    "custom_ocr_url": "string(default='')",
    "custom_ocr_model": "string(default='')",
    "custom_stt_url": "string(default='')",
    "custom_stt_model": "string(default='')",
    "custom_tts_url": "string(default='')",
    "custom_tts_model": "string(default='')",
    "custom_tts_voice": "string(default='')",
    "custom_operator_url": "string(default='')",
    "custom_operator_model": "string(default='')",
    "custom_video_model": "string(default='')",
    "custom_live_model": "string(default='')",
    "advanced_model_routing": "boolean(default=False)",
    "gemini_ocr_model": "string(default='')",
    "gemini_stt_model": "string(default='')",
    "gemini_tts_model": "string(default='')",
    "gemini_operator_model": "string(default='')",
    "gemini_video_model": "string(default='')",
    "gemini_live_model": "string(default='')",
    "openai_ocr_model": "string(default='')",
    "openai_stt_model": "string(default='')",
    "openai_tts_model": "string(default='')",
    "openai_operator_model": "string(default='')",
    "mistral_ocr_model": "string(default='')",
    "mistral_stt_model": "string(default='')",
    "mistral_tts_model": "string(default='')",
    "mistral_operator_model": "string(default='')",
    "groq_ocr_model": "string(default='')",
    "groq_stt_model": "string(default='')",
    "groq_tts_model": "string(default='')",
    "groq_operator_model": "string(default='')",
    "model_name": "string(default='gemini-flash-lite-latest')",
    "openai_model_name": "string(default='')",
    "mistral_model_name": "string(default='')",
    "groq_model_name": "string(default='')",
    "gemini_models_list": "string(default='')",
    "openai_models_list": "string(default='')",
    "mistral_models_list": "string(default='')",
    "groq_models_list": "string(default='')",
    "custom_models_list": "string(default='')",
    "proxy_url": "string(default='')",
    "ai_temperature": "float(default=0.7, min=0.0, max=2.0)",
    "target_language": "string(default='en')",
    "source_language": "string(default='auto')",
    "ai_response_language": "string(default='en')",
    "smart_swap": "boolean(default=True)",
    "captcha_mode": "string(default='navigator')",
    "custom_prompts": "string(default='')",
    "custom_prompts_v2": "string(default='')",
    "default_refine_prompts": "string(default='')",
    "check_update_startup": "boolean(default=False)",
    "clean_markdown_chat": "boolean(default=True)",
    "copy_to_clipboard": "boolean(default=False)",
    "skip_chat_dialog": "boolean(default=False)",
    "live_direct_output": "boolean(default=False)",
    "live_model": "string(default='gemini-3.1-flash-live-preview')",
    "live_thinking_level": "string(default='medium')",
    "ocr_engine": "string(default='chrome')",
    "ocr_batch_size": "integer(default=20, min=0, max=100)",
    "video_srt_chunk_minutes": "integer(default=10, min=0, max=60)",
    "video_chars_as_subtitle": "boolean(default=True)",
    "video_add_disclaimer": "boolean(default=True)",
    "tts_voice": "string(default='Puck')"
}

config.conf.spec["VisionAssistant"] = confspec

REFINE_PROMPT_KEYS = ("summarize", "fix_grammar", "fix_translate", "explain")


DEFAULT_SYSTEM_PROMPTS = (
    {
        "key": "summarize",
        # Translators: Section header for text refinement prompts in Prompt Manager.
        "section": _("Refine"),
        # Translators: Label for the text summarization prompt.
        "label": _("Summarize"),
        "prompt": "Summarize the text below in {response_lang}.",
    },
    {
        "key": "fix_grammar",
        # Translators: Section header for text refinement prompts in Prompt Manager.
        "section": _("Refine"),
        # Translators: Label for the grammar correction prompt.
        "label": _("Fix Grammar"),
        "prompt": "Fix grammar in the text below. Output ONLY the fixed text.",
    },
    {
        "key": "fix_translate",
        # Translators: Section header for text refinement prompts in Prompt Manager.
        "section": _("Refine"),
        # Translators: Label for the grammar correction and translation prompt.
        "label": _("Fix Grammar & Translate"),
        "prompt": "Fix grammar and translate to {target_lang}.{swap_instruction} Output ONLY the result.",
    },
    {
        "key": "explain",
        # Translators: Section header for text refinement prompts in Prompt Manager.
        "section": _("Refine"),
        # Translators: Label for the text explanation prompt.
        "label": _("Explain"),
        "prompt": "Explain the text below in {response_lang}.",
    },
    {
        "key": "translate_main",
        # Translators: Section header for translation-related prompts in Prompt Manager.
        "section": _("Translation"),
        # Translators: Label for the smart translation prompt.
        "label": _("Smart Translation"),
        "guarded": True,
        # Translators: Feature name used in guarded prompt warnings for smart translation.
        "guardedFeatureLabel": _("Smart Translation"),
        "requiredMarkers": ["{target_lang}", "{swap_target}", "{smart_swap}", "{text_content}"],
        "prompt": "Task: Translate the text below based on its DOMINANT language.\n\nConfiguration:\n- Target Language: \"{target_lang}\"\n- Swap Language: \"{swap_target}\"\n- Smart Swap: {smart_swap}\n\nCRITICAL RULES:\n1. DOMINANT LANGUAGE: First, determine the primary/dominant language of the input by focusing on the grammatical structure and the majority of the vocabulary. Ignore embedded technical jargon, user interface labels, software commands, or standalone foreign loanwords when deciding this dominant language.\n2. SMART SWAP: If the dominant language is ALREADY \"{target_lang}\" AND Smart Swap is True, translate the ENTIRE text into \"{swap_target}\".\n3. DEFAULT: In ALL OTHER CASES (or if Smart Swap is False), translate the ENTIRE text into \"{target_lang}\".\n\nConstraints:\n- Output ONLY the final translation.\n- Do NOT translate actual programming code (Python, C++, etc.) or URLs.\n- Do not add any introductory text or explanations.\n\nInput Text:\n{text_content}",
    },
    {
        "key": "translate_quick",
        # Translators: Section header for translation-related prompts in Prompt Manager.
        "section": _("Translation"),
        # Translators: Label for the quick translation prompt.
        "label": _("Quick Translation"),
        "prompt": "Translate to {target_lang}. Output ONLY translation.",
    },
    {
        "key": "document_chat_system",
        # Translators: Section header for document-related prompts in Prompt Manager.
        "section": _("Document"),
        # Translators: Label for the initial context prompt in document chat.
        "label": _("Document Chat Context"),
        "prompt": "STRICTLY Respond in {response_lang}. Use Markdown formatting. Analyze the attached content to answer.",
    },
    {
        "key": "document_chat_ack",
        "section": "Advanced",
        "label": "Document Chat Bootstrap Reply",
        "internal": True,
        "prompt": "Context received. Ready for questions.",
    },
    {
        "key": "vision_navigator_object",
        # Translators: Section header for image analysis prompts in Prompt Manager.
        "section": _("Vision"),
        # Translators: Label for the prompt used to analyze the current navigator object.
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
        # Translators: Section header for image analysis prompts in Prompt Manager.
        "section": _("Vision"),
        # Translators: Label for the prompt used to analyze the entire screen.
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
        "section": "Advanced",
        "label": "Vision Follow-up Context",
        "internal": True,
        "prompt": "Image Context. Target Language: {response_lang}",
    },
    {
        "key": "vision_followup_suffix",
        "section": "Advanced",
        "label": "Vision Follow-up Answer Rule",
        "internal": True,
        "prompt": "Answer strictly in {response_lang}",
    },
    {
        "key": "video_analysis",
        # Translators: Section header for video analysis prompts in Prompt Manager.
        "section": _("Video"),
        # Translators: Label for the general video content analysis prompt.
        "label": _("General Video Analysis"),
        "prompt": (
            "Analyze this video. Provide a detailed description of the visual content and a "
            "summary of the audio. IMPORTANT: Write the entire response STRICTLY in "
            "{response_lang} language."
        ),
    },
    {
        "key": "video_character_extraction",
        "section": "Advanced",
        "label": "Character Extraction (Pre-pass)",
        "internal": True,
        "prompt": (
            "Analyze the entire video and identify all distinct characters/people who appear or speak. "
            "Return a strictly valid JSON object.\n\n"
            "CRITICAL RULES:\n"
            "1. NO GUESSING OR SPECULATING NAMES: Listen with extreme precision to the dialogue. Pay close attention to exactly how characters address each other. Do not replace native, foreign, or local names with common generic names unless that is the exact phonetical name spoken in the audio. If you are not 100% sure of a person's name from the audio track, DO NOT invent or speculate a name. Instead, use a highly detailed physical description as a placeholder name.\n"
            "2. THIRD-PARTY MENTIONS (CRITICAL): People often talk about others who are not present. If a name is spoken in the dialogue, DO NOT automatically assign it to one of the speakers or someone on screen. A name should ONLY be assigned if a character introduces themselves (e.g., 'I am David') or is explicitly addressed by another (e.g., 'How are you, David?').\n"
            "3. DO NOT USE FACIAL RECOGNITION FOR NAMES: Under no circumstances should you guess a character's name based on the actor's real-world face. Only use names heard clearly in the audio.\n"
            "4. CHARACTER RELATIONSHIPS: Listen to verbal context to establish clear relationships (such as family ties or professional roles). Include these verified relationships in their description field.\n"
            "5. FACIAL FEATURES ARE PRIMARY: Clothing can change, so you MUST prioritize describing immutable facial features (e.g., eye shape, nose, jawline, skin tone, facial expressions) and other physical traits (hair color/style, age group, build). Make the face the main identifying factor.\n"
            "6. DO NOT TRANSLATE JSON KEYS. The keys 'characters', 'name', and 'description' MUST remain in English. Only translate the values into {response_lang}.\n"
            "7. Output format MUST be valid JSON matching this template:\n"
            "{\n"
            "  \"characters\": [\n"
            "    {\n"
            "      \"name\": \"Character Name (or descriptive placeholder if name is unverified)\",\n"
            "      \"description\": \"Detailed facial features, physical traits, and verified relationships.\"\n"
            "    }\n"
            "  ]\n"
            "}\n"
        )
    },
    {
        "key": "video_segment_instruction",
        "section": "Advanced",
        "label": "Video Segment Instruction",
        "internal": True,
        "prompt": (
            "CRITICAL TIME-SEGMENT INSTRUCTION:\n"
            "1. You MUST ONLY analyze the video segment starting exactly at {start_str} and ending at {end_str}.\n"
            "2. Your timestamps MUST be ABSOLUTE, continuing from {start_str} up to {end_str}.\n"
            "3. DO NOT stop early. You MUST provide detailed descriptions until you reach {end_str}.\n"
            "4. Do NOT summarize or add fake end credits."
        ),
    },
    {
        "key": "video_previous_context",
        # Translators: Section header for advanced/internal prompts.
        "section": "Advanced",
        # Translators: Label for the prompt that feeds the previous video segment's context to the AI.
        "label": "Video Previous Segment Context",
        "internal": True,
        "prompt": (
            "PREVIOUS SEGMENT DESCRIPTIONS (for context only — do NOT repeat these):\n"
            "{prev_descriptions}\n\n"
            "You MUST continue describing from where the previous segment ended. "
            "Do NOT re-describe events, scenes, or characters already covered above."
        ),
    },
    {
        "key": "video_audio_description",
        # Translators: Section header for video analysis prompts in Prompt Manager.
        "section": _("Video"),
        # Translators: Label for the Audio Description (SRT) generation prompt.
        "label": _("Audio Description Generation (SRT)"),
        "prompt": (
            "You are an expert Audio Describer creating accessible descriptions for a blind audience. "
            "Analyze this video segment and generate an audio description script strictly in JSON format.\n\n"
            "CRITICAL CHARACTER VERIFICATION & TEMPORAL ALIGNMENT RULES:\n"
            "1. STRICT CHARACTER VERIFICATION: You MUST strictly adhere to the GLOBAL CHARACTER DICTIONARY provided above. "
            "DO NOT lazily assume a character's identity based on the previous shot or subsequent events in the segment. "
            "Whenever a character enters the scene, you MUST cross-reference their specific facial features and visual traits against the dictionary before naming them.\n"
            "2. NO PRE-EMPTIVE NAMING (NO FUTURE LEAKING): Do NOT use a character's name in any description before the exact timestamp where they physically enter the screen. "
            "If a character only appears at 00:06:00, their name must never be mentioned at 00:01:00, even if the person visible at 00:01:00 shares a similar clothing color, hair color, or gender. "
            "Prioritize immutable facial structures (eyes, nose, jawline, age) over variable elements like clothing.\n"
            "3. NO GHOST MAPPING: If a character from the dictionary is not actively and clearly visible in this specific segment, "
            "do NOT force or assign their name to a random extra, background person, or different actor. "
            "It is completely normal if some characters from the dictionary do not appear in this segment.\n"
            "4. DEFAULT TO VISUAL DESCRIPTION: If a person appears on screen but you are not 100% sure they are a specific character from the dictionary, "
            "do NOT use any of the dictionary names. Instead, describe them objectively by their visual appearance (e.g., 'a man with short brown hair', 'a young female student with glasses').\n"
            "5. NO DIALOGUE-BASED GUESSING & THIRD-PARTY MENTIONS: Characters frequently talk about people who are off-screen or absent. Do not label a visible person with a name from the dictionary just because you hear that name spoken in the background audio track, "
            "unless you visually verify they match the dictionary's physical description.\n\n"
            "BLIND ACCESSIBILITY & PRECISION RULES:\n"
            "- Focus on describing visual actions, emotions, and settings vividly. Paint a clear mental image for someone who cannot see.\n"
            "- STRICT OCR FOR ON-SCREEN TEXT: If there is ANY text visible on screen (e.g., phone screens, letters, signs, title cards, subtitles, and even long scrolling end credits), you MUST quote it VERBATIM. DO NOT summarize, omit, or truncate the text. Write exactly what is written. For example, instead of saying 'the title of the movie appears', you MUST write 'Text on screen reads: [Exact Text]'. Strict verbatim quoting is mandatory for all text without exception.\n"
            "- TIMELINE PRECISION: You MUST cover the ENTIRE duration of this video segment continuously, all the way to the very last second. Do NOT stop early.\n"
            "- SMART AUDIO TIMING (NATURAL GAPS): Listen to the audio carefully. Whenever possible, set the 'start' and 'end' timestamps of your descriptions during natural gaps where no one is speaking (e.g., silence, non-vocal background music, or ambient noise). Anchor your description to these gaps to avoid overlapping with dialogue.\n"
            "- DO NOT COMPROMISE DESCRIPTION QUALITY: You are strictly forbidden from omitting or truncating important visual details just to fit into a short audio gap. If a description requires more time than the available gap, extend the timestamp even if it overlaps with dialogue, but always try to anchor the start time to a natural pause.\n"
            "- Output 'start' and 'end' values strictly using 'HH:MM:SS' clock format (e.g., '00:02:05'). Sync timestamps perfectly with visual events.\n"
            "- NO DIALOGUE TRANSCRIPTION: Do not transcribe or summarize the spoken conversations. Focus strictly on visual actions.\n"
            "- Language: Write entirely in {response_lang}.\n\n"
            "OUTPUT FORMAT:\n"
            "Your output MUST be a valid JSON object exactly matching this structure:\n"
            "{\n"
            "  \"descriptions\": [\n"
            "    {\n"
            "      \"start\": \"00:01:20\",\n"
            "      \"end\": \"00:01:25\",\n"
            "      \"label\": \"Detailed scene description...\"\n"
            "    }\n"
            "  ]\n"
            "}"
        ),
    },
    {
        "key": "local_video_recording",
        # Translators: Section header for video analysis prompts in Prompt Manager.
        "section": _("Video"),
        # Translators: Label for the local video recording analysis prompt.
        "label": _("Local Video Recording Analysis"),
        "prompt": (
            "Analyze this recorded silent video from the user's screen. Describe the scene, layout, actions, "
            "and any visible text in high detail. If it is a movie, an animation, or a tutorial, describe the events, "
            "characters, and environment thoroughly. Focus on accessibility and paint a clear picture. "
            "IMPORTANT: Write the entire response STRICTLY in {response_lang} language."
        ),
    },
    {
        "key": "audio_transcription",
        # Translators: Section header for audio-related prompts in Prompt Manager.
        "section": _("Audio"),
        # Translators: Label for the audio file transcription prompt.
        "label": _("Audio Transcription"),
        "prompt": "Transcribe this audio in {response_lang}.",
    },
    {
        "key": "dictation_transcribe",
        # Translators: Section header for audio-related prompts in Prompt Manager.
        "section": _("Audio"),
        # Translators: Label for the smart voice dictation prompt.
        "label": _("Smart Dictation"),
        "guarded": True,
        # Translators: Feature name used in guarded prompt warnings for smart dictation.
        "guardedFeatureLabel": _("Smart Dictation"),
        "requiredMarkers": ["[[[NOSPEECH]]]"],
        "prompt": (
            "Transcribe speech. Use native script. Fix stutters. If there is no speech, silence, "
            "or background noise only, write exactly: [[[NOSPEECH]]]"
        ),
    },
    {
        "key": "ocr_image_extract",
        # Translators: Section header for OCR-related prompts in Prompt Manager.
        "section": _("OCR"),
        # Translators: Label for the OCR prompt used for image text extraction.
        "label": _("OCR Image Extraction"),
        "prompt": (
            "Extract all visible text from this image. Strictly preserve original formatting "
            "(headings, lists, tables) using Markdown. Do not output any system messages or "
            "code block backticks (```). Output ONLY the raw content."
        ),
    },
    {
        "key": "ocr_document_extract",
        # Translators: Section header for OCR-related prompts in Prompt Manager.
        "section": _("OCR"),
        # Translators: Label for the OCR prompt used for document text extraction.
        "label": _("OCR Document Extraction"),
        "guarded": True,
        # Translators: Feature name used in guarded prompt warnings for OCR document extraction.
        "guardedFeatureLabel": _("OCR Document Extraction"),
        "requiredMarkers": ["[[[PAGE_SEP]]]"],
        "prompt": (
            "Extract all visible text from this document. Strictly preserve original formatting "
            "(headings, lists, tables) using Markdown. You MUST insert the exact delimiter "
            "'[[[PAGE_SEP]]]' immediately after the content of every single page. Do not output "
            "any system messages or code block backticks (```). Output ONLY the raw content."
        ),
    },
    {
        "key": "ocr_document_translate",
        # Translators: Section header for document-related prompts in Prompt Manager.
        "section": _("Document"),
        # Translators: Label for the combined OCR and translation prompt for documents.
        "label": _("Document OCR + Translate"),
        "prompt": (
            "Extract all text from this document. Preserve formatting (Markdown). Then translate "
            "the content to {target_lang}. Output ONLY the translated content. Do not add "
            "explanations."
        ),
    },
    {
        "key": "captcha_solver_base",
        # Translators: Section header for CAPTCHA-related prompts in Prompt Manager.
        "section": _("CAPTCHA"),
        # Translators: Label for the CAPTCHA solving prompt.
        "label": _("CAPTCHA Solver"),
        "guarded": True,
        # Translators: Feature name used in guarded prompt warnings for CAPTCHA solver.
        "guardedFeatureLabel": _("CAPTCHA Solver"),
        "requiredMarkers": ["[[[NO_CAPTCHA]]]"],
        "prompt": (
            "Blind user. Return CAPTCHA code only. If NO CAPTCHA is detected in the image, "
            "strictly return: [[[NO_CAPTCHA]]].{captcha_extra}"
        ),
    },
    {
        "key": "refine_files_only",
        "section": "Advanced",
        "label": "Refine Files-Only Fallback",
        "internal": True,
        "prompt": "Analyze these files.",
    },
    {
        "key": "ui_explorer_system",
        # Translators: Section header for UI Explorer prompts in the Prompt Manager dialog.
        "section": _("Vision"),
        # Translators: Label for the UI Explorer system instruction prompt in the Prompt Manager.
        "label": _("UI Explorer Instruction"),
        "guarded": True,
        # Translators: Feature name shown in the warning dialog when a user tries to eid the UI Explorer prompt.
        "guardedFeatureLabel": _("UI Explorer"),
        "requiredMarkers": ["{app_name}"],
        "prompt": (
            "You are an expert accessibility assistant. Focus ONLY on the application: {app_name}. "
            "\n\nCRITICAL EXCLUSIONS:\n"
            "1. Ignore the Windows Taskbar, Start Button, Clock, and System Tray icons.\n"
            "2. Ignore any NVDA, Screen Reader, or 'Vision Assistant' dialogs.\n"
            "\nLABELING RULES:\n"
            "- Format: '[Type] Name (State)'.\n"
            "- Standard Types: Button, Checkbox, Radio Button, Tab, List Item, Menu Item, Text Field, Link.\n"
            "- Use 'Icon' ONLY for standalone graphical buttons that do not fit other categories.\n"
            "\nSTATE DETECTION (Be strict):\n"
            "- Use '(Checked)' or '(Unchecked)' ONLY for checkboxes and radio buttons.\n"
            "- Use '(Selected)' ONLY if the item has a clear visual highlight/indicator compared to others.\n"
            "- Use '(Expanded)' or '(Collapsed)' for menus or tree nodes.\n"
            "- If an item is in a list, call it '[List Item]' not '[Icon]'.\n"
            "\nCoordinates: Scale 0-1000. Provide center points.\n"
            "Output ONLY a valid JSON list of objects: "
            "[{\"label\": \"...\", \"x\": int, \"y\": int}, ...]"
        ),
    },
    {
        "key": "ai_operator_system",
        # Translators: Section header for AI Operator prompts in the Prompt Manager dialog.
        "section": _("Vision"),
        # Translators: Label for the AI Operator system instruction prompt in the Prompt Manager.
        "label": _("AI Operator Instruction"),
        "guarded": True,
        # Translators: Feature name shown in the warning dialog when a user tries to edit the AI Operator prompt.
        "guardedFeatureLabel": _("AI Operator"),
        "requiredMarkers": ["{user_command}", "{response_lang}", "{app_name}"],
        "prompt": (
            "You are a Windows operator. Foreground App: {app_name}. Task: {user_command}.\n"
            "STRICT RULES:\n"
            "1. RESPONSE LANGUAGE: Everything MUST be in {response_lang}.\n"
            "2. FINAL STEP: Set \"finished\": true as soon as your action fulfills the request. Set \"finished\": false ONLY when you are opening an intermediate menu to reach the final target in a next step.\n"
            "3. COORDINATES: scale 0-1000. \"x\"/\"y\" are the target point. For \"drag\", \"start_x\"/\"start_y\" is where you press and hold (the element to move) and \"x\"/\"y\" is where you release (the destination).\n"
            "4. ACTION: If an action is needed, output ONLY JSON: {\"x\": int, \"y\": int, \"start_x\": int, \"start_y\": int, \"action\": \"click\"/\"right_click\"/\"double_click\"/\"type\"/\"scroll\"/\"drag\"/\"keypress\", \"text\": \"...\", \"scroll_direction\": \"up\"/\"down\", \"keys\": \"...\", \"finished\": bool, \"explanation\": \"... (in {response_lang})\"}.\n"
            "- Use \"drag\" only to move/relocate an element from one place to another.\n"
            "- For \"keypress\", put key names like 'enter', 'tab', 'escape', 'up', 'down' in \"keys\".\n"
            "Ignore 'AI Operator' or 'NVDA' windows."
        ),
    },
    {
        "key": "label_single_system",
        # Translators: Section header for labeling prompts in Prompt Manager.
        "section": _("Vision"),
        # Translators: Label for the prompt used to identify a single UI icon.
        "label": _("Single Labeling Instruction"),
        "requiredMarkers": ["{app_name}", "{response_lang}"],
        "prompt": (
            "Analyze this UI screenshot for the app: {app_name}.\n"
            "Identify the focused element and provide a short descriptive name.\n"
            "Rules:\n"
            "1. If the element has visible text in the image, return that exact text. DO NOT translate it.\n"
            "2. If it is a purely visual icon, provide a functional name in {response_lang}.\n"
            "3. Output ONLY the raw name without any punctuation. Do NOT include the role (like 'button' or 'icon') in the label."
        ),
    },
    {
        "key": "label_batch_system",
        # Translators: Section header for labeling prompts in Prompt Manager.
        "section": _("Vision"),
        # Translators: Label for the prompt used to identify multiple unnamed elements at once.
        "label": _("Batch Labeling Instruction"),
        "guarded": True,
        # Translators: Feature name used in guarded prompt warnings for Batch Labeling.
        "guardedFeatureLabel": _("Batch Labeling"),
        "requiredMarkers": ["{app_name}", "{response_lang}"],
        "prompt": (
            "Task: Identify UI elements for the app: {app_name}.\n"
            "Output Format: A strictly valid JSON array of objects. No intro/outro text.\n"
            "Rules:\n"
            "1. If an element has visible text in the image, return that exact text. DO NOT translate it.\n"
            "2. If it is a purely visual icon, provide a functional name in {response_lang}.\n"
            "3. Ensure every object in the JSON array is separated by a comma. Verify the syntax before responding.\n"
            "JSON Template: [{\"label\": \"Name\", \"x\": 123, \"y\": 456}, ...]\n"
            "Coordinates scale: 0-1000."
        ),
    },
    {
        "key": "live_assistant_system",
        # Translators: Section header for the Live Assistant prompt in Prompt Manager.
        "section": _("Live"),
        # Translators: Label for the Live Assistant system instruction prompt in the Prompt Manager.
        "label": _("Live Assistant Instruction"),
        "guarded": True,
        # Translators: Feature name shown in the warning dialog when a user tries to edit the Live Assistant prompt.
        "guardedFeatureLabel": _("Live Assistant"),
        "requiredMarkers": ["{response_lang}"],
        "prompt": (
            "You are a helpful voice assistant for a blind user. You can see the user's screen "
            "through the video frames being streamed to you. Use them to understand what the "
            "user is doing and what they are asking about.\n\n"
            "CRITICAL RULES TO AVOID HALLUCINATION:\n"
            "1. NO GUESSING: Only describe what is actually, clearly, and unmistakably visible in the current frames. "
            "Do NOT assume or hallucinate apps, websites, or layout elements (such as claiming you see Facebook or any other page when you do not).\n"
            "2. TEXT PRECISION: Pay extreme attention to reading text, labels, and UI elements with absolute accuracy. "
            "Read only the exact words you can see. If the text is blurred or illegible, state that it is not clear enough to read instead of guessing.\n"
            "3. HONESTY: If you do not see something clearly, or if you do not see the specific element the user asks about, "
            "explicitly state that you cannot see it or that you do not have enough visual information.\n"
            "4. You MUST always speak and respond STRICTLY in {response_lang} language, regardless of the language the user speaks in."
        ),
    },
)

PROMPT_VARIABLES_GUIDE = (
    # Translators: Description and input type for the [selection] variable in the Variables Guide.
    ("[selection]", _("Currently selected text"), _("Text")),
    # Translators: Description for the [clipboard] variable in the Variables Guide.
    ("[clipboard]", _("Clipboard content"), _("Text")),
    # Translators: Description for the [clipboard_image] variable in the Variables Guide.
    ("[clipboard_image]", _("Image currently in clipboard"), _("Image")),
    # Translators: Description and input type for the [screen_obj] variable in the Variables Guide.
    ("[screen_obj]", _("Screenshot of the navigator object"), _("Image")),
    # Translators: Description for the [screen_full] variable in the Variables Guide.
    ("[screen_full]", _("Screenshot of the entire screen"), _("Image")),
    # Translators: Description for the [screen_fg_obj] variable in the Variables Guide.
    ("[screen_fg_obj]", _("Screenshot of the active foreground window"), _("Image")),
    # Translators: Description and input type for the [file_ocr] variable in the Variables Guide.
    ("[file_ocr]", _("Select image/PDF/TIFF for text extraction"), _("Image, PDF, TIFF")),
    # Translators: Description and input type for the [file_read] variable in the Variables Guide.
    ("[file_read]", _("Select document for reading"), _("TXT, Code, PDF")),
    # Translators: Description and input type for the [file_audio] variable in the Variables Guide.
    ("[file_audio]", _("Select audio file for analysis"), _("MP3, WAV, OGG")),
    # Translators: Description for the {target_lang} variable in the Variables Guide.
    ("{target_lang}", _("Current target language"), _("Text")),
    # Translators: Description for the {source_lang} variable in the Variables Guide.
    ("{source_lang}", _("Current source language"), _("Text")),
    # Translators: Description for the {response_lang} variable in the Variables Guide.
    ("{response_lang}", _("Current AI response language"), _("Text")),
    # Translators: Description for the {swap_target} variable in the Variables Guide.
    ("{swap_target}", _("Fallback language for translation"), _("Text")),
    # Translators: Description for the {swap_instruction} variable in the Variables Guide.
    ("{swap_instruction}", _("Smart swap translation instruction"), _("Text")),
)

# --- Helpers ---

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
    for item in DEFAULT_SYSTEM_PROMPTS:
        p = str(item["prompt"]).strip()
        guarded = bool(item.get("guarded"))
        builtins.append({
            "key": item["key"],
            "section": item["section"],
            "label": item["label"],
            "display_label": f"{item['section']} - {item['label']}",
            "internal": bool(item.get("internal")),
            "guarded": guarded,
            "guardedFeatureLabel": str(item.get("guardedFeatureLabel", item["label"])).strip() if guarded else "",
            "requiredMarkers": _normalize_required_markers(item.get("requiredMarkers")),
            "requiredRegex": _normalize_required_regex_checks(item.get("requiredRegex")),
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
            return func(*args, **kwargs)
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


def convert_json_to_srt_string(json_text, chunk_size=1200, segments=None, global_chars=None):
    def parse_seconds(ts):
        ts_str = str(ts).strip()
        total_seconds = 0.0
        if re.match(r'^\d+(?:[.,]\d+)?$', ts_str):
            try:
                total_seconds = float(ts_str.replace(',', '.'))
            except Exception:
                pass
        else:
            ts_clean = ts_str.replace('.', ',')
            main_time = ts_clean.split(',', 1)[0]
            parts = main_time.split(':')
            try:
                if len(parts) == 2:
                    total_seconds = float(int(parts[0]) * 60 + int(parts[1]))
                elif len(parts) == 3:
                    total_seconds = float(int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2]))
            except Exception:
                pass
        return total_seconds

    def format_srt_time(total_seconds):
        if total_seconds < 0:
            total_seconds = 0.0
        h = int(total_seconds // 3600)
        m = int((total_seconds % 3600) // 60)
        s = int(total_seconds % 60)
        ms = int(round((total_seconds - int(total_seconds)) * 1000))
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    def normalize_timestamp(ts, seg_window=None):
        total_seconds = parse_seconds(ts)
        if seg_window is not None:
            seg_start, seg_end = seg_window
            if total_seconds < seg_start:
                if total_seconds < (seg_end - seg_start + 10):
                    total_seconds += seg_start
                else:
                    total_seconds = seg_start
            if total_seconds > seg_end and seg_end > 0:
                total_seconds = seg_end
        return format_srt_time(total_seconds)

    if isinstance(json_text, list):
        chunks = json_text
    else:
        chunks = [json_text]

    srt_content = ""
    counter = 1
    is_first_subtitle = True

    for chunk_idx, raw_chunk in enumerate(chunks):
        seg_window = None
        if segments and chunk_idx < len(segments):
            sw = segments[chunk_idx]
            if sw and sw[1] is not None and sw[1] > sw[0] >= 0:
                seg_window = sw
        clean_text = raw_chunk.strip()
        
        if "```json" in clean_text.lower():
            try:
                clean_text = re.split(r'```json', clean_text, flags=re.IGNORECASE)[1].split("```")[0].strip()
            except Exception: pass
        elif "```srt" in clean_text.lower():
            try:
                clean_text = re.split(r'```srt', clean_text, flags=re.IGNORECASE)[1].split("```")[0].strip()
            except Exception: pass
        elif "```" in clean_text:
            try:
                clean_text = clean_text.split("```")[1].split("```")[0].strip()
            except Exception: pass

        try:
            data = json.loads(clean_text)
            descriptions = []
            if isinstance(data, list):
                descriptions = data
            elif isinstance(data, dict):
                descriptions = data.get("descriptions", data.get("descriptions_list", []))
            
            for desc in descriptions:
                start_val = desc.get("start")
                end_val = desc.get("end")
                text = desc.get("label", desc.get("text", "")).strip()
                
                if not text:
                    continue
                    
                start = normalize_timestamp(start_val, seg_window)
                end = normalize_timestamp(end_val, seg_window)
                
                if start == "00:00:00,000" and end == "00:00:00,000":
                    continue
                
                if is_first_subtitle and global_chars:
                    text = f"{global_chars.strip()}\n{text}"
                    is_first_subtitle = False
                    
                srt_content += f"{counter}\n{start} --> {end}\n{text}\n\n"
                counter += 1
                
        except Exception:
            blocks = re.findall(r'\{[^{}]*?"start"\s*:[^{}]*?\}', clean_text, re.DOTALL|re.IGNORECASE)
            if blocks:
                for block in blocks:
                    start_m = re.search(r'"start"\s*:\s*"([^"]+)"', block, re.IGNORECASE)
                    end_m = re.search(r'"end"\s*:\s*"([^"]+)"', block, re.IGNORECASE)
                    
                    label_m = re.search(r'"(?:label|text)"\s*:\s*"(.*?)"\s*(?:,|})', block, re.IGNORECASE | re.DOTALL)
                    
                    if start_m and end_m and label_m:
                        start_val = start_m.group(1)
                        end_val = end_m.group(1)
                        text = label_m.group(1).strip().replace('\\"', '"')
                        
                        start = normalize_timestamp(start_val, seg_window)
                        end = normalize_timestamp(end_val, seg_window)
                        
                        if start == "00:00:00,000" and end == "00:00:00,000":
                            continue
                        
                        if is_first_subtitle and global_chars:
                            text = f"{global_chars.strip()}\n{text}"
                            is_first_subtitle = False
                            
                        srt_content += f"{counter}\n{start} --> {end}\n{text}\n\n"
                        counter += 1
            else:
                pattern = r'\[(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.*)'
                matches = re.finditer(pattern, clean_text)
                for match in matches:
                    start_time = normalize_timestamp(match.group(1), seg_window)
                    end_time = normalize_timestamp(match.group(2), seg_window)
                    desc_text = match.group(3).strip()
                    
                    if desc_text:
                        if is_first_subtitle and global_chars:
                            desc_text = f"{global_chars.strip()}\n\n{desc_text}"
                            is_first_subtitle = False
                        srt_content += f"{counter}\n{start_time} --> {end_time}\n{desc_text}\n\n"
                        counter += 1

    if srt_content:
        return srt_content
        
    fallback_text = chunks[0].strip()
    if fallback_text.startswith("```json"):
        fallback_text = fallback_text[7:]
    if fallback_text.endswith("```"):
        fallback_text = fallback_text[:-3]
        
    if global_chars:
        fallback_text = f"{global_chars.strip()}\n\n{fallback_text}"
        
    return f"1\n00:00:00,000 --> 00:00:05,000\n{fallback_text.strip()}\n\n"

def strip_thinking_tags(text):
    if not text: return ""
    text = re.sub(r'\s*<think>.*?</think>\s*', '\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\s*<reasoning>.*?</reasoning>\s*', '\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\s*<thought>.*?</thought>\s*', '\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    return text.strip()

def markdown_to_html(text, full_page=False):
    if not text: return ""
    
    html_body = ""
    use_regex_fallback = False
    
    if markdown_lib:
        try:
            html_body = markdown_lib.markdown(text, extensions=['tables', 'fenced_code'])
        except Exception as e:
            log.error(f"Markdown library failed: {e}")
            use_regex_fallback = True
    else:
        use_regex_fallback = True

    if use_regex_fallback:
        html = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html)
        html = re.sub(r'__(.*?)__', r'<b>\1</b>', html)
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
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>body{{font-family:"Segoe UI",Arial,sans-serif;line-height:1.6;padding:20px;color:#333;max-width:800px;margin:0 auto}}h1,h2,h3{{color:#2c3e50;border-bottom:1px solid #eee;padding-bottom:5px}}pre{{background-color:#f4f4f4;padding:10px;border-radius:5px;overflow-x:auto;font-family:Consolas,monospace}}code{{background-color:#f4f4f4;padding:2px 5px;border-radius:3px;font-family:Consolas,monospace}}table{{border-collapse:collapse;width:100%;margin-bottom:10px}}td,th{{border:1px solid #ccc;padding:8px;text-align:left}}strong,b{{color:#000;font-weight:bold}}li{{margin-bottom:5px}}</style></head><body>{html_body}</body></html>"""

def get_mime_type(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf': return 'application/pdf'
    if ext in ['.jpg', '.jpeg']: return 'image/jpeg'
    if ext == '.png': return 'image/png'
    if ext == '.webp': return 'image/webp'
    if ext in ['.tif', '.tiff']: return 'image/jpeg'
    if ext in ['.heic', '.heif']: return 'image/heic'
    if ext == '.mp3': return 'audio/mpeg'
    if ext == '.wav': return 'audio/wav'
    if ext == '.ogg': return 'audio/ogg'
    if ext == '.mp4': return 'video/mp4'
    return 'application/octet-stream'

def show_error_dialog(message):
    # Translators: Title of the error dialog box
    title = _("{name} Error").format(name=ADDON_NAME)
    wx.CallAfter(gui.messageBox, message, title, wx.OK | wx.ICON_ERROR)

def check_screen_curtain_active():
    try:
        if bool(ctypes.windll.nvdaHelperLocal.isScreenFullyBlack()):
            # Translators: Error message shown when trying to take a screenshot while NVDA's Screen Curtain is enabled.
            msg = _("The Screen Curtain is currently enabled. Please disable it (NVDA+Control+Escape) before using visual recognition features.")
            show_error_dialog(msg)
            return True
    except Exception:
        pass
    return False

def send_ctrl_v():
    try:
        winUser.keybd_event(0x11, 0, 0, 0)
        winUser.keybd_event(0x56, 0, 0, 0)
        winUser.keybd_event(0x56, 0, 2, 0)
        winUser.keybd_event(0x11, 0, 2, 0)
    except Exception as e:
        log.debugWarning(f"send_ctrl_v failed: {e}")

def get_proxy_opener(target_url=None):
    proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
    
    is_local = False
    if target_url:
        parsed_target = urlparse(target_url)
        hostname = parsed_target.hostname or ""
        if hostname.lower() in ["localhost", "127.0.0.1"]:
            is_local = True

    is_reverse_proxy = False
    if proxy_url:
        try:
            clean_proxy = proxy_url if "://" in proxy_url else "http://" + proxy_url
            parsed_proxy = urlparse(clean_proxy)
            p_host = parsed_proxy.hostname or ""
            if p_host and "." in p_host and not p_host.replace(".", "").isdigit() and p_host.lower() not in ["localhost", "127.0.0.1"]:
                is_reverse_proxy = True
        except Exception:
            pass

    if is_local or is_reverse_proxy:
        opener = request.build_opener(request.ProxyHandler({}))
    else:
        opener = request.build_opener()
        if proxy_url:
            if not (proxy_url.startswith("http://") or proxy_url.startswith("https://")):
                proxy_url = "http://" + proxy_url
            try:
                parsed = urlparse(proxy_url)
                if parsed.username:
                    proxy_host = parsed.hostname
                    if parsed.port:
                        proxy_host += f":{parsed.port}"
                    clean_proxy_url = f"{parsed.scheme}://{proxy_host}"
                    auth_str = f"{parsed.username}:{parsed.password or ''}"
                    encoded_auth = base64.b64encode(auth_str.encode()).decode()
                    handler = request.ProxyHandler({'http': clean_proxy_url, 'https': clean_proxy_url})
                    opener = request.build_opener(handler)
                    opener.addheaders.append(('Proxy-Authorization', f'Basic {encoded_auth}'))
                else:
                    handler = request.ProxyHandler({'http': proxy_url, 'https': proxy_url})
                    opener = request.build_opener(handler)
            except Exception as e:
                log.error(f"Proxy Setup Failed: {e}")
    opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'))
    return opener

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
    except Exception as e:
        log.error(f"Twitter download extraction failed: {e}")
    return None

def get_instagram_download_link(insta_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://indown.io/en1"
    }
    try:
        cookie_handler = request.HTTPCookieProcessor()
        opener = get_proxy_opener()
        opener.add_handler(cookie_handler)
        
        req_get = request.Request("https://indown.io/en1", headers=headers)
        with opener.open(req_get, timeout=15) as res:
            html_page = res.read().decode('utf-8')

        token_match = re.search(r'name="_token"\s+value="([^"]+)"|value="([^"]+)"\s+name="_token"', html_page)
        if not token_match:
            log.error("Failed to extract CSRF token from indown.io.")
            return None
        csrf_token = token_match.group(1) if token_match.group(1) else token_match.group(2)

        payload = {
            "referer": "https://indown.io/en1",
            "locale": "en",
            "_token": csrf_token,
            "link": insta_url,
            "p": "p"
        }
        data = urlencode(payload).encode('utf-8')
        
        post_headers = headers.copy()
        post_headers["Content-Type"] = "application/x-www-form-urlencoded"
        post_headers["Origin"] = "https://indown.io"
        
        req_post = request.Request("https://indown.io/download", data=data, headers=post_headers, method='POST')
        
        with opener.open(req_post, timeout=20) as res:
            result_html = res.read().decode('utf-8')
            
            links = re.findall(r'href="(https?://[^"\s]+/fetch\?url=[^"\s]+)"', result_html)
            if not links:
                links = re.findall(r'href="(https?://[^\s"]+cdninstagram[^\s"]+\.mp4[^\s"]+)"', result_html)
            if not links:
                links = re.findall(r'href="(https?://[^\s"]+rapidcdn[^\s"]+)"', result_html)
            if not links:
                links = re.findall(r'href="(https?://[^\s"]+\.mp4[^\s"]+)"', result_html)

            if links:
                return links[0].replace('&amp;', '&')
    except Exception as e:
        log.error(f"Instagram download extraction failed: {e}")
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
        with opener.open(req, timeout=120) as response:
            res = json.loads(response.read().decode('utf-8'))
            if res.get('code') == 0:
                play_url = res['data']['play']
                return play_url if play_url.startswith('http') else "https://www.tikwm.com" + play_url
    except Exception as e:
        log.error(f"TikTok download extraction failed: {e}")
    return None

def get_youtube_duration(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        opener = get_proxy_opener()
        req = request.Request(url, headers=headers)
        with opener.open(req, timeout=15) as res:
            html = res.read().decode('utf-8', 'ignore')
            
        m = re.search(r'"lengthSeconds":"(\d+)"', html)
        if not m:
            m = re.search(r'lengthSeconds[^\d]+(\d+)', html)
        if m:
            return float(m.group(1))
            
        m = re.search(r'"approxDurationMs":"(\d+)"', html)
        if not m:
            m = re.search(r'approxDurationMs[^\d]+(\d+)', html)
        if m:
            return float(m.group(1)) / 1000.0
    except Exception as e:
        log.error(f"YouTube duration fetch failed: {e}")
    return None

def _download_temp_video(url, abort_checker=None):
    try:
        req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with request.urlopen(req, timeout=600) as response:
            fd, path = tempfile.mkstemp(suffix=".mp4")
            os.close(fd)
            try:
                with open(path, 'wb') as f:
                    while True:
                        if abort_checker and abort_checker(): break
                        chunk = response.read(8192)
                        if not chunk: break
                        f.write(chunk)
                if abort_checker and abort_checker():
                    try: os.remove(path)
                    except Exception: pass
                    return None
                return path
            except Exception as e:
                log.error(f"Error writing temp video: {e}")
                if os.path.exists(path):
                    try: os.remove(path)
                    except Exception: pass
                return None
    except Exception as e:
        log.error(f"Error downloading temp video: {e}")
    return None


class _LocalVideoSource:

    is_direct = False

    def __init__(self, path):
        self.path = path
        # Translators: Error message shown when processing a local video file fails.
        self.error_message = _("Error processing local video.")
        self.log_label = "Local video thread failed"
        self._compressed_path = None

    def prepare(self, report, abort_check):
        return True

    def ensure_local(self, owner, report, abort_check):
        if self._compressed_path and os.path.exists(self._compressed_path):
            return self._compressed_path
        # Translators: Status message when compressing a local video file before uploading.
        report(_("Compressing video (this may take a moment)..."))
        self._compressed_path = owner._compress_video(self.path)
        if not self._compressed_path:
            # Translators: Error message shown when video compression fails or is cancelled by the user.
            report(_("Error: Video compression failed or was cancelled."))
            return None
        return self._compressed_path

    def duration(self, file_uri):
        return getattr(GeminiHandler, '_file_durations', {}).get(file_uri)

    def cleanup(self):
        cp = self._compressed_path
        if cp and cp != self.path and os.path.exists(cp):
            try: os.remove(cp)
            except Exception: pass


class _DownloadVideoSource:

    is_direct = False

    def __init__(self, url, platform):
        self.url = url
        self.platform = platform
        # Translators: Error message shown when processing an online video fails.
        self.error_message = _("Error processing video.")
        self.log_label = "Online video analysis thread failed"
        self._direct_link = None
        self._temp_path = None

    def prepare(self, report, abort_check):
        # Translators: Message reported when the add-on starts processing an online video link.
        report(_("Processing Video..."))
        return True

    def _extract_link(self, report):
        if self.platform == "instagram":
            link = get_instagram_download_link(self.url)
            # Translators: Error message when the add-on fails to get a direct download link for an Instagram video.
            err = _("Error: Could not extract Instagram video.")
        elif self.platform == "twitter":
            link = get_twitter_download_link(self.url)
            # Translators: Error message when the add-on fails to get a direct download link for a Twitter/X video.
            err = _("Error: Could not extract Twitter video.")
        else:
            link = get_tiktok_download_link(self.url)
            # Translators: Error message when the add-on fails to get a direct download link for a TikTok video.
            err = _("Error: Could not extract TikTok video.")
        if not link:
            log.error(f"Video direct link extraction failed for: {self.url}")
            report(err)
        return link

    def ensure_local(self, owner, report, abort_check):
        if self._temp_path and os.path.exists(self._temp_path):
            return self._temp_path
        if abort_check(): return None
        if not self._direct_link:
            self._direct_link = self._extract_link(report)
            if not self._direct_link:
                return None
        if abort_check(): return None
        # Translators: Message reported when the add-on is downloading the video from the extracted link.
        report(_("Downloading Video..."))
        self._temp_path = _download_temp_video(self._direct_link, abort_checker=abort_check)
        if not self._temp_path:
            log.error(f"Video download failed for link: {self._direct_link}")
            # Translators: Error message when downloading the online video fails.
            report(_("Error: Download failed."))
            return None
        return self._temp_path

    def duration(self, file_uri):
        return getattr(GeminiHandler, '_file_durations', {}).get(file_uri)

    def cleanup(self):
        if self._temp_path and os.path.exists(self._temp_path):
            try: os.remove(self._temp_path)
            except Exception: pass


class _YouTubeVideoSource:

    is_direct = True

    def __init__(self, url):
        self.url = url
        self.error_message = _("Error processing video.")
        self.log_label = "Online video analysis thread failed"

    @property
    def direct_uri(self):
        return self.url

    def prepare(self, report, abort_check):
        # Translators: Message reported when the add-on starts processing an online video link.
        report(_("Processing Video..."))
        return True

    def ensure_local(self, owner, report, abort_check):
        return None

    def duration(self, file_uri):
        return get_youtube_duration(self.url)

    def cleanup(self):
        pass


class _InvalidVideoSource:
    is_direct = False

    def __init__(self, message):
        self.message = message
        self.error_message = message
        self.log_label = "Online video analysis thread failed"

    def prepare(self, report, abort_check):
        report(self.message)
        return False

    def ensure_local(self, owner, report, abort_check):
        return None

    def duration(self, file_uri):
        return None

    def cleanup(self):
        pass


def get_file_path(title, wildcard, mode="open", multiple=False, default_name=""):
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST if mode == "open" else wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
    if multiple: style |= wx.FD_MULTIPLE
    gui.mainFrame.prePopup()
    try:
        with wx.FileDialog(gui.mainFrame, title, wildcard=wildcard, style=style, defaultFile=default_name) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                return dlg.GetPaths() if multiple else dlg.GetPath()
    finally:
        gui.mainFrame.postPopup()
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
                    img_pdf.close()
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
            with opener.open(req, timeout=120) as response:
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
            with opener.open(req, timeout=120) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    text = data.get("text", "").replace("\\n", "\n")
                    return text if text.strip() else None
        except error.HTTPError as e:
            if e.code == 400:
                return None
        except Exception:
            pass
        return None

def _apply_gemma_thinking_patch(payload, url_or_model):
    model_name = ""
    if url_or_model:
        if "/models/" in url_or_model:
            try:
                model_name = url_or_model.split("/models/")[-1].split(":")[0].split("?")[0]
            except Exception:
                pass
        else:
            model_name = url_or_model

    if model_name and ("gemma-4" in model_name.lower() or "gemma4" in model_name.lower()):
        if "generationConfig" not in payload:
            payload["generationConfig"] = {}
        payload["generationConfig"]["thinkingConfig"] = {"thinkingLevel": "MINIMAL"}
    return payload

def _extract_text_from_parts(parts):
    if not parts:
        return ""
    text_parts = [part.get("text", "") for part in parts if not part.get("thought")]
    if text_parts:
        return "".join(text_parts)
    return parts[0].get("text", "")

class GoogleTranslator:
    @staticmethod
    def translate(text, target_lang):
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_lang}&dt=t&q={quote(text)}"
            opener = get_proxy_opener()
            req = request.Request(url)
            with opener.open(req, timeout=15) as r:
                res = json.loads(r.read().decode('utf-8'))
                if res and isinstance(res, list) and res[0]:
                    translated_parts = [sentence[0] for sentence in res[0] if sentence[0]]
                    return "".join(translated_parts).strip()
        except Exception as e:
            log.error(f"GoogleTranslator failed, falling back to original text: {e}")
        return text

class GeminiHandler:
    _working_key_idx = 0 
    _file_uri_keys = {}
    _max_retries = 10

    @staticmethod
    def _get_current_model_for_ban(task=None):
        p = config.conf["VisionAssistant"]["active_provider"]
        if p == "custom":
            return config.conf["VisionAssistant"].get("custom_model_name", "default").strip()
            
        model = config.conf["VisionAssistant"].get("model_name", "gemini-1.5-flash").strip()
        if not model: model = "gemini-1.5-flash"
        
        adv_routing = config.conf["VisionAssistant"].get("advanced_model_routing", False)
        if adv_routing and task:
            adv = ""
            if task == "video":
                adv = config.conf["VisionAssistant"].get("gemini_video_model", "").strip()
            elif task == "ocr":
                adv = config.conf["VisionAssistant"].get("gemini_ocr_model", "").strip()
            elif task == "stt":
                adv = config.conf["VisionAssistant"].get("gemini_stt_model", "").strip()
            elif task == "tts":
                adv = config.conf["VisionAssistant"].get("gemini_tts_model", "").strip()
            elif task == "operator":
                adv = config.conf["VisionAssistant"].get("gemini_operator_model", "").strip()
            elif task == "live":
                adv = config.conf["VisionAssistant"].get("gemini_live_model", "").strip()
                
            if adv and "Default" not in adv and "Auto" not in adv:
                model = adv
                
        return model

    @staticmethod
    def _is_key_banned(key, model=None, task=None):
        banned_str = config.conf["VisionAssistant"].get("banned_gemini_keys", "{}")
        try:
            banned = json.loads(banned_str)
        except Exception:
            banned = {}
            
        if model is None:
            model = GeminiHandler._get_current_model_for_ban(task=task)
        key_model = f"{key}::{model}"
            
        ban_time = banned.get(key_model)
        if not ban_time: return False
        
        if time.time() < ban_time:
            return True
            
        del banned[key_model]
        config.conf["VisionAssistant"]["banned_gemini_keys"] = json.dumps(banned)
        return False

    @staticmethod
    def _ban_key(key, minutes=None, model=None):
        banned_str = config.conf["VisionAssistant"].get("banned_gemini_keys", "{}")
        try:
            banned = json.loads(banned_str)
        except Exception:
            banned = {}
            
        now = time.time()
        if minutes is not None:
            reset_ts = now + (minutes * 60)
        else:
            gm = time.gmtime(now)
            seconds_since_midnight = gm.tm_hour * 3600 + gm.tm_min * 60 + gm.tm_sec
            midnight_utc = now - seconds_since_midnight
            reset_ts = midnight_utc + 8 * 3600
            if now >= reset_ts:
                reset_ts += 24 * 3600
            
        if model is None:
            model = GeminiHandler._get_current_model_for_ban()
        key_model = f"{key}::{model}"
            
        banned[key_model] = reset_ts
        config.conf["VisionAssistant"]["banned_gemini_keys"] = json.dumps(banned)

    @staticmethod
    def _get_api_keys(task=None):
        p = config.conf["VisionAssistant"]["active_provider"]
        raw = config.conf["VisionAssistant"]["api_key"]
        if p == "custom" and config.conf["VisionAssistant"]["custom_api_type"] == "gemini":
            raw = config.conf["VisionAssistant"]["custom_api_key"]
        clean_raw = raw.replace('\r\n', ',').replace('\n', ',')
        keys = [k.strip() for k in clean_raw.split(',') if k.strip()]
        if not keys and p == "custom":
            keys = [""]
            
        available_keys = [k for k in keys if not GeminiHandler._is_key_banned(k, task=task)]
        return available_keys

    @staticmethod
    def _get_opener(url=None):
        return get_proxy_opener(url)

    @staticmethod
    def _handle_error(e):
        server_msg = getattr(e, 'parsed_msg', None)
        retry_delay = getattr(e, 'retry_delay', None)
        is_daily_quota = getattr(e, 'is_daily', False)
        
        if server_msg is not None:
            return server_msg
            
        if hasattr(e, 'read'):
            try:
                if not hasattr(e, '_cached_raw_err'):
                    e._cached_raw_err = e.read().decode('utf-8')
                raw_err = e._cached_raw_err
                
                log.error(f"RAW API ERROR RESPONSE: {raw_err}")
                if raw_err:
                    err_json = json.loads(raw_err)
                    err_val = err_json.get("error")
                    if isinstance(err_val, dict):
                        server_msg = err_val.get("message")
                        
                        details = err_val.get("details", [])
                        for item in details:
                            if not isinstance(item, dict):
                                continue
                            
                            if "RetryInfo" in str(item.get("@type", "")):
                                delay_str = item.get("retryDelay", "")
                                if delay_str and delay_str.endswith("s"):
                                    try:
                                        retry_delay = float(delay_str[:-1])
                                    except Exception:
                                        pass
                            
                            elif "QuotaFailure" in str(item.get("@type", "")):
                                violations = item.get("violations", [])
                                for viol in violations:
                                    if isinstance(viol, dict):
                                        q_id = str(viol.get("quotaId", "")).lower()
                                        if any(x in q_id for x in ["perday", "requestsperday", "daily"]):
                                            is_daily_quota = True
                    else:
                        server_msg = err_val or err_json.get("message")
            except Exception as ex:
                log.error(f"Failed to parse raw error: {ex}")
                
        if server_msg:
            if is_daily_quota and "requestsperday" not in server_msg.lower():
                # Translators: Note appended to the API error message when the daily RequestsPerDay quota limit is reached.
                server_msg += _(" (RequestsPerDay quota exceeded)")
            e.parsed_msg = server_msg
            e.is_daily = is_daily_quota
            if retry_delay is not None:
                e.retry_delay = retry_delay
            return server_msg
            
        if hasattr(e, 'code'):
            # Translators: Error message for Bad Request (400)
            if e.code == 400: return _("Error 400: Bad Request (Check API Key)")
            # Translators: Error message for Forbidden (403)
            if e.code == 403: return _("Error 403: Forbidden (Check Region)")
            if e.code == 429: return "QUOTA_EXCEEDED"
            if e.code >= 500: return "SERVER_ERROR"
            
        return str(e)

    @staticmethod
    def _call_with_retry(func_logic, key, *args, max_retries=None):
        if max_retries is None:
            max_retries = GeminiHandler._max_retries
        last_exc = None
        for attempt in range(max_retries):
            try:
                return func_logic(key, *args)
            except error.HTTPError as e:
                err_msg = GeminiHandler._handle_error(e)
                err_msg_lower = err_msg.lower()
                e.parsed_msg = err_msg
                
                is_retryable = False
                if hasattr(e, 'code') and e.code >= 500:
                    is_retryable = True
                
                if hasattr(e, 'code') and e.code == 429:
                    used_model = None
                    if hasattr(e, 'url') and e.url and "/models/" in e.url:
                        used_model = e.url.split("/models/")[-1].split(":")[0].split("?")[0]
                        
                    if any(x in err_msg_lower for x in ["daily", "per day", "per_day", "perday", "requestsperday"]):
                        GeminiHandler._ban_key(key, model=used_model)
                        is_retryable = False
                    else:
                        is_retryable = True
                elif "high demand" in err_msg_lower or "exhausted" in err_msg_lower or "quota" in err_msg_lower:
                    used_model = None
                    if hasattr(e, 'url') and e.url and "/models/" in e.url:
                        used_model = e.url.split("/models/")[-1].split(":")[0].split("?")[0]
                        
                    if not any(x in err_msg_lower for x in ["daily", "per day", "per_day", "perday", "requestsperday"]):
                        is_retryable = True
                    else:
                        GeminiHandler._ban_key(key, model=used_model)
                        
                delay_sec = getattr(e, 'retry_delay', None)
                if delay_sec is None:
                    match = re.search(r"retry in ([\d\.]+)s", err_msg_lower)
                    if match:
                        try: delay_sec = float(match.group(1))
                        except Exception: pass
                        
                if delay_sec is not None and delay_sec > 0 and is_retryable:
                    n_keys = len(GeminiHandler._get_api_keys())
                    if n_keys > 1:
                        is_retryable = False
                    else:
                        if attempt == 0:
                            time.sleep(delay_sec + 0.5)
                            continue
                        else:
                            is_retryable = False
                
                if not is_retryable:
                    raise e
                    
                last_exc = e
            except error.URLError as e:
                last_exc = e
                
            if attempt < max_retries - 1:
                time.sleep(1.0 * (attempt + 1))
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
    def _call_with_key(func_logic, key, *args, max_retries=None):
        try:
            return GeminiHandler._call_with_retry(func_logic, key, *args, max_retries=max_retries)
        except error.HTTPError as e:
            err_msg = getattr(e, 'parsed_msg', GeminiHandler._handle_error(e))
            if err_msg == "QUOTA_EXCEEDED":
                # Translators: Message of a dialog which may pop up while performing an AI call
                err_msg = _("Error 429: Quota Exceeded (Try later)")
            elif err_msg == "SERVER_ERROR":
                # Translators: Message of a dialog which may pop up while performing an AI call
                err_msg = _("Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
            return "ERROR:" + err_msg
        except Exception as e:
            log.error(f"Gemini call with key failed: {e}", exc_info=True)
            return "ERROR:" + str(e)

    @staticmethod
    def _logic(key, prompt, attachments, json_mode, task="chat"):
        p_active = config.conf["VisionAssistant"]["active_provider"]
        model = ""
        if p_active == "custom":
            model = config.conf["VisionAssistant"]["custom_model_name"].strip()
        
        base_endpoint = AIHandler.get_endpoint(task, model_override=model if model else None)
        connector = "&" if "?" in base_endpoint else "?"
        url = f"{base_endpoint}{connector}key={key}"
        
        temp = config.conf["VisionAssistant"].get("ai_temperature", 0.7)
        if isinstance(prompt, list):
            contents = prompt
        else:
            parts = []
            if attachments:
                for att in attachments:
                    if 'file_uri' in att:
                        fd_part = {
                            "fileData": {
                                "mimeType": att['mime_type'],
                                "fileUri": att['file_uri']
                            }
                        }
                        if att.get('video_metadata'):
                            fd_part['videoMetadata'] = {
                                "startOffset": att['video_metadata'].get('start_offset'),
                                "endOffset": att['video_metadata'].get('end_offset')
                            }
                        parts.append(fd_part)
                    elif 'data' in att:
                        parts.append({"inline_data": {"mime_type": att['mime_type'], "data": att['data']}})
            if prompt: parts.append({"text": prompt})
            contents = [{"parts": parts}]
            
        p_str = str(prompt).lower() if isinstance(prompt, str) else ""
        if any(x in p_str for x in ["extract", "translate", "ocr", "transcribe"]): temp = 0.0

        payload = {
            "contents": contents,
            "generationConfig": {"temperature": temp},
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        }
        if json_mode: payload["generationConfig"]["response_mime_type"] = "application/json"
            
        _apply_gemma_thinking_patch(payload, base_endpoint)
            
        headers = {"Content-Type": "application/json"}

        if task == "video" and ":generateContent" in base_endpoint:
            stream_endpoint = base_endpoint.replace(":generateContent", ":streamGenerateContent")
            s_connector = "&" if "?" in stream_endpoint else "?"
            stream_url = f"{stream_endpoint}{s_connector}alt=sse&key={key}"
            req = request.Request(stream_url, data=json.dumps(payload).encode('utf-8'), headers=headers)

            collected = []
            block_reason = None
            safety_blocked = False
            with GeminiHandler._get_opener(stream_url).open(req, timeout=600) as r:
                for raw_line in r:
                    line = raw_line.decode('utf-8', 'ignore').strip()
                    if not line or not line.startswith("data:"):
                        continue
                    chunk = line[5:].strip()
                    if not chunk or chunk == "[DONE]":
                        continue
                    try:
                        obj = json.loads(chunk)
                    except Exception:
                        continue
                    pf = obj.get('promptFeedback')
                    if pf and pf.get('blockReason'):
                        block_reason = pf['blockReason']
                    for cand in obj.get('candidates', []):
                        if cand.get('finishReason') == "SAFETY":
                            safety_blocked = True
                        collected.append(_extract_text_from_parts(cand.get('content', {}).get('parts', [])))

            text = "".join(collected)
            if text:
                return text
            if block_reason:
                # Translators: Error prefix shown when the AI response is blocked by safety filters.
                return "ERROR:" + _("Blocked by AI Safety Filters: ") + block_reason
            if safety_blocked:
                # Translators: Error shown when the AI response is blocked during generation.
                return "ERROR:" + _("The response was blocked mid-generation by safety filters.")
            # Translators: Generic error message when Gemini returns an empty response.
            return "ERROR:" + _("AI failed to provide a response. This might be due to safety filters or a temporary server issue.")

        req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)

        with GeminiHandler._get_opener(url).open(req, timeout=600) as r:
            res = json.loads(r.read().decode())
            candidates = res.get('candidates')
            if not candidates:
                if 'promptFeedback' in res and 'blockReason' in res['promptFeedback']:
                    # Translators: Error prefix shown when the AI response is blocked by safety filters.
                    return "ERROR:" + _("Blocked by AI Safety Filters: ") + res['promptFeedback']['blockReason']
                # Translators: Generic error message when Gemini returns an empty response.
                return "ERROR:" + _("AI failed to provide a response. This might be due to safety filters or a temporary server issue.")
            
            first_candidate = candidates[0]
            content = first_candidate.get('content', {})
            parts = content.get('parts', [])
            if not parts:
                if first_candidate.get('finishReason') == "SAFETY":
                    # Translators: Error shown when the AI response is blocked during generation.
                    return "ERROR:" + _("The response was blocked mid-generation by safety filters.")
                # Translators: Error shown when the response structure is unexpected or empty.
                return "ERROR:" + _("AI returned an empty response structure.")
            return _extract_text_from_parts(parts)

    @staticmethod
    def _call_with_rotation(func_logic, *args, **kwargs):
        task = kwargs.pop('task', None)
        keys = GeminiHandler._get_api_keys(task=task)
        if not keys: 
            # Translators: Error when no API keys are found in settings
            return "ERROR:" + _("No valid API key available or daily quota exhausted for all keys.")
        
        num_keys = len(keys)
        for i in range(num_keys):
            idx = (GeminiHandler._working_key_idx + i) % num_keys
            key = keys[idx]
            try:
                res = GeminiHandler._call_with_retry(func_logic, key, *args)
                GeminiHandler._working_key_idx = idx 
                return res
            except error.HTTPError as e:
                err_msg = getattr(e, 'parsed_msg', GeminiHandler._handle_error(e))
                err_msg_lower = err_msg.lower()
                
                is_quota_or_server = (
                    err_msg in ["QUOTA_EXCEEDED", "SERVER_ERROR"] or
                    "quota" in err_msg_lower or 
                    "exhausted" in err_msg_lower or
                    (hasattr(e, 'code') and e.code == 429) or
                    (hasattr(e, 'code') and e.code >= 500)
                )

                if is_quota_or_server:
                    log.debugWarning(f"Gemini Key index {idx} failed with {err_msg}. Trying next...")
                    if i < num_keys - 1: continue
                    
                    log.error(f"All Gemini API Keys failed. Last error: {err_msg}")
                    if hasattr(e, 'code') and e.code >= 500:
                        # Translators: Message of a dialog which may pop up while performing an AI call
                        err_msg = _("Server Error {code}: {reason}").format(code=e.code, reason=e.reason)
                        return "ERROR:" + err_msg
                    else:
                        # Translators: Error when all available API keys fail
                        return "ERROR:" + _("All API Keys failed (Quota/Server).")
                        
                log.error(f"Gemini API Error with key {idx}: {err_msg}")
                return "ERROR:" + err_msg
            except Exception as e:
                log.error(f"Unexpected error in Gemini rotation with key {idx}: {e}", exc_info=True)
                return "ERROR:" + str(e)
        # Translators: Generic error message when an operation fails for an unknown reason.
        return "ERROR:" + _("Unknown error occurred.")

    @staticmethod
    def translate(text, target_lang):
        def _logic(key, txt, lang):

            p_active = config.conf["VisionAssistant"]["active_provider"]
            if p_active == "custom":
                base_url = AIHandler.get_base_url("custom")
                model = config.conf["VisionAssistant"]["custom_model_name"].strip()
            else:
                base_url = AIHandler.get_base_url("gemini")
                model = config.conf["VisionAssistant"]["model_name"]
            clean_base = re.sub(r'/(v1|v1beta|v1alpha)$', '', base_url, flags=re.IGNORECASE)
            v_tag = "/v1beta"
            url = f"{clean_base}{v_tag}/models/{model}:generateContent"
            
            quick_template = get_prompt_text("translate_quick") or "Translate to {target_lang}. Output ONLY translation."
            quick_prompt = apply_prompt_template(quick_template, [("target_lang", lang)])
            payload = {"contents": [{"parts": [{"text": quick_prompt}, {"text": txt}]}]}
            
            _apply_gemma_thinking_patch(payload, model)
            
            req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json", "x-goog-api-key": key})
            with GeminiHandler._get_opener(url).open(req, timeout=90) as r:
                res = json.loads(r.read().decode())
                parts = res['candidates'][0]['content'].get('parts', [])
                return _extract_text_from_parts(parts)
        return GeminiHandler._call_with_rotation(_logic, text, target_lang)

    @staticmethod
    def ocr_page(image_bytes):
        def _logic(key, img_data):
            url = AIHandler.get_endpoint("ocr")
            connector = "&" if "?" in url else "?"
            full_url = f"{url}{connector}key={key}"
            
            ocr_image_prompt = get_prompt_text("ocr_image_extract")
            payload = {"contents": [{"parts": [{"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(img_data).decode('utf-8')}}, {"text": ocr_image_prompt}]}]}
            
            _apply_gemma_thinking_patch(payload, url)
            
            req = request.Request(full_url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
            with GeminiHandler._get_opener(full_url).open(req, timeout=120) as r:
                res = json.loads(r.read().decode())
                parts = res['candidates'][0]['content'].get('parts', [])
                return _extract_text_from_parts(parts)
        return GeminiHandler._call_with_rotation(_logic, image_bytes)

    @staticmethod
    def upload_and_process_batch(file_path, mime_type, page_count, prompt=None, page_range_text="", abort_checker=None):
        keys = GeminiHandler._get_api_keys(task="ocr")
        if not keys: 
            # Translators: Error message for missing API Keys
            return [ "ERROR:" + _("No API Keys.") ]
            
        p_active = config.conf["VisionAssistant"]["active_provider"]
        upload_support = True
        if p_active == "custom":
            upload_support = config.conf["VisionAssistant"].get("custom_upload_support", False)
        
        model = AIHandler.get_endpoint("ocr").split('/')[-1].split(':')[0]
        
        if not upload_support:
            try:
                parts = []
                doc = fitz.open(file_path)
                for i in range(len(doc)):
                    page = doc.load_page(i)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_data = base64.b64encode(pix.tobytes("jpg")).decode('utf-8')
                    parts.append({"inline_data": {"mime_type": "image/jpeg", "data": img_data}})
                doc.close()
                if not prompt:
                    prompt = get_prompt_text("ocr_document_extract")
                parts.append({"text": prompt})
                res_text = GeminiHandler._call_with_rotation(GeminiHandler._logic, [{"parts": parts}], None, False, "ocr", task="ocr")
                if res_text.startswith("ERROR:"): return [res_text]
                return res_text.split('[[[PAGE_SEP]]]')
            except Exception as e:
                return ["ERROR:" + str(e)]

        upload_url_base = AIHandler.get_endpoint("upload")
        opener = GeminiHandler._get_opener(upload_url_base)
        
        num_keys = len(keys)
        for i in range(num_keys):
            idx = (GeminiHandler._working_key_idx + i) % num_keys
            key = keys[idx]
            try:
                f_size = os.path.getsize(file_path)
                headers = {"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start", "X-Goog-Upload-Header-Content-Length": str(f_size), "X-Goog-Upload-Header-Content-Type": mime_type, "Content-Type": "application/json", "x-goog-api-key": key}
                
                req = request.Request(upload_url_base, data=json.dumps({"file": {"display_name": "batch"}}).encode(), headers=headers, method="POST")
                with opener.open(req, timeout=120) as r: upload_url = r.headers.get("x-goog-upload-url")
                
                with open(file_path, 'rb') as f: f_data = f.read()
                req_up = request.Request(upload_url, data=f_data, headers={"Content-Length": str(f_size), "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"}, method="POST")
                with opener.open(req_up, timeout=300) as r:
                    res = json.loads(r.read().decode())
                    uri, name = res['file']['uri'], res['file']['name']
                
                base_api_url = AIHandler.get_base_url(p_active).rstrip('/')
                clean_base = re.sub(r'/(v1|v1beta|v1alpha)$', '', base_api_url, flags=re.IGNORECASE)
                v_tag = "/v1beta"
                
                active = False
                for attempt in range(30):
                    check_url = f"{clean_base}{v_tag}/{name}?key={key}"
                    req_check = request.Request(check_url)
                    with opener.open(req_check, timeout=30) as r:
                        state = json.loads(r.read().decode()).get('state')
                        if state == "ACTIVE":
                            active = True
                            break
                        if state == "FAILED": break
                    if abort_checker and abort_checker(): return ["ERROR: Aborted"]
                    time.sleep(2)

                if not active:
                    if i < num_keys - 1:
                        if _vision_assistant_instance:
                            # Translators: Message reported when an upload fails and the system automatically switches to the next available API key.
                            msg = _("Upload failed. Rotating key...")
                            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', msg)
                            wx.CallAfter(ui.message, msg)
                        continue
                    # Translators: Error message for upload failure
                    return [ "ERROR:" + _("Upload failed.") ]

                GeminiHandler._register_file_uri(uri, key)
                if not prompt:
                    prompt = get_prompt_text("ocr_document_extract")
                attachments = [{'mime_type': mime_type, 'file_uri': uri}]
                
                for gen_attempt in range(10):
                    res = GeminiHandler._call_with_key(GeminiHandler._logic, key, prompt, attachments, False, "ocr", max_retries=1)
                    
                    if res and not res.startswith("ERROR:"):
                        GeminiHandler._working_key_idx = idx
                        return res.split('[[[PAGE_SEP]]]')
                        
                    err_msg = res[6:] if res.startswith("ERROR:") else "Unknown Error"
                    err_msg_lower = err_msg.lower()
                    
                    is_fatal_error = any(x in err_msg_lower for x in [
                        "daily", "per day", "per_day", "perday", "requestsperday", "quota_exceeded_daily",
                        "400", "403", "bad request", "forbidden", "blocked"
                    ])
                    
                    if is_fatal_error:
                        if i < num_keys - 1:
                            break
                        return [res]
                        
                    delay_sec = 0
                    match = re.search(r"retry in ([\d\.]+)s", err_msg_lower)
                    if match:
                        try: delay_sec = float(match.group(1))
                        except Exception: pass
                        
                    if delay_sec > 0:
                        if _vision_assistant_instance:
                            # Translators: Message shown when an API rate limit is reached. {sec} is the number of seconds to wait.
                            retry_msg = _("Rate limit reached. Waiting {sec}s before retry...").format(sec=int(delay_sec))
                            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', retry_msg)
                            wx.CallAfter(ui.message, retry_msg)
                        for step in range(int(delay_sec * 2) + 2):
                            if abort_checker and abort_checker(): return ["ERROR: Aborted"]
                            time.sleep(0.5)
                        continue
                        
                    if gen_attempt < 9:
                        if _vision_assistant_instance:
                            if page_range_text:
                                # Translators: Status message indicating an API request retry due to a temporary error for specific pages. {error} is replaced with details, {range} is the page range, {current} and {total} are attempts.
                                retry_msg = _("Temporary error ({error}). Retrying API request for pages {range} (Attempt {current}/{total})...").format(error=err_msg, range=page_range_text, current=gen_attempt + 2, total=10)
                            else:
                                # Translators: Status message indicating an API request retry due to a temporary error. {error} is replaced with details, {current} and {total} are attempts.
                                retry_msg = _("Temporary error ({error}). Retrying on current key (Attempt {current}/{total})...").format(error=err_msg, current=gen_attempt + 2, total=10)
                            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', retry_msg)
                            wx.CallAfter(ui.message, retry_msg)
                        time_limit_sleep = 5.0 * (gen_attempt + 1)
                        for step in range(int(time_limit_sleep * 2)):
                            if abort_checker and abort_checker(): return ["ERROR: Aborted"]
                            time.sleep(0.5)
                else:
                    if i == num_keys - 1:
                        return [res] if res else ["ERROR:" + _("All keys failed.")]
                        
            except Exception as e:
                log.error(f"Error in upload_and_process_batch with key index {idx}: {e}", exc_info=True)
                if i == num_keys - 1:
                    return ["ERROR:" + str(e)]
                    
            if i < num_keys - 1:
                if _vision_assistant_instance:
                    # Translators: Message reported when API quota is exhausted and the system rotates key.
                    msg = _("Daily quota exhausted or retries failed. Rotating key and re-uploading...")
                    wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', msg)
                    wx.CallAfter(ui.message, msg)

        # Translators: Error when all available API keys fail
        return ["ERROR:" + _("All keys failed.")]

    @staticmethod
    def chat(history, new_msg, file_uri, mime_type, file_data=None):
        def _logic(key, hist, msg, uri, mime, f_data):
            url = AIHandler.get_endpoint("chat")
            connector = "&" if "?" in url else "?"
            full_url = f"{url}{connector}key={key}"
            
            contents = list(hist)
            user_parts = []
            if uri: 
                user_parts.append({"file_data": {"mime_type": mime, "file_uri": uri}})
            elif f_data:
                user_parts.append({"inline_data": {"mime_type": mime, "data": f_data}})
            user_parts.append({"text": msg})
            contents.append({"role": "user", "parts": user_parts})
            
            payload = {"contents": contents}
            _apply_gemma_thinking_patch(payload, url)
            
            req = request.Request(full_url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
            with GeminiHandler._get_opener().open(req, timeout=120) as r:
                res = json.loads(r.read().decode())
                parts = res['candidates'][0]['content'].get('parts', [])
                return _extract_text_from_parts(parts)
        forced_key = GeminiHandler._get_registered_key(file_uri) if file_uri else None
        if forced_key:
            return GeminiHandler._call_with_key(_logic, forced_key, history, new_msg, file_uri, mime_type, file_data)
        return GeminiHandler._call_with_rotation(_logic, history, new_msg, file_uri, mime_type, file_data)

    @staticmethod
    def upload_for_chat(file_path, mime_type):
        p_active = config.conf["VisionAssistant"]["active_provider"]
        if p_active == "custom" and not config.conf["VisionAssistant"].get("custom_upload_support", False):
            return None
            
        keys = GeminiHandler._get_api_keys(task="chat")
        if not keys: return "ERROR:" + _("No valid API key available or daily quota exhausted for all keys.")
        opener = GeminiHandler._get_opener()
        upload_url_base = AIHandler.get_endpoint("upload")
        base_api_url = AIHandler.get_base_url(p_active).rstrip('/')
        clean_base = base_api_url.lower().split("/v1beta")[0].split("/v1")[0].rstrip('/')
        v_tag = "/v1beta"

        for key in keys:
            try:
                f_size = os.path.getsize(file_path)
                headers = {"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start", "X-Goog-Upload-Header-Content-Length": str(f_size), "X-Goog-Upload-Header-Content-Type": mime_type, "Content-Type": "application/json", "x-goog-api-key": key}
                req = request.Request(upload_url_base, data=json.dumps({"file": {"display_name": os.path.basename(file_path)}}).encode(), headers=headers, method="POST")
                with opener.open(req, timeout=120) as r: upload_url = r.headers.get("x-goog-upload-url")
                with open(file_path, 'rb') as f: f_data = f.read()
                req_up = request.Request(upload_url, data=f_data, headers={"Content-Length": str(f_size), "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"}, method="POST")
                with opener.open(req_up, timeout=180) as r:
                    res = json.loads(r.read().decode())
                    uri, name = res['file']['uri'], res['file']['name']
                for attempt in range(30):
                    check_url = f"{clean_base}{v_tag}/{name}?key={key}"
                    req_check = request.Request(check_url)
                    with opener.open(req_check, timeout=30) as r:
                        state = json.loads(r.read().decode()).get('state')
                        if state == "ACTIVE":
                            GeminiHandler._register_file_uri(uri, key)
                            return uri
                    time.sleep(2)
                return None 
            except Exception: continue 
        return None

    @staticmethod
    def generate_speech(text, voice_name):
        def _logic(key, txt, voice):
            p_active = config.conf["VisionAssistant"]["active_provider"]
            if p_active == "custom":
                main_model = config.conf["VisionAssistant"]["custom_model_name"].strip()
                adv_tts = config.conf["VisionAssistant"].get("custom_tts_model", "").strip()
            else:
                main_model = config.conf["VisionAssistant"]["model_name"]
                adv_tts = config.conf["VisionAssistant"].get("gemini_tts_model", "").strip()
            if config.conf["VisionAssistant"].get("advanced_model_routing", False) and adv_tts:
                tts_model = adv_tts
            else:
                if p_active == "custom":
                    tts_model = main_model
                else:
                    if "pro" in main_model.lower():
                        tts_model = "gemini-2.5-pro-preview-tts"
                    else:
                        tts_model = "gemini-3.1-flash-tts-preview"

            if p_active == "custom":
                base_url = AIHandler.get_base_url("custom")
            else:
                proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
                base_url = proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"

            clean_base = re.sub(r'/(v1|v1beta|v1alpha)$', '', base_url, flags=re.IGNORECASE)
            v_tag = "/v1beta"
            url = f"{clean_base}{v_tag}/models/{tts_model}:generateContent"
            
            payload = {
                "contents": [{"parts": [{"text": txt}]}],
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}
                }
            }
            req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json", "x-goog-api-key": key})
            with GeminiHandler._get_opener(url).open(req, timeout=600) as r:
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
        return GeminiHandler._call_with_rotation(_logic, text, voice_name, task="tts")

    @staticmethod
    def _upload_video_with_key(file_path, key, abort_checker=None):
        base_upload_url = AIHandler.get_endpoint("upload")
        try:
            file_size = os.path.getsize(file_path)
            headers_init = {"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start", "X-Goog-Upload-Header-Content-Length": str(file_size), "X-Goog-Upload-Header-Content-Type": "video/mp4", "Content-Type": "application/json", "x-goog-api-key": key}
            req_init = request.Request(base_upload_url, data=json.dumps({"file": {"display_name": os.path.basename(file_path)}}).encode(), headers=headers_init, method="POST")
            with get_proxy_opener().open(req_init, timeout=120) as r:
                upload_url = r.headers.get("x-goog-upload-url")

            if not upload_url or (abort_checker and abort_checker()): return None

            with open(file_path, 'rb') as f: data = f.read()
            req_up = request.Request(upload_url, data=data, headers={"Content-Length": str(file_size), "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"}, method="POST")
            with get_proxy_opener().open(req_up, timeout=900) as r:
                res = json.loads(r.read().decode())
                file_name_id = res['file']['name']

            if abort_checker and abort_checker(): return None

            p_base = AIHandler.get_base_url("gemini").rstrip('/')
            clean_base = re.sub(r'/(v1|v1beta|v1alpha)$', '', p_base, flags=re.IGNORECASE)
            check_url = f"{clean_base}/v1beta/{file_name_id}"

            for attempt in range(150):
                if abort_checker and abort_checker(): return None
                req_check = request.Request(check_url, headers={"x-goog-api-key": key})
                try:
                    with get_proxy_opener().open(req_check, timeout=30) as r:
                        data = json.loads(r.read().decode())
                        if data.get('state') == "ACTIVE":
                            uri = data.get('uri')
                            GeminiHandler._register_file_uri(uri, key)
                            duration_sec = None
                            v_meta = data.get('videoMetadata') or data.get('video_metadata') or {}
                            dur_str = v_meta.get('videoDuration') or v_meta.get('video_duration') or v_meta.get('duration') or ''
                            if dur_str:
                                try:
                                    duration_sec = float(dur_str.rstrip('s'))
                                except Exception:
                                    pass
                            if duration_sec:
                                if not hasattr(GeminiHandler, '_file_durations'):
                                    GeminiHandler._file_durations = {}
                                GeminiHandler._file_durations[uri] = duration_sec
                            return uri
                except Exception:
                    pass
                for step in range(4):
                    if abort_checker and abort_checker(): return None
                    time.sleep(0.5)
            return None
        except error.HTTPError as e:
            err_msg = GeminiHandler._handle_error(e)
            log.error(f"Gemini video upload HTTPError: {err_msg}")
            if hasattr(e, 'code') and e.code == 429:
                GeminiHandler._ban_key(key, getattr(e, 'is_daily', False), task="video")
            return None
        except Exception as e:
            log.error(f"Gemini video upload error: {e}")
            return None

    @staticmethod
    def upload_and_get_duration(file_path, report_callback=None, abort_checker=None):
        keys = GeminiHandler._get_api_keys(task="video")
        num_keys = len(keys)
        for i in range(num_keys):
            if abort_checker and abort_checker(): return None, None, None
            idx = (GeminiHandler._working_key_idx + i) % num_keys
            key = keys[idx]
            if report_callback:
                file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                # Translators: Status message indicating video upload progress with file size in MB.
                report_callback(_("Uploading to AI ({size:.1f} MB)...").format(size=file_size_mb))
            
            uri = GeminiHandler._upload_video_with_key(file_path, key, abort_checker)
            if uri:
                dur = GeminiHandler._file_durations.get(uri)
                GeminiHandler._working_key_idx = idx
                return uri, dur, key
        return None, None, None

    @staticmethod
    def process_video_task(file_path, prompt, start_offset_sec=None, end_offset_sec=None, json_mode=False, report_callback=None, abort_checker=None, current_uri=None, current_key=None, is_direct=False, validator=None):
        keys = GeminiHandler._get_api_keys(task="video")
        num_keys = len(keys)
        
        if current_key in keys:
            GeminiHandler._working_key_idx = keys.index(current_key)

        keys_exhausted = 0
        
        while keys_exhausted < num_keys:
            if abort_checker and abort_checker(): return None, None, None
            
            idx = GeminiHandler._working_key_idx % num_keys
            key = keys[idx]
            
            if not is_direct and key != current_key:
                current_uri = None
                
            try:
                if not current_uri and file_path and not is_direct:
                    if report_callback:
                        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                        # Translators: Status message indicating video upload progress with file size in MB and retry attempt numbers.
                        report_callback(_("Uploading to AI ({size:.1f} MB) (Key {current}/{total})...").format(size=file_size_mb, current=idx+1, total=num_keys))
                    
                    current_uri = GeminiHandler._upload_video_with_key(file_path, key, abort_checker)
                    if not current_uri:
                        if report_callback:
                            # Translators: Message reported when a file upload fails and the system is retrying.
                            report_callback(_("Upload failed. Retrying..."))
                        time.sleep(2.0)
                        keys_exhausted += 1
                        GeminiHandler._working_key_idx = (GeminiHandler._working_key_idx + 1) % num_keys
                        continue 
                    current_key = key
                elif is_direct and not current_uri:
                    current_uri = file_path
                    current_key = key
                
                if not current_uri:
                    keys_exhausted += 1
                    GeminiHandler._working_key_idx = (GeminiHandler._working_key_idx + 1) % num_keys
                    continue

                attachments = [{'mime_type': 'video/mp4', 'file_uri': current_uri}]
                if start_offset_sec is not None and end_offset_sec is not None and end_offset_sec != -1:
                    attachments[0]['video_metadata'] = {
                        "start_offset": f"{int(start_offset_sec)}s",
                        "end_offset": f"{int(end_offset_sec)}s"
                    }
                
                res = None
                for attempt in range(10):
                    if abort_checker and abort_checker(): return None, None, None
                    
                    res = GeminiHandler._call_with_key(GeminiHandler._logic, key, prompt, attachments, json_mode, "video", max_retries=1)
                    
                    if res and not res.startswith("ERROR:"):
                        if validator and not validator(res):
                            # Translators: Error shown internally when AI stops early
                            res = "ERROR:" + _("Incomplete description. AI stopped early.")
                        else:
                            return res, current_uri, current_key
                    
                    err_msg = res[6:] if res and res.startswith("ERROR:") else "Unknown Error"
                    err_msg_lower = err_msg.lower()
                    
                    is_fatal_error = any(x in err_msg_lower for x in [
                        "daily", "per day", "per_day", "perday", "requestsperday", "quota_exceeded_daily",
                        "400", "403", "bad request", "forbidden", "blocked"
                    ])
                    
                    if is_fatal_error:
                        break
                        
                    delay_sec = 0
                    match = re.search(r"retry in ([\d\.]+)s", err_msg_lower)
                    if match:
                        try: delay_sec = float(match.group(1))
                        except Exception: pass
                        
                    if delay_sec > 0:
                        if report_callback:
                            report_callback(_("Rate limit reached. Waiting {sec}s before retry...").format(sec=int(delay_sec)))
                        for step in range(int(delay_sec * 2) + 2):
                            if abort_checker and abort_checker(): return None, None, None
                            time.sleep(0.5)
                        continue
                            
                    if report_callback:
                        # Translators: Status message indicating an API request retry due to a temporary error. {error} is replaced with details, {current} and {total} are attempts.
                        report_callback(_("Temporary error ({error}). Retrying on current key (Attempt {current}/{total})...").format(error=err_msg, current=attempt+1, total=10))
                    
                    time_limit_sleep = 5.0 * (attempt + 1)
                    for step in range(int(time_limit_sleep * 2)):
                        if abort_checker and abort_checker(): return None, None, None
                        time.sleep(0.5)
                        
                if res and not res.startswith("ERROR:"):
                    return res, current_uri, current_key
                    
                keys_exhausted += 1
                if keys_exhausted < num_keys:
                    GeminiHandler._working_key_idx = (GeminiHandler._working_key_idx + 1) % num_keys
                    if report_callback:
                        # Translators: Message reported when API quota is exhausted and the system rotates key.
                        report_callback(_("Daily quota exhausted or retries failed. Rotating key and re-uploading..."))
                else:
                    if report_callback:
                        # Translators: Message reported when all available API keys have reached their usage limits.
                        report_callback(_("All API keys exhausted or server unavailable."))
                    break
                    
            except Exception as e:
                log.error(f"Error under key {idx}: {e}")
                keys_exhausted += 1
                GeminiHandler._working_key_idx = (GeminiHandler._working_key_idx + 1) % num_keys
                continue
                
        # Translators: Error message shown when all API keys run out of quota or fail.
        return "ERROR:" + _("All API keys failed or daily quota exhausted."), None, None

class AIHandler:
    @staticmethod
    def is_tts_supported(provider=None):
        p = provider if provider else config.conf["VisionAssistant"]["active_provider"]
        
        if p in ["gemini", "openai", "minimax"]:
            return True

        if p == "custom":
            return True

        return False

    @staticmethod
    def get_voices(provider):
        if provider == "minimax":
            try:
                cache = config.conf["VisionAssistant"].get("minimax_voices_cache", "")
                cache_time_raw = config.conf["VisionAssistant"].get("minimax_voices_cache_time", 0)
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
                req = request.Request(url, data=payload, headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                })
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
                        config.conf["VisionAssistant"]["minimax_voices_cache"] = ",".join(storage_parts)
                        config.conf["VisionAssistant"]["minimax_voices_cache_time"] = int(time.time())
                        log.debug(f"Fetched and cached {len(voices)} MiniMax voices")
                        return voices
                    return []
            except Exception as e:
                log.warning(f"Failed to fetch MiniMax voices: {e}")
                return []
        if provider == "gemini":
            return GEMINI_VOICES
        if provider == "openai":
            return OPENAI_VOICES
        if provider == "custom":
            return OPENAI_VOICES
        return []

    @staticmethod
    def filter_models(provider, models_info, task="main"):
        if task != "main":
            return models_info
        filtered = []
        for mid_orig, mname_orig in models_info:
            mid = mid_orig.lower()
            mname = mname_orig.lower()
            if provider == "gemini":
                excluded = ["nano", "banana", "robotic", "vo3", "v03", "veo", "tts", "native", "audio", "image", "aqa", "lyria", "embedding", "bison", "gecko", "deep", "antigravity", "computer"]
                if any(x in mid or x in mname for x in excluded):
                    continue
            elif provider == "groq":
                excluded = ["whisper", "audio", "vision-preview", "embedding"]
                if any(x in mid or x in mname for x in excluded):
                    continue
            elif provider == "openai":
                excluded = ["whisper", "tts", "dall-e", "embedding", "moderation", "audio", "realtime", "babbage"]
                if any(x in mid or x in mname for x in excluded):
                    continue
            elif provider == "mistral":
                excluded = ["embed", "moderation"]
                if any(x in mid or x in mname for x in excluded):
                    continue
            filtered.append((mid_orig, mname_orig))
        return filtered

    @staticmethod
    def is_gemini():
        p = config.conf["VisionAssistant"]["active_provider"]
        if p == "gemini": return True
        if p == "custom":
            return config.conf["VisionAssistant"]["custom_api_type"] == "gemini"
        return False

    @staticmethod
    def get_base_url(provider):
        if provider == "custom":
            return config.conf["VisionAssistant"].get("custom_api_url", "").strip().rstrip('/')
        
        proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
        
        if proxy_url:
            if not (proxy_url.startswith("http://") or proxy_url.startswith("https://")):
                proxy_url = "http://" + proxy_url
            
            try:
                parsed = urlparse(proxy_url)
                if parsed.hostname in ["127.0.0.1", "localhost"] or parsed.username:
                    proxy_url = ""
                else:
                    netloc = parsed.hostname
                    if parsed.port: netloc += f":{parsed.port}"
                    proxy_url = f"{parsed.scheme}://{netloc}"
            except Exception:
                pass

        if provider == "gemini":
            return proxy_url.rstrip('/') if proxy_url else "https://generativelanguage.googleapis.com"
        elif provider == "openai":
            return proxy_url.rstrip('/') if proxy_url else "https://api.openai.com"
        elif provider == "mistral":
            return proxy_url.rstrip('/') if proxy_url else "https://api.mistral.ai"
        elif provider == "groq":
            return proxy_url.rstrip('/') if proxy_url else "https://api.groq.com/openai"
        elif provider == "minimax":
            return proxy_url.rstrip('/') if proxy_url else config.conf["VisionAssistant"].get("minimax_api_host", "https://api.minimax.io/v1").strip() or "https://api.minimax.io/v1"
        return ""

    @staticmethod
    def get_endpoint(task_type, model_override=None):
        p = config.conf["VisionAssistant"]["active_provider"]
        adv = config.conf["VisionAssistant"]["use_advanced_endpoints"]
        base = AIHandler.get_base_url(p)
        
        model = model_override or ""
        if not model:
            if p == "custom":
                target_model_map = {
                    "vision": "custom_ocr_model",
                    "ocr": "custom_ocr_model",
                    "stt": "custom_stt_model",
                    "tts": "custom_tts_model",
                    "operator": "custom_operator_model",
                    "video": "custom_video_model"
                }
                if task_type in target_model_map:
                    model = config.conf["VisionAssistant"].get(target_model_map[task_type], "").strip()
                
                if not model:
                    model = config.conf["VisionAssistant"]["custom_model_name"].strip()
            
            if not model and config.conf["VisionAssistant"].get("advanced_model_routing", False):
                model = config.conf["VisionAssistant"].get(f"{p}_{task_type}_model", "").strip()
            
            if not model:
                m_key = "model_name" if p == "gemini" else f"{p}_model_name"
                model = config.conf["VisionAssistant"].get(m_key, "")

        if task_type == "tts" and AIHandler.is_gemini() and "gemini" in model.lower():
            if "pro" in model.lower(): model = "gemini-2.5-pro-preview-tts"
            else: model = "gemini-3.1-flash-tts-preview"

        if not base:
            base_map = {"mistral": "https://api.mistral.ai", "openai": "https://api.openai.com", "groq": "https://api.groq.com/openai", "gemini": "https://generativelanguage.googleapis.com", "minimax": "https://api.minimax.io/v1"}
            base = base_map.get(p, "")
            
        if p == "custom" and adv:
            target_map = {"models": "custom_models_url", "vision": "custom_ocr_url", "ocr": "custom_ocr_url", "stt": "custom_stt_url", "tts": "custom_tts_url", "operator": "custom_operator_url"}
            target_key = target_map.get(task_type)
            if target_key:
                target = config.conf["VisionAssistant"].get(target_key, "").strip()
                if target.lower().startswith("http"): return target

        base = base.rstrip('/')
        if AIHandler.is_gemini():
            if ":generateContent" in base: return base
            clean_base = re.sub(r'/(v1|v1beta|v1alpha)$', '', base, flags=re.IGNORECASE)
            v_tag = "/v1beta"
            if task_type == "models": return f"{clean_base}{v_tag}/models"
            if task_type == "upload":
                return f"{clean_base}/upload{v_tag}/files"
            return f"{clean_base}{v_tag}/models/{model}:generateContent"
            
        v1_base = base if "/v1" in base.lower() else f"{base}/v1"
        if task_type == "models": return f"{v1_base}/models"
        if task_type in ["chat", "vision", "ocr", "operator"]: return f"{v1_base}/chat/completions"
        if task_type == "upload": return f"{v1_base}/files"
        if task_type == "stt": return f"{v1_base}/audio/transcriptions"
        if task_type == "tts": return f"{v1_base}/audio/speech"
        return v1_base

    @staticmethod
    def get_keys(provider):
        if provider == "gemini": key_name = "api_key"
        elif provider == "custom": key_name = "custom_api_key"
        else: key_name = f"{provider}_api_key"
        raw = config.conf["VisionAssistant"].get(key_name, "")
        return [k.strip() for k in str(raw).replace('\r\n', ',').replace('\n', ',').split(',') if k.strip()]

    @staticmethod
    def get_models(task="main"):
        p = config.conf["VisionAssistant"]["active_provider"]
        keys = AIHandler.get_keys(p)
        key = keys[0] if keys else ""
        
        custom_type = config.conf["VisionAssistant"].get("custom_api_type", "openai")
        is_gemini_logic = (p == "gemini" or (p == "custom" and custom_type == "gemini"))
        
        url = AIHandler.get_endpoint("models")
        
        if not url:
            return []
            
        if is_gemini_logic and key and "key=" not in url:
            url += ("&" if "?" in url else "?") + f"key={key}"
            
        try:
            ssl_context = ssl.create_default_context()
            proxy_opener = get_proxy_opener(url)
            proxy_opener.add_handler(request.HTTPSHandler(context=ssl_context))
            
            req = request.Request(url, method="GET")
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            req.add_header("Accept", "application/json")
            
            if not is_gemini_logic and key:
                req.add_header("Authorization", f"Bearer {key}")
                
            with proxy_opener.open(req, timeout=15) as r:
                res_body = r.read().decode('utf-8')
                data = json.loads(res_body)
                models_info = []

                if "data" in data and isinstance(data["data"], list):
                    for m in data["data"]:
                        m_id = m.get("id")
                        if m_id: models_info.append((m_id, m_id))
                elif "models" in data and isinstance(data["models"], list):
                    for m in data["models"]:
                        full_name = m.get("name", "")
                        m_id = full_name.split("/")[-1] if "/" in full_name else full_name
                        if m_id: models_info.append((m_id, m.get("displayName", m_id)))
                elif isinstance(data, list):
                    for m in data:
                        m_id = m.get("id") or m.get("name")
                        if m_id: models_info.append((m_id, m_id))

                return AIHandler.filter_models(p, models_info, task=task)
        except error.HTTPError as e:
            try:
                raw_err = e.read().decode('utf-8')
                err_json = json.loads(raw_err)
                err_val = err_json.get("error")
                if isinstance(err_val, dict):
                    server_msg = err_val.get("message")
                else:
                    server_msg = err_val or err_json.get("message")
                if server_msg:
                    log.error(f"Fetch models failed for {p}: {server_msg}")
                    return []
            except Exception:
                pass
            log.error(f"Fetch models failed for {p}: {e}")
            return []
        except Exception as e:
            log.error(f"Fetch models failed for {p}: {e}")
            return []

    @staticmethod
    def call(prompt, attachments=None, json_mode=False, task="chat"):
        p = config.conf["VisionAssistant"]["active_provider"]
        if AIHandler.is_gemini():
            forced_key = None
            if attachments:
                for att in attachments:
                    if isinstance(att, dict) and 'file_uri' in att:
                        forced_key = GeminiHandler._get_registered_key(att['file_uri'])
                        if forced_key:
                            break
            if forced_key:
                return GeminiHandler._call_with_key(GeminiHandler._logic, forced_key, prompt, attachments, json_mode, task)

            return GeminiHandler._call_with_rotation(GeminiHandler._logic, prompt, attachments, json_mode, task, task=task)
        

        keys = AIHandler.get_keys(p)
        if not keys and p != "custom":
            # Translators: Error when no API keys are found in settings
            return "ERROR:" + _("No API Keys configured.")
        if not keys: keys = [""]

        is_audio = any(a.get('mime_type', '').startswith('audio/') for a in attachments) if attachments else False
        is_image = any(a.get('mime_type', '').startswith('image/') for a in attachments) if attachments else False
        
        custom_audio_chat = (
            p == "custom"
            and is_audio
            and not (
                config.conf["VisionAssistant"].get("use_advanced_endpoints", False)
                and config.conf["VisionAssistant"].get("custom_stt_url", "").strip()
            )
        )

        if is_audio and not AIHandler.is_gemini() and not custom_audio_chat:
            audio_att = next(a for a in attachments if a.get('mime_type', '').startswith('audio/'))
            url = AIHandler.get_endpoint("stt")
            model = "whisper-1"
            if p == "groq": model = "whisper-large-v3-turbo"
            elif p == "mistral": model = "voxtral-mini-latest"
            elif p == "minimax": model = config.conf["VisionAssistant"]["minimax_stt_model"].strip() or "asr-01"
            if p == "custom":
                model = config.conf["VisionAssistant"]["custom_stt_model"].strip() or config.conf["VisionAssistant"]["custom_model_name"].strip() or model
            elif config.conf["VisionAssistant"].get("advanced_model_routing", False):
                adv_stt = config.conf["VisionAssistant"].get(f"{p}_stt_model", "").strip()
                if adv_stt: model = adv_stt
            return AIHandler._transcribe_helper(keys[0], audio_att, url, model)

        for key in keys:
            try:
                current_task = "vision" if is_image and task == "chat" else task
                url = AIHandler.get_endpoint(current_task)
                
                if p == "custom":
                    model = config.conf["VisionAssistant"]["custom_model_name"].strip()
                    if current_task in ["vision", "ocr"]: model = config.conf["VisionAssistant"]["custom_ocr_model"].strip()
                    if not model: model = config.conf["VisionAssistant"]["custom_model_name"].strip()
                else:
                    m_key = f"{p}_model_name"
                    model = config.conf["VisionAssistant"].get(m_key, "")
                    if config.conf["VisionAssistant"].get("advanced_model_routing", False):
                        adv_model = config.conf["VisionAssistant"].get(f"{p}_{current_task}_model", "").strip()
                        if adv_model: model = adv_model

                if not model:
                    return "ERROR: Model name is empty."

                if isinstance(prompt, str):
                    if attachments:
                        contents = []
                        if prompt: contents.append({"type": "text", "text": prompt})
                        for att in attachments:
                            if "data" in att and att.get('mime_type', '').startswith('image/'):
                                contents.append({"type": "image_url", "image_url": {"url": f"data:{att['mime_type']};base64,{att['data']}"}})
                            elif custom_audio_chat and "data" in att and att.get('mime_type', '').startswith('audio/'):
                                audio_format = att['mime_type'].split('/', 1)[-1].replace('mpeg', 'mp3')
                                contents.append({
                                    "type": "input_audio",
                                    "input_audio": {
                                        "data": att['data'],
                                        "format": audio_format,
                                    },
                                })
                        messages = [{"role": "user", "content": contents}]
                    else:
                        messages = [{"role": "user", "content": prompt}]
                else:
                    messages = prompt

                temp = config.conf["VisionAssistant"].get("ai_temperature", 0.7)
                payload = {"model": model, "messages": messages, "temperature": temp, "stream": False}
                if json_mode: payload["response_format"] = {"type": "json_object"}
                
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
                if key and key.strip(): headers["Authorization"] = f"Bearer {key}"
                
                req = request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
                with get_proxy_opener(url).open(req, timeout=180) as r:
                    res = json.loads(r.read().decode('utf-8'))
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
                    raw_err = e.read().decode('utf-8')
                    err_json = json.loads(raw_err)
                    err_val = err_json.get("error")
                    if isinstance(err_val, dict):
                        server_msg = err_val.get("message")
                    else:
                        server_msg = err_val or err_json.get("message")
                    if server_msg:
                        if key == keys[-1]: return f"ERROR: {server_msg}"
                        continue
                except Exception:
                    pass
                if key == keys[-1]: return f"ERROR: {str(e)}"
                continue
            except Exception as e:
                if key == keys[-1]: return f"ERROR: {str(e)}"
                continue

    @staticmethod
    def ocr(img_or_pdf_base64, mime_type="image/jpeg"):
        p = config.conf["VisionAssistant"]["active_provider"]
        if p == "mistral":
            keys = AIHandler.get_keys("mistral")
            # Translators: Error message shown when the user attempts an AI operation without configuring any API keys in the settings.
            if not keys: return "ERROR:" + _("No API Keys configured.")
            
            is_pdf = "pdf" in mime_type.lower()
            base_url = AIHandler.get_base_url("mistral").rstrip('/')
            v1_base = base_url if "/v1" in base_url.lower() else f"{base_url}/v1"
            
            upload_url = f"{v1_base}/files"
            ocr_url = f"{v1_base}/ocr"
            
            model = config.conf["VisionAssistant"].get("mistral_ocr_model", "").strip()
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
                        
                    boundary = f"Boundary-{uuid4()}"
                    body = []
                    body.append(f"--{boundary}".encode())
                    filename = "document.pdf" if is_pdf else "image.jpg"
                    body.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode())
                    body.append(f"Content-Type: {mime_type}".encode())
                    body.append(b'')
                    body.append(file_bytes)
                    body.append(f"--{boundary}".encode())
                    body.append(b'Content-Disposition: form-data; name="purpose"')
                    body.append(b'')
                    body.append(b'ocr')
                    body.append(f"--{boundary}--".encode())
                    body.append(b'')
                    
                    upload_headers = {
                        "Content-Type": f"multipart/form-data; boundary={boundary}",
                        "Authorization": f"Bearer {key}",
                        "User-Agent": "Mozilla/5.0"
                    }
                    
                    req_upload = request.Request(upload_url, data=b'\r\n'.join(body), headers=upload_headers, method="POST")
                    with get_proxy_opener(upload_url).open(req_upload, timeout=120) as r:
                        upload_res = json.loads(r.read().decode())
                        file_id = upload_res.get("id")
                        
                    if not file_id:
                        raise ValueError("File upload failed to return an ID")
                        
                    payload = {
                        "model": model,
                        "document": {
                            "type": "file",
                            "file_id": file_id
                        }
                    }
                    
                    ocr_headers = {
                        "Authorization": f"Bearer {key}",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0"
                    }
                    
                    req_ocr = request.Request(ocr_url, data=json.dumps(payload).encode(), headers=ocr_headers, method="POST")
                    with get_proxy_opener(ocr_url).open(req_ocr, timeout=120) as r:
                        res = json.loads(r.read().decode())
                        
                        try:
                            delete_url = f"{v1_base}/files/{file_id}"
                            req_del = request.Request(delete_url, headers={"Authorization": f"Bearer {key}"}, method="DELETE")
                            with get_proxy_opener(delete_url).open(req_del, timeout=10) as r_del: pass
                        except Exception: pass
                        
                        return "[[[PAGE_SEP]]]".join([pg.get("markdown", "") for pg in res.get("pages", [])])
                        
                except error.HTTPError as e:
                    if (e.code == 429 or e.code >= 500) and key != keys[-1]: continue
                    return f"ERROR: {e.code}"
                except Exception as e:
                    if key == keys[-1]: return f"ERROR: {str(e)}"
                    continue
        return AIHandler.call(get_prompt_text("ocr_image_extract"), attachments=[{'mime_type': mime_type, 'data': img_or_pdf_base64}], task="ocr")

    @staticmethod
    def _transcribe_helper(key, audio_att, url, model_name):
        try:
            boundary = f"Boundary-{uuid.uuid4()}"
            body = []
            body.append(f"--{boundary}".encode()); body.append(b'Content-Disposition: form-data; name="file"; filename="audio.wav"'); body.append(f"Content-Type: {audio_att['mime_type']}".encode()); body.append(b''); body.append(base64.b64decode(audio_att['data'])); body.append(f"--{boundary}".encode()); body.append(b'Content-Disposition: form-data; name="model"'); body.append(b''); body.append(model_name.encode()); body.append(f"--{boundary}--".encode()); body.append(b'')
            headers = {"Content-Type": f"multipart/form-data; boundary={boundary}", "User-Agent": "Mozilla/5.0"}
            if key and key.strip(): headers["Authorization"] = f"Bearer {key}"
            req = request.Request(url, data=b'\r\n'.join(body), headers=headers)
            with get_proxy_opener(url).open(req, timeout=60) as r: return json.loads(r.read().decode())["text"]
        except Exception as e: 
            log.error(f"Transcription helper failed: {e}")
            # Translators: Error message when speech-to-text fails.
            return "ERROR: " + _("Transcription Failed") + f" ({str(e)})"

    @staticmethod
    def generate_speech(text, voice_name, model_override=None):
        if not AIHandler.is_tts_supported():
            # Translators: Error message when TTS is not supported by the provider
            return "ERROR:" + _("TTS is not supported by this provider."), False
            
        p = config.conf["VisionAssistant"]["active_provider"]
        if AIHandler.is_gemini(): return GeminiHandler.generate_speech(text, voice_name), True
        keys = AIHandler.get_keys(p)
        if not keys and p != "custom": 
            # Translators: Error when no API keys are found in settings
            return "ERROR:" + _("No API Keys configured."), False
        if not keys: keys = [""]
        url = AIHandler.get_endpoint("tts")
        m_key = "model_name" if p == "gemini" else f"{p}_model_name"
        model = model_override or config.conf["VisionAssistant"].get(m_key, "")
        
        if p == "custom": 
            model = config.conf["VisionAssistant"]["custom_tts_model"].strip() or "tts-1"
        elif config.conf["VisionAssistant"].get("advanced_model_routing", False):
            adv_tts = config.conf["VisionAssistant"].get(f"{p}_tts_model", "").strip()
            if adv_tts: model = adv_tts
            elif p == "openai": model = "tts-1"
        elif p == "openai":
            model = "tts-1"

        if p == "minimax":
            minimax_base = AIHandler.get_base_url("minimax").rstrip('/') or "https://api.minimax.io/v1"
            minimax_tts_url = f"{minimax_base}/t2a_v2"
            model = config.conf["VisionAssistant"].get("minimax_tts_model", "speech-2.8-hd").strip() or "speech-2.8-hd"
            minimax_voice = voice_name if voice_name else config.conf["VisionAssistant"]["minimax_tts_voice"].strip() or "English_expressive_narrator"
            minimax_payload = {
                "model": model,
                "text": text,
                "voice_setting": {"voice_id": minimax_voice, "speed": 1.0, "vol": 1.0, "pitch": 0},
                "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1}
            }
            for key in keys:
                try:
                    headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
                    if key and key.strip(): headers["Authorization"] = f"Bearer {key}"
                    req = request.Request(minimax_tts_url, data=json.dumps(minimax_payload).encode(), headers=headers)
                    with get_proxy_opener(minimax_tts_url).open(req, timeout=600) as r:
                        resp_json = json.loads(r.read().decode("utf-8"))
                        hex_audio = resp_json.get("data", {}).get("audio", "")
                        if not hex_audio:
                            return "ERROR: MiniMax TTS returned no audio data.", False
                        audio_bytes = bytes.fromhex(hex_audio)
                        return base64.b64encode(audio_bytes).decode("utf-8"), False
                except Exception as e:
                    if key == keys[-1]: return f"ERROR: {str(e)}", False
                    continue

        payload = {"model": model, "input": text, "voice": voice_name.lower(), "response_format": "mp3"}
        for key in keys:
            try:
                headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
                if key and key.strip(): headers["Authorization"] = f"Bearer {key}"
                req = request.Request(url, data=json.dumps(payload).encode(), headers=headers)
                with get_proxy_opener(url).open(req, timeout=600) as r: return base64.b64encode(r.read()).decode('utf-8'), False
            except Exception as e:
                if key == keys[-1]: return f"ERROR: {str(e)}", False
                continue

    @staticmethod
    def translate(text, target_lang):
        if AIHandler.is_gemini():
            return GeminiHandler.translate(text, target_lang)
        quick_template = get_prompt_text("translate_quick") or "Translate to {target_lang}. Output ONLY translation."
        quick_prompt = apply_prompt_template(quick_template, [("target_lang", target_lang)])
        prompt = f"{quick_prompt}\n\n{text}"
        res = AIHandler.call(prompt)
        if res and not res.startswith("ERROR:"):
            return res
        return text

    @staticmethod
    def upload_to_mistral_for_chat(file_path):
        keys = AIHandler.get_keys("mistral")
        if not keys: return None, "ERROR:" + _("No API Keys configured.")
        
        base_url = AIHandler.get_base_url("mistral").rstrip('/')
        v1_base = base_url if "/v1" in base_url.lower() else f"{base_url}/v1"
        upload_url = f"{v1_base}/files"
        
        for key in keys:
            try:
                with open(file_path, "rb") as f:
                    file_bytes = f.read()
                    
                boundary = f"Boundary-{uuid4()}"
                body = []
                body.append(f"--{boundary}".encode())
                body.append(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(file_path)}"'.encode())
                body.append(b"Content-Type: application/pdf")
                body.append(b'')
                body.append(file_bytes)
                body.append(f"--{boundary}".encode())
                body.append(b'Content-Disposition: form-data; name="purpose"')
                body.append(b'')
                body.append(b'ocr')
                body.append(f"--{boundary}--".encode())
                body.append(b'')
                
                upload_headers = {
                    "Content-Type": f"multipart/form-data; boundary={boundary}",
                    "Authorization": f"Bearer {key}",
                    "User-Agent": "Mozilla/5.0"
                }
                
                req_upload = request.Request(upload_url, data=b'\r\n'.join(body), headers=upload_headers, method="POST")
                opener = get_proxy_opener(upload_url)
                with opener.open(req_upload, timeout=120) as r:
                    upload_res = json.loads(r.read().decode())
                    file_id = upload_res.get("id")
                    
                if not file_id:
                    continue

                signed_url_endpoint = f"{v1_base}/files/{file_id}/url?expiry=24"
                req_signed = request.Request(signed_url_endpoint, headers={"Authorization": f"Bearer {key}", "Accept": "application/json"})
                with opener.open(req_signed, timeout=30) as r:
                    signed_res = json.loads(r.read().decode())
                    signed_url = signed_res.get("url")
                    
                if signed_url:
                    return file_id, signed_url
                    
            except Exception as e:
                log.error(f"Mistral upload failed: {e}")
                continue
                
        # Translators: Error message for upload failure
        return None, "ERROR:" + _("Upload failed.")

    @staticmethod
    def delete_mistral_file(file_id):
        keys = AIHandler.get_keys("mistral")
        if not keys or not file_id: return
        base_url = AIHandler.get_base_url("mistral").rstrip('/')
        v1_base = base_url if "/v1" in base_url.lower() else f"{base_url}/v1"
        delete_url = f"{v1_base}/files/{file_id}"
        
        for key in keys:
            try:
                req_del = request.Request(delete_url, headers={"Authorization": f"Bearer {key}"}, method="DELETE")
                with get_proxy_opener(delete_url).open(req_del, timeout=10) as r_del:
                    break
            except Exception:
                pass

class _MinimalWebSocket:

    def __init__(self, host, path, timeout=30):
        self.host = host
        self.path = path
        self.timeout = timeout
        self.sock = None
        self._recv_buf = b""
        self.closed = False
        self.close_reason = None
        self._send_lock = threading.Lock()

    def connect(self):
        proxy_url = config.conf["VisionAssistant"]["proxy_url"].strip()
        raw = None
        is_reverse_proxy = False
        
        if proxy_url:
            try:
                clean_proxy = proxy_url if "://" in proxy_url else "http://" + proxy_url
                parsed_proxy = urlparse(clean_proxy)
                p_host = parsed_proxy.hostname or ""
                if p_host and "." in p_host and not p_host.replace(".", "").isdigit() and p_host.lower() not in ["localhost", "127.0.0.1"]:
                    is_reverse_proxy = True
            except Exception:
                pass
        
        if proxy_url and not is_reverse_proxy:
            if not (proxy_url.startswith("http://") or proxy_url.startswith("https://")):
                proxy_url = "http://" + proxy_url
            try:
                parsed = urlparse(proxy_url)
                proxy_host = parsed.hostname
                proxy_port = parsed.port if parsed.port else 80
                
                raw = socket.create_connection((proxy_host, proxy_port), timeout=self.timeout)
                connect_req = f"CONNECT {self.host}:443 HTTP/1.1\r\nHost: {self.host}:443\r\n"
                
                if parsed.username:
                    auth_str = f"{parsed.username}:{parsed.password or ''}"
                    encoded_auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
                    connect_req += f"Proxy-Authorization: Basic {encoded_auth}\r\n"
                    
                connect_req += "\r\n"
                raw.sendall(connect_req.encode('utf-8'))
                
                resp = b""
                while b"\r\n\r\n" not in resp:
                    chunk = raw.recv(4096)
                    if not chunk:
                        raise ConnectionError("Proxy tunnel closed connection abruptly.")
                    resp += chunk
                    
                status_line = resp.split(b"\r\n", 1)[0]
                if b" 200 " not in status_line:
                    raise ConnectionError(f"Proxy tunnel establishment failed: {status_line.decode('utf-8', 'replace')}")
            except Exception as e:
                log.error(f"Failed to connect through proxy: {e}", exc_info=True)
                if raw:
                    try: raw.close()
                    except Exception: pass
                raise
        else:
            raw = socket.create_connection((self.host, 443), timeout=self.timeout)
            
        ctx = ssl.create_default_context()
        self.sock = ctx.wrap_socket(raw, server_hostname=self.host)
        key = base64.b64encode(os.urandom(16)).decode()
        handshake = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(handshake.encode())
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("WebSocket handshake closed")
            resp += chunk
        if b" 101 " not in resp.split(b"\r\n", 1)[0]:
            raise ConnectionError(f"WebSocket handshake failed: {resp[:120]!r}")
        self._recv_buf = resp.split(b"\r\n\r\n", 1)[1]
        
        self.sock.settimeout(1.0)

    def _send_frame(self, opcode, payload):
        if self.closed:
            return
        header = bytearray()
        header.append(0x80 | opcode)
        mask = os.urandom(4)
        length = len(payload)
        if length < 126:
            header.append(0x80 | length)
        elif length < 65536:
            header.append(0x80 | 126)
            header += struct.pack(">H", length)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", length)
        header += mask
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        frame = bytes(header) + masked
        with self._send_lock:
            if self.closed:
                return
            self.sock.sendall(frame)

    def send_text(self, text):
        self._send_frame(0x1, text.encode("utf-8"))

    def _recv_exact(self, n):
        while len(self._recv_buf) < n:
            if self.closed:
                raise ConnectionError("WebSocket closed")
            try:
                chunk = self.sock.recv(65536)
                if not chunk:
                    self.close()
                    raise ConnectionError("WebSocket connection closed")
                self._recv_buf += chunk
            except (BlockingIOError, ssl.SSLWantReadError, socket.timeout):
                time.sleep(0.01)
                continue
            except ssl.SSLError as e:
                if "timed out" in str(e).lower():
                    time.sleep(0.01)
                    continue
                self.close()
                raise
            except Exception:
                self.close()
                raise
        data, self._recv_buf = self._recv_buf[:n], self._recv_buf[n:]
        return data

    def recv(self):

        try:
            b0, b1 = self._recv_exact(2)
            opcode = b0 & 0x0F
            length = b1 & 0x7F
            if length == 126:
                length = struct.unpack(">H", self._recv_exact(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self._recv_exact(8))[0]
            payload = self._recv_exact(length) if length else b""
            if opcode == 0x8:
                if len(payload) >= 2:
                    code = struct.unpack(">H", payload[:2])[0]
                    text = payload[2:].decode("utf-8", "replace")
                    self.close_reason = f"{code} {text}".strip()
                self.closed = True
                return None, None
            return opcode, payload
        except Exception as e:
            self.close_reason = self.close_reason or f"recv error: {e}"
            self.closed = True
            return None, None

    def close(self):
        if self.closed:
            return
        try:
            self._send_frame(0x8, b"")
        except Exception:
            pass
        self.closed = True
        try:
            if self.sock: self.sock.close()
        except Exception:
            pass

class _MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]

class _KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]

class _HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]

class _INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", _MOUSEINPUT),
        ("ki", _KEYBDINPUT),
        ("hi", _HARDWAREINPUT),
    ]

class _INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("union", _INPUT_UNION),
    ]

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_EXTENDEDKEY = 0x0001
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x1000
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_VIRTUALDESK = 0x4000
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79
class MouseSimulator:
    _user32 = ctypes.windll.user32
    
    @staticmethod
    def _get_screen_size():
        try:
            dpi = ctypes.windll.user32.GetDpiForSystem()
            if dpi <= 0:
                dpi = 96
        except Exception:
            dpi = 96
        w_logical = ctypes.windll.user32.GetSystemMetrics(0)
        h_logical = ctypes.windll.user32.GetSystemMetrics(1)
        scale = dpi / 96.0
        w_physical = int(w_logical * scale)
        h_physical = int(h_logical * scale)
        return w_physical, h_physical, scale
    
    @staticmethod
    def _make_mouse_input(flags, dx=0, dy=0, data=0):
        inp = _INPUT()
        inp.type = INPUT_MOUSE
        inp.union.mi.dx = dx
        inp.union.mi.dy = dy
        inp.union.mi.mouseData = data
        inp.union.mi.dwFlags = flags
        inp.union.mi.time = 0
        inp.union.mi.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0))
        return inp
    
    @staticmethod
    def _make_keyboard_input(vk, flags=0):
        inp = _INPUT()
        inp.type = INPUT_KEYBOARD
        inp.union.ki.wVk = vk
        inp.union.ki.wScan = 0
        inp.union.ki.dwFlags = flags
        inp.union.ki.time = 0
        inp.union.ki.dwExtraInfo = ctypes.pointer(ctypes.c_ulong(0))
        return inp
    
    @staticmethod
    def _send_inputs(*inputs):
        n = len(inputs)
        arr = (_INPUT * n)(*inputs)
        result = ctypes.windll.user32.SendInput(
            n,
            ctypes.pointer(arr),
            ctypes.sizeof(_INPUT)
        )
        if result != n:
            log.warning(f"SendInput injected {result}/{n} events")
        return result == n
    
    @staticmethod
    def move_to(x, y, smooth=False, steps=15, step_delay=0.01):
        if smooth:
            try:
                curr_x, curr_y = winUser.getCursorPos()
            except Exception:
                curr_x, curr_y = 0, 0
            for i in range(1, steps + 1):
                progress = i / steps
                eased = 1 - (1 - progress) ** 2
                cx = int(curr_x + (x - curr_x) * eased)
                cy = int(curr_y + (y - curr_y) * eased)
                ctypes.windll.user32.SetCursorPos(cx, cy)
                time.sleep(step_delay)
        else:
            ctypes.windll.user32.SetCursorPos(int(x), int(y))
            time.sleep(0.02)
    
    @staticmethod
    def click(x, y, button="left", double=False):
        MouseSimulator.move_to(x, y)
        time.sleep(0.05)
        if button == "left":
            down_flag = MOUSEEVENTF_LEFTDOWN
            up_flag = MOUSEEVENTF_LEFTUP
        elif button == "right":
            down_flag = MOUSEEVENTF_RIGHTDOWN
            up_flag = MOUSEEVENTF_RIGHTUP
        elif button == "middle":
            down_flag = MOUSEEVENTF_MIDDLEDOWN
            up_flag = MOUSEEVENTF_MIDDLEUP
        else:
            down_flag = MOUSEEVENTF_LEFTDOWN
            up_flag = MOUSEEVENTF_LEFTUP
        count = 2 if double else 1
        for _i in range(count):
            inputs = [
                MouseSimulator._make_mouse_input(down_flag),
                MouseSimulator._make_mouse_input(up_flag),
            ]
            MouseSimulator._send_inputs(*inputs)
            if double:
                time.sleep(0.05)
        time.sleep(0.1)
    
    @staticmethod
    def _get_virtual_rect():
        u = ctypes.windll.user32
        vx = u.GetSystemMetrics(SM_XVIRTUALSCREEN)
        vy = u.GetSystemMetrics(SM_YVIRTUALSCREEN)
        vw = u.GetSystemMetrics(SM_CXVIRTUALSCREEN)
        vh = u.GetSystemMetrics(SM_CYVIRTUALSCREEN)
        if vw <= 0: vw = u.GetSystemMetrics(0)
        if vh <= 0: vh = u.GetSystemMetrics(1)
        return vx, vy, vw, vh

    @staticmethod
    def _abs_move(x, y, rect):
        vx, vy, vw, vh = rect
        nx = int((x - vx) * 65535 / max(vw - 1, 1))
        ny = int((y - vy) * 65535 / max(vh - 1, 1))
        move = MouseSimulator._make_mouse_input(
            MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK,
            dx=nx, dy=ny)
        MouseSimulator._send_inputs(move)

    @staticmethod
    def drag(start_x, start_y, end_x, end_y, duration=0.8, steps=60):
        start_x, start_y = int(start_x), int(start_y)
        end_x, end_y = int(end_x), int(end_y)
        rect = MouseSimulator._get_virtual_rect()

        MouseSimulator._abs_move(start_x, start_y, rect)
        time.sleep(0.15)
        MouseSimulator._abs_move(start_x, start_y, rect)
        time.sleep(0.15)

        down_input = MouseSimulator._make_mouse_input(MOUSEEVENTF_LEFTDOWN)
        MouseSimulator._send_inputs(down_input)
        time.sleep(0.25)

        nudge_x = 8 if end_x >= start_x else -8
        nudge_y = 8 if end_y >= start_y else -8
        MouseSimulator._abs_move(start_x + nudge_x, start_y + nudge_y, rect)
        time.sleep(0.12)

        step_delay = duration / steps
        for i in range(1, steps + 1):
            progress = i / steps
            cx = int(start_x + (end_x - start_x) * progress)
            cy = int(start_y + (end_y - start_y) * progress)
            MouseSimulator._abs_move(cx, cy, rect)
            time.sleep(step_delay)

        MouseSimulator._abs_move(end_x, end_y, rect)
        time.sleep(0.2)
        MouseSimulator._abs_move(end_x, end_y, rect)
        time.sleep(0.35)

        up_input = MouseSimulator._make_mouse_input(MOUSEEVENTF_LEFTUP)
        MouseSimulator._send_inputs(up_input)
        time.sleep(0.15)

    @staticmethod
    def scroll(x, y, direction="down", clicks=3):
        MouseSimulator.move_to(x, y)
        time.sleep(0.05)
        delta = 120 if direction == "up" else -120
        total_delta = delta * clicks
        scroll_input = MouseSimulator._make_mouse_input(
            MOUSEEVENTF_WHEEL,
            data=total_delta & 0xFFFFFFFF
        )
        MouseSimulator._send_inputs(scroll_input)
        time.sleep(0.1)
    
    @staticmethod
    def key_press(vk_code, extended=False):
        flags_down = KEYEVENTF_EXTENDEDKEY if extended else 0
        flags_up = KEYEVENTF_KEYUP | (KEYEVENTF_EXTENDEDKEY if extended else 0)
        inputs = [
            MouseSimulator._make_keyboard_input(vk_code, flags_down),
            MouseSimulator._make_keyboard_input(vk_code, flags_up),
        ]
        MouseSimulator._send_inputs(*inputs)
    
    @staticmethod
    def type_text(text, press_enter=False):
        old_clip = None
        try:
            old_clip = api.getClipData()
        except Exception:
            pass
        try:
            clean_text = text.replace('\n', '').strip()
            api.copyToClip(clean_text)
            time.sleep(0.2)
            VK_CONTROL = 0x11
            VK_V = 0x56
            inputs = [
                MouseSimulator._make_keyboard_input(VK_CONTROL, 0),
                MouseSimulator._make_keyboard_input(VK_V, 0),
                MouseSimulator._make_keyboard_input(VK_V, KEYEVENTF_KEYUP),
                MouseSimulator._make_keyboard_input(VK_CONTROL, KEYEVENTF_KEYUP),
            ]
            MouseSimulator._send_inputs(*inputs)
            time.sleep(0.3)
        finally:
            if old_clip is not None:
                try:
                    api.copyToClip(old_clip)
                except Exception:
                    pass
        if press_enter:
            time.sleep(0.2)
            MouseSimulator.key_press(0x0D)

class _WAVEFORMATEX(ctypes.Structure):
    _fields_ = [
        ("wFormatTag", ctypes.c_ushort),
        ("nChannels", ctypes.c_ushort),
        ("nSamplesPerSec", ctypes.c_uint),
        ("nAvgBytesPerSec", ctypes.c_uint),
        ("nBlockAlign", ctypes.c_ushort),
        ("wBitsPerSample", ctypes.c_ushort),
        ("cbSize", ctypes.c_ushort),
    ]


class _WAVEHDR(ctypes.Structure):
    pass


_WAVEHDR._fields_ = [
    ("lpData", ctypes.c_char_p),
    ("dwBufferLength", ctypes.c_uint),
    ("dwBytesRecorded", ctypes.c_uint),
    ("dwUser", ctypes.c_void_p),
    ("dwFlags", ctypes.c_uint),
    ("dwLoops", ctypes.c_uint),
    ("lpNext", ctypes.POINTER(_WAVEHDR)),
    ("reserved", ctypes.c_void_p),
]


class _MicCapture:
    _CALLBACK_NULL = 0x00000000
    _WHDR_DONE = 0x00000001

    def __init__(self, on_data, sample_rate=16000, block_ms=100):
        self.on_data = on_data
        self.sample_rate = sample_rate
        self.block_size = int(sample_rate * 2 * block_ms / 1000)
        self.hwi = None
        self._running = False
        self._thread = None
        self._buffers = []

    def start(self):
        winmm = ctypes.windll.winmm
        fmt = _WAVEFORMATEX(
            wFormatTag=1,
            nChannels=1,
            nSamplesPerSec=self.sample_rate,
            nAvgBytesPerSec=self.sample_rate * 2,
            nBlockAlign=2,
            wBitsPerSample=16,
            cbSize=0,
        )
        self.hwi = ctypes.c_void_p()
        res = winmm.waveInOpen(ctypes.byref(self.hwi), 0xFFFFFFFF, ctypes.byref(fmt), 0, 0, self._CALLBACK_NULL)
        if res != 0:
            raise OSError(f"waveInOpen failed: {res}")
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def _make_header(self):
        buf = ctypes.create_string_buffer(self.block_size)
        hdr = _WAVEHDR()
        hdr.lpData = ctypes.cast(buf, ctypes.c_char_p)
        hdr.dwBufferLength = self.block_size
        hdr.dwFlags = 0
        return buf, hdr

    def _loop(self):
        winmm = ctypes.windll.winmm
        hdr_size = ctypes.sizeof(_WAVEHDR)
        headers = [self._make_header() for _i in range(4)]
        for buf, hdr in headers:
            winmm.waveInPrepareHeader(self.hwi, ctypes.byref(hdr), hdr_size)
            winmm.waveInAddBuffer(self.hwi, ctypes.byref(hdr), hdr_size)
        winmm.waveInStart(self.hwi)
        try:
            while self._running:
                progressed = False
                for buf, hdr in headers:
                    if hdr.dwFlags & self._WHDR_DONE:
                        recorded = hdr.dwBytesRecorded
                        if recorded and self.on_data:
                            try: self.on_data(buf.raw[:recorded])
                            except Exception: pass
                        winmm.waveInUnprepareHeader(self.hwi, ctypes.byref(hdr), hdr_size)
                        hdr.dwFlags = 0
                        hdr.dwBytesRecorded = 0
                        winmm.waveInPrepareHeader(self.hwi, ctypes.byref(hdr), hdr_size)
                        winmm.waveInAddBuffer(self.hwi, ctypes.byref(hdr), hdr_size)
                        progressed = True
                if not progressed:
                    time.sleep(0.01)
        finally:
            try: winmm.waveInStop(self.hwi)
            except Exception: pass
            for buf, hdr in headers:
                try: winmm.waveInUnprepareHeader(self.hwi, ctypes.byref(hdr), hdr_size)
                except Exception: pass

    def stop(self):
        self._running = False
        if self.hwi:
            try: ctypes.windll.winmm.waveInReset(self.hwi)
            except Exception: pass
        if self._thread:
            self._thread.join(timeout=2)
        if self.hwi:
            try: ctypes.windll.winmm.waveInClose(self.hwi)
            except Exception: pass
            self.hwi = None


class LiveSession:
    HOST = "generativelanguage.googleapis.com"

    def __init__(self, on_text, on_status, on_closed, on_stream=None):
        self.on_text = on_text
        self.on_status = on_status
        self.on_closed = on_closed
        self.on_stream = on_stream
        self.ws = None
        self.mic = None
        self.player = None
        self._running = False
        self._recv_thread = None
        self._stream_speaker = None
        self._interrupted = False
        self._player_lock = threading.Lock()

    def _get_player(self):
        with self._player_lock:
            if self._interrupted:
                return None
            if self.player is None:
                try:
                    device = ""
                    try:
                        device = config.conf["audio"]["outputDevice"]
                    except (KeyError, IndexError):
                        try:
                            device = config.conf["speech"]["outputDevice"]
                        except (KeyError, IndexError):
                            pass
                    self.player = nvwave.WavePlayer(channels=1, samplesPerSec=24000, bitsPerSample=16, outputDevice=device)
                except Exception as e:
                    log.warning(f"Live: WavePlayer with configured device failed ({e}); using default device.")
                    self.player = nvwave.WavePlayer(channels=1, samplesPerSec=24000, bitsPerSample=16)
            return self.player

    def _stop_player(self):
        with self._player_lock:
            self._interrupted = True
            if self.player:
                try:
                    self.player.stop()
                    self.player.close()
                except Exception: pass
                self.player = None

    def _resolve_model(self):
        conf = config.conf["VisionAssistant"]
        default_live = "gemini-3.1-flash-live-preview"
        provider = conf["active_provider"]
        model = ""
        if conf.get("advanced_model_routing", False):
            model = conf.get(f"{provider}_live_model", "").strip()
        if not model:
            model = conf.get("live_model", default_live).strip()
        if not model:
            model = default_live
        if "live" not in model.lower():
            log.warning(f"Live: selected model '{model}' is not a Live model; using '{default_live}'.")
            model = default_live
        return model

    def _resolve_host(self):
        try:
            base = AIHandler.get_base_url(config.conf["VisionAssistant"]["active_provider"])
            host = urlparse(base).hostname
            if host:
                return host
        except Exception:
            pass
        return self.HOST

    def start(self):
        keys = AIHandler.get_keys(config.conf["VisionAssistant"]["active_provider"])
        if not keys:
            # Translators: Error when no API keys are found in settings
            self.on_status("ERROR:" + _("No API Keys configured."))
            return False
        model = self._resolve_model()
        voice = ""
        thinking_level = ""
        plugin = _vision_assistant_instance
        if plugin and getattr(plugin, "live_dlg", None) and plugin.live_dlg:
            try:
                dlg = plugin.live_dlg
                if hasattr(dlg, "voice_sel") and dlg.voice_sel:
                    sel = dlg.voice_sel.GetSelection()
                    if sel != wx.NOT_FOUND:
                        voice = GEMINI_VOICES[sel][0]
                if hasattr(dlg, "thinking_sel") and dlg.thinking_sel:
                    t_sel = dlg.thinking_sel.GetSelection()
                    if t_sel != wx.NOT_FOUND:
                        thinking_level = dlg.thinking_choices[t_sel][1]
            except Exception:
                pass
        if not voice:
            voice = config.conf["VisionAssistant"].get("tts_voice", "Puck").strip() or "Puck"
        if not thinking_level:
            thinking_level = config.conf["VisionAssistant"].get("live_thinking_level", "medium").strip() or "medium"
        host = self._resolve_host()
        path = f"/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key={keys[0]}"
        try:
            self.ws = _MinimalWebSocket(host, path)
            self.ws.connect()
        except Exception as e:
            log.error(f"Live connect failed: {e}", exc_info=True)
            
            err_str = str(e)
            if "b'HTTP" in err_str:
                try:
                    status_part = err_str.split("HTTP/1.1 ")[1].split("\\r")[0]
                    err_str = f"HTTP {status_part}"
                except Exception:
                    pass
            
            # Translators: Error shown when the live voice session fails to connect. {error} is replaced with the specific error detail.
            err_msg = _("Could not connect to the Live service: {error}").format(error=err_str)
            self.on_status("ERROR:" + err_msg)
            return False

        lang = get_lang_name("ai_response_language")
        self.response_lang = lang
        live_instruction = apply_prompt_template(
            get_prompt_text("live_assistant_system"), [("response_lang", lang)]
        )
        setup = {
            "setup": {
                "model": f"models/{model}",
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}},
                    "thinkingConfig": {
                        "thinkingLevel": thinking_level
                    }
                },
                "realtimeInputConfig": {
                    "automaticActivityDetection": {
                        "disabled": False
                    }
                },
                "systemInstruction": {"parts": [{"text": live_instruction}]},
                "outputAudioTranscription": {},
                "inputAudioTranscription": {},
            }
        }
        try:
            self.ws.send_text(json.dumps(setup))
        except Exception as e:
            log.error(f"Live: Failed to send setup payload: {e}")
            self.stop()
            return False

        self._running = True
        self._recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._recv_thread.start()
        try:
            self.mic = _MicCapture(self._on_mic_data, block_ms=100)
            self.mic.start()
        except Exception as e:
            log.error(f"Mic capture failed: {e}", exc_info=True)
            # Translators: Error shown when the microphone cannot be opened for the live session.
            self.on_status("ERROR:" + _("Could not open the microphone."))
            self.stop()
            return False
        return True

    def _on_mic_data(self, pcm_bytes):
        if not self._running or not self.ws or self.ws.closed:
            return

        try:
            samples = array.array('h', pcm_bytes)
            peak = max(abs(s) for s in samples)
            if peak > 3000:  
                if self.player is not None:
                    self._stop_player()
                    try:
                        cancel_msg = {"clientContent": {"turnComplete": True}}
                        self.ws.send_text(json.dumps(cancel_msg))
                    except Exception: pass
        except Exception: pass

        msg = {
            "realtimeInput": {
                "audio": {
                    "mimeType": "audio/pcm;rate=16000",
                    "data": base64.b64encode(pcm_bytes).decode()
                }
            }
        }
        try:
            self.ws.send_text(json.dumps(msg))
        except Exception: pass

    def send_video_frame(self, jpeg_b64):
        if not self._running or not self.ws or self.ws.closed or not jpeg_b64:
            return
        msg = {
            "realtimeInput": {
                "video": {
                    "mimeType": "image/jpeg",
                    "data": jpeg_b64
                }
            }
        }
        try:
            self.ws.send_text(json.dumps(msg))
        except Exception: pass

    def _recv_loop(self):
        while self._running:
            opcode, payload = self.ws.recv()
            if opcode is None:
                if self._running:
                    reason = self.ws.close_reason
                    # Translators: Line shown when the live server unexpectedly closes the connection. {reason} is the server's reason.
                    self.on_text(_("[Connection closed: {reason}]").format(reason=reason or _("unknown")))
                break
            if opcode != 0x1 and opcode != 0x2:
                continue
            try:
                data = json.loads(payload.decode("utf-8", "replace"))
                self._handle_message(data)
            except Exception as e:
                log.error(f"Live: Failed to decode received payload: {e}")
        if self._running:
            self.stop()

    def _handle_message(self, data):
        if "setupComplete" in data:
            # Translators: Message announced by NVDA when the live voice conversation starts.
            self.on_status("STATUS:" + _("Live conversation started. You can speak now."))
            lang = getattr(self, "response_lang", "English")
            trigger_prompt = (
                f"Please greet the user warmly, introduce yourself exactly as 'Vision Assistant Pro' (DO NOT translate this name, keep it in English), "
                f"and ask how you can help them today. Speak strictly in {lang}."
            )
            
            msg = {
                "clientContent": {
                    "turns": [
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": trigger_prompt
                                }
                            ]
                        }
                    ],
                    "turnComplete": True
                }
            }
            try:
                self.ws.send_text(json.dumps(msg))
            except Exception as e:
                log.error(f"Live: Failed to send dynamic welcome trigger: {e}")
            return
        if "error" in data:
            err = data.get("error", {})
            err_msg = err.get("message") if isinstance(err, dict) else str(err)
            log.error(f"Live: Server returned error: {err_msg}")
            self.on_status("ERROR:" + str(err_msg))
            return

        server_content = data.get("serverContent")
        if not server_content:
            return

        if server_content.get("interrupted"):
            self._stop_player()
            self._end_stream_line()

        if "inputTranscription" in server_content or "input_transcription" in server_content:
            self._interrupted = False
            in_tx = server_content.get("inputTranscription") or server_content.get("input_transcription") or {}
            if in_tx.get("text"):
                # Translators: Prefix for the user's transcribed speech line in the Live Assistant history.
                self._stream("user", _("You: "), in_tx["text"])

        out_tx = server_content.get("outputTranscription") or server_content.get("output_transcription")
        if out_tx and out_tx.get("text"):
            # Translators: Prefix for an AI message line in the Live Assistant history.
            self._stream("ai", _("AI: "), out_tx["text"])

        model_turn = server_content.get("modelTurn") or server_content.get("model_turn") or {}
        for part in model_turn.get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                if not self._interrupted:
                    try:
                        p = self._get_player()
                        if p:
                            p.feed(base64.b64decode(inline["data"]))
                    except Exception as e:
                        log.error(f"Live playback failed: {e}")
            text = part.get("text")
            if text:
                # Translators: Prefix for an AI message line in the Live Assistant history.
                self._stream("ai", _("AI: "), text)

        if server_content.get("turnComplete") or server_content.get("turn_complete"):
            self._interrupted = False
            self._end_stream_line()

    def _stream(self, speaker, prefix, text):
        if self._stream_speaker != speaker:
            if self._stream_speaker is not None and self.on_stream:
                self.on_stream("\n")
            if self.on_stream:
                self.on_stream(prefix)
            self._stream_speaker = speaker
        if self.on_stream:
            self.on_stream(text)

    def _end_stream_line(self):
        if self._stream_speaker is not None and self.on_stream:
            self.on_stream("\n")
        self._stream_speaker = None

    def stop(self):
        if not self._running and self.ws is None:
            return
        self._running = False
        if self.mic:
            try: self.mic.stop()
            except Exception: pass
            self.mic = None
        if self.ws:
            try: self.ws.close()
            except Exception: pass
            self.ws = None
        self._stop_player()
        if self.on_closed:
            try: self.on_closed()
            except Exception: pass


class LiveAssistantDialog(wx.Dialog):
    instance = None

    def __init__(self, parent, start_callback, end_callback):
        # Translators: Title of the Live Assistant conversation window.
        title_text = _("{name} - Live Assistant").format(name=ADDON_NAME)
        super().__init__(parent, title=title_text, size=(500, 500), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.start_callback = start_callback
        self.end_callback = end_callback
        self.is_active = True
        LiveAssistantDialog.instance = self

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Translators: Label for the conversation history area in the Live Assistant window.
        sizer.Add(wx.StaticText(panel, label=_("Conversation:")), 0, wx.ALL, 5)
        self.history = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        sizer.Add(self.history, 1, wx.EXPAND | wx.ALL, 5)
        
        hbox_voice = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Label for TTS Voice selection in the Live Assistant window.
        hbox_voice.Add(wx.StaticText(panel, label=_("&TTS Voice:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        
        self.voice_sel = wx.Choice(panel, choices=[f"{v[0]} - {v[1]}" for v in GEMINI_VOICES])
        curr_voice = config.conf["VisionAssistant"].get("tts_voice", "Puck")
        for i, v in enumerate(GEMINI_VOICES):
            if v[0] == curr_voice:
                self.voice_sel.SetSelection(i)
                break
        else:
            if self.voice_sel.GetCount() > 0:
                self.voice_sel.SetSelection(0)
        
        self.voice_sel.Bind(wx.EVT_CHOICE, self.on_voice_change)
        hbox_voice.Add(self.voice_sel, 1, wx.EXPAND)
        sizer.Add(hbox_voice, 0, wx.EXPAND | wx.ALL, 5)

        hbox_thinking = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Label for Thinking Depth selection in the Live Assistant window.
        hbox_thinking.Add(wx.StaticText(panel, label=_("Thinking &Depth:")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        
        self.thinking_choices = [
            # Translators: Thinking level option for no reasoning (lowest latency)
            (_("Minimal (Fastest)"), "minimal"),
            # Translators: Thinking level option for slight reasoning
            (_("Low (Agentic)"), "low"),
            # Translators: Thinking level option for standard reasoning (balanced)
            (_("Medium (Balanced)"), "medium"),
            # Translators: Thinking level option for deep reasoning
            (_("High (Deep)"), "high")
        ]
        self.thinking_sel = wx.Choice(panel, choices=[x[0] for x in self.thinking_choices])
        curr_thinking = config.conf["VisionAssistant"].get("live_thinking_level", "medium")
        for i, x in enumerate(self.thinking_choices):
            if x[1] == curr_thinking:
                self.thinking_sel.SetSelection(i)
                break
        else:
            self.thinking_sel.SetSelection(2)
            
        self.thinking_sel.Bind(wx.EVT_CHOICE, self.on_thinking_change)
        hbox_thinking.Add(self.thinking_sel, 1, wx.EXPAND)
        sizer.Add(hbox_thinking, 0, wx.EXPAND | wx.ALL, 5)
        
        # Translators: Button that ends the live voice conversation.
        self.toggle_btn = wx.Button(panel, label=_("&End"))
        self.toggle_btn.Bind(wx.EVT_BUTTON, self.on_toggle)
        sizer.Add(self.toggle_btn, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        
        panel.SetSizer(sizer)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(main_sizer)
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_char_hook)
        self.history.SetFocus()

    def on_voice_change(self, event):
        sel = self.voice_sel.GetSelection()
        if sel != wx.NOT_FOUND:
            config.conf["VisionAssistant"]["tts_voice"] = GEMINI_VOICES[sel][0]
            if self.is_active:
                # Translators: Message shown in conversation log when voice is changed
                self.append_line(_("--- Changing voice, reconnecting... ---"))
                self._restart_session()

    def on_thinking_change(self, event):
        sel = self.thinking_sel.GetSelection()
        if sel != wx.NOT_FOUND:
            config.conf["VisionAssistant"]["live_thinking_level"] = self.thinking_choices[sel][1]
            if self.is_active:
                # Translators: Message shown in conversation log when thinking depth is changed
                self.append_line(_("--- Changing thinking depth, reconnecting... ---"))
                self._restart_session()

    def _restart_session(self):
        if self.end_callback:
            self.end_callback()
        
        def restart():
            if self.start_callback:
                self.start_callback()
        
        wx.CallLater(1200, restart)

    def on_char_hook(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        else:
            event.Skip()

    def append_line(self, line):
        self.history.AppendText(line + "\n")

    def append_raw(self, text):
        self.history.AppendText(text)

    def set_active(self, active):
        self.is_active = active
        # Translators: Button label to end the live conversation / Button label to start it again.
        self.toggle_btn.SetLabel(_("&End") if active else _("&Start"))

    def on_toggle(self, event):
        if self.is_active:
            if self.end_callback:
                self.end_callback()
        else:
            if self.start_callback:
                self.start_callback()

    def on_close(self, event):
        if self.is_active and self.end_callback:
            self.end_callback()
        LiveAssistantDialog.instance = None
        self.Destroy()

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
            opener = get_proxy_opener(url)
            with opener.open(req, timeout=60) as response:
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
                            # Translators: Error message when an update is found but the addon file is missing from GitHub.
                            msg = _("Update found but no .nvda-addon file in release.")
                            show_error_dialog(msg)
                    elif not silent:
                        # Translators: Status message informing the user they are already on the latest version.
                        msg = _("You have the latest version.")
                        wx.CallAfter(ui.message, msg)
        except Exception as e:
            if not silent:
                # Translators: Error message shown when the add-on fails to check for updates. The {error} placeholder is replaced with specific error details.
                msg = _("Update check failed: {error}").format(error=e)
                show_error_dialog(msg)

    def _compare_versions(self, v1, v2):
        try:
            parts1 = [int(x) for x in v1.split('.')]
            parts2 = [int(x) for x in v2.split('.')]
            
            max_len = max(len(parts1), len(parts2))
            parts1.extend([0] * (max_len - len(parts1)))
            parts2.extend([0] * (max_len - len(parts2)))
            
            return (parts1 > parts2) - (parts1 < parts2)
        except Exception: return 0 if v1 == v2 else 1

    def _prompt_update(self, version, url, changes):
        gui.mainFrame.prePopup()
        try:
            dlg = UpdateDialog(gui.mainFrame, version, ADDON_NAME, changes)
            if dlg.ShowModal() == wx.ID_YES:
                threading.Thread(target=self._download_install_worker, args=(url,), daemon=True).start()
            dlg.Destroy()
        finally:
            gui.mainFrame.postPopup()

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
        response_text, _unused = result_tuple
        if response_text:
            if response_text.startswith("ERROR:"):
                wx.CallAfter(show_error_dialog, response_text[6:])
                if _vision_assistant_instance:
                    # Translators: Initial status when the add-on is doing nothing
                    wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))
                return

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
                # Translators: Message shown on successful save of a file.
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
                with open(path, "w", encoding="utf-8-sig") as f: f.write(full_html)
                # Translators: Message on successful save
                self.report_save(_("Saved."))
            except Exception as e:
                # Translators: Message in the error dialog when saving fails.
                msg = _("Save failed: {error}").format(error=e)
                show_error_dialog(msg)

class SettingsPanel(gui.settingsDialogs.SettingsPanel):
    title = ADDON_NAME
    def makeSettings(self, settingsSizer):
        self._all_models_backup = []
        self._temp_models = {}
        
        # --- Connection Group ---
        # Translators: Title of the settings group for connection and updates
        groupLabel = _("Connection")
        self.connectionBox = wx.StaticBox(self, label=groupLabel)
        connectionSizer = wx.StaticBoxSizer(self.connectionBox, wx.VERTICAL)
        cHelper = gui.guiHelper.BoxSizerHelper(self.connectionBox, sizer=connectionSizer)
        
        providers = [
            # Translators: Name of the Google Gemini AI provider
            (_("Google Gemini"), "gemini"),
            # Translators: Name of the OpenAI provider
            (_("OpenAI"), "openai"),
            # Translators: Name of the Mistral AI provider
            (_("Mistral AI"), "mistral"),
            # Translators: Name of the Groq AI provider
            (_("Groq"), "groq"),
            # Translators: Name of the MiniMax AI provider
            (_("MiniMax"), "minimax"),
            # Translators: Option for a user-defined custom AI provider
            (_("Custom"), "custom")
        ]
        # Translators: Label for AI Provider selection
        self.provider_sel = cHelper.addLabeledControl(_("Provider:"), wx.Choice, choices=[x[0] for x in providers])
        curr_p = config.conf["VisionAssistant"]["active_provider"]
        try:
            self.provider_sel.SetSelection(next(i for i, x in enumerate(providers) if x[1] == curr_p))
        except Exception: self.provider_sel.SetSelection(0)
        self.provider_sel.Bind(wx.EVT_CHOICE, self.onProviderChange)

        # Translators: Label for API Key input
        apiLabel = wx.StaticText(self.connectionBox, label=_("API Key (Separate multiple keys with comma or newline):"))
        cHelper.addItem(apiLabel)
        
        curr_key = config.conf["VisionAssistant"]["api_key" if curr_p == "gemini" else (f"{curr_p}_api_key" if curr_p != "custom" else "custom_api_key")]
        self.apiKeyCtrl_hidden = wx.TextCtrl(self.connectionBox, value=curr_key, style=wx.TE_PASSWORD)
        self.apiKeyCtrl_visible = wx.TextCtrl(self.connectionBox, value=curr_key, style=wx.TE_MULTILINE | wx.TE_DONTWRAP, size=(-1, 60))
        self.apiKeyCtrl_visible.Hide()
        cHelper.addItem(self.apiKeyCtrl_hidden)
        cHelper.addItem(self.apiKeyCtrl_visible)
        
        # Translators: Checkbox to toggle API Key visibility
        self.showApiCheck = wx.CheckBox(self.connectionBox, label=_("Show API Key"))
        self.showApiCheck.Bind(wx.EVT_CHECKBOX, self.onToggleApiVisibility)
        cHelper.addItem(self.showApiCheck)

        # Custom Fields Box
        # Translators: Static box title for custom AI provider settings
        self.customBox = wx.StaticBox(self.connectionBox, label=_("Custom Provider Settings"))
        self.customSizer = wx.StaticBoxSizer(self.customBox, wx.VERTICAL)

        # Translators: Button label to automatically configure local AI engines (Ollama, LM Studio, etc.)
        self.btn_setup_local_ai = wx.Button(self.customBox, label=_("Setup Local AI"))
        self.btn_setup_local_ai.Bind(wx.EVT_BUTTON, self.onSetupLocalAI)
        self.customSizer.Add(self.btn_setup_local_ai, 0, wx.ALL, 5)

        # Translators: Label for Custom API URL input
        self.customSizer.Add(wx.StaticText(self.customBox, label=_("API URL:")), 0, wx.ALL, 2)
        self.customUrl = wx.TextCtrl(self.customBox, value=config.conf["VisionAssistant"]["custom_api_url"])
        self.customSizer.Add(self.customUrl, 0, wx.EXPAND | wx.ALL, 2)
        self.customUrl.Bind(wx.EVT_TEXT, self.onCustomUrlChange)
                # Translators: Label for Custom API Type selection
        self.customSizer.Add(wx.StaticText(self.customBox, label=_("API Type:")), 0, wx.ALL, 2)
        # Translators: AI API compatibility types
        self.customType = wx.Choice(self.customBox, choices=[_("OpenAI Compatible"), _("Gemini Compatible")])
        self.customType.Bind(wx.EVT_CHOICE, self.onCustomTypeChange)
        self.customType.SetSelection(0 if config.conf["VisionAssistant"]["custom_api_type"] == "openai" else 1)
        self.customSizer.Add(self.customType, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom Model Name input
        self.lbl_customModelName = wx.StaticText(self.customBox, label=_("Model Name (Manual):"))
        self.customSizer.Add(self.lbl_customModelName, 0, wx.ALL, 2)
        self.customModelName = wx.TextCtrl(self.customBox, value=config.conf["VisionAssistant"]["custom_model_name"])
        self.customSizer.Add(self.customModelName, 0, wx.EXPAND | wx.ALL, 2)
                
        # Translators: Checkbox to indicate if custom provider supports file upload
        self.customUploadSupport = wx.CheckBox(self.customBox, label=_("Supports File Upload"))
        self.customUploadSupport.Value = config.conf["VisionAssistant"]["custom_upload_support"]
        self.customUploadSupport.Bind(wx.EVT_CHECKBOX, self.onCustomUploadSupportChange)
        self.customSizer.Add(self.customUploadSupport, 0, wx.ALL, 5)

        # Advanced Endpoints Section
        # Translators: Checkbox to toggle advanced endpoint URLs
        self.useAdvancedEndpoints = wx.CheckBox(self.customBox, label=_("Advanced Endpoint Configuration"))
        self.useAdvancedEndpoints.Value = config.conf["VisionAssistant"]["use_advanced_endpoints"]
        self.useAdvancedEndpoints.Bind(wx.EVT_CHECKBOX, self.onToggleAdvanced)
        self.customSizer.Add(self.useAdvancedEndpoints, 0, wx.ALL, 5)

        self.advEndpointBox = wx.Panel(self.customBox)
        advVBox = wx.BoxSizer(wx.VERTICAL)
        
        # Translators: Label for Custom Models List URL
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("Models List URL:")), 0, wx.ALL, 2)
        self.customModelsUrl = wx.TextCtrl(self.advEndpointBox, value=config.conf["VisionAssistant"]["custom_models_url"])
        advVBox.Add(self.customModelsUrl, 0, wx.EXPAND | wx.ALL, 2)
        
        # Translators: Label for Custom OCR URL
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("OCR Endpoint URL:")), 0, wx.ALL, 2)
        self.customOcrUrl = wx.TextCtrl(self.advEndpointBox, value=config.conf["VisionAssistant"]["custom_ocr_url"])
        advVBox.Add(self.customOcrUrl, 0, wx.EXPAND | wx.ALL, 2)
        
        # Translators: Label for Custom OCR Model
        self.lblCustomOcrModel = wx.StaticText(self.advEndpointBox, label=_("Custom OCR Model (Optional):"))
        advVBox.Add(self.lblCustomOcrModel, 0, wx.ALL, 2)
        self.customOcrModel = wx.TextCtrl(self.advEndpointBox, value=config.conf["VisionAssistant"]["custom_ocr_model"])
        advVBox.Add(self.customOcrModel, 0, wx.EXPAND | wx.ALL, 2)
        
        # Translators: Label for Custom STT URL
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("Speech-to-Text (STT) URL:")), 0, wx.ALL, 2)
        self.customSttUrl = wx.TextCtrl(self.advEndpointBox, value=config.conf["VisionAssistant"]["custom_stt_url"])
        advVBox.Add(self.customSttUrl, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom STT Model
        self.lblCustomSttModel = wx.StaticText(self.advEndpointBox, label=_("Custom STT Model (Optional):"))
        advVBox.Add(self.lblCustomSttModel, 0, wx.ALL, 2)
        self.customSttModel = wx.TextCtrl(self.advEndpointBox, value=config.conf["VisionAssistant"]["custom_stt_model"])
        advVBox.Add(self.customSttModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom TTS URL
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("Text-to-Speech (TTS) URL:")), 0, wx.ALL, 2)
        self.customTtsUrl = wx.TextCtrl(self.advEndpointBox, value=config.conf["VisionAssistant"]["custom_tts_url"])
        advVBox.Add(self.customTtsUrl, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom TTS Model
        self.lblCustomTtsModel = wx.StaticText(self.advEndpointBox, label=_("Custom TTS Model (Optional):"))
        advVBox.Add(self.lblCustomTtsModel, 0, wx.ALL, 2)
        self.customTtsModel = wx.TextCtrl(self.advEndpointBox, value=config.conf["VisionAssistant"]["custom_tts_model"])
        advVBox.Add(self.customTtsModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for a text field in the "Custom Provider Settings" section of settings where the user enters the AI Operator URL.
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("AI Operator URL:")), 0, wx.ALL, 2)
        self.customAssistantUrl = wx.TextCtrl(self.advEndpointBox, value=config.conf["VisionAssistant"].get("custom_operator_url", ""))
        advVBox.Add(self.customAssistantUrl, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for a text field in the "Custom Provider Settings" section of settings where the user manually enters the model name for AI Operator.
        self.lblCustomOperatorModel = wx.StaticText(self.advEndpointBox, label=_("Custom Operator Model (Optional):"))
        advVBox.Add(self.lblCustomOperatorModel, 0, wx.ALL, 2)
        self.customAssistantModel = wx.TextCtrl(self.advEndpointBox, value=config.conf["VisionAssistant"]["custom_operator_model"])
        advVBox.Add(self.customAssistantModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for Custom TTS Voice Name
        advVBox.Add(wx.StaticText(self.advEndpointBox, label=_("Custom TTS Voice Name (Optional):")), 0, wx.ALL, 2)
        self.customTtsVoice = wx.TextCtrl(self.advEndpointBox, value=config.conf["VisionAssistant"]["custom_tts_voice"])
        advVBox.Add(self.customTtsVoice, 0, wx.EXPAND | wx.ALL, 2)
        
        self.advEndpointBox.SetSizer(advVBox)
        self.customSizer.Add(self.advEndpointBox, 0, wx.EXPAND)
        self.advEndpointBox.Show(self.useAdvancedEndpoints.Value)
        cHelper.addItem(self.customSizer)

        # Standard Fetch & Model Logic
        # Translators: Button to fetch available models from the selected provider
        self.btn_fetch = wx.Button(self.connectionBox, label=_("Fetch Models"))
        self.btn_fetch.Bind(wx.EVT_BUTTON, self.onFetchModels)
        cHelper.addItem(self.btn_fetch)

        # Translators: Label for AI Model selection choice box
        self.modelLabel = wx.StaticText(self.connectionBox, label=_("AI Model:"))
        cHelper.addItem(self.modelLabel)
# Translators: Accessible name for the AI model selection combo box.
        self.model = wx.ComboBox(self.connectionBox, style=wx.TE_PROCESS_ENTER, name=_("AI Model:"))
        self.model.Bind(wx.EVT_TEXT, self.onModelFilter)
        cHelper.addItem(self.model)

        # Advanced Model Routing Box
        # Translators: Checkbox to toggle advanced model routing
        self.advRoutingCheck = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Advanced Model Routing (Task-specific)")))
        self.advRoutingCheck.Value = config.conf["VisionAssistant"].get("advanced_model_routing", False)
        self.advRoutingCheck.Bind(wx.EVT_CHECKBOX, self.onToggleAdvRouting)

        self.advRoutingBox = wx.Panel(self.connectionBox)
        advRSizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: Label for OCR model selection
        self.lbl_advOcr = wx.StaticText(self.advRoutingBox, label=_("OCR / Vision Model:"))
        advRSizer.Add(self.lbl_advOcr, 0, wx.ALL, 2)
        self.advOcrModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advOcrModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advOcrModel, 0, wx.EXPAND | wx.ALL, 2)
        
        # Translators: Label for STT model selection
        self.lbl_advStt = wx.StaticText(self.advRoutingBox, label=_("Speech-to-Text (STT) Model:"))
        advRSizer.Add(self.lbl_advStt, 0, wx.ALL, 2)
        self.advSttModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advSttModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advSttModel, 0, wx.EXPAND | wx.ALL, 2)
        
        # Translators: Label for TTS model selection (Assigning to self to toggle visibility)
        self.lbl_advTts = wx.StaticText(self.advRoutingBox, label=_("Text-to-Speech (TTS) Model:"))
        advRSizer.Add(self.lbl_advTts, 0, wx.ALL, 2)
        self.advTtsModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advTtsModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advTtsModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for a dropdown menu in the "Advanced Model Routing" section of settings to choose a specific model for AI Operator tasks.
        self.lbl_advOperator = wx.StaticText(self.advRoutingBox, label=_("AI Operator Model:"))
        advRSizer.Add(self.lbl_advOperator, 0, wx.ALL, 2)
        self.advOperatorModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advOperatorModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advOperatorModel, 0, wx.EXPAND | wx.ALL, 2)
        # Translators: Label for the Video Analysis model selection in the Advanced Model Routing section.
        self.lbl_advVideo = wx.StaticText(self.advRoutingBox, label=_("Video Analysis Model (Gemini only):"))
        advRSizer.Add(self.lbl_advVideo, 0, wx.ALL, 2)
        self.advVideoModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advVideoModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advVideoModel, 0, wx.EXPAND | wx.ALL, 2)

        # Translators: Label for the Live Assistant model selection in the Advanced Model Routing section (Gemini only).
        self.lbl_advLive = wx.StaticText(self.advRoutingBox, label=_("Live Assistant Model (Gemini only):"))
        advRSizer.Add(self.lbl_advLive, 0, wx.ALL, 2)
        self.advLiveModel = wx.ComboBox(self.advRoutingBox, style=wx.TE_PROCESS_ENTER)
        self.advLiveModel.Bind(wx.EVT_TEXT, self.onModelFilter)
        advRSizer.Add(self.advLiveModel, 0, wx.EXPAND | wx.ALL, 2)

        self.advRoutingBox.SetSizer(advRSizer)
        cHelper.addItem(self.advRoutingBox)

        # Translators: Label for Proxy URL input
        self.proxyUrl = cHelper.addLabeledControl(_("Proxy URL:"), wx.TextCtrl)
        self.proxyUrl.Value = config.conf["VisionAssistant"]["proxy_url"]

        # Translators: Checkbox to enable/disable automatic update checks on startup
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
        # Translators: Checkbox to start the Live Assistant without its conversation window (open it later with the Show Last Result key).
        self.liveDirectOutput = cHelper.addItem(wx.CheckBox(self.connectionBox, label=_("Live Assistant: Direct Output (No Window)")))
        self.liveDirectOutput.Value = config.conf["VisionAssistant"]["live_direct_output"]
        settingsSizer.Add(connectionSizer, 0, wx.EXPAND | wx.ALL, 5)
        
        # --- AI Behavior Group ---
        # Translators: Title of the settings group for AI behavior
        groupLabel = _("AI Behavior")
        aiBox = wx.StaticBox(self, label=groupLabel)
        aiSizer = wx.StaticBoxSizer(aiBox, wx.VERTICAL)
        aiHelper = gui.guiHelper.BoxSizerHelper(aiBox, sizer=aiSizer)
        # Translators: Label for AI Temperature setting
        tempLabelText = _("Creativity (Temperature, does not affect OCR/Translation):")
        temp_choices = [f"{x/10:.1f}" for x in range(0, 21)]
        self.aiTemp = aiHelper.addLabeledControl(tempLabelText, wx.Choice, choices=temp_choices)
        current_temp = str(config.conf["VisionAssistant"].get("ai_temperature", 0.7))
        idx = self.aiTemp.FindString(current_temp)
        if idx != wx.NOT_FOUND: self.aiTemp.SetSelection(idx)
        else: self.aiTemp.SetSelection(7)
        settingsSizer.Add(aiSizer, 0, wx.EXPAND | wx.ALL, 5)

        # --- Translation Languages Group ---
        # Translators: Title of the settings group for translation languages configuration
        groupLabel = _("Translation Languages")
        langBox = wx.StaticBox(self, label=groupLabel)
        langSizer = wx.StaticBoxSizer(langBox, wx.VERTICAL)
        lHelper = gui.guiHelper.BoxSizerHelper(langBox, sizer=langSizer)
        # Translators: Label for Source Language selection
        self.sourceLang = lHelper.addLabeledControl(_("Source:"), wx.Choice, choices=SOURCE_NAMES)
        curr_s_code = config.conf["VisionAssistant"]["source_language"]
        s_idx = next((i for i, x in enumerate(SOURCE_LIST) if x[1] == curr_s_code), 0)
        self.sourceLang.SetSelection(s_idx)
        # Translators: Label for Target Language selection
        self.targetLang = lHelper.addLabeledControl(_("Target:"), wx.Choice, choices=TARGET_NAMES)
        curr_t_code = config.conf["VisionAssistant"]["target_language"]
        t_idx = next((i for i, x in enumerate(TARGET_LIST) if x[1] == curr_t_code), 0)
        self.targetLang.SetSelection(t_idx)
        # Translators: Label for AI Response Language selection
        self.aiResponseLang = lHelper.addLabeledControl(_("AI Response:"), wx.Choice, choices=TARGET_NAMES)
        curr_ai_code = config.conf["VisionAssistant"]["ai_response_language"]
        ai_idx = next((i for i, x in enumerate(TARGET_LIST) if x[1] == curr_ai_code), 0)
        self.aiResponseLang.SetSelection(ai_idx)
        # Translators: Checkbox for Smart Swap feature
        self.smartSwap = lHelper.addItem(wx.CheckBox(langBox, label=_("Smart Swap")))
        self.smartSwap.Value = config.conf["VisionAssistant"]["smart_swap"]
        settingsSizer.Add(langSizer, 0, wx.EXPAND | wx.ALL, 5)

        # --- Document Reader Settings ---
        # Translators: Title of settings group for Document Reader features
        groupLabel = _("Document Reader")
        self.docBox = wx.StaticBox(self, label=groupLabel)
        docSizer = wx.StaticBoxSizer(self.docBox, wx.VERTICAL)
        dHelper = gui.guiHelper.BoxSizerHelper(self.docBox, sizer=docSizer)
        # Translators: Label for OCR Engine selection
        self.ocr_sel = dHelper.addLabeledControl(_("OCR Engine:"), wx.Choice, choices=[x[0] for x in OCR_ENGINES])
        curr_ocr = config.conf["VisionAssistant"]["ocr_engine"]
        try:
            o_idx = next(i for i, v in enumerate(OCR_ENGINES) if v[1] == curr_ocr)
            self.ocr_sel.SetSelection(o_idx)
        except Exception: self.ocr_sel.SetSelection(0)

        # Translators: Label for the OCR batch size setting. Set to 0 to process all pages in a single request.
        self.lbl_batch = wx.StaticText(self.docBox, label=_("OCR Batch Size (Pages per request, 0 to disable):"))
        dHelper.addItem(self.lbl_batch)
        self.batch_size = wx.SpinCtrl(self.docBox, min=0, max=100, initial=config.conf["VisionAssistant"]["ocr_batch_size"])
        dHelper.addItem(self.batch_size)

        # Translators: Label for TTS Voice selection (Assigning to self to toggle visibility)
        self.lbl_voice = wx.StaticText(self.docBox, label=_("TTS Voice:"))
        dHelper.addItem(self.lbl_voice)
        self.voice_sel = wx.Choice(self.docBox, choices=[])
        self.voice_sel.Bind(wx.EVT_CHOICE, self.onVoiceSelectionChanged)
        dHelper.addItem(self.voice_sel)
        settingsSizer.Add(docSizer, 0, wx.EXPAND | wx.ALL, 5)

        # --- Video Settings Group ---
        self.vidPanel = wx.Panel(self)
        # Translators: Title of settings group for Video features
        groupLabel = _("Video")
        vidBox = wx.StaticBox(self.vidPanel, label=groupLabel)
        vidSizer = wx.StaticBoxSizer(vidBox, wx.VERTICAL)
        vHelper = gui.guiHelper.BoxSizerHelper(vidBox, sizer=vidSizer)
        
        # Translators: Label for Video Chunk Size setting. Explains the trade-off between chunk size, API requests, and description quality.
        self.lbl_vid_chunk = wx.StaticText(self.vidPanel, label=_("Video Chunk Size for Audio Description (Minutes, 0 to disable):\nTip: Higher values use fewer API requests but rely on luck to succeed. Lower values guarantee highly detailed and precise descriptions."))
        vHelper.addItem(self.lbl_vid_chunk)
        self.vid_chunk_size = wx.SpinCtrl(self.vidPanel, min=0, max=300, initial=config.conf["VisionAssistant"]["video_srt_chunk_minutes"])
        vHelper.addItem(self.vid_chunk_size)

        # Translators: Checkbox label to add character list as the first subtitle in video SRT output.
        self.vid_chars_as_sub = wx.CheckBox(self.vidPanel, label=_("Add character list as first subtitle"))
        self.vid_chars_as_sub.SetValue(config.conf["VisionAssistant"].get("video_chars_as_subtitle", True))
        vHelper.addItem(self.vid_chars_as_sub)

        # Translators: Checkbox label to add an AI warning disclaimer at the beginning of the video SRT output.
        self.vid_add_disclaimer = wx.CheckBox(self.vidPanel, label=_("Add AI disclaimer at the beginning"))
        self.vid_add_disclaimer.SetValue(config.conf["VisionAssistant"].get("video_add_disclaimer", True))
        vHelper.addItem(self.vid_add_disclaimer)
        self.vidPanel.SetSizer(vidSizer)
        settingsSizer.Add(self.vidPanel, 0, wx.EXPAND | wx.ALL, 5)

        # Translators: Title of the settings group for Captchas
        # --- CAPTCHA Group ---
        groupLabel = _("CAPTCHA")
        capBox = wx.StaticBox(self, label=groupLabel)
        capSizer = wx.StaticBoxSizer(capBox, wx.VERTICAL)
        capHelper = gui.guiHelper.BoxSizerHelper(capBox, sizer=capSizer)
        # Translators: Label for CAPTCHA capture method selection.
        self.captchaMode = capHelper.addLabeledControl(_("Capture Method:"), wx.Choice, choices=[
            # Translators: A choice for capture method. Captures only the specific object under the cursor.
            _("Navigator Object"),
            # Translators: A choice for capture method. Captures the entire visible screen area.
            _("Full Screen")
        ])
        
        self.captchaMode.SetSelection(0 if config.conf["VisionAssistant"]["captcha_mode"] == 'navigator' else 1)
        settingsSizer.Add(capSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.defaultPromptItems = get_configured_default_prompts()
        self.customPromptItems = load_configured_custom_prompts()

        # --- Prompts Group ---
        # Translators: Title of the settings group for prompt management.
        groupLabel = _("Prompts")
        promptsBox = wx.StaticBox(self, label=groupLabel)
        promptsSizer = wx.StaticBoxSizer(promptsBox, wx.VERTICAL)
        pHelper = gui.guiHelper.BoxSizerHelper(promptsBox, sizer=promptsSizer)
        # Translators: Description for the prompt manager button.
        pHelper.addItem(wx.StaticText(promptsBox, label=_("Manage default and custom prompts.")))
        # Translators: Button label to open prompt manager dialog.
        self.managePromptsBtn = wx.Button(promptsBox, label=_("Manage Prompts..."))
        self.managePromptsBtn.Bind(wx.EVT_BUTTON, self.onManagePrompts)
        pHelper.addItem(self.managePromptsBtn)
        self.promptsSummary = wx.StaticText(promptsBox)
        pHelper.addItem(self.promptsSummary)
        self._refreshPromptSummary()
        settingsSizer.Add(promptsSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.refreshModelList(curr_p)
        self.updateVoiceList(curr_p)
        self.updateCustomFieldsVisibility(curr_p)


    def updateVoiceList(self, p_name):
        self.voice_sel.Clear()
        if p_name == "openai" or p_name == "custom":
            voices = OPENAI_VOICES
        else:
            voices = AIHandler.get_voices(p_name) or GEMINI_VOICES
        for v in voices:
            self.voice_sel.Append(f"{v[0]} - {v[1]}", v[0])
        if p_name == "minimax":
            threading.Thread(target=self._refresh_minimax_voices, daemon=True).start()
        else:
            curr_voice = config.conf["VisionAssistant"].get("tts_voice", "Puck")
            self._select_voice_in_list(curr_voice)

    def _refresh_minimax_voices(self):
        try:
            config.conf["VisionAssistant"]["minimax_voices_cache"] = ""
            config.conf["VisionAssistant"]["minimax_voices_cache_time"] = 0
            voices = AIHandler.get_voices("minimax")
            if voices and hasattr(self, 'voice_sel'):
                wx.CallAfter(self._populate_voice_sel, voices)
        except Exception as e:
            log.warning(f"Background MiniMax voice refresh failed: {e}")

    def _populate_voice_sel(self, voices):
        try:
            self.voice_sel.Clear()
            for v in voices:
                self.voice_sel.Append(f"{v[0]} - {v[1]}", v[0])
            curr_voice = config.conf["VisionAssistant"].get("tts_voice", "English_expressive_narrator")
            self._select_voice_in_list(curr_voice)
        except Exception as e:
            log.warning(f"Failed to populate voice_sel: {e}")

    def _select_voice_in_list(self, voice_id):
        try:
            for i in range(self.voice_sel.GetCount()):
                if self.voice_sel.GetClientData(i) == voice_id:
                    self.voice_sel.SetSelection(i)
                    return
            if self.voice_sel.GetCount() > 0:
                self.voice_sel.SetSelection(0)
        except Exception:
            pass

    def _refreshPromptSummary(self):
        # Translators: Summary text for prompt counts in settings.
        summary = _("Default prompts: {defaultCount}, Custom prompts: {customCount}").format(
            defaultCount=len(self.defaultPromptItems),
            customCount=len(self.customPromptItems),
        )
        self.promptsSummary.SetLabel(summary)

    def onManagePrompts(self, event):
        top = wx.GetTopLevelParent(self)
        gui.mainFrame.prePopup()
        try:
            dlg = PromptManagerDialog(
                self,
                self.defaultPromptItems,
                self.customPromptItems,
                PROMPT_VARIABLES_GUIDE,
            )
            if dlg.ShowModal() == wx.ID_OK:
                self.defaultPromptItems = dlg.get_default_items()
                self.customPromptItems = dlg.get_custom_items()
                self._refreshPromptSummary()
            dlg.Destroy()
        finally:
            gui.mainFrame.postPopup()
            if top:
                top.Enable(True)
                top.SetFocus()

    def _live_supported_for(self, provider):
        if provider == "gemini":
            return True
        if provider == "custom":
            if hasattr(self, "customType") and self.customType.GetSelection() != wx.NOT_FOUND:
                return self.customType.GetSelection() == 1
            return config.conf["VisionAssistant"].get("custom_api_type", "openai") == "gemini"
        return False

    def updateCustomFieldsVisibility(self, provider):
        is_custom = (provider == "custom")
        self.customBox.Show(is_custom)
        self.advRoutingCheck.Show(True)
        
        tts_supported = AIHandler.is_tts_supported(provider)
        routing_enabled = self.advRoutingCheck.Value
        self.advRoutingBox.Show(routing_enabled)
        
        live_supported = self._live_supported_for(provider)
        self.liveDirectOutput.Show(live_supported)
        
        if routing_enabled:
            self.advOcrModel.Show(True)
            self.advSttModel.Show(True)
            self.advTtsModel.Show(tts_supported)
            self.lbl_advTts.Show(tts_supported)
            self.advOperatorModel.Show(True)
            self.lbl_advOperator.Show(True)
            self.advVideoModel.Show(live_supported)
            self.lbl_advVideo.Show(live_supported)
            self.advLiveModel.Show(live_supported)
            self.lbl_advLive.Show(live_supported)

        self.voice_sel.Show(tts_supported)
        self.lbl_voice.Show(tts_supported)
        self.btn_fetch.Show(True)
        
        has_fetched_models = self.model.GetCount() > 0
        if is_custom:
            self.modelLabel.Show(has_fetched_models)
            self.model.Show(has_fetched_models)
            
            if hasattr(self, 'lbl_customModelName'):
                self.lbl_customModelName.Show(not has_fetched_models)
            self.customModelName.Show(not has_fetched_models)
            
            self.advEndpointBox.Show(self.useAdvancedEndpoints.Value)
            
            show_manual_fields = self.useAdvancedEndpoints.Value and not has_fetched_models
            
            if hasattr(self, 'lblCustomOcrModel'):
                self.lblCustomOcrModel.Show(show_manual_fields)
            self.customOcrModel.Show(show_manual_fields)
            
            if hasattr(self, 'lblCustomSttModel'):
                self.lblCustomSttModel.Show(show_manual_fields)
            self.customSttModel.Show(show_manual_fields)
            
            if hasattr(self, 'lblCustomTtsModel'):
                self.lblCustomTtsModel.Show(show_manual_fields)
            self.customTtsModel.Show(show_manual_fields)
            
            if hasattr(self, 'lblCustomOperatorModel'):
                self.lblCustomOperatorModel.Show(show_manual_fields)
            self.customAssistantModel.Show(show_manual_fields)
            
            self.customTtsVoice.Show(self.useAdvancedEndpoints.Value)
        else:
            self.modelLabel.Show(True)
            self.model.Show(True)
            if hasattr(self, 'lbl_customModelName'):
                self.lbl_customModelName.Show(False)
            self.customModelName.Hide()

        if hasattr(self, 'advEndpointBox'):
            self.advEndpointBox.Layout()
        is_gemini_api = False
        if provider == "gemini":
            is_gemini_api = True
        elif provider == "custom":
            custom_type_idx = self.customType.GetSelection()
            if custom_type_idx != wx.NOT_FOUND:
                is_gemini_api = (custom_type_idx == 1)
            else:
                is_gemini_api = (config.conf["VisionAssistant"].get("custom_api_type") == "gemini")
                
        if hasattr(self, 'vidPanel'):
            self.vidPanel.Show(is_gemini_api)
        self.Layout()
        p = self.connectionBox.GetParent()
        if p: p.Layout()
        show_batch_size = False
        if provider == "gemini" or provider == "mistral":
            show_batch_size = True
        elif provider == "custom":
            custom_type_idx = self.customType.GetSelection()
            if custom_type_idx != wx.NOT_FOUND:
                is_custom_gemini = (custom_type_idx == 1)
            else:
                is_custom_gemini = (config.conf["VisionAssistant"].get("custom_api_type") == "gemini")
            
            is_upload_supported = self.customUploadSupport.Value
            if is_custom_gemini and is_upload_supported:
                show_batch_size = True
                
        self.lbl_batch.Show(show_batch_size)
        self.batch_size.Show(show_batch_size)

    def onCustomUploadSupportChange(self, event):
        self.updateCustomFieldsVisibility("custom")

    def onToggleAdvRouting(self, event):
        self.advRoutingBox.Show(self.advRoutingCheck.Value)
        p = self.connectionBox.GetParent()
        if p: p.Layout()

    def onProviderChange(self, event):
        p_idx = self.provider_sel.GetSelection()
        p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
        
        key_name = "api_key" if p_name == "gemini" else (f"{p_name}_api_key" if p_name != "custom" else "custom_api_key")
        val = config.conf["VisionAssistant"].get(key_name, "")
        
        self.Freeze()
        try:
            self.apiKeyCtrl_hidden.SetValue(val)
            self.apiKeyCtrl_visible.SetValue(val)
            
            self.refreshModelList(p_name)
            self.updateVoiceList(p_name)
            self.updateCustomFieldsVisibility(p_name)
        finally:
            self.Thaw()
            p = self.connectionBox.GetParent()
            if p: 
                p.Layout()

    def onCustomTypeChange(self, event):
        self.updateCustomFieldsVisibility("custom")

    def onSetupLocalAI(self, event):
        # Translators: Title of the local AI setup dialog
        title = _("Setup Local AI")
        # Translators: Prompt message to select local AI engine
        msg = _("Select the local AI engine you are running:")
        choices = [
            "Ollama (http://127.0.0.1:11434)",
            "LM Studio (http://127.0.0.1:1234)",
            "Jan.ai (http://127.0.0.1:1337)",
            "KoboldCPP (http://127.0.0.1:5001)"
        ]
        
        gui.mainFrame.prePopup()
        try:
            with wx.SingleChoiceDialog(self, msg, title, choices) as dlg:
                if dlg.ShowModal() != wx.ID_OK:
                    return
                idx = dlg.GetSelection()
        finally:
            gui.mainFrame.postPopup()
            
        ports = ["11434", "1234", "1337", "5001"]
        url = f"http://127.0.0.1:{ports[idx]}"
        
        # Translators: Progress message shown when testing connection to local AI
        ui.message(_("Connecting to Local AI..."))
        
        def worker():
            try:
                endpoint = f"{url}/api/tags" if idx == 0 else f"{url}/v1/models"
                
                opener = get_proxy_opener(endpoint)
                req = request.Request(endpoint, method="GET")
                with opener.open(req, timeout=15) as r:
                    res_body = r.read().decode('utf-8')
                    data = json.loads(res_body)
                    
                models_info = []
                if idx == 0:
                    if "models" in data and isinstance(data["models"], list):
                        for m in data["models"]:
                            name = m.get("name")
                            if name:
                                models_info.append((name, name))
                else:
                    if "data" in data and isinstance(data["data"], list):
                        for m in data["data"]:
                            m_id = m.get("id")
                            if m_id:
                                models_info.append((m_id, m_id))
                                
                wx.CallAfter(self._onSetupLocalAISuccess, url, models_info)
            except Exception:
                # Translators: Error message when connection to local AI fails
                err_msg = _("Could not connect to the selected local AI. Make sure it is running on {url}").format(url=url)
                wx.CallAfter(self._onSetupLocalAIFail, err_msg)
                
        threading.Thread(target=worker, daemon=True).start()

    def _onSetupLocalAISuccess(self, url, models_info):
        self.customUrl.SetValue(url)
        self.customType.SetSelection(0)
        self.customUploadSupport.SetValue(False)
        
        self._on_fetch_models_complete("custom", models_info)
        
        # Translators: Announcement message when local AI setup succeeds
        ui.message(_("Local AI configured successfully!"))

    def _onSetupLocalAIFail(self, err_msg):
        # Translators: Title of an error dialog box
        wx.MessageBox(err_msg, _("Error"), wx.OK | wx.ICON_ERROR)

    def onFetchModels(self, event):
        p_idx = self.provider_sel.GetSelection()
        p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
        
        val = self.apiKeyCtrl_visible.Value if self.showApiCheck.IsChecked() else self.apiKeyCtrl_hidden.Value
        k_key = "api_key" if p_name == "gemini" else (f"{p_name}_api_key" if p_name != "custom" else "custom_api_key")
        config.conf["VisionAssistant"][k_key] = val.strip()
        config.conf["VisionAssistant"]["active_provider"] = p_name

        if p_name == "custom":
            config.conf["VisionAssistant"]["custom_api_url"] = self.customUrl.Value.strip()
            config.conf["VisionAssistant"]["custom_api_type"] = "openai" if self.customType.GetSelection() == 0 else "gemini"
            config.conf["VisionAssistant"]["use_advanced_endpoints"] = self.useAdvancedEndpoints.Value
            config.conf["VisionAssistant"]["custom_models_url"] = self.customModelsUrl.Value.strip()

        self.btn_fetch.Disable()
        # Translators: Progress message shown while fetching AI models from the server
        ui.message(_("Fetching models..."))
        threading.Thread(target=self._fetch_models_thread, args=(p_name,), daemon=True).start()

    def _fetch_models_thread(self, p_name):
        models_info = AIHandler.get_models(task="all")
        wx.CallAfter(self._on_fetch_models_complete, p_name, models_info)

    def _on_fetch_models_complete(self, p_name, models_info):
        self.btn_fetch.Enable()
        if models_info:
            self.model.Freeze()
            self.model.Clear()
            self.advOcrModel.Clear()
            self.advSttModel.Clear()
            self.advTtsModel.Clear()
            self.advOperatorModel.Clear()
            self.advVideoModel.Clear()
            self.advLiveModel.Clear()

            # Translators: Option to follow the main model selected in the primary dropdown
            default_main_label = _("Default (Main Model)")
            # Translators: Option for the system to automatically choose the best model for this specific task
            auto_task_label = _("Auto (Optimized)")

            self.advOcrModel.Append(default_main_label, "")
            self.advSttModel.Append(default_main_label, "")
            self.advOperatorModel.Append(default_main_label, "")
            self.advVideoModel.Append(default_main_label, "")
            self.advLiveModel.Append(auto_task_label, "")
            self.advTtsModel.Append(auto_task_label, "")

            self._current_model_ids = []
            storage_parts = []
            main_models = AIHandler.filter_models(p_name, models_info, task="main")
            for m_id, m_name in main_models:
                self.model.Append(m_name, m_id)
                self._current_model_ids.append(m_id)
            for m_id, m_name in models_info:
                self.advOcrModel.Append(m_name, m_id)
                self.advSttModel.Append(m_name, m_id)
                self.advTtsModel.Append(m_name, m_id)
                self.advOperatorModel.Append(m_name, m_id)
                self.advVideoModel.Append(m_name, m_id)
                if "live" in m_id.lower():
                    self.advLiveModel.Append(m_name, m_id)
                storage_parts.append(f"{m_id}|{m_name}")
            
            config.conf["VisionAssistant"][f"{p_name}_models_list"] = ",".join(storage_parts)
            
            if self.model.GetCount() > 0:
                self.model.SetSelection(0)
                self.model.ChangeValue(self.model.GetString(0))
            else:
                self.model.SetValue("")
            
            self.model.Thaw()
            
            self.advOcrModel.SetSelection(0)
            self.advSttModel.SetSelection(0)
            self.advTtsModel.SetSelection(0)
            self.advOperatorModel.SetSelection(0)
            self.advVideoModel.SetSelection(0)
            self.advLiveModel.SetSelection(0)
            
            self._all_models_backup = [(self.model.GetString(i), self.model.GetClientData(i)) for i in range(self.model.GetCount())]
            
            self.updateVoiceList(p_name)
            
            self.updateCustomFieldsVisibility(p_name)
            # Translators: Status message when the AI models list is successfully refreshed.
            ui.message(_("Models updated"))
        else:
            # Translators: Error message shown when the add-on cannot retrieve the list of models from the server.
            ui.message(_("Failed to fetch models"))

    def refreshModelList(self, p_name):
        self.model.Clear()
        self.advOcrModel.Clear()
        self.advSttModel.Clear()
        self.advTtsModel.Clear()
        self.advOperatorModel.Clear()
        self.advVideoModel.Clear()
        self.advLiveModel.Clear()

        # Translators: Option to follow the main model selected in the primary dropdown.
        default_main_label = _("Default (Main Model)")
        # Translators: Option for the system to automatically choose the best model for this task.
        auto_task_label = _("Auto (Optimized)")

        self.advOcrModel.Append(default_main_label, "")
        self.advSttModel.Append(default_main_label, "")
        self.advOperatorModel.Append(default_main_label, "")
        self.advVideoModel.Append(default_main_label, "")
        self.advLiveModel.Append(auto_task_label, "")
        self.advTtsModel.Append(auto_task_label, "")

        self._current_model_ids = []
        saved_models_raw = config.conf["VisionAssistant"].get(f"{p_name}_models_list", "")
        all_models = []
        if saved_models_raw:
            items = saved_models_raw.split(",")
            for item in items:
                if "|" in item:
                    m_id, m_name = item.split("|", 1)
                    all_models.append((m_id, m_name))
        elif p_name == "gemini":
            for m_name, m_id in MODELS: all_models.append((m_id, m_name))

        main_models = AIHandler.filter_models(p_name, all_models, task="main")
        for m_id, m_name in main_models:
            self.model.Append(m_name, m_id)
            self._current_model_ids.append(m_id)
        for m_id, m_name in all_models:
            self.advOcrModel.Append(m_name, m_id)
            self.advSttModel.Append(m_name, m_id)
            self.advTtsModel.Append(m_name, m_id)
            self.advOperatorModel.Append(m_name, m_id)
            self.advVideoModel.Append(m_name, m_id)
            if "live" in m_id.lower():
                self.advLiveModel.Append(m_name, m_id)
            if m_id not in self._current_model_ids: self._current_model_ids.append(m_id)
        
        m_key = "model_name" if p_name == "gemini" else f"{p_name}_model_name"
        curr_model = self._temp_models.get(p_name, config.conf["VisionAssistant"].get(m_key, ""))
        if p_name == "custom" and not curr_model:
            curr_model = config.conf["VisionAssistant"].get("custom_model_name", "")

        for i in range(self.model.GetCount()):
            if self.model.GetClientData(i) == curr_model:
                self.model.SetSelection(i)
                self.model.ChangeValue(self.model.GetString(i))
                break
        else:
            if self.model.GetCount() > 0:
                self.model.SetSelection(0)
                self.model.ChangeValue(self.model.GetString(0))
            else:
                self.model.ChangeValue("")
            
        routing_map = [
            (self.advOcrModel, f"{p_name}_ocr_model"),
            (self.advSttModel, f"{p_name}_stt_model"),
            (self.advTtsModel, f"{p_name}_tts_model"),
            (self.advOperatorModel, f"{p_name}_operator_model"),
        ]
        if self._live_supported_for(p_name):
            routing_map.append((self.advVideoModel, f"{p_name}_video_model"))
            routing_map.append((self.advLiveModel, f"{p_name}_live_model"))
        for attr, conf_key in routing_map:
            saved_id = config.conf["VisionAssistant"].get(conf_key, "")
            for i in range(attr.GetCount()):
                if attr.GetClientData(i) == saved_id:
                    attr.SetSelection(i)
                    break
            else: attr.SetSelection(0)
        self._all_models_backup = [(self.model.GetString(i), self.model.GetClientData(i)) for i in range(self.model.GetCount())]
        self.updateCustomFieldsVisibility(p_name)


    def onToggleAdvanced(self, event):
        p_idx = self.provider_sel.GetSelection()
        if p_idx != wx.NOT_FOUND:
            p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
            self.updateCustomFieldsVisibility(p_name)

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

    def onModelPickerChange(self, event):
        cb = event.GetEventObject()
        sel = cb.GetSelection()
        if sel != wx.NOT_FOUND:
            model_id = cb.GetClientData(sel)
            if model_id:
                p_idx = self.provider_sel.GetSelection()
                p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
                self._temp_models[p_name] = model_id
                if p_name == "custom":
                    self.customModelName.SetValue(model_id)

    def onVoiceSelectionChanged(self, event):
        sel = self.voice_sel.GetSelection()
        if sel != wx.NOT_FOUND:
            voice_id = self.voice_sel.GetClientData(sel)
            p_idx = self.provider_sel.GetSelection()
            if p_idx != wx.NOT_FOUND:
                p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
                if p_name == "custom":
                    self.customTtsVoice.SetValue(voice_id)

    def onCustomUrlChange(self, event):
        self.model.Clear()
        self._all_models_backup = []
        p_idx = self.provider_sel.GetSelection()
        if p_idx != wx.NOT_FOUND:
            p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
            if p_name == "custom":
                config.conf["VisionAssistant"]["custom_models_list"] = ""
                self.updateCustomFieldsVisibility("custom")
        event.Skip()

    def onSave(self):
        try:
            p_idx = self.provider_sel.GetSelection()
            p_name = ["gemini", "openai", "mistral", "groq", "minimax", "custom"][p_idx]
            config.conf["VisionAssistant"]["active_provider"] = p_name
            
            val = self.apiKeyCtrl_visible.Value if self.showApiCheck.IsChecked() else self.apiKeyCtrl_hidden.Value
            k_key = "api_key" if p_name == "gemini" else (f"{p_name}_api_key" if p_name != "custom" else "custom_api_key")
            config.conf["VisionAssistant"][k_key] = val.strip()
            
            m_key = "model_name" if p_name == "gemini" else f"{p_name}_model_name"
            has_fetched_models = self.model.GetCount() > 0
            if p_name == "custom":
                model_val = ""
                if has_fetched_models and self.model.GetSelection() != wx.NOT_FOUND:
                    model_val = self.model.GetClientData(self.model.GetSelection())
                if not model_val:
                    model_val = self.customModelName.Value.strip()
                if model_val:
                    config.conf["VisionAssistant"]["custom_model_name"] = model_val
                    config.conf["VisionAssistant"][m_key] = model_val
            else:
                sel_idx = self.model.GetSelection()
                if sel_idx != wx.NOT_FOUND:
                    model_val = self.model.GetClientData(sel_idx)
                    config.conf["VisionAssistant"][m_key] = model_val
                
            config.conf["VisionAssistant"]["advanced_model_routing"] = self.advRoutingCheck.Value
            routing_save = [
                (self.advOcrModel, f"{p_name}_ocr_model"),
                (self.advSttModel, f"{p_name}_stt_model"),
                (self.advTtsModel, f"{p_name}_tts_model"),
                (self.advOperatorModel, f"{p_name}_operator_model"),
            ]
            if self._live_supported_for(p_name):
                routing_save.append((self.advVideoModel, f"{p_name}_video_model"))
                routing_save.append((self.advLiveModel, f"{p_name}_live_model"))
            for attr, conf_key in routing_save:
                idx = attr.GetSelection()
                if idx != wx.NOT_FOUND:
                    config.conf["VisionAssistant"][conf_key] = attr.GetClientData(idx)

            if p_name == "custom":
                config.conf["VisionAssistant"]["custom_api_url"] = self.customUrl.Value.strip()
                config.conf["VisionAssistant"]["custom_api_type"] = "openai" if self.customType.GetSelection() == 0 else "gemini"
                config.conf["VisionAssistant"]["custom_upload_support"] = self.customUploadSupport.Value
                config.conf["VisionAssistant"]["use_advanced_endpoints"] = self.useAdvancedEndpoints.Value
                config.conf["VisionAssistant"]["custom_models_url"] = self.customModelsUrl.Value.strip()
                config.conf["VisionAssistant"]["custom_ocr_url"] = self.customOcrUrl.Value.strip()
                config.conf["VisionAssistant"]["custom_stt_url"] = self.customSttUrl.Value.strip()
                config.conf["VisionAssistant"]["custom_tts_url"] = self.customTtsUrl.Value.strip()
                config.conf["VisionAssistant"]["custom_operator_url"] = self.customAssistantUrl.Value.strip()
                if not has_fetched_models:
                    config.conf["VisionAssistant"]["custom_ocr_model"] = self.customOcrModel.Value.strip()
                    config.conf["VisionAssistant"]["custom_stt_model"] = self.customSttModel.Value.strip()
                    config.conf["VisionAssistant"]["custom_tts_model"] = self.customTtsModel.Value.strip()
                    config.conf["VisionAssistant"]["custom_operator_model"] = self.customAssistantModel.Value.strip()
                
                config.conf["VisionAssistant"]["custom_tts_voice"] = self.customTtsVoice.Value.strip()

            final_voice = ""
            if p_name == "custom" and self.customTtsVoice.Value.strip():
                final_voice = self.customTtsVoice.Value.strip()
            else:
                v_idx = self.voice_sel.GetSelection()
                if v_idx != wx.NOT_FOUND:
                    final_voice = self.voice_sel.GetClientData(v_idx)
            
            if final_voice:
                config.conf["VisionAssistant"]["tts_voice"] = final_voice

            config.conf["VisionAssistant"]["ai_temperature"] = float(self.aiTemp.GetStringSelection())
            config.conf["VisionAssistant"]["proxy_url"] = self.proxyUrl.Value.strip()
            config.conf["VisionAssistant"]["source_language"] = SOURCE_LIST[self.sourceLang.GetSelection()][1]
            config.conf["VisionAssistant"]["target_language"] = TARGET_LIST[self.targetLang.GetSelection()][1]
            config.conf["VisionAssistant"]["ai_response_language"] = TARGET_LIST[self.aiResponseLang.GetSelection()][1]
            config.conf["VisionAssistant"]["smart_swap"] = self.smartSwap.Value
            config.conf["VisionAssistant"]["check_update_startup"] = self.checkUpdateStartup.Value
            config.conf["VisionAssistant"]["clean_markdown_chat"] = self.cleanMarkdown.Value
            config.conf["VisionAssistant"]["copy_to_clipboard"] = self.copyToClipboard.Value
            config.conf["VisionAssistant"]["skip_chat_dialog"] = self.skipChatDialog.Value
            config.conf["VisionAssistant"]["live_direct_output"] = self.liveDirectOutput.Value
            config.conf["VisionAssistant"]["captcha_mode"] = 'navigator' if self.captchaMode.GetSelection() == 0 else 'fullscreen'
            config.conf["VisionAssistant"]["ocr_engine"] = OCR_ENGINES[self.ocr_sel.GetSelection()][1]
            config.conf["VisionAssistant"]["ocr_batch_size"] = self.batch_size.GetValue()
            config.conf["VisionAssistant"]["video_srt_chunk_minutes"] = self.vid_chunk_size.GetValue()
            config.conf["VisionAssistant"]["video_chars_as_subtitle"] = self.vid_chars_as_sub.Value
            config.conf["VisionAssistant"]["video_add_disclaimer"] = self.vid_add_disclaimer.Value
            config.conf["VisionAssistant"]["custom_prompts_v2"] = serialize_custom_prompts_v2(self.customPromptItems)
            config.conf["VisionAssistant"]["default_refine_prompts"] = serialize_default_prompt_overrides(self.defaultPromptItems)
        except Exception as e:
            # Translators: Error message shown when saving settings fails.
            wx.CallAfter(gui.messageBox, _("Save Error: {error}").format(error=e), _("Error"), wx.OK | wx.ICON_ERROR)

    def onModelFilter(self, event):
        cb = event.GetEventObject()
        if cb.IsFrozen(): return
        
        sel = cb.GetSelection()
        if sel != wx.NOT_FOUND:
            model_id = cb.GetClientData(sel)
            if cb == getattr(self, 'model', None):
                p_idx = getattr(self, 'provider_sel', None).GetSelection() if getattr(self, 'provider_sel', None) else -1
                if p_idx == 4 and model_id:
                    self.customModelName.SetValue(model_id)
            return

        query = cb.GetValue()
        query_low = query.lower()
        
        if not hasattr(cb, '_all_models_backup') and cb.GetCount() > 0:
            cb._all_models_backup = [(cb.GetString(i), cb.GetClientData(i)) for i in range(cb.GetCount())]
            
        backup = getattr(cb, '_all_models_backup', [])
        
        if not query_low:
            if cb.GetCount() != len(backup):
                cb.Freeze()
                cb.Clear()
                for name, data in backup:
                    cb.Append(name, data)
                cb.SetValue("")
                cb.Thaw()
            return

        filtered = [(name, data) for name, data in backup if query_low in name.lower()]
        
        cb.Freeze()
        cb.Clear()
        for name, data in filtered:
            cb.Append(name, data)
        
        cb.ChangeValue(query) 
        cb.SetInsertionPointEnd()
        cb.Thaw()
        
        if filtered:
            # Translators: Notification showing the number of items found after filtering the model list.
            ui.message(_("{count} items found").format(count=len(filtered)))

class RangeDialog(wx.Dialog):
    def __init__(self, parent, total_pages):
        # Translators: Title of the PDF and document options dialog (range, translation, etc.)
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
        curr_t_code = config.conf["VisionAssistant"]["target_language"]
        t_idx = next((i for i, x in enumerate(TARGET_LIST) if x[1] == curr_t_code), 0)
        self.cmb_lang.SetSelection(t_idx)
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
            'lang': TARGET_LIST[self.cmb_lang.GetSelection()][1]
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
        self.display.SetValue(_("Uploading to AI...\n"))
        
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
        if getattr(self, "mistral_file_id", None):
            threading.Thread(target=AIHandler.delete_mistral_file, args=(self.mistral_file_id,), daemon=True).start()
        ChatDialog.instance = None
        self.Destroy()

    def init_upload(self):
        try:
            p = config.conf["VisionAssistant"]["active_provider"]
            if AIHandler.is_gemini():
                uri = GeminiHandler.upload_for_chat(self.file_path, self.mime_type)
                if uri and not str(uri).startswith("ERROR:"):
                    self.file_uri = uri
                    wx.CallAfter(self.on_ready)
                else:
                    # Translators: Error message shown when uploading a file fails
                    err_msg = str(uri)[6:] if uri else _("Upload failed.")
                    wx.CallAfter(show_error_dialog, err_msg)
                    wx.CallAfter(self.Close)
            elif p == "mistral" and "pdf" in self.mime_type.lower():
                file_id, url_or_err = AIHandler.upload_to_mistral_for_chat(self.file_path)
                if file_id:
                    self.mistral_file_id = file_id
                    self.file_uri = url_or_err
                    wx.CallAfter(self.on_ready)
                else:
                    err_msg = url_or_err[6:] if url_or_err and str(url_or_err).startswith("ERROR:") else _("Upload failed.")
                    wx.CallAfter(show_error_dialog, err_msg)
                    wx.CallAfter(self.Close)
            else:
                try:
                    with open(self.file_path, "rb") as f:
                        self.file_data = base64.b64encode(f.read()).decode('utf-8')
                    wx.CallAfter(self.on_ready)
                except Exception as e:
                    wx.CallAfter(show_error_dialog, str(e))
                    wx.CallAfter(self.Close)
        except Exception as e:
            wx.CallAfter(show_error_dialog, str(e))
            wx.CallAfter(self.Close)

    def on_ready(self):
        # Translators: Message shown in the chat area when the file is uploaded and the AI is ready to answer questions.
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
        p = config.conf["VisionAssistant"]["active_provider"]
        if AIHandler.is_gemini():
            f_data = getattr(self, "file_data", None) if not self.file_uri else None
            resp = GeminiHandler.chat(self.history, msg, self.file_uri, self.mime_type, f_data)
            if str(resp).startswith("ERROR:"):
                wx.CallAfter(show_error_dialog, resp[6:])
                if _vision_assistant_instance: 
                    wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))
                return
            if not self.history:
                u_parts = []
                if self.file_uri: u_parts.append({"file_data": {"mime_type": self.mime_type, "file_uri": self.file_uri}})
                elif f_data: u_parts.append({"inline_data": {"mime_type": self.mime_type, "data": f_data}})
                u_parts.append({"text": msg})
                self.history.append({"role": "user", "parts": u_parts})
            else:
                self.history.append({"role": "user", "parts": [{"text": msg}]})
            self.history.append({"role": "model", "parts": [{"text": resp}]})
        else:
            messages = list(self.history)
            is_pdf = "pdf" in self.mime_type.lower()
            
            if is_pdf:
                if p == "mistral":
                    if not self.history and self.file_uri:
                        content = [
                            {"type": "text", "text": msg},
                            {"type": "document_url", "document_url": self.file_uri}
                        ]
                        messages.append({"role": "user", "content": content})
                    else:
                        messages.append({"role": "user", "content": msg})
                else:
                    doc_text = ""
                    if hasattr(self.parent, "page_cache") and self.parent.page_cache:
                        cached_keys = sorted(self.parent.page_cache.keys())
                        doc_text = "\n\n".join(self.parent.page_cache[k] for k in cached_keys)
                    if not doc_text:
                        # Translators: Placeholder text used in document chat when the text is still being extracted or is empty.
                        doc_text = _("[Text extraction in progress or empty]")
                    
                    system_template = get_prompt_text("document_chat_system")
                    system_instr = apply_prompt_template(system_template, [("response_lang", get_lang_name("ai_response_language"))])
                    
                    if not self.history:
                        messages.append({"role": "user", "content": f"{system_instr}\n\nContext content:\n{doc_text}"})
                        messages.append({"role": "assistant", "content": get_prompt_text("document_chat_ack") or "Context received."})
                    messages.append({"role": "user", "content": msg})
            else:
                if not self.history and getattr(self, "file_data", None):
                    content = [
                        {"type": "text", "text": msg},
                        {"type": "image_url", "image_url": {"url": f"data:{self.mime_type};base64,{self.file_data}"}}
                    ]
                    messages.append({"role": "user", "content": content})
                else:
                    messages.append({"role": "user", "content": msg})
            
            resp = AIHandler.call(messages)
            if resp and resp.startswith("ERROR:"):
                wx.CallAfter(show_error_dialog, resp[6:])
                if _vision_assistant_instance: 
                    wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))
                return

            if is_pdf:
                if p == "mistral":
                    if not self.history and self.file_uri:
                        self.history.append({
                            "role": "user", 
                            "content": [
                                {"type": "text", "text": msg}, 
                                {"type": "document_url", "document_url": self.file_uri}
                            ]
                        })
                    else:
                        self.history.append({"role": "user", "content": msg})
                else:
                    if not self.history:
                        self.history.append({"role": "user", "content": f"{system_instr}\n\nContext content:\n{doc_text}"})
                        self.history.append({"role": "assistant", "content": get_prompt_text("document_chat_ack") or "Context received."})
                    self.history.append({"role": "user", "content": msg})
            else:
                if not self.history and getattr(self, "file_data", None):
                     self.history.append({
                         "role": "user", 
                         "content": [
                             {"type": "text", "text": msg}, 
                             {"type": "image_url", "image_url": {"url": f"data:{self.mime_type};base64,{self.file_data}"}}
                         ]
                     })
                else:
                     self.history.append({"role": "user", "content": msg})
            self.history.append({"role": "assistant", "content": resp})

        # Translators: Spoken prefix for AI response
        ai_prefix = _("AI: ")
        wx.CallAfter(self.display.AppendText, f"{ai_prefix}{resp}\n\n")
        wx.CallAfter(ui.message, ai_prefix + resp)
        if _vision_assistant_instance: 
            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))

class DocumentViewerDialog(wx.Dialog):
    def __init__(self, parent, virtual_doc, settings, resume=None):
        # Translators: Title of the Document Reader window.
        title_text = f"{ADDON_NAME} - {_('Document Reader')}"
        super().__init__(parent, title=title_text, size=(800, 600), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX)
        self.v_doc = virtual_doc
        self.start_page = settings['start']
        self.end_page = settings['end']
        self.do_translate = settings['translate']
        self.target_lang = settings['lang']
        self.range_count = self.end_page - self.start_page + 1
        self.page_cache = {}
        if resume:
            for k, v in resume.get("pages", {}).items():
                self.page_cache[int(k)] = v
        self.current_page = self.start_page
        self.thread_pool = ThreadPoolExecutor(max_workers=5)
        self.abort = False
        self._progress_key = GlobalPlugin._ocr_progress_key("document", list(virtual_doc.file_paths))

        self.init_ui()
        self.Centre()
        if _vision_assistant_instance:
            _vision_assistant_instance._ocr_task_running["document"] = True
            _vision_assistant_instance._ocr_abort["document"] = False
            _vision_assistant_instance.doc_viewer_dlg = self
        threading.Thread(target=self.start_auto_processing, daemon=True).start()

    def _save_doc_progress(self):
        if self.abort:
            return
        OCRProgressStore.save(self._progress_key, {
            "paths": list(self.v_doc.file_paths),
            "start": self.start_page,
            "end": self.end_page,
            "do_translate": self.do_translate,
            "target_lang": self.target_lang if self.do_translate else "",
            "pages": {str(k): v for k, v in self.page_cache.items() if not _is_failed_ocr_page(v)},
        })

    def _on_extraction_complete(self):
        if len(self.page_cache) >= self.range_count:
            OCRProgressStore.clear(self._progress_key)
            if _vision_assistant_instance:
                _vision_assistant_instance._ocr_task_running["document"] = False
                wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))

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
        
        show_tts = AIHandler.is_tts_supported()
        
        hbox_actions = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Button to Ask questions about the document
        self.btn_ask = wx.Button(panel, label=_("Ask AI (Alt+A)"))
        self.btn_ask.Bind(wx.EVT_BUTTON, self.on_ask)
        hbox_actions.Add(self.btn_ask, 0, wx.RIGHT, 5)
        
        # Translators: Button to force re-scan
        self.btn_gemini = wx.Button(panel, label=_("Re-scan with AI (Alt+R)"))
        self.btn_gemini.Bind(wx.EVT_BUTTON, self.on_gemini_scan)
        hbox_actions.Add(self.btn_gemini, 0, wx.RIGHT, 5)
        
        # Translators: Button to generate audio
        self.btn_tts = wx.Button(panel, label=_("Generate Audio (Alt+G)"))
        self.btn_tts.Bind(wx.EVT_BUTTON, self.on_tts)
        hbox_actions.Add(self.btn_tts, 0, wx.RIGHT, 5)
        self.btn_tts.Show(show_tts)

        # Translators: Button to view formatted content
        self.btn_view = wx.Button(panel, label=_("View Formatted"))
        self.btn_view.Bind(wx.EVT_BUTTON, self.on_view)
        hbox_actions.Add(self.btn_view, 0, wx.RIGHT, 5)

        # Translators: Button to save text
        self.btn_save = wx.Button(panel, label=_("Save (Alt+S)"))
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save_all)
        hbox_actions.Add(self.btn_save, 0)
        
        vbox.Add(hbox_actions, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        if show_tts:
            hbox_tts = wx.BoxSizer(wx.HORIZONTAL)
            # Translators: Label for TTS Voice selection
            self.lbl_voice = wx.StaticText(panel, label=_("TTS Voice:"))
            hbox_tts.Add(self.lbl_voice, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
            
            p_name = config.conf["VisionAssistant"]["active_provider"]
            voices = AIHandler.get_voices(p_name) or (OPENAI_VOICES if p_name in ["openai", "custom"] else GEMINI_VOICES)
            voice_choices = [f"{v[0]} - {v[1]}" for v in voices]

            self.voice_sel = wx.Choice(panel, choices=voice_choices)
            curr_voice = config.conf["VisionAssistant"]["tts_voice"]
            try:
                v_idx = next(i for i, v in enumerate(voices) if v[0] == curr_voice)
                self.voice_sel.SetSelection(v_idx)
            except Exception: self.voice_sel.SetSelection(0)
            if p_name == "minimax":
                threading.Thread(target=self._refresh_minimax_voices_in_format_dialog, daemon=True).start()

            hbox_tts.Add(self.voice_sel, 1, wx.EXPAND)
            vbox.Add(hbox_tts, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        # Translators: Label for a button to close the dialog.
        btn_close = wx.Button(panel, wx.ID_CLOSE, label=_("Close"))
        btn_close.Bind(wx.EVT_BUTTON, self.on_close)
        vbox.Add(btn_close, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        
        panel.SetSizer(vbox)
        accel_list = [
            (wx.ACCEL_CTRL, wx.WXK_PAGEDOWN, self.btn_next.GetId()),
            (wx.ACCEL_CTRL, wx.WXK_PAGEUP, self.btn_prev.GetId()),
            (wx.ACCEL_CTRL, ord('S'), self.btn_save.GetId()),
            (wx.ACCEL_ALT, ord('S'), self.btn_save.GetId()),
            (wx.ACCEL_ALT, ord('A'), self.btn_ask.GetId()),
            (wx.ACCEL_ALT, ord('R'), self.btn_gemini.GetId())
        ]
        if show_tts:
            accel_list.append((wx.ACCEL_ALT, ord('G'), self.btn_tts.GetId()))
            
        self.SetAcceleratorTable(wx.AcceleratorTable(accel_list))
        self.cmb_pages.SetSelection(0)
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
        
        self.update_view()
        self.txt_content.SetFocus()

    def on_close(self, event):
        self.abort = True
        self.thread_pool.shutdown(wait=False)
        if _vision_assistant_instance:
            _vision_assistant_instance._ocr_task_running["document"] = False
            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))
            if getattr(_vision_assistant_instance, "doc_viewer_dlg", None) is self:
                _vision_assistant_instance.doc_viewer_dlg = None
        self.Destroy()

    def start_auto_processing(self):
        self._save_doc_progress()
        if _vision_assistant_instance:
            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Extracting Text..."))
            
        p = config.conf["VisionAssistant"]["active_provider"]
        engine = config.conf["VisionAssistant"]["ocr_engine"]
        
        if engine == 'gemini' and AIHandler.is_gemini():
            threading.Thread(target=self.gemini_scan_batch_thread, daemon=True).start()
        elif engine == 'gemini' and p == "mistral":
            threading.Thread(target=self.mistral_scan_batch_thread, daemon=True).start()
        else:
            for i in range(self.start_page, self.end_page + 1):
                if i in self.page_cache:
                    continue
                self.thread_pool.submit(self.process_page_worker, i)

    @staticmethod
    def _extract_text_layer_from_page(page):
        blocks = page.get_text("blocks", sort=True)
        processed_blocks = []
        
        for b in blocks:
            lines = [l.strip() for l in b[4].splitlines() if l.strip()]
            if not lines:
                continue
            
            if lines[0] == ':' and len(lines) > 1:
                lines[1] = lines[1] + ':'
                lines.pop(0)
            
            block_text = " ".join(lines)
            
            if block_text.startswith(':') and any('\u0600' <= c <= '\u06FF' for c in block_text):
                parts = block_text[1:].strip().split(' ', 1)
                if len(parts) > 1:
                    block_text = parts[0] + ': ' + parts[1]
                else:
                    block_text = parts[0] + ':'
                    
            processed_blocks.append(block_text)
        
        return "\n".join(processed_blocks)

    def process_page_worker(self, page_num):
        if page_num in self.page_cache: return
        if self.abort: return
        text = self._get_page_text_logic(page_num)
        if self.abort: return
        self.page_cache[page_num] = text
        self._save_doc_progress()
        
        is_complete = len(self.page_cache) >= self.range_count
        if not is_complete and _vision_assistant_instance:
            completed = len(self.page_cache)
            progress_msg = _("Processing page {current} of {total}...").format(current=completed, total=self.range_count)
            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', progress_msg)
            
        self._on_extraction_complete()
        
        if page_num == self.current_page:
            wx.CallAfter(self.update_view)
            # Translators: Spoken message when the current page is ready
            wx.CallAfter(ui.message, _("Page {num} ready").format(num=page_num + 1))

    def _get_page_text_logic(self, page_num):
        file_path, page_idx = self.v_doc.get_page_info(page_num)
        if not file_path: return ""
        doc = None
        try:
            doc = fitz.open(file_path)
            page = doc.load_page(page_idx)
            
            engine = config.conf["VisionAssistant"]["ocr_engine"]
            text = None
            
            if engine == 'none':
                text = self._extract_text_layer_from_page(page)
                if not text:
                    # Translators: Message shown when a PDF has no text layer.
                    text = _("The 'None (Extract Text Layer)' engine cannot process image-based content. Please change the OCR Engine to 'Chrome' or 'AI (Advanced)' in settings.")
            else:
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("jpg")
                
                if engine == 'gemini':
                    img_b64 = base64.b64encode(img_bytes).decode('utf-8')
                    text = AIHandler.ocr(img_b64, "image/jpeg")
                elif engine == 'chrome':
                    text = ChromeOCREngine.recognize(img_bytes)
                
                if not text or not text.strip():
                    # Translators: Placeholder text when OCR fails
                    text = _("[OCR failed. Try a different AI model or provider.]")
            
            final_text = str(text) if text else ""
            doc.close()
            
            if self.do_translate and final_text and not final_text.startswith("["):
                if engine == 'chrome':
                    final_text = GoogleTranslator.translate(final_text, self.target_lang)
                else:
                    final_text = AIHandler.translate(final_text, self.target_lang)
            
            return final_text
        except Exception as e:
            if doc: 
                try: doc.close()
                except Exception: pass
            log.error(f"Page processing failed: {str(e)}")
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
        p = config.conf["VisionAssistant"]["active_provider"]
        keys = AIHandler.get_keys(p)
        if not keys:
            # Translators: Error when no API keys are found in settings
            wx.MessageBox(_("No API Keys configured."), _("Error"), wx.ICON_ERROR)
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
        ui.message(_("Scanning with AI..."))
        threading.Thread(target=self.gemini_scan_single_thread, args=(self.current_page,), daemon=True).start()

    def gemini_scan_single_thread(self, page_num):
        def _run():
            try:
                file_path, page_idx = self.v_doc.get_page_info(page_num)
                doc = fitz.open(file_path); page = doc.load_page(page_idx)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                img_bytes = pix.tobytes("jpg"); doc.close()
                
                img_b64 = base64.b64encode(img_bytes).decode('utf-8')
                text = AIHandler.ocr(img_b64, "image/jpeg")
                
                if text and text.startswith("ERROR:"):
                    # Translators: Error shown when a specific page scan fails.
                    self.page_cache[page_num] = _("[Scan failed: {err}]").format(err=text[6:])
                else:
                    if self.do_translate:
                        text = AIHandler.translate(text, self.target_lang)
                    # Translators: Message shown when OCR returns no text for a page.
                    self.page_cache[page_num] = text if text else _("[No text detected]")
                    
                if self.current_page == page_num: 
                    wx.CallAfter(self.update_view)
                    # Translators: Message when scan is complete
                    wx.CallAfter(ui.message, _("Scan complete"))
            except Exception as e:
                # Translators: Generic system error message inside the document viewer.
                self.page_cache[page_num] = _("[Error: {msg}]").format(msg=str(e))
                wx.CallAfter(self.update_view)

        self.thread_pool.submit(_run)

    def do_rescan_all(self, event):
        threading.Thread(target=self.gemini_scan_batch_thread, daemon=True).start()

    def gemini_scan_batch_thread(self):
        engine = config.conf["VisionAssistant"]["ocr_engine"]
        
        if engine == 'none':
            # Translators: Status message for local text extraction
            msg = _("Extracting text layer...")
            wx.CallAfter(ui.message, msg)
            for i in range(self.start_page, self.end_page + 1):
                self.thread_pool.submit(self.process_page_worker, i)
            return

        # Translators: Message when batch scan starts
        msg = _("Batch Processing Started")
        if _vision_assistant_instance: 
            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', msg)
        wx.CallAfter(ui.message, msg)
        
        raw_batch_size = config.conf["VisionAssistant"].get("ocr_batch_size", 20)
        total_pages = self.end_page - self.start_page + 1
        
        batch_size = total_pages if raw_batch_size == 0 else raw_batch_size
        
        for i in range(self.start_page, self.end_page + 1, batch_size):
            if self.abort:
                break
            batch_end = min(i + batch_size - 1, self.end_page)
            if all((idx in self.page_cache) for idx in range(i, batch_end + 1)):
                continue
            current_batch_count = batch_end - i + 1

            # Translators: Status message showing the progress of document scanning. {start} and {end} are page numbers.
            progress_msg = _("Processing pages {start} to {end}...").format(start=i+1, end=batch_end+1)
            if _vision_assistant_instance:
                wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', progress_msg)
            wx.CallAfter(ui.message, progress_msg)

            upload_path = self.v_doc.create_merged_pdf(i, batch_end)
            if not upload_path: continue

            try:
                p_text = apply_prompt_template(
                    get_prompt_text("ocr_document_translate" if self.do_translate else "ocr_document_extract"),
                    [("target_lang", self.target_lang)]
                )
                range_str = f"{i+1}-{batch_end+1}"
                results = GeminiHandler.upload_and_process_batch(upload_path, "application/pdf", current_batch_count, prompt=p_text, page_range_text=range_str, abort_checker=lambda: self.abort)
                if self.abort:
                    break
                if results and not str(results[0]).startswith("ERROR:"):
                    for j, text_part in enumerate(results):
                        page_idx = i + j
                        if page_idx <= self.end_page:
                            self.page_cache[page_idx] = text_part.strip()
                    self._save_doc_progress()
                    self._on_extraction_complete()
                    wx.CallAfter(self.update_view)
                else:
                    err_msg = results[0][6:] if results else "Unknown"
                    for j in range(i, batch_end + 1):
                        # Translators: Error message shown in the document viewer when a specific page scan fails. The {err} placeholder is replaced with the error details.
                        self.page_cache[j] = _("[Scan failed: {err}]").format(err=err_msg)
                    wx.CallAfter(self.update_view)
            finally:
                if upload_path and os.path.exists(upload_path):
                    try: os.remove(upload_path)
                    except Exception: pass

        if _vision_assistant_instance:
            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))
        if self.abort:
            return
        self._on_extraction_complete()
        # Translators: Success message shown when all batches of the document have been processed.
        wx.CallAfter(ui.message, _("All document pages have been processed."))

    def mistral_scan_batch_thread(self):
        # Translators: Message when batch scan starts
        msg = _("Batch Processing Started")
        if _vision_assistant_instance: 
            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', msg)
        wx.CallAfter(ui.message, msg)
        
        raw_batch_size = config.conf["VisionAssistant"].get("ocr_batch_size", 20)
        total_pages = self.end_page - self.start_page + 1
        batch_size = total_pages if raw_batch_size == 0 else raw_batch_size
        
        for i in range(self.start_page, self.end_page + 1, batch_size):
            if self.abort:
                break
            batch_end = min(i + batch_size - 1, self.end_page)
            if all((idx in self.page_cache) for idx in range(i, batch_end + 1)):
                continue
            current_batch_count = batch_end - i + 1

            # Translators: Status message showing the progress of document scanning. {start} and {end} are page numbers.
            progress_msg = _("Processing pages {start} to {end}...").format(start=i+1, end=batch_end+1)
            if _vision_assistant_instance:
                wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', progress_msg)
            wx.CallAfter(ui.message, progress_msg)

            upload_path = self.v_doc.create_merged_pdf(i, batch_end)
            if not upload_path: continue

            try:
                res = AIHandler.ocr(upload_path, "application/pdf")
                if self.abort:
                    break
                
                if res and not res.startswith("ERROR:"):
                    results = res.split('[[[PAGE_SEP]]]')
                    is_empty_response = len(results) == 1 and not results[0].strip()
                    
                    for j in range(current_batch_count):
                        page_idx = i + j
                        if page_idx <= self.end_page:
                            if is_empty_response:
                                # Translators: Error shown in the document reader when the AI returns an empty response for a batch of pages.
                                self.page_cache[page_idx] = _("[Error: Empty response received from AI. Try reducing the batch size in settings or scanning page-by-page.]")
                            elif j < len(results):
                                page_text = results[j].strip()
                                if self.do_translate and page_text:
                                    page_text = AIHandler.translate(page_text, self.target_lang)
                                self.page_cache[page_idx] = page_text
                            else:
                                # Translators: Error shown in the document reader when a page is dropped because the AI output exceeded its limit during batch processing.
                                self.page_cache[page_idx] = _("[Error: Page skipped during batch processing due to model output limits. Try a smaller batch size in settings.]")
                                
                    self._save_doc_progress()
                    self._on_extraction_complete()
                    wx.CallAfter(self.update_view)
                else:
                    err_msg = res[6:] if res else "Unknown"
                    for j in range(i, batch_end + 1):
                        # Translators: Error message shown in the document viewer when a specific page scan fails. The {err} placeholder is replaced with the error details.
                        self.page_cache[j] = _("[Scan failed: {err}]").format(err=err_msg)
                    wx.CallAfter(self.update_view)
                    
            except Exception as e:
                log.error(f"Error in Mistral batch scan: {e}", exc_info=True)
                err_msg = str(e)
                for j in range(i, batch_end + 1):
                    self.page_cache[j] = _("[Scan failed: {err}]").format(err=err_msg)
                wx.CallAfter(self.update_view)
                
            finally:
                if upload_path and os.path.exists(upload_path):
                    try: os.remove(upload_path)
                    except Exception: pass

        if _vision_assistant_instance:
            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))
        if self.abort:
            return
        self._on_extraction_complete()
        # Translators: Success message shown when all batches of the document have been processed.
        wx.CallAfter(ui.message, _("All document pages have been processed."))

    def on_tts(self, event):
        if not AIHandler.is_tts_supported():
            # Translators: Error message when trying to use TTS with an unsupported provider
            wx.MessageBox(_("TTS is not supported by the current provider or configuration."), _("Error"), wx.ICON_ERROR)
            return

        p = config.conf["VisionAssistant"]["active_provider"]
        keys = AIHandler.get_keys(p)
        if not keys and p != "custom":
            # Translators: Error when no API keys are found in settings
            wx.MessageBox(_("No API Keys configured."), _("Error"), wx.ICON_ERROR)
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
            wait_count = 0
            while i not in self.page_cache and wait_count < 600:
                time.sleep(0.1)
                wait_count += 1
            # Translators: Placeholder text shown in the document reader when processing takes too long
            full_text.append(self.page_cache.get(i, _("[Processing timeout]")))
        final_text = "\n".join(full_text).strip()
        if not final_text: return
        wx.CallAfter(self._save_tts, final_text)

    def _save_tts(self, text):
        # Translators: File dialog title for saving audio
        path = get_file_path(_("Save Audio"), "MP3 Files (*.mp3)|*.mp3|WAV Files (*.wav)|*.wav", mode="save")
        if path:
            voice = config.conf["VisionAssistant"]["tts_voice"]
            if hasattr(self, "voice_sel") and self.voice_sel:
                sel = self.voice_sel.GetSelection()
                if sel != wx.NOT_FOUND:
                    voice = self.voice_sel.GetClientData(sel)
            threading.Thread(target=self.tts_worker, args=(text, voice, path), daemon=True).start()

    def tts_worker(self, text, voice, path):
        # Translators: Message while generating audio
        msg = _("Generating Audio...")
        if _vision_assistant_instance: 
            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', msg)
        wx.CallAfter(ui.message, msg)
        try:
            audio_b64, is_raw_pcm = AIHandler.generate_speech(text, voice)
            if not audio_b64 or audio_b64.startswith("ERROR:"):
                 # Translators: Fallback error message during text-to-speech generation.
                 err_msg = audio_b64[6:] if audio_b64 else _("Unknown Error")
                 # Translators: Error message shown when text-to-speech generation fails.
                 wx.CallAfter(wx.MessageBox, _("TTS Error: {error}").format(error=err_msg), _("Error"), wx.ICON_ERROR)
                 if _vision_assistant_instance: 
                     wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))
                 return
            
            missing_padding = len(audio_b64) % 4
            if missing_padding: audio_b64 += '=' * (4 - missing_padding)
            audio_data = base64.b64decode(audio_b64)

            if not is_raw_pcm:
                with open(path, "wb") as f:
                    f.write(audio_data)
            else:
                if path.lower().endswith(".mp3"):
                    lame_path = os.path.join(os.path.dirname(__file__), "lib", "lame.exe")
                    if not os.path.exists(lame_path):
                        # Translators: Error message when the MP3 encoder (LAME) is missing.
                        wx.CallAfter(wx.MessageBox, _("lame.exe not found in lib folder."), "Error", wx.ICON_ERROR)
                        if _vision_assistant_instance: 
                            wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))
                        return
                    process = subprocess.Popen([lame_path, "-r", "-s", "24", "-m", "m", "-b", "128", "--bitwidth", "16", "--resample", "24", "-q", "0", "-", path],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
                    )
                    process.communicate(input=audio_data)
                else:
                    with wave.open(path, "wb") as wf:
                        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(24000); wf.writeframes(audio_data)

            # Translators: Spoken message when audio is saved
            res_msg = _("Audio Saved")
            if _vision_assistant_instance: 
                wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))
            wx.CallAfter(ui.message, res_msg)
            # Translators: Success message after generating TTS audio.
            wx.CallAfter(wx.MessageBox, _("Audio file generated and saved successfully."), _("Success"), wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            if _vision_assistant_instance: 
                wx.CallAfter(setattr, _vision_assistant_instance, 'current_status', _("Idle"))
            # Translators: Error message shown when text-to-speech generation fails.
            wx.CallAfter(wx.MessageBox, _("TTS Error: {error}").format(error=e), _("Error"), wx.ICON_ERROR)

    def on_ask(self, event):
        p = config.conf["VisionAssistant"]["active_provider"]
        keys = AIHandler.get_keys(p)
        if not keys and p != "custom":
            # Translators: Error when no API keys are found in settings
            wx.MessageBox(_("No API Keys configured."), _("Error"), wx.ICON_ERROR)
            return
        if ChatDialog.instance:
            ChatDialog.instance.Raise()
            ChatDialog.instance.SetFocus()
            return
        file_path, _unused = self.v_doc.get_page_info(self.current_page)
        if file_path: 
            dlg = ChatDialog(self, file_path)
            dlg.Show()

    def on_save_all(self, event):
        # Translators: File dialog filter for saving text/html
        wildcard = "Text File (*.txt)|*.txt|HTML File (*.html)|*.html"
        default_name = ""
        if self.v_doc and self.v_doc.file_paths:
            base = os.path.basename(self.v_doc.file_paths[0])
            name, _ext = os.path.splitext(base)
            default_name = name + ".txt"
        # Translators: File dialog title for saving
        path = get_file_path(_("Save"), wildcard, mode="save", default_name=default_name)
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
                
                wait_count = 0
                while i not in self.page_cache and wait_count < 600:
                    time.sleep(0.1)
                    wait_count += 1
                # Translators: Placeholder text shown in the document reader when processing takes too long
                txt = self.page_cache.get(i, _("[Processing timeout]"))
                
                if is_html:
                    h = markdown_to_html(txt)
                    if "<body>" in h: h = h.split("<body>")[1].split("</body>")[0]
                    # Translators: Heading for each page in the formatted content view.
                    page_label = _("Page {num}").format(num=i+1)
                    sep = "" if i == self.start_page else "<hr>"
                    full_content.append(f"{sep}<h2>{page_label}</h2>{h}")
                else:
                    sep = "" if i == self.start_page else "\n"
                    full_content.append(f"{sep}--- Page {i+1} ---\n{txt}\n")
            with open(path, "w", encoding="utf-8-sig") as f:
                if is_html: f.write(f"<!DOCTYPE html><html><head><meta charset=\"UTF-8\"></head><body>{''.join(full_content)}</body></html>")
                else: f.write("\n".join(full_content))
            # Translators: Status label when save is complete
            wx.CallAfter(self.lbl_status.SetLabel, _("Saved"))
            # Translators: Message box content for successful save
            wx.CallAfter(wx.MessageBox, _("File saved successfully."), _("Success"), wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            # Translators: Error message shown when saving a file fails.
            wx.CallAfter(wx.MessageBox, _("Save Error: {error}").format(error=e), _("Error"), wx.ICON_ERROR)
        finally: wx.CallAfter(self.btn_save.Enable)

    def _refresh_minimax_voices_in_format_dialog(self):
        try:
            config.conf["VisionAssistant"]["minimax_voices_cache"] = ""
            config.conf["VisionAssistant"]["minimax_voices_cache_time"] = 0
            voices = AIHandler.get_voices("minimax")
            if voices and hasattr(self, 'voice_sel') and self.voice_sel:
                wx.CallAfter(self._populate_format_voice_sel, voices)
        except Exception as e:
            log.warning(f"Background MiniMax voice refresh (format dialog) failed: {e}")

    def _populate_format_voice_sel(self, voices):
        try:
            if not hasattr(self, 'voice_sel') or not self.voice_sel:
                return
            self.voice_sel.Clear()
            for v in voices:
                self.voice_sel.Append(f"{v[0]} - {v[1]}", v[0])
            curr_voice = config.conf["VisionAssistant"].get("tts_voice", "English_expressive_narrator")
            for i in range(self.voice_sel.GetCount()):
                if self.voice_sel.GetClientData(i) == curr_voice:
                    self.voice_sel.SetSelection(i)
                    return
            if self.voice_sel.GetCount() > 0:
                self.voice_sel.SetSelection(0)
        except Exception as e:
            log.warning(f"Failed to populate format voice_sel: {e}")

def _generate_object_signature(obj):
    role_type = int(getattr(obj, "role", 0))
    unique_signature = ""
    
    try:
        if hasattr(obj, "UIAElement") and obj.UIAElement.currentAutomationId:
            unique_signature = f"uia_{obj.UIAElement.currentAutomationId}"
    except Exception:
        pass
        
    if not unique_signature:
        try:
            win_ctrl_id = getattr(obj, "windowControlID", None)
            class_name = getattr(obj, "windowClassName", None)
            if win_ctrl_id and class_name:
                unique_signature = f"win_{class_name}_{win_ctrl_id}"
        except Exception:
            pass
            
    if not unique_signature:
        loc = getattr(obj, "location", None)
        if loc:
            try:
                handle = getattr(obj, "windowHandle", None)
                if handle:
                    rect = winUser.getWindowRect(handle)
                    w_left, w_top = rect.left, rect.top
                else:
                    w_left, w_top = 0, 0
            except Exception:
                w_left, w_top = 0, 0
            rel_x = loc.left - w_left
            rel_y = loc.top - w_top
            unique_signature = f"coords_{rel_x},{rel_y}"
            
    if not unique_signature:
        return None
        
    try:
        raw_name = obj._get_name() if hasattr(obj, '_get_name') else getattr(obj, "name", "")
    except Exception:
        raw_name = getattr(obj, "name", "")
    raw_name = raw_name or ""
    
    return f"sig_{role_type}_{unique_signature}_{raw_name}"

class CustomLabelOverlay(NVDAObjects.NVDAObject):
    @property
    def name(self):
        instance = _vision_assistant_instance
        uniqueId = instance._getAppId(self) if instance else self.appModule.appName
        
        key = _generate_object_signature(self)
        cache = getattr(instance, "labels_cache", {})
        if uniqueId in cache:
            if key and key in cache[uniqueId]:
                return cache[uniqueId][key]
                                
        return super().name

class LabelManagerDialog(wx.Dialog):
    def __init__(self, parent, app_name, labels_dict):
        # Translators: Title of the Label Manager dialog.
        title_text = _("Label Manager - {app}").format(app=app_name)
        super().__init__(parent, title=title_text, size=(550, 700))
        self.app_name = app_name
        self.labels_dict = labels_dict
        self.action_type = None
        self.target_keys = []
        self.new_name = ""

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Translators: Instruction for managing labels using the list view.
        instruction_text = _("Check items to delete, or select one to rename:")
        instruction = wx.StaticText(self, label=instruction_text)
        main_sizer.Add(instruction, 0, wx.ALL, 10)

        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list_ctrl.EnableCheckBoxes()
        
        # Translators: Header for the label name column in the manager list.
        self.list_ctrl.InsertColumn(0, _("Label Name"), width=300)
        # Translators: Header for the role column in the manager list.
        self.list_ctrl.InsertColumn(1, _("Role"), width=150)

        self.keys_list = list(labels_dict.keys())
        self.list_ctrl.Freeze()
        for i, k in enumerate(self.keys_list):
            try:
                role_id = int(k.split(':')[0])
                role_name = controlTypes.roleLabels.get(role_id, str(role_id))
            except Exception:
                role_name = "Unknown"
            self.list_ctrl.InsertItem(i, labels_dict[k])
            self.list_ctrl.SetItem(i, 1, role_name)
        self.list_ctrl.Thaw()

        main_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        selection_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Button to check all items in the list.
        self.btn_select_all = wx.Button(self, label=_("Select &All"))
        self.btn_select_all.Bind(wx.EVT_BUTTON, self.on_select_all)
        # Translators: Button to uncheck all items in the list.
        self.btn_deselect_all = wx.Button(self, label=_("Deselect A&ll"))
        self.btn_deselect_all.Bind(wx.EVT_BUTTON, self.on_deselect_all)
        
        selection_sizer.Add(self.btn_select_all, 1, wx.RIGHT, 5)
        selection_sizer.Add(self.btn_deselect_all, 1, wx.LEFT, 5)
        main_sizer.Add(selection_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        btn_grid = wx.GridSizer(2, 2, 5, 5)
        # Translators: Button to rename the currently focused label.
        self.btn_rename = wx.Button(self, label=_("&Rename"))
        self.btn_rename.Bind(wx.EVT_BUTTON, self.on_rename)
        # Translators: Button to delete all checked labels.
        self.btn_delete = wx.Button(self, label=_("&Delete Checked"))
        self.btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        # Translators: Button to trigger a new full scan of the application.
        btn_rescan = wx.Button(self, label=_("Re&scan"))
        btn_rescan.Bind(wx.EVT_BUTTON, self.on_rescan)
        # Translators: Button to close the label manager.
        btn_close = wx.Button(self, wx.ID_CANCEL, label=_("&Close"))

        btn_grid.Add(self.btn_rename, 0, wx.EXPAND)
        btn_grid.Add(self.btn_delete, 0, wx.EXPAND)
        btn_grid.Add(btn_rescan, 0, wx.EXPAND)
        btn_grid.Add(btn_close, 0, wx.EXPAND)
        
        main_sizer.Add(btn_grid, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(main_sizer)
        
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_CHECKED, self.update_ui)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_UNCHECKED, self.update_ui)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.update_ui)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.update_ui)
        self.list_ctrl.Bind(wx.EVT_CHAR_HOOK, self.on_key_event)
        
        self.update_ui()
        self.list_ctrl.SetFocus()

    def on_key_event(self, event):
        if event.ControlDown() and event.GetKeyCode() == ord('A'):
            self.on_select_all(None)
        else:
            event.Skip()

    def update_ui(self, event=None):
        count = self.list_ctrl.GetItemCount()
        checked_count = sum(1 for i in range(count) if self.list_ctrl.IsItemChecked(i))
        selected_idx = self.list_ctrl.GetFirstSelected()
        can_rename = (checked_count == 1) or (checked_count == 0 and selected_idx != -1)
        self.btn_rename.Enable(can_rename)
        self.btn_delete.Enable(checked_count > 0 or selected_idx != -1)

    def on_select_all(self, event):
        self.list_ctrl.Freeze()
        for i in range(self.list_ctrl.GetItemCount()):
            self.list_ctrl.CheckItem(i, True)
        self.list_ctrl.Thaw()
        self.update_ui()

    def on_deselect_all(self, event):
        self.list_ctrl.Freeze()
        for i in range(self.list_ctrl.GetItemCount()):
            self.list_ctrl.CheckItem(i, False)
        self.list_ctrl.Thaw()
        self.update_ui()

    def on_rename(self, event):
        idx = -1
        for i in range(self.list_ctrl.GetItemCount()):
            if self.list_ctrl.IsItemChecked(i):
                idx = i
                break
        if idx == -1:
            idx = self.list_ctrl.GetFirstSelected()
        if idx == -1:
            # Translators: Error message shown when no item is selected for renaming.
            ui.message(_("Please select an item from the list to rename."))
            return
        
        key = self.keys_list[idx]
        current_name = self.labels_dict[key]
        # Translators: Prompt message for entering a new label name.
        rename_prompt = _("Enter new name:")
        # Translators: Window title for the rename dialog.
        rename_title = _("Rename Label")
        
        with wx.TextEntryDialog(self, rename_prompt, rename_title, value=current_name) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.action_type = "rename"
                self.target_keys = [key]
                self.new_name = dlg.GetValue()
                self.EndModal(wx.ID_OK)

    def on_delete(self, event):
        self.target_keys = [self.keys_list[i] for i in range(self.list_ctrl.GetItemCount()) if self.list_ctrl.IsItemChecked(i)]
        if not self.target_keys:
            idx = self.list_ctrl.GetFirstSelected()
            if idx != -1:
                self.target_keys = [self.keys_list[idx]]
        if not self.target_keys:
            # Translators: Error message shown when no items are checked for deletion.
            ui.message(_("Please check at least one item to delete."))
            return
        self.action_type = "delete"
        self.EndModal(wx.ID_OK)

    def on_rescan(self, event):
        self.action_type = "rescan"
        self.EndModal(wx.ID_OK)


class VideoSourceDialog(wx.Dialog):
    def __init__(self, parent):
        # Translators: Title of the video analysis dialog
        title = _("{name} - Analyze Video").format(name=ADDON_NAME)
        super().__init__(parent, title=title, size=(550, 290))
        self.local_path = None
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Translators: Label instructing the user to enter a URL or browse for a local video
        lbl = wx.StaticText(self, label=_("Enter Video URL (YouTube, Instagram, Twitter, TikTok) or Browse for a local video:"))
        sizer.Add(lbl, 0, wx.ALL, 10)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.url_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        hbox.Add(self.url_input, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        
        # Translators: Button to browse for a local video file
        btn_browse = wx.Button(self, label=_("&Browse..."))
        btn_browse.Bind(wx.EVT_BUTTON, self.on_browse)
        hbox.Add(btn_browse, 0, wx.ALIGN_CENTER_VERTICAL)
        
        sizer.Add(hbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        
        # Translators: Options for video analysis mode
        choices = [_("General Video Analysis"), _("Generate Audio Description (SRT File)")]
        self.action_choice = wx.RadioBox(
            self, 
            # Translators: Label for the video action radio box
            label=_("Action"), 
            choices=choices,
            majorDimension=1, 
            style=wx.RA_SPECIFY_COLS
        )
        sizer.Add(self.action_choice, 0, wx.EXPAND | wx.ALL, 10)

        self.action_choice.Bind(wx.EVT_RADIOBOX, self.on_action_change)

        # Translators: Checkbox label to add character list as the first subtitle in video SRT output.
        self.chars_as_sub_check = wx.CheckBox(self, label=_("Add character list as first subtitle"))
        self.chars_as_sub_check.SetValue(config.conf["VisionAssistant"].get("video_chars_as_subtitle", True))
        sizer.Add(self.chars_as_sub_check, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.chars_as_sub_check.Show(False)

        # Translators: Checkbox label to add an AI warning disclaimer at the beginning of the video SRT output.
        self.disclaimer_check = wx.CheckBox(self, label=_("Add AI disclaimer at the beginning"))
        self.disclaimer_check.SetValue(config.conf["VisionAssistant"].get("video_add_disclaimer", True))
        sizer.Add(self.disclaimer_check, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        self.disclaimer_check.Show(False)

        btn_sizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        self.SetSizer(sizer)
        self.url_input.SetFocus()

    def on_browse(self, event):
        # Translators: Filter for video files in the file dialog
        wildcard = _("Video Files") + " (*.mp4;*.avi;*.mkv;*.mov;*.wmv;*.flv;*.webm)|*.mp4;*.avi;*.mkv;*.mov;*.wmv;*.flv;*.webm"
        # Translators: Title of the file dialog for selecting a video
        with wx.FileDialog(self, _("Select Local Video"), wildcard=wildcard, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.local_path = dlg.GetPath()
                self.url_input.SetValue(self.local_path)

    def on_action_change(self, event):
        is_srt = (self.action_choice.GetSelection() == 1)
        self.chars_as_sub_check.Show(is_srt)
        self.disclaimer_check.Show(is_srt)
        self.Layout()

class VideoSRTProgressDialog(wx.Dialog):
    def __init__(self, parent, regenerate_cb=None, original_path=None):
        # Translators: Title of the progress dialog when generating SRT
        title = _("{name} - Generating Audio Description").format(name=ADDON_NAME)
        super().__init__(parent, title=title, size=(550, 480), style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.srt_content = None
        self.abort = False
        self.regenerate_cb = regenerate_cb
        self.original_path = original_path
        self.file_uri = None
        self.is_srt_done = False
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Translators: Label for the status log text box
        lbl = wx.StaticText(self, label=_("Process Status / Subtitle Content:"))
        sizer.Add(lbl, 0, wx.ALL, 10)
        self.txt_status = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        sizer.Add(self.txt_status, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        hbox_voice = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Label for selecting the offline Windows TTS voice
        self.lbl_voice = wx.StaticText(self, label=_("Offline Narration Voice:"))
        hbox_voice.Add(self.lbl_voice, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.voice_sel = wx.Choice(self, choices=[])
        self.voice_sel.Bind(wx.EVT_CHOICE, self.on_voice_change)
        hbox_voice.Add(self.voice_sel, 1, wx.EXPAND)
        self.voice_sel.Disable()
        sizer.Add(hbox_voice, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.hbox_variant = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Label for selecting the eSpeak voice variant
        self.lbl_variant = wx.StaticText(self, label=_("eSpeak Voice Variant:"))
        self.hbox_variant.Add(self.lbl_variant, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        
        self.espeak_variant_sel = wx.ComboBox(self, style=wx.TE_PROCESS_ENTER)
        self.espeak_variant_sel.Bind(wx.EVT_TEXT, self.onModelFilter)
        for vname, vid in self._get_espeak_variants():
            self.espeak_variant_sel.Append(vname, vid)
        if self.espeak_variant_sel.GetCount() > 0:
            self.espeak_variant_sel.SetSelection(0)
            
        self.hbox_variant.Add(self.espeak_variant_sel, 1, wx.EXPAND)
        
        # Translators: Button to download missing eSpeak-NG
        self.btn_download_espeak = wx.Button(self, label=_("Download eSpeak-NG"))
        self.btn_download_espeak.Bind(wx.EVT_BUTTON, self.on_download_espeak)
        self.hbox_variant.Add(self.btn_download_espeak, 1, wx.EXPAND)
        
        sizer.Add(self.hbox_variant, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.lbl_variant.Show(False)
        self.espeak_variant_sel.Show(False)
        self.btn_download_espeak.Show(False)
        self.espeak_variant_sel.Disable()
        self.btn_download_espeak.Disable()

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Translators: Button to save the generated SRT file
        self.btn_save = wx.Button(self, label=_("&Save SRT"))
        self.btn_save.Disable()
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)

        # Translators: Button to generate a synced MP3 narration using offline TTS
        self.btn_generate_mp3 = wx.Button(self, label=_("&Generate Synced Narration (MP3)"))
        self.btn_generate_mp3.Disable()
        self.btn_generate_mp3.Bind(wx.EVT_BUTTON, self.on_generate_mp3)

        # Translators: Button to regenerate the audio description
        self.btn_regenerate = wx.Button(self, label=_("&Regenerate"))
        self.btn_regenerate.Disable()
        self.btn_regenerate.Bind(wx.EVT_BUTTON, self.on_regenerate)

        # Translators: Button to close the dialog
        self.btn_close = wx.Button(self, wx.ID_CANCEL, label=_("&Close / Cancel"))
        self.btn_close.Bind(wx.EVT_BUTTON, self.on_close)

        btn_sizer.Add(self.btn_save, 0, wx.RIGHT, 5)
        btn_sizer.Add(self.btn_generate_mp3, 0, wx.RIGHT, 5)
        btn_sizer.Add(self.btn_regenerate, 0, wx.RIGHT, 5)
        btn_sizer.Add(self.btn_close, 0)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        self.SetSizer(sizer)
        self.CenterOnParent()
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Translators: Initial status message in the text box
        self.update_status(_("Initializing..."))
        self.txt_status.SetFocus()
        
        threading.Thread(target=self._load_offline_voices, daemon=True).start()

    def _get_espeak_variants(self):
        espeak_dir = os.path.join(lib_dir, "espeak-ng", "espeak-ng-data", "voices", "!v")
        variants = []
        
        if os.path.exists(espeak_dir):
            try:
                for f in sorted(os.listdir(espeak_dir)):
                    file_path = os.path.join(espeak_dir, f)
                    if os.path.isfile(file_path) and not f.startswith('.'):
                        vid = f
                        vname = vid.capitalize()
                        
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                                for line in file:
                                    line_clean = line.strip()
                                    if line_clean.lower().startswith("name "):
                                        extracted_name = line_clean[5:].strip()
                                        if extracted_name:
                                            vname = extracted_name.capitalize()
                                            break
                        except Exception:
                            pass
                            
                        variants.append((vname, vid))
            except Exception as e:
                log.error(f"Failed to dynamically parse espeak variants: {e}")
                
        return variants

    def _update_variant_visibility(self):
        sel = self.voice_sel.GetSelection()
        if sel != wx.NOT_FOUND:
            voice_id = self.voice_sel.GetClientData(sel)
            is_espeak = str(voice_id).startswith("espeak")
            
            if is_espeak:
                exe_path = os.path.join(lib_dir, "espeak-ng", "espeak-ng.exe")
                if os.path.exists(exe_path):
                    self.lbl_variant.Show(True)
                    self.btn_download_espeak.Show(False)
                    self.espeak_variant_sel.Show(True)
                    
                    current_vid = None
                    variants = self._get_espeak_variants()
                    
                    if self.espeak_variant_sel.GetCount() == 0:
                        for vname, vid in variants:
                            self.espeak_variant_sel.Append(vname, vid)
                    
                    is_first_run = not hasattr(self, "_first_variant_run")
                    if is_first_run:
                        self._first_variant_run = False
                        
                    if not is_first_run:
                        v_sel = self.espeak_variant_sel.GetSelection()
                        if v_sel != wx.NOT_FOUND and v_sel < len(variants):
                            current_vid = variants[v_sel][1]
                    
                    if not current_vid:
                        try:
                            import synthDriverHandler
                            synth = synthDriverHandler.getSynth()
                            if synth.name == "espeak":
                                current_vid = getattr(synth, "variant", "max")
                            else:
                                current_vid = "max"
                        except Exception:
                            current_vid = "max"
                            
                    match_idx = 0
                    for i, (vname, vid) in enumerate(variants):
                        if vid == current_vid:
                            match_idx = i
                            break
                            
                    if self.espeak_variant_sel.GetCount() > 0:
                        self.espeak_variant_sel.SetSelection(match_idx)
                        
                    if self.is_srt_done:
                        self.espeak_variant_sel.Enable()
                        self.btn_generate_mp3.Enable()
                    else:
                        self.espeak_variant_sel.Disable()
                        self.btn_generate_mp3.Disable()
                else:
                    self.lbl_variant.Show(False)
                    self.espeak_variant_sel.Show(False)
                    self.btn_download_espeak.Show(True)
                    self.btn_generate_mp3.Disable()
                    if self.is_srt_done:
                        self.btn_download_espeak.Enable()
                    else:
                        self.btn_download_espeak.Disable()
            else:
                self.lbl_variant.Show(False)
                self.espeak_variant_sel.Show(False)
                self.btn_download_espeak.Show(False)
                if self.is_srt_done:
                    self.btn_generate_mp3.Enable()
                else:
                    self.btn_generate_mp3.Disable()
            self.Layout()

    def onModelFilter(self, event):
        cb = event.GetEventObject()
        if cb.IsFrozen(): return
        
        sel = cb.GetSelection()
        if sel != wx.NOT_FOUND: return

        query = cb.GetValue()
        query_low = query.lower()
        
        if not hasattr(cb, '_all_models_backup') and cb.GetCount() > 0:
            cb._all_models_backup = [(cb.GetString(i), cb.GetClientData(i)) for i in range(cb.GetCount())]
            
        backup = getattr(cb, '_all_models_backup', [])
        
        if not query_low:
            if cb.GetCount() != len(backup):
                cb.Freeze()
                cb.Clear()
                for name, data in backup:
                    cb.Append(name, data)
                cb.SetValue("")
                cb.Thaw()
            return

        filtered = [(name, data) for name, data in backup if query_low in name.lower()]
        
        cb.Freeze()
        cb.Clear()
        for name, data in filtered:
            cb.Append(name, data)
        
        cb.ChangeValue(query) 
        cb.SetInsertionPointEnd()
        cb.Thaw()
        
        if filtered:
            cb.Popup()


    def _generate_espeak_wav(self, text, voice_id, espeak_variant, output_wav):
        espeak_exe = os.path.join(lib_dir, "espeak-ng", "espeak-ng.exe")
        if not os.path.exists(espeak_exe):
            return False

        espeak_voice = "en"
        if voice_id.startswith("espeak_") and voice_id != "espeak_current":
            espeak_voice = voice_id.split("_")[1]

        espeak_speed = "175"
        espeak_pitch = "50"
        espeak_volume = "100"
        espeak_inflection = "75"

        if voice_id == "espeak_current":
            try:
                import synthDriverHandler
                synth = synthDriverHandler.getSynth()
                if synth.name == "espeak":
                    v = getattr(synth, "voice", "en")
                    if '\\' in v:
                        v = v.split('\\')[-1]
                    espeak_voice = v
                    
                    nvda_rate = getattr(synth, "rate", 50)
                    espeak_speed = str(int(80 + (nvda_rate / 100.0) * 370))
                    
                    nvda_pitch = getattr(synth, "pitch", 50)
                    espeak_pitch = str(int(nvda_pitch))
                    
                    nvda_volume = getattr(synth, "volume", 100)
                    espeak_volume = str(int((nvda_volume / 100.0) * 200))
                    nvda_inflection = getattr(synth, "inflection", 75)
                    espeak_inflection = str(int(nvda_inflection))
            except Exception:
                pass

        ssml_text = f'<speak><prosody range="{espeak_inflection}">{text}</prosody></speak>'

        if espeak_variant:
            espeak_voice = espeak_voice.split('+')[0]
            espeak_voice += f"+{espeak_variant}"

        try:
            subprocess.run(
                [
                    espeak_exe, 
                    "-v", espeak_voice,
                    "-s", espeak_speed,
                    "-p", espeak_pitch,
                    "-a", espeak_volume,
                    "-m",
                    "--stdin",
                    "-w", output_wav,
                ],
                input=ssml_text.encode('utf-8'),
                capture_output=True,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
            )
            return os.path.exists(output_wav) and os.path.getsize(output_wav) > 44
        except Exception as e:
            log.error(f"eSpeak generation failed: {e}")
            return False

    def on_voice_change(self, event):
        self._update_variant_visibility()



    def on_download_espeak(self, event):
        threading.Thread(target=self._download_espeak_worker, daemon=True).start()

    def _download_espeak_worker(self):
        espeak_dir = os.path.join(lib_dir, "espeak-ng")
        exe_path = os.path.join(espeak_dir, "espeak-ng.exe")
        wx.CallAfter(self.btn_download_espeak.Disable)
        try:
            # Translators: Status message when downloading eSpeak-NG
            wx.CallAfter(self.update_status, _("Downloading eSpeak-NG, please wait..."))
            download_url = "https://raw.githubusercontent.com/mahmoodhozhabri/VisionAssistantPro/main/eSpeak-NG-portable.zip"
            
            opener = get_proxy_opener(download_url)
            req = request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
            zip_path = os.path.join(lib_dir, "espeak-temp.zip")
            
            with opener.open(req, timeout=300) as response:
                with open(zip_path, 'wb') as f:
                    shutil.copyfileobj(response, f)
            
            # Translators: Status message when extracting eSpeak-NG
            wx.CallAfter(self.update_status, _("Extracting eSpeak-NG..."))
            os.makedirs(espeak_dir, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(espeak_dir)
            try: os.remove(zip_path)
            except Exception: pass
            
            if os.path.exists(exe_path):
                # Translators: Success message after eSpeak-NG download completes
                wx.CallAfter(self.update_status, _("eSpeak-NG downloaded successfully!"))
                if self.is_srt_done:
                    wx.CallAfter(self.update_status, self.srt_content)
                wx.CallAfter(self._update_variant_visibility)
        except Exception as e:
            log.error(f"eSpeak download failed: {e}", exc_info=True)
            # Translators: Error message when eSpeak-NG download fails
            wx.CallAfter(show_error_dialog, _("Failed to download eSpeak-NG: {error}").format(error=str(e)))
            wx.CallAfter(self.btn_download_espeak.Enable)

    def _load_offline_voices(self):
        try:
            voice_list = []
            target_selection = None
            
            try:
                import synthDriverHandler
                synth = synthDriverHandler.getSynth()
                synth_name = getattr(synth, "name", "")
                current_nvda_voice = getattr(synth, "voice", "")
            except Exception:
                synth_name = ""
                current_nvda_voice = ""

            if synth_name == "espeak":
                # Translators: Option for eSpeak voice matching the user's current NVDA voice settings
                voice_list.append(("espeak_current", _("eSpeak (Current NVDA Language)")))
                target_selection = "espeak_current"
            else:
                # Translators: Option for default English eSpeak voice
                voice_list.append(("espeak_en", _("eSpeak (English Default)")))
                
            try:
                import comtypes.client
                engine = comtypes.client.CreateObject("SAPI.SpVoice")
                voices = engine.GetVoices()
                for i in range(voices.Count):
                    voice = voices.Item(i)
                    desc = voice.GetDescription()
                    vid = f"sapi5_{voice.Id}"
                    voice_list.append((vid, f"SAPI5 - {desc}"))
                    
                    if synth_name == "sapi5" and current_nvda_voice == voice.Id:
                        target_selection = vid
            except Exception as e:
                log.error(f"SAPI5 load failed: {e}")

            wx.CallAfter(self._populate_voices, voice_list, target_selection)
        except Exception as e:
            log.error(f"Failed to load offline voices: {e}", exc_info=True)

    def _populate_voices(self, voice_list, target_selection):
        try:
            self.voice_sel.Clear()
            for vid, vname in voice_list:
                self.voice_sel.Append(vname, vid)
                
            if target_selection:
                for i in range(self.voice_sel.GetCount()):
                    if self.voice_sel.GetClientData(i) == target_selection:
                        self.voice_sel.SetSelection(i)
                        self._update_variant_visibility()
                        return
                        
            if self.voice_sel.GetCount() > 0:
                self.voice_sel.SetSelection(0)
                self._update_variant_visibility()
        except Exception:
            pass
        finally:
            if self.is_srt_done:
                self.voice_sel.Enable()

    def update_status(self, msg):
        if self.abort: return
        self.txt_status.SetValue(msg)
        if _vision_assistant_instance:
            _vision_assistant_instance.current_status = msg
        ui.message(msg)

    def on_finished(self, srt_content):
        if self.abort: return
        self.srt_content = srt_content
        self.is_srt_done = True
        self.txt_status.SetValue(srt_content)
        self.btn_save.Enable()
        self.btn_regenerate.Enable()
        self.btn_generate_mp3.Enable()
        self.voice_sel.Enable()
        self._update_variant_visibility()
        self.txt_status.SetFocus()
        tones.beep(1000, 100)
        # Translators: Success announcement when generation is complete
        ui.message(_("Audio description generated successfully! You can read the subtitle content in the text box."))

    def on_error(self, err_msg):
        if self.abort: return
        self.is_srt_done = True
        # Translators: Status message when an error occurs during SRT generation
        self.update_status(_("Error: {err}").format(err=err_msg))
        self.btn_regenerate.Enable()
        self.btn_generate_mp3.Disable()
        self.voice_sel.Enable()
        self._update_variant_visibility()

    def on_regenerate(self, event):
        self.srt_content = None
        self.abort = False
        self.is_srt_done = False
        self.btn_save.Disable()
        self.btn_regenerate.Disable()
        self.btn_generate_mp3.Disable()
        self.voice_sel.Disable()
        self.espeak_variant_sel.Disable()
        self.btn_download_espeak.Disable()
        # Translators: Status message when restarting generation
        self.update_status(_("Re-initializing..."))
        if self.regenerate_cb:
            self.regenerate_cb(self)

    def on_save(self, event):
        if not self.srt_content: return
        
        default_name = "Audio_Description.srt"
        if getattr(self, "original_path", None):
            if str(self.original_path).startswith("http"):
                default_name = "Online_Video_Description.srt"
            else:
                default_name = os.path.splitext(os.path.basename(self.original_path))[0] + ".srt"

        gui.mainFrame.prePopup()
        try:
            # Translators: File dialog title for saving the generated SRT file
            with wx.FileDialog(gui.mainFrame, _("Save Audio Description"), wildcard="SRT Files (*.srt)|*.srt", defaultFile=default_name, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    path = dlg.GetPath()
                else:
                    path = None
        finally:
            gui.mainFrame.postPopup()
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.srt_content)
                # Translators: Success message when SRT file is saved
                ui.message(_("SRT file saved successfully."))
            except Exception as e:
                show_error_dialog(str(e))

    def _parse_srt(self, srt_text):
        blocks = []
        parts = re.split(r'\n\s*\n', srt_text.strip())
        for part in parts:
            lines = [l.strip() for l in part.strip().split('\n') if l.strip()]
            if len(lines) < 3:
                continue
            time_line = lines[1]
            if '-->' not in time_line:
                continue
            try:
                start_str, end_str = [t.strip() for t in time_line.split('-->')]
                start_ms = self._time_to_ms(start_str)
                end_ms = self._time_to_ms(end_str)
                text = ' '.join(lines[2:])
                blocks.append({'start_ms': start_ms, 'end_ms': end_ms, 'text': text})
            except Exception:
                continue
        return blocks

    def _time_to_ms(self, t):
        h, m, rest = t.replace(',', '.').split(':')
        s, ms = rest.split('.')
        return int(h) * 3600000 + int(m) * 60000 + int(s) * 1000 + int(ms.ljust(3, '0')[:3])

    def _get_wav_duration(self, wav_path):
        try:
            with wave.open(wav_path, 'rb') as wf:
                return wf.getnframes() / wf.getframerate()
        except Exception:
            return 0.0

    def _generate_sapi5_wav(self, text, real_voice_id, output_wav):
        try:
            import comtypes.client
            engine = comtypes.client.CreateObject("SAPI.SpVoice")
            voices = engine.GetVoices()
            for i in range(voices.Count):
                if voices.Item(i).Id == real_voice_id:
                    engine.Voice = voices.Item(i)
                    break
            
            stream = comtypes.client.CreateObject("SAPI.SpFileStream")
            stream.Open(output_wav, 3)
            engine.AudioOutputStream = stream
            engine.Speak(text)
            stream.Close()
            return os.path.exists(output_wav) and os.path.getsize(output_wav) > 44
        except Exception as e:
            log.error(f"SAPI5 TTS to WAV failed: {e}")
            return False

    def on_generate_mp3(self, event):
        if not self.srt_content:
            return
        blocks = self._parse_srt(self.srt_content)
        if not blocks:
            # Translators: Error when SRT parsing finds no valid subtitle blocks
            show_error_dialog(_("No valid subtitle blocks found in the SRT content."))
            return

        ffmpeg_path = None
        if _vision_assistant_instance:
            ffmpeg_path = _vision_assistant_instance._ensure_ffmpeg()
        if not ffmpeg_path:
            return

        sel = self.voice_sel.GetSelection()
        if sel == wx.NOT_FOUND:
            # Translators: Error when no voice is selected
            show_error_dialog(_("Please select an offline voice from the list."))
            return
            
        voice_id = self.voice_sel.GetClientData(sel)
        
        espeak_variant = ""
        if str(voice_id).startswith("espeak"):
            v_sel = self.espeak_variant_sel.GetSelection()
            if v_sel != wx.NOT_FOUND:
                espeak_variant = self.espeak_variant_sel.GetClientData(v_sel)

        default_name = "Audio_Narration.mp3"
        video_path = None
        
        if hasattr(self, "local_path") and self.local_path and os.path.exists(self.local_path):
            video_path = self.local_path
        elif hasattr(self, "original_path") and self.original_path and os.path.exists(self.original_path):
            video_path = self.original_path

        has_video = bool(video_path)

        if not has_video:
            default_name = "Online_Video_Narration.mp3"
            is_online = True
        else:
            if getattr(self, "original_path", None) and not str(self.original_path).startswith("http"):
                default_name = os.path.splitext(os.path.basename(self.original_path))[0] + "_narration.mp3"
            else:
                default_name = "Audio_Narration.mp3"
            is_online = False

        mode_selection = 0
        apply_ducking = False

        if is_online:
            gui.mainFrame.prePopup()
            try:
                # Translators: Warning prompt for online videos indicating that the output will only contain narration.
                warn_msg = _("Because the source is an online video, the final file will ONLY contain the AI voice narration (synced to the timestamps) and will NOT include the original background audio of the video. Do you want to proceed?")
                # Translators: Title of the warning dialog when opening an online video link.
                with wx.MessageDialog(self, warn_msg, _("Online Video Mode"), wx.YES_NO | wx.ICON_WARNING) as dlg:
                    if dlg.ShowModal() != wx.ID_YES:
                        return
            finally:
                gui.mainFrame.postPopup()
        else:
            # Translators: Title of the narration mode selection dialog.
            title_dlg = _("Select Narration Mode")
            # Translators: Instruction prompt for narration mode selection.
            msg_dlg = _("Choose how the narration should be mixed with the video audio:")
            choices_dlg = [
                # Translators: Option for mixing voice directly over the video without pausing.
                _("Standard AD (Mix voice directly over audio - No Pausing)"),
                # Translators: Option for pausing the background video audio during descriptions.
                _("Extended AD (Pause background audio during descriptions)")
            ]
            
            gui.mainFrame.prePopup()
            try:
                with wx.SingleChoiceDialog(self, msg_dlg, title_dlg, choices_dlg) as dlg:
                    if dlg.ShowModal() != wx.ID_OK:
                        return
                    mode_selection = dlg.GetSelection()
            finally:
                gui.mainFrame.postPopup()

            if mode_selection == 0:
                gui.mainFrame.prePopup()
                try:
                    # Translators: Prompt asking whether to lower the background video audio during the descriptions.
                    duck_msg = _("Do you want to fade/duck the background video audio during the descriptions?")
                    # Translators: Title for the audio ducking prompt.
                    duck_title = _("Audio Ducking")
                    with wx.MessageDialog(self, duck_msg, duck_title, wx.YES_NO | wx.ICON_QUESTION) as dlg:
                        if dlg.ShowModal() == wx.ID_YES:
                            apply_ducking = True
                finally:
                    gui.mainFrame.postPopup()

        gui.mainFrame.prePopup()
        try:
            # Translators: File dialog title for saving audio narration
            with wx.FileDialog(
                gui.mainFrame,
                # Translators: Button label or menu item to save the generated AI audio narration synced to the video.
                _("Save Synced Narration"),
                wildcard="MP3 Files (*.mp3)|*.mp3",
                defaultFile=default_name,
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            ) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    output_path = dlg.GetPath()
                else:
                    output_path = None
        finally:
            gui.mainFrame.postPopup()

        if not output_path:
            return
        if not output_path.lower().endswith('.mp3'):
            output_path += '.mp3'

        self.btn_generate_mp3.Disable()
        self.btn_regenerate.Disable()
        self.btn_save.Disable()
        self.voice_sel.Disable()
        self.espeak_variant_sel.Disable()
        self.btn_download_espeak.Disable()
        
        # Translators: Status message when narration generation starts
        ui.message(_("Generating offline synced narration. This may take a few moments..."))
        threading.Thread(target=self._offline_tts_worker, args=(blocks, output_path, voice_id, espeak_variant, ffmpeg_path, video_path, mode_selection, apply_ducking), daemon=True).start()

    def _detect_silences(self, ffmpeg_path, video_path, noise_db=-32, duration_sec=0.3):
        startupinfo = None
        creationflags = 0
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            creationflags = 0x08000000

        vol_cmd = [
            ffmpeg_path, "-y", "-i", video_path, "-vn",
            "-af", "volumedetect", "-f", "null", "-"
        ]
        vol_res = subprocess.run(vol_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, creationflags=creationflags)
        vol_stderr = vol_res.stderr.decode('utf-8', errors='ignore')
        
        mean_volume = -20.0
        for line in vol_stderr.splitlines():
            if "mean_volume:" in line:
                try:
                    mean_volume = float(line.split("mean_volume:")[1].strip().split()[0])
                except Exception:
                    pass
                break
        
        dynamic_noise_db = max(-50.0, min(-20.0, mean_volume - 15.0))

        cmd = [
            ffmpeg_path, "-y", "-i", video_path, "-vn",
            "-af", f"highpass=f=200,lowpass=f=3000,afftdn,silencedetect=noise={dynamic_noise_db:.1f}dB:d={duration_sec}",
            "-f", "null", "-"
        ]

        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, creationflags=creationflags)
        stderr_data = res.stderr.decode('utf-8', errors='ignore')
        
        silences = []
        current_start = None
        
        for line in stderr_data.splitlines():
            if "silence_start:" in line:
                try:
                    val = line.split("silence_start:")[1].strip().split()[0]
                    current_start = int(float(val) * 1000)
                except Exception:
                    pass
            elif "silence_end:" in line:
                if current_start is not None:
                    try:
                        val = line.split("silence_end:")[1].strip().split("|")[0].strip().split()[0]
                        end_ms = int(float(val) * 1000)
                        silences.append((current_start, end_ms))
                    except Exception:
                        pass
                    current_start = None
        return silences

    def _find_best_pause_time(self, target_ms, silences, max_shift_ms=3000):
        if not silences:
            return target_ms

        for start, end in silences:
            if start <= target_ms <= end:
                return (start + end) // 2
        
        best_time = target_ms
        min_diff = float('inf')
        
        for start, end in silences:
            midpoint = (start + end) // 2
            
            if target_ms < start:
                dist = start - target_ms
            elif target_ms > end:
                dist = target_ms - end
            else:
                dist = 0
                
            if dist < min_diff and dist <= max_shift_ms:
                min_diff = dist
                best_time = midpoint
                
        return best_time

    def _offline_tts_worker(self, blocks, output_path, voice_id, espeak_variant, ffmpeg_path, video_path, mode_selection, apply_ducking=False):
        temp_dir = tempfile.mkdtemp()
        try:
            import comtypes
            try:
                comtypes.CoInitialize()
            except Exception:
                pass
        except ImportError:
            pass

        try:
            has_video = False
            if video_path and os.path.exists(video_path):
                has_video = True
            else:
                video_path = None
                mode_selection = 0

            orig_audio_wav = os.path.join(temp_dir, "original_audio.wav")
            orig_bytes = None
            total_orig_ms = 0
            silences = []

            if has_video:
                # Translators: Status message shown when extracting the original video audio tracks.
                wx.CallAfter(self.update_status, _("Extracting original video audio..."))
                
                subprocess.run(
                    [
                        ffmpeg_path, "-y", 
                        "-i", video_path, 
                        "-vn", 
                        "-acodec", "pcm_s16le", 
                        "-ar", "24000", 
                        "-ac", "1", 
                        orig_audio_wav
                    ],
                    capture_output=True,
                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
                )

                if not os.path.exists(orig_audio_wav):
                    # Translators: Error message shown when extraction of the video's original audio fails.
                    wx.CallAfter(show_error_dialog, _("Failed to extract video audio."))
                    return

                with wave.open(orig_audio_wav, "rb") as wf:
                    orig_bytes = wf.readframes(wf.getnframes())
                    total_orig_ms = int((len(orig_bytes) / 48))

                if mode_selection == 1:
                    # Translators: Status message shown when analyzing the video's audio to detect periods of silence.
                    wx.CallAfter(self.update_status, _("Analyzing video for natural silences..."))
                    silences = self._detect_silences(ffmpeg_path, video_path, noise_db=-32, duration_sec=0.3)
            else:
                total_orig_ms = blocks[-1]['end_ms'] + 2000

            for i, block in enumerate(blocks):
                if self.abort: return
                text = block['text'].replace('*', '').replace('_', '')
                if not text.strip(): continue
                
                # Translators: Progress message during narration generation. {current} is the current block number, {total} is total blocks.
                progress_msg = _("Generating narration: part {current} of {total}...").format(current=i + 1, total=len(blocks))
                wx.CallAfter(self.update_status, progress_msg)

                wav_path = os.path.join(temp_dir, f"block_{i:04d}.wav")
                success = False
                
                if str(voice_id).startswith("espeak_"):
                    success = self._generate_espeak_wav(text, voice_id, espeak_variant, wav_path)
                elif str(voice_id).startswith("sapi5_"):
                    real_id = voice_id[6:] 
                    success = self._generate_sapi5_wav(text, real_id, wav_path)
                
                if success:
                    resampled_wav = os.path.join(temp_dir, f"block_{i:04d}_r.wav")
                    subprocess.run(
                        [
                            ffmpeg_path, "-y",
                            "-i", wav_path,
                            "-ar", "24000",
                            "-ac", "1",
                            "-c:a", "pcm_s16le",
                            resampled_wav
                        ],
                        capture_output=True,
                        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
                    )
                    if os.path.exists(resampled_wav):
                        block['wav_path'] = resampled_wav
                    else:
                        block['wav_path'] = wav_path
                else:
                    block['wav_path'] = None

            final_wav_path = os.path.join(temp_dir, "final_mix.wav")

            if mode_selection == 0:
                # Translators: Status message when combining audio blocks
                wx.CallAfter(self.update_status, _("Arranging audio track... Please wait."))
                
                tts_base_path = os.path.join(temp_dir, "tts_base.wav")
                final_end_s = total_orig_ms / 1000.0
                subprocess.run(
                    [
                        ffmpeg_path, "-y", "-f", "lavfi", "-t", str(final_end_s),
                        "-i", "anullsrc=r=24000:cl=mono", "-ar", "24000", "-ac", "1", tts_base_path
                    ],
                    capture_output=True,
                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
                )

                wav_entries = []
                last_end_ms = 0
                for i, block in enumerate(blocks):
                    w_path = block.get('wav_path')
                    if w_path and os.path.exists(w_path):
                        try:
                            with wave.open(w_path, 'rb') as wf:
                                dur_ms = int((wf.getnframes() / wf.getframerate()) * 1000)
                        except Exception:
                            dur_ms = 0
                            
                        start_ms = int(block['start_ms'])
                        if start_ms < last_end_ms:
                            start_ms = last_end_ms + 150
                            
                        wav_entries.append({
                            'path': w_path,
                            'start_ms': start_ms
                        })
                        last_end_ms = start_ms + dur_ms

                current_tts_mix = tts_base_path
                batch_size = 40
                for batch_start in range(0, len(wav_entries), batch_size):
                    batch = wav_entries[batch_start:batch_start + batch_size]
                    batch_out = os.path.join(temp_dir, f"tts_mix_{batch_start}.wav")
                    
                    cmd = [ffmpeg_path, "-y", "-i", current_tts_mix]
                    filter_parts = []
                    
                    for idx, entry in enumerate(batch):
                        cmd.extend(["-i", entry['path']])
                        delay_ms = int(entry['start_ms'])
                        filter_parts.append(f"[{idx+1}:a]adelay={delay_ms}|{delay_ms}[a{idx+1}]")
                        
                    mix_inputs = "[0:a]" + "".join(f"[a{i+1}]" for i in range(len(batch)))
                    filter_parts.append(f"{mix_inputs}amix=inputs={len(batch)+1}:duration=longest:normalize=0[out]")
                    
                    cmd.extend(["-filter_complex", ";".join(filter_parts), "-map", "[out]", "-ar", "24000", "-ac", "1", batch_out])
                    subprocess.run(cmd, capture_output=True, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
                    current_tts_mix = batch_out

                if has_video:
                    # Translators: Status message when mixing generated narration with original video audio
                    wx.CallAfter(self.update_status, _("Mixing narration with original video audio..."))
                    
                    filter_complex = "[0:a][1:a]amix=inputs=2:duration=longest:normalize=0"
                    if apply_ducking:
                        filter_complex = "[1:a]asplit=2[sc][tts];[0:a][sc]sidechaincompress=threshold=0.05:ratio=5:attack=50:release=1000[bg];[bg][tts]amix=inputs=2:duration=longest:normalize=0"
                        
                    subprocess.run(
                        [
                            ffmpeg_path, "-y",
                            "-i", orig_audio_wav,
                            "-i", current_tts_mix,
                            "-filter_complex", filter_complex,
                            "-ar", "24000", "-ac", "1",
                            final_wav_path
                        ],
                        capture_output=True,
                        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
                    )
                else:
                    final_wav_path = current_tts_mix

            else:
                # Translators: Status message when slicing and splicing the audio file with natural pauses.
                wx.CallAfter(self.update_status, _("Splicing audio based on natural pauses..."))
                output_bytes = bytearray()
                last_copied_ms = 0

                for block in blocks:
                    if self.abort: return
                    if not block.get('wav_path') or not os.path.exists(block['wav_path']):
                        continue

                    raw_start_ms = block['start_ms']
                    smart_start_ms = self._find_best_pause_time(raw_start_ms, silences, max_shift_ms=3000)

                    if smart_start_ms > total_orig_ms:
                        smart_start_ms = total_orig_ms

                    if smart_start_ms > last_copied_ms:
                        chunk_bytes = orig_bytes[last_copied_ms * 48 : smart_start_ms * 48]
                        output_bytes.extend(chunk_bytes)
                        last_copied_ms = smart_start_ms

                    with wave.open(block['wav_path'], 'rb') as wf_block:
                        tts_frames = wf_block.readframes(wf_block.getnframes())
                        output_bytes.extend(tts_frames)

                if last_copied_ms < total_orig_ms:
                    remaining_bytes = orig_bytes[last_copied_ms * 48 :]
                    output_bytes.extend(remaining_bytes)

                with wave.open(final_wav_path, "wb") as wf_out:
                    wf_out.setnchannels(1)
                    wf_out.setsampwidth(2)
                    wf_out.setframerate(24000)
                    wf_out.writeframes(output_bytes)

            # Translators: Status message shown when converting the final raw WAV mix to MP3 format.
            wx.CallAfter(self.update_status, _("Converting final audio to MP3..."))
            subprocess.run(
                [
                    ffmpeg_path, "-y",
                    "-i", final_wav_path,
                    "-codec:a", "libmp3lame",
                    "-q:a", "2",
                    output_path
                ],
                capture_output=True,
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)
            )

            if os.path.exists(output_path):
                wx.CallAfter(self.update_status, self.srt_content)
                # Translators: Message spoken on successful save of the synced narration.
                ui.message(_("Synced extended narration with silence detection saved successfully."))
                # Translators: Success message shown when narration generation is successfully completed with silence detection.
                wx.CallAfter(wx.MessageBox, _("Synced extended audio narration file generated successfully with smart silence matching."), _("Success"), wx.OK | wx.ICON_INFORMATION)
            else:
                # Translators: Error message shown when the final MP3 conversion fails.
                wx.CallAfter(show_error_dialog, _("Failed to generate the final MP3 file."))

        except Exception as e:
            log.error(f"Synced narration insertion failed: {e}", exc_info=True)
            # Translators: Error message shown when narration generation fails.
            wx.CallAfter(show_error_dialog, _("Narration Error: {error}").format(error=e))
        finally:
            try:
                import comtypes
                comtypes.CoUninitialize()
            except Exception:
                pass
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception:
                pass
            wx.CallAfter(self.btn_generate_mp3.Enable)
            wx.CallAfter(self.btn_regenerate.Enable)
            wx.CallAfter(self.btn_save.Enable)
            wx.CallAfter(self.voice_sel.Enable)
            wx.CallAfter(self._update_variant_visibility)

    def on_close(self, event):
        self.abort = True
        if _vision_assistant_instance:
            # Translators: Status message when the addon is idle.
            _vision_assistant_instance.current_status = _("Idle")
        # Translators: Message announced when user cancels the process
        ui.message(_("Process cancelled."))
        self.Destroy()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    scriptCategory = ADDON_NAME
    
    last_translation = "" 
    is_recording = False
    temp_audio_file = os.path.join(tempfile.gettempdir(), "vision_dictate.wav")
    
    translation_cache = {}
    _last_source_text = None
    _last_params = None
    update_timer = None

    is_ui_explorer_active = False

    _operator_history = []
    _operator_context = {}

    current_status = _("Idle")

    def __init__(self):
        super(GlobalPlugin, self).__init__()
        global _vision_assistant_instance
        _vision_assistant_instance = self

            
        if not globalVars.appArgs.secure:
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SettingsPanel)
            self.updater = UpdateManager(GITHUB_REPO)
            self._is_operator_running = False
            self._abort_operator = False
            self._operator_thread_token = 0
            self._dialog_open = False
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
            
            # Translators: Menu item to open the Telegram channel
            item_telegram = self.va_menu.Append(wx.ID_ANY, _("Telegram &Channel"))
            self.va_menu.Bind(wx.EVT_MENU, self.on_telegram_click, item_telegram)
            
            self.tools_menu = gui.mainFrame.sysTrayIcon.toolsMenu
            # Translators: The name of the addon's sub-menu in the NVDA Tools menu.
            self.va_submenu_item = self.tools_menu.AppendSubMenu(self.va_menu, _("Vision Assistant"))
            
            if config.conf["VisionAssistant"]["check_update_startup"]:
                self.update_timer = wx.CallLater(10000, self.updater.check_for_updates, True)
        
        self.refine_dlg = None
        self.refine_menu_dlg = None
        self.vision_dlg = None
        self.doc_dlg = None
        self.doc_viewer_dlg = None
        self.translation_dlg = None
        self.toggling = False
        self._last_result_data = None
        self.live_session = None
        self.live_dlg = None

        self.is_video_recording = False
        self.recording_process = None
        self.recording_output_path = None
        self.recording_start_time = None

        self.labels_cache = {}
        if os.path.exists(LABELS_FILE):
            try:
                with open(LABELS_FILE, "r", encoding="utf-8") as f:
                    self.labels_cache = json.load(f)
            except Exception: pass

        self._ocr_task_running = {"smartfile": False, "document": False}
        self._ocr_abort = {"smartfile": False, "document": False}

    @staticmethod
    def _ocr_progress_key(context, paths):
        return context + "|" + "|".join(sorted(paths))

    def _stop_ocr_task(self, context):
        self._ocr_abort[context] = True
        self._ocr_task_running[context] = False
        self.current_status = _("Idle")
        # Translators: Announcement when an in-progress OCR extraction is stopped by the user.
        ui.message(_("OCR operation stopped."))
        tones.beep(300, 150)

    def _maybe_resume_ocr(self, context, paths):

        key = self._ocr_progress_key(context, paths)
        record = OCRProgressStore.load(key)
        if not record:
            return None

        total_pages = record.get("end", 0) - record.get("start", 0) + 1
        done_pages = min(len(record.get("pages", {})), total_pages)
        file_count = len(record.get("paths", paths))

        # Translators: Title of the dialog asking whether to resume an OCR operation that did not finish (for example after NVDA closed unexpectedly).
        title = _("Unfinished Operation")
        # Translators: Message asking whether to continue an interrupted OCR extraction. {done} is the number of pages already processed, {total} is the total number of pages, and {files} is the number of files involved.
        msg = _("You have an unfinished operation: {done} of {total} pages processed across {files} file(s). Would you like to continue from where it stopped?").format(done=done_pages, total=total_pages, files=file_count)

        result = {}
        done = threading.Event()

        def ask():
            try:
                result["yes"] = (gui.messageBox(msg, title, wx.YES_NO | wx.ICON_QUESTION) == wx.YES)
            finally:
                done.set()

        if wx.IsMainThread():
            ask()
        else:
            wx.CallAfter(ask)
            done.wait()

        if result.get("yes"):
            return record
        OCRProgressStore.clear(key)
        return None

    def _getFocusedExplorerFile(self):
        try:
            hwnd = api.getForegroundObject().windowHandle
            try:
                root_hwnd = winUser.getAncestor(hwnd, winUser.GA_ROOT)
            except Exception:
                root_hwnd = hwnd
            shell = comtypes.client.CreateObject("Shell.Application")
            windows = shell.Windows()
            for win in windows:
                try:
                    if win.HWND in (hwnd, root_hwnd):
                        selected = win.Document.SelectedItems()
                        if selected.Count > 0:
                            return [selected.Item(i).Path for i in range(selected.Count)]
                except Exception: continue
        except Exception: pass
        return []

    def _getClipboardImageFile(self):
        path = None
        if not wx.TheClipboard.Open():
            return None
        try:
            if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_BITMAP)):
                bmp_data = wx.BitmapDataObject()
                if wx.TheClipboard.GetData(bmp_data):
                    bmp = bmp_data.GetBitmap()
                    if bmp.IsOk():
                        fd, path = tempfile.mkstemp(suffix=".png")
                        os.close(fd)
                        if not bmp.SaveFile(path, wx.BITMAP_TYPE_PNG):
                            try: os.remove(path)
                            except Exception: pass
                            path = None
        except Exception as e:
            log.error(f"Clipboard image extraction failed: {e}")
            path = None
        finally:
            wx.TheClipboard.Close()
        return path

    def _browse_and_run(self, worker_fn, wildcard, multiple=False):
        # Translators: Standard title for opening a file
        title = _("Open")
        path = get_file_path(title, wildcard, multiple=multiple)
        if path:
            threading.Thread(target=worker_fn, args=(path,), daemon=True).start()


    def _open_document_reader(self):
        self._dialog_open = True
        # Translators: File dialog filter for supported files
        wc = _("Supported Files") + "|*.pdf;*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.heic;*.heif"
        self._browse_and_run(self._scan_and_open, wc, multiple=True)
        self._dialog_open = False

    def _scan_and_open(self, paths, resume=None):
        try:
            if not fitz:
                # Translators: Error when PyMuPDF is missing
                wx.CallAfter(wx.MessageBox, _("PyMuPDF library is missing."), "Error", wx.ICON_ERROR)
                return

            engine = config.conf["VisionAssistant"]["ocr_engine"]
            image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.heic', '.heif')
            has_images = any(p.lower().endswith(image_extensions) for p in paths)

            if engine == 'none' and has_images:
                # Translators: Error message shown when a user tries to use "None (Extract Text)" engine on image files.
                msg = _("The 'None (Extract Text Layer)' engine cannot process image-based content. Please change the OCR Engine to 'Chrome' or 'AI (Advanced)' in settings.")
                # Translators: Title of the error dialog shown when the selected OCR engine cannot process the chosen image-based files.
                wx.CallAfter(gui.messageBox, msg, _("OCR Engine Error"), wx.OK | wx.ICON_ERROR)
                return

            v_doc = VirtualDocument(paths)
            v_doc.scan()
            if v_doc.total_pages == 0:
                 # Translators: Error when no pages found
                 wx.CallAfter(wx.MessageBox, _("No readable pages found."), "Error", wx.ICON_ERROR)
                 return
            if resume is None:
                resume = self._maybe_resume_ocr("document", list(paths))
            if resume:
                settings = {'start': resume['start'], 'end': resume['end'], 'translate': resume['do_translate'], 'lang': resume['target_lang']}
                wx.CallAfter(lambda: self._open_document_viewer(v_doc, settings, resume))
            elif v_doc.total_pages == 1:
                settings = {'start': 0, 'end': 0, 'translate': False, 'lang': TARGET_NAMES[0]}
                wx.CallAfter(lambda: self._open_document_viewer(v_doc, settings))
            else:
                wx.CallAfter(self._show_range_dialog, v_doc)
        except Exception as e:
            log.error(f"Error opening files: {e}", exc_info=True)

    def _open_document_viewer(self, v_doc, settings, resume=None):
        self.doc_viewer_dlg = DocumentViewerDialog(gui.mainFrame, v_doc, settings, resume=resume)
        self.doc_viewer_dlg.Show()

    def _show_range_dialog(self, v_doc):
        gui.mainFrame.prePopup()
        try:
            range_dlg = RangeDialog(gui.mainFrame, v_doc.total_pages)
            if range_dlg.ShowModal() == wx.ID_OK:
                settings = range_dlg.get_settings()
                wx.CallAfter(lambda: self._open_document_viewer(v_doc, settings))
            range_dlg.Destroy()
        finally:
            gui.mainFrame.postPopup()

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
        if globalVars.appArgs.secure:
            return
            
        if self.toggling:
            self.script_error(gesture)
            return
        
        self.bindGestures(self.__VisionGestures)
        self.toggling = True
        tones.beep(500, 100)

    def terminate(self):
        global _vision_assistant_instance
        try:
            if not globalVars.appArgs.secure:
                if hasattr(self, 'va_submenu_item') and self.va_submenu_item:
                    self.tools_menu.Remove(self.va_submenu_item.GetId())
            
            gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SettingsPanel)
            
        except Exception: pass
        
        if hasattr(self, 'update_timer') and self.update_timer and self.update_timer.IsRunning():
            self.update_timer.Stop()

        self._abort_operator = True
        self._is_operator_running = False
        self._operator_thread_token = getattr(self, "_operator_thread_token", 0) + 1

        if self.live_session:
            try: self.live_session.stop()
            except Exception: pass
            self.live_session = None

        for dlg in [self.refine_dlg, self.refine_menu_dlg, self.vision_dlg, self.doc_dlg, self.doc_viewer_dlg, self.translation_dlg]:
            if dlg:
                try:
                    if getattr(dlg, "abort", None) is not None:
                        dlg.abort = True
                    dlg.Destroy()
                except Exception: pass
        
        if self.is_recording:
            try:
                ctypes.windll.winmm.mciSendStringW('close all', None, 0, 0)
            except Exception: pass
        
        self.translation_cache = {}
        self._last_source_text = None
        _vision_assistant_instance = None
        gc.collect()

    def report_status(self, msg):
        self.current_status = msg
        ui.message(msg)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Shows a list of available commands in the layer."))
    def script_showHelp(self, gesture):
        if self.toggling: self.finish()
    # Translators: Help text shown in a dialog listing all available commands in the Command Layer.
        help_msg = (
            "Shift+A: " + _("Asks the AI Operator to perform an action or describe the screen.") + "\n" +
            "E: " + _("Toggles the interactive UI elements explorer.") + "\n" +
            "T: " + _("Translates the selected text or navigator object.") + "\n" +
            "Shift+T: " + _("Translates the text currently in the clipboard.") + "\n" +
            "R: " + _("Opens a menu to Explain, Summarize, or Fix the selected text.") + "\n" +
            "O: " + _("Performs OCR and description on the entire screen.") + "\n" +
            "V: " + _("Describes the current object (Navigator Object).") + "\n" +
            "D: " + _("Opens the Document Reader for detailed page-by-page analysis (PDF/Images).") + "\n" +
            # Translators: Help message describing the F key shortcut in the Vision Assistant layer.
            "F: " + _("Performs smart actions (OCR or Description) on a selected image or PDF file.") + "\n" +
            "A: " + _("Transcribes a selected audio file.") + "\n" +
            # Translators: Help message describing the Shift+V key shortcut in the Vision Assistant layer.
            # Translators: Help message describing the Shift+V key shortcut in the Vision Assistant layer.
            "Shift+V: " + _("Analyzes a local video file or an online video URL.") + "\n" +
            "Control+V: " + _("Starts or stops local video recording of the screen.") + "\n" +
            "C: " + _("Attempts to solve a CAPTCHA on the screen or navigator object.") + "\n" +
            "S: " + _("Records voice, transcribes it using AI, and types the result.") + "\n" +
            "I: " + _("Announces the current status of the add-on.") + "\n" +
            "L: " + _("Labels the current navigator object using AI.") + "\n" +
            "Shift+L: " + _("Manages existing labels or scans the entire app to label unnamed elements.") + "\n" +
            "U: " + _("Checks for updates manually.") + "\n" +
            # Translators: Help message describing the Space key shortcut in the Vision Assistant layer.
            "Space: " + _("Shows the last AI response in a chat dialog for review or follow-up questions.") + "\n" +
            # Translators: Help message describing the H key shortcut in the Vision Assistant layer.
            "H: " + _("Shows a list of available commands in the layer.") + "\n" +
            "Control+L: " + _("Starts or ends a live voice conversation with the AI assistant.") + "\n" +
            # Translators: Help message describing the Alt+S key shortcut in the Vision Assistant layer.
            "Alt+S: " + _("Opens the Vision Assistant settings dialog.") + "\n" +
            # Translators: Help message describing the Alt+Q key shortcut in the Vision Assistant layer.
            "Alt+Q: " + _("Reports the number of banned Gemini API keys and their unban time.") + "\n" +
            # Translators: Help message describing the Alt+M key shortcut in the Vision Assistant layer.
            "Alt+M: " + _("Reports the AI models selected in advanced routing.")
        )
        # Translators: Title of the help dialog
        ui.browseableMessage(help_msg, _("{name} Help").format(name=ADDON_NAME))

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Announces the current status of the add-on."))
    def script_announceStatus(self, gesture):
        if self.toggling: self.finish()
        idle_msg = _("Idle")
        msg = self.current_status if self.current_status else idle_msg
        ui.message(msg)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Starts or ends a live voice conversation with the AI assistant."))
    def script_toggleLiveAssistant(self, gesture):
        if self.toggling: self.finish()
        if self.live_session:
            self._end_live_session()
            return
        if not AIHandler.is_gemini():
            # Translators: Error shown when the Live Assistant is used with a non-Gemini provider.
            show_error_dialog(_("The Live Assistant is only supported with the Gemini provider (or a Custom provider with API type set to Gemini)."))
            return
        self._start_live_session()

    # Translators: Script description for Input Gestures dialog.
    @scriptHandler.script(description=_("Opens the Vision Assistant settings dialog."))
    def script_openSettings(self, gesture):
        if self.toggling: self.finish()
        wx.CallAfter(self.on_settings_click, None)

    # Translators: Script description for Input Gestures dialog.
    @scriptHandler.script(description=_("Reports the number of Gemini API keys that have exceeded their daily quota and their reset time."))
    def script_reportQuotaExhaustedKeys(self, gesture):
        if self.toggling: self.finish()
        if not AIHandler.is_gemini():
            # Translators: Message shown when a user tries to check Gemini API quotas but another provider is active.
            wx.CallAfter(ui.message, _("This feature is only available for Google Gemini."))
            return
        try:
            import json
            banned_str = config.conf["VisionAssistant"].get("banned_gemini_keys", "{}")
            banned = json.loads(banned_str)
        except Exception:
            banned = {}
            
        import time
        now = time.time()
        
        unique_keys = {}
        max_time_per_key = {}
        
        for k_m, ban_time in list(banned.items()):
            if now < ban_time:
                parts = k_m.split("::")
                k = parts[0]
                m = parts[1] if len(parts) > 1 else "Unknown"
                if k not in unique_keys:
                    unique_keys[k] = []
                unique_keys[k].append(m)
                max_time_per_key[k] = max(max_time_per_key.get(k, 0), ban_time)
            else:
                del banned[k_m]
                
        config.conf["VisionAssistant"]["banned_gemini_keys"] = json.dumps(banned)
        
        if not unique_keys:
            # Translators: Message when no API keys are out of quota
            ui.message(_("No API keys have exceeded their daily quota."))
            return
            
        model_combinations = {}
        for k, models in unique_keys.items():
            models.sort()
            m_tuple = tuple(models)
            if m_tuple not in model_combinations:
                model_combinations[m_tuple] = []
            model_combinations[m_tuple].append(max_time_per_key[k])
            
        import datetime
        today = datetime.date.today()
        
        msg_parts = []
        for m_tuple, times in model_combinations.items():
            count = len(times)
            max_time = max(times)
            model_str = ", ".join(m_tuple)
            ban_date = datetime.datetime.fromtimestamp(max_time).date()
            time_str = time.strftime("%H:%M", time.localtime(max_time))
            if ban_date > today:
                # Translators: Prefix for time when the daily quota resets on the next day
                time_str = _("tomorrow at {time}").format(time=time_str)
            # Translators: Status message for API keys that are out of daily quota
            msg_parts.append(_("{count} key(s) exceeded daily quota for model {model} (resets around {time_str})").format(count=count, model=model_str, time_str=time_str))
            
        ui.message(". ".join(msg_parts))

    # Translators: Script description for Input Gestures dialog.
    @scriptHandler.script(description=_("Reports the AI models selected in advanced routing."))
    def script_reportSelectedModels(self, gesture):
        if self.toggling: self.finish()
        models = []
        conf = config.conf["VisionAssistant"]
        p = conf.get("active_provider", "gemini")
        
        m_key = "model_name" if p == "gemini" else f"{p}_model_name"
        main_m = conf.get(m_key, "")
        if main_m: 
            # Translators: Prefix for main model status
            models.append(_("Main: {model}").format(model=main_m))
        
        def add_adv(task, name):
            m = conf.get(f"{p}_{task}_model", "")
            if m and "Default" not in m and "Auto" not in m:
                models.append(f"{name}: {m}")
                
        # Translators: Status prefix for specific tasks
        add_adv("ocr", _("OCR"))
        # Translators: Abbreviation for Speech-to-Text.
        add_adv("stt", _("STT"))
        # Translators: Abbreviation for Text-to-Speech.
        add_adv("tts", _("TTS"))
        add_adv("operator", _("Operator"))
        add_adv("video", _("Video"))
        add_adv("live", _("Live"))
        
        if not models:
            # Translators: Message when no specific AI models are selected in advanced routing
            ui.message(_("No specific models selected."))
        else:
            ui.message(". ".join(models))

    def _start_live_session(self):
        if self.live_session or not AIHandler.is_gemini():
            return
        tones.beep(660, 120)
        direct = config.conf["VisionAssistant"]["live_direct_output"]
        self.live_session = LiveSession(
            on_text=lambda line: wx.CallAfter(self._live_append, line),
            on_status=lambda msg: wx.CallAfter(self._live_status, msg),
            on_closed=lambda: wx.CallAfter(self._live_on_closed),
            on_stream=lambda chunk: wx.CallAfter(self._live_stream, chunk),
        )
        if not direct:
            self._show_live_window()
        self._live_video_timer = wx.Timer(gui.mainFrame)
        gui.mainFrame.Bind(wx.EVT_TIMER, self._on_live_video_tick, self._live_video_timer)
        self._live_video_timer.Start(2000)
        threading.Thread(target=self._start_live_worker, daemon=True).start()

    def _show_live_window(self):
        if getattr(self, "live_dlg", None) and LiveAssistantDialog.instance is self.live_dlg:
            self.live_dlg.set_active(bool(self.live_session))
        else:
            self.live_dlg = LiveAssistantDialog(gui.mainFrame, self._start_live_session, self._end_live_session)
            self.live_dlg.set_active(bool(self.live_session))
            self.live_dlg.Show()
        self.live_dlg.Raise()
        self.live_dlg.history.SetFocus()

    def _on_live_video_tick(self, event):
        session = self.live_session
        if not session:
            return
        jpeg_b64, w, h, m = self._capture_fullscreen()
        if jpeg_b64:
            threading.Thread(target=session.send_video_frame, args=(jpeg_b64,), daemon=True).start()

    def _start_live_worker(self):
        session = self.live_session
        if session and not session.start():
            wx.CallAfter(self._live_on_closed)

    def _live_append(self, line):
        if getattr(self, "live_dlg", None):
            try: self.live_dlg.append_line(line)
            except Exception: pass

    def _live_stream(self, chunk):
        if getattr(self, "live_dlg", None):
            try: self.live_dlg.append_raw(chunk)
            except Exception: pass

    def _live_status(self, msg):
        if msg.startswith("ERROR:"):
            show_error_dialog(msg[6:])
            self._end_live_session()
        elif msg.startswith("STATUS:"):
            self.report_status(msg[7:])

    def _end_live_session(self):
        if self.live_session:
            try: self.live_session.stop()
            except Exception: pass

    def _live_on_closed(self):
        self.live_session = None
        if getattr(self, "_live_video_timer", None):
            try:
                self._live_video_timer.Stop()
                gui.mainFrame.Unbind(wx.EVT_TIMER, handler=self._on_live_video_tick, source=self._live_video_timer)
            except Exception: pass
            self._live_video_timer = None
        if getattr(self, "live_dlg", None) and LiveAssistantDialog.instance:
            try:
                self.live_dlg.set_active(False)
                # Translators: Line appended to the conversation when the live session has ended.
                self.live_dlg.append_line(_("--- Session ended ---"))
            except Exception: pass
        else:
            self.live_dlg = None
        tones.beep(440, 120)
        # Translators: Message announced by NVDA when the live voice conversation ends.
        self.report_status(_("Live conversation ended."))

    def _browse_file(self, wildcard):
        # Translators: Standard title for opening a file
        return get_file_path(_("Open"), wildcard)

    def _upload_file_to_gemini(self, file_path, mime_type, silent=False, abort_checker=None):
        p = config.conf["VisionAssistant"]["active_provider"]
        keys = AIHandler.get_keys(p)
        if not keys: return None
        
        if not AIHandler.is_gemini():
            url = AIHandler.get_endpoint("upload")
            boundary = "Boundary-" + uuid4().hex
            with open(file_path, "rb") as f:
                data = f.read()
            body = []
            body.append(f"--{boundary}".encode())
            body.append(f'Content-Disposition: form-data; name="purpose"'.encode())
            body.append(b'')
            body.append(b'ocr')
            body.append(f"--{boundary}".encode())
            body.append(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(file_path)}"' .encode())
            body.append(f'Content-Type: {mime_type}'.encode())
            body.append(b'')
            body.append(data)
            body.append(f"--{boundary}--".encode())
            body.append(b'')
            
            for key in keys:
                if abort_checker and abort_checker(): return None
                try:
                    req = request.Request(url, data=b'\r\n'.join(body), headers={"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
                    with get_proxy_opener().open(req, timeout=600) as r:
                        res = json.loads(r.read().decode())
                        return res.get("id") or res.get("name")
                except Exception: continue
            return None

        api_key = keys[GeminiHandler._working_key_idx % len(keys)]
        base_upload_url = AIHandler.get_endpoint("upload")
        try:
            file_size = os.path.getsize(file_path)
            headers_init = {"X-Goog-Upload-Protocol": "resumable", "X-Goog-Upload-Command": "start", "X-Goog-Upload-Header-Content-Length": str(file_size), "X-Goog-Upload-Header-Content-Type": mime_type, "Content-Type": "application/json", "x-goog-api-key": api_key}
            req_init = request.Request(base_upload_url, data=json.dumps({"file": {"display_name": os.path.basename(file_path)}}).encode(), headers=headers_init, method="POST")
            with get_proxy_opener().open(req_init, timeout=120) as r:
                upload_url = r.headers.get("x-goog-upload-url")
            
            if not upload_url or (abort_checker and abort_checker()): return None
            
            with open(file_path, 'rb') as f: data = f.read()
            req_up = request.Request(upload_url, data=data, headers={"Content-Length": str(file_size), "X-Goog-Upload-Offset": "0", "X-Goog-Upload-Command": "upload, finalize"}, method="POST")
            with get_proxy_opener().open(req_up, timeout=900) as r:
                res = json.loads(r.read().decode())
                file_name_id = res['file']['name']
            
            if abort_checker and abort_checker(): return None
            
            p_base = AIHandler.get_base_url(p)
            check_url = f"{p_base}/v1beta/{file_name_id}"
            
            for attempt in range(150):
                if abort_checker and abort_checker(): return None
                req_check = request.Request(check_url, headers={"x-goog-api-key": api_key})
                try:
                    with get_proxy_opener().open(req_check, timeout=30) as r:
                        data = json.loads(r.read().decode())
                        if data.get('state') == "ACTIVE":
                            uri = data.get('uri')
                            GeminiHandler._register_file_uri(uri, api_key)
                            
                            duration_sec = None
                            v_meta = data.get('videoMetadata') or data.get('video_metadata') or {}
                            dur_str = v_meta.get('videoDuration') or v_meta.get('video_duration') or v_meta.get('duration') or ''
                            if dur_str:
                                try:
                                    duration_sec = float(dur_str.rstrip('s'))
                                except Exception:
                                    pass
                            if duration_sec:
                                if not hasattr(GeminiHandler, '_file_durations'):
                                    GeminiHandler._file_durations = {}
                                GeminiHandler._file_durations[uri] = duration_sec
                                
                            return uri
                except Exception:
                    pass
                for step in range(4):
                    if abort_checker and abort_checker(): return None
                    time.sleep(0.5)
            return None
        except error.HTTPError as e:
            err_msg = GeminiHandler._handle_error(e)
            log.error(f"File upload HTTPError: {err_msg}")
            if hasattr(e, 'code') and e.code == 429:
                GeminiHandler._ban_key(api_key, getattr(e, 'is_daily', False), task=None)
            
            msg = _("File Upload Error: {error}").format(error=err_msg)
            self.report_status(msg)
            if not silent:
                show_error_dialog(msg)
            return None
        except Exception as e:
            # Translators: Message of a dialog which may pop up while performing an AI call
            msg = _("File Upload Error: {error}").format(error=e)
            self.report_status(msg)
            if not silent:
                show_error_dialog(msg)
            return None

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Records voice, transcribes it using AI, and types the result."))
    def script_smartDictation(self, gesture):
        if self.toggling: self.finish()
        if not self.is_recording:
            self.is_recording = True
            tones.beep(800, 100)
            try:
                ret_open = ctypes.windll.winmm.mciSendStringW('open new type waveaudio alias myaudio', None, 0, 0)
                if ret_open != 0:
                    self.is_recording = False
                    # Translators: Message in an error dialog which can pop up while trying dictation.
                    msg = _("Audio Hardware Error: {error}").format(error=f"MCI_OPEN_ERR_{ret_open}")
                    show_error_dialog(msg)
                    return
                
                ret_rec = ctypes.windll.winmm.mciSendStringW('record myaudio', None, 0, 0)
                if ret_rec != 0:
                    self.is_recording = False
                    ctypes.windll.winmm.mciSendStringW('close all', None, 0, 0)
                    # Translators: Message in an error dialog which can pop up while trying dictation.
                    msg = _("Audio Hardware Error: {error}").format(error=f"MCI_RECORD_ERR_{ret_rec}")
                    show_error_dialog(msg)
                    return

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
                    if os.path.exists(self.temp_audio_file):
                        try: os.remove(self.temp_audio_file)
                        except Exception: pass
                    return
            except Exception as e:
                log.debugWarning(f"Dictation duration check failed: {e}")

            with open(self.temp_audio_file, "rb") as f:
                audio_data = base64.b64encode(f.read()).decode('utf-8')
            
            dictation_template = get_prompt_text("dictation_transcribe") or (
                "Transcribe speech. Use native script. Fix stutters. If there is no speech, "
                "silence, or background noise only, write exactly: [[[NOSPEECH]]]"
            )
            p = apply_prompt_template(dictation_template, [("response_lang", get_lang_name("ai_response_language"))])
            
            res = AIHandler.call(p, attachments=[{'mime_type': 'audio/wav', 'data': audio_data}])
            
            if res:
                if res.startswith("ERROR:"):
                    log.error(f"Dictation AI call error: {res}")
                    wx.CallAfter(show_error_dialog, res[6:])
                    wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                elif "[[[NOSPEECH]]]" in res:
                    # Translators: Message reported when the AI detects silence or empty speech
                    msg = _("No speech detected.")
                    wx.CallAfter(self.report_status, msg)
                    wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                else:
                    cleaned_text = clean_markdown(res)
                    wx.CallAfter(self._paste_text, cleaned_text)
                    wx.CallAfter(setattr, self, 'current_status', _("Idle"))
            else: 
                log.error("Dictation: AI returned empty response")
                # Translators: Message reported while trying dictation.
                msg = _("No speech recognized or Error.")
                wx.CallAfter(self.report_status, msg)
                wx.CallAfter(setattr, self, 'current_status', _("Idle"))

            if os.path.exists(self.temp_audio_file):
                try: os.remove(self.temp_audio_file)
                except Exception: pass
        except Exception as e:
            log.error(f"Dictation thread failed: {e}", exc_info=True)
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))

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
        try:
            p_name = config.conf["VisionAssistant"]["active_provider"]
            t = get_lang_name("target_language")
            s = get_lang_name("source_language")
            swap = config.conf["VisionAssistant"]["smart_swap"]
            fallback = "English" if s == "Auto-detect" else s
            
            current_params = f"{p_name}|{t}|{swap}"
            if text == self._last_source_text and current_params == self._last_params and self.last_translation:
                wx.CallAfter(self._announce_translation, self.last_translation)
                return

            translation_template = get_prompt_text("translate_main")
            p = apply_prompt_template(translation_template,[("target_lang", t), ("swap_target", fallback), ("smart_swap", str(swap)), ("text_content", text)])
            
            res = AIHandler.call(p)
            if res:
                if res.startswith("ERROR:"):
                    log.error(f"Translation AI call error: {res}")
                    wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                    wx.CallAfter(show_error_dialog, res[6:])
                    return
                
                clean_res = clean_markdown(res)
                self._last_source_text = text
                self._last_params = current_params
                self.last_translation = clean_res
                wx.CallAfter(self._announce_translation, clean_res)
            
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))

        except Exception as e:
            log.error(f"Translation thread failed: {e}", exc_info=True)
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))

    def _announce_translation(self, text):
        # Translators: Message reported when calling translation command
        msg = _("Translated: {text}").format(text=text)
        self.report_status(msg)
        tones.beep(1000, 100)
        wx.CallAfter(self._open_translation_dialog, text)

    def _open_translation_dialog(self, text, force_show=False, is_recall=False):
        self._last_result_data = (self._open_translation_dialog, (text,))
        
        if config.conf["VisionAssistant"]["copy_to_clipboard"]:
            api.copyToClip(text)
            
        if config.conf["VisionAssistant"]["skip_chat_dialog"] and not force_show:
            return
            
        if self.translation_dlg:
            try: self.translation_dlg.Destroy()
            except Exception: pass
            self.translation_dlg = None

        def noop_callback(ctx, q, history, extra):
            return None, None

        self.translation_dlg = VisionQADialog(
            gui.mainFrame, 
            # Translators: Dialog title for Translation results
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
            except Exception: pass

        try:
            info = focus_obj.makeTextInfo(textInfos.POSITION_SELECTION)
            if info and info.text and not info.text.isspace():
                return info.text
        except Exception: pass

        if isinstance(focus_obj, NVDAObjects.behaviors.EditableText):
            try:
                info = focus_obj.makeTextInfo(textInfos.POSITION_ALL)
                if info and info.text and not info.text.isspace():
                    return info.text
            except Exception: pass
        
        if isinstance(focus_obj, NVDAObjects.behaviors.Terminal):
            try:
                info = focus_obj.makeTextInfo(textInfos.POSITION_ALL)
                return info.text
            except Exception: pass

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
                except Exception: pass
                
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
        
        gui.mainFrame.prePopup()
        try:
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
            
            modal_res = self.refine_menu_dlg.ShowModal()
        finally:
            gui.mainFrame.postPopup()

        if modal_res == wx.ID_OK:
            selection_index = self.refine_menu_dlg.GetSelection()
            custom_content = options[selection_index][1]

            file_paths = []
            needs_file = False
            wc = "Files|*.*"
            
            if "[file_ocr]" in custom_content:
                needs_file = True
                wc = "Images/PDF/TIFF|*.png;*.jpg;*.webp;*.pdf;*.tif;*.tiff;*.heic;*.heif"
            elif "[file_read]" in custom_content:
                needs_file = True
                wc = "Documents|*.txt;*.py;*.md;*.html;*.pdf;*.tif;*.tiff"
            elif "[file_audio]" in custom_content:
                needs_file = True
                wc = "Audio|*.mp3;*.wav;*.ogg"
            
            if needs_file:
                gui.mainFrame.prePopup()
                try:
                    # Translators: Standard title for opening a file
                    dlg = wx.FileDialog(gui.mainFrame, _("Open"), wildcard=wc, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
                    if dlg.ShowModal() == wx.ID_OK:
                        file_paths = dlg.GetPaths()
                        file_paths.sort()
                        wx.CallLater(200, lambda: threading.Thread(target=self._thread_refine, args=(captured_text, custom_content, file_paths), daemon=True).start())
                    dlg.Destroy()
                finally:
                    gui.mainFrame.postPopup()
            else:
                # Translators: Message while processing request of the refine text command
                msg = _("Processing...")
                self.report_status(msg)
                threading.Thread(target=self._thread_refine, args=(captured_text, custom_content, None), daemon=True).start()
        
        if self.refine_menu_dlg:
            self.refine_menu_dlg.Destroy()
            self.refine_menu_dlg = None

    def _thread_refine(self, captured_text, custom_content, file_paths=None):
        target_lang = get_lang_name("target_language")
        source_lang = get_lang_name("source_language")
        smart_swap = config.conf["VisionAssistant"]["smart_swap"]
        resp_lang = get_lang_name("ai_response_language")
        
        if file_paths and isinstance(file_paths, str):
            file_paths = [file_paths]
        elif not file_paths:
            file_paths = []

        prompt_text = custom_content
        attachments =[]
        needs_screenshot = "[screen_obj]" in prompt_text or "[screen_full]" in prompt_text or "[screen_fg_obj]" in prompt_text
        if needs_screenshot and check_screen_curtain_active():
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))
            return
        fallback = "English" if source_lang == "Auto-detect" else source_lang
        swap_instr = f" If text is in {target_lang}, translate to {fallback}." if smart_swap else ""
        prompt_text = apply_prompt_template(prompt_text,[
            ("target_lang", target_lang),
            ("source_lang", source_lang),
            ("response_lang", resp_lang),
            ("swap_target", fallback),
            ("swap_instruction", swap_instr),
        ])
        
        if "[fix_translate]" in prompt_text:
            prompt_text = prompt_text.replace("[fix_translate]", 
                f"Fix grammar and translate to {target_lang}.{swap_instr} Output ONLY the result.")
        
        prompt_text = prompt_text.replace("[summarize]", f"Summarize the text below in {resp_lang}.").replace("[fix_grammar]", "Fix grammar in the text below. Output ONLY the fixed text.").replace("[explain]", f"Explain the text below in {resp_lang}.")
        
        used_selection = False
        if "[selection]" in prompt_text: 
            prompt_text = prompt_text.replace("[selection]", captured_text)
            used_selection = True
            
        if "[clipboard]" in prompt_text: 
            prompt_text = prompt_text.replace("[clipboard]", api.getClipData())
            
        if "[clipboard_image]" in prompt_text:
            clip_path = self._getClipboardImageFile()
            if clip_path:
                try:
                    with open(clip_path, "rb") as f:
                        d = base64.b64encode(f.read()).decode('utf-8')
                    attachments.append({'mime_type': 'image/png', 'data': d})
                    os.remove(clip_path)
                except Exception:
                    pass
            prompt_text = prompt_text.replace("[clipboard_image]", "")
        
        if "[screen_obj]" in prompt_text:
            d, w, h, m = self._capture_navigator()
            if d: attachments.append({'mime_type': m, 'data': d})
            prompt_text = prompt_text.replace("[screen_obj]", "")
            
        if "[screen_full]" in prompt_text:
            d, w, h, m = self._capture_fullscreen()
            if d: attachments.append({'mime_type': m, 'data': d})
            prompt_text = prompt_text.replace("[screen_full]", "")

        if "[screen_fg_obj]" in prompt_text:
            d, x_fg, y_fg, w, h, m = self._capture_foreground()
            if d: attachments.append({'mime_type': m, 'data': d})
            prompt_text = prompt_text.replace("[screen_fg_obj]", "")

        if file_paths:
            # Translators: Message reported when executing the refine command
            msg = _("Uploading file...")
            wx.CallAfter(self.report_status, msg)
            
            if "[file_ocr]" in prompt_text:
                if AIHandler.is_gemini() and fitz:
                    v_doc = VirtualDocument(file_paths)
                    v_doc.scan()
                    if v_doc.total_pages > 0:
                        upload_path = v_doc.create_merged_pdf(0, v_doc.total_pages - 1)
                        if upload_path:
                            file_uri = self._upload_file_to_gemini(upload_path, "application/pdf")
                            if file_uri:
                                attachments.append({'mime_type': 'application/pdf', 'file_uri': file_uri})
                            try: os.remove(upload_path)
                            except Exception: pass
                else:
                    for f_path in file_paths:
                        mime_type = get_mime_type(f_path)
                        ext = os.path.splitext(f_path)[1].lower()
                        if ext in ['.pdf', '.tif', '.tiff'] and fitz:
                            try:
                                doc = fitz.open(f_path)
                                for i in range(len(doc)):
                                    page = doc.load_page(i)
                                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                                    data = base64.b64encode(pix.tobytes("jpg")).decode('utf-8')
                                    attachments.append({'mime_type': 'image/jpeg', 'data': data})
                                doc.close()
                            except Exception: pass
                        else:
                            if AIHandler.is_gemini():
                                file_uri = self._upload_file_to_gemini(f_path, mime_type)
                                if file_uri: attachments.append({'mime_type': mime_type, 'file_uri': file_uri})
                            else:
                                try:
                                    with open(f_path, "rb") as f: data = base64.b64encode(f.read()).decode('utf-8')
                                    attachments.append({'mime_type': mime_type, 'data': data})
                                except Exception: pass
                                
            elif "[file_read]" in prompt_text:
                for f_path in file_paths:
                    mime_type = get_mime_type(f_path)
                    if AIHandler.is_gemini():
                        file_uri = self._upload_file_to_gemini(f_path, mime_type)
                        if file_uri: attachments.append({'mime_type': mime_type, 'file_uri': file_uri})
                    else:
                        try:
                            with open(f_path, "rb") as f: raw = f.read()
                            txt = raw.decode('utf-8')
                            prompt_text += f"\n\nFile Content ({os.path.basename(f_path)}):\n{txt}\n"
                        except Exception: pass

            elif "[file_audio]" in prompt_text:
                for f_path in file_paths:
                    mime_type = get_mime_type(f_path)
                    if AIHandler.is_gemini():
                        file_uri = self._upload_file_to_gemini(f_path, mime_type)
                        if file_uri: attachments.append({'mime_type': mime_type, 'file_uri': file_uri})
                    else:
                        try:
                            with open(f_path, "rb") as f: data = base64.b64encode(f.read()).decode('utf-8')
                            attachments.append({'mime_type': mime_type, 'data': data})
                        except Exception: pass

            prompt_text = prompt_text.replace("[file_ocr]", "").replace("[file_read]", "").replace("[file_audio]", "")
            
            if not prompt_text.strip() and attachments:
                 prompt_text = get_prompt_text("refine_files_only") or "Analyze these files."
            
        if captured_text and not used_selection and not file_paths:
            prompt_text += f"\n\n---\nInput Text:\n{captured_text}\n---\n"
            
        # Translators: Message reported when executing the refine command
        msg = _("Analyzing...")
        wx.CallAfter(self.report_status, msg)
        res = AIHandler.call(prompt_text, attachments=attachments)
        
        if res:
             if res.startswith("ERROR:"):
                 log.error(f"Refine AI call returned error: {res}")
                 wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                 wx.CallAfter(show_error_dialog, res[6:])
                 return
             wx.CallAfter(setattr, self, 'current_status', _("Idle"))
             wx.CallAfter(self._open_refine_result_dialog, res, attachments, captured_text, prompt_text)

    def _open_refine_result_dialog(self, result_text, attachments, original_text, initial_prompt, force_show=False, is_recall=False):
        self._last_result_data = (self._open_refine_result_dialog, (result_text, attachments, original_text, initial_prompt))
        
        if config.conf["VisionAssistant"]["copy_to_clipboard"]:
            api.copyToClip(result_text)

        if config.conf["VisionAssistant"]["skip_chat_dialog"] and not force_show:
            if not is_recall: tones.beep(1000, 100)
            ui.message(clean_markdown(result_text))
            return

        if self.refine_dlg:
            try: self.refine_dlg.Destroy()
            except Exception: pass
            
        if not is_recall:
            tones.beep(1000, 100)

        def refine_callback(ctx, q, history, extra):
            atts, orig, first_p = ctx
            
            if AIHandler.is_gemini():
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
                return AIHandler.call(messages), None
            else:
                messages = []
                messages.append({"role": "user", "content": first_p})
                messages.append({"role": "assistant", "content": result_text})
                
                if history:
                    for h in history:
                        if h.get("role") == "model" and h["parts"][0]["text"] == result_text: continue
                        role = "assistant" if h["role"] == "model" else "user"
                        messages.append({"role": role, "content": h["parts"][0]["text"]})
                
                messages.append({"role": "user", "content": q})
                return AIHandler.call(messages), None

        context = (attachments, original_text, initial_prompt)
        has_file_context = any('file_uri' in a for a in attachments)

        self.refine_dlg = VisionQADialog(
            gui.mainFrame, 
            # Translators: Title of Refine Result dialog
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
    @scriptHandler.script(description=_("Performs smart actions on a selected image or PDF file."))
    def script_smartFileAction(self, gesture):
        if self.toggling: self.finish()
        if getattr(self, "_dialog_open", False):
            return

        if self._ocr_task_running["smartfile"]:
            self._stop_ocr_task("smartfile")
            return

        focused_paths = self._getFocusedExplorerFile()

        valid_exts = ('.pdf', '.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.heic', '.heif')
        valid_paths = [p for p in focused_paths if p.lower().endswith(valid_exts)]
        if valid_paths:
            threading.Thread(target=self._pre_process_smart_file, args=(valid_paths,), daemon=True).start()
            return
        clip_path = self._getClipboardImageFile()
        if clip_path:
            # Translators: Status reported when an image found in the clipboard is being processed.
            self.report_status(_("Processing clipboard image..."))
            threading.Thread(target=self._pre_process_smart_file, args=([clip_path],), daemon=True).start()
            return
        wx.CallLater(100, self._open_smart_file_dialog)

    def _open_smart_file_dialog(self):
        self._dialog_open = True
        wc = "Files|*.pdf;*.jpg;*.jpeg;*.png;*.webp;*.tif;*.tiff;*.heic;*.heif"
        self._browse_and_run(self._pre_process_smart_file, wc, multiple=True)
        self._dialog_open = False

    def _pre_process_smart_file(self, paths, resume=None):
        engine = config.conf["VisionAssistant"]["ocr_engine"]
        is_single_image = len(paths) == 1 and paths[0].lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.heic', '.heif'))

        if engine == 'none' and any(p.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.heic', '.heif')) for p in paths):
            # Translators: Error message when "None" engine is used on images via F key.
            msg = _("The 'None (Extract Text Layer)' engine cannot process image-based content. Please change the OCR Engine to 'Chrome' or 'AI (Advanced)' in settings.")
            wx.CallAfter(gui.messageBox, msg, _("OCR Engine Error"), wx.OK | wx.ICON_ERROR)
            return

        if is_single_image and engine == 'gemini':
            time.sleep(0.5)
            wx.CallAfter(self._ask_file_action, paths[0])
            return
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
            if resume is None:
                resume = self._maybe_resume_ocr("smartfile", list(paths))
            if resume:
                threading.Thread(target=self._process_file_ocr, args=(v_doc, resume["start"], resume["end"], resume["do_translate"], resume["target_lang"], resume), daemon=True).start()
            elif v_doc.total_pages == 1:
                threading.Thread(target=self._process_file_ocr, args=(v_doc, 0, 0), daemon=True).start()
            else:
                wx.CallAfter(self._show_ocr_range_dialog, v_doc)
        except Exception as e:
            log.error(f"Error preparing file: {e}")

    def _ask_file_action(self, path):
        self._dialog_open = True
        # Translators: Options for the image file action menu
        choices = [_("Extract Text (OCR)"), _("Describe Image")]
        gui.mainFrame.prePopup()
        try:
            # Translators: Instruction prompt and window title for the menu that appears when a user performs an action on a single image file.
            dlg = wx.SingleChoiceDialog(gui.mainFrame, _("Choose action:"), _("Image File"), choices)
            if dlg.ShowModal() == wx.ID_OK:
                selection = dlg.GetSelection()
                if selection == 0:
                    v_doc = VirtualDocument([path])
                    v_doc.scan()
                    if v_doc.total_pages > 1:
                        wx.CallAfter(self._show_ocr_range_dialog, v_doc)
                    else:
                        threading.Thread(target=self._process_file_ocr, args=(v_doc, 0, 0, False, get_lang_name("target_language")), daemon=True).start()
                else:
                    # Translators: Status reported when an image file is being analyzed
                    self.report_status(_("Analyzing Image File..."))
                    threading.Thread(target=self._thread_image_describe, args=(path,), daemon=True).start()
            dlg.Destroy()
        finally:
            gui.mainFrame.postPopup()
            self._dialog_open = False

    def _pre_process_file_ocr_single(self, path):
        v_doc = VirtualDocument([path])
        v_doc.scan()
        self._process_file_ocr(v_doc, 0, 0)

    def _show_ocr_range_dialog(self, v_doc):
        gui.mainFrame.prePopup()
        try:
            range_dlg = RangeDialog(gui.mainFrame, v_doc.total_pages)
            if range_dlg.ShowModal() == wx.ID_OK:
                settings = range_dlg.get_settings()
                threading.Thread(target=self._process_file_ocr, 
                                 args=(v_doc, settings['start'], settings['end'], settings['translate'], settings['lang']), 
                                 daemon=True).start()
            range_dlg.Destroy()
        finally:
            gui.mainFrame.postPopup()

    def _process_file_ocr(self, v_doc, start_page, end_page, do_translate=False, target_lang=None, resume=None):
        if target_lang is None:
            target_lang = get_lang_name("target_language")
        engine = config.conf["VisionAssistant"]["ocr_engine"]
        p = config.conf["VisionAssistant"]["active_provider"]
        progress_key = self._ocr_progress_key("smartfile", list(v_doc.file_paths))

        total_pages = end_page - start_page + 1
        done_pages = dict(resume.get("pages", {})) if resume else {}
        self._ocr_abort["smartfile"] = False
        self._ocr_task_running["smartfile"] = True

        def save_progress():
            OCRProgressStore.save(progress_key, {
                "paths": list(v_doc.file_paths),
                "start": start_page,
                "end": end_page,
                "do_translate": do_translate,
                "target_lang": target_lang,
                "pages": done_pages,
            })

        def finalize_running():
            self._ocr_task_running["smartfile"] = False

        if engine == 'none':
            def fast_worker(page_idx):
                try:
                    f_path, internal_idx = v_doc.get_page_info(page_idx)
                    doc = fitz.open(f_path)
                    page = doc.load_page(internal_idx)
                    txt = DocumentViewerDialog._extract_text_layer_from_page(page)
                    doc.close()
                    return page_idx, (f"--- Page {page_idx + 1} ---\n{txt}\n" if txt else "")
                except Exception: return page_idx, ""
            pending = [i for i in range(start_page, end_page + 1) if str(i) not in done_pages]
            with ThreadPoolExecutor(max_workers=5) as executor:
                for page_idx, part in executor.map(fast_worker, pending):
                    if self._ocr_abort["smartfile"]:
                        break
                    done_pages[str(page_idx)] = part
                    save_progress()
                    
                    completed_count = len(done_pages)
                    # Translators: Status message showing page-by-page progress during file OCR.
                    progress_msg = _("Processing page {current} of {total}...").format(current=completed_count, total=total_pages)
                    wx.CallAfter(setattr, self, 'current_status', progress_msg)
            finalize_running()
            if self._ocr_abort["smartfile"]:
                return
            full_text = "\n".join(p for _dummy, p in sorted(((int(k), v) for k, v in done_pages.items())) if p).strip()
            if not full_text:
                OCRProgressStore.clear(progress_key)
                # Translators: Error message shown when the 'None' engine is used on image-based content or scanned PDFs.
                wx.CallAfter(show_error_dialog, _("The 'None (Extract Text Layer)' engine cannot process image-based content. Please change the OCR Engine to 'Chrome' or 'AI (Advanced)' in settings."))
                return
            if do_translate:
                full_text = AIHandler.translate(full_text, target_lang)
            OCRProgressStore.clear(progress_key)
            wx.CallAfter(self._open_doc_chat_dialog, full_text, [], full_text, full_text)
            return

        # Translators: Message reported when extracting text from a file
        msg = _("Extracting Text...")
        wx.CallAfter(self.report_status, msg)
        
        upload_supported = AIHandler.is_gemini() or p == "mistral"
        if p == "custom":
            upload_supported = config.conf["VisionAssistant"].get("custom_upload_support", False)

        if engine == 'chrome' or not upload_supported or total_pages == 1:
            errors_list = []
            errors_lock = threading.Lock()

            def page_worker(page_idx):
                try:
                    f_path, internal_idx = v_doc.get_page_info(page_idx)
                    doc = fitz.open(f_path)
                    page = doc.load_page(internal_idx)
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    img_bytes = pix.tobytes("jpg")
                    doc.close()

                    if engine == 'chrome':
                        txt = ChromeOCREngine.recognize(img_bytes)
                    else:
                        img_b64 = base64.b64encode(img_bytes).decode('utf-8')
                        txt = AIHandler.ocr(img_b64, "image/jpeg")

                    if not txt: 
                        return page_idx, ""
                    
                    if txt.startswith("ERROR:"):
                        with errors_lock:
                            errors_list.append(txt[6:])
                        log.error(f"SmartFile OCR page {page_idx + 1} failed: {txt}")
                        return page_idx, ""

                    if do_translate:
                        txt = AIHandler.translate(txt, target_lang)
                    return page_idx, f"--- Page {page_idx + 1} ---\n{txt}\n"
                except Exception as e:
                    log.error(f"Exception in page_worker for page {page_idx + 1}: {e}", exc_info=True)
                    return page_idx, ""

            pending = [i for i in range(start_page, end_page + 1) if str(i) not in done_pages]
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(page_worker, i): i for i in pending}
                for future in as_completed(futures):
                    if self._ocr_abort["smartfile"]:
                        break
                    try:
                        page_idx, part = future.result()
                        if not _is_failed_ocr_page(part):
                            done_pages[str(page_idx)] = part
                            save_progress()
                            
                            completed_count = len(done_pages)
                            # Translators: Status message showing page-by-page progress during file OCR.
                            progress_msg = _("Processing page {current} of {total}...").format(current=completed_count, total=total_pages)
                            wx.CallAfter(ui.message, progress_msg)
                            wx.CallAfter(setattr, self, 'current_status', progress_msg)
                    except Exception as e:
                        log.error(f"Error retrieving future result: {e}", exc_info=True)

            finalize_running()
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))
            if self._ocr_abort["smartfile"]:
                return
            full_text = "\n".join(p for _dummy, p in sorted(((int(k), v) for k, v in done_pages.items())) if p).strip()
            if not full_text:
                OCRProgressStore.clear(progress_key)
                if errors_list:
                    wx.CallAfter(show_error_dialog, errors_list[0])
                else:
                    # Translators: Error message shown when the OCR process fails to detect any text in the file or an unknown error occurs during extraction.
                    wx.CallAfter(show_error_dialog, _("No text detected or error occurred."))
                return
            OCRProgressStore.clear(progress_key)
            wx.CallAfter(self._open_doc_chat_dialog, full_text, [], full_text, full_text)

        else:
            raw_batch_size = config.conf["VisionAssistant"].get("ocr_batch_size", 20)
            batch_size = total_pages if raw_batch_size == 0 else raw_batch_size
            had_error = False

            for i in range(start_page, end_page + 1, batch_size):
                if self._ocr_abort["smartfile"]:
                    break
                if str(i) in done_pages:
                    continue
                b_end = min(i + batch_size - 1, end_page)
                upload_path = v_doc.create_merged_pdf(i, b_end)
                if not upload_path: continue

                # Translators: Status message showing batch progress during file OCR.
                wx.CallAfter(self.report_status, _("Analyzing batch {start}-{end}...").format(start=i+1, end=b_end+1))
                
                mime_type = "application/pdf"
                res = None

                if p == "mistral":
                    res = AIHandler.ocr(upload_path, "application/pdf")
                else:
                    file_uri = None
                    for attempt in range(3):
                        file_uri = self._upload_file_to_gemini(upload_path, mime_type, silent=True)
                        if file_uri:
                            break
                        time.sleep(0.5 * (attempt + 1))

                    if not file_uri:
                        if os.path.exists(upload_path): os.remove(upload_path)
                        had_error = True
                        # Translators: Error message shown when the upload fails.
                        msg = _("Failed to upload document batch {start}-{end} after multiple attempts.").format(start=i+1, end=b_end+1)
                        wx.CallAfter(show_error_dialog, msg)
                        continue

                    p_text = apply_prompt_template(get_prompt_text("ocr_document_translate" if do_translate else "ocr_document_extract"), [("target_lang", target_lang)])
                    attachments = [{'mime_type': mime_type, 'file_uri': file_uri}]
                    for attempt in range(3):
                        res = AIHandler.call(p_text, attachments=attachments)
                        if res and not res.startswith("ERROR:"):
                            break
                        time.sleep(0.5 * (attempt + 1))

                if os.path.exists(upload_path): os.remove(upload_path)

                if res and not res.startswith("ERROR:"):
                    if p == "mistral":
                        results = res.split('[[[PAGE_SEP]]]')
                        for j, text_part in enumerate(results):
                            page_idx = i + j
                            if page_idx <= end_page:
                                page_text = text_part.strip()
                                if do_translate and page_text:
                                    page_text = AIHandler.translate(page_text, target_lang)
                                done_pages[str(page_idx)] = page_text
                    else:
                        done_pages[str(i)] = res
                    save_progress()
                else:
                    had_error = True
                    # Translators: Error message shown when the connection to the server times out
                    err_msg = res[6:] if res and res.startswith("ERROR:") else _("Connection Timeout")
                    # Translators: Error message shown when the AI processing fails.
                    msg = _("Failed to process document batch {start}-{end}: {error}").format(start=i+1, end=b_end+1, error=err_msg)
                    wx.CallAfter(show_error_dialog, msg)

            finalize_running()
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))
            if self._ocr_abort["smartfile"]:
                return
            all_text_parts = [v for _dummy, v in sorted(((int(k), v) for k, v in done_pages.items()))]
            if all_text_parts:
                OCRProgressStore.clear(progress_key)
                final_combined = "\n\n".join(all_text_parts)
                wx.CallAfter(self._open_doc_chat_dialog, final_combined, [], final_combined, final_combined)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Opens the Document Reader for detailed page-by-page analysis (PDF/Images)."))
    def script_analyzeDocument(self, gesture):
        if self.toggling: self.finish()
        if getattr(self, "_dialog_open", False):
            return

        if self._ocr_task_running["document"]:
            self._stop_ocr_task("document")
            viewer = getattr(self, "doc_viewer_dlg", None)
            if viewer:
                viewer.abort = True
            return

        focused_paths = self._getFocusedExplorerFile()

        valid_exts = ('.pdf', '.jpg', '.jpeg', '.png', '.tif', '.tiff', '.heic', '.heif')
        valid_paths = [p for p in focused_paths if p.lower().endswith(valid_exts)]
        if valid_paths:
            threading.Thread(target=self._scan_and_open, args=(valid_paths,), daemon=True).start()
            return
        clip_path = self._getClipboardImageFile()
        if clip_path:
            # Translators: Status reported when an image found in the clipboard is being processed.
            self.report_status(_("Processing clipboard image..."))
            threading.Thread(target=self._scan_and_open, args=([clip_path],), daemon=True).start()
            return
        wx.CallAfter(self._open_document_reader)

    def _open_doc_chat_dialog(self, init_msg, initial_attachments, doc_text, raw_text_for_save=None, force_show=False, is_recall=False):
        self._last_result_data = (self._open_doc_chat_dialog, (init_msg, initial_attachments, doc_text, raw_text_for_save))
        
        if config.conf["VisionAssistant"]["copy_to_clipboard"]:
            api.copyToClip(raw_text_for_save if raw_text_for_save else init_msg)

        if config.conf["VisionAssistant"]["skip_chat_dialog"] and not force_show:
            if not is_recall: tones.beep(1000, 100)
            ui.message(clean_markdown(init_msg))
            return

        if self.doc_dlg:
            try: 
                self.doc_dlg.Destroy()
            except Exception: pass
            self.doc_dlg = None
            
        if not is_recall:
            tones.beep(1000, 100)

        def doc_callback(ctx_atts, q, history, dum2):
            lang = get_lang_name("ai_response_language")
            system_template = get_prompt_text("document_chat_system")
            system_instr = apply_prompt_template(system_template, [("response_lang", lang)])
            
            if AIHandler.is_gemini():
                context_parts = []
                if ctx_atts:
                    for att in ctx_atts:
                        if 'file_uri' in att:
                            context_parts.append({"file_data": {"mime_type": att['mime_type'], "file_uri": att['file_uri']}})
                        elif 'data' in att:
                            context_parts.append({"inline_data": {"mime_type": att['mime_type'], "data": att['data']}})
                else:
                    context_parts.append({"text": f"Context content:\n{doc_text}"})
                
                context_parts.append({"text": f"Instruction: {system_instr}"})
                messages = [{"role": "user", "parts": context_parts}]
                ack_text = get_prompt_text("document_chat_ack") or "Context received. Ready for questions."
                messages.append({"role": "model", "parts": [{"text": ack_text}]})
                if history: messages.extend(history)
                messages.append({"role": "user", "parts": [{"text": q}]})
                return AIHandler.call(messages), None
            else:
                messages = []
                messages.append({"role": "user", "content": f"{system_instr}\n\nContext content:\n{doc_text}"})
                messages.append({"role": "assistant", "content": get_prompt_text("document_chat_ack") or "Context received."})
                if history:
                    for h in history:
                        role = "assistant" if h["role"] == "model" else "user"
                        messages.append({"role": role, "content": h["parts"][0]["text"]})
                messages.append({"role": "user", "content": q})
                return AIHandler.call(messages), None
            
        self.doc_dlg = VisionQADialog(
            gui.mainFrame, 
            # Translators: Dialog title for a Chat dialog
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
        if check_screen_curtain_active():
            return
        self._start_vision(True)

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Describes the current object (Navigator Object)."))
    def script_describeObject(self, gesture):
        if self.toggling: self.finish()
        if check_screen_curtain_active():
            return
        self._start_vision(False)

    def _start_vision(self, full):
        if full: d, w, h, m = self._capture_fullscreen()
        else: d, w, h, m = self._capture_navigator()
        if d:
            # Translators: Message reported when calling an image analysis command
            msg = _("Scanning...")
            self.report_status(msg)
            wx.CallLater(100, lambda: threading.Thread(target=self._thread_vision, args=(d, w, h, m, full), daemon=True).start())
        else: 
            # Translators: Message reported when calling an image analysis command
            msg = _("Capture failed.")
            self.report_status(msg)

    def _thread_vision(self, img, w, h, m, full=False):
        lang = get_lang_name("ai_response_language")
        vision_key = "vision_fullscreen" if full else "vision_navigator_object"
        vision_template = get_prompt_text(vision_key)
        p = apply_prompt_template(vision_template,[
            ("response_lang", lang),
            ("width", w),
            ("height", h),
        ])
        att = [{'mime_type': m, 'data': img}]
        res = AIHandler.call(p, attachments=att)
        if res:
            if res.startswith("ERROR:"):
                log.error(f"Vision analysis AI call failed: {res}")
                wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                wx.CallAfter(show_error_dialog, res[6:])
                return
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))
            wx.CallAfter(self._open_vision_dialog, res, att, None)
        else:
            log.error("Vision analysis: AI returned empty response")
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))

    def _thread_image_describe(self, path):
        try:
            mime_type = get_mime_type(path)
            with open(path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode('utf-8')
            
            lang = get_lang_name("ai_response_language")
            vision_template = get_prompt_text("vision_navigator_object")
            p = apply_prompt_template(vision_template, [("response_lang", lang)])
            
            att = [{'mime_type': mime_type, 'data': img_data}]
            res = AIHandler.call(p, attachments=att)
            
            if res:
                if res.startswith("ERROR:"):
                    wx.CallAfter(show_error_dialog, res[6:])
                else:
                    wx.CallAfter(self._open_vision_dialog, res, att, None)
            
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))
        except Exception as e:
            log.error(f"Image file analysis failed: {e}", exc_info=True)
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))

    def _open_vision_dialog(self, text, atts, size, force_show=False, is_recall=False):
        self._last_result_data = (self._open_vision_dialog, (text, atts, size))
        
        if config.conf["VisionAssistant"]["copy_to_clipboard"]:
            api.copyToClip(text)

        if config.conf["VisionAssistant"]["skip_chat_dialog"] and not force_show:
            if not is_recall: tones.beep(1000, 100)
            ui.message(clean_markdown(text))
            return

        if self.vision_dlg:
            try: self.vision_dlg.Destroy()
            except Exception: pass
            self.vision_dlg = None
            
        if not is_recall:
            tones.beep(1000, 100)

        def cb(atts, q, history, sz):
            lang = get_lang_name("ai_response_language")
            followup_suffix_template = get_prompt_text("vision_followup_suffix") or "Answer strictly in {response_lang}"
            followup_suffix = apply_prompt_template(followup_suffix_template, [("response_lang", lang)])
            
            if AIHandler.is_gemini():
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
                return AIHandler.call(messages, attachments=atts), None
            else:
                messages = []
                followup_context_template = get_prompt_text("vision_followup_context") or "Image Context. Target Language: {response_lang}"
                followup_context = apply_prompt_template(followup_context_template, [("response_lang", lang)])
                
                initial_content = [{"type": "text", "text": followup_context}]
                for att in atts:
                    initial_content.append({"type": "image_url", "image_url": {"url": f"data:{att['mime_type']};base64,{att['data']}"}})
                
                messages.append({"role": "user", "content": initial_content})
                messages.append({"role": "assistant", "content": text})
                
                if history:
                    for h in history:
                        if h.get("role") == "model" and h["parts"][0]["text"] == text: continue
                        role = "assistant" if h["role"] == "model" else "user"
                        messages.append({"role": role, "content": h["parts"][0]["text"]})
                
                messages.append({"role": "user", "content": f"{q} ({followup_suffix})"})
                return AIHandler.call(messages, attachments=atts), None
            
        self.vision_dlg = VisionQADialog(
            gui.mainFrame, 
            # Translators: Dialog title for Image Analysis
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
        if getattr(self, "_dialog_open", False):
            return
        wx.CallLater(100, self._open_audio)

    def _open_audio(self):
        self._dialog_open = True
        wc = "Audio|*.mp3;*.wav;*.ogg"
        self._browse_and_run(self._thread_audio, wc)
        self._dialog_open = False

    def _thread_audio(self, path):
        try:
            # Translators: Message reported when calling the audio transcription command
            msg = _("Uploading...")
            wx.CallAfter(self.report_status, msg)
            mime_type = get_mime_type(path)
            lang = get_lang_name("ai_response_language")
            audio_template = get_prompt_text("audio_transcription")
            p = apply_prompt_template(audio_template, [("response_lang", lang)])
            
            if AIHandler.is_gemini():
                file_uri = self._upload_file_to_gemini(path, mime_type)
                if not file_uri: 
                    wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                    return
                att = [{'mime_type': mime_type, 'file_uri': file_uri}]
            else:
                with open(path, "rb") as f: audio_data = base64.b64encode(f.read()).decode('utf-8')
                att =[{'mime_type': mime_type, 'data': audio_data}]

            # Translators: Message reported when calling the audio transcription command
            msg = _("Analyzing...")
            wx.CallAfter(self.report_status, msg)
            res = AIHandler.call(p, attachments=att)
            
            if res:
                if res.startswith("ERROR:"):
                    wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                    wx.CallAfter(show_error_dialog, res[6:])
                    return
                wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                wx.CallAfter(self._open_doc_chat_dialog, res, att, res, res)
        except Exception as e:
            log.error(f"Audio analysis thread failed: {e}")
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Analyzes a local video file or an online video URL."))
    def script_analyzeOnlineVideo(self, gesture):
        if self.toggling: self.finish()
        if getattr(self, "_dialog_open", False):
            return

        focused_paths = self._getFocusedExplorerFile()
        valid_exts = (
            '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
            '.mpg', '.mpeg', '.m4v', '.3gp', '.3g2', '.ts', '.mts', 
            '.m2ts', '.vob', '.asf', '.divx', '.ogv'
        )
        valid_paths = [p for p in focused_paths if p.lower().endswith(valid_exts)]
        
        target_path = None
        is_local = False
        
        if valid_paths:
            target_path = valid_paths[0]
            is_local = True
        else:
            try:
                clip_data = api.getClipData().strip()
                if clip_data.startswith(("http://", "https://", "www.")):
                    domain = urlparse(clip_data).netloc.lower()
                    if any(d in domain for d in ["youtube.com", "youtu.be", "instagram.com", "twitter.com", "x.com", "tiktok.com"]):
                        target_path = clip_data
                        is_local = False
            except Exception:
                pass

        if target_path:
            wx.CallLater(100, self._ask_video_action, target_path, is_local)
        else:
            wx.CallLater(100, self._open_video_dialog)

    def _ask_video_action(self, target_path, is_local):
        self._dialog_open = True
        choices = [
            # Translators: Dialog choice for analyzing video content generally.
            _("General Video Analysis"),
            # Translators: Dialog choice for generating an audio description SRT file.
            _("Generate Audio Description (SRT File)")
        ]
        
        gui.mainFrame.prePopup()
        try:
            # Translators: Title of the quick action dialog.
            dlg = wx.SingleChoiceDialog(gui.mainFrame, _("Choose action:"), _("Video Action"), choices)
            
            if dlg.ShowModal() == wx.ID_OK:
                selection = dlg.GetSelection()
                is_srt_mode = (selection == 1)
                prog_dlg = None
                
                if is_srt_mode:
                    def run_generation(dialog_instance):
                        if is_local:
                            threading.Thread(target=self._thread_local_video, args=(target_path, True, dialog_instance), daemon=True).start()
                        else:
                            threading.Thread(target=self._thread_video, args=(target_path, True, dialog_instance), daemon=True).start()
                    
                    prog_dlg = VideoSRTProgressDialog(gui.mainFrame, regenerate_cb=run_generation, original_path=target_path if is_local else None)
                    prog_dlg.Show()
                    
                if is_local:
                    threading.Thread(target=self._thread_local_video, args=(target_path, is_srt_mode, prog_dlg), daemon=True).start()
                else:
                    threading.Thread(target=self._thread_video, args=(target_path, is_srt_mode, prog_dlg), daemon=True).start()
            
            dlg.Destroy()
        finally:
            gui.mainFrame.postPopup()
            self._dialog_open = False

    def _open_video_dialog(self):
        self._dialog_open = True
        if not AIHandler.is_gemini():
            self._dialog_open = False
            # Translators: Error message when video analysis is attempted with a non-Gemini provider.
            wx.CallAfter(self.report_status, _("Video analysis is only supported by Gemini providers."))
            return

        gui.mainFrame.prePopup()
        try:
            dlg = VideoSourceDialog(gui.mainFrame)
            dlg.Raise()
            if dlg.ShowModal() == wx.ID_OK:
                is_srt_mode = (dlg.action_choice.GetSelection() == 1)
                if is_srt_mode:
                    config.conf["VisionAssistant"]["video_chars_as_subtitle"] = dlg.chars_as_sub_check.Value
                    config.conf["VisionAssistant"]["video_add_disclaimer"] = dlg.disclaimer_check.Value
                
                input_val = dlg.url_input.GetValue().strip()
                if not input_val:
                    dlg.Destroy()
                    gui.mainFrame.postPopup()
                    self._dialog_open = False
                    return

                is_local_file = False
                try:
                    if os.path.exists(input_val) and os.path.isfile(input_val):
                        is_local_file = True
                except Exception:
                    pass

                prog_dlg = None
                if is_srt_mode:
                    def run_generation(dialog_instance):
                        if is_local_file:
                            threading.Thread(target=self._thread_local_video, args=(input_val, True, dialog_instance), daemon=True).start()
                        else:
                            threading.Thread(target=self._thread_video, args=(input_val, True, dialog_instance), daemon=True).start()
                    
                    prog_dlg = VideoSRTProgressDialog(gui.mainFrame, regenerate_cb=run_generation, original_path=input_val if is_local_file else None)
                    prog_dlg.Show()
                    
                if is_local_file:
                    threading.Thread(target=self._thread_local_video, args=(input_val, is_srt_mode, prog_dlg), daemon=True).start()
                else:
                    threading.Thread(target=self._thread_video, args=(input_val, is_srt_mode, prog_dlg), daemon=True).start()
            dlg.Destroy()
        finally:
            gui.mainFrame.postPopup()
            self._dialog_open = False

    def _parse_seconds_helper(self, ts_str):
        try:
            ts_clean = str(ts_str).replace('.', ',').split(',', 1)[0].strip()
            parts = ts_clean.split(':')
            if len(parts) == 2:
                return float(int(parts[0]) * 60 + int(parts[1]))
            elif len(parts) == 3:
                return float(int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2]))
        except Exception:
            pass
        return 0.0

    def _is_segment_complete(self, json_str, start_sec, end_sec, total_duration):
        try:
            expected_end = end_sec if end_sec != -1 else total_duration
            if not expected_end: return True
            
            chunk_length = expected_end - start_sec
            if chunk_length <= 0: return True
            
            clean_json = json_str.strip()
            if "```json" in clean_json: clean_json = clean_json.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_json: clean_json = clean_json.split("```")[1].split("```")[0].strip()
            
            descriptions = None
            try:
                data = json.loads(clean_json)
                if isinstance(data, list):
                    descriptions = data
                elif isinstance(data, dict):
                    descriptions = data.get("descriptions", data.get("descriptions_list", []))
            except Exception:
                pass

            max_generated_sec = 0
            
            from collections import Counter
            ts_counter = Counter()

            if descriptions and isinstance(descriptions, list):
                if len(descriptions) < 2:
                    return False
                for desc in descriptions:
                    if not isinstance(desc, dict): continue
                    ts_str = desc.get("end") or desc.get("start")
                    if ts_str:
                        ts_counter[ts_str] += 1
                        t_sec = self._parse_seconds_helper(ts_str)
                        if t_sec > max_generated_sec:
                            max_generated_sec = t_sec
            else:
                matches = re.findall(r'"end"\s*:\s*"([^"]+)"', clean_json)
                if not matches or len(matches) < 2:
                    return False
                for ts_str in matches:
                    ts_counter[ts_str] += 1
                    t_sec = self._parse_seconds_helper(ts_str)
                    if t_sec > max_generated_sec:
                        max_generated_sec = t_sec
                        
            if any(count >= 5 for count in ts_counter.values()):
                log.warning("Segment rejected due to AI looping on the same timestamp.")
                return False
            
            if start_sec > 0 and max_generated_sec < start_sec:
                target_to_reach = chunk_length
                current_reached = max_generated_sec
            else:
                target_to_reach = expected_end
                current_reached = max_generated_sec

            tolerance = max(60, chunk_length * 0.15)
            
            if current_reached >= (target_to_reach - tolerance):
                return True
            return False
        except Exception as e:
            log.warning(f"Segment validation error: {e}")
            return True

    def _thread_local_video(self, path, is_srt_mode=False, prog_dlg=None):
        self._run_video_analysis(_LocalVideoSource(path), is_srt_mode=is_srt_mode, prog_dlg=prog_dlg)

    def _thread_video(self, url, is_srt_mode=False, prog_dlg=None):
        source = self._build_online_video_source(url)
        self._run_video_analysis(source, is_srt_mode=is_srt_mode, prog_dlg=prog_dlg)

    def _build_online_video_source(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        if not domain:
            # Translators: Error message when the provided video URL is not valid.
            return _InvalidVideoSource(_("Error: Invalid URL."))

        if any(d in domain for d in ["youtube.com", "youtu.be"]):
            return _YouTubeVideoSource(url)
        if "instagram.com" in domain:
            return _DownloadVideoSource(url, "instagram")
        if any(d in domain for d in ["twitter.com", "x.com"]):
            return _DownloadVideoSource(url, "twitter")
        if "tiktok.com" in domain:
            return _DownloadVideoSource(url, "tiktok")

        # Translators: Error message when the video URL is from an unsupported website.
        return _InvalidVideoSource(_("Error: Unsupported platform. Only YouTube, Instagram, Twitter, and TikTok are supported."))

    def _run_video_analysis(self, source, is_srt_mode=False, prog_dlg=None):
        intervals = []
        master_data_list = []
        final_res_string = ""
        global_character_context = ""
        # Translators: Disclaimer added at the beginning of AI-generated SRT files.
        srt_disclaimer = _("Disclaimer: This audio description was generated by AI. Some details, including character identities or events, may not be entirely accurate.")

        def abort_check():
            if prog_dlg is not None:
                try:
                    return prog_dlg.abort
                except Exception:
                    return True
            return False

        def report(msg, speak=True):
            if abort_check(): return
            display_text = msg
            if is_srt_mode and master_data_list:
                combined_header = ""

                if config.conf["VisionAssistant"].get("video_add_disclaimer", True):
                    combined_header = srt_disclaimer
                    

                if global_character_context and config.conf["VisionAssistant"].get("video_chars_as_subtitle", True):
                    if combined_header:
                        combined_header += "\n\n" + global_character_context
                    else:
                        combined_header = global_character_context

                partial_srt = convert_json_to_srt_string(master_data_list, segments=intervals[:len(master_data_list)], global_chars=combined_header)
                if partial_srt:
                    display_text = msg + "\n\n" + partial_srt
            elif not is_srt_mode and final_res_string:
                display_text = msg + "\n\n" + final_res_string.strip()

            if prog_dlg is not None:
                try: wx.CallAfter(prog_dlg.txt_status.SetValue, display_text)
                except Exception: pass
                if speak:
                    if _vision_assistant_instance:
                        _vision_assistant_instance.current_status = msg
                    wx.CallAfter(ui.message, msg)
            else:
                if speak: wx.CallAfter(self.report_status, msg)

        try:
            if not source.prepare(report, abort_check):
                if not prog_dlg: wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                return

            file_uri = getattr(prog_dlg, 'file_uri', None) if prog_dlg else None
            current_key = getattr(prog_dlg, 'current_key', None) if prog_dlg else None
            local_path = getattr(prog_dlg, 'local_path', None) if prog_dlg else None
            duration_sec = None

            if source.is_direct:
                file_uri = source.direct_uri
                duration_sec = source.duration(file_uri)
            else:
                if not local_path or not os.path.exists(local_path):
                    local_path = source.ensure_local(self, report, abort_check)
                    if abort_check(): return
                    if not local_path:
                        if not prog_dlg: wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                        return
                    if prog_dlg: prog_dlg.local_path = local_path
                
                if not file_uri:
                    file_uri, duration_sec, current_key = GeminiHandler.upload_and_get_duration(local_path, report_callback=report, abort_checker=abort_check)
                    if not file_uri:
                        # Translators: Error message shown when uploading the video to the AI server fails.
                        report(_("Upload failed."))
                        if not prog_dlg: wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                        return
                    if prog_dlg:
                        prog_dlg.file_uri = file_uri
                        prog_dlg.current_key = current_key
                else:
                    duration_sec = source.duration(file_uri)

            intervals.clear()
            chunk_minutes = config.conf["VisionAssistant"].get("video_srt_chunk_minutes", 5)
            chunk_size_sec = chunk_minutes * 60

            if is_srt_mode and chunk_size_sec > 0 and duration_sec and duration_sec > chunk_size_sec:
                start = 0
                while start < duration_sec:
                    end = min(start + chunk_size_sec, duration_sec)
                    intervals.append((start, end))
                    start = end
            else:
                intervals.append((0, duration_sec if duration_sec else -1))

            lang = get_lang_name("ai_response_language")

            if is_srt_mode:
                # Translators: Status message when the AI is analyzing the whole video to extract character names and appearances.
                report(_("Extracting characters (First pass)..."))
                char_template = get_prompt_text("video_character_extraction")
                char_prompt = apply_prompt_template(char_template, [("response_lang", lang)])

                char_res, file_uri, current_key = GeminiHandler.process_video_task(
                    local_path, char_prompt, None, None, True, report, abort_check, file_uri, current_key, source.is_direct
                )
                if prog_dlg:
                    prog_dlg.file_uri = file_uri
                    prog_dlg.current_key = current_key

                if char_res and not char_res.startswith("ERROR:"):
                    try:
                        clean_json = char_res.strip()
                        if "```json" in clean_json: clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                        elif "```" in clean_json: clean_json = clean_json.split("```")[1].split("```")[0].strip()
                        chars = []
                        try:
                            char_data = json.loads(clean_json)
                            if "characters" in char_data: chars = char_data["characters"]
                            else:
                                for v in char_data.values():
                                    if isinstance(v, list):
                                        chars = v; break
                            if not chars and isinstance(char_data, list): chars = char_data
                        except Exception: pass

                        if not chars:

                            blocks = re.findall(r'"name"\s*:\s*"([^"]+)"\s*,\s*"description"\s*:\s*"([^"]+)"', clean_json, re.IGNORECASE)
                            for block in blocks: chars.append({"name": block[0], "description": block[1]})

                        if chars:
                            ctx_lines = []
                            for c in chars:
                                if isinstance(c, dict):

                                    n = c.get('name') or c.get('Name') or 'Unknown'
                                    d = c.get('description') or c.get('Description') or ''
                                    ctx_lines.append(f"- {n}: {d}")
                                elif isinstance(c, str):
                                    ctx_lines.append(f"- {c}")

                            if ctx_lines:
                                # Translators: Header for the list of extracted characters in the generated subtitle.
                                dict_title = _("GLOBAL CHARACTER DICTIONARY:") + "\n"
                                global_character_context = dict_title + "\n".join(ctx_lines)
                    except Exception as e:
                        log.warning(f"Failed to parse character extraction JSON: {e}")

            master_data_list.clear()
            segment_success = True
            final_res_string = ""
            prev_descriptions = ""

            for seg_idx, (start_sec, end_sec) in enumerate(intervals):
                if abort_check(): return

                needs_cooldown = (seg_idx > 0) or (seg_idx == 0 and is_srt_mode)
                if needs_cooldown:
                    cooldown_seconds = 30 if (seg_idx == 0 and is_srt_mode) else 20
                    # Translators: Status message shown when the add-on pauses briefly between API requests to prevent hitting server rate limits.
                    report(_("Cooling down to prevent rate limits ({seconds} seconds)...").format(seconds=cooldown_seconds))
                    for step in range(cooldown_seconds * 2):
                        if abort_check(): return
                        time.sleep(0.5)

                if is_srt_mode:
                    video_template = get_prompt_text("video_audio_description")
                else:
                    video_template = get_prompt_text("video_analysis")

                h_start, m_start, s_start = int(start_sec//3600), int((start_sec%3600)//60), int(start_sec%60)
                h_end, m_end, s_end = int(end_sec//3600), int((end_sec%3600)//60), int(end_sec%60) if end_sec != -1 else (0, 0, 0)

                start_str = f"{h_start:02d}:{m_start:02d}:{s_start:02d}"
                end_str = f"{h_end:02d}:{m_end:02d}:{s_end:02d}" if end_sec != -1 else "end"

                segment_template = get_prompt_text("video_segment_instruction")
                end_text = f"{end_str} ({int(end_sec)} seconds)" if end_sec != -1 else "the end of the video"
                segment_instruction = apply_prompt_template(segment_template, [
                    ("start_str", f"{start_str} ({int(start_sec)} seconds)"),
                    ("end_str", end_text)
                ])

                p = apply_prompt_template(video_template, [("response_lang", lang)])
                if global_character_context:
                    p = f"{global_character_context}\n\n{p}"
                if prev_descriptions:
                    prev_context_template = get_prompt_text("video_previous_context")
                    if prev_context_template:
                        prev_context_str = apply_prompt_template(prev_context_template, [("prev_descriptions", prev_descriptions)])
                        p = f"{p}\n\n{prev_context_str}"

                prompt_with_segment = f"{segment_instruction}\n\n{p}" if len(intervals) > 1 else p

                if len(intervals) > 1:
                    # Translators: Status message reporting which segment of the video is currently being analyzed. {current} is the current segment number and {total} is the total segment count.
                    report(_("Analyzing video segment {current} of {total}...").format(current=seg_idx + 1, total=len(intervals)))
                else:
                    # Translators: Message reported when AI is analyzing the video
                    report(_("Analyzing video..."))

                validator = None
                if is_srt_mode and len(intervals) > 1:
                    validator = lambda r: self._is_segment_complete(r, start_sec, end_sec, duration_sec)

                seg_res, file_uri, current_key = GeminiHandler.process_video_task(
                    local_path, prompt_with_segment, start_sec, end_sec, is_srt_mode, report, abort_check, file_uri, current_key, source.is_direct, validator=validator
                )
                if prog_dlg:
                    prog_dlg.file_uri = file_uri
                    prog_dlg.current_key = current_key

                if not seg_res or seg_res.startswith("ERROR:"):
                    segment_success = False
                    break

                if is_srt_mode:
                    master_data_list.append(seg_res)
                    prev_descriptions = ""
                    try:
                        clean_res = seg_res.strip()
                        if "```json" in clean_res: clean_res = clean_res.split("```json")[1].split("```")[0].strip()
                        elif "```" in clean_res: clean_res = clean_res.split("```")[1].split("```")[0].strip()
                        parsed = json.loads(clean_res)
                        descs = parsed if isinstance(parsed, list) else parsed.get("descriptions", parsed.get("descriptions_list", []))
                        if descs:
                            cutoff_sec = max(0, end_sec - 120)
                            recent = []
                            for d in descs:
                                try:
                                    t = d.get("end", d.get("start", ""))
                                    t = t.split(",")[0].split(".")[0]
                                    parts = t.split(":")
                                    if len(parts) >= 3:
                                        ds = int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
                                        if ds >= cutoff_sec:
                                            label = d.get("label", d.get("text", "")).strip()
                                            s = d.get("start", "")
                                            if label:
                                                recent.append(f"[{s}] {label}")
                                except Exception:
                                    continue
                            if recent:
                                prev_descriptions = "\n".join(recent[-10:])
                    except Exception:
                        pass
                else:
                    if len(intervals) > 1:
                        final_res_string += f"\n\n--- [Part {seg_idx + 1}: {start_str} - {end_str}] ---\n" + seg_res
                    else:
                        final_res_string = seg_res

                if seg_idx + 1 < len(intervals):
                    # Translators: Status message shown when a video segment finishes processing and the system is moving to the next one. {current} is the completed segment number.
                    report(_("Segment {current} finished. Preparing next...").format(current=seg_idx+1))
                else:
                    # Translators: Status message when all segments are done and it is finalizing.
                    report(_("Finalizing..."))

            if abort_check(): return

            if segment_success:
                if is_srt_mode:
                    combined_header = ""
                    if config.conf["VisionAssistant"].get("video_add_disclaimer", True):
                        combined_header = srt_disclaimer
                        
                    if global_character_context and config.conf["VisionAssistant"].get("video_chars_as_subtitle", True):
                        if combined_header:
                            combined_header += "\n\n" + global_character_context
                        else:
                            combined_header = global_character_context

                    srt_content = convert_json_to_srt_string(master_data_list, segments=intervals, global_chars=combined_header)
                    if srt_content:
                        wx.CallAfter(prog_dlg.on_finished, srt_content)
                    else:
                        # Translators: Error message shown when the AI output cannot be converted into a valid SRT subtitle file.
                        wx.CallAfter(prog_dlg.on_error, _("Failed to parse AI output into SRT."))
                else:
                    attachments = [{'mime_type': 'video/mp4', 'file_uri': file_uri}] if file_uri else []
                    wx.CallAfter(self._open_doc_chat_dialog, final_res_string.strip(), attachments, final_res_string.strip(), final_res_string.strip())
            else:
                # Translators: Error message reported when video segment analysis fails after multiple retries due to network issues.
                report_err = seg_res[6:] if seg_res and seg_res.startswith("ERROR:") else _("Connection failed after retries.")
                log.error(f"Video analysis failed permanently: {report_err}")
                if prog_dlg: wx.CallAfter(prog_dlg.on_error, report_err)
                else: wx.CallAfter(show_error_dialog, report_err)

            if not prog_dlg: wx.CallAfter(setattr, self, 'current_status', _("Idle"))
        except Exception as e:
            log.error(f"{source.log_label}: {e}", exc_info=True)
            report(source.error_message)
            if not prog_dlg: wx.CallAfter(setattr, self, 'current_status', _("Idle"))
        finally:
            source.cleanup()


    def _compress_video(self, input_path):
        ffmpeg_path = self._ensure_ffmpeg()
        if not ffmpeg_path:
            return None

        fd, temp_path = tempfile.mkstemp(suffix=".mp4", prefix="vision_assistant_comp_")
        os.close(fd)

        cmd = [
            ffmpeg_path,
            "-i", input_path,
            "-vf", "scale=-2:min(480\\,ih)",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "30",
            "-c:a", "aac",
            "-b:a", "64k",
            "-movflags", "+faststart",
            "-y",
            temp_path
        ]

        startupinfo = None
        creationflags = 0
        if sys.platform == "win32":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            creationflags = 0x08000000

        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, creationflags=creationflags, check=True)
            try:
                if os.path.getsize(temp_path) >= os.path.getsize(input_path):
                    os.remove(temp_path)
                    return input_path
            except Exception: pass
            return temp_path
        except subprocess.CalledProcessError as e:
            log.error(f"Video compression failed: {e.stderr}")
            try:
                os.remove(temp_path)
            except Exception: pass
            return None



    def _ensure_ffmpeg(self):

        ffmpeg_lib_path = os.path.join(lib_dir, "ffmpeg.exe")

        if os.path.exists(ffmpeg_lib_path):
            return ffmpeg_lib_path

        try:
            result = subprocess.run(["ffmpeg", "-version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                return "ffmpeg"
        except Exception:
            pass

        # Translators: Title of dialog asking user to download ffmpeg
        title = _("Download ffmpeg?")
        # Translators: Message asking user to download ffmpeg for video recording
        message = _(
            "Screen recording requires ffmpeg (approximately 70MB download).\n\n"
            "Download ffmpeg now to the addon's lib folder?\n\n"
            "This is a one-time download."
        )

        user_choice = [wx.ID_NO]
        dlg_closed = threading.Event()

        def ask_user():
            gui.mainFrame.prePopup()
            try:
                dlg = wx.MessageDialog(gui.mainFrame, message, title, wx.YES_NO | wx.ICON_QUESTION)
                user_choice[0] = dlg.ShowModal()
                dlg.Destroy()
            finally:
                gui.mainFrame.postPopup()
                dlg_closed.set()

        wx.CallAfter(ask_user)
        dlg_closed.wait()

        if user_choice[0] != wx.ID_YES:
            # Translators: Message when user cancels ffmpeg download
            wx.CallAfter(ui.message, _("Recording cancelled. ffmpeg is required for video recording."))
            return None

        return self._download_ffmpeg(ffmpeg_lib_path)

    def _download_ffmpeg(self, target_path):
        try:
            # Translators: Status message when downloading ffmpeg
            msg_start = _("Downloading ffmpeg, please wait...")
            wx.CallAfter(self.report_status, msg_start)

            download_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

            opener = get_proxy_opener(download_url)
            req = request.Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})

            zip_path = target_path + ".zip"
            with opener.open(req, timeout=300) as response:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                with open(zip_path, 'wb') as f:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            # Translators: Progress message during ffmpeg download, {percent} is download percentage
                            self.current_status = _("Downloading ffmpeg: {percent}%").format(percent=percent)

                            if downloaded % (10 * 1024 * 1024) < 1024 * 1024:
                                wx.CallAfter(ui.message, self.current_status)

            # Translators: Status message when extracting ffmpeg
            self.current_status = _("Extracting ffmpeg...")
            wx.CallAfter(ui.message, self.current_status)
            

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                ffmpeg_file = None
                for name in zip_ref.namelist():
                    if name.endswith('bin/ffmpeg.exe'):
                        ffmpeg_file = name
                        break

                if ffmpeg_file:
                    temp_extract = os.path.join(tempfile.gettempdir(), "ffmpeg_temp_extract")
                    os.makedirs(temp_extract, exist_ok=True)
                    zip_ref.extract(ffmpeg_file, temp_extract)

                    extracted_path = os.path.join(temp_extract, ffmpeg_file)
                    
                    shutil.move(extracted_path, target_path)

                    try:
                        shutil.rmtree(temp_extract)
                    except Exception:
                        pass

            try:
                os.remove(zip_path)
            except Exception:
                pass

            if os.path.exists(target_path):
                # Translators: Success message after ffmpeg download completes
                msg_success = _("ffmpeg downloaded successfully!")
                wx.CallAfter(self.report_status, msg_success)
                wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                return target_path
            else:
                raise Exception("Failed to extract ffmpeg.exe")

        except Exception as e:
            log.error(f"ffmpeg download failed: {e}", exc_info=True)
            # Translators: Error message when ffmpeg download fails
            wx.CallAfter(show_error_dialog, _("Failed to download ffmpeg: {error}").format(error=str(e)))
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))
            return None


    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Starts or stops local video recording of the screen."))
    def script_recordLocalVideo(self, gesture):
        if self.toggling:
            self.finish()

        if not self.is_video_recording:
            threading.Thread(target=self._start_local_video_recording, daemon=True).start()
        else:
            threading.Thread(target=self._stop_and_analyze_recording, daemon=True).start()


    def _start_local_video_recording(self, force_desktop=False):
        if not AIHandler.is_gemini():
            # Translators: Error message when video recording is attempted with a non-Gemini provider
            wx.CallAfter(self.report_status, _("Video recording is only supported by Gemini providers."))
            return

        if check_screen_curtain_active():
            return

        ffmpeg_path = self._ensure_ffmpeg()
        if not ffmpeg_path:
            return

        try:
            fd, temp_path = tempfile.mkstemp(suffix=".mp4", prefix="vision_assistant_rec_")
            os.close(fd)
            self.recording_output_path = temp_path

            if not force_desktop:
                # Translators: Status message reported when starting video recording
                wx.CallAfter(self.report_status, _("Starting recording..."))

            crop_filter = ""
            
            if not force_desktop:
                try:
                    fg_obj = api.getForegroundObject()
                    if fg_obj and fg_obj.location:
                        x, y, w, h = fg_obj.location
                        

                        screen_w = ctypes.windll.user32.GetSystemMetrics(0)
                        screen_h = ctypes.windll.user32.GetSystemMetrics(1)

                        if x < 0:
                            w += x
                            x = 0
                        if y < 0:
                            h += y
                            y = 0
                            
                        if x + w > screen_w:
                            w = screen_w - x
                        if y + h > screen_h:
                            h = screen_h - y

                        if w > 100 and h > 100:
                            w = w if w % 2 == 0 else w - 1
                            h = h if h % 2 == 0 else h - 1
                            crop_filter = f"crop={w}:{h}:{x}:{y},"
                except Exception as e:
                    log.warning(f"Failed to calculate window dimensions: {e}")

            cmd = [
                ffmpeg_path,
                "-f", "gdigrab",
                "-framerate", "15",
                "-i", "desktop",
            ]

            vf_string = f"{crop_filter}scale=854:-2,format=yuv420p"

            cmd.extend([
                "-vf", vf_string,
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "28",
                "-y",
                temp_path
            ])

            startupinfo = None
            creationflags = 0
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
                creationflags = 0x08000000

            self.recording_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                startupinfo=startupinfo,
                creationflags=creationflags
            )

            self.is_video_recording = True
            self.recording_start_time = time.time()

            def check_process_status():
                if self.is_video_recording and self.recording_process:
                    if self.recording_process.poll() is not None:
                        self.recording_process = None
                        self.is_video_recording = False
                        
                        if not force_desktop:
                            log.warning("ffmpeg crashed on window capture. Retrying full screen.")
                            # Translators: Message when window capture fails and switches to full screen capture
                            wx.CallAfter(ui.message, _("Window capture failed. Trying full screen..."))
                            threading.Thread(target=self._start_local_video_recording, args=(True,), daemon=True).start()
                        else:
                            # Translators: Error message when ffmpeg fails completely
                            wx.CallAfter(show_error_dialog, _("Recording failed to start. FFmpeg encountered a fatal error."))

            wx.CallAfter(wx.CallLater, 2000, check_process_status)

            if not force_desktop:
                # Translators: Message when video recording starts
                msg = _("Recording started. Press the same shortcut again to stop.")
                def announce_start():
                    if self.is_video_recording:
                        tones.beep(800, 100)
                        self.report_status(msg)
                wx.CallAfter(wx.CallLater, 2500, announce_start)

        except Exception as e:
            log.error(f"Failed to start recording: {e}", exc_info=True)
            self.is_video_recording = False
            self.recording_process = None
            # Translators: Error message when recording fails to start
            show_error_dialog(_("Failed to start recording: {error}").format(error=str(e)))

    def _stop_and_analyze_recording(self):
        if not self.is_video_recording or not self.recording_process:
            return

        try:
            self.is_video_recording = False

            try:
                self.recording_process.communicate(input=b'q', timeout=5)
            except Exception:
                try:
                    self.recording_process.terminate()
                except Exception:
                    pass

            time.sleep(0.5)

            duration = time.time() - self.recording_start_time if self.recording_start_time else 0

            wx.CallAfter(tones.beep, 400, 100)

            if not os.path.exists(self.recording_output_path):
                log.error("Recording file not found after stopping ffmpeg")
                # Translators: Error when recorded video file is not found
                wx.CallAfter(show_error_dialog, _("Recording file not found."))
                return

            file_size = os.path.getsize(self.recording_output_path)
            size_mb = file_size / (1024 * 1024)

            if file_size < 1024:
                log.error(f"Recording file too small: {file_size} bytes")
                # Translators: Error when recorded video file is too small/corrupted
                wx.CallAfter(show_error_dialog, _("The recording was too short or the video file is corrupted. Please try recording for at least a few seconds."))
                return

            # Translators: Status message showing recording info, {duration} is seconds, {size} is MB
            wx.CallAfter(ui.message, _("Recording stopped ({duration:.0f} seconds, {size:.1f} MB)").format(
                duration=duration, size=size_mb
            ))

            def report(msg):
                if _vision_assistant_instance:
                    _vision_assistant_instance.current_status = msg
                wx.CallAfter(ui.message, msg)

            file_uri, _dur, current_key = GeminiHandler.upload_and_get_duration(self.recording_output_path, report_callback=report)

            if not file_uri:
                log.error("Upload returned None - upload failed")
                wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                return

            lang = get_lang_name("ai_response_language")
            video_template = get_prompt_text("local_video_recording")
            prompt = apply_prompt_template(video_template, [("response_lang", lang)])

            # Translators: Message when AI is analyzing the recorded video
            report(_("Analyzing video..."))

            res, file_uri, current_key = GeminiHandler.process_video_task(
                self.recording_output_path, prompt, None, None, False, report, None, file_uri, current_key, False
            )

            if res:
                if res.startswith("ERROR:"):
                    log.error(f"Video analysis error: {res}")
                    wx.CallAfter(show_error_dialog, res[6:])
                else:
                    chat_attachments = [{'mime_type': 'video/mp4', 'file_uri': file_uri}]
                    wx.CallAfter(self._open_doc_chat_dialog, res, chat_attachments, res, res)

            wx.CallAfter(setattr, self, 'current_status', _("Idle"))

        except Exception as e:
            log.error(f"Failed to process recording: {e}", exc_info=True)
            # Translators: Error message when processing recorded video fails
            wx.CallAfter(show_error_dialog, _("Failed to process recording: {error}").format(error=str(e)))
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))
        finally:
            self.recording_process = None
            if self.recording_output_path and os.path.exists(self.recording_output_path):
                try:
                    os.remove(self.recording_output_path)
                except Exception:
                    pass
            self.recording_output_path = None
            self.recording_start_time = None

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Attempts to solve a CAPTCHA on the screen or navigator object."))
    def script_solveCaptcha(self, gesture):
        if self.toggling: self.finish()
        if check_screen_curtain_active():
            return
        mode = config.conf["VisionAssistant"]["captcha_mode"]
        if mode == 'fullscreen': d, w, h, m = self._capture_fullscreen()
        else: d, w, h, m = self._capture_navigator()
        
        is_gov = False
        try:
            if api.getForegroundObject() and "پنجره ملی خدمات دولت هوشمند" in api.getForegroundObject().name: 
                is_gov = True
        except Exception: pass

        if d:
            # Translators: Message reported by NVDA when the user triggers the CAPTCHA solving command.
            msg = _("Solving...")
            self.report_status(msg)
            threading.Thread(target=self._thread_cap, args=(d, m, is_gov), daemon=True).start()
        else: 
            # Translators: Error message reported when screen or object capture fails for CAPTCHA solving.
            msg = _("Capture failed.")
            self.report_status(msg)
        
    def _thread_cap(self, d, m, is_gov):
        cap_template = get_prompt_text("captcha_solver_base")
        cap_extra = " Read 5 Persian digits, convert to English." if is_gov else " Convert to English digits."
        p = apply_prompt_template(cap_template, [("captcha_extra", cap_extra)])
        
        r = AIHandler.call(p, attachments=[{'mime_type': m, 'data': d}])
        if r:
            if r.startswith("ERROR:"):
                wx.CallAfter(setattr, self, 'current_status', _("Idle"))
                wx.CallAfter(show_error_dialog, r[6:])
                return
            
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))
            
            if "[[[NO_CAPTCHA]]]" in r:
                # Translators: Message reported by NVDA when the AI cannot detect any CAPTCHA in the captured image.
                wx.CallAfter(self.report_status, _("No CAPTCHA detected."))
            else:
                wx.CallAfter(self._finish_captcha, r.strip())
        else: 
            wx.CallAfter(setattr, self, 'current_status', _("Idle"))

    def _finish_captcha(self, text):
        clean_text = re.sub(r'[^a-zA-Z0-9]', '', text)
        for char in clean_text:
            try:
                keyboardHandler.KeyboardInputGesture.fromName(char).send()
            except Exception:
                vk = winUser.user32.VkKeyScanW(ord(char)) & 0xFF
                winUser.keybd_event(vk, 0, 0, 0)
                winUser.keybd_event(vk, 0, 2, 0)
            time.sleep(0.02)
        tones.beep(1000, 100)
        # Translators: Message reported by NVDA after successfully solving a text CAPTCHA, announcing the characters found.
        msg = _("Captcha: {text}").format(text=clean_text)
        self.report_status(msg)


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
            if not obj or not obj.location: return None, 0, 0, ""
            x, y, w, h = obj.location
            if w < 1 or h < 1: return None, 0, 0, ""
            bmp = wx.Bitmap(w, h)
            wx.MemoryDC(bmp).Blit(0, 0, w, h, wx.ScreenDC(), x, y)
            s = io.BytesIO()
            img = bmp.ConvertToImage()
            img.SetOption("quality", 90)
            img.SaveFile(s, wx.BITMAP_TYPE_JPEG)
            m = "image/jpeg"
            return base64.b64encode(s.getvalue()).decode('utf-8'), w, h, m
        except Exception as e:
            log.error(f"Screen capture failed: {e}")
            return None, 0, 0, ""

    def _capture_fullscreen(self):
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            dpi = 96
            if hwnd:
                try:
                    dpi = int(ctypes.windll.user32.GetDpiForWindow(hwnd))
                except Exception:
                    dpi = 96
            if dpi <= 0:
                dpi = 96
            scale = dpi / 96.0

            w_logical, h_logical = wx.GetDisplaySize()
            w_physical = int(round(w_logical * scale))
            h_physical = int(round(h_logical * scale))

            bmp = wx.Bitmap(w_physical, h_physical)
            screen = wx.ScreenDC()
            memory = wx.MemoryDC()
            memory.SelectObject(bmp)
            try:
                memory.Blit(0, 0, w_physical, h_physical, screen, 0, 0)
            finally:
                memory.SelectObject(wx.NullBitmap)

            image = bmp.ConvertToImage()
            if scale != 1.0:
                image = image.Scale(w_logical, h_logical, wx.IMAGE_QUALITY_HIGH)

            s = io.BytesIO()
            image.SetOption("quality", 90)
            image.SaveFile(s, wx.BITMAP_TYPE_JPEG)
            m = "image/jpeg"
            return base64.b64encode(s.getvalue()).decode('utf-8'), w_logical, h_logical, m
        except Exception as e:
            log.error(f"DPI-aware capture failed: {e}", exc_info=True)
            return None, 0, 0, ""

    def _capture_foreground(self):
        try:
            obj = api.getForegroundObject()
            if not obj or not obj.location: return None, 0, 0, 0, 0, ""
            x, y, w, h = obj.location
            if w < 1 or h < 1: return None, 0, 0, 0, 0, ""
            bmp = wx.Bitmap(w, h)
            wx.MemoryDC(bmp).Blit(0, 0, w, h, wx.ScreenDC(), x, y)
            s = io.BytesIO()
            img = bmp.ConvertToImage()
            img.SetOption("quality", 90)
            img.SaveFile(s, wx.BITMAP_TYPE_JPEG)
            m = "image/jpeg"
            return base64.b64encode(s.getvalue()).decode('utf-8'), x, y, w, h, m
        except Exception as e: 
            log.error(f"Foreground capture failed: {e}")
            return None, 0, 0, 0, 0, ""    

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

    # Translators: Script description for Input Gestures dialog
    @scriptHandler.script(description=_("Shows the last AI response in a chat dialog for review or follow-up questions."))
    def script_showLastResult(self, gesture):
        if self.toggling: self.finish()
        if self.live_session:
            self._show_live_window()
            return
        if not self._last_result_data:
            # Translators: Message reported when the user tries to show the last result but none is stored.
            ui.message(_("No previous result to show."))
            return
        
        func, args = self._last_result_data
        wx.CallAfter(func, *args, force_show=True, is_recall=True)

    def on_settings_click(self, event):
        instance = getattr(gui.settingsDialogs.NVDASettingsDialog, "instance", None)
        if instance:
            try:
                instance.Show(True)
                instance.Raise()
                instance.SetFocus()
                if hasattr(instance, "setPanel"):
                    instance.setPanel(SettingsPanel)
                return
            except Exception:
                gui.settingsDialogs.NVDASettingsDialog.instance = None

        def _force_open():
            gui.settingsDialogs.NVDASettingsDialog.instance = None
            try:
                gui.mainFrame.prePopup()
                new_inst = gui.settingsDialogs.NVDASettingsDialog(gui.mainFrame, SettingsPanel)
                new_inst.Show()
                new_inst.Raise()
                gui.mainFrame.postPopup()
            except Exception:
                gui.settingsDialogs.NVDASettingsDialog.instance = None
                try:
                    gui.mainFrame.postPopup()
                except Exception:
                    pass

        wx.CallLater(100, _force_open)

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
            wx.CallAfter(donate_dialog.requestDonations, gui.mainFrame)
        except Exception as e:
            show_error_dialog(str(e))
            
    def on_telegram_click(self, event):
        try:
            os.startfile("https://t.me/VisionAssistantPro")
        except Exception as e:
            show_error_dialog(str(e))

    # Translators: Script description for Input Gestures dialog.
    @scriptHandler.script(description=_("Toggles the interactive UI elements explorer."))
    def script_toggleUIExplorer(self, gesture):
        if self.toggling: self.finish()
        if not self.is_ui_explorer_active:
            self.is_ui_explorer_active = True
            # Translators: Status message when UI Explorer starts
            self.report_status(_("UI Explorer Active"))
            wx.CallAfter(lambda: threading.Thread(target=self._thread_ui_explorer, daemon=True).start())
        else:
            self.is_ui_explorer_active = False
            # Translators: Status message when UI Explorer stops
            self.report_status(_("UI Explorer Stopped"))
            tones.beep(200, 100)

    def _thread_ui_explorer(self):
        if not self.is_ui_explorer_active: return
        if check_screen_curtain_active():
            self.is_ui_explorer_active = False
            return
        time.sleep(0.5)
        img, w, h, m = self._capture_fullscreen()
        if not img: 
            self.is_ui_explorer_active = False
            return
        tones.beep(800, 50)
        fg_app = api.getForegroundObject().appModule.appName
        prompt_template = get_prompt_text("ui_explorer_system")
        prompt = apply_prompt_template(prompt_template, [("app_name", fg_app)])
        res = AIHandler.call(prompt, attachments=[{'mime_type': m, 'data': img}], json_mode=True, task="operator")
        if not res or res.startswith("ERROR:"):
            self.is_ui_explorer_active = False
            # Translators: Generic error message for AI failures
            err_msg = res[6:] if res else _("Unknown AI Error")
            wx.CallAfter(show_error_dialog, err_msg)
            return
        try:
            clean_res = res.strip()
            if "```json" in clean_res: clean_res = clean_res.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_res: clean_res = clean_res.split("```")[1].split("```")[0].strip()
            elements = json.loads(clean_res)
            tones.beep(1000, 100)
            wx.CallAfter(self._show_elements_selector, elements, w, h)
        except Exception as e:
            log.error(f"UI Explorer parsing failed: {e}")
            if self.is_ui_explorer_active:
                self.is_ui_explorer_active = False
                # Translators: Error shown when AI fails to find UI elements
                wx.CallAfter(show_error_dialog, _("AI failed to identify UI elements."))

    def _show_elements_selector(self, elements, sw, sh):
        if not self.is_ui_explorer_active: return
        choices, valid_elements = [], []
        for el in elements:
            label = el.get('label', '').strip()
            if label and label not in choices:
                choices.append(label)
                valid_elements.append(el)
        if not choices:
            self.is_ui_explorer_active = False
            return
        gui.mainFrame.prePopup()
        # Translators: Instruction for the elements list dialog
        dlg = wx.SingleChoiceDialog(gui.mainFrame, _("Select an element to click:"), _("UI Elements Explorer"), choices)
        if dlg.ShowModal() == wx.ID_OK:
            idx = dlg.GetSelection()
            target = valid_elements[idx]
            x, y = int(target['x'] * sw / 1000), int(target['y'] * sh / 1000)
            dlg.Destroy()
            gui.mainFrame.postPopup()
            self._do_mouse_action(x, y, "click")
            wx.CallLater(2000, lambda: threading.Thread(target=self._thread_ui_explorer, daemon=True).start())
        else:
            self.is_ui_explorer_active = False
            dlg.Destroy()
            gui.mainFrame.postPopup()
            # Translators: Status message when UI Explorer stops
            self.report_status(_("UI Explorer Stopped"))

    # Translators: Script description for Input Gestures dialog.
    @scriptHandler.script(description=_("Asks the AI Operator to perform an action or describe the screen."))
    def script_aiOperatorAction(self, gesture):
        if self.toggling: self.finish()
        if getattr(self, "_dialog_open", False):
            return
        if getattr(self, "_is_operator_running", False):
            self._abort_operator = True
            self._is_operator_running = False
            # Translators: Announcement when the AI Operator is manually stopped
            ui.message(_("AI Operator stopped."))
            tones.beep(300, 150)
            return

        def show_cmd_dialog():
            self._dialog_open = True
            gui.mainFrame.prePopup()
            # Translators: Title and message for AI Operator command dialog
            dlg = wx.TextEntryDialog(gui.mainFrame, _("What should I do or what is your question?"), _("AI Operator"))
            if dlg.ShowModal() == wx.ID_OK:
                command = dlg.GetValue()
                dlg.Destroy()
                gui.mainFrame.postPopup()
                self._dialog_open = False

                time.sleep(0.5) 
                
                if command.strip():
                    self._operator_history = []
                    # Translators: Status reported when AI starts processing a command
                    wx.CallLater(300, self.report_status, _("Processing..."))
                    self._operator_thread_token = getattr(self, "_operator_thread_token", 0) + 1
                    token = self._operator_thread_token
                    wx.CallLater(800, lambda: threading.Thread(target=self._thread_ai_computer_use, args=(command, token), daemon=True).start())
                return
            dlg.Destroy()
            gui.mainFrame.postPopup()
            self._dialog_open = False
        wx.CallAfter(show_cmd_dialog)

    def _thread_ai_computer_use(self, user_command, token):
        self._abort_operator = False
        self._is_operator_running = True
        try:
            max_turns = 10
            current_command = user_command
            if not self._operator_history: self._operator_history = []
            resp_lang = get_lang_name("ai_response_language")
            fg_app = api.getForegroundObject().appModule.appName
            is_gemini = AIHandler.is_gemini()
            for turn in range(max_turns):
                if self._should_abort(token):
                    break
                
                if turn > 0:
                    for i in range(35):
                        if self._should_abort(token):
                            break
                        time.sleep(0.1)
                    if self._should_abort(token):
                        break

                time.sleep(0.5)
                if self._should_abort(token):
                    break
                
                img, w, h, m = self._capture_fullscreen()
                if not img: break
                if self._should_abort(token):
                    break
                
                tones.beep(800, 50)
                system_template = get_prompt_text("ai_operator_system")
                prompt = apply_prompt_template(system_template, [("user_command", current_command), ("response_lang", resp_lang), ("app_name", fg_app)])
                
                messages = []
                for item in self._operator_history:
                    role = item["role"]
                    content = item.get("content") or ""
                    if "{" in content and "explanation" in content:
                        try:
                            exp_match = re.search(r'"explanation":\s*"([^"]*)"', content)
                            if exp_match:
                                content = exp_match.group(1)
                        except Exception: pass
                    if is_gemini:
                        messages.append({"role": "user" if role == "user" else "model", "parts": [{"text": content}]})
                    else:
                        messages.append({"role": role if role != "model" else "assistant", "content": content})
                
                if is_gemini:
                    messages.append({"role": "user", "parts": [{"text": prompt}, {"inline_data": {"mime_type": m, "data": img}}]})
                else:
                    messages.append({"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:{m};base64,{img}"}}
                    ]})

                res = AIHandler.call(messages, task="operator")
                
                if self._should_abort(token):
                    break
                
                if not res or res.startswith("ERROR:"):
                    # Translators: Fallback error message shown in the AI Operator if the server returns an empty or invalid response.
                    wx.CallAfter(show_error_dialog, res[6:] if res else _("AI Error"))
                    break
                    
                display_text, is_finished, action_info = self._process_ai_action_logic(res, w, h)
                
                # Translators: Internal history label for user actions in operator sessions
                hist_user = current_command if turn == 0 else _("Action performed. Checking result...")
                self._operator_history.append({"role": "user", "content": hist_user})
                self._operator_history.append({"role": "assistant", "content": res})
                
                if not self._should_abort(token):
                    self._last_result_data = (self._open_operator_chat_dialog, (display_text, {"last_w": w, "last_h": h}))
                    wx.CallAfter(ui.message, clean_markdown(display_text))
                
                if action_info:
                    if self._should_abort(token):
                        break
                    for i in range(20):
                        if self._should_abort(token):
                            break
                        time.sleep(0.1)
                    if self._should_abort(token):
                        break
                        
                    act, rx, ry, txt_val, p_ent, scroll_dir, keys_val, rsx, rsy = action_info
                    if act == "type" and txt_val:
                        self._do_type(rx, ry, txt_val, p_ent)
                    elif act == "keypress" and keys_val:
                        self._do_keypress(keys_val)
                    elif act == "scroll":
                        self._do_mouse_action(rx, ry, act, scroll_direction=scroll_dir)
                    else:
                        self._do_mouse_action(rx, ry, act, start_x=rsx, start_y=rsy)
                    tones.beep(1000, 100)

                if is_finished or ("{" not in res and not action_info):
                    if self._should_abort(token):
                        break
                    if config.conf["VisionAssistant"]["copy_to_clipboard"]:
                        api.copyToClip(display_text)
                    if not config.conf["VisionAssistant"]["skip_chat_dialog"]:
                        wx.CallAfter(self._open_operator_chat_dialog, display_text, {"last_w": w, "last_h": h})
                    break
                
                if self._should_abort(token):
                    break
                time.sleep(2.5)             
                current_command = "The action was initiated. Continue if necessary."
        finally:
            if not self._should_abort(token):
                self._is_operator_running = False
                self._abort_operator = False
                self.current_status = _("Idle")

    def _open_operator_chat_dialog(self, text, context, force_show=False, is_recall=False):
        self._last_result_data = (self._open_operator_chat_dialog, (text, context))
        if config.conf["VisionAssistant"]["skip_chat_dialog"] and not force_show:
            return
        if self.vision_dlg:
            try: self.vision_dlg.Destroy()
            except Exception: pass
            self.vision_dlg = None

        def operator_callback(ctx, q, history, extra):
            self._operator_history = []
            for h in history:
                role = "user" if h["role"] == "user" else "assistant"
                text_val = h.get("content") or (h.get("parts", [{}])[0].get("text", "") if h.get("parts") else "")
                if text_val and text_val != q:
                    self._operator_history.append({"role": role, "content": text_val})
            
            wx.CallAfter(self.vision_dlg.Close)
            self._operator_thread_token = getattr(self, "_operator_thread_token", 0) + 1
            token = self._operator_thread_token
            threading.Thread(target=self._thread_ai_computer_use, args=(q, token), daemon=True).start()
            return None, None

        if not is_recall:
            tones.beep(1000, 100)

        # Translators: The title of the interactive chat dialog for the AI Operator feature.
        title_text = _("{name} - AI Operator").format(name=ADDON_NAME)
        self.vision_dlg = VisionQADialog(gui.mainFrame, title_text, text, context, operator_callback, status_callback=self.report_status)
        
        if self._operator_history:
            dialog_history = []
            self.vision_dlg.outputArea.Clear()
            for h in self._operator_history:
                role = "user" if h["role"] == "user" else "model"
                content = h.get("content") or h.get("parts", [{}])[0].get("text", "")
                dialog_history.append({"role": role, "parts": [{"text": content}]})
                # Translators: Labels for the AI and User in chat history
                role_label = _("Operator") if h["role"] in ["assistant", "model"] else _("You")
                content_only = ""
                try:
                    if "{" in content:
                        json_match = re.search(r'\{.*\}', content, flags=re.DOTALL)
                        if json_match:
                            data = json.loads(json_match.group(0))
                            content_only = data.get("explanation", "")
                except Exception: pass
                if not content_only: 
                    content_only = re.sub(r'\{.*\}', '', content, flags=re.DOTALL).strip()
                if "Windows operator" not in content and content_only:
                    self.vision_dlg.outputArea.AppendText(f"{role_label}: {clean_markdown(content_only)}\n\n")
            self.vision_dlg.chat_history = dialog_history

        self.vision_dlg.Show()
        self.vision_dlg.Raise()
        self.vision_dlg.SetFocus()

    def _process_ai_action_logic(self, res, sw, sh):
        is_finished = False
        action_info = None
        clean_text = res
        exp_match = re.search(r'"explanation":\s*"([^"]*)"', res)
        if exp_match:
            clean_text = exp_match.group(1)
        else:
            clean_text = re.sub(r'\{.*\}', '', res, flags=re.DOTALL).strip()
            if not clean_text: clean_text = res

        try:
            json_match = re.search(r'\{.*\}', res.replace('\n', ' '))
            if json_match:
                json_str = json_match.group(0)
                try:
                    data = json.loads(json_str)
                    x, y = data.get("x") or data.get("end_x"), data.get("y") or data.get("end_y")
                    start_x, start_y = data.get("start_x"), data.get("start_y")
                    action = data.get("action", "click")
                    is_finished = data.get("finished", False)
                    explanation = data.get("explanation", clean_text)
                    t_val = data.get("text", "")
                    scroll_dir = data.get("scroll_direction", "down")
                    keys_val = data.get("keys", "")
                except Exception:
                    x_m = re.search(r'"(?:end_)?x":\s*(\d+)', json_str)
                    y_m = re.search(r'"(?:end_)?y":\s*(\d+)', json_str)
                    sx_m = re.search(r'"start_x":\s*(\d+)', json_str)
                    sy_m = re.search(r'"start_y":\s*(\d+)', json_str)
                    x = int(x_m.group(1)) if x_m else None
                    y = int(y_m.group(1)) if y_m else None
                    start_x = int(sx_m.group(1)) if sx_m else None
                    start_y = int(sy_m.group(1)) if sy_m else None
                    action = "click"
                    act_m = re.search(r'"action":\s*"([^"]*)"', json_str)
                    if act_m: action = act_m.group(1)
                    is_finished = bool(re.search(r'"finished":\s*true', json_str.lower()))
                    explanation = clean_text
                    t_m = re.search(r'"text":\s*"([^"]*)"', json_str)
                    t_val = t_m.group(1) if t_m else ""
                    scroll_dir = "down"
                    keys_val = ""

                if x is not None and y is not None:
                    real_x, real_y = int(x * sw / 1000), int(y * sh / 1000)
                    real_start_x = int(start_x * sw / 1000) if start_x is not None else None
                    real_start_y = int(start_y * sh / 1000) if start_y is not None else None
                    p_ent = t_val.endswith("\n") or "اینتر" in explanation or "enter" in explanation.lower()
                    action_info = (action, real_x, real_y, t_val, p_ent, scroll_dir, keys_val, real_start_x, real_start_y)

                return explanation, is_finished, action_info
            else:
                return clean_text, True, None
        except Exception:
            return clean_text, True, None

    def _do_mouse_action(self, x, y, action_type, scroll_direction="down", start_x=None, start_y=None):
        try:
            if action_type == "scroll":
                MouseSimulator.scroll(x, y, direction=scroll_direction, clicks=3)
            elif action_type == "drag":
                if start_x is None or start_y is None:
                    start_x, start_y = x, y
                MouseSimulator.drag(start_x, start_y, x, y, duration=0.8, steps=40)
            elif action_type == "right_click":
                MouseSimulator.click(x, y, button="right")
            elif action_type == "double_click":
                MouseSimulator.click(x, y, button="left", double=True)
            else:
                MouseSimulator.click(x, y, button="left")
            time.sleep(0.2)
        except Exception as e:
            log.error(f"Mouse action failed: {e}", exc_info=True)
            try:
                winUser.setCursorPos(int(x), int(y))
                time.sleep(0.1)
                mouseHandler.doPrimaryClick()
            except Exception as e2:
                log.error(f"Mouse fallback also failed: {e2}")

    def _do_keypress(self, key_name):
        VK_MAP = {
            "enter": 0x0D,
            "return": 0x0D,
            "tab": 0x09,
            "escape": 0x1B,
            "esc": 0x1B,
            "up": 0x26,
            "down": 0x28,
            "left": 0x25,
            "right": 0x27,
            "space": 0x20,
            "backspace": 0x08,
            "delete": 0x2E,
            "home": 0x24,
            "end": 0x23,
            "pageup": 0x21,
            "pagedown": 0x22,
            "insert": 0x2D,
            "f1": 0x70, "f2": 0x71, "f3": 0x72, "f4": 0x73,
            "f5": 0x74, "f6": 0x75, "f7": 0x76, "f8": 0x77,
            "f9": 0x78, "f10": 0x79, "f11": 0x7A, "f12": 0x7B,
        }
        EXTENDED_KEYS = {"up", "down", "left", "right", "home", "end", 
                         "pageup", "pagedown", "insert", "delete"}
        key_lower = str(key_name).lower()
        vk = VK_MAP.get(key_lower)
        if vk:
            extended = key_lower in EXTENDED_KEYS
            MouseSimulator.key_press(vk, extended=extended)
            time.sleep(0.15)
        else:
            log.warning(f"Unknown key name: {key_name}")

    def _do_type(self, x, y, text, press_enter=False):
        try:
            MouseSimulator.click(x, y, button="left")
            time.sleep(0.3)
            VK_CONTROL = 0x11
            VK_A = 0x41
            inputs = [
                MouseSimulator._make_keyboard_input(VK_CONTROL, 0),
                MouseSimulator._make_keyboard_input(VK_A, 0),
                MouseSimulator._make_keyboard_input(VK_A, KEYEVENTF_KEYUP),
                MouseSimulator._make_keyboard_input(VK_CONTROL, KEYEVENTF_KEYUP),
            ]
            MouseSimulator._send_inputs(*inputs)
            time.sleep(0.1)
            MouseSimulator.key_press(0x2E)
            time.sleep(0.1)
            MouseSimulator.type_text(text, press_enter=press_enter)
        except Exception as e:
            log.error(f"Type action failed: {e}", exc_info=True)

    def _should_abort(self, token):
        return getattr(self, "_abort_operator", False) or token != getattr(self, "_operator_thread_token", 0)

    def _getAppId(self, obj):
        try:
            appName = obj.appModule.appName.lower()
        except Exception:
            appName = "unknown_app"
            
        if appName == "applicationframehost":
            try:
                fg = api.getForegroundObject()
                if fg and fg.name:
                    return f"{appName}_{fg.name}"
            except Exception: pass
        return appName

    def chooseNVDAObjectOverlayClasses(self, obj, clsList):
        if not hasattr(self, "labels_cache"):
            return
        
        app_module = getattr(obj, "appModule", None)
        if not app_module:
            return
            
        app_name = app_module.appName.lower()
        if app_name in ["chrome", "msedge", "firefox", "opera", "brave"]:
            return

        class_name = getattr(obj, "windowClassName", None)
        if class_name == "Internet Explorer_Server":
            return

        uniqueId = self._getAppId(obj)
        if uniqueId not in self.labels_cache:
            return

        key = _generate_object_signature(obj)
        if key and key in self.labels_cache[uniqueId]:
            clsList.insert(0, CustomLabelOverlay)
            return

    # Translators: Script description for the 'Label Object' command in the Input Gestures dialog. This command sends the current UI element to AI to generate a descriptive name.
    @scriptHandler.script(description=_("Labels the current navigator object using AI."))
    def script_labelObject(self, gesture):
        if self.toggling: self.finish()
        obj = api.getNavigatorObject()
        if not obj or not obj.location: return

        if check_screen_curtain_active():
            return

        uniqueId = self._getAppId(obj)
        if uniqueId in ["chrome", "msedge", "firefox", "opera", "brave"]:
            # Translators: Message shown when a user tries to use AI labeling in a web browser.
            ui.message(_("AI Labeling is currently not supported in web browsers."))
            return

        loc = obj.location
        sig_key = _generate_object_signature(obj)
        old_key = f"{int(obj.role)}:{loc.left},{loc.top}" if loc else None
        
        is_labeled = False
        found_label = ""
        if uniqueId in self.labels_cache:
            if sig_key and sig_key in self.labels_cache[uniqueId]:
                is_labeled = True
                found_label = self.labels_cache[uniqueId][sig_key]
            elif old_key and old_key in self.labels_cache[uniqueId]:
                is_labeled = True
                found_label = self.labels_cache[uniqueId][old_key]
                
        if is_labeled:
            # Translators: Message spoken by NVDA when the current object already has a custom or AI-generated label. {name} is replaced with the existing label text.
            ui.message(_("Already labeled as: {name}").format(name=found_label))
            return

        tones.beep(800, 100)
        # Translators: Progress message spoken when the add-on starts taking a screenshot of the current focused object.
        self.current_status = _("Identifying object...")
        ui.message(self.current_status)
        
        def worker():
            img, w, h, m = self._capture_navigator()
            if not img:
                self.current_status = _("Idle")
                return
            # Translators: Progress message spoken when the add-on has sent the image to the AI and is waiting for the AI to return a label.
            self.current_status = _("Analyzing...")
            wx.CallAfter(ui.message, self.current_status)
            
            resp_lang = get_lang_name("ai_response_language")
            prompt_template = get_prompt_text("label_single_system")
            prompt = apply_prompt_template(prompt_template, [
                ("app_name", uniqueId),
                ("response_lang", resp_lang)
            ])
            
            res = AIHandler.call(prompt, attachments=[{'mime_type': m, 'data': img}], task="operator")
            self.current_status = _("Idle")
            
            if res and not res.startswith("ERROR:"):
                clean_name = clean_markdown(res)
                
                def save_ui_thread():
                    if uniqueId not in self.labels_cache: self.labels_cache[uniqueId] = {}
                    sig_key = _generate_object_signature(obj)
                    if sig_key:
                        self.labels_cache[uniqueId][sig_key] = clean_name
                        self._save_all_labels()
                        tones.beep(1000, 100)
                        # Translators: Success message spoken when the AI successfully assigns a new label to the object. {name} is replaced with the AI-generated label.
                        ui.message(_("Labeled as: {name}").format(name=clean_name))
                        
                wx.CallAfter(save_ui_thread)
            elif res and res.startswith("ERROR:"):
                wx.CallAfter(show_error_dialog, res[6:])
        
        threading.Thread(target=worker, daemon=True).start()

    # Translators: Script description for managing existing labels or starting a full app scan.
    @scriptHandler.script(description=_("Manages existing labels or scans the entire app to label unnamed elements."))
    def script_manageOrScanApp(self, gesture):
        if self.toggling: self.finish()
        obj = api.getFocusObject()
        app_name = obj.appModule.appName.lower()
        if app_name in ["chrome", "msedge", "firefox", "opera", "brave"]:
            # Translators: Message shown when a user tries to use AI labeling in a web browser.
            ui.message(_("AI Labeling is currently not supported in web browsers."))
            return
        uniqueId = self._getAppId(obj)
        
        if uniqueId in self.labels_cache and self.labels_cache[uniqueId]:
            def show_manager():
                gui.mainFrame.prePopup()
                dlg = LabelManagerDialog(gui.mainFrame, uniqueId, self.labels_cache[uniqueId])
                if dlg.ShowModal() == wx.ID_OK:
                    if dlg.action_type == "delete":
                        for k in dlg.target_keys: del self.labels_cache[uniqueId][k]
                    elif dlg.action_type == "rename":
                        self.labels_cache[uniqueId][dlg.target_keys[0]] = dlg.new_name
                    elif dlg.action_type == "rescan":
                        wx.CallLater(600, self._batchLabelApp, uniqueId)
                    
                    if dlg.action_type in ["delete", "rename"]:
                        self._save_all_labels()
                        # Translators: Confirmation message shown after labels are deleted or renamed.
                        ui.message(_("Labels updated."))
                dlg.Destroy()
                gui.mainFrame.postPopup()
            wx.CallAfter(show_manager)
        else:
            self._batchLabelApp(uniqueId)

    def _save_all_labels(self):
        try:
            with open(LABELS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.labels_cache, f, ensure_ascii=False, indent=4)
        except Exception: pass

    def _batchLabelApp(self, unique_id):
        if check_screen_curtain_active():
            return
        tones.beep(800, 100)
        # Translators: Progress message spoken when the add-on begins scanning the current application window to find UI elements (like buttons or icons) that do not have accessibility names.
        self.current_status = _("Scanning application UI...")
        ui.message(self.current_status)
        
        def worker():
            root = api.getForegroundObject()
            candidates = []
            stack = [(root, 0)]
            target_roles = {
                controlTypes.Role.BUTTON, controlTypes.Role.TOGGLEBUTTON, 
                controlTypes.Role.CHECKBOX, controlTypes.Role.RADIOBUTTON, 
                controlTypes.Role.MENUITEM, controlTypes.Role.LINK, 
                controlTypes.Role.TAB, controlTypes.Role.DATAITEM, 
                controlTypes.Role.LISTITEM, controlTypes.Role.COMBOBOX, 
                controlTypes.Role.GRAPHIC, controlTypes.Role.ICON, 
                controlTypes.Role.TABLECELL
            }
            
            while stack and len(candidates) < 1500:
                obj, depth = stack.pop()
                if depth > 25: continue 
                try:
                    role = obj.role
                    loc = obj.location
                    name = obj.name
                    if loc and role in target_roles and (not name or not name.strip()):
                        candidates.append(obj)
                    
                    child = obj.firstChild
                    while child:
                        stack.append((child, depth + 1))
                        child = child.next
                except Exception: continue

            if not candidates:
                self.current_status = _("Idle")
                # Translators: Message spoken when the add-on finishes the UI scan but finds no unnamed elements to label (everything already has a name).
                wx.CallAfter(ui.message, _("No unnamed elements found."))
                return

            # Translators: Progress message spoken when the add-on has found unnamed elements and is now sending the full application screenshot to AI for batch labeling.
            self.current_status = _("Analyzing application...")
            wx.CallAfter(ui.message, self.current_status)
            
            img, w, h, m = self._capture_fullscreen()
            prompt_template = get_prompt_text("label_batch_system")
            prompt = apply_prompt_template(prompt_template, [
                ("app_name", unique_id),
                ("response_lang", get_lang_name("ai_response_language"))
            ])
            
            res = AIHandler.call(prompt, attachments=[{'mime_type': m, 'data': img}], json_mode=True, task="operator")
            self.current_status = _("Idle")
            
            if res and not res.startswith("ERROR:"):
                try:
                    raw_res = res.strip()
                    start_idx = raw_res.find('[')
                    end_idx = raw_res.rfind(']')
                    
                    if start_idx != -1 and end_idx != -1:
                        clean_json = raw_res[start_idx:end_idx+1]
                    else:
                        clean_json = raw_res

                    ai_items = json.loads(clean_json)
                    
                    def save_batch_ui_thread():
                        if unique_id not in self.labels_cache: self.labels_cache[unique_id] = {}
                        
                        for item in ai_items:
                            if not all(k in item for k in ('x', 'y', 'label')): continue
                            
                            try:
                                x_val = float(item['x'])
                                y_val = float(item['y'])
                            except (ValueError, TypeError, KeyError):
                                continue
                            
                            ai_x, ai_y = int(x_val * w / 1000), int(y_val * h / 1000)
                            best_match, min_dist = None, 100
                            
                            for cand in candidates:
                                c_loc = cand.location
                                if not c_loc: continue
                                cx, cy = c_loc.left + c_loc.width/2, c_loc.top + c_loc.height/2
                                dist = ((cx - ai_x)**2 + (cy - ai_y)**2)**0.5
                                if dist < min_dist:
                                    min_dist = dist
                                    best_match = cand
                            
                            if best_match:
                                sig_key = _generate_object_signature(best_match)
                                if sig_key:
                                    self.labels_cache[unique_id][sig_key] = item['label']
                        
                        self._save_all_labels()
                        tones.beep(1000, 100)
                        # Translators: Success message spoken when the AI finishes analyzing the app and successfully names multiple elements in the background.
                        ui.message(_("Application labeling complete."))
                        
                    wx.CallAfter(save_batch_ui_thread)
                except Exception as e:
                    log.error(f"Batch labeling mapping failed: {e}")
                    # Translators: Error message spoken when the add-on fails to parse or map the labels returned by the AI (e.g., due to invalid AI response format).
                    wx.CallAfter(ui.message, _("Batch labeling failed."))
            elif res and res.startswith("ERROR:"):
                wx.CallAfter(show_error_dialog, res[6:])
        
        wx.CallLater(400, lambda: threading.Thread(target=worker, daemon=True).start())

    __gestures = {
        "kb:NVDA+shift+v": "activateLayer",
    }
    
    __VisionGestures = {
        "kb:t": "translateSmart",
        "kb:r": "refineText",
        "kb:o": "ocrFullScreen",
        "kb:v": "describeObject",
        "kb:d": "analyzeDocument",
"kb:f": "smartFileAction",
        "kb:a": "transcribeAudio",
        "kb:c": "solveCaptcha",
        "kb:i": "announceStatus",
        "kb:s": "smartDictation",
        "kb:u": "checkUpdate",
        "kb:shift+t": "translateClipboard",
        "kb:shift+v": "analyzeOnlineVideo",
        "kb:control+v": "recordLocalVideo",
        "kb:space": "showLastResult",
        "kb:h": "showHelp",
        "kb:e": "toggleUIExplorer",
        "kb:shift+a": "aiOperatorAction",
        "kb:l": "labelObject",
        "kb:shift+l": "manageOrScanApp",
        "kb:control+l": "toggleLiveAssistant",
        "kb:alt+s": "openSettings",
        "kb:alt+q": "reportQuotaExhaustedKeys",
        "kb:alt+m": "reportSelectedModels",
    }
