# -*- coding: UTF-8 -*-
from site_scons.site_tools.NVDATool.typings import AddonInfo, BrailleTables, SymbolDictionaries
from site_scons.site_tools.NVDATool.utils import _

addon_info = AddonInfo(
    addon_name="VisionAssistant",
    addon_summary=_("Vision Assistant Pro"),
    addon_description=_("""An advanced AI assistant for NVDA using Gemini models.
Features:
- Smart Translator (NVDA+Ctrl+Shift+T/Y)
- Smart Dictation (NVDA+Ctrl+Shift+S)
- Text Refiner (NVDA+Ctrl+Shift+R)
- Vision & Screen Analysis (NVDA+Ctrl+Shift+V/O)
- Document QA (NVDA+Ctrl+Shift+D)
- CAPTCHA Solver (NVDA+Ctrl+Shift+C)
- Audio Transcription (NVDA+Ctrl+Shift+A)
- File Selection & OCR (NVDA+Ctrl+Shift+Insert+F)"""),
    addon_version="2.6.0",
    addon_changelog=_("""• Added Russian translation support. (Thanks to nvda-ru)
• Updated error messages to provide more descriptive feedback regarding connectivity.
• Added File Selection & OCR (NVDA+Ctrl+Shift+Insert+F)"""),
    addon_author="Mahmood Hozhabri",
    addon_url="https://github.com/mahmoodhozhabri/VisionAssistantPro",
    addon_sourceURL="https://github.com/mahmoodhozhabri/VisionAssistantPro",
    addon_docFileName="readme.html",
    addon_minimumNVDAVersion="2019.3",
    addon_lastTestedNVDAVersion="2025.3.1",
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