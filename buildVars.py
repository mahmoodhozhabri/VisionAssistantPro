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
- Direct Chat (Shift+C)
- Media Transcription & Dubbing (M)
- Smart Dictation (S)
        - Voice Translation (Control+T)
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
- Report Advanced Routing (Alt+M)
- Quick Settings (Up/Down/Left/Right)"""),
    addon_version="2026.09.02",
    # Brief changelog for this version
    # Translators: what's new content for the add-on version to be shown in the add-on store
    addon_changelog=_("""## Changes for 2026.09.02

*   **Google AI Studio API Keys**: Added support for the newer Gemini authorization API keys created in Google AI Studio. Compatible Gemini API keys created in Google Cloud Console will continue to be supported.
*   **Encrypted API Credentials**: API keys are now encrypted with Windows DPAPI before being stored in `nvda.ini`. Existing API keys stored in plaintext by earlier versions are automatically converted to DPAPI-encrypted values when the add-on starts, and plaintext fallback is refused if encryption fails. Plaintext keys are never retained in `nvda.ini`; both plaintext keys and DPAPI-protected values are removed from `nvda.log` and Vision Assistant's dedicated log file.
*   **Protected or Portable Settings Backups**: API keys remain encrypted in backups by default. Users can optionally create a transferable plaintext-key backup after accepting a security warning. Restored keys are immediately encrypted on the destination system. Disabling backup protection never permits plaintext keys in:
    *   `nvda.ini`
    *   `nvda.log`
    *   Vision Assistant's dedicated log file
"""),
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

pythonSources: list[str] = [
    "addon/globalPlugins/visionAssistant/*.py",
    "addon/globalPlugins/visionAssistant/ai/*.py",
    "addon/globalPlugins/visionAssistant/ai/providers/*.py",
    "addon/globalPlugins/visionAssistant/dialogs/*.py",
    "addon/globalPlugins/visionAssistant/features/*.py",
    "addon/globalPlugins/visionAssistant/utils/*.py",
]
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
