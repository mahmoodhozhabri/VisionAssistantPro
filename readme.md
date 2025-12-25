Vision Assistant Pro Documentation

# Vision Assistant Pro

**Vision Assistant Pro** is an advanced, multi-modal AI assistant for NVDA. It leverages Google's Gemini models to provide intelligent screen reading, translation, voice dictation, and document analysis capabilities.

_This add-on was released to the community in honor of the International Day of Persons with Disabilities._

## 1. Setup & Configuration

Go to **NVDA Menu > Preferences > Settings > Vision Assistant Pro**.

- **API Key:** Required. The field is masked by default for security (use "Show API Key" to view). Get a free key from [Google AI Studio](https://aistudio.google.com/).
- **Model:** Choose between **Flash** (Fastest/Free) or **Pro** (High Intelligence) models based on your needs.
- **Proxy URL:** Optional. Use this if Google is blocked in your region. You need a server address (URL) that receives your requests and forwards them to the Gemini API.
  > **Note:** This is **not** for standard VPN/SOCKS proxies (like `127.0.0.1:1080`). It must be a web address (e.g., `https://my-custom-proxy.com`) that acts as a bridge to Google.
- **Languages:** Set Source, Target, and AI Response languages.
- **Smart Swap:** Automatically swaps languages if the source text matches the target language.
- **Direct Output:** Skips the chat window and announces the response directly via speech.
- **Clipboard Integration:** Automatically copies the AI response to the clipboard.

## 2. Command Layer & Shortcuts

To prevent keyboard conflicts, this add-on uses a **Command Layer**.
1. Press **NVDA + Shift + V** (Master Key) to activate the layer (you will hear a beep).
2. Release keys, then press one of the following single keys:

| Key           | Function                 | Description                                                                 |
|---------------|--------------------------|-----------------------------------------------------------------------------|
| **T**         | Smart Translator         | Translates text under navigator cursor or selection.                        |
| **Shift + T** | Clipboard Translator     | Translates content currently in the clipboard.                              |
| **R**         | Text Refiner             | Summarize, Fix Grammar, Explain, or run **Custom Prompts**.                 |
| **V**         | Object Vision            | Describes the current navigator object.                                     |
| **O**         | Full Screen Vision       | Analyzes the entire screen layout and content.                              |
| **Shift + V** | Online Video Analysis    | Analyze **YouTube** or **Instagram** videos via URL.                        |
| **D**         | Document Analysis        | Chat with PDF/TXT/MD/PY files.                                              |
| **F**         | File OCR                 | Direct OCR from image/PDF/TIFF files (Multi-page TIFF supported).           |
| **A**         | Audio Transcription      | Transcribe MP3/WAV/OGG files.                                               |
| **C**         | CAPTCHA Solver           | Captures and solves CAPTCHA automatically.                                  |
| **S**         | Smart Dictation          | Converts speech to text. Press to start recording, again to stop/type.      |
| **L**         | Status Reporting         | Announces the current status (e.g., "Uploading...", "Idle").                |
| **U**         | Update Check             | Check GitHub for the latest version.                                        |

## 3. Custom Prompts & Variables

Create commands in Settings: `Name:Prompt Text` (separate with `|` or new lines).

### Available Variables

| Variable         | Description                                      | Input Type       |
|------------------|--------------------------------------------------|------------------|
| `[selection]`    | Currently selected text                          | Text             |
| `[clipboard]`    | Clipboard content                                | Text             |
| `[screen_obj]`   | Screenshot of navigator object                   | Image            |
| `[screen_full]`  | Full screen screenshot                           | Image            |
| `[file_ocr]`     | Select image/PDF/TIFF (defaults to "Extract text")| Image, PDF, TIFF |
| `[file_read]`    | Select text document                             | TXT, Code, PDF   |
| `[file_audio]`   | Select audio file                                | MP3, WAV, OGG    |

### Example Custom Prompts

- **Quick OCR:** `My OCR:[file_ocr]`
- **Translate Image:** `Translate Img:Extract text from this image and translate to Persian. [file_ocr]`
- **Analyze Audio:** `Summarize Audio:Listen to this recording and summarize the main points. [file_audio]`
- **Code Debugger:** `Debug:Find bugs in this code and explain them: [selection]`

**Note:** An active internet connection is required for all AI features. Multi-page TIFFs are automatically processed.

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