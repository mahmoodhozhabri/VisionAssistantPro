# -*- coding: UTF-8 -*-
from site_scons.site_tools.NVDATool.typings import AddonInfo, BrailleTables, SymbolDictionaries
from site_scons.site_tools.NVDATool.utils import _

addon_info = AddonInfo(
    addon_name="VisionAssistant",
    # Add-on summary/title, usually the user visible name of the add-on
    # Translators: Summary/title for this add-on
    # to be shown on installation and add-on information found in add-on store
    addon_summary=_("Vision Assistant Pro"),
# Add-on description
    # Translators: Long description to be shown for this add-on on add-on information from add-on store
    addon_description=_("""An advanced AI assistant for NVDA using Gemini models.
Command Layer: Press NVDA+Shift+V, then:
- Smart Translator (T) / Clipboard (Shift+T)
- Text Refiner (R)
- Describe Object (V) / Full Screen (O)
- Video Analysis (Shift+V)
- Local Video Recording (Control+V)
- Document Reader (D)
- File OCR (F)
- CAPTCHA Solver (C)
- Audio Transcription (A)
- Smart Dictation (S)
- Announce Status (I)
- Label Object (L)
- Manage/Scan Labels (Shift+L)
- UI Explorer (E)
- AI Operator (Shift+A)
- Check Update (U)
- Recall Last Result (Space)
- Commands Help (H)
- Open Settings (Alt+S)
- Report Quota Exhausted Keys (Alt+Q)
- Report Advanced Routing (Alt+M)"""),
    addon_version="2026.07.16",
    # Brief changelog for this version
    # Translators: what's new content for the add-on version to be shown in the add-on store
    addon_changelog=_("""## Changes for 2026.07.15

*   **Intelligent API Model Filtering**: Complete overhaul of the model filtering system to use a pure blacklist approach instead of whitelists. Added stronger filtering keywords (`embedding`, `bison`, `gecko`, `audio`, `realtime`, `babbage`, `moderation`, `deep`, `antigravity`, `computer`) to ensure the main chat model dropdown remains perfectly clean and future-proof, while keeping all specialized models accessible in the Advanced Routing section.
*   **Advanced Routing Search**: All Advanced Model Routing dropdowns (OCR, STT, TTS, Operator, Video, Live) and the eSpeak Variant selector are now fully searchable. You can quickly type to filter and find your desired model or variant.
*   **New Command Layer Shortcuts**:
    *   **Settings (`Alt + S`)**: Instantly opens the Vision Assistant Pro settings dialog.
    *   **Quota Exhausted Keys Report (`Alt + Q`)**: Reports the exact number of Gemini API keys that have exceeded their daily quota, identifying which specific model they are exhausted on, and announces their exact reset time.
    *   **Routing Audit (`Alt + M`)**: Audits and announces your current Advanced Routing configuration, reading out which models are actively selected for specialized tasks (skipping default settings).
*   **Video Analyzer Complete Overhaul**: The Video Analyzer has been completely transformed! Previously, it only provided a basic description of online videos. Now, it is a comprehensive video processing suite tailored for blind users:
    *   **Local Screen Recording (`Control+V`)**: You can now record silent videos directly from your screen. The AI will analyze the recorded segment and provide a highly detailed description of the scene, layout, and actions.
    *   **Audio Description Generation (SRT)**: The add-on can now generate highly detailed Audio Description scripts (in standard SRT format) for videos, complete with smart gap-timing to intelligently anchor descriptions to natural pauses in the audio track, and verbatim OCR for any on-screen text.
    *   **Synchronized Audio Narration (MP3 Export)**: Beyond text-based subtitles, the add-on can synthesize the Audio Description into speech, automatically mix it with the video's original audio track, apply audio ducking (lowering background volume during descriptions), and export the final synchronized result as an MP3 file!
    *   **Smart Video File Action**: If you focus on a local video file and press the video shortcut, the add-on will automatically detect it and process the file directly.
    *   **Advanced Character Tracking**: The AI now performs a character extraction pre-pass. It builds a global character dictionary and tracks characters accurately segment-by-segment without confusing identities.
    *   **Video Analysis Configuration**: Added new settings to control SRT chunk sizes, character subtitling, and disclaimers.
    *   **Extended Model Routing**: You can now explicitly select specialized video models (`gemini_video_model`, `custom_video_model`) in the Advanced Model Routing settings.
*   **Smart API Quota Management**: Enhanced handling of 429 (Daily Limit) errors by tracking quotas per-model. If a key hits its daily limit on one model, it is intelligently quarantined for that specific model only, leaving the key available for use with other models."""),
    addon_author="Mahmood Hozhabri",
    addon_url="https://github.com/mahmoodhozhabri/VisionAssistantPro",
    addon_sourceURL="https://github.com/mahmoodhozhabri/VisionAssistantPro",
    addon_docFileName="readme.html",
    addon_minimumNVDAVersion="2025.1",
    addon_lastTestedNVDAVersion="2026.1",
    addon_updateChannel=None,
    addon_license="GPL-2.0",
    addon_licenseURL="https://www.gnu.org/licenses/gpl-2.0.html",
)

pythonSources: list[str] = ["addon/globalPlugins/visionAssistant/*.py"]
i18nSources = pythonSources + ["buildVars.py"]
excludedFiles: list[str] = []

baseLanguage: str = "en"

markdownExtensions: list[str] = [
    "markdown.extensions.tables",
    "markdown.extensions.toc",
    "markdown.extensions.nl2br",
    "markdown.extensions.extra",
]

brailleTables: BrailleTables = {}
symbolDictionaries: SymbolDictionaries = {}