# -*- coding: UTF-8 -*-
from site_scons.site_tools.NVDATool.typings import AddonInfo, BrailleTables, SymbolDictionaries, SpeechDictionaries
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
- Live Assistant (Control+L) / Live Operator (Control+A)
- Gemini API Key Manager (G)
- Check Update (U)
- Recall Last Result (Space)
- Commands Help (H)
- Open Settings (Alt+S)
- Report Quota Exhausted Keys (Alt+Q)
- Report Advanced Routing (Alt+M)
- Quick Settings (Up/Down/Left/Right)"""),
    addon_version="2026.10.15",
    # Brief changelog for this version
    # Translators: what's new content for the add-on version to be shown in the add-on store
    addon_changelog=_("""## Changes for 2026.10.15

*   **The Most Requested Fix — Creating a Gemini API Key Is Finally Easy**: Getting an API key on **aistudio.google.com** used to be the hardest step of all. With a screen reader the pages were confusing, and some people simply could not create a key at all. That problem is now solved directly inside the add-on. Press **G** in the Command Layer (or use **Get a Gemini API Key...** in Settings), sign in through your default browser with zero external setup, and your key is created and configured with one confirmation — even if you never had a project before.
*   **Ambient Observer**: The background assistant is here. Press **Shift+O** in the Command Layer to start it, and press it again to stop it. It can translate what it hears (your microphone or the sound of the system), watch the screen and tell you what changed, or open the Live Assistant with your webcam and Push to Talk so you can ask about whatever the camera sees. It sends a picture only when something really changed, so a still screen costs you nothing, and it stays quiet when nothing is happening. You can also launch and toggle the observer directly through Custom Prompts and dedicated shortcut keys using `[ambient_screen]`, `[ambient_webcam]`, or `[ambient_audio]` along with modifiers (`[loopback]`, `[mic]`, `[brief]`, `[detailed]`, `[lang:code]`), with automatic validation against conflicting variable combinations.
*   **Live Operator**: The Live Assistant can now carry out what you ask on your computer while you talk to it. Press **Control+A** in the Command Layer to start a live operator session, then just ask in plain language. It works through multi-step requests, says every step in the Live Assistant’s own voice, takes care of the key combinations it needs, and decides by itself when the task is finished. **Live Direct Output (No Window)** is in Quick Settings too.
*   **Character Dictionary & Series Management**: The Video Analysis dialog now includes a powerful **Character Dictionary** system! Add, edit, import, or manage character names, physical descriptions, and roles per series — the AI automatically matches discovered characters to your dictionary and merges new ones as you analyze more episodes. Your manual notes are always preserved with priority over AI updates, while physical descriptions stay up-to-date across episodes. The dictionary is saved per series and reused for every video in that series. In the character list, press **F2** to edit the selected character and **Delete** to remove it.
*   **SOCKS5, HTTP, and Reverse Proxy Support with Latency Testing**: Seamlessly bypass network restrictions with complete proxy support across the entire add-on — including the Live Assistant, Ambient Observer, and TTS generation! Choose from 4 operating modes in General settings: **Auto-detect**, **SOCKS5 Proxy**, **HTTP Proxy**, or **Reverse Proxy**. SOCKS5 supports RFC 1929 username/password authentication and domain tunneling; HTTP proxy supports Basic authentication. A new **Test Proxy Connection** button runs in the background and announces your connection latency in milliseconds.
*   **48-Hour Video File Caching**: Videos uploaded to Gemini are now cached for 48 hours! You can regenerate SRT or MP3 outputs for the same video without re-uploading — even after restarting NVDA. The cache is key-aware and automatically invalidated when your API key changes.
*   **AI-Powered Silence Detection (Silero VAD)**: Extended AD now uses the Silero VAD neural model for precise silence detection — distinguishing natural dialogue pauses from music and background noise. The model is downloaded automatically on first use (with your permission), just like ffmpeg and eSpeak.
*   **Webcam Video for Live Assistant**: The Live Assistant window now has a **Use &Webcam** checkbox to send your webcam feed to the AI instead of your screen — perfect for asking questions about physical objects, documents, or your surroundings. If ffmpeg isn't installed yet, ticking the box downloads it (one-time, with your permission). The option is disabled when no camera is detected or Windows privacy settings block camera access, with a button to open the camera privacy settings. If the camera is enabled but produces no frames, the problem is logged to the NVDA log for diagnosis instead of silently switching back to the screen.
*   **Audio Output Device Selection**: You can now select a dedicated audio output device for the Live Assistant and Ambient Observer. Choose between NVDA's default output, Windows Sound Mapper, or any connected physical sound card (like USB headphones or external speakers) in the Live Settings tab, directly inside the Live Assistant dialog, or on the fly via Quick Settings (NVDA+Shift+V then Up/Down/Left/Right).
*   **Prompt Manager**: The Default Prompts tab has a **Filter** list now, so you can show all prompts or just one section (for example **Ambient**). You can also edit the observer’s context texts and the new **Live Operator Instruction** there.
*   **Smart Model Filtering in Advanced Routing**: Advanced Model Routing dropdowns now dynamically categorize Gemini models by capability without clutter. The Live Assistant only displays genuine bidirectional live and native-audio models, TTS only displays dedicated speech synthesis models, STT prioritizes Transcribe and multimodal models, and Video Analysis, OCR, and AI Operator cleanly filter out single-purpose utility models (such as image generation, video generation, and embedding models). Future models are detected automatically based on capability without requiring version updates.
*   **Character First-Appearance Tracking**: The AI now describes each character's physical appearance only once — at their first appearance in the video. Subsequent appearances use names only, eliminating repetitive descriptions across segments while keeping the narrative fresh and natural.
*   **Unified Data Directory**: All add-on data files (history, series, labels, OCR progress, caches, and logs) have been migrated into a single `VisionAssistant` folder inside your NVDA configuration directory — keeping everything organized and making manual backups effortless.
*   **Improved Video Save Experience**: When saving SRT or MP3 files, the file dialog now opens in the source video's folder by default, whether you open the video via the file dialog or Shift+V from Explorer.
*   **Delete Documents With or Without Their Cached Text**: The History dialog (`Control + H`) now offers two ways to delete a document — press Delete and choose **Delete from history only** or **Delete from history and cached text**. The second option clears that document's cached OCR text, so the next open re-scans it from scratch — ideal after a poor scan. A **Don't ask again** checkbox remembers your choice for future deletions. Your interrupted-operation resume data is never touched.
*   **Engine-Aware, Merging OCR Cache in the Document Reader**: Cached OCR text is now stored per OCR engine, so switching the OCR engine always re-scans with the new engine instead of replaying the old result. Reopening a document shows the page-range dialog again (pre-filled with your last choice), instantly reusing already-scanned pages and scanning only the missing ones — the cache merges page by page instead of being replaced, so every range you read is kept for later.
*   **PDF Compression in Document Reader**: Added an optional **Compress PDF pages before processing** setting in the Document Reader's page range dialog. When uploading large or high-resolution scanned PDF documents to Gemini or Mistral, pages are automatically downscaled and re-compressed to dramatically reduce upload payload size, speed up processing, and prevent network timeouts. The option is disabled by default and automatically hidden when using the Chrome engine or base64-based image providers.
*   **Per-Prompt Feedback Behavior Customization**: Customize how each custom prompt delivers its output individually! In the custom prompt editor, choose between **Global setting**, **Copy to clipboard**, **Direct Output (NVDA message)**, **Copy to clipboard and Direct Output**, or **Chat window**. This allows specific prompts to speak directly without opening a window while others open a full chat.
*   **New Dynamic Prompt Variables (`[currentURL]` & `[text]`)**: Custom Prompts now support `[currentURL]` to capture the active document URL across Google Chrome, Mozilla Firefox, and Microsoft Edge, and `[text]` to dynamically insert the full text content of the currently focused edit field (ignoring protected password boxes).
*   **Twitter/X Video Downloader Overhaul**: Restored downloading and analysis of Twitter/X videos following upstream scraper failures. Video extraction now utilizes the robust FixTweet API to directly fetch highest-quality MP4 streams from Twitter's CDN, complete with automatic TwitSave fallback and proxy support.
*   **Instagram Video Downloader Fix**: Restored downloading and analysis of Instagram Reels and video URLs following upstream form changes on the downloader service.
*   **Fixes & Performance**: Push to Talk answers the moment you press the key, the Live Assistant no longer starts a reply in the middle of a sentence, the observer no longer reports the previous picture, and the Thinking Depth list only offers what your model actually supports. The AI Operator can scroll left and right too. Fixed an `AttributeError` when analyzing online videos, and prevented custom prompts without text selection from accidentally injecting background window titles into AI requests.
"""),

    addon_author="Mahmood Hozhabri",
    addon_url="https://github.com/mahmoodhozhabri/VisionAssistantPro",
    addon_sourceURL="https://github.com/mahmoodhozhabri/VisionAssistantPro",
    addon_docFileName="readme.html",
    addon_minimumNVDAVersion="2025.1",
    addon_lastTestedNVDAVersion="2026.2",
    addon_updateChannel="beta",
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
speechDictionaries: SpeechDictionaries = {}
