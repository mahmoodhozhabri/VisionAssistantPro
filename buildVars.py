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
    addon_version="5.5",
    # Brief changelog for this version
    # Translators: what's new content for the add-on version to be shown in the add-on store
    addon_changelog=_("""## Changes for 5.5 (The Automation Update)

*   **AI Operator (Autonomous Control - Shift+A):** This is the crown jewel of v5.5. Vision Assistant Pro has graduated from being a passive assistant to becoming your personal **AI Operator**. It doesn't just describe the screen—it takes command.
    *   *How it works:* You can now give verbal instructions to operate your PC. For example, in a completely inaccessible application where your screen reader stays silent, you can press **Shift+A** and type: *"Click on the Settings button"* or *"Find the search field, type 'Latest News' and press enter."* The AI visually identifies the elements, moves the mouse, and executes the task for you.
    *   *Performance Note:* This feature is optimized for **Gemini 3.0 Flash (Preview)**, delivering incredibly fast and intelligent responses that can handle even the most complex UI layouts.
    *   **⚠️ API Usage Warning:** Because the AI Operator needs to "see" exactly what's happening to be accurate, it sends a high-resolution screenshot with every step. Please note that frequent use will consume your API quota much faster than standard text-based tasks.
*   **Visual UI Explorer (E):** Tired of navigating through "unlabeled buttons"? Press **E** to activate the UI Explorer. The AI will scan the entire window and generate a list of every clickable element it sees—including icons, graphics, and menus. Simply pick an item from the list, and the AI Operator will click it for you. It’s like having an "accessible layer" on top of any app.
*   **Context-Aware Smart File Action (F):** The "F" key has been completely overhauled. It no longer assumes you only want OCR. When you select a single image, it now intelligently asks for your intent: you can choose a **Detailed Visual Description** to understand the scene or a **Structured Text Extraction (OCR)** for reading. The menu adapts dynamically based on the file type and your active AI engine.
*   **Core Optimization:** We've performed a deep cleanup of the add-on’s internal logic, removing unused legacy functions and redundant code. This results in a leaner, faster, and more reliable experience for all users."""),
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