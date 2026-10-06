# KI Assistent pro Dokumentation

<!-- DOWNLOAD_COUNT_START --> Total Downloads: 75,451 <!-- DOWNLOAD_COUNT_END -->

**KI Assistent pro** ist ein fortschrittlicher, multimodaler KI-Assistent für NVDA. Er nutzt erstklassige KI-Engines, um intelligentes Screenreading, Übersetzungen, Sprachdiktate und Dokumentenanalysen zu ermöglichen.

_Dieses Add-on wurde zu Ehren des Internationalen Tages der Menschen mit Behinderungen für die Community veröffentlicht._

## 1. Einrichtung & Konfiguration

Gehen Sie zu **NVDA-Menü > Optionen > Einstellungen > KI Assistent pro**. Das Einstellungsfenster ist in 9 barrierefreie Reiter unterteilt: **Verbindung**, **Live-Assistent**, **KI-Verhalten**, **Übersetzungssprachen**, **Dokumentenleser**, **Video**, **CAPTCHA**, **Prompts** und **Erweitert**.

### 1.1 Verbindung Reiter

- **Anbieter:** Wählen Sie Ihren bevorzugten KI-Dienst. Unterstützte Anbieter sind **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** und **Benutzerdefiniert** (OpenAI-kompatible Server wie Ollama, LM Studio, Jan.ai oder KoboldCPP).
- **API-Schlüssel:** Geben Sie einzelne oder mehrere API-Schlüssel ein (getrennt durch Kommas oder neue Zeilen), um eine automatische Rotation zu ermöglichen.
- **Modelle abrufen:** Nachdem Sie Ihren API-Schlüssel eingegeben haben, drücken Sie diese Schaltfläche, um die aktuelle Liste der verfügbaren Modelle vom Anbieter herunterzuladen.
- **KI-Modell:** Wählen Sie das Hauptmodell aus, das für den allgemeinen Chat und die Analysen verwendet werden soll.
- **Advanced Model Routing (Task-specific):** Optionally select dedicated models from dropdowns for OCR, STT, TTS, AI Operator, Video, and Live Assistant tasks. For Gemini, models are dynamically categorized by capability without clutter.
- **Einstellungen für benutzerdefinierte Anbieter:** Konfigurieren Sie lokale oder benutzerdefinierte Endpunkte. Enthält **Lokale KI einrichten** (Ein-Klick-Konfiguration für Ollama, LM Studio, Jan.ai oder KoboldCPP) und die **Erweiterte Endpunkt-Konfiguration**.
- **Proxy Configuration:** Full support for tunneling and endpoint redirection across the entire add-on (including the Live Assistant, Ambient Observer, and TTS). Enter your **Proxy URL** and select your **Proxy Mode**:
  - **Auto-detect:** Automatically detects whether the URL is a forward proxy or reverse proxy.
  - **SOCKS5 Proxy:** Forces forward tunneling via SOCKS5 with RFC 1929 username/password authentication and domain name resolution.
  - **HTTP Proxy:** Forces forward tunneling via an HTTP proxy with Basic authentication.
  - **Reverse Proxy:** Direct endpoint replacement for custom AI gateways and self-hosted mirrors (credentials are disabled in this mode).
- **Test Proxy Connection:** A non-blocking button that tests connectivity and measures server latency in milliseconds (spoken via NVDA).
- **Verbindungs- & Ausgabeoptionen:** Konfigurieren Sie Proxy-URL, Update-Prüfung beim Start, Bereinigtes Markdown im Chat, KI-Antworten in die Zwischenablage kopieren und Direkte Ausgabe (Kein Chat-Fenster).
- **Chats im Verlauf speichern:** Behalten Sie Ihre Chat-Gespräche in der Verlaufsliste.

### 1.2 Live-Assistent Reiter

- **Live-Assistent: Direkte Ausgabe (Kein Fenster):** Startet den Live-Assistenten ohne eigenes Konversationsfenster; öffnen Sie dieses später jederzeit über das Kürzel für das letzte Ergebnis (`Leertaste`).
- **Push-to-Talk:** Schaltet den Push-to-Talk-Modus um. Wenn aktiviert, überträgt das Mikrofon Audio nur, solange Sie die zugewiesene Taste gedrückt halten.
- **Push-to-Talk-Taste:** Drücken Sie die gewünschte Tastenkombination zur Aufzeichnung des Kürzels (z. B. `F12` oder `Strg+F12`) – selbst einzelne Modifikatortasten wie `Linke Strg-Taste` werden unterstützt. Halten Sie die Taste zum Sprechen gedrückt und lassen Sie sie los, um zu beenden; ein kurzer Signalton bestätigt jedes Drücken und Loslassen.

_Hinweis: Dieser Reiter wird nur angezeigt, wenn **Google Gemini** (oder ein Gemini-kompatibler benutzerdefinierter Anbieter) als aktiver Anbieter eingestellt ist._

### 1.3 AI Behavior Tab

- **Kreativität (Temperatur):** Steuert die Zufälligkeit und Kreativität der KI (von 0.0 bis 2.0). Niedrigere Werte liefern deterministischere und präzisere Übersetzungs- und OCR-Ergebnisse.

### 1.4 Übersetzungssprachen Reiter

- **Quellsprache:** Wählen Sie Ihre Standard-Eingabesprache.
- **Zielsprache:** Wählen Sie Ihre primäre Übersetzungssprache.
- **KI-Antwortsprache:** Wählen Sie die Sprache für allgemeine KI-Antworten.
- **Smart Swap (Intelligenter Tausch):** Tauscht Quell- und Zielsprache automatisch basierend auf der erkannten Eingabe.

### 1.5 Dokumentenleser Reiter

- **OCR-Engine:** Wählen Sie zwischen **Chrome (Schnell)** für schnelle Ergebnisse oder **KI (Erweitert)** für eine überlegene Beibehaltung des Layouts.
- **OCR-Stapelgröße:** Geben Sie die Seiten pro Anfrage an (auf 0 setzen für Einzelanfragen-Verarbeitung).
- **Bilder inline beschreiben:** Schaltet die Beschreibung von Bildern direkt im Textfluss während der Textextraktion ein oder aus.
- **Seitenzahlen exportieren:** Schaltet Seitenzahlen und Trennlinien bei mehrseitigen Dokumentausgaben ein oder aus.
- **TTS-Stimme:** Wählen Sie Ihren bevorzugten Stimmenstil für die Audioerzeugung.
- **Dokumente im Verlauf speichern:** Behalten Sie geöffnete Dokumente in der Verlaufsliste; zwischengespeicherte OCR-Texte und Wiederaufnahmedaten bleiben ohnehin gespeichert.

### 1.6 Video Reiter

- **Video-Segmentgröße:** Dauer der Abschnitte in Minuten für die Erstellung von Audiobeschreibungen (auf 0 setzen, um die gesamte Datei auf einmal zu verarbeiten).
- **Charakterliste hinzufügen:** Option, das Charakter-Wörterbuch als ersten Untertiteleintrag einzufügen.
- **KI-Haftungsausschluss hinzufügen:** Option, einen Hinweis auf KI-Generierung am Anfang von SRT-Untertiteln einzufügen.
- **Charakter-Wörterbuch & Serienverwaltung:** Erstellen, bearbeiten, importieren und verwalten Sie Charakternamen, physische Beschreibungen und Rollen pro Serie – die KI gleicht erkannte Charaktere automatisch mit Ihrem Wörterbuch ab und fügt im Laufe neuer Episoden weitere hinzu. Ihre manuellen Notizen genießen stets Vorrang vor KI-Aktualisierungen, während physische Beschreibungen über alle Episoden hinweg aktuell bleiben.

### 1.7 CAPTCHA Reiter

- **Visuellen CAPTCHA-Löser aktivieren:** Schaltet das automatische Lösen visueller Aufgaben (hCaptcha, reCAPTCHA) ein oder aus.
- **Text-CAPTCHA-Methode:** Wählen Sie zwischen der Erfassung des **Navigator-Objekts** oder des **Vollbilds**.

### 1.8 Prompts Reiter

- **System-Prompt für Direkten Chat:** Der Direkte Chat (`Umschalt+C`) besitzt nun einen eigenen editierbaren System-Prompt („Direct Chat Instruction“), um Persönlichkeit und Ausgabesprache festzulegen.
- **Eigene Prompt-Tastenkombinationen:** Weisen Sie jedem benutzerdefinierten Prompt direkt im Prompt-Manager ein eigenes Tastaturkürzel zu. Drücken Sie die Tasten zur Aufnahme – Einzeltasten funktionieren innerhalb der Befehlsebene (und global als `NVDA + Umschalt + Taste`), Tastenkombinationen wie `Strg + Umschalt + 1` funktionieren eigenständig global.
- **Per-Prompt Feedback Behavior:** Choose how each prompt outputs its result individually (Global setting, Copy to clipboard, Direct Output / NVDA message, Copy to clipboard + Direct Output, or Chat window).

### 1.9 Erweitert Reiter & Globales Logging

Navigieren Sie zum Reiter **Erweitert**, um das globale Logging des Add-ons zu konfigurieren:

- **Dedizierte Log-Datei aktivieren:** Schaltet die Protokollierung aller betrieblichen Ereignisse, API-Anfragen und Fehler über alle Module hinweg in eine separate Datei (`vision_assistant.log`) ein.
- **Log-Level:** Wählen Sie die Detailtiefe zwischen **Debug (Alle Details)**, **Info (General Information)**, **Warning (Nur Warnungen)** und **Error (Nur Fehler)**.
- **Logs aufbewahren für:** Legen Sie automatische Aufbewahrungsfristen fest, um ältere Log-Einträge automatisch zu bereinigen (von 1 Stunde bis 90 Tage).
- **Log-Verwaltung:** Nutzen Sie **Log-Datei öffnen**, **Log-Ordner öffnen** oder **Log-Datei löschen**, um Protokolldaten direkt zu überprüfen oder zu bereinigen, ohne NVDA neu zu starten oder reguläre NVDA-Protokolle zu beeinträchtigen.
- **Einheitliches Datenverzeichnis:** Alle Datendateien des Add-ons (Verlauf, Serien, Beschriftungen, OCR-Fortschritte, Caches und Logs) werden in einem einzigen `VisionAssistant`-Ordner innerhalb Ihres NVDA-Konfigurationsverzeichnisses gespeichert – das hält Ordnung und macht manuelle Backups zum Kinderspiel.

### 1.10 Einstellungen sichern & wiederherstellen

Der Reiter **Erweitert** enthält zudem einen Bereich für **Sichern und Wiederherstellen**:

- **Sichern:** Speichert Ihre Konfiguration in einer einzelnen JSON-Datei. Beim Klick wählen Sie den Umfang: **Alles** (Einstellungen, benutzerdefinierte Beschriftungen, OCR-Fortschritte und Verlauf) oder **Nur Einstellungen**.
- **Wiederherstellen:** Lädt ein zuvor gespeichertes Backup, um Ihre Einstellungen und Daten jederzeit, auf jedem System oder nach einer NVDA-Neuinstallation wiederherzustellen. Sie werden vorab um Bestätigung gebeten, da das Wiederherstellen alle aktuellen Einstellungen und Daten ersetzt.

## 2. Gemini-API-Schlüsselmanager

Creating a Gemini API key on **aistudio.google.com** used to be the hardest step of the add-on. With a screen reader the pages were confusing, and some people simply could not create a key at all. The **Gemini API Key Manager** solves that problem. Press **G** in the Command Layer, or open **NVDA Menu > Preferences > Settings > Vision Assistant > Connection** and press **Get a Gemini API Key...**.

- **Signing in:** When you open the manager, your default browser opens directly with Google's secure sign-in page. Sign in with your Google account — no external tools, SDKs, or command-line setups are required. The account you are signed in with is always shown on the **Sign Out** button.
- **Creating a key:** After signing in, you can create a key immediately with **New Project and Key** without any prior setup. If you already have existing projects, they appear in a simple list where you can select one and press **Create Key for Selected Project**.
- **What happens next:** The new key is copied to the clipboard straight away, saved inside the add-on for later, and you are asked once whether to add it to the add-on's key list. That is all you need — no web pages to hunt through.
- **Working with your keys:** **Copy Key for Selected Project** copies the key of the project you have selected, **Copy Last Created Key** copies the key you created a moment ago, and **Export Saved Keys to CSV...** saves everything you have created to a file.
- **Deleting a key:** **Delete a Key...** shows the keys that exist on the selected project, asks you which one to remove, and confirms before deleting. Deleting a key also removes it from the add-on's key list, so no broken key is ever left in the rotation. Keys created outside the add-on can be deleted too, as long as your account has permission on that project.
- **Signing out:** **Sign Out** removes the stored sign-in information from your computer, so you can switch to another account whenever you like.

## 3. Befehlsebene & Tastenkombinationen

Um Tastaturkonflikte zu vermeiden, verwendet dieses Add-on eine **Befehlsebene**.

1. Drücken Sie **NVDA + Umschalt + V** (Haupttaste), um die Ebene zu aktivieren (Sie hören einen Signalton).
2. Lassen Sie die Tasten los und drücken Sie dann eine der folgenden Einzeltasten:

| Key                                                                                                                                                                                                                              | Funktion                                                                                                                                                                                                                                                                                                                              | Beschreibung                                                                                                                                                                                                                                                                                          |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Umschalt + A**                                                                                                                                                                                                                 | **KI-Operator**                                                                                                                                                                                                                                                                                                                       | **Autonome Steuerung:** Weisen Sie die KI an, eine Aufgabe auf Ihrem Bildschirm auszuführen. Erneutes Drücken bricht die Aktion sofort ab.                                                                                                            |
| **Szenario: Sie haben ein Bild auf einer Webseite oder eine unbeschriftete Grafik in einem Dokument gefunden.**                                                                                  | **UI Explorer**                                                                                                                                                                                                                                                                                                                       | \|&#xA;\| **E** \| **UI-Explorer** \| **Interaktiver Klick:** Identifiziert und klickt auf UI-Elemente in jeder Anwendung.                                                                                                                                            |
| **Szenario: Sie stoßen auf unerwartete Fehler, API-Verbindungsabbrüche oder möchten lokale Server analysieren.**                                                                                 | \|&#xA;\| **T** \| Intelligenter Übersetzer \| Übersetzt Text unter dem Navigator-Objekt oder der Markierung.                                                                                                                                                                                                         | Translates text under navigator cursor or selection.                                                                                                                                                                                                                                  |
| \|&#xA;\| **Strg + T** \| Sprach-Übersetzung \| Transkribiert, übersetzt und tippt das Ergebnis basierend auf Ihren Spracheinstellungen.                                                                         | Übersetzung                                                                                                                                                                                                                                                                                                                           | Translates content currently in the clipboard.                                                                                                                                                                                                                                        |
| **Szenario: Sie möchten ein langes, 50-seitiges PDF-Dokument lesen.**                                                                                                                            | Text Refiner                                                                                                                                                                                                                                                                                                                          | \|&#xA;\| **R** \| Text-Optimierer \| Zusammenfassen, Grammatik korrigieren, Erklären oder **Eigene Prompts** ausführen.                                                                                                                                                              |
| Übersetzt von **BFW Würzburg** im Rahmen des Projekts "NVDA Nachhaltig"                                                                                                                                                          | Object Vision                                                                                                                                                                                                                                                                                                                         | \|&#xA;\| **V** \| Objekt-Vision \| Beschreibt das aktuelle Navigator-Objekt.                                                                                                                                                                                                         |
| \|                                                                                                                                                                                                                               | KI Assistent pro enthält einen hochoptimierten Dokumentenleser, der für mehrseitige PDFs, komplexe Bilder und sogar iPhone-HEIC-Formate entwickelt wurde.                                                                                                                                                             | \|&#xA;\| **O** \| Vollbild-Vision \| Analysiert das gesamte Bildschirmlayout und den Inhalt.                                                                                                                                                                                         |
| **Visuelle CAPTCHA-Unterstützung:** Unterstützung für das automatische Lösen komplexer visueller Aufgaben wie hCaptcha und reCAPTCHA hinzugefügt.                                                | Video Analysis                                                                                                                                                                                                                                                                                                                        | \|&#xA;\| **Umschalt + V** \| Videoanalyse \| Analysiert lokale Videodateien oder Online-Videos von **YouTube**, **Instagram**, **TikTok** oder **Twitter (X)**.                                                                                                   |
| \|&#xA;\| **Alt + M** \| Routing-Prüfung \| Meldet die aktuell im erweiterten Modell-Routing ausgewählten KI-Modelle.                                                                                            | Local Video Recording                                                                                                                                                                                                                                                                                                                 | \|&#xA;\| **Strg + V** \| Lokale Videoaufnahme \| Nimmt ein lautloses Video Ihres Bildschirms auf und analysiert die Aktionen und das Layout.                                                                                                                                         |
| **Szenario: Sie sehen sich eine stumme Videoanleitung oder Animation auf Ihrem Bildschirm an.**                                                                                                  | Document Reader                                                                                                                                                                                                                                                                                                                       | \|&#xA;\| **D** \| Dokumentenleser \| Fortgeschrittener Leser für PDF, Bilder und einfache Text-/HTML-Dateien mit Seitenbereichsauswahl.                                                                                                                                              |
| Wie es funktioniert                                                                                                                                                                                                              | **Smart File Action**                                                                                                                                                                                                                                                                                                                 | \|&#xA;\| **F** \| **Smarte Datei-Aktion** \| Kontextabhängige Erkennung aus ausgewählten Bild-, PDF- oder TIFF-Dateien.                                                                                                                                                              |
| **Optionale Seitenzahlen im Dokumentenleser:** Neue Einstellung zum Ein- oder Ausblenden von Seitenzahlen und Trennlinien in exportierten Texten/HTML-Dateien sowie in der formatierten Ansicht. | Media Transcription & Dubbing                                                                                                                                                                                                                                                                                     | \|&#xA;\| **M** \| Medien-Transkription & Synchronisation \| Transkribiert oder synchronisiert Audio-/Videodateien (MP3, WAV, MP4 usw.) in Ihre Zielsprache.                                                                   |
| **C**                                                                                                                                                                                                                            | CAPTCHA Solver                                                                                                                                                                                                                                                                                                                        | \|&#xA;\| **C** \| CAPTCHA-Löser \| Erfasst und löst CAPTCHAs.                                                                                                                                                                                                                        |
| **Sprach-Übersetzung (`Strg+T`):** Neues Feature zum Diktieren von Sprache, die mittels KI sofort übersetzt und direkt an der Cursorposition eingefügt wird.                  | Direct Chat                                                                                                                                                                                                                                                                                                                           | Opens a direct text-based chat interface with the AI.                                                                                                                                                                                                                                 |
| **Szenario: Sie müssen ein unzugängliches CAPTCHA umgehen.**                                                                                                                                     | Smart Dictation                                                                                                                                                                                                                                                                                                                       | \|&#xA;\| **S** \| Intelligentes Diktat \| Wandelt Sprache in Text um. Drücken zum Starten, erneut drücken zum Stoppen/Einfügen.                                                                                                                                      |
| \|&#xA;\| **Umschalt + T** \| Zwischenablage-Übersetzer \| Übersetzt den aktuellen Inhalt der Zwischenablage.                                                                                                    | **Überarbeitung der Audio-Transkription:** Das Modul unterstützt nun Audio- und Videodateien und bietet 3 Modi: Transkribieren, Transkribieren & Übersetzen sowie eine neue Sprach-Synchronfassung ("Dub and Translate", exklusiv für Gemini). | Transcribes, translates, and types the result based on your language settings.                                                                                                                                                                                                        |
| **Szenario: Sie stoßen auf eine App voller „unbenannter Schaltflächen“.**                                                                                                                        | **Online-Videoanalyse:** Unterstützung für **Twitter (X)** Videos hinzugefügt sowie URL-Erkennung verbessert.                                                                                                                                                                      | \|&#xA;\| **Strg + L** \| **Live-Assistent** \| **Echtzeit-Copilot (nur Gemini):** Startet oder beendet ein Live-Sprach- und Bildschirmgespräch mit dem KI-Assistenten.                                                                            |
| **Strg+A**                                                                                                                                                                                                                       | **Live-Operator**                                                                                                                                                                                                                                                                                                                     | **Autonome Computersteuerung (nur Gemini):** Startet oder beendet eine Live-Operatorsitzung, um Bildschirm und Aktionen an die KI zu delegieren.                                                                                                   |
| **G**                                                                                                                                                                                                                            | **Gemini-API-Schlüsselmanager**                                                                                                                                                                                                                                                                                                       | **Erstellen Sie Ihren API-Schlüssel ohne Web (nur Gemini):** Öffnet den Manager, der die Anforderungen Ihres Computers einrichtet, den Browser zur Anmeldung öffnet und einen Schlüssel für das ausgewählte Projekt erstellt, kopiert oder löscht. |
| **I**                                                                                                                                                                                                                            | Statusbericht                                                                                                                                                                                                                                                                                                                         | Kündigt den aktuellen Fortschritt an (z. B. „Scannen...“, „Leerlauf“).                                                                                                             |
| **L**                                                                                                                                                                                                                            | **Objekt beschriften**                                                                                                                                                                                                                                                                                                                | **Semantische KI-Beschriftung:** Beschriftet das aktuell fokussierte Navigator-Objekt oder Symbol dauerhaft.                                                                                                                                                          |
| **Umschalt + L**                                                                                                                                                                                                                 | **Beschriftungen verwalten/scannen**                                                                                                                                                                                                                                                                                                  | Öffnet den Beschriftungs-Manager (falls vorhanden) oder scannt die App nach unbeschrifteten Elementen.                                                                                                                                                             |
| **U**                                                                                                                                                                                                                            | Nach Updates suchen                                                                                                                                                                                                                                                                                                                   | Sucht auf GitHub manuell nach der neuesten Version des Add-ons.                                                                                                                                                                                                                       |
| **Leertaste**                                                                                                                                                                                                                    | Letztes Ergebnis abrufen                                                                                                                                                                                                                                                                                                              | Zeigt die letzte KI-Antwort in einem Chat-Dialog zur Überprüfung oder Weiterverfolgung an.                                                                                                                                                                                            |
| **H**                                                                                                                                                                                                                            | Befehlshilfe                                                                                                                                                                                                                                                                                                                          | Zeigt eine Liste aller verfügbaren Tastenkombinationen an.                                                                                                                                                                                                                            |
| **Strg + H**                                                                                                                                                                                                                     | **Verlauf**                                                                                                                                                                                                                                                                                                                           | Öffnet das Verlaufsdialogfeld, in dem Ihre vergangenen Chats und Dokumente mit Typfiltern und Optionen zum Löschen aufgelistet sind.                                                                                                                                                  |
| **Alt + S**                                                                                                                                                                                                                      | Einstellungen                                                                                                                                                                                                                                                                                                                         | Öffnet das Dialogfeld „Einstellungen von Vision Assistant Pro“.                                                                                                                                                                                                                       |
| **Alt + Q**                                                                                                                                                                                                                      | Bericht über Schlüssel mit erschöpftem Kontingent                                                                                                                                                                                                                                                                                     | Meldet die Anzahl der Gemini-API-Schlüssel, die ihr Tageskontingent überschritten haben, welche Modelle betroffen sind und deren Zurücksetzungszeit.                                                                                                                                  |
| **Alt + M**                                                                                                                                                                                                                      | Routing-Audit                                                                                                                                                                                                                                                                                                                         | Meldet die KI-Modelle, die derzeit im erweiterten Routing für spezielle Aufgaben ausgewählt sind (überspringt Standardeinstellungen).                                                                                                                              |
| **Auf / Ab**                                                                                                                                                                                                                     | Schnelleinstellungs-Navigation                                                                                                                                                                                                                                                                                                        | Navigiert zwischen Schnelleinstellungs-Kategorien (Anbieter, Modell, Ausgabe)... in der Befehlsebene.                                                                                                              |
| **Links / Rechts**                                                                                                                                                                                                               | Change Quick Setting                                                                                                                                                                                                                                                                                                                  | \|&#xA;\| **Pfeil links / rechts** \| Schnelleinstellung ändern \| Ändert den Wert der aktuell ausgewählten Schnelleinstellung.                                                                                                                                                       |

## 4. Chat & Verlauf

Chat-Fenster und der Verlaufsdialog greifen nahtlos über alle Funktionen hinweg ineinander, sodass Sie Konversationen nachlesen und jederzeit dort weitermachen können, wo Sie aufgehört haben.

### 3.1 Tastenkombinationen für das Chatfenster

Wenn ein Chat-Fenster geöffnet ist (Direkter Chat, Dokumenten-Chat, Text-Optimierer usw.), können Sie das Gespräch mit folgenden Tasten prüfen:

- **Alt + Pfeil runter:** Liest die nächste Nachricht vor.
- **Alt + Pfeil hoch:** Liest die vorherige Nachricht vor.
- **Alt + C:** Kopiert die aktuell ausgewählte Nachricht in die Zwischenablage.

### 3.2 Verlauf (Strg + H)

Drücken Sie **Strg + H** in der Befehlsebene, um den **Verlauf** Ihrer bisherigen Chats und Dokumente zu öffnen, filterbar nach Typ (Alle / Chats / Dokumente). Öffnen Sie einen Chat, um die Konversation fortzusetzen – einschließlich angehängter Dateien, die automatisch erneut verknüpft werden – oder öffnen Sie ein Dokument zum Weiterlesen. Drücken Sie **Entf** auf einem Eintrag, um ihn zu entfernen, oder **Alle löschen**, um die Liste zu leeren. Bei Dokumenten fragt das System beim Löschen, ob nur der Verlaufseintrag entfernt oder auch der zwischengespeicherte OCR-Text bereinigt werden soll, damit beim nächsten Öffnen komplett frisch gescannt wird – inklusive einer Option **Nicht mehr fragen**, um Ihre Wahl zu speichern.

You can also choose what the list remembers. Sie können auch festlegen, was die Liste speichert: **Chats im Verlauf speichern** (Reiter Verbindung) und **Dokumente im Verlauf speichern** (Reiter Dokumentenleser) sind standardmäßig aktiviert und können beide über die Schnelleinstellungen umgeschaltet werden. Die Dokumentenoption betrifft nur den Verlaufseintrag – zwischengespeicherte OCR-Texte und Wiederaufnahmedaten bleiben stets erhalten.

## 5. KI-Operator – Autonome Computersteuerung

Der **KI-Operator** macht aus KI Assistent pro von einem passiven Leser einen aktiven Assistenten, der in Ihrem Namen mit Ihrem Computer interagieren kann. Sie können ihn bitten, den Bildschirm zu beschreiben, Fragen zu dem zu beantworten, was er sieht, oder sogar die Kontrolle zu übernehmen – Knöpfe anklicken, Elemente ziehen, Text tippen und durch Anwendungen navigieren, indem Sie ganz normale Alltagssprache verwenden.

Der größte Vorteil? Es funktioniert perfekt in absolut unzugänglicher Software. Wenn Sie in einer benutzerdefinierten Anwendung, einer Remotedesktop-Verbindung oder auf einer Website feststecken, bei der Ihr Screenreader völlig stumm bleibt, stört das den Operator nicht. Da er den Bildschirm visuell „sieht“, kann er Elemente finden, lesen und mit ihnen interagieren, die keinerlei Barrierefreiheits-Labels besitzen.

### 4.1 So funktioniert es

1. Drücken Sie **NVDA + Umschalt + V** und dann **Umschalt + A** (oder nutzen Sie die direkte Tastenkombination), um den KI-Operator-Dialog zu öffnen.
2. Tippen Sie in verständlicher Sprache ein, was Sie tun möchten (z. B. „Klicke auf die Schaltfläche Speichern“, „Was sagt die Fehlermeldung?“ oder „Benenne die Datei in endgueltig.pdf um“).
3. Die KI analysiert Ihren Bildschirm, identifiziert die relevanten Elemente und führt die Aktion aus oder liefert die Antwort. Wenn eine Aufgabe mehrere Schritte erfordert, arbeitet der Operator so lange weiter, bis sie abgeschlossen ist.
4. Drücken Sie jederzeit erneut **Umschalt + A**, um eine laufende Aktion sofort abzubrechen.

### 4.2 Unterstützte Aktionen

Der Operator versteht eine Vielzahl von Befehlen:

- **Beschreiben & Antworten:** „Beschreibe das Bildschirmlayout“ oder „Was sagt die Fehlermeldung?“
- **Klicken:** „Klicke auf die Schaltfläche Speichern“
- **Rechtsklick:** „Mache einen Rechtsklick auf die Datei“
- **Doppelklick:** „Doppelklicke auf das Dokument“
- **Ziehen & Ablegen (Drag & Drop):** „Ziehe das Dokument in den Archiv-Ordner“
- **Tippen:** „Tippe 'Hallo Welt' in das Suchfeld“
- **Scrollen:** „Scrolle dreimal nach unten“
- **Tastendruck:** „Drücke Enter“, „Drücke Tab“, „Drücke Escape“
- **Mehrschrittige Aufgaben:** „Öffne den Datei-Explorer, suche den Bericht und benenne ihn in endgueltig.pdf um“

### 4.3 Wichtige Hinweise

- **⚠️ Warnung zur API-Nutzung:** Da der Operator genau „sehen“ muss, was auf dem Bildschirm passiert, um präzise zu sein, sendet er bei jedem Schritt einen hochauflösenden Screenshot. Eine häufige Nutzung verbraucht Ihr API-Kontingent viel schneller als standardmäßige textbasierte Aufgaben.
- **Administrator-Anwendungen:** Wenn NVDA nicht mit Administratorrechten ausgeführt wird, kann der Operator möglicherweise nicht mit Fenstern interagieren, die erhöhte Rechte erfordern. Dies ist eine Sicherheitsbeschränkung von Windows, kein Fehler im Add-on.
- **Best Practices:** Um die besten Ergebnisse zu erzielen, geben Sie klare und spezifische Befehle. „Klicke auf die blaue Senden-Schaltfläche unten im Formular“ funktioniert fast immer besser als nur „Klicke auf die Schaltfläche“.

### 4.4 Live-Operator (Strg+A)

Der Live-Assistent macht KI Assistent pro zu einem interaktiven Echtzeit-Copiloten.
_(Hinweis: Diese Funktion ist exklusiv für Google Gemini und Gemini-kompatible benutzerdefinierte Anbieter verfügbar)_.

- **Globales & Dediziertes File-Logging:** Neues optionales Protokollierungssystem im Reiter "Erweitert" zur Aufzeichnung aller Aktionen in eine separate Datei (`vision_assistant.log`) mit konfigurierbaren Log-Levels und Aufbewahrungsfristen.
- **How it works:** Ask in plain language, for example "open Chrome and search for a website" or "rename this file to final". The operator looks at the screen, carries out the steps one by one, and keeps working through multi-step requests until the task is done.
- **Announcements:** Every step is spoken in the Live Assistant's own voice, and it tells you when the task is finished, or why it could not be done.
- **CAPTCHA:** If a CAPTCHA appears, the operator tries your built-in **CAPTCHA solver** first; if it cannot solve it, it asks you to complete the accessible challenge yourself.
- **Neugestaltung der Einstellungen:** Das Einstellungsfenster wurde auf ein modernes Layout mit Reitern umgestellt.
- **Settings:** The operator's own instruction can be edited in the Prompt Manager (section **Live**, **Live Operator Instruction**). The **Live Direct Output (No Window)** switch is available in Quick Settings as well.

## 6. Videoanalyse & Audiobeschreibung

> **Hinweis:** Die Funktionen zur Videoanalyse und Audiobeschreibung werden ausschließlich durch den Anbieter **Google Gemini** unterstützt. Stellen Sie sicher, dass Ihr aktiver Anbieter in den Add-on-Einstellungen auf Google Gemini eingestellt ist.

KI Assistent pro führt leistungsstarke Videoverarbeitungsfunktionen ein, die speziell für blinde und sehbehinderte Benutzer entwickelt wurden. Es kann sowohl Online-Videos als auch lokale Bildschirmaufnahmen analysieren, um hochdetaillierte visuelle Beschreibungen zu liefern und professionelle Audiobeschreibungs-Skripte (SRT) zu erstellen.

### 5.1 Lokale Bildschirmaufnahme (Strg + V)

Wenn Sie auf ein stummes Video, eine Animation oder eine Anleitung auf Ihrem Bildschirm stoßen, können Sie diese direkt aufnehmen:

1. Drücken Sie **NVDA + Umschalt + V**, um die Befehlsebene zu aktivieren, und drücken Sie dann **Strg + V**.
2. Das Add-on nimmt Ihren Bildschirm geräuschlos im Hintergrund auf.
3. Drücken Sie erneut **Strg + V**, um die Aufnahme zu stoppen.
4. Die KI analysiert den aufgenommenen Videoabschnitt und liefert eine hochdetaillierte Beschreibung der Szene, der Charaktere und der Aktionen.

### 5.2 Videoanalyse (Umschalt + V)

Sie können sowohl lokale Videodateien als auch Online-Videos analysieren. Wählen Sie einfach eine lokale Datei im Explorer aus oder kopieren Sie einen Videolink in Ihre Zwischenablage. Sie können auch überall **Umschalt + V** drücken (z. B. im Mediaplayer), um einen Dialog zum Auswählen einer Datei oder Einfügen einer URL aufzurufen.

- **Unterstützte Online-Plattformen:** YouTube, Instagram, TikTok und Twitter (X).
- Die KI erkennt die Datei bzw. URL automatisch, verarbeitet das Video und liefert eine umfassende visuelle Beschreibung und Audio-Zusammenfassung.
- **48-Stunden-Zwischenspeicherung von Videodateien:** Zu Gemini hochgeladene Videos werden 48 Stunden lang zwischengespeichert! Sie können SRT- oder MP3-Ausgaben für dasselbe Video ohne erneuten Upload neu generieren – selbst nach einem Neustart von NVDA. Der Cache erkennt den verwendeten API-Schlüssel und wird bei einem Schlüsselwechsel automatisch ungültig.

### 5.3 Erstellung von Audiobeschreibungen (SRT)

Für ein strukturierteres Erlebnis kann das Add-on professionelle Audiobeschreibungs-Skripte im Standard-SubRip-Format (SRT) generieren.

- **Smarte Pausen-Anpassung (Gap-Timing):** Die KI hört auf die Tonspur und verankert ihre Beschreibungen gezielt in natürlichen Sprechpausen, um Überschneidungen mit Dialogen intelligent zu minimieren.
- **Charakter-Verfolgung:** Die Engine führt vorab eine Analyse durch, um Personen anhand unveränderlicher Gesichtsmerkmale zu erfassen. Sie baut ein globales Wörterbuch auf, um Charaktere über Szenen hinweg fehlerfrei zu benennen. Zudem wird der **erste Auftritt** jedes Charakters verfolgt: Seine optische Erscheinung wird nur einmalig beim ersten Auftauchen beschrieben – spätere Szenen nutzen nur noch den etablierten Namen, was die Erzählung flüssig und natürlich hält.
- **Wortgetreues Text-OCR:** Jeder Text auf dem Bildschirm (Schilder, Telefone, Abspanne) wird strikt wortgetreu zitiert.
- **Nutzung:** Legen Sie die generierte `.srt`-Datei einfach in denselben Ordner wie Ihre Videodatei mit exakt demselben Dateinamen. Konfigurieren Sie Ihren Mediaplayer (z. B. VLC oder PotPlayer) so, dass der Untertiteltext während der Wiedergabe direkt an Ihren Screenreader oder Ihre TTS-Engine weitergeleitet wird. Konfigurieren Sie dann Ihren Media-Player (z. B. VLC oder PotPlayer) so, dass der Untertiteltext während der Wiedergabe direkt an Ihren Screenreader oder Ihre TTS-Engine weitergeleitet wird.
- **Verbesserter Speicher-Workflow:** Beim Speichern von SRT- oder MP3-Dateien öffnet sich der Dateidialog nun standardmäßig direkt im Ordner des Quellvideos – unabhängig davon, ob das Video über den Auswahldialog oder per Umschalt+V aus dem Explorer geöffnet wurde.

### 5.4 Synchronisierte Audiosprachausgabe (MP3-Export)

Das Add-on geht über die Erstellung textbasierter SRT-Dateien hinaus und fungiert als vollständiges Werkzeug zur Erstellung von Audiobeschreibungen, indem es die Beschreibungen in Sprache synthetisiert und mit dem Video abmischt. Sie können nun **Gemini Live TTS** als Sprach-Engine wählen, um unbegrenzte und hochrealistische Beschreibungen über die Gemini Live API zu erzeugen. Beim Generieren einer MP3-Datei für lokale Videos stehen Ihnen mehrere Mischmodi zur Verfügung:

- **Standard-AD (Ton mischen):** Die Sprachbeschreibung wird direkt über den Originalton des Videos gelegt. Sie werden gefragt, ob Sie **Audio-Ducking** aktivieren möchten (wodurch die Hintergrundlautstärke während der Beschreibungen abgesenkt wird), um eine klare Verständlichkeit zu gewährleisten.
- **KI-gestützte Stille-Erkennung (Silero VAD):** Die erweiterte Audiobeschreibung (Extended AD) nutzt jetzt das neuronale Modell Silero VAD für eine hochpräzise Stille-Erkennung – und unterscheidet natürliche Dialogpausen zuverlässig von Musik und Hintergrundgeräuschen. Das Modell wird bei der ersten Nutzung automatisch heruntergeladen (mit Ihrer Zustimmung), genau wie ffmpeg und eSpeak.
- **YouTube-Videos:** Bei YouTube-Quellen (die nicht lokal heruntergeladen werden) enthält der MP3-Export ausschließlich die synchronisierte KI-Stimme ohne den Hintergrundton des Videos.

## 7. Medientranskription & Synchronisation (M)

Das Modul zur Audio-Transkription unterstützt sowohl Audio- als auch Videodateien (MP3, WAV, MP4, MKV usw.). Drücken Sie **M** in der Befehlsebene, um eine Mediendatei auszuwählen und eine von 3 Betriebsarten zu wählen:

1. **Transkribieren (Originalsprache):** Transkribiert die gesprochene Sprache präzise in ihrer Originalsprache.
2. **Transkribieren und Übersetzen (Zielsprache):** Transkribiert die Sprache und übersetzt sie in Ihre konfigurierte Zielsprache.
3. **Synchronisieren und Übersetzen (Zielsprache) _(nur Gemini)_:** Eine leistungsstarke Funktion, die Sprache transkribiert, übersetzt und mit der TTS-Engine des Add-ons eine neu eingesprochene Audio-Synchronfassung erzeugt.

## 8) Erweiterter Dokumenten- & Bildleser

Der **Dokumentenleser** verwandelt Dokumente in sauberen, lesbaren Text – damit Sie von eingescannten Büchern bis hin zu Fotostapeln alles lesen, übersetzen und anhören können. Er verarbeitet mehrseitige PDFs, komplexe Bilder, iPhone-HEIC-Formate und sogar reine Text- (`.txt`) sowie HTML-Dateien (`.html`, `.htm`), die ganz ohne OCR- oder KI-Verarbeitung sofort geöffnet werden. Wenn Sie mehrere Dateien auf einmal auswählen, werden diese in Seitenreihenfolge zu einem einzigen Dokument zusammengefügt. Drei OCR-Engines stehen bereit – **Chrome (Schnell)**, **KI (Erweitert)** für hervorragenden Layouterhalt und **Keine (Textschicht extrahieren)** für durchsuchbare PDFs – wählbar unter Einstellungen → Dokumentenleser.

### Wie es funktioniert

1. Drücken Sie **NVDA + Umschalt + V** und dann **D**, um den Dokumentenleser zu öffnen – oder markieren Sie vorher eine Datei im Explorer und drücken Sie **D** / **F**, um den Dateidialog direkt zu überspringen.
2. Wählen Sie eine oder mehrere PDFs bzw. Bilddateien. Das Add-on scannt sie und sagt die Gesamtseitenzahl an.
3. Im Dialog **Optionen** wählen Sie den Seitenbereich (Von/Bis). Sie können auch **Ausgabe übersetzen** aktivieren und die Zielsprache wählen, oder **Bilder inline während OCR beschreiben** zuschalten.
4. Die Textextraktion startet im Hintergrund in Stapeln. Sie können das Fenster jederzeit schließen und später fortfahren – es geht nichts verloren.
5. Sobald Seiten bereitstehen, lesen Sie diese im Viewer: blättern Sie zwischen Seiten, springen Sie zu bestimmten Seiten, stellen Sie der KI Fragen, speichern Sie den Text oder erzeugen Sie eine Audio-Sprachausgabe.

### 7.1 Stapelverarbeitung & Fortsetzen

Sie müssen ein riesiges Dokument nicht auf einmal lesen. Wählen Sie einen Seitenbereich (z. B. `1-20`) oder behalten Sie die Standardeinstellung bei, und die KI extrahiert alle Seiten im Hintergrund. Falls NVDA abstürzt oder der Scan unterbrochen wird, merkt sich das Add-on Ihren Fortschritt und bietet an, genau dort **fortzufahren**, wo Sie aufgehört haben – selbst über Neustarts hinweg! Vollständig gescannte Dokumente werden zudem zwischengespeichert, sodass ein erneutes Öffnen (aus den Zuletzt gelesenen Dokumenten oder über **D**) den Text sofort ohne erneutes OCR lädt, sofern sich die Quelldateien nicht geändert haben.

### 7.2 Intelligente Dateiaktion

Sie müssen das Dokument nicht immer zuerst über den Dialog öffnen. Markieren Sie im Explorer einfach eine PDF-, Bild- oder Text-/HTML-Datei und drücken Sie **D** (Dokumentenleser) – oder markieren Sie eine PDF- oder Bilddatei und drücken Sie **F** (Smarte Datei-Aktion) in der Befehlsebene. Das Add-on umgeht den Dateidialog sofort und verarbeitet die markierte Datei. Die Auswahl mehrerer Dateien verarbeitet diese gebündelt als ein Gesamtdokument.

### 7.3 Steuerelemente & Tastenkombinationen des Dokumentenbetrachters

Wenn das Fenster des Dokumentenlesers geöffnet ist, stehen folgende Optionen zur Verfügung:

#### Tastenkombinationen

- **Strg + BildAb / Strg + BildAuf:** Zur nächsten / vorherigen Seite wechseln.
- **Pfeil runter / hoch:** Erreicht Ihr Cursor die letzte Zeile einer Seite, springt **Pfeil runter** automatisch zur nächsten Seite; **Pfeil hoch** am oberen Seitenrand bringt Sie nahtlos zur vorherigen Seite zurück.
- **Alt + A:** Öffnet einen Chat-Dialog, um Fragen zum Dokument zu stellen.
- **Alt + R:** Erzwingt einen **erneuten Scan mit KI** über Ihren aktiven Anbieter.
- **Alt + G:** Erzeugt und speichert eine hochwertige Audiodatei (WAV/MP3). _Ausgeblendet, wenn der Anbieter kein TTS unterstützt._
- **Alt + S / Strg + S:** Speichert den extrahierten Text als TXT- oder HTML-Datei.

#### Schaltflächen & Steuerelemente

- **Gehe zu:** Wählen Sie eine beliebige Seite aus der Seitenauswahl.
- **Formatiert anzeigen:** Zeigt das gesamte Dokument zusammenhängend als formatierten Text an.
- **Retry Failed Pages:** Retry only the batches that failed due to a temporary server error (e.g., high demand). This button appears automatically when needed.
- **TTS-Stimme / TTS-Engine:** Wählen Sie die Stimme; bei Gemini können Sie zwischen **Standard TTS** und gestreamtem **Gemini Live** wählen.
- **Zurück / Weiter:** Zwischen Seiten blättern (entspricht Strg+BildAuf/BildAb).

### 7.4 Zuletzt geöffnete Dokumente (D)

**Zuletzt gelesene Dokumente im Reader:** Das Drücken von **D** in der Befehlsebene zeigt nun Ihre kürzlich gelesenen Dokumente an erster Stelle. Wählen Sie eines aus, um an der vorherigen Leseposition fortzufahren – selbst wenn das OCR bereits beendet war – oder drücken Sie **Datei öffnen...** (`Strg + O`), um wie gewohnt zu suchen.

## 9. Semantische KI-Beschriftung & UI Explorer

Stecken Sie in einer Anwendung fest, in der überall nur „unbenannte Schaltfläche“ angesagt wird? Die semantische KI-Beschriftungs-Engine löst dieses Problem dauerhaft.

### 8.1 Dauerhafte Objektbeschriftung (L)

Fokussieren Sie Ihren Screenreader auf eine unbenannte Grafik oder Schaltfläche und drücken Sie **L** in der Befehlsebene. Die KI schaut sich die Schaltfläche visuell an, ermittelt ihre Funktion und vergibt eine dauerhafte Beschriftung.
Im Gegensatz zu älteren Beschriftungswerkzeugen verwendet dieses Add-on ein fortschrittliches, hybrides „Objektsignatur-System“ (AutomationId/ControlID). Ihre benutzerdefinierten Beschriftungen überstehen das Ändern der Fenstergröße, Monitorwechsel und Anwendungs-Updates!

### 8.2 Vollständiger Anwendungs-Scan (Umschalt + L)

Drücken Sie **Umschalt + L**, um das gesamte aktive Fenster auf einmal zu scannen. Die KI findet alle unbeschrifteten Elemente und benennt sie intelligent in einem Rutsch. Sie können diese Beschriftungen später im integrierten Beschriftungs-Manager anzeigen, umbenennen oder im Stapel löschen.

### 8.3 UI Explorer (E)

Möchten Sie mit einem Element interagieren, ohne manuell dorthin zu navigieren? Drücken Sie **E**, um den UI-Explorer zu aktivieren. Die KI scannt den Bildschirm und generiert eine barrierefreie Liste aller anklickbaren Elemente (und ignoriert dabei System-Rauschen wie die Taskleiste). Wählen Sie ein Element aus der Liste, und das Add-on klickt es sofort für Sie an.

## 10. Live-Sprachassistent

The Live Assistant turns Vision Assistant Pro into a real-time, interactive copilot.
_(Note: This feature is exclusive to Google Gemini and Gemini-compatible Custom providers)._

- **Aktivierung:** Drücken Sie **Strg + L** in der Befehlsebene, um den Live-Assistenten-Dialog zu öffnen.
- **Echtzeit-Interaktion:** Sprechen Sie ganz natürlich durch Ihr Mikrofon. Die KI hört gleichzeitig auf Ihre Stimme und schaut auf Ihren aktiven Bildschirm. Sie können Fragen stellen wie „Was sehe ich hier?“ oder „Lies mir den dritten Absatz vor.“
- **Push-to-Talk:** Aktivieren Sie **Push-to-Talk** im Reiter Live-Assistent (oder schalten Sie es direkt im Live-Assistenten-Fenster um), halten Sie die zugewiesene Taste zum Sprechen und lassen Sie sie los, um abzuschließen. Das hält das Mikrofon stumm, bis Sie drücken – ideal für laute Umgebungen.
- **Webcam-Eingabe:** Aktivieren Sie das Kontrollkästchen **&Webcam verwenden** im Live-Assistenten-Fenster, um anstelle des Bildschirms Ihren Kamerafeed an die KI zu senden – fragen Sie nach physischen Gegenständen, gedruckten Texten oder Ihrer Umgebung. Ist ffmpeg noch nicht installiert, lädt das Aktivieren der Option die Komponente einmalig mit Ihrer Zustimmung herunter; die Option ist deaktiviert, wenn keine Kamera erkannt wird oder Windows-Datenschutzeinstellungen den Zugriff blockieren.
- **Anpassung:** Direkt im Dialog können Sie den Sprachstil der KI ändern (z. B. Professionell, Freundlich, Aufgeweckt) und die „Denktiefe“ anpassen, um zu steuern, wie gründlich die KI vor einer Antwort nachdenkt.

## 11. Ambient Observer (Hintergrund-Assistent)

The Ambient Observer turns Vision Assistant Pro into your background eyes, without any conversation: it keeps listening and watching while you work, reports what changes, and stays silent when nothing happens.
_(Note: This feature is exclusive to Google Gemini and Gemini-compatible Custom providers)._

- **Visueller Übersetzungsdialog:** Neues Fenster für Übersetzungsergebnisse, das zeilenweises Lesen langer Texte ermöglicht.
- **Modes:** **Audio Translation Only** translates what it hears, **Screen Watcher Only** reports screen changes, and **Webcam Watcher Only** opens the Live Assistant window with your camera and Push to Talk, so you can ask questions about what the camera sees.
- **Audio Source:** In the audio mode, choose whether to translate your **Microphone** or the **System Audio (Loopback)**. The small loopback library is downloaded once on first use, with your permission.
- **Context:** For the screen and webcam modes, pick an optional **About what I am doing** option (for example watching a film, following a meeting or call, reading a label, or checking your appearance) to focus the reports; you can also type your own context.
- **Reporting:** The add-on compares every new frame with the previous one and sends it to the AI only when the picture really changed, so a static screen never costs you requests. The AI then reports only what is new and never repeats itself.
- **Welcome Message:** Except in the translation mode, the observer greets you briefly when it starts, so you know it is listening.
- **Settings:** In **Settings > Live Assistant**, set the **Observer Mode**, the **Frame Interval** (1 to 10 seconds) and the **Reporting Style** (brief or detailed). The observer instruction and each context text can be edited in the Prompt Manager (section **Ambient**).

## 12. Benutzerdefinierte Eingabeaufforderungen & Variablen

Sie können Prompts unter **Einstellungen > Prompts > Prompts verwalten...** verwalten.

- **Filter:** The **Default Prompts** tab has a **Filter** list above the prompt list that shows **All** prompts or only one section at a time (for example **Ambient**), so long lists stay easy to navigate.

### Eigene Prompt-Tastenkombinationen

Weisen Sie benutzerdefinierten Prompts direkt im Prompt-Manager ein eigenes Tastaturkürzel zu, um sie sofort mit der aktuellen Auswahl oder dem Kontext auszuführen:

- **Befehlsebene:** Einführung der Befehlsebene (Standard: `NVDA+Umschalt+V`), um Kürzel unter einer Haupttaste zu gruppieren.
- **Tastenkombination** (z. B. `Strg + Umschalt + 1`, `Alt + P` oder `Einfügen + 1`): Funktioniert eigenständig global.

### Per-Prompt Feedback Behavior

Each custom prompt can individually define its output delivery behavior:

- **Global setting:** Follows the general Connection output setting (Direct Output or Chat window).
- **Diktat-Stabilität:** Ignoriert nun Audioclips unter 1 Sekunde, um Halluzinationen zu vermeiden.
- **Direct Output (NVDA message):** Speaks/brailles the AI response directly via NVDA speech.
- **Copy to clipboard and Direct Output:** Copies the response to the clipboard and speaks it directly.
- **Chat window:** Always opens the result in an interactive conversation window.

### Unterstützte Variablen

- `[selection]`: Aktuell markierter Text.
- `[text]`: Complete text content of the currently focused edit field (automatically ignores protected password boxes).
- `[currentURL]`: Webpage or document URL from supported web browsers (Chrome, Edge, Firefox).
- `[clipboard]`: Inhalt der Zwischenablage.
- `[clipboard_image]`: Aktuell in der Zwischenablage befindliches Bild.
- `[screen_obj]`: Screenshot des Navigator-Objekts.
- `[screen_fg_obj]`: Screenshot des aktiven Vordergrundfensters.
- `[screen_full]`: Vollbild-Screenshot.
- `[file_ocr]`: Bild-/PDF-Datei für Textextraktion auswählen.
- `[file_read]`: Dokument zum Lesen auswählen (TXT, Code, PDF).
- `[file_audio]`: Audiodatei zur Analyse auswählen (MP3, WAV, OGG).
- `[ambient_screen]`: Starts continuous Screen Observer background session.
- `[ambient_webcam]`: Starts continuous Webcam Observer background session (checks Push to Talk from settings).
- `[ambient_audio]`: Starts live Audio Observer translation session.
- `[loopback]`: Uses system audio playback as sound source (for `[ambient_audio]`).
- `[mic]`: Uses microphone as sound source (for `[ambient_audio]` and `[ambient_webcam]`).
- `[brief]`: Sets observer reporting style to brief (single sentence).
- `[detailed]`: Sets observer reporting style to detailed (2-3 sentences).
- `[lang:code]`: Specifies target language code for audio translation (e.g., `[lang:fa]`, `[lang:en]`).
- `{target_lang}`: Aktuelle Zielsprache.
- `{source_lang}`: Aktuelle Quellsprache.
- `{response_lang}`: Aktuelle KI-Antwortsprache.
- `{swap_target}`: Ausweichsprache für die intelligente Übersetzung mit automatischem Tausch.
- `{swap_instruction}`: Anweisungsblock für die intelligente Übersetzung mit automatischem Tausch.

_Note on Ambient Prompts:_ Prompts containing ambient variables act as a toggle — pressing the shortcut while active immediately stops the session. Incompatible combinations (such as combining static screenshot variables like `[screen_full]` with ambient observer modes, combining multiple ambient modes, or adding prompt instructions to `[ambient_audio]`) are strictly validated and prevented when saving.

## 13. Praktische Anwendungsfälle (Welche Funktion sollte ich verwenden?)

KI Assistent pro ist vollgepackt mit fortschrittlichen Werkzeugen. Hier sind einige häufige Szenarien, die Ihnen bei der Auswahl der richtigen Funktion helfen:

- _Lösung:_ Drücken Sie **O** (Vollbild-Vision). Die KI analysiert den gesamten Bildschirm und beschreibt genau, wo Elemente, Texte und Schaltflächen positioniert sind.

- _Lösung:_ Bewegen Sie Ihr Navigator-Objekt auf die Grafik und drücken Sie **V** (Objekt-Vision). Die KI beschreibt speziell, was dieses Bild enthält.

- _Lösung:_ Drücken Sie **Umschalt + V** auf Ihrem Video und wählen Sie **„Audiobeschreibung generieren (SRT-Datei)“**. Wenn der Vorgang abgeschlossen ist, klicken Sie auf **„Synchronisierte Sprachausgabe generieren (MP3)“** und wählen Sie **„Erweiterte AD“**. Das Add-on erstellt eine Tonspur, die den Filmdialog intelligent pausiert, um die visuellen Szenen zu beschreiben.

- _Lösung:_ Drücken Sie **L**, um die spezifische Schaltfläche mithilfe von KI dauerhaft zu beschriften. Oder drücken Sie **Umschalt + L**, um das gesamte Fenster auf einmal zu scannen und zu beschriften. Wenn Sie nur schnell auf etwas klicken möchten, drücken Sie **E** (UI-Explorer), um eine Liste aller anklickbaren Elemente zu erhalten.

- _Lösung:_ Drücken Sie **C** (CAPTCHA-Löser). Die KI erfasst das CAPTCHA automatisch, löst es und trägt die Antwort in das richtige Feld ein.

- _Lösung:_ Drücken Sie **D** (Dokumentenleser), stellen Sie Ihren Anbieter auf Google Gemini ein und geben Sie den Seitenbereich `1-50` ein. Das Add-on extrahiert den Text im Hintergrund fehlerfrei.

- _Lösung:_ Drücken Sie **Strg + V**, um die Aufnahme des Bildschirms zu starten. Lassen Sie die Anleitung laufen und drücken Sie dann erneut **Strg + V**. Die KI erklärt Ihnen genau, was gezeigt wurde.

- _Lösung:_ Gehen Sie zu **Einstellungen > Erweitert**, aktivieren Sie **"Dedizierte Log-Datei aktivieren"** und stellen Sie das **Log-Level** auf **"Debug"**. Führen Sie die Aktion erneut aus und klicken Sie auf **"Log-Datei öffnen"**, um technische Details einzusehen oder die Datei `vision_assistant.log` an ein Support-Ticket anzuhängen.

***

**Hinweis:** Für alle KI-Funktionen ist eine aktive Internetverbindung erforderlich. Mehrseitige Dokumente werden automatisch verarbeitet.

## 14. Support & Community

Bleiben Sie auf dem Laufenden über Neuigkeiten, Funktionen und Veröffentlichungen:

- **Telegram-Kanal:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro?utm_source=gemini)
- **GitHub Issues:** Für Fehlermeldungen und Funktionsanfragen.

### Fehlerbehebung & Protokolle melden

Wenn Sie ein Issue auf GitHub erstellen oder Support anfragen, geben Sie bitte Details zu Ihrem aktiven KI-Anbieter, Modell und der NVDA-Version an. Wenn Sie Verbindungsprobleme oder unerwartete Abstürze haben, aktivieren Sie die dedizierte Log-Datei unter **Einstellungen > Erweitert**, stellen Sie das Problem nach und hängen Sie Ihre `vision_assistant.log`-Datei an, damit wir das Problem schneller lösen können.

## 15. Projekt-Unterstützer

Ein herzliches Dankeschön an unsere Community-Mitglieder, die die kontinuierliche Entwicklung und Pflege dieses Projekts durch ihre großzügigen finanziellen Beiträge unterstützen:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**
- **leonardo0216**
- **Sergei Fleytin**
- **Arne Siebert**
- **Schalkefan**
- **Rainer Brell**
- **[avalai.org](https://avalai.org?utm_source=gemini)**

_Wenn Sie das Projekt finanziell unterstützen und Ihren Namen hier sehen möchten, finden Sie die Option **Spenden** im NVDA-Werkzeuge-Menü (Untermenü KI-Assistent) oder während des Einrichtungsprozesses nach der Installation._

---

## Änderungen für 2026.10.15

- **The Most Requested Fix — Creating a Gemini API Key Is Finally Easy**: Getting an API key on **aistudio.google.com** used to be the hardest step of all. With a screen reader the pages were confusing, and some people simply could not create a key at all. That problem is now solved directly inside the add-on. Press **G** in the Command Layer (or use **Get a Gemini API Key...** in Settings), sign in through your default browser with zero external setup, and your key is created and configured with one confirmation — even if you never had a project before.
- **Ambient Observer**: The background assistant is here. Press **Shift+O** in the Command Layer to start it, and press it again to stop it. It can translate what it hears (your microphone or the sound of the system), watch the screen and tell you what changed, or open the Live Assistant with your webcam and Push to Talk so you can ask about whatever the camera sees. It sends a picture only when something really changed, so a still screen costs you nothing, and it stays quiet when nothing is happening. You can also launch and toggle the observer directly through Custom Prompts and dedicated shortcut keys using `[ambient_screen]`, `[ambient_webcam]`, or `[ambient_audio]` along with modifiers (`[loopback]`, `[mic]`, `[brief]`, `[detailed]`, `[lang:code]`), with automatic validation against conflicting variable combinations.
- **Live Operator**: The Live Assistant can now carry out what you ask on your computer while you talk to it. Press **Control+A** in the Command Layer to start a live operator session, then just ask in plain language. It works through multi-step requests, says every step in the Live Assistant’s own voice, takes care of the key combinations it needs, and decides by itself when the task is finished. **Live Direct Output (No Window)** is in Quick Settings too.
- **Charakter-Wörterbuch & Serienverwaltung:** Der Videoanalyse-Dialog enthält nun ein leistungsstarkes **Charakter-Wörterbuch**-System! Fügen Sie Charakternamen, optische Beschreibungen und Rollen pro Serie hinzu, bearbeiten, importieren oder verwalten Sie diese – die KI gleicht erkannte Personen automatisch mit dem Wörterbuch ab und fügt neue Charaktere beim Analysieren weiterer Episoden hinzu. Ihre manuellen Notizen behalten immer Vorrang vor KI-Aktualisierungen, während Beschreibungen über Episoden hinweg aktuell bleiben. Das Wörterbuch wird pro Serie gespeichert und für jedes Video der Serie wiederverwendet. Drücken Sie in der Liste **F2** zum Bearbeiten und **Entf** zum Löschen.
- **SOCKS5, HTTP, and Reverse Proxy Support with Latency Testing**: Seamlessly bypass network restrictions with complete proxy support across the entire add-on — including the Live Assistant, Ambient Observer, and TTS generation! Choose from 4 operating modes in General settings: **Auto-detect**, **SOCKS5 Proxy**, **HTTP Proxy**, or **Reverse Proxy**. SOCKS5 supports RFC 1929 username/password authentication and domain tunneling; HTTP proxy supports Basic authentication. A new **Test Proxy Connection** button runs in the background and announces your connection latency in milliseconds.
- **48-Stunden-Zwischenspeicherung von Videos:** Zu Gemini hochgeladene Videos werden nun für 48 Stunden zwischengespeichert! Sie können SRT- oder MP3-Dateien für dasselbe Video neu generieren, ohne es erneut hochzuladen – selbst nach einem Neustart von NVDA. Der Cache ist schlüsselabhängig und wird automatisch zurückgesetzt, wenn sich Ihr API-Schlüssel ändert.
- Die Stille-Erkennung nutzt nun das neuronale Modell **Silero VAD** (das bei Erstbenutzung genau wie ffmpeg und eSpeak mit Ihrer Zustimmung automatisch heruntergeladen wird) für hochpräzises Gap-Timing – wodurch echte Dialogpausen zuverlässig von Musik und Hintergrundgeräuschen unterschieden werden. The model is downloaded automatically on first use (with your permission), just like ffmpeg and eSpeak.
- **Webcam-Video für den Live-Assistenten:** Das Live-Assistenten-Fenster bietet nun die Option **&Webcam verwenden**, um Ihren Kamerafeed statt des Bildschirms an die KI zu senden – perfekt für Fragen zu realen Objekten, Dokumenten oder Ihrer Umgebung. Fehlt ffmpeg, wird es einmalig mit Ihrer Zustimmung heruntergeladen. Die Option ist deaktiviert, wenn keine Kamera erkannt wird oder Windows-Datenschutzeinstellungen blockieren. Liefert die aktivierte Kamera keine Bilder, wird dies im NVDA-Log protokolliert, statt geräuschlos zum Bildschirm zurückzukehren.
- **Audio Output Device Selection**: You can now select a dedicated audio output device for the Live Assistant and Ambient Observer. Choose between NVDA's default output, Windows Sound Mapper, or any connected physical sound card (like USB headphones or external speakers) in the Live Settings tab, directly inside the Live Assistant dialog, or on the fly via Quick Settings (NVDA+Shift+V then Up/Down/Left/Right).
- **Prompt Manager**: The Default Prompts tab has a **Filter** list now, so you can show all prompts or just one section (for example **Ambient**). You can also edit the observer’s context texts and the new **Live Operator Instruction** there.
- **Smart Model Filtering in Advanced Routing**: Advanced Model Routing dropdowns now dynamically categorize Gemini models by capability without clutter. The Live Assistant only displays genuine bidirectional live and native-audio models, TTS only displays dedicated speech synthesis models, STT prioritizes Transcribe and multimodal models, and Video Analysis, OCR, and AI Operator cleanly filter out single-purpose utility models (such as image generation, video generation, and embedding models). Future models are detected automatically based on capability without requiring version updates.
- **Erfassung des ersten Auftretens von Charakteren:** Die KI beschreibt das Aussehen jedes Charakters nun nur noch ein einziges Mal – beim ersten Auftauchen im Video. Nachfolgende Auftritte verwenden nur noch die Namen, was redundante Beschreibungen verhindert und die Erzählung lebendig und natürlich hält.
- **Einheitliches Datenverzeichnis:** Alle Datendateien des Add-ons (Verlauf, Serien, Beschriftungen, OCR-Fortschritte, Caches und Logs) wurden in einem einzigen `VisionAssistant`-Ordner innerhalb Ihres NVDA-Konfigurationsverzeichnisses zusammengeführt – was Ordnung schafft und manuelle Sicherungen vereinfacht.
- **Verbesserter Speicher-Workflow für Videos:** Beim Speichern von SRT- oder MP3-Dateien öffnet sich der Dateidialog nun standardmäßig im Quellordner des Videos, egal ob Sie das Video über den Dateidialog oder per Umschalt+V aus dem Explorer geöffnet haben.
- **Dokumente mit oder ohne Zwischenspeicher löschen:** Der Verlaufsdialog (`Strg + H`) bietet nun zwei Löschoptionen für Dokumente – drücken Sie Entf und wählen Sie **Nur aus Verlauf löschen** oder **Aus Verlauf und Cache löschen**. Die zweite Option leert den OCR-Cache des Dokuments, sodass es beim nächsten Öffnen von Grund auf neu gescannt wird – ideal nach einem fehlerhaften Scan. Ein Kontrollkästchen **Nicht mehr fragen** merkt sich Ihre Wahl. Wiederaufnahmedaten unterbrochener Vorgänge bleiben unangetastet.
- **Engine-abhängiger, zusammenführender OCR-Cache im Dokumentenleser:** Zwischengespeicherter OCR-Text wird nun pro OCR-Engine getrennt gespeichert; das Wechseln der Engine scannt somit stets mit der neuen Engine neu, anstatt alte Ergebnisse abzuspielen. Beim erneuten Öffnen eines Dokuments erscheint der Seitenbereichsdialog erneut (mit Ihrer letzten Auswahl vorausgewählt), bereits gescannte Seiten werden sofort wiederverwendet und nur fehlende Seiten nachgeladen – der Cache führt Seiten zusammen, statt überschrieben zu werden.
- **PDF Compression in Document Reader**: Added an optional **Compress PDF pages before processing** setting in the Document Reader's page range dialog. When uploading large or high-resolution scanned PDF documents to Gemini or Mistral, pages are automatically downscaled and re-compressed to dramatically reduce upload payload size, speed up processing, and prevent network timeouts. The option is disabled by default and automatically hidden when using the Chrome engine or base64-based image providers.
- **Per-Prompt Feedback Behavior Customization**: Customize how each custom prompt delivers its output individually! In the custom prompt editor, choose between **Global setting**, **Copy to clipboard**, **Direct Output (NVDA message)**, **Copy to clipboard and Direct Output**, or **Chat window**. This allows specific prompts to speak directly without opening a window while others open a full chat.
- **New Dynamic Prompt Variables (`[currentURL]` & `[text]`)**: Custom Prompts now support `[currentURL]` to capture the active document URL across Google Chrome, Mozilla Firefox, and Microsoft Edge, and `[text]` to dynamically insert the full text content of the currently focused edit field (ignoring protected password boxes).
- **Twitter/X Video Downloader Overhaul**: Restored downloading and analysis of Twitter/X videos following upstream scraper failures. Video extraction now utilizes the robust FixTweet API to directly fetch highest-quality MP4 streams from Twitter's CDN, complete with automatic TwitSave fallback and proxy support.
- **Instagram Video Downloader Fix**: Restored downloading and analysis of Instagram Reels and video URLs following upstream form changes on the downloader service.
- **Fixes & Performance**: Push to Talk answers the moment you press the key, the Live Assistant no longer starts a reply in the middle of a sentence, the observer no longer reports the previous picture, and the Thinking Depth list only offers what your model actually supports. The AI Operator can scroll left and right too. Fixed an `AttributeError` when analyzing online videos, and prevented custom prompts without text selection from accidentally injecting background window titles into AI requests.

## Änderungen für 01.09.2026

- **Verlauf (Strg + H):** Die Befehlsebene enthält nun einen **Verlaufsdialog** (`Strg + H`), der vergangene Chats und Dokumente mit Filtern für Alle, Chats und Dokumente auflistet. Öffnen Sie jeden Chat mit dem gesamten Konversationsverlauf erneut – angehängte Dateien werden automatisch wieder verknüpft – oder setzen Sie das Lesen von Dokumenten fort. Drücken Sie **Entf**, um einzelne Einträge zu entfernen, oder leeren Sie alles auf einmal.
- Das Drücken von **D** in der Befehlsebene listet Ihre kürzlich geöffneten Dokumente zuerst auf. Wählen Sie eines aus, um direkt auf der Seite weiterzulesen, auf der Sie zuletzt waren – selbst wenn das OCR bereits komplett abgeschlossen ist – oder drücken Sie **Datei öffnen...** (`Strg + O`), um wie gewohnt nach einer Datei zu suchen.
- **Push-to-Talk für den Live-Assistenten:** Übernehmen Sie die volle Kontrolle über Live-Gespräche! Aktivieren Sie **Push-to-Talk** im neuen Reiter für den Live-Assistenten und weisen Sie eine beliebige Taste zu – selbst einzelne Sondertasten wie `Linke Strg-Taste`. Halten Sie die Taste zum Sprechen gedrückt und lassen Sie sie los, wenn Sie fertig sind, begleitet von einem kurzen Signalton. Ein Umschalter existiert auch direkt im Live-Fenster.
- **Gemini 2.5 Flash Native Audio:** Der Live-Assistent unterstützt nun das native Audiomodell von Gemini 2.5 Flash (`gemini-2.5-flash-native-audio-preview-12-2025`) für extrem latenzarme und natürliche Sprachgespräche. Wählbar unter **Einstellungen → Erweitertes Modell-Routing → Live-Assistenten-Modell (nur Gemini)** oder auf „Auto“ belassen.
- **Einstellungen sichern & wiederherstellen:** Umfangreiches Backup- und Wiederherstellungssystem im Reiter **Erweitert** hinzugefügt! Sichern Sie alle Add-on-Einstellungen – inklusive API-Schlüssel, Modelle, eigene Prompts und Präferenzen – in einer JSON-Datei. Beim Backup kann zwischen **Alles** (Einstellungen, eigene Beschriftungen, OCR-Fortschritte und Verlauf) oder **Nur Einstellungen** gewählt werden.
- **Direktes Lesen von Text & HTML:** Der Dokumentenleser kann nun reine Text- (`.txt`) und HTML-Dateien (`.html`, `.htm`) direkt öffnen! Kodierungen werden automatisch erkannt, störende Skripte und Formatierungen bereinigt und Inhalte intelligent in Seiten aufgeteilt – ganz ohne OCR oder KI-Aufwand!
- **Gemini Live TTS für den Dokumentenleser:** Die Schaltfläche „Audio generieren“ unterstützt jetzt Gemini Live – eine hochwertige, flüssige Streaming-Text-to-Speech-Engine! Ist Gemini aktiv, kann direkt im Reader zwischen Standard-TTS und Gemini Live gewählt werden.
- **Custom Prompt Shortcuts**: You can now assign a shortcut key to any of your custom prompts right from the Prompt Manager! Give every prompt its own dedicated key or key combination to run it instantly, automatically capturing your current selection or context with zero extra steps!
- **Navigation durch Chat-Nachrichten:** Navigieren Sie freihändig durch jedes Gespräch! Drücken Sie in Chat-Fenstern `Alt + Pfeil runter` für die nächste und `Alt + Pfeil hoch` für die vorherige Nachricht – mit klarer Ansage von „Sie“ / „KI“ sowie Randmeldungen („Erste Nachricht“ / „Letzte Nachricht“).
- **Chat-Nachricht kopieren (Alt + C):** Kopieren Sie die aktuell ausgewählte Nachricht beim Durchgehen mit `Alt + Pfeil hoch/runter` per `Alt + C` in die Zwischenablage – unter Beachtung der Markdown-Bereinigungseinstellung.
- **Direct Chat System Prompt**: The Direct Chat (`Shift+C`) now has its own editable system prompt — "Direct Chat Instruction" — that sets the assistant's persona and response language for every conversation. You can customize it from the Prompt Manager's Default Prompts tab.
- **Document Reader Cursor Page Navigation**: Reading multi-page documents just got smoother! **Cursor-Seitenwechsel im Dokumentenleser:** Erreicht Ihr Cursor beim Lesen die letzte Zeile einer Seite und Sie drücken `Pfeil runter`, springt das Dokument automatisch zur nächsten Seite. Pressing `Up` at the start of a page seamlessly takes you back to the previous one — no more manual page switching while reading!
- **Neue Schalter in den Schnelleinstellungen:** Die Optionen „KI-Antworten in die Zwischenablage kopieren“, „Direkte Ausgabe (Kein Chat-Fenster)“, „Bereinigtes Markdown im Chat“ und „Smart Swap“ können nun direkt über die Schnelleinstellungen der Befehlsebene ein- und ausgeschaltet werden.
- **Eigener Reiter für den Live-Assistenten:** Der Live-Assistent hat einen eigenen Einstellungsreiter erhalten. Die Option „Direkte Ausgabe (Kein Fenster)“ wurde hierhin verschoben. Der Reiter erscheint dynamisch nur, wenn Google Gemini (oder ein kompatibler benutzerdefinierter Anbieter) aktiv ist.

## Änderungen für 06.08.2026

- **Beschriftung im UI-Explorer:** Elemente können nun direkt innerhalb des UI-Explorers beschriftet werden! Eine neue Schaltfläche "Beschriftung hinzufügen" wurde ergänzt, und das Fenster bleibt geöffnet, damit mehrere Objekte nacheinander barrierefrei beschriftet werden können.
- **Erweiterte Schnelleinstellungs-Ebene:** Die Befehlsebene (`NVDA+Umschalt+V`) bleibt nun aktiv und interaktiv! Sie können `Pfeil hoch/runter` nutzen, um zwischen Schnelleinstellungen (Anbieter, Modell, KI-Antwortsprache, TTS-Modell) zu navigieren, und `Pfeil links/rechts`, um Werte sofort mit Sprachausgabe zu ändern. Your selections take effect immediately (including auto-enabling advanced routing when necessary), and the layer stays alive while you configure.
- **Direkter Chat (`Umschalt+C`):** Neuer Befehl in der Befehlsebene! Press `Shift+C` to instantly open a "Direct Chat" window. This provides a clean, text-based conversational interface with the AI right away, without needing an image or document as a starting point.
- **Flawless Chat History Recall**: Fixed a major bug where pressing `Space` to recall the last result would lose your subsequent chat history. Now, the add-on globally tracks your conversation. If you chat, close the dialog, and press `Space` to recall it, your entire back-and-forth history is perfectly restored! Works for Direct Chat, Vision Analysis, Document Chat, and Translation.
- **Inline-Bildbeschreibungen bei OCR:** Optionale Funktion zur Beschreibung von Bildern direkt im OCR-Textfluss hinzugefügt. Dies kann in den Einstellungen, vor der Extraktion im Dokumentenleser oder spontan über die Schnelleinstellungs-Ebene umgeschaltet werden.
- **Voice Translation (`Control+T`)**: Added a powerful new feature! Dictate speech and instantly translate and type it using AI based on your configured source and target languages.
- **Fehlerbehebungen & Stabilitätsverbesserungen:** Ein Hänger bei der MP3-Generierung beim Schließen des Fortschrittsdialogs wurde behoben, eine Race-Condition im Speicher des Charakter-Wörterbuchs beseitigt, eine saubere Fehlerberichterstattung bei MP3-Kodierungsfehlern ergänzt und die Warteschleife des Dokumentenlesers so angepasst, dass Benutzerabbrüche sofort beachtet werden.
- **Fortschrittsanzeige bei Updates & eSpeak-NG:** Der Download-Dialog für Add-on-Updates sowie eSpeak-NG zeigt nun den genauen Fortschritt in Prozent an.
- **Resilientes Stapel-OCR:** Behebt Unterbrechungen bei der Stapel-PDF-Verarbeitung; wenn ein API-Schlüssel sein Limit erreicht, wird automatisch zum nächsten Schlüssel gewechselt und der Scan fortgesetzt.
- **Visual Captcha Support**: Added robust support for visual captcha solving. It attempts to automatically solve complex image challenges like hCaptcha and reCAPTCHA, significantly enhancing accessibility on challenging web forms.
- **Audio Transcriber Overhaul**: The Audio Transcriber module has been completely rebuilt and now supports both audio and video files. It features 3 distinct operation modes: "Transcribe (Original Language)", "Transcribe and Translate (Target Language)", and a new powerful "Dub and Translate (Target Language)" option (exclusive to Gemini) that generates a translated audio dub of the original speech.
- **Optional Page Numbers in Document Reader**: Added a new setting to toggle the inclusion of page numbers and separators in multi-page document outputs. You can easily manage this option from the main settings or toggle it on-the-fly via the Quick Settings layer. This feature applies to both text/HTML file exports and the inline "View Formatted" window, allowing you to read combined documents seamlessly.
- **Unlimited Gemini Live TTS for Video Descriptions**: You can now select "Gemini Live TTS" as the voice engine when generating Synchronized Audio Narration (MP3) for videos. This utilizes the Gemini Live API to synthesize high-quality audio descriptions without any character limits or length restrictions.
- **Codebase-Modularisierung:** Das Add-on wurde von einer einzelnen Datei in eine modulare Architektur mit mehreren Dateien aufgeteilt.
- **Settings UI Redesign**: Completely redesigned the Settings dialog to use a modern, tab-based interface instead of a grouped layout, providing better organization and easier navigation while keeping all existing options.
- **Global & Dedicated File Logging**: Added an optional global file logging system under the new "Advanced" settings tab. Automatically captures operational events, API traffic, and errors across all add-on modules into a dedicated file (`vision_assistant.log`). Supports configurable log verbosity levels (Debug, Info, Warning, Error), automated retention periods (1 hour to 90 days), and direct log opening or clearing from settings with zero performance impact or NVDA log interference.
- **Gemini Upload-Fortschritt:** Echtzeit-Fortschrittsanzeigen in Prozent beim Hochladen großer Dateien (Video, Audio, Dokumente) zur Gemini API.

## Änderungen für 15.07.2026

- **Intelligente API-Modellfilterung:** Komplette Überarbeitung des Modellfilterungssystems hin zu einem reinen Blacklist-Ansatz anstelle von Whitelists. Es wurden stärkere Filter-Schlüsselwörter eingeführt (`embedding`, `bison`, `gecko`, `audio`, `realtime`, `babbage`, `moderation`, `deep`, `antigravity`, `computer`), um sicherzustellen, dass die Haupt-Chat-Modellauswahl sauber und zukunftssicher bleibt, während alle spezialisierten Modelle im erweiterten Routing-Bereich weiterhin verfügbar sind.
- **Durchsuchbares erweitertes Routing:** Alle Dropdown-Menüs im erweiterten Modell-Routing (OCR, STT, TTS, Operator, Video, Live) sowie die eSpeak-Variantenauswahl sind nun vollständig durchsuchbar. Sie können tippen, um das gewünschte Modell oder die Variante schnell zu filtern und zu finden.
- **Neue Tastenkombinationen in der Befehlsebene:**
  - |
    \| **Alt + S** | Einstellungen | Öffnet direkt das Einstellungsfenster von KI Assistent pro.
  - **Bericht über erschöpfte Kontingente (`Alt + Q`):** Meldet die genaue Anzahl der Gemini-API-Schlüssel, die ihr tägliches Kontingent überschritten haben, identifiziert das betroffene Modell und sagt die genaue Zurücksetzungszeit an.
  - **Routing-Prüfung (`Alt + M`):** Überprüft und meldet Ihre aktuelle Konfiguration des erweiterten Modell-Routings und liest vor, welche Modelle aktiv für spezialisierte Aufgaben ausgewählt sind (Standardeinstellungen werden übersprungen).
- **Komplette Überarbeitung der Videoanalyse:** Die Videoanalyse wurde von Grund auf transformiert! Zuvor bot sie nur eine einfache Beschreibung von Online-Videos. Jetzt ist sie eine umfassende Videoverarbeitungssuite, die speziell für blinde Nutzer entwickelt wurde:
  - **Lokale Bildschirmaufnahme (`Strg+V`):** Sie können jetzt stumme Videos direkt von Ihrem Bildschirm aufnehmen. Die KI analysiert den aufgezeichneten Abschnitt und liefert eine hochdetaillierte Beschreibung der Szene, des Layouts und der Aktionen.
  - **Erstellung von Audiobeschreibungen (SRT):** Das Add-on kann nun hochdetaillierte Audiobeschreibungs-Skripte (im Standard-SRT-Format) für Videos generieren, komplett mit intelligentem Gap-Timing zur Pausenerkennung und wortgetreuem OCR für Bildschirmtexte.
  - **Synchronisierte Sprachausgabe (MP3-Export):** Neben textbasierten Untertiteln kann das Add-on die Audiobeschreibung in Sprache umwandeln, diese automatisch mit dem Originalton des Videos mischen, Audio-Ducking anwenden und das synchronisierte Ergebnis als MP3-Datei exportieren!
  - **Smarte Video-Datei-Aktion:** Wenn Sie eine lokale Videodatei fokussieren und die Video-Tastenkombination drücken, erkennt das Add-on diese automatisch und verarbeitet die Datei direkt.
  - **Fortgeschrittene Charakter-Verfolgung:** Die KI führt vorab eine Charakter-Erkennung durch. Sie erstellt ein globales Charakter-Wörterbuch und verfolgt Personen Abschnitt für Abschnitt fehlerfrei, ohne Identitäten zu verwechseln.
  - **Konfiguration der Videoanalyse:** Neue Einstellungen zur Steuerung von SRT-Blockgrößen, Charakter-Untertiteln und Haftungsausschlüssen wurden hinzugefügt.
  - **Erweitertes Modell-Routing:** Sie können nun explizit spezialisierte Videomodelle (`gemini_video_model`, `custom_video_model`) in den Einstellungen für das erweiterte Modell-Routing auswählen.
- **Smarte API-Kontingentverwaltung:** Verbesserte Handhabung von 429-Fehlern (Tägliches Limit) durch Modell-spezifische Erfassung. Wenn ein Schlüssel das Limit für ein bestimmtes Modell erreicht, wird er intelligent nur für dieses Modell gesperrt, bleibt aber für andere Modelle weiterhin einsatzbereit.

## Änderungen in 7.0.0

- **Fortsetzen nicht beendeter Scans:** Eine Fortsetzungsfunktion wurde sowohl für den Dokumentenleser als auch für die Smarten Datei-Aktionen hinzugefügt. Wenn ein Scan unterbrochen wird, können Sie nun an der Stelle weitermachen, an der er gestoppt wurde, anstatt von vorne beginnen zu müssen.
- **Neue Variable `[screen_fg_obj]`:** Eine neue Variable für eigene Prompts wurde hinzugefügt, um einen Screenshot ausschließlich des aktiven Vordergrundfensters anstelle des gesamten Bildschirms aufzunehmen.
- **Smarte Wiederholungen & Schlüsselrotation:** Das Add-on versucht nun bei temporären Serverüberlastungen (wie hoher Auslastung oder fehlerhaften Antworten) bis zu 5-mal unbemerkt eine Wiederholung mit demselben Schlüssel. Schlagen die Versuche fehl, wird automatisch zum nächsten API-Schlüssel in Ihrer Liste gewechselt.
- **Bildschirmvorhang-Erkennung:** Eine Prüfung wurde hinzugefügt, die verhindert, dass Screenshots aufgenommen werden, wenn der NVDA-Bildschirmvorhang aktiv ist (egal ob dauerhaft oder temporär über die Tastenkombination aktiviert). Das Add-on warnt Sie und bricht ab, um das Senden schwarzer Bilder und das Verschwenden von API-Tokens zu verhindern.
- **Verbesserungen im Dokumentenleser:** Der PDF-Seitenbereichsdialog wählt nun automatisch die in den Add-on-Einstellungen festgelegte Zielsprache vor. Zudem wurde die Thread-Verarbeitung optimiert, um sicherzustellen, dass Hintergrundaufgaben sauber beendet werden, wenn der Leser geschlossen wird.
- **Native Mistral OCR-Integration:** Die native Document OCR API von Mistral wurde integriert. Mehrseitige Dokumente werden automatisch zusammengeführt, hochgeladen und in Stapeln über den spezialisierten `/v1/ocr`-Endpunkt von Mistral verarbeitet, während einseitige Bilder ohne unnötige PDF-Konvertierung direkt verarbeitet werden.
- **Dynamische Handhabung benutzerdefinierter URLs:** Das Ändern der benutzerdefinierten API-URL löscht nun sofort die zwischengespeicherte Modellliste und stellt das manuelle Texteingabefeld für Modelle wieder her. Dies gewährleistet volle Kompatibilität mit benutzerdefinierten Endpunkten (wie Cloudflare AI Gateway), die den Standard-Endpunkt `/v1/models` nicht unterstützen.
- **Überarbeitete Eingabe-Engine für den KI-Operator:** Das zugrundeliegende Maus- und Tastatursimulationssystem für den KI-Operator wurde komplett neu geschrieben. Die veraltete `mouse_event`-API wurde durch die moderne Windows `SendInput`-API ersetzt, was eine deutlich höhere Kompatibilität mit modernen Anwendungen, benutzerkontengesteuerten Fenstern (UAC) und High-DPI-Displays mit sich bringt.
- **Stabile Drag & Drop-Aktionen:** Drag-and-Drop-Aktionen im KI-Operator laufen nun absolut stabil und zuverlässig. Die neue Engine nutzt natürliche Bewegungskurven, präzise Cursorpositionierung, optimiertes Timing und eine intelligente Anstups-Technik, um sicherzustellen, dass Windows und Anwendungen Drag-and-Drop-Gesten fehlerfrei erkennen.
- **Mehrere Monitore unterstützt:** Der KI-Operator unterstützt nun vollständig Setups mit mehreren Monitoren. Mausbewegungen und Klicks funktionieren über das `MOUSEEVENTF_VIRTUALDESK`-Flag korrekt auf allen Bildschirmen, was eine präzise Positionierung unabhängig vom Monitor der Zielanwendung garantiert.
- **Verbesserte Tastatursimulation:** Die Tastatureingabe wurde verbessert, um "Erweiterte Tasten" (wie Pfeiltasten, Pos1, Ende, BildAuf/Ab, Einfügen, Entf und F1-F12) vollständig zu unterstützen. Dies stellt sicher, dass Navigations- und Tastaturbefehle des KI-Operators in allen Anwendungen fehlerfrei funktionieren.
- **HEIC/HEIF-Bildunterstützung:** Native Unterstützung für iPhone-Fotoformate wurde hinzugefügt. Sie können nun `.heic`- und `.heif`-Dateien direkt für KI-Beschreibungen, OCR oder den Dokumentenleser auswählen, ohne sie vorher konvertieren zu müssen.

## Änderungen in 6.5.0

- **Live-Assistent:** Echtzeit-Sprach- und Bildschirmassistent hinzugefügt, der exklusiv für Google Gemini (oder Gemini-kompatible benutzerdefinierte Anbieter) verfügbar ist. Beinhaltet eine interaktive Anpassung von Stimme und Denktiefe direkt im Dialog, mit automatischer Wiederverbindung nach Einstellungsänderungen.
- **MiniMax KI-Anbieter:** MiniMax wurde als gleichwertiger Anbieter mit vollständiger multimodaler Unterstützung (Chat, Vision, OCR), benutzerdefiniertem TTS mit über 300+ dynamischen Stimmen und automatischem Entfernen von Denkblöcken (z. B. `<think>...</think>`) aus den Ausgaben integriert.
- **Übersetzung im Dokumentenleser:** Ein stiller Übersetzungsfehler für nicht-englische NVDA-Benutzer wurde behoben, indem sichergestellt wird, dass der standardmäßige zweistellige Sprachcode an Google Translate gesendet wird anstelle des lokalisierten Sprachnamens.
- **PDF-Stapelscan-Wiederholung:** Eine hochoptimierte, separate und stille Wiederholungslogik für das Scannen von PDF-Dokumentenstapeln wurde implementiert, um redundante Uploads zu vermeiden und störende Fehler-Popups während der Wiederholungen zu verhindern.
- **Status des Dokumentenlesers:** Ein Fehler wurde behoben, bei dem der Gesamtstatus des Plugins (überprüft mit `I`) während langer Dokumentenscans auf „Stapelverarbeitung gestartet“ hängen blieb.
- **Threading-Absturz behoben:** Ein schwerwiegender Thread-Assertion-Absturz (`IsMain() failed in wxTimerImpl`) beim Öffnen von Dokumenten aus einem Hintergrund-Thread wurde behoben, indem die GUI-Callback-Warteschlange auf `wx.CallAfter` umgestellt wurde.

## Änderungen in 6.1.2

- **Vorabprüfung auf doppelte Beschriftungen:** Ein Problem bei der Einzelbeschriftung wurde behoben, bei dem die Prüfung auf Duplikate alte Koordinatenschlüssel verwendete. Dies führte dazu, dass NVDA doppelte KI-Anfragen für bereits beschriftete Objekte stellte, anstatt die vorhandene Beschriftung anzusagen.
- **Dokumenten-Chat für Nicht-Gemini-Anbieter:** Eine strikte API-Schlüsselprüfung im Dokumenten-Chat (`on_ask`) wurde korrigiert, um sicherzustellen, dass Benutzer von OpenAI, Groq oder lokalen benutzerdefinierten Anbietern (wie Ollama) erfolgreich mit Dokumenten chatten können, ohne blockiert zu werden.
- **Schnelle Chrome-OCR-Übersetzung:** Die kostenlose, schlüssellose Übersetzungs-API für Chrome-OCR wurde wiederhergestellt. Das Übersetzen von extrahiertem Text umgeht nun Gemini-KI, was API-Kontingente spart und den Übersetzungsprozess beschleunigt.
- **Alphanumerischer Filter für CAPTCHAs:** Die Filterlogik im CAPTCHA-Löser wurde korrigiert, um sicherzustellen, dass nicht-alphanumerische Zeichen in allen Situationen ordnungsgemäß bereinigt werden.
- **Aktualisierung der Hilfe für die Befehlsebene:** Die Tastenkombination für die Statusansage im Hilfemenü wurde von `L` auf `I` korrigiert und beide Beschriftungsbefehle (`L` und `Umschalt+L`) wurden zur Liste hinzugefügt.

## Änderungen in 6.1.1

- **Korrektur der Denkausgabe bei Gemma 4:** Ein Problem mit Gemma 4-Modellen wurde behoben, bei dem der gesamte interne Denkprozess als endgültige Antwort angezeigt wurde oder das Deaktivieren des Denkens zu leeren Antworten führte. Das Add-on isoliert und extrahiert nun korrekt nur die finale, bereinigte Textantwort.
- **Stapel-OCR aus dem Datei-Explorer:** Sie können nun mehrere Fotos oder PDFs direkt im Windows Datei-Explorer auswählen und als Stapel Text extrahieren oder analysieren lassen. Das Add-on filtert und verarbeitet automatisch nur die unterstützten Dateiformate.

## Änderungen in 6.1.0

- **Universelle lokale KI-Integration (Lokale KI einrichten):** Eine neue Schaltfläche **"Lokale KI einrichten"** wurde in den Einstellungen für benutzerdefinierte Anbieter hinzugefügt. Benutzer können nun lokale KI-Engines wie **Ollama**, **LM Studio**, **Jan.ai** und **KoboldCPP** sofort automatisch konfigurieren.
- **Intelligenter lokaler Proxy-Bypass:** Die Verbindungslogik wurde mit einem fortschrittlichen Proxy-Bypass-Mechanismus neu aufgebaut. Das Add-on ist nun intelligent genug, um Windows-System-Proxys für lokale Loopback-Verbindungen vollständig zu umgehen, was stabile lokale KI-Verbindungen gewährleistet, selbst wenn Ihr VPN/TUN-Modus aktiv ist.
- **Ultra-stabile KI-Beschriftung (v2):** Absolute Bildschirmkoordinatenschlüssel wurden durch ein fortschrittliches, hybrides **Objektsignatur-System** ersetzt. Beschriftungen basieren nun auf programmgesteuerten Identifikatoren (UIA **AutomationId** oder Win32 **ControlID**) und fensterrelativen Koordinaten.
- **Nahtlose automatische Beschriftungsmigration:** Das Upgrade erfolgt völlig transparent. Das Add-on migriert Ihre älteren, auf Legacy-Koordinaten basierenden Beschriftungen beim ersten Fokussieren automatisch im Hintergrund in das neue, stabile Fingerabdruckformat – ganz ohne Datenverlust.

## Änderungen in 6.0

- **Einführung der semantischen KI-Beschriftung:** Benutzer können nun unbenannte Schaltflächen und Symbole mithilfe von KI dauerhaft beschriften. Drücken Sie **L**, um das aktuelle Navigator-Objekt zu beschriften (unterstützt sowohl den Tab-Fokus als auch die Objektnavigation), oder **Umschalt+L**, um die gesamte Anwendung auf einmal zu scannen und zu beschriften.
- **Intelligente Beschriftungsverwaltung:** Ein neuer, vollständig barrierefreier Beschriftungs-Manager-Dialog wurde hinzugefügt (erreichbar über **Umschalt+L**, falls Beschriftungen existieren), um benutzerdefinierte Beschriftungen anzuzeigen, umzubenennen oder im Stapel zu löschen.
- **Direkte Dateianalyse (Dateidialog umgehen):** Das Add-on ist nun intelligent genug, um zu erkennen, ob Sie gerade eine PDF- oder Bilddatei im Windows Datei-Explorer fokussieren. Das Drücken von **F (Smarte Datei-Aktion)** oder **D (Dokumentenleser)** auf einer markierten Datei verarbeitet diese sofort und umgeht den Standard-"Öffnen"-Dialog komplett.

## Änderungen in 5.6

- **OCR-Engine "Keine (Textschicht extrahieren)" hinzugefügt:** Benutzer können nun Text direkt aus durchsuchbaren PDFs extrahieren, ohne KI-Guthaben zu verbrauchen, was die Geschwindigkeit und den Datenschutz bei textbasierten Dokumenten erheblich verbessert.
- **Verfeinerte UI-Explorer-Genauigkeit:** Die UI-Explorer-Eingabeaufforderung wurde verbessert, um Elementtypen (wie Listeneinträge) besser zu identifizieren und Zustände wie „(Aktiviert)“, „(Ausgewählt)“ oder „(Erweitert)“ korrekt zu melden, während Windows-Systemkomponenten wie die Taskleiste und die Uhr ignoriert werden.
- **Installations-Einrichtungshinweis:** Nach der Installation wurde eine Benachrichtigung hinzugefügt, um Benutzer zum Einstellungsmenü zu führen, damit sie ihre API-Schlüssel und Präferenzen konfigurieren können.

## Änderungen in 5.5.2

- **Problem beim Tippen des KI-Operators behoben:** Ein Fehler wurde behoben, bei dem auf bestimmten Systemen der Buchstabe 'v' getippt wurde, anstatt Text einzufügen. Diese Korrektur behebt Timing-Konflikte, die bei hoher Systemlast auftraten.
- **Erhöhte Stabilität:** Es wurde eine robuste Fehlerbehandlung für Zwischenablage-Operationen hinzugefügt, um Abstürze des Add-ons zu verhindern, wenn die Systemzwischenablage vorübergehend durch andere Anwendungen gesperrt ist.
- **Timing-Optimierung:** Interne Verzögerungen für Tastaturereignisse wurden angepasst, um eine höhere Zuverlässigkeit bei unterschiedlichen Systemgeschwindigkeiten und eine bessere Kompatibilität mit Zwischenablage-Managern von Drittanbietern zu gewährleisten.

## Änderungen in 5.5 (Das Automatisierungs-Update)

- **KI-Operator (Autonome Steuerung - Umschalt+A):** Dies ist das Herzstück von v5.5. KI Assistent pro hat sich von einem passiven Assistenten zu Ihrem persönlichen **KI-Operator** weiterentwickelt. Er beschreibt nicht mehr nur den Bildschirm – er übernimmt das Kommando.
  - _Wie es funktioniert:_ Sie können jetzt sprachliche oder schriftliche Anweisungen geben, um Ihren PC zu steuern. In einer völlig unzugänglichen Anwendung, in der Ihr Screenreader stumm bleibt, können Sie beispielsweise **Umschalt+A** drücken und eingeben: _„Klicke auf die Schaltfläche Einstellungen“_ oder _„Suche das Suchfeld, tippe 'Aktuelle Nachrichten' ein und drücke Enter.“_ Die KI identifiziert die Elemente visuell, bewegt die Maus und führt die Aufgabe für Sie aus.
  - _Leistungshinweis:_ Diese Funktion ist für **Gemini 3.0 Flash (Preview)** optimiert und liefert unglaublich schnelle und intelligente Antworten, die selbst mit komplexesten UI-Layouts umgehen können.
  - **⚠️ Warnung zur API-Nutzung:** Da der KI-Operator genau „sehen“ muss, was passiert, um präzise zu sein, sendet er bei jedem Schritt einen hochauflösenden Screenshot. Bitte beachten Sie, dass eine häufige Nutzung Ihr API-Kontingent viel schneller verbraucht als standardmäßige textbasierte Aufgaben.
- **Visueller UI-Explorer (E):** Müde davon, durch „unbenannte Schaltflächen“ zu navigieren? Drücken Sie **E**, um den UI-Explorer zu aktivieren. Die KI scannt das gesamte Fenster und erstellt eine Liste aller anklickbaren Elemente, die sie sieht – einschließlich Symbolen, Grafiken und Menüs. Wählen Sie einfach ein Element aus der Liste aus, und der KI-Operator klickt es für Sie an. Es ist wie eine „barrierefreie Schicht“ über jeder App.
- **Kontextabhängige smarte Datei-Aktion (F):** Die Taste „F“ wurde komplett überarbeitet. Sie geht nicht mehr pauschal davon aus, dass Sie nur OCR möchten. Wenn Sie eine einzelne Bilddatei auswählen, fragt sie nun intelligent nach Ihrer Absicht: Sie können eine **Detaillierte visuelle Beschreibung** wählen, um die Szene zu verstehen, oder eine **Strukturierte Textextraktion (OCR)** zum Lesen. Das Menü passt sich dynamisch an den Dateityp und Ihre aktive KI-Engine an.
- **Kernoptimierung:** Wir haben die interne Logik des Add-ons gründlich bereinigt, ungenutzte Legacy-Funktionen und redundanten Code entfernt. Dies führt zu einer schlankeren, schnelleren und zuverlässigeren Benutzererfahrung für alle.

## Änderungen in 5.0

- **Multi-Anbieter-Architektur**: Volle Unterstützung für **OpenAI**, **Groq** und **Mistral** neben Google Gemini hinzugefügt. Benutzer können nun ihr bevorzugtes KI-Backend wählen.
- **Erweitertes Modell-Routing**: Benutzer nativer Anbieter (Gemini, OpenAI etc.) können nun spezifische Modelle für verschiedene Aufgaben (OCR, STT, TTS) aus einer Liste wählen.
- **Erweiterte Endpunkt-Konfiguration**: Benutzerdefinierte Anbieter können URLs und Modellnamen manuell eingeben, um die volle Kontrolle über lokale oder Drittanbieter-Server zu haben.
- **Intelligente Sichtbarkeit von Funktionen**: Das Einstellungsmenü und die Benutzeroberfläche des Dokumentenlesers blenden nicht unterstützte Funktionen (wie TTS) basierend auf dem gewählten Anbieter automatisch aus.
- **Dynamisches Abrufen von Modellen**: Das Add-on ruft die Liste der verfügbaren Modelle nun direkt über die API des Anbieters ab, um Kompatibilität mit neuen Modellen sofort nach deren Erscheinen sicherzustellen.
- **Hybrid-OCR & Übersetzung**: Die Logik wurde optimiert, um Google Translate für Geschwindigkeit bei Chrome-OCR zu nutzen und KI-basierte Übersetzung bei Gemini/Groq/OpenAI-Engines zu verwenden.
- **Universelles "Erneuter Scan mit KI"**: Die Re-Scan-Funktion des Dokumentenlesers ist nicht mehr auf Gemini beschränkt. Sie nutzt nun den jeweils aktiven KI-Anbieter zur Neuverarbeitung von Seiten.

## Änderungen in 4.6

- **Interaktives Abrufen von Ergebnissen:** Die **Leertaste** wurde zur Befehlsebene hinzugefügt, wodurch Benutzer die letzte KI-Antwort sofort in einem Chat-Fenster für Folgefragen öffnen können, auch wenn der Modus "Direkte Ausgabe" aktiv ist.
- **Telegram Community-Hub:** Link zum "Offiziellen Telegram-Kanal" im NVDA-Werkzeuge-Menü hinzugefügt.
- **Erhöhte Antwortstabilität:** Kernlogik für Übersetzung, OCR und Vision optimiert, um eine zuverlässigere Leistung bei direkter Sprachausgabe zu gewährleisten.
- **Verbesserte Benutzerführung:** Beschreibungen in den Einstellungen aktualisiert, um das neue Abrufsystem besser zu erklären.

## Änderungen in 4.5

- **Erweiterter Prompt-Manager:** Separater Verwaltungsdialog in den Einstellungen zum Anpassen von System-Prompts und Verwalten benutzerdefinierter Prompts (Hinzufügen, Bearbeiten, Sortieren, Vorschau).
- **Umfassende Proxy-Unterstützung:** Sichergestellt, dass Proxy-Einstellungen strikt auf alle API-Anfragen angewendet werden.
- **Automatisierte Datenmigration:** System zur automatischen Aktualisierung alter Prompt-Konfigurationen auf das v2 JSON-Format beim ersten Start.
- **Aktualisierte Kompatibilität (2025.1):** Erforderliche Mindestversion von NVDA auf 2025.1 gesetzt.
- **Optimierte Benutzeroberfläche:** Bereinigung der Einstellungen durch Auslagerung der Prompt-Verwaltung in einen eigenen Dialog.
- **Leitfaden für Prompt-Variablen:** Integrierter Leitfaden in den Prompt-Dialogen zur Verwendung von Variablen wie [selection], [clipboard] und [screen_obj].

## Änderungen in 4.0.3

- **Verbesserte Netzwerk-Resilienz:** Automatischer Wiederholungsmechanismus bei instabilen Verbindungen hinzugefügt.
- **Visual Translation Dialog:** Introduced a dedicated window for translation results. Users can now easily navigate and read long translations line-by-line, similar to OCR results.
- **Aggregierte formatierte Ansicht:** Die Funktion "Formatiert anzeigen" im Dokumentenleser zeigt nun alle verarbeiteten Seiten in einem einzigen, organisierten Fenster an.
- **Optimierter OCR-Workflow:** Überspringt die Seitenbereichsauswahl bei einseitigen Dokumenten automatisch.
- **Verbesserte API-Stabilität:** Umstellung auf Header-basierte Authentifizierung zur Vermeidung von Fehlern bei der Schlüsselrotation.
- **Bug Fixes:** Resolved several potential crashes, including an issue during add-on termination and a focus error in the chat dialog.

## Änderungen in 4.0.1

- **Fortgeschrittener Dokumentenleser:** Neuer Viewer für PDF und Bilder mit Seitenbereichsauswahl und Hintergrundverarbeitung.
- **Neues Werkzeuge-Untermenü:** Untermenü "KI Assistent" unter NVDA-Werkzeuge für schnelleren Zugriff hinzugefügt.
- **Flexible Anpassung:** OCR-Engine und TTS-Stimme direkt in den Einstellungen wählbar.
- **API-Schlüssel:** Erforderlich. Sie können mehrere Schlüssel eingeben (getrennt durch Kommas oder neue Zeilen), um eine automatische Rotation zu ermöglichen.
- **Alternative OCR-Engine:** Neue Engine zur Texterkennung hinzugefügt, falls das Gemini-Kontingent erschöpft ist.
- **Unterstützung mehrerer API-Schlüssel:** Unterstützung für mehrere Gemini-Schlüssel (einer pro Zeile oder durch Komma getrennt).
- **Dokument zu MP3/WAV:** Fähigkeit zur Erzeugung hochwertiger Audiodateien direkt im Reader integriert.
- **Instagram Stories & TikTok Support:** Analyse von Stories und TikTok-Videos über deren URLs hinzugefügt.
- **Gemini Live TTS für Videobeschreibungen:** Gemini Live TTS kann nun als Stimme für synchronisierte Sprachausgaben (MP3) gewählt werden, um unbegrenzte und hochwertige Beschreibungen ohne Längenbeschränkung zu generieren.
- **Redesigned Update Dialog:** Features a new accessible interface with a scrollable text box to clearly read version changes before installing.
- **Unified Status & UX:** Standardized file dialogs across the add-on and enhanced the 'L' command to report real-time progress.

## Änderungen in 3.6.0

- **Hilfesystem:** Hilfe-Befehl (`H`) innerhalb der Befehlsebene hinzugefügt.
- **Online Video Analysis:** Expanded support to include **Twitter (X)** videos. Also improved URL detection and stability for a more reliable experience.
- **Project Contribution:** Added an optional donation dialog for users who wish to support the project’s future updates and continuous growth.

## Änderungen in 3.5.0

**Einzeltaste** (z. B. `1`, `p` oder `F3`): Funktioniert innerhalb der Befehlsebene und global als `NVDA + Umschalt + Taste`. For example, instead of pressing `NVDA+Control+Shift+T` for translation, you now press `NVDA+Shift+V` followed by `T`.
\*   \*\*Online Video Analysis:\*\* Added a new feature to analyze YouTube and Instagram videos directly by providing a URL.

## Änderungen in 3.1.0

- **Direkter Ausgabemodus:** Option zum Überspringen des Chat-Dialogs, um KI-Antworten sofort per Sprache zu hören.
- **Zwischenablage-Integration:** Einstellung zum automatischen Kopieren von KI-Antworten in die Zwischenablage.

## Änderungen in 3.0

- **Neue Sprachen:** Persisch und Vietnamesisch hinzugefügt.
- **Erweiterte KI-Modelle:** Modellliste mit Präfixen (`[Free]`, `[Pro]`, `[Auto]`) neu organisiert. Unterstützung für **Gemini 3.0 Pro** und **Gemini 2.0 Flash Lite**.
- **Dictation Stability:** Significantly improved Smart Dictation stability. Added a safety check to ignore audio clips shorter than 1 second, preventing AI hallucinations and empty errors.
- **Dateihandhabung:** Fehler beim Hochladen von Dateien mit nicht-englischen Namen behoben.
- **Prompt Optimization:** Improved Translation logic and structured Vision results.

## Änderungen in 2.9

- **Französische und türkische Übersetzungen hinzugefügt.**
- **Formatierte Ansicht:** Schaltfläche "Formatiert anzeigen" in Chat-Dialogen hinzugefügt (Überschriften, Fettdruck, Code).
- **Markdown Setting:** Added a new option "Clean Markdown in Chat" in Settings. Unchecking this allows users to see raw Markdown syntax (e.g., `**`, `#`) in the chat window.
- **Dialog Management:** Fixed an issue where the "Refine Text" or chat windows would open multiple times or fail to focus correctly.
- **UX Improvements:** Standardized file dialog titles to "Open" and removed redundant speech announcements (e.g., "Opening menu...") for a smoother experience.

## Änderungen in 2.8

- Italienische Übersetzung hinzugefügt.
- **Statusbericht:** Neuer Befehl (NVDA+Strg+Umschalt+I) zum Ansagen des aktuellen Status.
- **HTML-Export:** Speichern-Schaltfläche exportiert nun als formatiertes HTML.
- **Settings UI:** Improved the Settings panel layout with accessible grouping.
- **New Models:** Added support for gemini-flash-latest and gemini-flash-lite-latest.
- **Sprachen:** Nepali hinzugefügt.
- **Refine Menu Logic:** Fixed a critical bug where "Refine Text" commands would fail if the NVDA interface language was not English.
- **Dictation:** Improved silence detection to prevent incorrect text output when no speech is input.
- **Update Settings:** "Check for updates on startup" is now disabled by default to comply with Add-on Store policies.
- Code Cleanup.

## Änderungen in 2.7

- Projektstruktur auf die offizielle NV Access Vorlage migriert.
- Automatisches Retry bei HTTP 429 (Rate Limit) Fehlern.
- Optimized translation prompts for higher accuracy and better "Smart Swap" logic handling.
- Optimierte Übersetzungs-Prompts.

## Änderungen in 2.6

- Russische Übersetzung hinzugefügt.
- Updated error messages to provide more descriptive feedback regarding connectivity.
- Standard-Zielsprache auf Englisch geändert.

## Änderungen in 2.5

- Native Datei-OCR (NVDA+Strg+Umschalt+F) hinzugefügt.
- "Chat speichern" Schaltfläche hinzugefügt.
- Implemented full localization support (i18n).
- Migrated audio feedback to NVDA's native tones module.
- Umstellung auf Gemini File API für bessere PDF- und Audio-Handhabung.
- Fixed crash when translating text containing curly braces.

## 1.3 KI-Verhalten Reiter

- Fixed an issue where the [file_ocr] variable was not functioning correctly within Custom Prompts.

## Änderungen in 2.1

- Standardisierung aller Kürzel auf NVDA+Strg+Umschalt, um Konflikte mit dem Laptop-Layout zu vermeiden.

## Änderungen in 2.0

- Integriertes Auto-Update-System.
- Intelligenter Übersetzungscache hinzugefügt.
- Konversationsgedächtnis für Kontext im Chat hinzugefügt.
- Separater Befehl für Zwischenablage-Übersetzung (NVDA+Strg+Umschalt+Y).
- Optimized AI prompts to strictly enforce target language output.
- Fixed crash caused by special characters in input text.

## Änderungen in 1.5

- Unterstützung für über 20 neue Sprachen.
- Interaktiver Optimierungs-Dialog für Folgefragen.
- Native "Intelligentes Diktat" Funktion.
- Added "Vision Assistant" category to NVDA's Input Gestures dialog.
- Fixed COMError crashes in specific applications like Firefox and Word.
- Added automatic retry mechanism for server errors.

## Änderungen in 1.0

- Erstveröffentlichung.
