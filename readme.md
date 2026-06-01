# Vision Assistant Pro Documentation

**Vision Assistant Pro** is an advanced, multi-modal AI assistant for NVDA. It leverages world-class AI engines to provide intelligent screen reading, translation, voice dictation, and document analysis.

_This add-on was released to the community in honor of the International Day of Persons with Disabilities._

## 1. Setup & Configuration

Go to **NVDA Menu > Preferences > Settings > Vision Assistant Pro**.

### 1.1 Connection Settings
- **Provider:** Select your preferred AI service. Supported providers include **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, and **Custom** (OpenAI-compatible servers like Ollama, LM Studio, Jan.ai, or KoboldCPP).
- **Important Note:** We strongly recommend using **Google Gemini** for the best performance and accuracy (especially for image/file analysis).
- **API Key:** Required. You can enter multiple keys (separated by commas or new lines) for automatic rotation.
- **Fetch Models:** After entering your API key, press this button to download the latest list of available models from the provider.
- **AI Model:** Select the main model used for general chat and analysis.

### 1.2 Advanced Model Routing
*Available for all providers including Gemini, OpenAI, Groq, Mistral, and Custom.*

> **⚠️ Warning:** These settings are intended for **advanced users only**. If you are unsure what a specific model does, please leave this **unchecked**. Selecting an incompatible model for a task (e.g., a text-only model for Vision) will cause errors and stop the add-on from working.

Check **"Advanced Model Routing (Task-specific)"** to unlock detailed control. This allows you to select specific models from the dropdown list for different tasks:
- **OCR / Vision Model:** Choose a specialized model for analyzing images.
- **Speech-to-Text (STT):** Choose a specific model for dictation.
- **Text-to-Speech (TTS):** Choose a model for generating audio.
- **AI Operator Model:** Select a specific model for autonomous computer operation tasks.
*Note: Unsupported features (e.g., TTS for Groq) will be automatically hidden.*

### 1.3 Advanced Endpoint Configuration (Custom Provider)
*Available only when "Custom" is selected.*

> **⚠️ Warning:** This section allows for manual API configuration and is designed for **power users** running local servers or proxies. Incorrect URLs or model names will break connectivity. If you don't know exactly what these endpoints are, keep this **unchecked**.

Check **"Advanced Endpoint Configuration"** to manually input server details. Unlike native providers, here you must **type** the specific URLs and Model Names:
- **Models List URL:** The endpoint to fetch available models.
- **OCR/STT/TTS Endpoint URL:** Full URLs for specific services (e.g., `http://localhost:11434/v1/audio/speech`).
- **Custom Models:** Manually type the model name (e.g., `llama3:8b`) for each task.

### 1.3.1 Setup Local AI (One-Action Configuration)
To make local, completely offline AI integration extremely simple, a dedicated **"Setup Local AI"** button is available inside the Custom Provider Settings.

If you are running a local AI model server on your computer:
1. Select **Custom** as your Provider.
2. Press the **Setup Local AI** button.
3. Choose your local AI engine from the accessible dialog:
   - **Ollama** (defaulting to `http://127.0.0.1:11434`)
   - **LM Studio** (defaulting to `http://127.0.0.1:1234`)
   - **Jan.ai** (defaulting to `http://127.0.0.1:1337`)
   - **KoboldCPP** (defaulting to `http://127.0.0.1:5001`)
4. The add-on will instantly configure the correct local URL, API type, and automatically fetch your active offline models to populate the **AI Model** selection box.

*Note on Network & Proxies:* This local connection engine features an advanced proxy bypass mechanism. Even if you are running an active system VPN or TUN-mode proxy, your local AI requests will bypass it completely, ensuring stable offline connections without 502 Bad Gateway errors.

### 1.4 General Preferences
- **OCR Engine:** Choose between **Chrome (Fast)** for quick results or **AI (Advanced)** for superior layout preservation.
    - *Note:* If you select "AI (Advanced)" but your provider is set to OpenAI/Groq, the addon will intelligently route the image to your active provider's vision model.
- **TTS Voice:** Select your preferred voice style. This list updates dynamically based on your active provider.
- **Creativity (Temperature):** Controls the randomness of the AI. Lower values are better for accurate translation/OCR.
- **Proxy URL:** Configure this if AI services are restricted in your region (supports local proxies like `127.0.0.1` or bridge URLs).

## 2. Command Layer & Shortcuts

To prevent keyboard conflicts, this add-on uses a **Command Layer**.
1. Press **NVDA + Shift + V** (Master Key) to activate the layer (you will hear a beep).
2. Release keys, then press one of the following single keys:

| Key           | Function                 | Description                                                                 |
|---------------|--------------------------|-----------------------------------------------------------------------------|
| **Shift + A** | **AI Operator**         | **Autonomous Operation:** Tell the AI to perform a task on your screen. Pressing it again instantly aborts active operations. |
| **E**         | **UI Explorer**          | **Interactive Click:** Identifies and clicks UI elements in any app.        |
| **T**         | Smart Translator         | Translates text under navigator cursor or selection.                        |
| **Shift + T** | Clipboard Translator     | Translates content currently in the clipboard.                              |
| **R**         | Text Refiner             | Summarize, Fix Grammar, Explain, or run **Custom Prompts**.                 |
| **V**         | Object Vision            | Describes the current navigator object.                                     |
| **O**         | Full Screen Vision       | Analyzes the entire screen layout and content.                              |
| **Shift + V** | Online Video Analysis    | Analyze **YouTube**, **Instagram**, **TikTok**, or **Twitter (X)** videos.  |
| **D**         | Document Reader          | Advanced reader for PDF and images with page range selection.               |
| **F**         | **Smart File Action**    | Context-aware recognition from selected image, PDF, or TIFF files.          |
| **A**         | Audio Transcription      | Transcribe MP3, WAV, or OGG files into text.                                |
| **C**         | CAPTCHA Solver           | Captures and solves CAPTCHAs (Supports Gov portals).                        |
| **S**         | Smart Dictation          | Converts speech to text. Press to start recording, again to stop/type.      |
| **I**         | Status Reporting         | Announces current progress (e.g., "Scanning...", "Idle").                   |
| **L**         | **Label Object**         | **Semantic AI Labeling:** Permanently labels the current focused element/icon. |
| **Shift + L** | **Manage/Scan Labels**   | Opens Label Manager (if labels exist) or scans the app for unnamed elements. |
| **U**         | Update Check             | Manually check GitHub for the latest version of the add-on.                 |
| **Space**     | Recall Last Result       | Shows the last AI response in a chat dialog for review or follow-up.        |
| **H**         | Commands Help            | Displays a list of all available shortcuts.                                 |

### 2.1 Document Reader Shortcuts (Inside Viewer)
- **Ctrl + PageDown:** Move to the next page.
- **Ctrl + PageUp:** Move to the previous page.
- **Alt + A:** Open a chat dialog to ask questions about the document.
- **Alt + R:** Force a **Re-scan with AI** using your active provider.
- **Alt + G:** Generate and save a high-quality audio file (WAV/MP3). *Hidden if provider doesn't support TTS.*
- **Alt + S / Ctrl + S:** Save the extracted text as a TXT or HTML file.

## 3. Custom Prompts & Variables

You can manage prompts in **Settings > Prompts > Manage Prompts...**.

### Supported Variables
- `[selection]`: Currently selected text.
- `[clipboard]`: Clipboard content.
- `[screen_obj]`: Screenshot of the navigator object.
- `[screen_full]`: Full screen screenshot.
- `[file_ocr]`: Select image/PDF file for text extraction.
- `[file_read]`: Select document for reading (TXT, Code, PDF).
- `[file_audio]`: Select audio file for analysis (MP3, WAV, OGG).

***
**Note:** An active internet connection is required for all AI features. Multi-page documents are processed automatically.

## 4. Support & Community

Stay updated with the latest news, features, and releases:
- **Telegram Channel:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** For bug reports and feature requests.

## 5. Project Supporters

A heartfelt thank you to our community members who support the continuous development and maintenance of this project through their generous financial contributions:

*   **@Alyabani94**
*   **Ali Alamri**
*   **Ilya**

*If you wish to support the project financially and see your name here, you can find the **Donate** option in the NVDA Tools menu (Vision Assistant submenu) or during the setup process after installation.*


---
## Changes for 6.1.1

*   **Gemma 4 Thinking Output Fix**: Fixed an issue with Gemma 4 models where the entire internal thought process was displayed as the final response, or where disabling thinking resulted in empty responses. The add-on now correctly isolates and extracts only the final clean text response.
*   **Batch OCR from File Explorer**: You can now select multiple photos or PDFs directly in Windows File Explorer and extract text or analyze them in batch. The add-on will automatically filter and process only the supported file formats.

## Changes for 6.1.0

*   **Universal Local AI Integration (Setup Local AI)**: Added a new **"Setup Local AI"** button in Custom Provider Settings. Users can now automatically configure local AI engines, including **Ollama**, **LM Studio**, **Jan.ai**, and **KoboldCPP** instantly.
*   **Intelligent Local Proxy Bypass**: Rebuilt the connection logic with an advanced proxy bypass mechanism. The add-on is now smart enough to completely bypass Windows system proxies for local loopback connections, ensuring stable local AI connections even when your VPN/TUN-mode is active.
*   **Ultra-Stable AI Labeling (v2)**: Replaced absolute screen coordinate keys with an advanced, hybrid **Object Signature** system. Labels now rely on programmatic identifiers (UIA **AutomationId** or Win32 **ControlID**) and window-relative coordinates, making your custom labels completely resistant to window resizing, moving, monitor switching, or scaling.
*   **Seamless Automatic Label Migration**: Upgrading is completely transparent. The add-on will automatically migrate your older legacy coordinate-based labels to the new stable fingerprint format in the background upon first focus, with zero data loss.

## Changes for 6.0

*   **Introducing Semantic AI Labeling**: Users can now permanently label unnamed buttons and icons using AI. Press **L** to label the current navigator object (supporting both Tab focus and object navigation) or **Shift+L** to scan and label the entire application at once.
*   **Intelligent Label Management**: Added a new, fully accessible Label Manager dialog (via **Shift+L** if labels exist) to view, rename, or batch-delete custom labels.
*   **Direct File Analysis (Bypass File Dialog)**: The add-on is now smart enough to detect if you are currently focusing on a PDF or image file in Windows File Explorer. Pressing **F (Smart File Action)** or **D (Document Reader)** on a highlighted file will immediately process it, bypassing the standard "Open" dialog entirely.

## Changes for 5.6

*   **Added "None (Extract Text Layer)" OCR Engine**: Users can now extract text directly from searchable PDFs without using AI credits, significantly improving speed and privacy for text-based documents.
*   **Refined UI Explorer Accuracy**: Improved the UI Explorer prompt to better identify element types (like List Items) and accurately report states such as "(Checked)", "(Selected)", or "(Expanded)" while ignoring Windows system components like the Taskbar and Clock.
*   **Installation Setup Reminder**: Added a notification after installation to guide users to the settings menu for configuring their API keys and preferences.

## Changes for 5.5.2

*   **Fixed AI Operator Typing Issue:** Resolved a bug where the letter 'v' was typed instead of pasting text on certain systems. This fix addresses timing conflicts that occurred during high system load.
*   **Enhanced Stability:** Added robust error handling for clipboard operations to prevent addon crashes when the system clipboard is temporarily locked by other applications.
*   **Timing Optimization:** Adjusted internal delays for keyboard events to ensure higher reliability across different system speeds and better compatibility with third-party Clipboard Managers.

## Changes for 5.5 (The Automation Update)

*   **AI Operator (Autonomous Control - Shift+A):** This is the crown jewel of v5.5. Vision Assistant Pro has graduated from being a passive assistant to becoming your personal **AI Operator**. It doesn't just describe the screen—it takes command.
    *   *How it works:* You can now give verbal instructions to operate your PC. For example, in a completely inaccessible application where your screen reader stays silent, you can press **Shift+A** and type: *"Click on the Settings button"* or *"Find the search field, type 'Latest News' and press enter."* The AI visually identifies the elements, moves the mouse, and executes the task for you.
    *   *Performance Note:* This feature is optimized for **Gemini 3.0 Flash (Preview)**, delivering incredibly fast and intelligent responses that can handle even the most complex UI layouts.
    *   **⚠️ API Usage Warning:** Because the AI Operator needs to "see" exactly what's happening to be accurate, it sends a high-resolution screenshot with every step. Please note that frequent use will consume your API quota much faster than standard text-based tasks.
*   **Visual UI Explorer (E):** Tired of navigating through "unlabeled buttons"? Press **E** to activate the UI Explorer. The AI will scan the entire window and generate a list of every clickable element it sees—including icons, graphics, and menus. Simply pick an item from the list, and the AI Operator will click it for you. It’s like having an "accessible layer" on top of any app.
*   **Context-Aware Smart File Action (F):** The "F" key has been completely overhauled. It no longer assumes you only want OCR. When you select a single image, it now intelligently asks for your intent: you can choose a **Detailed Visual Description** to understand the scene or a **Structured Text Extraction (OCR)** for reading. The menu adapts dynamically based on the file type and your active AI engine.
*   **Core Optimization:** We've performed a deep cleanup of the add-on’s internal logic, removing unused legacy functions and redundant code. This results in a leaner, faster, and more reliable experience for all users.

## Changes for 5.0

* **Multi-Provider Architecture**: Added full support for **OpenAI**, **Groq**, and **Mistral** alongside Google Gemini. Users can now choose their preferred AI backend.
* **Advanced Model Routing**: Users of native providers (Gemini, OpenAI, etc.) can now select specific models from a dropdown list for different tasks (OCR, STT, TTS).
* **Advanced Endpoint Configuration**: Custom provider users can manually input specific URLs and model names for granular control over local or third-party servers.
* **Smart Feature Visibility**: The settings menu and Document Reader UI now automatically hide unsupported features (like TTS) based on the selected provider.
* **Dynamic Model Fetching**: The addon now fetches the available model list directly from the provider's API, ensuring compatibility with new models as soon as they are released.
* **Hybrid OCR & Translation**: Optimized the logic to use Google Translate for speed when using Chrome OCR, and AI-powered translation when using Gemini/Groq/OpenAI engines.
* **Universal "Re-scan with AI"**: The Document Reader's re-scan feature is no longer limited to Gemini. It now utilizes whatever AI provider is currently active to re-process pages.

## Changes for 4.6
* **Interactive Result Recall:** Added the **Space** key to the command layer, allowing users to instantly reopen the last AI response in a chat window for follow-up questions, even when "Direct Output" mode is active.
* **Telegram Community Hub:** Added an "Official Telegram Channel" link to the NVDA Tools menu, providing a quick way to stay updated with the latest news, features, and releases.
* **Enhanced Response Stability:** Optimized the core logic for Translation, OCR, and Vision features to ensure more reliable performance and a smoother experience when using direct speech output.
* **Improved Interface Guidance:** Updated the settings descriptions and documentation to better explain the new recall system and how it works alongside the direct output settings.

## Changes for 4.5
* **Advanced Prompt Manager:** Introduced a dedicated management dialog in settings to customize default system prompts and manage user-defined prompts with full support for adding, editing, reordering, and previewing.
* **Comprehensive Proxy Support:** Resolved network connectivity issues by ensuring that user-configured proxy settings are strictly applied to all API requests, including translation, OCR, and speech generation.
* **Automated Data Migration:** Integrated a smart migration system to automatically upgrade legacy prompt configurations to a robust v2 JSON format upon the first run without data loss.
* **Updated Compatibility (2025.1):** Set the minimum required NVDA version to 2025.1 due to library dependencies in advanced features like the Document Reader to ensure stable performance.
* **Optimized Settings Interface:** Streamlined the settings interface by reorganizing prompt management into a separate dialog, providing a cleaner and more accessible user experience.
* **Prompt Variables Guide:** Added a built-in guide within the prompt dialogs to help users easily identify and use dynamic variables such as [selection], [clipboard], and [screen_obj].

## Changes for 4.0.3
*   **Enhanced Network Resilience:** Added an automatic retry mechanism to better handle unstable internet connections and temporary server errors, ensuring more reliable AI responses.
*   **Visual Translation Dialog:** Introduced a dedicated window for translation results. Users can now easily navigate and read long translations line-by-line, similar to OCR results.
*   **Aggregated Formatted View:** The "View Formatted" feature in the Document Reader now displays all processed pages in a single, organized window with clear page headers.
*   **Optimized OCR Workflow:** Automatically skips the page range selection for single-page documents, making the recognition process faster and more seamless.
*   **Improved API Stability:** Switched to a more robust header-based authentication method, resolving potential "All API Keys failed" errors caused by key rotation conflicts.
*   **Bug Fixes:** Resolved several potential crashes, including an issue during add-on termination and a focus error in the chat dialog.

## Changes for 4.0.1
*   **Advanced Document Reader:** A powerful new viewer for PDF and images with page range selection, background processing, and seamless `Ctrl+PageUp/Down` navigation.
*   **New Tools Submenu:** Added a dedicated "Vision Assistant" submenu under NVDA's Tools menu for quicker access to core features, settings, and documentation.
*   **Flexible Customization:** You can now choose your preferred OCR engine and TTS voice directly from the settings panel.
*   **Multiple API Key Support:** Added support for multiple Gemini API keys. You can enter one key per line or separate them with commas in the settings.
*   **Alternative OCR Engine:** Introduced a new OCR engine to ensure reliable text recognition even when hitting Gemini API quota limits.
*   **Smart API Key Rotation:** Automatically switches to and remembers the fastest working API key to bypass quota limits.
*   **Document to MP3/WAV:** Integrated capability to generate and save high-quality audio files in both MP3 (128kbps) and WAV formats directly within the reader.
*   **Instagram Stories Support:** Added the ability to describe and analyze Instagram Stories using their URLs.
*   **TikTok Support:** Introduced support for TikTok videos, allowing for full visual description and audio transcription of clips.
*   **Redesigned Update Dialog:** Features a new accessible interface with a scrollable text box to clearly read version changes before installing.
*   **Unified Status & UX:** Standardized file dialogs across the add-on and enhanced the 'L' command to report real-time progress.

## Changes for 3.6.0
*   **Help System:** Added a help command (`H`) within the Command Layer to provide an easy-to-access list of all shortcuts and their functions.
*   **Online Video Analysis:** Expanded support to include **Twitter (X)** videos. Also improved URL detection and stability for a more reliable experience.
*   **Project Contribution:** Added an optional donation dialog for users who wish to support the project’s future updates and continuous growth.

## Changes for 3.5.0
\*   \*\*Command Layer:\*\* Introduced a Command Layer system (default: `NVDA+Shift+V`) to group shortcuts under a single master key. For example, instead of pressing `NVDA+Control+Shift+T` for translation, you now press `NVDA+Shift+V` followed by `T`.
\*   \*\*Online Video Analysis:\*\* Added a new feature to analyze YouTube and Instagram videos directly by providing a URL.

## Changes for 3.1.0
*   **Direct Output Mode:** Added an option to skip the chat dialog and hear AI responses directly via speech for a faster and more seamless experience.
*   **Clipboard Integration:** Added a new setting to automatically copy AI responses to the clipboard.

## Changes for 3.0

*   **New Languages:** Added **Persian** and **Vietnamese** translations.
*   **Expanded AI Models:** Reorganized the model selection list with clear prefixes (`[Free]`, `[Pro]`, `[Auto]`) to help users distinguish between free and rate-limited (paid) models. Added support for **Gemini 3.0 Pro** and **Gemini 2.0 Flash Lite**.
*   **Dictation Stability:** Significantly improved Smart Dictation stability. Added a safety check to ignore audio clips shorter than 1 second, preventing AI hallucinations and empty errors.
*   **File Handling:** Fixed an issue where uploading files with non-English names would fail.
*   **Prompt Optimization:** Improved Translation logic and structured Vision results.
## Changes for 2.9

*   **Added French and Turkish translations.**
*   **Formatted View:** Added a "View Formatted" button in chat dialogs to view the conversation with proper styling (Headings, Bold, Code) in a standard browseable window.
*   **Markdown Setting:** Added a new option "Clean Markdown in Chat" in Settings. Unchecking this allows users to see raw Markdown syntax (e.g., `**`, `#`) in the chat window.
*   **Dialog Management:** Fixed an issue where the "Refine Text" or chat windows would open multiple times or fail to focus correctly.
*   **UX Improvements:** Standardized file dialog titles to "Open" and removed redundant speech announcements (e.g., "Opening menu...") for a smoother experience.

## Changes for 2.8
* Added Italian translation.
* **Status Reporting:** Added a new command (NVDA+Control+Shift+I) to announce the current status of the add-on (e.g., "Uploading...", "Analyzing...").
* **HTML Export:** The "Save Content" button in result dialogs now saves output as a formatted HTML file, preserving styles like headings and bold text.
* **Settings UI:** Improved the Settings panel layout with accessible grouping.
* **New Models:** Added support for gemini-flash-latest and gemini-flash-lite-latest.
* **Languages:** Added Nepali to supported languages.
* **Refine Menu Logic:** Fixed a critical bug where "Refine Text" commands would fail if the NVDA interface language was not English.
* **Dictation:** Improved silence detection to prevent incorrect text output when no speech is input.
* **Update Settings:** "Check for updates on startup" is now disabled by default to comply with Add-on Store policies.
* Code Cleanup.

## Changes for 2.7
* Migrated project structure to the official NV Access Add-on Template for better standards compliance.
* Implemented automatic retry logic for HTTP 429 (Rate Limit) errors to ensure reliability during high traffic.
* Optimized translation prompts for higher accuracy and better "Smart Swap" logic handling.
* Updated Russian translation.

## Changes for 2.6
* Added Russian translation support (Thanks to nvda-ru).
* Updated error messages to provide more descriptive feedback regarding connectivity.
* Changed default target language to English.

## Changes for 2.5
* Added Native File OCR Command (NVDA+Control+Shift+F).
* Added "Save Chat" button to result dialogs.
* Implemented full localization support (i18n).
* Migrated audio feedback to NVDA's native tones module.
* Switched to Gemini File API for better handling of PDF and audio files.
* Fixed crash when translating text containing curly braces.

## Changes for 2.1.1
* Fixed an issue where the [file_ocr] variable was not functioning correctly within Custom Prompts.

## Changes for 2.1
* Standardized all shortcuts to use NVDA+Control+Shift to eliminate conflicts with NVDA's Laptop layout and system hotkeys.

## Changes for 2.0
* Implemented built-in Auto-Update system.
* Added Smart Translation Cache for instant retrieval of previously translated text.
* Added Conversation Memory to contextually refine results in chat dialogs.
* Added Dedicated Clipboard Translation command (NVDA+Control+Shift+Y).
* Optimized AI prompts to strictly enforce target language output.
* Fixed crash caused by special characters in input text.

## Changes for 1.5
* Added support for over 20 new languages.
* Implemented Interactive Refine Dialog for follow-up questions.
* Added Native Smart Dictation feature.
* Added "Vision Assistant" category to NVDA's Input Gestures dialog.
* Fixed COMError crashes in specific applications like Firefox and Word.
* Added automatic retry mechanism for server errors.

## Changes for 1.0
* Initial release.
