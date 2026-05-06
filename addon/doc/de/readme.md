# KI Assistent pro Dokumentation

**KI Assistent pro** ist ein fortschrittlicher, multimodaler KI-Assistent für NVDA. Er nutzt erstklassige KI-Engines, um intelligentes Screenreading, Übersetzungen, Sprachdiktate und Dokumentenanalysen zu ermöglichen.

_Dieses Add-on wurde zu Ehren des Internationalen Tages der Menschen mit Behinderungen für die Community veröffentlicht._

## 1. Einrichtung & Konfiguration

Gehen Sie zu **NVDA-Menü > Optionen > Einstellungen > KI Assistent pro**.

### 1.1 Verbindungseinstellungen
- **Anbieter:** Wählen Sie Ihren bevorzugten KI-Dienst. Unterstützte Anbieter sind **Google Gemini**, **OpenAI**, **Mistral**, **Groq** und **Benutzerdefiniert** (OpenAI-kompatible Server wie Ollama/LM Studio).
- **Wichtiger Hinweis:** Wir empfehlen dringend die Verwendung von **Google Gemini** für die beste Leistung und Genauigkeit (insbesondere bei der Bild-/Dateianalyse).
- **API-Schlüssel:** Erforderlich. Sie können mehrere Schlüssel eingeben (getrennt durch Kommas oder neue Zeilen), um eine automatische Rotation zu ermöglichen.
- **Modelle abrufen:** Nachdem Sie Ihren API-Schlüssel eingegeben haben, drücken Sie diese Schaltfläche, um die aktuelle Liste der verfügbaren Modelle vom Anbieter herunterzuladen.
- **KI-Modell:** Wählen Sie das Hauptmodell aus, das für den allgemeinen Chat und die Analysen verwendet werden soll.

### 1.2 Erweitertes Modell-Routing (Native Anbieter)
*Verfügbar für Gemini, OpenAI, Groq und Mistral.*

> **⚠️ Warnung:** Diese Einstellungen sind **nur für fortgeschrittene Benutzer** gedacht. Wenn Sie sich unsicher sind, was ein bestimmtes Modell bewirkt, lassen Sie dies bitte **deaktiviert**. Die Auswahl eines inkompatiblen Modells für eine Aufgabe (z. B. ein reines Textmodell für Vision-Aufgaben) führt zu Fehlern und stoppt die Funktion des Add-ons.

Aktivieren Sie **"Erweitertes Modell-Routing (Aufgabenspezifisch)"**, um detaillierte Steuerungsmöglichkeiten freizuschalten. Dies ermöglicht es Ihnen, spezifische Modelle aus der Dropdown-Liste für verschiedene Aufgaben auszuwählen:
- **OCR / Vision-Modell:** Wählen Sie ein spezialisiertes Modell für die Analyse von Bildern.
- **Speech-to-Text (STT):** Wählen Sie ein spezifisches Modell für das Diktat.
- **Text-to-Speech (TTS):** Wählen Sie ein Modell zur Generierung von Audio.
*Hinweis: Nicht unterstützte Funktionen (z. B. TTS für Groq) werden automatisch ausgeblendet.*

### 1.3 Erweiterte Endpunkt-Konfiguration (Benutzerdefinierter Anbieter)
*Nur verfügbar, wenn "Benutzerdefiniert" ausgewählt ist.*

> **Warnung:** Dieser Abschnitt ermöglicht die manuelle API-Konfiguration und ist für **Power-User** konzipiert, die lokale Server oder Proxys betreiben. Falsche URLs oder Modellnamen unterbrechen die Konnektivität. Wenn Sie nicht genau wissen, was diese Endpunkte sind, lassen Sie dies **deaktiviert**.

Aktivieren Sie **"Erweiterte Endpunkt-Konfiguration"**, um Serverdetails manuell einzugeben. Im Gegensatz zu nativen Anbietern müssen Sie hier die spezifischen URLs und Modellnamen **tippen**:
- **Modelllisten-URL:** Der Endpunkt zum Abrufen verfügbarer Modelle.
- **OCR/STT/TTS Endpunkt-URL:** Vollständige URLs für spezifische Dienste (z. B. `http://localhost:11434/v1/audio/speech`).
- **Benutzerdefinierte Modelle:** Geben Sie den Modellnamen (z. B. `llama3:8b`) für jede Aufgabe manuell ein.

### 1.4 Allgemeine Einstellungen
- **OCR-Engine:** Wählen Sie zwischen **Chrome (Schnell)** für schnelle Ergebnisse oder **Gemini (Formatiert)** für eine überlegene Beibehaltung des Layouts.
    - *Hinweis:* Wenn Sie "Gemini (Formatiert)" wählen, Ihr Anbieter aber auf OpenAI/Groq eingestellt ist, leitet das Add-on das Bild intelligent an das Vision-Modell Ihres aktiven Anbieters weiter.
- **TTS-Stimme:** Wählen Sie Ihren bevorzugten Stimmenstil. Diese Liste wird dynamisch basierend auf Ihrem aktiven Anbieter aktualisiert.
- **Kreativität (Temperatur):** Steuert die Zufälligkeit der KI. Niedrigere Werte sind besser für genaue Übersetzungen/OCR.
- **Proxy-URL:** Konfigurieren Sie dies, falls KI-Dienste in Ihrer Region eingeschränkt sind (unterstützt lokale Proxys wie `127.0.0.1` oder Bridge-URLs).

## 2. Befehlsebene & Tastenkombinationen

Um Tastaturkonflikte zu vermeiden, verwendet dieses Add-on eine **Befehlsebene**.
1. Drücken Sie **NVDA + Umschalt + V** (Haupttaste), um die Ebene zu aktivieren (Sie hören einen Signalton).
2. Lassen Sie die Tasten los und drücken Sie dann eine der folgenden Einzeltasten:

| Taste           | Funktion                 | Beschreibung                                                                 |
|---------------|--------------------------|-----------------------------------------------------------------------------|
| **T**         | Intelligenter Übersetzer  | Übersetzt Text unter dem Navigator-Objekt oder der Markierung.               |
| **Umschalt+T** | Zwischenablage-Übersetzer | Übersetzt den aktuellen Inhalt der Zwischenablage.                           |
| **R**         | Text-Optimierer          | Zusammenfassen, Grammatik korrigieren, Erklären oder **Eigene Prompts**.     |
| **V**         | Objekt-Vision            | Beschreibt das aktuelle Navigator-Objekt.                                    |
| **O**         | Vollbild-Vision          | Analysiert das gesamte Bildschirmlayout und den Inhalt.                      |
| **Umschalt+V** | Online-Videoanalyse      | Analysiert **YouTube**, **Instagram**, **TikTok** oder **Twitter (X)** Videos.|
| **D**         | Dokumentenleser          | Fortgeschrittener Leser für PDF und Bilder mit Seitenbereichsauswahl.        |
| **F**         | Datei-OCR                | Direkte Texterkennung aus ausgewählten Bild-, PDF- oder TIFF-Dateien.        |
| **A**         | Audio-Transkription      | Transkribiert MP3-, WAV- oder OGG-Dateien in Text.                           |
| **C**         | CAPTCHA-Löser            | Erfasst und löst CAPTCHAs (Unterstützt Regierungsportale).                   |
| **S**         | Intelligentes Diktat     | Wandelt Sprache in Text um. Drücken zum Starten, erneut drücken zum Stoppen. |
| **L**         | Statusbericht            | Meldet den aktuellen Fortschritt (z. B. "Scannen...", "Bereit").              |
| **U**         | Update-Prüfung           | Prüft manuell auf GitHub nach der neuesten Version des Add-ons.              |
| **Leertaste** | Letztes Ergebnis abrufen | Zeigt die letzte KI-Antwort in einem Chat-Dialog zur Überprüfung an.         |
| **H**         | Befehlshilfe             | Zeigt eine Liste aller verfügbaren Kürzel innerhalb der Befehlsebene an.     |

### 2.1 Tastenkombinationen im Dokumentenleser (Innerhalb des Viewers)
- **Strg + BildAb:** Zur nächsten Seite wechseln.
- **Strg + BildAuf:** Zur vorherigen Seite wechseln.
- **Alt + A:** Öffnet einen Chat-Dialog, um Fragen zum Dokument zu stellen.
- **Alt + R:** Erzwingt einen **erneuten Scan mit KI** über Ihren aktiven Anbieter.
- **Alt + G:** Erzeugt und speichert eine hochwertige Audiodatei (WAV/MP3). *Ausgeblendet, wenn der Anbieter kein TTS unterstützt.*
- **Alt + S / Strg + S:** Speichert den extrahierten Text als TXT- oder HTML-Datei.

## 3. Eigene Prompts & Variablen

Sie können Prompts unter **Einstellungen > Prompts > Prompts verwalten...** verwalten.

### Unterstützte Variablen
- `[selection]`: Aktuell markierter Text.
- `[clipboard]`: Inhalt der Zwischenablage.
- `[screen_obj]`: Screenshot des Navigator-Objekts.
- `[screen_full]`: Vollbild-Screenshot.
- `[file_ocr]`: Bild-/PDF-Datei für Textextraktion auswählen.
- `[file_read]`: Dokument zum Lesen auswählen (TXT, Code, PDF).
- `[file_audio]`: Audiodatei zur Analyse auswählen (MP3, WAV, OGG).

***
**Hinweis:** Für alle KI-Funktionen ist eine aktive Internetverbindung erforderlich. Mehrseitige Dokumente werden automatisch verarbeitet.

## 4. Support & Community

Bleiben Sie auf dem Laufenden über Neuigkeiten, Funktionen und Veröffentlichungen:
- **Telegram-Kanal:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Für Fehlermeldungen und Funktionsanfragen.

## Änderungen in 5.0

* **Multi-Anbieter-Architektur**: Volle Unterstützung für **OpenAI**, **Groq** und **Mistral** neben Google Gemini hinzugefügt. Benutzer können nun ihr bevorzugtes KI-Backend wählen.
* **Erweitertes Modell-Routing**: Benutzer nativer Anbieter (Gemini, OpenAI etc.) können nun spezifische Modelle für verschiedene Aufgaben (OCR, STT, TTS) aus einer Liste wählen.
* **Erweiterte Endpunkt-Konfiguration**: Benutzerdefinierte Anbieter können URLs und Modellnamen manuell eingeben, um die volle Kontrolle über lokale oder Drittanbieter-Server zu haben.
* **Intelligente Sichtbarkeit von Funktionen**: Das Einstellungsmenü und die Benutzeroberfläche des Dokumentenlesers blenden nicht unterstützte Funktionen (wie TTS) basierend auf dem gewählten Anbieter automatisch aus.
* **Dynamisches Abrufen von Modellen**: Das Add-on ruft die Liste der verfügbaren Modelle nun direkt über die API des Anbieters ab, um Kompatibilität mit neuen Modellen sofort nach deren Erscheinen sicherzustellen.
* **Hybrid-OCR & Übersetzung**: Die Logik wurde optimiert, um Google Translate für Geschwindigkeit bei Chrome-OCR zu nutzen und KI-basierte Übersetzung bei Gemini/Groq/OpenAI-Engines zu verwenden.
* **Universelles "Erneuter Scan mit KI"**: Die Re-Scan-Funktion des Dokumentenlesers ist nicht mehr auf Gemini beschränkt. Sie nutzt nun den jeweils aktiven KI-Anbieter zur Neuverarbeitung von Seiten.

## Änderungen in 4.6
* **Interaktives Abrufen von Ergebnissen:** Die **Leertaste** wurde zur Befehlsebene hinzugefügt, wodurch Benutzer die letzte KI-Antwort sofort in einem Chat-Fenster für Folgefragen öffnen können, auch wenn der Modus "Direkte Ausgabe" aktiv ist.
* **Telegram Community-Hub:** Link zum "Offiziellen Telegram-Kanal" im NVDA-Werkzeuge-Menü hinzugefügt.
* **Erhöhte Antwortstabilität:** Kernlogik für Übersetzung, OCR und Vision optimiert, um eine zuverlässigere Leistung bei direkter Sprachausgabe zu gewährleisten.
* **Verbesserte Benutzerführung:** Beschreibungen in den Einstellungen aktualisiert, um das neue Abrufsystem besser zu erklären.

## Änderungen in 4.5
* **Erweiterter Prompt-Manager:** Separater Verwaltungsdialog in den Einstellungen zum Anpassen von System-Prompts und Verwalten benutzerdefinierter Prompts (Hinzufügen, Bearbeiten, Sortieren, Vorschau).
* **Umfassende Proxy-Unterstützung:** Sichergestellt, dass Proxy-Einstellungen strikt auf alle API-Anfragen angewendet werden.
* **Automatisierte Datenmigration:** System zur automatischen Aktualisierung alter Prompt-Konfigurationen auf das v2 JSON-Format beim ersten Start.
* **Aktualisierte Kompatibilität (2025.1):** Erforderliche Mindestversion von NVDA auf 2025.1 gesetzt.
* **Optimierte Benutzeroberfläche:** Bereinigung der Einstellungen durch Auslagerung der Prompt-Verwaltung in einen eigenen Dialog.
* **Leitfaden für Prompt-Variablen:** Integrierter Leitfaden in den Prompt-Dialogen zur Verwendung von Variablen wie [selection], [clipboard] und [screen_obj].

## Änderungen in 4.0.3
*   **Verbesserte Netzwerk-Resilienz:** Automatischer Wiederholungsmechanismus bei instabilen Verbindungen hinzugefügt.
*   **Visueller Übersetzungsdialog:** Neues Fenster für Übersetzungsergebnisse, das zeilenweises Lesen langer Texte ermöglicht.
*   **Aggregierte formatierte Ansicht:** Die Funktion "Formatiert anzeigen" im Dokumentenleser zeigt nun alle verarbeiteten Seiten in einem einzigen, organisierten Fenster an.
*   **Optimierter OCR-Workflow:** Überspringt die Seitenbereichsauswahl bei einseitigen Dokumenten automatisch.
*   **Verbesserte API-Stabilität:** Umstellung auf Header-basierte Authentifizierung zur Vermeidung von Fehlern bei der Schlüsselrotation.

## Änderungen in 4.0.1
*   **Fortgeschrittener Dokumentenleser:** Neuer Viewer für PDF und Bilder mit Seitenbereichsauswahl und Hintergrundverarbeitung.
*   **Neues Werkzeuge-Untermenü:** Untermenü "KI Assistent" unter NVDA-Werkzeuge für schnelleren Zugriff hinzugefügt.
*   **Flexible Anpassung:** OCR-Engine und TTS-Stimme direkt in den Einstellungen wählbar.
*   **Unterstützung mehrerer API-Schlüssel:** Unterstützung für mehrere Gemini-Schlüssel (einer pro Zeile oder durch Komma getrennt).
*   **Alternative OCR-Engine:** Neue Engine zur Texterkennung hinzugefügt, falls das Gemini-Kontingent erschöpft ist.
*   **Dokument zu MP3/WAV:** Fähigkeit zur Erzeugung hochwertiger Audiodateien direkt im Reader integriert.
*   **Instagram Stories & TikTok Support:** Analyse von Stories und TikTok-Videos über deren URLs hinzugefügt.

## Änderungen in 3.6.0
*   **Hilfesystem:** Hilfe-Befehl (`H`) innerhalb der Befehlsebene hinzugefügt.
*   **Online-Videoanalyse:** Unterstützung für **Twitter (X)** Videos hinzugefügt sowie URL-Erkennung verbessert.

## Änderungen in 3.5.0
*   **Befehlsebene:** Einführung der Befehlsebene (Standard: `NVDA+Umschalt+V`), um Kürzel unter einer Haupttaste zu gruppieren.
*   **Online-Videoanalyse:** Neue Funktion zur Analyse von YouTube- und Instagram-Videos per URL.

## Änderungen in 3.1.0
*   **Direkter Ausgabemodus:** Option zum Überspringen des Chat-Dialogs, um KI-Antworten sofort per Sprache zu hören.
*   **Zwischenablage-Integration:** Einstellung zum automatischen Kopieren von KI-Antworten in die Zwischenablage.

## Änderungen in 3.0
*   **Neue Sprachen:** Persisch und Vietnamesisch hinzugefügt.
*   **Erweiterte KI-Modelle:** Modellliste mit Präfixen (`[Free]`, `[Pro]`, `[Auto]`) neu organisiert. Unterstützung für **Gemini 3.0 Pro** und **Gemini 2.0 Flash Lite**.
*   **Diktat-Stabilität:** Ignoriert nun Audioclips unter 1 Sekunde, um Halluzinationen zu vermeiden.
*   **Dateihandlung:** Fehler beim Hochladen von Dateien mit nicht-englischen Namen behoben.

## Änderungen in 2.9
*   **Französische und türkische Übersetzungen hinzugefügt.**
*   **Formatierte Ansicht:** Schaltfläche "Formatiert anzeigen" in Chat-Dialogen hinzugefügt (Überschriften, Fettdruck, Code).
*   **Markdown-Einstellung:** Option "Bereinigtes Markdown im Chat" hinzugefügt.

## Änderungen in 2.8
*   Italienische Übersetzung hinzugefügt.
*   **Statusbericht:** Neuer Befehl (NVDA+Strg+Umschalt+I) zum Ansagen des aktuellen Status.
*   **HTML-Export:** Speichern-Schaltfläche exportiert nun als formatiertes HTML.
*   **Sprachen:** Nepali hinzugefügt.

## Änderungen in 2.7
*   Projektstruktur auf die offizielle NV Access Vorlage migriert.
*   Automatisches Retry bei HTTP 429 (Rate Limit) Fehlern.
*   Optimierte Übersetzungs-Prompts.

## Änderungen in 2.6
*   Russische Übersetzung hinzugefügt.
*   Standard-Zielsprache auf Englisch geändert.

## Änderungen in 2.5
*   Native Datei-OCR (NVDA+Strg+Umschalt+F) hinzugefügt.
*   "Chat speichern" Schaltfläche hinzugefügt.
*   Umstellung auf Gemini File API für bessere PDF- und Audio-Handhabung.

## Änderungen in 2.1
*   Standardisierung aller Kürzel auf NVDA+Strg+Umschalt, um Konflikte mit dem Laptop-Layout zu vermeiden.

## Änderungen in 2.0
*   Integriertes Auto-Update-System.
*   Intelligenter Übersetzungscache hinzugefügt.
*   Konversationsgedächtnis für Kontext im Chat hinzugefügt.
*   Separater Befehl für Zwischenablage-Übersetzung (NVDA+Strg+Umschalt+Y).

## Änderungen in 1.5
*   Unterstützung für über 20 neue Sprachen.
*   Interaktiver Optimierungs-Dialog für Folgefragen.
*   Native "Intelligentes Diktat" Funktion.

## Änderungen in 1.0
*   Erstveröffentlichung.

## Übersetzung
* Übersetzt von **BFW Würzburg** im Rahmen des Projekts "NVDA Nachhaltig"