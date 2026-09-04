# Vision Assistant Pro Documentation

<!-- DOWNLOAD_COUNT_START --> Total Downloads: 72,209 <!-- DOWNLOAD_COUNT_END -->

**Vision Assistant Pro** is an advanced, multi-modal AI assistant for NVDA. It leverages world-class AI engines to provide intelligent screen reading, translation, voice dictation, and document analysis.

_This add-on was released to the community in honor of the International Day of Persons with Disabilities._

## 1. Setup & Configuration

Go to **NVDA Menu > Preferences > Settings > Vision Assistant Pro**. The settings dialog is organized into 9 accessible tabs: **Connection**, **Live Assistant**, **AI Behavior**, **Translation Languages**, **Document Reader**, **Video**, **CAPTCHA**, **Prompts**, and **Advanced**.

### 1.1 Connection Tab
- **Provider:** Select your preferred AI service. Supported providers include **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax**, and **Custom** (OpenAI-compatible servers like Ollama, LM Studio, Jan.ai, or KoboldCPP).
- **API Key:** Enter single or multiple API keys (separated by commas or newlines) for automatic rotation.
- **Fetch Models:** Press this button after entering your API key to download the latest available model list from the provider.
- **AI Model:** Select the main model used for general chat and analysis.
- **Custom Provider Settings:** Configure local or custom endpoints. Includes **Setup Local AI** (one-click setup for Ollama, LM Studio, Jan.ai, or KoboldCPP) and **Advanced Endpoint Configuration**.
- **Advanced Model Routing (Task-specific):** Optionally select dedicated models from dropdowns for OCR, STT, TTS, AI Operator, Video, and Live Assistant tasks.
- **Connection & Output Options:** Configure Proxy URL, startup update checks, Clean Markdown in Chat, Copy AI responses to clipboard, and Direct Output (No Chat Window).

### 1.2 Live Assistant Tab
- **Live Assistant: Direct Output (No Window):** Start the Live Assistant without its conversation window; open it later with the Recall Last Result key (`Space`).
- **Push to Talk:** Toggle push-to-talk mode. When enabled, your microphone only sends audio while you hold the assigned key.
- **Push to Talk Key:** Press the keys to record the shortcut (for example `F12` or `Ctrl+F12`) — you can even assign a lone modifier like `Left Ctrl`. Hold the key to speak and release it to finish; a short beep confirms each press and release.

Note: This tab appears only when **Google Gemini** (or a Gemini-compatible Custom provider) is your active provider.

### 1.3 AI Behavior Tab
- **Creativity (Temperature):** Controls AI randomness and creativity (from 0.0 to 2.0). Lower values produce more deterministic and accurate translation/OCR results.

### 1.4 Translation Languages Tab
- **Source Language:** Select your default input language.
- **Target Language:** Select your primary target translation language.
- **AI Response Language:** Select the language for general AI responses.
- **Smart Swap:** Automatically swaps source and target languages based on detected input.

### 1.5 Document Reader Tab
- **OCR Engine:** Choose between **Chrome (Fast)** for quick results or **AI (Advanced)** for superior layout preservation.
- **OCR Batch Size:** Specify pages per request (set to 0 for single-request processing).
- **Describe Images Inline:** Toggle inline image descriptions during document text extraction.
- **Export Page Numbers:** Toggle page numbers and separators in multi-page document outputs.
- **TTS Voice:** Select default voice style for audio generation.

### 1.6 Video Tab
- **Video Chunk Size:** Segment duration in minutes for Audio Description generation (set to 0 to process whole file).
- **Add Character List:** Option to add character dictionary as the first subtitle entry.
- **Add AI Disclaimer:** Option to insert an AI disclaimer at the beginning of video SRT subtitles.

### 1.7 CAPTCHA Tab
- **Enable Visual CAPTCHA Solver:** Toggle automated visual challenge solving (hCaptcha, reCAPTCHA).
- **Text CAPTCHA Method:** Choose between capturing the **Navigator Object** or **Full Screen**.

### 1.8 Prompts Tab
- **Manage Prompts:** Opens a dedicated dialog to customize default system prompts or create, edit, reorder, and preview custom user-defined prompts with dynamic variables (e.g., `[selection]`, `[screen_fg_obj]`).
- **Custom Prompt Shortcuts:** Assign a dedicated shortcut key to any custom prompt right in the Prompt Manager. Press the keys to record them — single keys run inside the Command Layer (and globally as `NVDA + Shift + key`), while combinations like `Control + Shift + 1` run globally on their own.

### 1.9 Advanced Tab & Global Logging
Navigate to the **Advanced** tab to configure global add-on logging:
- **Enable dedicated log file:** Toggles logging of all operational events, API traffic, and errors across all add-on modules into a separate file (`vision_assistant.log`).
- **Log Level:** Select verbosity between **Debug (All Details)**, **Info (General Information)**, **Warning (Warnings Only)**, and **Error (Errors Only)**.
- **Keep Logs For:** Set automatic retention periods to automatically clean up older log entries (ranging from 1 hour to 90 days).
- **Log Management Controls:** Use **Open Log File**, **Open Log Folder**, or **Clear Log File** to inspect or clear log data directly without restarting NVDA or interfering with standard NVDA logs.

### 1.10 Settings Backup & Restore
The **Advanced** tab also includes a **Backup and Restore** section:
- **Backup:** Saves your configuration into a single JSON file. When you click it, you choose what to include: **Everything** (settings, custom labels, OCR progress, and history) or **Settings Only**.
- **Restore:** Loads a previously saved backup to restore your configuration and data at any time, on any machine, or after reinstalling NVDA. You will be asked to confirm first, since restoring replaces all of your current settings and data.

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
| **Shift + V** | Video Analysis    | Analyze local video files or online **YouTube**, **Instagram**, **TikTok**, or **Twitter (X)** videos.  |
| **Control + V** | Local Video Recording  | Records a silent video of your screen and analyzes the actions and layout.  |
| **D**         | Document Reader          | Advanced reader for PDF, images, and plain text/HTML files with page range selection.               |
| **F**         | **Smart File Action**    | Context-aware recognition from selected image, PDF, or TIFF files.          |
| **M**         | Media Transcription & Dubbing | Transcribe or Dub audio/video files (MP3, WAV, MP4, etc.) into your target language. |
| **C**         | CAPTCHA Solver           | Captures and solves CAPTCHAs.                        |
| **Shift + C** | Direct Chat              | Opens a direct text-based chat interface with the AI.                       |
| **S**         | Smart Dictation          | Converts speech to text. Press to start recording, again to stop/type.      |
| **Control+T** | Voice Translation        | Transcribes, translates, and types the result based on your language settings. |
| **Control+L** | **Live Assistant**       | **Real-time Copilot (Gemini only):** Starts or ends a live voice and screen conversation with the AI assistant. |
| **I**         | Status Reporting         | Announces current progress (e.g., "Scanning...", "Idle").                   |
| **L**         | **Label Object**         | **Semantic AI Labeling:** Permanently labels the current focused element/icon. |
| **Shift + L** | **Manage/Scan Labels**   | Opens Label Manager (if labels exist) or scans the app for unnamed elements. |
| **U**         | Update Check             | Manually check GitHub for the latest version of the add-on.                 |
| **Space**     | Recall Last Result       | Shows the last AI response in a chat dialog for review or follow-up.        |
| **H**         | Commands Help            | Displays a list of all available shortcuts.                                 |
| **Control + H** | **History**            | Opens the History dialog listing your past chats and documents, with type filters and Delete/Clear options. |
| **Alt + S**   | Settings                 | Opens the Vision Assistant Pro settings dialog.                             |
| **Alt + Q**   | Quota Exhausted Keys Report | Reports the number of Gemini API keys that have exceeded their daily quota and their reset time. |
| **Alt + M**   | Routing Audit            | Reports the AI models currently selected in advanced routing.               |
| **Up / Down** | Quick Settings Nav       | Navigates between quick settings categories (Provider, Model, etc.) in the layer. |
| **Left / Right**| Change Quick Setting   | Changes the value of the currently selected quick setting.                  |

## 3. Chat & History

Chat windows and the History dialog work across all features, so you can review conversations and pick up right where you left off.

### 3.1 Chat Window Shortcuts
When a chat window is open (Direct Chat, document chat, refine, and similar), you can review the conversation with:
- **Alt + Down:** Read the next message.
- **Alt + Up:** Read the previous message.
- **Alt + C:** Copy the current message.

### 3.2 History (Control + H)
Press **Control + H** in the Command Layer to open the **History** dialog with your past chats and documents, filterable by type (All / Chats / Documents). Open a chat to continue the conversation — including its attached files, which are re-attached automatically — or open a document and keep reading. Press **Delete** on any item to remove it, or **Clear All** to empty the list.

## 4. AI Operator - Autonomous Computer Control

The **AI Operator** turns Vision Assistant Pro from a passive reader into an active assistant that can interact with your computer on your behalf. You can ask it to describe the screen, answer questions about what it sees, or even take control—clicking buttons, dragging items, typing text, and navigating through applications using natural language commands.

The biggest advantage? It works perfectly in completely inaccessible software. If you are stuck in a custom app, a remote desktop, or a website where your screen reader goes totally silent, the operator doesn't mind. Because it "sees" the screen visually, it can find, read, and interact with elements that have zero accessibility labels.

### How It Works
1. Press **NVDA + Shift + V**, then press **Shift + A** (or use the direct shortcut) to open the AI Operator dialog.
2. Type what you want to do in plain language (e.g., "Click the Save button", "What does the error message say?", or "Rename the file to final.pdf").
3. The AI will analyze your screen, identify the relevant elements, and carry out the action or provide the answer. If a task requires multiple steps, the operator will continue working until it's complete.
4. Press **Shift + A** again at any time to instantly abort an ongoing operation.

### Supported Actions
The operator understands a wide range of commands:
- **Describe & Answer**: "Describe the screen layout" or "What does the error message say?"
- **Click**: "Click the Save button"
- **Right Click**: "Right-click the file"
- **Double Click**: "Double-click the document"
- **Drag & Drop**: "Drag the document to the Archive folder"
- **Type**: "Type 'Hello World' in the search box"
- **Scroll**: "Scroll down three times"
- **Keypress**: "Press Enter", "Press Tab", "Press Escape"
- **Multi-step Tasks**: "Open File Explorer, find the report, and rename it to final.pdf"

### Important Notes
- **⚠️ API Usage Warning**: Because the operator needs to "see" exactly what's happening on screen, it sends a high-resolution screenshot with every step. Frequent use will consume your API quota much faster than standard text-based features.
- **Administrator Applications**: If NVDA is not running with Administrator privileges, the operator may not be able to interact with windows that require elevated permissions. This is a Windows security limitation, not a bug in the add-on.
- **Best Practices**: For best results, give clear and specific commands. "Click the blue Submit button at the bottom of the form" will almost always work better than just "Click the button".

## 5. Video Analysis & Audio Description

> **Note:** The Video Analysis and Audio Description features are strictly powered by the **Google Gemini** provider. Ensure that your active provider in the add-on settings is set to Google Gemini.

Vision Assistant Pro introduces powerful video processing capabilities designed specifically for blind users. It can analyze both online videos and local screen recordings to provide highly detailed visual descriptions and generate professional Audio Description scripts (SRT).

### 5.1 Local Screen Recording (Control + V)
If you encounter a silent video, an animation, or a tutorial on your screen, you can capture it directly:
1. Press **NVDA + Shift + V** to enter the Command Layer, then press **Control + V**.
2. The add-on will silently record your screen in the background.
3. Press **Control + V** again to stop recording.
4. The AI will then analyze the recorded video segment and provide a highly detailed description of the scene, characters, and actions.

### 5.2 Video Analysis (Shift + V)
You can analyze both local video files and online videos. Simply select a local video file in Windows Explorer, or copy an online video link to your clipboard. You can also press **Shift + V** anywhere (like inside a media player) to open a dialog where you can browse for a video file or paste a URL manually.
- **Supported Online Platforms:** YouTube, Instagram, TikTok, and Twitter (X).
- The AI will automatically detect the local file or the URL, process the video, and provide a comprehensive visual description and audio summary.

### 5.3 Audio Description Generation (SRT)
For a more structured experience, the add-on can generate professional Audio Description scripts in standard SubRip (SRT) format. 
- **Smart Gap-Timing:** The AI listens to the audio track and specifically anchors its visual descriptions to natural pauses and silent gaps to intelligently minimize dialogue overlap.
- **Character Tracking:** The engine performs a pre-pass to extract distinct characters based on immutable facial features. It builds a global dictionary to accurately track and label characters across different scenes without confusion.
- **Verbatim Text OCR:** Any text appearing on the screen (signs, phones, credits) is strictly quoted verbatim.
- **How to Use:** To listen to the generated subtitle, simply place the `.srt` file in the same folder as your video file and give it the exact same name. Then, configure your media player (e.g., VLC or PotPlayer) to route the subtitle text directly to your screen reader or TTS engine during playback.

### 5.4 Synchronized Audio Narration (MP3 Export)
Beyond just creating text-based SRT files, the add-on functions as a complete Audio Description production tool by synthesizing the descriptions into speech and mixing them with the video. You can now choose **Gemini Live TTS** as the voice engine, which utilizes the Gemini Live API to generate highly realistic, unlimited voice narration. When generating an MP3 for local video files, you have multiple mixing modes:
- **Standard AD (Mix Voice):** The narration is overlaid directly on top of the video's audio. You will be prompted if you want to apply **Audio Ducking** (lowering the background volume during descriptions) to ensure the narration is clear.
- **Extended AD (Pause Audio):** The engine pauses the original video audio during descriptions, ensuring you never miss a single word of the original dialogue or the AI narration.
- **YouTube Videos:** For YouTube sources (which are not downloaded locally), the MP3 export will strictly contain the synchronized AI voice track without the background video audio.

## 6. Media Transcription & Dubbing (M)
The Audio Transcriber has been completely rebuilt to support both audio and video files (MP3, WAV, MP4, MKV, etc.). Press **M** in the Command Layer to select a media file and choose one of 3 distinct operation modes:
1. **Transcribe (Original Language)**: Accurately transcribes the spoken speech in its original language.
2. **Transcribe and Translate (Target Language)**: Transcribes the speech and translates it into your configured target language.
3. **Dub and Translate (Target Language)** *(Gemini Only)*: A powerful new feature that transcribes the speech, translates it into your target language, and synthesizes a spoken audio dub using the add-on's TTS engine.

## 7. Advanced Document & Image Reader

The **Document Reader** turns your documents into clean, readable text — so you can read, translate, and listen to anything from a scanned book to a stack of photos. It handles multi-page PDFs, complex images, iPhone HEIC formats, and even plain text (`.txt`) and HTML (`.html`, `.htm`) files, which are opened instantly with no OCR or AI processing. Select several files at once and they are merged into a single continuous document in page order. Three OCR engines are available — **Chrome (Fast)**, **AI (Advanced)** for superior layout preservation, and **None (Extract Text Layer)** for searchable PDFs — selected in Settings → Document Reader.

### How It Works
1. Press **NVDA + Shift + V**, then **D** to open the Document Reader — or highlight a file in File Explorer first and press **D** / **F** to skip the file dialog entirely.
2. Pick one or more PDFs or images. The add-on scans them and announces the total page count.
3. In the **Options** dialog, choose the page range (From/To). You can also check **Translate Output** and pick the target language, or toggle **Describe images inline during OCR**.
4. Text extraction starts in the background in batches. You can close the window at any time and continue later — nothing is lost.
5. Once pages are ready, read them in the viewer: move between pages, jump to any page, ask the AI questions, save the text, or generate an audio narration.

### 7.1 Batch Processing & Resume
You don't need to read a massive document all at once. Choose a page range (e.g., `1-20`) or keep the defaults to process everything, and the AI extracts all pages in the background. If NVDA crashes or you interrupt the scan, the add-on remembers your progress and offers to **Resume** exactly where it left off — even across restarts. Completed documents are also cached, so reopening them (from Recent Documents or via **D**) loads the text instantly without re-running OCR, unless the source files have changed.

### 7.2 Smart File Action
You don't always need to open the document first. In Windows File Explorer, simply highlight a PDF, image, or text/HTML file and press **D** (Document Reader) — or highlight a PDF or image and press **F** (Smart File Action) — inside the Command Layer. The add-on instantly bypasses the file dialog and begins processing the highlighted file. Selecting several files at once processes them together as one document.

### 7.3 Document Viewer Controls & Shortcuts
When the Document Reader window is open, you can use the following:

#### Keyboard Shortcuts
- **Ctrl + PageDown / Ctrl + PageUp:** Move to the next / previous page.
- **Down / Up Arrow:** When your cursor reaches the last line of a page, press **Down** to jump to the next page; press **Up** at the top of a page to return to the previous one.
- **Alt + A:** Open a chat dialog to ask questions about the document.
- **Alt + R:** Force a **Re-scan with AI** using your active provider.
- **Alt + G:** Generate and save a high-quality audio file (WAV/MP3). *(Hidden if the provider doesn't support TTS).*
- **Alt + S / Ctrl + S:** Save the extracted text as a TXT or HTML file.

#### Buttons & Controls
- **Go to:** Choose any page from the page selector.
- **View Formatted:** See the whole document combined as formatted text.
- **Retry Failed Pages:** Retry only the batches that failed due to a temporary server error (e.g., high demand). This button appears automatically when needed.
- **TTS Voice / TTS Engine:** Pick the voice, and on Gemini, choose between **Standard TTS** and **Gemini Live** streaming.
- **Previous / Next:** Move between pages (same as the Ctrl+PageUp/Down shortcuts).

### 7.4 Recent Documents (D)
Pressing **D** in the Command Layer lists your recently read documents first. Choose one to continue from the page you were on — even if the OCR already finished — or press **Open File...** (`Ctrl + O`) to browse for a file as usual.

## 8. Semantic AI Labeling & UI Explorer

Stuck in an application with "unlabeled button" everywhere? The Semantic AI Labeling engine solves this permanently.

### 8.1 Permanent Object Labeling (L)
Focus your screen reader on an unlabeled graphic or button and press **L** in the Command Layer. The AI will look at the button visually, determine its function, and apply a permanent label. 
*Unlike older screen reader labeling tools, this add-on uses an advanced hybrid "Object Signature" system (AutomationId/ControlID). Your custom labels will survive window resizing, monitor switching, and application updates!*

### 8.2 Full Application Scan (Shift + L)
Press **Shift + L** to scan the entire active window at once. The AI will find all unlabeled elements and intelligently name them in one go. You can later manage, rename, or batch-delete these labels from the built-in Label Manager.

### 8.3 UI Explorer (E)
Need to interact with an element without navigating to it manually? Press **E** to activate the UI Explorer. The AI will scan the screen and generate an accessible list of every clickable element (ignoring system noise like taskbars). Pick an item from the list, and the add-on will instantly click it for you.

## 9. Live Voice Assistant

The Live Assistant turns Vision Assistant Pro into a real-time, interactive copilot.
*(Note: This feature is exclusive to Google Gemini and Gemini-compatible Custom providers).*

- **Activation:** Press **Control + L** in the Command Layer to open the Live Assistant dialog.
- **Real-time Interaction:** Talk naturally through your microphone. The AI will simultaneously listen to your voice and look at your active screen. You can ask questions like "What am I looking at?" or "Read the third paragraph to me."
- **Push to Talk:** Enable **Push to Talk** in the Live Assistant settings tab (or toggle it right inside the Live Assistant window), then hold your assigned key to speak and release it to finish. This keeps the microphone muted until you press the key — perfect for noisy environments.
- **Customization:** Inside the dialog, you can change the AI's Voice Style (e.g., Professional, Friendly, Upbeat) and adjust its "Thinking Depth" to control how deeply it reasons before answering.

## 10. Custom Prompts & Variables

You can manage prompts in **Settings > Prompts > Manage Prompts...**.

### Custom Prompt Shortcuts
Give any custom prompt its own shortcut key directly in the Prompt Manager, and run it instantly with your current selection or context:
- **Single key** (e.g., `1`, `p`, or `F3`): Works inside the Command Layer, and also globally as `NVDA + Shift + key`.
- **Key combination** (e.g., `Control + Shift + 1`, `Alt + P`, or `Insert + 1`): Works globally on its own.

### Supported Variables
- `[selection]`: Currently selected text.
- `[clipboard]`: Clipboard content.
- `[clipboard_image]`: Image currently in clipboard.
- `[screen_obj]`: Screenshot of the navigator object.
- `[screen_fg_obj]`: Screenshot of the active foreground window.
- `[screen_full]`: Full screen screenshot.
- `[file_ocr]`: Select image/PDF file for text extraction.
- `[file_read]`: Select document for reading (TXT, Code, PDF).
- `[file_audio]`: Select audio file for analysis (MP3, WAV, OGG).
- `{target_lang}`: Current target language.
- `{source_lang}`: Current source language.
- `{response_lang}`: Current AI response language.
- `{swap_target}`: Fallback language for smart swap translation.
- `{swap_instruction}`: Smart swap translation instruction block.

## 11. Real-World Use Cases (Which feature should I use?)

Vision Assistant Pro is packed with advanced tools. Here are some common scenarios to help you choose the right one:

- **Scenario: You want to understand the complete layout of a complicated window or inaccessible app.**
  *Solution:* Press **O** (Full Screen Vision). The AI will analyze the entire screen and describe exactly where elements, texts, and buttons are positioned.

- **Scenario: You found an image on a webpage or an unlabeled graphic in a document.**
  *Solution:* Move your navigator object to the graphic and press **V** (Object Vision). The AI will describe specifically what that image contains.

- **Scenario: You want to watch a movie or video clip with audio descriptions.**
  *Solution:* Press **Shift + V** on your video and choose **"Generate Audio Description (SRT File)"**. When it finishes, click **"Generate Synced Narration (MP3)"** and select **"Extended AD"**. The add-on will create an audio track that intelligently pauses the movie's dialogue to describe the visual scenes.

- **Scenario: You encountered an app full of "unlabeled buttons".**
  *Solution:* Press **L** to permanently label the specific button using AI. Or, press **Shift + L** to scan and label the entire window at once. If you just want to click something quickly, press **E** (UI Explorer) to get a list of all clickable items.

- **Scenario: You need to bypass an inaccessible CAPTCHA.**
  *Solution:* Press **C** (CAPTCHA Solver). The AI will automatically capture the CAPTCHA, solve it, and inject the answer into the correct field.

- **Scenario: You want to read a long, 50-page PDF document.**
  *Solution:* Press **D** (Document Reader), set your provider to Google Gemini, and enter the page range `1-50`. The add-on will extract the text accurately in the background.

- **Scenario: You are watching a silent video tutorial or animation on your screen.**
  *Solution:* Press **Control + V** to start recording the screen. Let the tutorial play, then press **Control + V** again. The AI will explain exactly what was demonstrated.

- **Scenario: You encounter an unexpected error, API connection failure, or want to diagnose issues with custom local servers.**
  *Solution:* Go to **Settings > Advanced**, check **"Enable dedicated log file"**, and set the **Log Level** to **"Debug"**. Perform the action again, then click **"Open Log File"** to inspect technical details or attach `vision_assistant.log` to a support ticket.

***
**Note:** An active internet connection is required for all AI features. Multi-page documents are processed automatically.

## 12. Support & Community

Stay updated with the latest news, features, and releases:
- **Telegram Channel:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** For bug reports and feature requests.

### Reporting Bugs & Logs
When opening a GitHub issue or asking for support, please include details about your active AI provider, model, and NVDA version. If you are experiencing connection issues or unexpected crashes, enable the dedicated log file in **Settings > Advanced**, recreate the issue, and attach your `vision_assistant.log` file to help us resolve the problem faster.

## 13. Project Supporters

A heartfelt thank you to our community members who support the continuous development and maintenance of this project through their generous financial contributions:

*   **@Alyabani94**
*   **Ali Alamri**
*   **Ilya**
*   **Anonymous Supporter**
*   **leonardo0216**
*   **Sergei Fleytin**
*   **Arne Siebert**

*If you wish to support the project financially and see your name here, you can find the **Donate** option in the NVDA Tools menu (Vision Assistant submenu) or during the setup process after installation.*


---
## Changes for 2026.09.01

*   **History (Control + H)**: The Command Layer now includes a **History** dialog (`Control + H`) that lists your past chats and documents with filters for All, Chats, and Documents. Reopen any chat with its full conversation — attached files are re-attached automatically — or reopen a document and keep reading. Press **Delete** on any item to remove it, or clear everything at once.
*   **Recent Documents in the Reader**: Pressing **D** in the Command Layer now shows your recently read documents first. Pick one to continue from the page you were on — even when the OCR already finished — or press **Open File...** (`Ctrl + O`) to browse as usual.
*   **Push to Talk for Live Assistant**: Take full control of your live conversations! Enable **Push to Talk** in the new Live Assistant settings tab and assign any key — or even a lone modifier like `Left Ctrl` — to talk. Hold the key to speak and release it when you're done, with a short beep on each press and release. A matching toggle also appears right in the Live Assistant window, so you can switch between push-to-talk and open-mic mode without leaving the conversation.
*   **Gemini 2.5 Flash Native Audio**: The Live Assistant now supports Gemini 2.5 Flash's native audio model (`gemini-2.5-flash-native-audio-preview-12-2025`) for low-latency, natural voice conversations. You can switch to it from **Settings → Advanced Model Routing → Live Assistant Model (Gemini only)**, or keep "Auto" to stay on the recommended model.
*   **Settings Backup & Restore**: Added a powerful backup and restore system in the **Advanced** tab! You can now save all of your add-on settings — including API keys, models, custom prompts, and preferences — into a single JSON file, and restore them perfectly at any time, on any machine, or after reinstalling NVDA.
*   **Direct Text & HTML Reading**: The Document Reader can now open plain text (`.txt`) and HTML (`.html`, `.htm`) files directly! It automatically detects the file encoding, strips scripts and formatting clutter, and intelligently splits the content into readable pages — even re-importing its own exported files while preserving page structure — so you can read them instantly with no OCR or AI processing!
*   **Gemini Live TTS for the Document Reader**: The "Generate Audio" button now supports Gemini Live — a high-quality, natural-pace streaming text-to-speech engine! When Gemini is your active provider, you can choose between Standard TTS and Gemini Live right in the reader, and your selection is remembered for next time!
*   **Custom Prompt Shortcuts**: You can now assign a shortcut key to any of your custom prompts right from the Prompt Manager! Give every prompt its own dedicated key or key combination to run it instantly, automatically capturing your current selection or context with zero extra steps!
*   **Chat Message Navigation**: Review any conversation hands-free! Inside any chat window (Direct Chat, document chat, refine, and more), press `Alt + Down` to hear the next message and `Alt + Up` to hear the previous one — with clear "You" / "AI" prefixes and "First message" / "Last message" boundaries announced as you go.
*   **Copy Chat Message (Alt + C)**: While reviewing a conversation with `Alt + Up/Down`, press `Alt + C` to copy the message you are currently on to the clipboard — respecting your Clean Markdown setting — with a spoken confirmation.
*   **Direct Chat System Prompt**: The Direct Chat (`Shift+C`) now has its own editable system prompt — "Direct Chat Instruction" — that sets the assistant's persona and response language for every conversation. You can customize it from the Prompt Manager's Default Prompts tab.
*   **Document Reader Cursor Page Navigation**: Reading multi-page documents just got smoother! In the Document Viewer, when your cursor reaches the last line of a page and you press `Down`, the reader automatically jumps to the next page. Pressing `Up` at the start of a page seamlessly takes you back to the previous one — no more manual page switching while reading!
*   **New Quick Settings Toggles**: Copy AI responses to clipboard, Direct Output (no chat window), Clean Markdown in Chat, and Smart Swap can now be switched on and off instantly from the command layer's Quick Settings!
*   **Live Assistant Settings Tab**: The Live Assistant now has its own dedicated settings tab! The "Live Assistant: Direct Output (No Window)" option moved here from the Connection tab, and the tab appears only when Google Gemini (or a Gemini-compatible Custom provider) is your active provider.

## Changes for 2026.08.06

*   **UI Explorer Labeling**: You can now add labels directly to found elements inside the UI Explorer! A new "Add Label" button has been added, and the interface smartly stays open and preserves focus so you can rapidly label multiple objects without interruption.
*   **Quick Settings Layer Enhancement**: The Vision Assistant layer (`Insert+Shift+V`) is now persistent and highly interactive! You can use `Up/Down` arrows to navigate between quick settings (Provider, Model, AI Response Language, TTS Model) and `Left/Right` arrows to instantly change their values with smart, concise voice feedback. Your selections take effect immediately (including auto-enabling advanced routing when necessary), and the layer stays alive while you configure.
*   **Direct Chat (`Shift+C`)**: Added a new command to the layer! Press `Shift+C` to instantly open a "Direct Chat" window. This provides a clean, text-based conversational interface with the AI right away, without needing an image or document as a starting point.
*   **Flawless Chat History Recall**: Fixed a major bug where pressing `Space` to recall the last result would lose your subsequent chat history. Now, the add-on globally tracks your conversation. If you chat, close the dialog, and press `Space` to recall it, your entire back-and-forth history is perfectly restored! Works for Direct Chat, Vision Analysis, Document Chat, and Translation.
*   **Inline Image Descriptions in OCR**: Added an optional feature to describe images inline during document OCR. You can toggle this setting in the add-on's OCR settings, within the Document Reader options before extraction, and quickly on-the-fly via the Quick Settings layer.
*   **Voice Translation (`Control+T`)**: Added a powerful new feature! Dictate speech and instantly translate and type it using AI based on your configured source and target languages.
*   **Update Downloader Improvements**: The update download dialog now correctly displays download progress in percentages, and a bug where a phantom "Downloading update" message appeared upon canceling the installation has been fixed.
*   **eSpeak-NG Downloader Improvements**: Added percentage progress tracking for eSpeak-NG downloads.
*   **Batch OCR Resilience**: Fixed an issue in batch PDF OCR where the process would halt if the active API key reached its quota midway; it now automatically switches to the next available key and resumes the process.
*   **Visual Captcha Support**: Added robust support for visual captcha solving. It attempts to automatically solve complex image challenges like hCaptcha and reCAPTCHA, significantly enhancing accessibility on challenging web forms.
*   **Audio Transcriber Overhaul**: The Audio Transcriber module has been completely rebuilt and now supports both audio and video files. It features 3 distinct operation modes: "Transcribe (Original Language)", "Transcribe and Translate (Target Language)", and a new powerful "Dub and Translate (Target Language)" option (exclusive to Gemini) that generates a translated audio dub of the original speech.
*   **Optional Page Numbers in Document Reader**: Added a new setting to toggle the inclusion of page numbers and separators in multi-page document outputs. You can easily manage this option from the main settings or toggle it on-the-fly via the Quick Settings layer. This feature applies to both text/HTML file exports and the inline "View Formatted" window, allowing you to read combined documents seamlessly.
*   **Unlimited Gemini Live TTS for Video Descriptions**: You can now select "Gemini Live TTS" as the voice engine when generating Synchronized Audio Narration (MP3) for videos. This utilizes the Gemini Live API to synthesize high-quality audio descriptions without any character limits or length restrictions.
*   **Codebase Modularization**: Refactored the add-on structure from a single file to a multi-file modular architecture for improved maintainability.
*   **Settings UI Redesign**: Completely redesigned the Settings dialog to use a modern, tab-based interface instead of a grouped layout, providing better organization and easier navigation while keeping all existing options.
*   **Global & Dedicated File Logging**: Added an optional global file logging system under the new "Advanced" settings tab. Automatically captures operational events, API traffic, and errors across all add-on modules into a dedicated file (`vision_assistant.log`). Supports configurable log verbosity levels (Debug, Info, Warning, Error), automated retention periods (1 hour to 90 days), and direct log opening or clearing from settings with zero performance impact or NVDA log interference.
*   **Gemini Upload Progress Tracking**: Added real-time percentage progress announcements when uploading large files (video, audio, documents) to the Google Gemini API.

## Changes for 2026.07.15

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
*   **Smart API Quota Management**: Enhanced handling of 429 (Daily Limit) errors by tracking quotas per-model. If a key hits its daily limit on one model, it is intelligently quarantined for that specific model only, leaving the key available for use with other models.

## Changes for 7.0.0

*   **Resuming Unfinished Scans**: Added a resume feature for both the Document Reader and Smart File Actions. If a scan gets interrupted, you can now continue from where it stopped instead of starting over from scratch.
*   **New `[screen_fg_obj]` Variable**: Added a custom prompt variable to capture a screenshot of only the active foreground window rather than the entire screen.
*   **Smart Retries & Key Rotation**: The addon now silently retries up to 5 times on the same key when hitting temporary server overloads (like "high demand" or malformed responses). If the retries fail, it automatically switches to the next API key in your list.
*   **Screen Curtain Detection**: Added a check to prevent taking screenshots when the Screen Curtain is active (whether permanently enabled or toggled temporarily with the hotkey). It will warn you and stop, preventing you from sending black images and wasting API tokens.
*   **Document Reader Tweaks**: The PDF range dialog now automatically pre-selects the default target language from your addon settings. Also improved thread handling to make sure background tasks stop cleanly when the reader is closed.
*   **Native Mistral OCR Integration**: Integrated Mistral's native Document OCR API. Multi-page documents are automatically merged, uploaded, and processed in batches using Mistral's specialized `/v1/ocr` endpoint, while single-page images are processed directly without unnecessary PDF conversions [1].
*   **Dynamic Custom URL Handlers**: Modifying the Custom API URL now instantly clears the cached model list and restores the manual model entry text box. This ensures full compatibility with custom endpoints (such as Cloudflare AI Gateway) that do not support the standard `/v1/models` listing endpoint.
*   **Overhauled AI Operator Input Engine**: Completely rewritten the underlying mouse and keyboard simulation system for the AI Operator. Replaced the legacy `mouse_event` API with the modern Windows `SendInput` API, bringing significantly higher compatibility with modern applications, UAC-protected windows, and high-DPI displays.
*   **Fixed Drag & Drop Operations**: Drag and drop actions in the AI Operator are now fully stable and reliable. The new engine uses natural "easing" curves, precise cursor positioning, optimized timing, and a smart "nudge" technique to ensure that Windows and applications correctly recognize and execute drag-and-drop gestures without failing mid-way.
*   **Multi-Monitor Support**: The AI Operator now fully supports multi-monitor setups. Mouse movements and clicks work correctly across all monitors using the `MOUSEEVENTF_VIRTUALDESK` flag, ensuring accurate positioning regardless of which monitor the target application is on.
*   **Enhanced Keyboard Simulation**: Improved keystroke injection to fully support "Extended Keys" (such as Arrow keys, Home, End, Page Up/Down, Insert, Delete, and F1-F12). This ensures that navigation and shortcut commands sent by the AI Operator work flawlessly across all applications.
*   **HEIC/HEIF Image Support**: Added native support for iPhone photo formats. You can now directly select `.heic` and `.heif` files for AI description, OCR, or Document Reading without prior conversion.

## Changes for 6.5.0

*   **Live Assistant**: Added a real-time voice and screen assistant feature, available exclusively for the Google Gemini provider (or Gemini-compatible custom providers). Includes interactive voice and thinking depth customization directly inside the dialog, with automatic reconnection upon changing settings.
*   **MiniMax AI Provider**: Integrated MiniMax as a peer provider with full multimodal support (chat, vision, OCR), custom TTS using over 300+ dynamic voices, and automatic stripping of reasoning blocks (e.g., `<think>...</think>`) from outputs.
*   **Document Viewer Translation**: Corrected a silent translation failure for non-English NVDA users by ensuring the standard 2-letter language code is sent to Google Translate instead of the localized language name.
*   **PDF Batch Scan Retry**: Implemented a highly optimized, separate, and silent retry logic for PDF document batch scanning to prevent redundant uploads and avoid disruptive error popups during retries.
*   **Document Viewer Status**: Fixed a bug where the plugin's overall status (checked via `I`) remained stuck on "Batch Processing Started" during long document scans.
*   **Resolved Threading Crash**: Fixed a severe `IsMain() failed in wxTimerImpl` thread assertion crash when opening documents from a background thread by transitioning the GUI callback queue to `wx.CallAfter`.

## Changes for 6.1.2

*   **Duplicate Label Pre-Check**: Fixed an issue in single labeling where the duplicate check used old coordinate keys, causing NVDA to make duplicate AI requests for already labeled objects instead of announcing the existing label.
*   **Document Chat for Non-Gemini Providers**: Fixed a strict API key check in Document Chat (`on_ask`) to ensure that users on OpenAI, Groq, or local Custom providers (like Ollama) can successfully chat with documents without being blocked.
*   **Fast Chrome OCR Translation**: Restored the free, keyless translation API for Chrome OCR. Translating extracted text now bypasses Gemini AI, saving API quotas and speeding up the translation process.
*   **CAPTCHA Alphanumeric Filter**: Corrected the filtering logic in the CAPTCHA solver to ensure non-alphanumeric characters are properly cleaned in all situations.
*   **Command Layer Help Update**: Corrected the status announcement shortcut in the help menu from `L` to `I`, and added both labeling commands (`L` and `Shift+L`) to the list.

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
