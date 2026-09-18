# -*- coding: utf-8 -*-
import os
import json
import re
import logging

import addonHandler
import languageHandler
import config as nvda_config

log = logging.getLogger(__name__)

ADDON_NAME = addonHandler.getCodeAddon().manifest["summary"]
GITHUB_REPO = "mahmoodhozhabri/VisionAssistantPro"

# --- Constants & Config ---

# Default API Endpoints
DEFAULT_API_URLS = {
    "mistral": "https://api.mistral.ai",
    "openai": "https://api.openai.com",
    "groq": "https://api.groq.com/openai",
    "gemini": "https://generativelanguage.googleapis.com",
    "minimax": "https://api.minimax.io/v1"
}

CHROME_OCR_KEYS = [
    "AIzaSyA2KlwBX3mkFo30om9LUFYQhpqLoa_BNhE",
    "AIzaSyBOti4mM-6x9WDnZIjIeyEU21OpBXqWBgw"
]

addonHandler.initTranslation()

LAYER_BUSY_GESTURES = frozenset({
    "t", "r", "o", "v", "d", "f", "m", "c", "i", "s", "u", "h", "e", "l",
    "shift+c", "shift+t", "shift+v", "shift+a", "shift+l",
    "control+v", "control+l", "control+t", "control+h",
    "alt+s", "alt+q", "alt+m",
    "nvda+shift+v",
})

MODELS = [
    # --- 1. Recommended (Auto-Updating) ---
    # Translators: AI Model info. [Auto] = Automatic updates. (Latest) = Newest version.
    (_("[Auto]") + " Gemini Flash " + _("(Latest)"), "gemini-flash-latest"),
    (_("[Auto]") + " Gemini Flash Lite " + _("(Latest)"), "gemini-flash-lite-latest"),

    # --- 2. Current Standard (Free & Fast) ---
    # Translators: AI Model info. [Free] = Generous usage limits. (Preview) = Experimental or early-access version.
    (_("[Free]") + " Gemini 3.6 Flash", "gemini-3.6-flash"),
    (_("[Free]") + " Gemini 3.5 Flash", "gemini-3.5-flash"),
    (_("[Free]") + " Gemini 3.5 Flash Lite", "gemini-3.5-flash-lite"),
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
    ("Orus", _("Firm")), 
    # Translators: Adjective describing a breezy AI voice style.
    ("Aoede", _("Breezy")), 
    # Translators: Adjective describing an easy-going AI voice style.
    ("Callirrhoe", _("Easy-going")), 
    ("Autonoe", _("Bright")), 
    # Translators: Adjective describing a breathy AI voice style.
    ("Enceladus", _("Breathy")), 
    # Translators: Adjective describing a clear AI voice style.
    ("Iapetus", _("Clear")), 
    ("Umbriel", _("Easy-going")), 
    # Translators: Adjective describing a smooth AI voice style.
    ("Algieba", _("Smooth")), 
    ("Despina", _("Smooth")), 
    ("Erinome", _("Clear")), 
    # Translators: Adjective describing a gravelly AI voice style.
    ("Algenib", _("Gravelly")), 
    ("Rasalgethi", _("Informative")), 
    ("Laomedeia", _("Upbeat")), 
    # Translators: Adjective describing a soft AI voice style.
    ("Achernar", _("Soft")), 
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
    ("Sage", _("Gentle")),
    ("Shimmer", _("Clear")),
    # Translators: Adjective describing an expressive AI voice style.
    ("Verse", _("Expressive")),
    # Translators: Adjective describing a reliable AI voice style.
    ("Marin", _("Reliable")),
    # Translators: Adjective describing an energetic AI voice style.
    ("Cedar", _("Energetic"))
]

try:
    import globalVars
    DATA_DIR = os.path.join(globalVars.appArgs.configPath, "VisionAssistant")
    LABELS_FILE = os.path.join(DATA_DIR, "labels.json")
    OCR_PROGRESS_FILE = os.path.join(DATA_DIR, "ocr_progress.json")
    HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
    GEMINI_FILE_CACHE_FILE = os.path.join(DATA_DIR, "gemini_file_cache.json")
    OCR_TEXT_CACHE_FILE = os.path.join(DATA_DIR, "ocr_text_cache.json")
except Exception:
    LABELS_FILE = f"{ADDON_NAME}_labels.json"
    OCR_PROGRESS_FILE = f"{ADDON_NAME}_ocr_progress.json"
    HISTORY_FILE = f"{ADDON_NAME}_history.json"
    GEMINI_FILE_CACHE_FILE = f"{ADDON_NAME}_gemini_file_cache.json"
    OCR_TEXT_CACHE_FILE = f"{ADDON_NAME}_ocr_text_cache.json"

_MIGRATION_DONE = False

def _migrate_data_dir():
    global _MIGRATION_DONE
    if _MIGRATION_DONE:
        return
    _MIGRATION_DONE = True
    try:
        import shutil
        import globalVars
        config_path = globalVars.appArgs.configPath
        old_prefix = ADDON_NAME + "_"
        target = os.path.join(config_path, "VisionAssistant")
        file_map = {
            f"{ADDON_NAME}_labels.json": "labels.json",
            f"{ADDON_NAME}_history.json": "history.json",
            f"{ADDON_NAME}_ocr_progress.json": "ocr_progress.json",
            f"{ADDON_NAME}_gemini_file_cache.json": "gemini_file_cache.json",
            f"{ADDON_NAME}_ocr_text_cache.json": "ocr_text_cache.json",
        }
        if not os.path.isdir(target):
            os.makedirs(target, exist_ok=True)
        for old_name, new_name in file_map.items():
            src = os.path.join(config_path, old_name)
            dst = os.path.join(target, new_name)
            if os.path.isfile(src) and not os.path.isfile(dst):
                try:
                    shutil.move(src, dst)
                except Exception:
                    pass
        old_log_dir = os.path.join(config_path, "VisionAssistant_logs")
        new_log_dir = os.path.join(target, "logs")
        if os.path.isdir(old_log_dir) and not os.path.isdir(new_log_dir):
            try:
                shutil.move(old_log_dir, new_log_dir)
            except Exception:
                pass
    except Exception:
        pass

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
    code = nvda_config.conf["VisionAssistant"][conf_key]
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
    "document_export_page_numbers": "boolean(default=True)",
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
    "live_push_to_talk": "boolean(default=False)",
    "live_ptt_key": "string(default='')",
    "enable_visual_captcha_solver": "boolean(default=True)",
    "describe_images_ocr": "boolean(default=True)",
    "live_model": "string(default='gemini-3.1-flash-live-preview')",
    "live_thinking_level": "string(default='medium')",
    "ocr_engine": "string(default='chrome')",
    "ocr_batch_size": "integer(default=20, min=0, max=100)",
    "video_srt_chunk_minutes": "integer(default=10, min=0, max=60)",
    "video_chars_as_subtitle": "boolean(default=True)",
    "video_add_disclaimer": "boolean(default=True)",
    "enable_file_logging": "boolean(default=False)",
    "protect_api_keys_in_backups": "boolean(default=True)",
    "log_level": "string(default='DEBUG')",
    "log_retention_hours": "integer(default=168, min=1, max=2160)",
    "tts_voice": "string(default='Puck')",
    "tts_engine": "string(default='standard')"
}

nvda_config.conf.spec["VisionAssistant"] = confspec

LOG_RETENTION_OPTIONS = [
    # Translators: Log retention option: 1 hour
    (_("1 Hour"), 1),
    # Translators: Log retention option: 3 hours
    (_("3 Hours"), 3),
    # Translators: Log retention option: 6 hours
    (_("6 Hours"), 6),
    # Translators: Log retention option: 12 hours
    (_("12 Hours"), 12),
    # Translators: Log retention option: 24 hours (1 day)
    (_("24 Hours (1 Day)"), 24),
    # Translators: Log retention option: 3 days
    (_("3 Days"), 72),
    # Translators: Log retention option: 7 days
    (_("7 Days"), 168),
    # Translators: Log retention option: 14 days
    (_("14 Days"), 336),
    # Translators: Log retention option: 30 days
    (_("30 Days"), 720),
    # Translators: Log retention option: 90 days
    (_("90 Days"), 2160),
]

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
        # Translators: Title of the Refine dialog
        "section": _("Refine"),
        # Translators: Label for the grammar correction prompt.
        "label": _("Fix Grammar"),
        "prompt": "Fix grammar in the text below. Output ONLY the fixed text.",
    },
    {
        "key": "fix_translate",
        "section": _("Refine"),
        # Translators: Label for the grammar correction and translation prompt.
        "label": _("Fix Grammar & Translate"),
        "prompt": "Fix grammar and translate to {target_lang}.{swap_instruction} Output ONLY the result.",
    },
    {
        "key": "explain",
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
        "guardedFeatureLabel": _("Smart Translation"),
        "requiredMarkers": ["{target_lang}", "{swap_target}", "{smart_swap}", "{text_content}"],
        "prompt": "Task: Translate the text below based on its DOMINANT language.\n\nConfiguration:\n- Target Language: \"{target_lang}\"\n- Swap Language: \"{swap_target}\"\n- Smart Swap: {smart_swap}\n\nCRITICAL RULES:\n1. DOMINANT LANGUAGE: First, determine the primary/dominant language of the input by focusing on the grammatical structure and the majority of the vocabulary. Ignore embedded technical jargon, user interface labels, software commands, or standalone foreign loanwords when deciding this dominant language.\n2. SMART SWAP: If the dominant language is ALREADY \"{target_lang}\" AND Smart Swap is True, translate the ENTIRE text into \"{swap_target}\".\n3. DEFAULT: In ALL OTHER CASES (or if Smart Swap is False), translate the ENTIRE text into \"{target_lang}\".\n\nConstraints:\n- Output ONLY the final translation.\n- Do NOT translate actual programming code (Python, C++, etc.) or URLs.\n- Do not add any introductory text or explanations.\n\nInput Text:\n{text_content}",
    },
    {
        "key": "translate_quick",
        # Translators: Label for end page
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
        "key": "direct_chat_system",
        # Translators: Section header for direct chat prompts in Prompt Manager.
        "section": _("Chat"),
        # Translators: Label for the Direct Chat system instruction prompt in the Prompt Manager.
        "label": _("Direct Chat Instruction"),
        "prompt": (
            "You are Vision Assistant Pro, a helpful, knowledgeable AI assistant for a blind user "
            "who relies on the NVDA screen reader. Answer questions clearly and accurately. "
            "Use Markdown formatting for readability. ALWAYS respond STRICTLY in {response_lang}."
        ),
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
            "2. ALL APPEARANCE RANGES (CRITICAL): You MUST include 'appearance_ranges', an array of time windows [start_sec, end_sec] in seconds indicating ALL scenes/sections where this character physically appears on screen or speaks (e.g. [[120, 300], [1200, 1500]] for minutes 2-5 and 20-25).\n"
            "3. THIRD-PARTY MENTIONS (CRITICAL): People often talk about others who are not present. If a name is spoken in the dialogue, DO NOT automatically assign it to one of the speakers or someone on screen. A name should ONLY be assigned if a character introduces themselves or is explicitly addressed by another while visible.\n"
            "4. DO NOT USE FACIAL RECOGNITION FOR NAMES: Under no circumstances should you guess a character's name based on the actor's real-world face. Only use names heard clearly in the audio.\n"
            "5. CHARACTER RELATIONSHIPS: Listen to verbal context to establish clear relationships. Include these verified relationships in their description field.\n"
            "6. FACIAL FEATURES ARE PRIMARY: Clothing can change, so you MUST prioritize describing immutable facial features and physical traits.\n"
            "7. DO NOT TRANSLATE JSON KEYS. The keys 'characters', 'name', 'appearance_ranges', and 'description' MUST remain in English. Only translate the values into {response_lang}.\n"
            "8. Output format MUST be valid JSON matching this template:\n"
            "{\n"
            "  \"characters\": [\n"
            "    {\n"
            "      \"name\": \"Character Name (or descriptive placeholder if name is unverified)\",\n"
            "      \"appearance_ranges\": [\n"
            "        [120, 300],\n"
            "        [1200, 1500]\n"
            "      ],\n"
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
        "section": "Advanced",
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
        # Translators: Labels for the AI and User in chat history
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
        "key": "audio_translation",
        # Translators: Label for audio translation prompt in Prompt Manager.
        "section": _("Audio"),
        "label": _("Audio Translation"),
        "guarded": True,
        "guardedFeatureLabel": _("Audio Translation"),
        "requiredMarkers": ["{target_lang}"],
        "prompt": "Transcribe and translate the spoken audio from this file to {target_lang}. Output ONLY the final translation.",
    },
    {
        "key": "dictation_transcribe",
        "section": _("Audio"),
        # Translators: Label for the smart voice dictation prompt.
        "label": _("Smart Dictation"),
        "guarded": True,
        "guardedFeatureLabel": _("Smart Dictation"),
        "requiredMarkers": ["[[[NOSPEECH]]]"],
        "prompt": (
            "Transcribe speech. Use native script. Fix stutters. If there is no speech, silence, "
            "or background noise only, write exactly: [[[NOSPEECH]]]"
        ),
    },
    {
        "key": "dictation_translate",
        "section": _("Audio"),
        # Translators: Prompt Manager label for voice translation feature
        "label": _("Voice Translation"),
        "guarded": True,
        "guardedFeatureLabel": _("Voice Translation"),
        "requiredMarkers": ["{source_lang}", "{target_lang}", "{swap_target}", "{smart_swap}", "[[[NOSPEECH]]]"],
        "prompt": (
            "Transcribe and translate the spoken audio from {source_lang} to {target_lang}. "
            "If {source_lang} is Auto-detect, identify the language first. "
            "SMART SWAP RULE: If the spoken language is ALREADY {target_lang} AND Smart Swap is {smart_swap}, translate the audio into {swap_target} instead. "
            "Output ONLY the final translation. Do not add any extra comments or notes. "
            "If there is no speech, silence, or background noise only, write exactly: [[[NOSPEECH]]]"
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
        # Translators: Prefix for main model status
        "section": _("OCR"),
        # Translators: Label for the OCR prompt used for document text extraction.
        "label": _("OCR Document Extraction"),
        "guarded": True,
        "guardedFeatureLabel": _("OCR Document Extraction"),
        "requiredMarkers": ["[[[PAGE_SEP]]]"],
        "prompt": (
            "Extract all visible text from this document. Strictly preserve original formatting "
            "(headings, lists, tables) using Markdown. If there are any website URLs, "
            "convert them into active Markdown hyperlinks. {image_desc_instruction} IMPORTANT: "
            "Start directly with the content. Do not add introductory sentences like "
            "'Here is the analysis' or 'The image shows'. You MUST insert the exact delimiter "
            "'[[[PAGE_SEP]]]' immediately after the content of every single page. Do not output "
            "any system messages or code block backticks (```). Output ONLY the raw content."
        ),
    },
    {
        "key": "ocr_document_translate",
        "section": _("Document"),
        # Translators: Label for the combined OCR and translation prompt for documents.
        "label": _("Document OCR + Translate"),
        "guarded": True,
        "guardedFeatureLabel": _("Document OCR + Translate"),
        "requiredMarkers": ["[[[PAGE_SEP]]]"],
        "prompt": (
            "Extract all visible text from this document. Strictly preserve original formatting "
            "(headings, lists, tables) using Markdown. {image_desc_instruction} Then translate "
            "all the extracted content to {target_lang}. IMPORTANT: "
            "Start directly with the translated content. Do not add introductory sentences. "
            "You MUST insert the exact delimiter '[[[PAGE_SEP]]]' immediately after the translated "
            "content of every single page. Do not output any system messages or code block "
            "backticks (```). Output ONLY the raw translated content."
        ),
    },
    {
        "key": "ocr_image_desc_instruction",
        "section": _("OCR"),
        # Translators: Title for the sub-prompt that instructs the AI to describe images inline.
        "label": _("Image Description Instruction (Sub-prompt)"),
        "prompt": (
            "Embed the images in their original positions as presented in the document. "
            "For any photos, figures, diagrams, or illustrations, provide a comprehensive and detailed description of them "
            "inline at their original positions in {response_lang}. Do not describe them too simply; capture the visual essence thoroughly. "
            "CRITICAL: DO NOT transcribe the main body text of the document inside the image description. The image description is ONLY for visual elements, not for the page's reading text. "
            "If an illustration or chart contains specific labels, you may transcribe those labels, but never duplicate the main text. "
            "ALWAYS start each image description with a consistent phrase equivalent to 'Image description:' translated into {response_lang}. "
            "Do NOT output image file names."
        ),
    },
    {
        "key": "captcha_solver_base",
        # Translators: Checkbox label to add an AI warning disclaimer at the beginning of the video SRT output.
        "section": _("CAPTCHA"),
        "label": _("CAPTCHA Solver"),
        "guarded": True,
        "guardedFeatureLabel": _("CAPTCHA Solver"),
        "requiredMarkers": ["[[[NO_CAPTCHA]]]", "[[[VISUAL_CAPTCHA]]]"],
        "prompt": (
            "Blind user. Look at the image carefully. "
            "1. If you see an unchecked 'I'm not a robot' checkbox or a visual puzzle (like reCAPTCHA/hCaptcha), strictly return: [[[VISUAL_CAPTCHA]]]. "
            "2. If it is a text or math CAPTCHA, return the solved code only. "
            "3. If absolutely NO CAPTCHA is visible in the image, strictly return: [[[NO_CAPTCHA]]].{captcha_extra}"
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
        "key": "captcha_solver_loop",
        # Translators: Section header for advanced prompts in Prompt Manager.
        "section": _("Advanced"),
        # Translators: Label for the advanced visual CAPTCHA solver prompt.
        "label": _("Visual CAPTCHA Solver"),
        "internal": True,
        "prompt": (
            "You are a UI analysis assistant helping a blind user navigate complex interfaces. Look at the full-screen image. "
            "Coordinates MUST be exact in 0-1000 format. Return coordinates natively as [y, x] where y is the vertical axis (0=top, 1000=bottom) and x is the horizontal axis (0=left, 1000=right). "
            "1. If there is a confirmation checkbox on the screen, return JSON with action='click' and coordinates=[y,x] pointing to its exact CENTER. "
            "2. If there is an image grid challenge with selectable tiles and a main action button at the bottom, YOU MUST USE action='puzzle'. "
            "CRITICAL FOR 'is_fading': Set 'is_fading'=true ONLY IF the instruction explicitly contains the words 'once there are none left' (meaning clicked tiles fade away individually). For ALL OTHER grid challenges, YOU MUST set 'is_fading'=false. "
            "For 'tile_clicks', return the exact CENTER coordinate of each tile matching the requested object. IF NO TILES MATCH, leave it empty: []. "
            "CRITICAL FOR SLICED IMAGES: If the image is a single large picture cut into a grid, examine EVERY single square with extreme microscopic precision. Even if a square contains only a tiny fraction of the target object, YOU MUST INCLUDE IT in 'tile_clicks'. "
            "For 'action_button', YOU MUST ALWAYS return the exact CENTER coordinate of the bottom-right action button (e.g. Verify, Next, Skip). "
            "3. If it is a slider or drag-and-drop interface, use action='drag', drag_start=[y,x], drag_end=[y,x]. Include action_button=[y,x] if a confirmation button exists. "
            "4. If the challenge is successfully completed (e.g., green checkmark) OR the puzzle popup has completely disappeared from the screen, return JSON with action='solved'. "
            "5. If the interface is clearly still loading, return JSON with action='none'. "
            "Output ONLY valid JSON. Include only the keys relevant to your action. Example format: {\"action\": \"...\", \"is_fading\": true/false, \"tile_clicks\": [[y,x]], \"drag_start\": [y,x], \"drag_end\": [y,x], \"action_button\": [y,x], \"coordinates\": [y,x]}"
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
    ("[clipboard]", _("Clipboard content"), _("Text")),
    # Translators: Description for the [clipboard_image] variable in the Variables Guide.
    ("[clipboard_image]", _("Image currently in clipboard"), _("Image")),
    ("[screen_obj]", _("Screenshot of the navigator object"), _("Image")),
    ("[screen_full]", _("Screenshot of the entire screen"), _("Image")),
    ("[screen_fg_obj]", _("Screenshot of the active foreground window"), _("Image")),
    # Translators: Description and input type for the [file_ocr] variable in the Variables Guide.
    ("[file_ocr]", _("Select image/PDF/TIFF for text extraction"), _("Image, PDF, TIFF")),
    # Translators: Description and input type for the [file_read] variable in the Variables Guide.
    ("[file_read]", _("Select document for reading"), _("TXT, Code, PDF")),
    # Translators: Description and input type for the [file_audio] variable in the Variables Guide.
    ("[file_audio]", _("Select audio file for analysis"), _("MP3, WAV, OGG")),
    ("{target_lang}", _("Current target language"), _("Text")),
    ("{source_lang}", _("Current source language"), _("Text")),
    ("{response_lang}", _("Current AI response language"), _("Text")),
    ("{swap_target}", _("Fallback language for translation"), _("Text")),
    # Translators: Description for the {swap_instruction} variable in the Variables Guide.
    ("{swap_instruction}", _("Smart swap translation instruction"), _("Text")),
)

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

_HOTKEY_MODIFIER_ALIASES = {"ctrl": "control", "win": "windows", "insert": "nvda"}
_HOTKEY_ALLOWED_MODIFIERS = frozenset({"alt", "shift", "control", "nvda", "windows"})
_HOTKEY_MODIFIER_DISPLAY = {
    "control": "Ctrl",
    "shift": "Shift",
    "alt": "Alt",
    "nvda": "NVDA",
    "windows": "Win",
}


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
            normalized.append({
                "name": name,
                "content": content,
                "hotkey": _normalize_hotkey(item.get("hotkey")),
            })
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
