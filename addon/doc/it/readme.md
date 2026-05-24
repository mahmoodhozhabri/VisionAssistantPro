# Documentazione di Vision Assistant Pro

Vision Assistant Pro è un assistente IA multimodale avanzato per NVDA. Utilizza motori di intelligenza artificiale di alto livello per fornire lettura intelligente dello schermo, traduzione, dettatura vocale e analisi dei documenti.

_Questo componente aggiuntivo è stato rilasciato alla comunità in occasione della Giornata internazionale delle persone con disabilità._

## 1. Configurazione e impostazioni

Andare in **Menu NVDA > Preferenze > Impostazioni > Vision Assistant Pro**.

### 1.1 Impostazioni di connessione
- **Provider:** selezionare il servizio IA preferito. I provider supportati includono **Google Gemini**, **OpenAI**, **Mistral**, **Groq** e **Personalizzato** (server compatibili OpenAI come Ollama o LM Studio).
- **Nota importante:** si consiglia vivamente di utilizzare **Google Gemini** per ottenere le migliori prestazioni e precisione, soprattutto per l’analisi di immagini e file.
- **Chiave API:** obbligatoria. È possibile inserire più chiavi (separate da virgole o nuove righe) per consentire la rotazione automatica.
- **Recupera modelli:** dopo aver inserito la chiave API, premere questo pulsante per scaricare dal provider l’elenco aggiornato dei modelli disponibili.
- **Modello IA:** selezionare il modello principale utilizzato per la chat generale e l’analisi.

### 1.2 Instradamento avanzato dei modelli
*Disponibile per tutti i provider, inclusi Gemini, OpenAI, Groq, Mistral e Personalizzato.*

> **⚠️ Avviso:** queste impostazioni sono destinate esclusivamente agli **utenti avanzati**. Se non si conosce il funzionamento di un determinato modello, lasciare questa opzione **non selezionata**. La scelta di un modello incompatibile per una determinata attività (ad esempio un modello solo testuale per funzioni visive) provocherà errori e impedirà il funzionamento del componente aggiuntivo.

Selezionare **“Instradamento avanzato dei modelli (specifico per attività)”** per sbloccare i controlli dettagliati. Questa funzione consente di scegliere modelli specifici dall’elenco per diverse attività:
- **Modello OCR / Visione:** scegliere un modello specializzato per l’analisi delle immagini.
- **Speech-to-Text (STT):** scegliere un modello specifico per la dettatura.
- **Text-to-Speech (TTS):** scegliere un modello per la generazione dell’audio.
- **Modello operatore IA:** selezionare un modello specifico per attività autonome di controllo del computer.
*Nota: le funzioni non supportate (ad esempio il TTS per Groq) verranno nascoste automaticamente.*

### 1.3 Configurazione avanzata degli endpoint (provider personalizzato)
*Disponibile solo quando è selezionato “Personalizzato”.*

> **⚠️ Avviso:** questa sezione consente la configurazione manuale delle API ed è progettata per **utenti esperti** che utilizzano server locali o proxy. URL o nomi modello errati interromperanno la connettività. Se non si conosce esattamente il significato di questi endpoint, lasciare questa opzione **non selezionata**.

Selezionare **“Configurazione avanzata degli endpoint”** per inserire manualmente i dettagli del server. A differenza dei provider nativi, qui è necessario **digitare** URL e nomi dei modelli specifici:
- **URL elenco modelli:** endpoint utilizzato per recuperare i modelli disponibili.
- **URL endpoint OCR/STT/TTS:** URL completi per servizi specifici (ad esempio `http://localhost:11434/v1/audio/speech`).
- **Modelli personalizzati:** digitare manualmente il nome del modello (ad esempio `llama3:8b`) per ogni attività.

### 1.4 Preferenze generali
- **Motore OCR:** scegliere tra **Chrome (veloce)** per risultati rapidi oppure **IA (avanzato)** per una migliore conservazione del layout.
    - *Nota:* se viene selezionato “IA (avanzato)” mentre il provider attivo è OpenAI o Groq, il componente aggiuntivo instraderà automaticamente l’immagine verso il modello di visione del provider attivo.
- **Voce TTS:** selezionare lo stile vocale preferito. Questo elenco viene aggiornato dinamicamente in base al provider attivo.
- **Creatività (temperatura):** controlla il livello di casualità dell’IA. Valori più bassi sono preferibili per traduzioni e OCR accurati.
- **URL proxy:** configurare questa opzione se i servizi IA sono limitati nella propria area geografica (supporta proxy locali come `127.0.0.1` oppure URL bridge).

## 2. Livello comandi e scorciatoie da tastiera
Per evitare conflitti da tastiera, questo componente aggiuntivo utilizza un **livello comandi**.
1. Premere **NVDA + Shift + V** (tasto principale) per attivare il livello (verrà emesso un segnale acustico).
2. Rilasciare i tasti, quindi premere uno dei seguenti tasti singoli:

| Tasto         | Funzione                    | Descrizione                                                                 |
|---------------|-----------------------------|------------------------------------------------------------------------------|
| **Shift + A** | **Operatore IA**            | **Operazione autonoma:** consente all’IA di eseguire un’attività sullo schermo. |
| **E**         | **Esploratore interfaccia** | **Clic interattivo:** identifica e fa clic sugli elementi dell’interfaccia in qualsiasi applicazione. |
| **T**         | Traduttore intelligente     | Traduce il testo sotto il cursore navigatore o la selezione.                |
| **Shift + T** | Traduttore appunti          | Traduce il contenuto attualmente presente negli appunti.                    |
| **R**         | Rifinitore testo          | Riassume, corregge la grammatica, spiega o esegue **prompt personalizzati**. |
| **V**         | Visione oggetto             | Descrive l’oggetto navigatore corrente.                                     |
| **O**         | Visione schermo intero      | Analizza il layout e il contenuto dell’intero schermo.                      |
| **Shift + V** | Analisi video online        | Analizza video di **YouTube**, **Instagram**, **TikTok** o **Twitter (X)**. |
| **D**         | Lettore documenti           | Lettore avanzato per PDF e immagini con selezione dell’intervallo di pagine. |
| **F**         | **Azione file intelligente**| Riconoscimento contestuale di immagini, PDF o file TIFF selezionati.        |
| **A**         | Trascrizione audio          | Trascrive file MP3, WAV o OGG in testo.                                     |
| **C**         | Risolutore CAPTCHA          | Cattura e risolve CAPTCHA (supporta portali governativi).                   |
| **S**         | Dettatura intelligente      | Converte il parlato in testo. Premere per avviare la registrazione, di nuovo per interrompere e scrivere. |
| **I**         | Segnalazione stato          | Annuncia lo stato corrente (ad esempio “Scansione...”, “Inattivo”).         |
| **L**         | **Etichetta oggetto**       | **Etichettatura semantica IA:** assegna in modo permanente un’etichetta all’elemento o icona attualmente focalizzati. |
| **Shift + L** | **Gestisci/scansiona etichette** | Apre il gestore etichette (se esistono etichette) oppure analizza l’applicazione alla ricerca di elementi senza nome. |
| **U**         | Controllo aggiornamenti     | Controlla manualmente su GitHub la presenza di nuove versioni del componente aggiuntivo. |
| **Spazio**    | Richiama ultimo risultato   | Mostra l’ultima risposta dell’IA in una finestra chat per revisione o domande successive. |
| **H**         | Guida comandi               | Mostra un elenco di tutte le scorciatoie disponibili.                       |

### 2.1 Scorciatoie del lettore documenti (all’interno del visualizzatore)
- **Ctrl + Pagina giù:** passa alla pagina successiva.
- **Ctrl + Pagina su:** passa alla pagina precedente.
- **Alt + A:** apre una finestra chat per porre domande sul documento.
- **Alt + R:** forza una **nuova scansione con IA** utilizzando il provider attivo.
- **Alt + G:** genera e salva un file audio di alta qualità (WAV/MP3). *Nascosto se il provider non supporta il TTS.*
- **Alt + S / Ctrl + S:** salva il testo estratto come file TXT o HTML.

## 3. Prompt personalizzati e variabili

È possibile gestire i prompt in **Impostazioni > Prompt > Gestisci prompt...**.

### Variabili supportate
- `[selection]`: testo attualmente selezionato.
- `[clipboard]`: contenuto degli appunti.
- `[screen_obj]`: schermata dell’oggetto navigatore.
- `[screen_full]`: schermata completa dello schermo.
- `[file_ocr]`: seleziona un file immagine/PDF per l’estrazione del testo.
- `[file_read]`: seleziona un documento da leggere (TXT, codice, PDF).
- `[file_audio]`: seleziona un file audio da analizzare (MP3, WAV, OGG).
***
**Nota:** è necessaria una connessione Internet attiva per tutte le funzioni IA. I documenti multipagina vengono elaborati automaticamente.

## 4. Supporto e comunità

Rimani aggiornato sulle ultime notizie, funzionalità e versioni:
- **Canale Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Segnalazioni GitHub:** per segnalazioni di bug e richieste di nuove funzionalità.

## 5. Sostenitori del progetto

Un sentito ringraziamento ai membri della comunità che supportano lo sviluppo e la manutenzione continui di questo progetto tramite i loro generosi contributi economici:

*   **@Alyabani94**
*   **Ali Alamri**

*Se desideri sostenere economicamente il progetto e vedere il tuo nome qui, puoi trovare l’opzione **Dona** nel menu Strumenti di NVDA (sottomenu Vision Assistant) oppure durante la procedura di configurazione dopo l’installazione.*


---
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
