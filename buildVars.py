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
- Announce Status (I)
- Label Object (L)
- Manage/Scan Labels (Shift+L)
- UI Explorer (E)
- AI Operator (Shift+A)
- Check Update (U)
- Recall Last Result (Space)
- Commands Help (H)"""),
    addon_version="6.1.1",
    # Brief changelog for this version
    # Translators: what's new content for the add-on version to be shown in the add-on store
    addon_changelog=_("""## Changes for 6.1.1

*   **Gemma 4 Thinking Output Fix**: Fixed an issue with Gemma 4 models where the entire internal thought process was displayed as the final response, or where disabling thinking resulted in empty responses. The add-on now correctly isolates and extracts only the final clean text response.
*   **Batch OCR from File Explorer**: You can now select multiple photos or PDFs directly in Windows File Explorer and extract text or analyze them in batch. The add-on will automatically filter and process only the supported file formats."""),
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