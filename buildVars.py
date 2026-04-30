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
- Online Video Analysis (Shift+V)
- Document Reader (D)
- File OCR (F)
- CAPTCHA Solver (C)
- Audio Transcription (A)
- Smart Dictation (S)
- Announce Status (L)
- Check Update (U)
- Recall Last Result (Space),
- Commands Help (H),
"""),
    addon_version="5.0.2",
    # Brief changelog for this version
    # Translators: what's new content for the add-on version to be shown in the add-on store
    addon_changelog=_("""## Changes for 5.0
* **Multi-Provider Architecture**: Added full support for **OpenAI**, **Groq**, and **Mistral** alongside Google Gemini. Users can now choose their preferred AI backend.
* **Advanced Model Routing**: Users of native providers (Gemini, OpenAI, etc.) can now select specific models from a dropdown list for different tasks (OCR, STT, TTS).
* **Advanced Endpoint Configuration**: Custom provider users can manually input specific URLs and model names for granular control over local or third-party servers.
* **Smart Feature Visibility**: The settings menu and Document Reader UI now automatically hide unsupported features (like TTS) based on the selected provider.
* **Dynamic Model Fetching**: The addon now fetches the available model list directly from the provider's API, ensuring compatibility with new models as soon as they are released.
* **Hybrid OCR & Translation**: Optimized the logic to use Google Translate for speed when using Chrome OCR, and AI-powered translation when using Gemini/Groq/OpenAI engines.
* **Universal "Re-scan with AI"**: The Document Reader's re-scan feature is no longer limited to Gemini. It now utilizes whatever AI provider is currently active to re-process pages."""),
    addon_author="Mahmood Hozhabri",
    addon_url="https://github.com/mahmoodhozhabri/VisionAssistantPro",
    addon_sourceURL="https://github.com/mahmoodhozhabri/VisionAssistantPro",
    addon_docFileName="readme.html",
    addon_minimumNVDAVersion="2025.1",
    addon_lastTestedNVDAVersion="2025.3.3",
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