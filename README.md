Vision Assistant Pro Documentation

# Vision Assistant Pro

**Vision Assistant Pro** is an advanced, multi-modal AI assistant for NVDA. It leverages Google's Gemini models to provide intelligent screen reading, translation, voice dictation, and document analysis capabilities.

_This add-on was released to the community in honor of the International Day of Persons with Disabilities._

## 1. Setup & Configuration

Go to **NVDA Menu > Preferences > Settings > Vision Assistant Pro**.

- **API Key:** Required. Get a free key from [Google AI Studio](https://aistudio.google.com/).
- **Model:** Choose `gemini-2.5-flash-lite` (Fastest) or standard Flash models.
- **Languages:** Set Source, Target, and AI Response languages.
- **Smart Swap:** Automatically swaps languages if the source text matches the target language.

## 2. Global Shortcuts

To ensure maximum compatibility with laptop layouts, all shortcuts use **NVDA + Control + Shift**.

| Shortcut                    | Function             | Description                                                                 |
|-----------------------------|----------------------|-----------------------------------------------------------------------------|
| NVDA+Ctrl+Shift+T           | Smart Translator     | Translates the text under the navigator cursor. Prioritizes selection.     |
| NVDA+Ctrl+Shift+Y           | Clipboard Translator | Translates clipboard content. **Recommended for web browsers**.            |
| NVDA+Ctrl+Shift+S           | Smart Dictation      | Converts speech to text. Press once to start, again to stop and type.       |
| NVDA+Ctrl+Shift+R           | Text Refiner         | Summarize, Fix Grammar, Explain, or run **Custom Prompts**.                 |
| NVDA+Ctrl+Shift+C           | CAPTCHA Solver       | Captures and solves CAPTCHA automatically.                                 |
| NVDA+Ctrl+Shift+V           | Object Vision        | Describes the navigator object with follow-up chat.                         |
| NVDA+Ctrl+Shift+O           | Full Screen Vision   | Analyzes entire screen layout and content.                                  |
| NVDA+Ctrl+Shift+D           | Document Analysis    | Chat with PDF/TXT/MD/PY files.                                              |
| NVDA+Ctrl+Shift+F           | File OCR             | Direct OCR from image/PDF file.                                             |
| NVDA+Ctrl+Shift+A           | Audio Transcription  | Transcribe MP3/WAV/OGG files.                                               |
| NVDA+Ctrl+Shift+L           | Last Translation     | Re-read last translation without API.                                      |
| NVDA+Ctrl+Shift+U           | Update Check         | Check GitHub for latest version.                                            |

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

**Note:** File uploads limited to 15MB. Internet required. Multi-page TIFFs supported.

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