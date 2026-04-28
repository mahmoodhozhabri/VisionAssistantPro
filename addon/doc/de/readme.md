# Dokumentation für KI Assistent Pro

**KI Assistent Pro** ist ein fortschrittlicher, multimodaler KI-Assistent für NVDA. Er nutzt Googles Gemini-Modelle, um intelligente Bildschirmlese-, Übersetzungs-, Sprachdiktat- und Dokumentenanalyse-Funktionen bereitzustellen.

*Dieses Add-on wurde zu Ehren des Internationalen Tages der Menschen mit Behinderungen für die Community veröffentlicht.*

## 1. Einrichtung & Konfiguration

Gehen Sie zu **NVDA-Menü > Optionen > Einstellungen > KI Assistent Pro**.

* **API-Key:** Erforderlich. Sie können mehrere Keys eingeben (getrennt durch Kommas oder Zeilenumbrüche). Der Assistent rotiert automatisch zwischen ihnen, wenn ein Kontingentlimit erreicht ist.
* **KI-Modell:** Wählen Sie zwischen den Modellen **Flash** (schnellste/kostenlos), **Lite** oder **Pro** (hohe Intelligenz).
* **Proxy-URL:** Optional. Verwenden Sie diese, falls Google in Ihrer Region blockiert ist. Es muss eine Webadresse sein, die als Brücke zur Gemini-API fungiert.
* **OCR-Modell:** Wählen Sie zwischen **Chrome (Schnell)** für schnelle Ergebnisse oder **Gemini (Formatiert)** für überlegene Layouterhaltung und Tabellenerkennung.
* **TTS-Stimme:** Wählen Sie den bevorzugten Sprachstil für die Erstellung von Audiodateien aus Dokumentenseiten.
* **Intelligenter Tausch:** Tauscht automatisch die Sprachen, wenn der Quelltext der Zielsprache entspricht.
* **Direkte Ausgabe:** Überspringt das Chat-Fenster und kündigt die KI-Antwort direkt per Sprache an. **Hinweis:** Auch in diesem Modus können Sie die **Leertaste** innerhalb der Befehlsebene drücken, um das letzte Ergebnis in einem Chat-Dialog erneut zu öffnen.
* **Zwischenablage-Integration:** Kopiert die KI-Antwort automatisch in die Zwischenablage.

## 2. Befehlsebene & Tastenkombinationen

Um Tastaturkonflikte zu vermeiden, verwendet dieses Add-on eine **Befehlsebene**.

1. Drücken Sie **NVDA + Umschalt + V** (Master-Taste), um die Ebene zu aktivieren (Sie hören einen Piepton).
2. Lassen Sie die Tasten los und drücken Sie dann eine der folgenden einzelnen Tasten:

| Taste | Funktion | Beschreibung |
| --- | --- | --- |
| **T** | Intelligenter Übersetzer | Übersetzt Text unter dem Navigator-Cursor oder der Markierung. |
| **Umschalt + T** | Ablage-Übersetzer | Übersetzt den Inhalt, der sich aktuell in der Zwischenablage befindet. |
| **R** | Text-Optimierer | Zusammenfassen, Grammatik korrigieren, Erklären oder **Eigene Prompts** ausführen. |
| **V** | Objekt-Erkennung | Beschreibt das aktuelle Navigator-Objekt. |
| **O** | Vollbild-Analyse | Analysiert das gesamte Bildschirmlayout und den Inhalt. |
| **Umschalt + V** | Online-Videoanalyse | Analysiert **YouTube**, **Instagram**, **TikTok** oder **Twitter (X)** Videos. |
| **D** | Dokumentenleser | Fortschrittlicher Leser für PDF und Bilder mit Seitenbereichsauswahl. |
| **F** | Datei-OCR | Direkte Texterkennung aus ausgewählten Bild-, PDF- oder TIFF-Dateien. |
| **A** | Transkription | Transkribiert MP3-, WAV- oder OGG-Dateien in Text. |
| **C** | CAPTCHA-Löser | Erfasst und löst CAPTCHAs auf dem Bildschirm oder Navigator-Objekt. |
| **S** | Intelligentes Diktat | Wandelt Sprache in Text um. Drücken zum Starten, erneut zum Stoppen/Tippen. |
| **L** | Statusbericht | Meldet den aktuellen Fortschritt (z. B. „Scannen...“, „Bereit“). |
| **U** | Update-Check | Prüft manuell auf GitHub nach der neuesten Version des Add-ons. |
| **Leertaste** | Letztes Ergebnis | Zeigt die letzte KI-Antwort für Rückfragen erneut in einem Dialog an. |
| **H** | Befehlshilfe | Zeigt eine Liste aller verfügbaren Kürzel innerhalb der Befehlsebene an. |

### 2.1 Tastenkürzel im Dokumentenleser (Innerhalb des Betrachters)

Sobald ein Dokument über den **D**-Befehl geöffnet wurde:

* **Strg + Bild ab:** Zur nächsten Seite wechseln (kündigt Seitenzahl an).
* **Strg + Bild auf:** Zur vorherigen Seite wechseln (kündigt Seitenzahl an).
* **Alt + A:** Öffnet einen Chat-Dialog, um Fragen zum Dokument zu stellen.
* **Alt + R:** Erneutes Scannen der aktuellen oder aller Seiten mit der Gemini-Engine erzwingen.
* **Alt + G:** Erstellt und speichert eine hochwertige Audiodatei (WAV) des Inhalts.
* **Alt + S / Strg + S:** Speichert den extrahierten Text als TXT- oder HTML-Datei.

---

## 3. Eigene Prompts & Variablen

Öffnen Sie **Optionen > Einstellungen > KI Assistent Pro > Prompts verwalten...**, um System- und benutzerdefinierte Prompts zu konfigurieren.

* **Tab Standard-Prompts:** Bearbeiten Sie integrierte Prompts. Sie können einzelne Prompts oder alle Standards zurücksetzen.
* **Tab Eigene Prompts:** Hinzufügen, Bearbeiten, Entfernen und Neuanordnen benutzerdefinierter Prompts.
* **Schaltfläche Variablen-Helfer:** Öffnet ein Hilfefenster mit allen unterstützten Variablen und Eingabetypen.

### Verfügbare Variablen

| Variable | Beschreibung | Eingabetyp |
| --- | --- | --- |
| `[selection]` | Aktuell markierter Text | Text |
| `[clipboard]` | Inhalt der Zwischenablage | Text |
| `[screen_obj]` | Screenshot des Navigator-Objekts | Bild |
| `[screen_full]` | Vollständiger Screenshot | Bild |
| `[file_ocr]` | Bild-/PDF-Datei für Textextraktion wählen | Bild, PDF, TIFF |
| `[file_read]` | Dokument zum Lesen auswählen | TXT, Code, PDF |
| `[file_audio]` | Audiodatei zur Analyse auswählen | MP3, WAV, OGG |

### Beispiele für eigene Prompts

* **Schnell-OCR:** `Mein OCR:[file_ocr]`
* **Bild übersetzen:** `Bild übersetzen:Extrahiere Text aus diesem Bild und übersetze ihn ins Deutsche. [file_ocr]`
* **Audio analysieren:** `Audio zusammenfassen:Höre dir diese Aufnahme an und fasse die Hauptpunkte zusammen. [file_audio]`
* **Code-Debugger:** `Debug:Finde Fehler in diesem Code und erkläre sie: [selection]`

---

**Hinweis:** Für alle KI-Funktionen ist eine aktive Internetverbindung erforderlich. Mehrseitige Dokumente und TIFFs werden automatisch verarbeitet.

## 4. Support & Community

Bleiben Sie auf dem Laufenden mit den neuesten Nachrichten, Funktionen und Veröffentlichungen:

* **Telegram-Kanal:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
* **GitHub Issues:** Für Fehlerberichte und Funktionsanfragen.

---

## Änderungen in Version 4.6

* **Interaktiver Ergebnisaufruf:** Die **Leertaste** wurde zur Befehlsebene hinzugefügt, sodass Benutzer die letzte KI-Antwort sofort in einem Chat-Fenster für Folgefragen öffnen können, selbst wenn der Modus „Direkte Ausgabe“ aktiv ist.
* **Telegram Community Hub:** Link zum „Offiziellen Telegram-Kanal“ im NVDA-Werkzeuge-Menü hinzugefügt.
* **Verbesserte Antwortstabilität:** Die Kernlogik für Übersetzung, OCR und Vision wurde optimiert, um eine zuverlässigere Leistung und ein reibungsloseres Erlebnis bei der direkten Sprachausgabe zu gewährleisten.
* **Optimierte Benutzeroberflächen-Führung:** Die Beschreibungen in den Einstellungen und die Dokumentation wurden aktualisiert, um das neue Aufrufsystem und dessen Funktionsweise zusammen mit den Direktausgabe-Einstellungen besser zu erklären.

## Änderungen in Version 4.5

* **Fortschrittlicher Prompt-Manager:** Einführung eines speziellen Verwaltungsdialogs in den Einstellungen zur Anpassung von System-Prompts und zur Verwaltung benutzerdefinierter Prompts mit Unterstützung für Hinzufügen, Bearbeiten, Neuanordnen und Vorschau.
* **Umfassende Proxy-Unterstützung:** Netzwerkverbindungsprobleme wurden gelöst, indem sichergestellt wurde, dass benutzerdefinierte Proxy-Einstellungen strikt auf alle API-Anfragen (Übersetzung, OCR, Spracherzeugung) angewendet werden.
* **Automatisierte Datenmigration:** Integriertes System zur automatischen Aktualisierung alter Prompt-Konfigurationen in das robuste v2 JSON-Format beim ersten Start ohne Datenverlust.
* **Aktualisierte Kompatibilität (2025.1):** Die erforderliche Mindestversion von NVDA wurde aufgrund von Bibliotheksabhängigkeiten in erweiterten Funktionen wie dem Dokumentenleser auf 2025.1 gesetzt.
* **Optimierte Einstellungen-Oberfläche:** Die Benutzeroberfläche wurde durch die Auslagerung der Prompt-Verwaltung in einen separaten Dialog übersichtlicher und zugänglicher gestaltet.
* **Prompt-Variablen-Helfer:** Ein integrierter Guide in den Prompt-Dialogen hilft Benutzern, dynamische Variablen wie [selection], [clipboard] und [screen_obj] leicht zu identifizieren und zu nutzen.

## Änderungen in Version 4.0.3

* **Verbesserte Netzwerk-Resilienz:** Automatischer Wiederholungsmechanismus hinzugefügt, um instabile Internetverbindungen und temporäre Serverfehler besser zu handhaben.
* **Visueller Übersetzungsdialog:** Einführung eines speziellen Fensters für Übersetzungsergebnisse, in dem Benutzer lange Übersetzungen Zeile für Zeile navigieren können.
* **Aggregierte formatierte Ansicht:** Die Funktion „Formatiert anzeigen“ im Dokumentenleser zeigt nun alle verarbeiteten Seiten in einem einzigen Fenster mit klaren Seitenüberschriften an.
* **Optimierter OCR-Workflow:** Die Seitenbereichsauswahl wird bei einseitigen Dokumenten automatisch übersprungen.
* **Verbesserte API-Stabilität:** Wechsel zu einer robusteren Header-basierten Authentifizierungsmethode zur Vermeidung von Fehlern bei der Key-Rotation.
* **Fehlerbehebungen:** Behebung potenzieller Abstürze beim Beenden des Add-ons und eines Fokusfehlers im Chat-Dialog.

## Änderungen in Version 4.0.1

* **Fortschrittlicher Dokumentenleser:** Ein mächtiger neuer Viewer für PDFs und Bilder mit Seitenbereichsauswahl, Hintergrundverarbeitung und `Strg+BildAuf/Ab` Navigation.
* **Neues Werkzeuge-Untermenü:** Spezielles Untermenü „KI Assistent“ unter NVDA-Werkzeuge für schnelleren Zugriff hinzugefügt.
* **Flexible Anpassung:** OCR-Modell und TTS-Stimme können nun direkt in den Einstellungen gewählt werden.
* **Unterstützung mehrerer API-Keys:** Erlaubt die Eingabe mehrerer Gemini-Keys (einer pro Zeile oder durch Kommas getrennt).
* **Alternative OCR-Modelle:** Einführung eines neuen OCR-Modells für zuverlässige Erkennung bei Quota-Limits.
* **Intelligente API-Key-Rotation:** Automatischer Wechsel zum schnellsten funktionierenden Key.
* **Dokument zu MP3/WAV:** Integration der Erstellung hochwertiger Audiodateien (MP3 128kbps und WAV) direkt im Reader.
* **Instagram-Stories Unterstützung:** Analyse von Instagram-Stories via URL möglich.
* **TikTok Unterstützung:** Analyse und Transkription von TikTok-Videos hinzugefügt.
* **Überarbeiteter Update-Dialog:** Barrierefreie Oberfläche mit scrollbarem Textfeld zum Lesen der Änderungen vor der Installation.
* **Einheitlicher Status & UX:** Standardisierung der Dateidialoge und Verbesserung des 'L'-Befehls für Echtzeit-Fortschrittsmeldungen.

## Änderungen in Version 3.6.0

* **Hilfesystem:** Hilfe-Befehl (`H`) innerhalb der Befehlsebene hinzugefügt.
* **Online-Videoanalyse:** Unterstützung für **Twitter (X)** Videos hinzugefügt und URL-Erkennung verbessert.
* **Projekt-Unterstützung:** Optionaler Spendendialog für Nutzer hinzugefügt.

## Änderungen in Version 3.5.0

* **Befehlsebene:** Einführung des Befehlsebenen-Systems (Standard: `NVDA+Umschalt+V`), um Kürzel unter einer Master-Taste zu gruppieren.
* **Online-Videoanalyse:** Neue Funktion zur Analyse von YouTube- und Instagram-Videos per URL.

## Änderungen in Version 3.1.0

* **Direkt-Ausgabe-Modus:** Option hinzugefügt, den Chat-Dialog zu überspringen und Antworten direkt per Sprache zu hören.
* **Zwischenablage-Integration:** Einstellung zum automatischen Kopieren der KI-Antworten hinzugefügt.

## Änderungen in Version 3.0

* **Neue Sprachen:** Unterstützung für **Persisch** und **Vietnamesisch** hinzugefügt.
* **Erweiterte KI-Modelle:** Neuorganisation der Modellliste mit Präfixen wie `[Free]` oder `[Pro]`. Unterstützung für **Gemini 3.0 Pro** und **Gemini 2.0 Flash Lite** hinzugefügt.
* **Diktat-Stabilität:** Signifikante Verbesserungen beim Smart-Diktat; Clips unter 1 Sekunde werden nun ignoriert.
* **Datei-Handling:** Fehler beim Hochladen von Dateien mit nicht-englischen Namen behoben.
* **Prompt-Optimierung:** Verbesserte Übersetzungslogik und strukturierte Vision-Ergebnisse.

## Änderungen in Version 2.9

* **Sprachen:** Französische und türkische Übersetzungen hinzugefügt.
* **Formatierte Ansicht:** Schaltfläche „Formatiert anzeigen“ im Chat-Dialog hinzugefügt (Überschriften, Fettdruck, Code).
* **Markdown-Einstellung:** Option „Markdown im Chat säubern“ hinzugefügt, um Roh-Markdown-Syntax wahlweise anzuzeigen.
* **Dialog-Management:** Fokusfehler und mehrfaches Öffnen von Fenstern behoben.
* **UX-Verbesserungen:** Standardisierte Dateidialog-Titel und Entfernung redundanter Ansagen.

## Änderungen in Version 2.8

* Italienische Übersetzung hinzugefügt.
* **Status-Bericht:** Neuer Befehl (NVDA+Strg+Umschalt+I) zur Ansage des aktuellen Status.
* **HTML-Export:** Speichern-Schaltfläche exportiert nun als formatierte HTML-Datei.
* **Neue Modelle:** Unterstützung für gemini-flash-latest und gemini-flash-lite-latest.
* **Sprachen:** Nepali hinzugefügt.
* **Refine-Menü:** Fehler behoben, bei dem Befehle fehlschlugen, wenn NVDA nicht auf Englisch eingestellt war.
* **Diktat:** Verbesserte Stille-Erkennung.

## Änderungen in Version 2.7

* Migration auf das offizielle NV Access Add-on Template.
* Automatischer Retry bei HTTP 429 Fehlern (Rate Limit).
* Optimierte Prompts für höhere Genauigkeit und bessere Smart-Swap-Logik.

## Änderungen in Version 2.6

* Russische Übersetzung hinzugefügt.
* Beschreibendere Fehlermeldungen bei Verbindungsproblemen.
* Standard-Zielsprache auf Englisch geändert.

## Änderungen in Version 2.5

* Befehl für natives Datei-OCR hinzugefügt (NVDA+Strg+Umschalt+F).
* „Chat speichern“-Button in Dialogen hinzugefügt.
* Vollständige Lokalisierungsunterstützung (i18n).
* Nutzung der Gemini File API für PDFs und Audio.

## Änderungen in Version 2.1.1

* Fehler mit der `[file_ocr]` Variable in eigenen Prompts behoben.

## Änderungen in Version 2.1

* Standardisierung aller Kürzel auf NVDA+Strg+Umschalt zur Vermeidung von Konflikten.

## Änderungen in Version 2.0

* Integriertes Auto-Update-System.
* Smart-Translation-Cache für sofortige Abrufe.
* Konversationsgedächtnis für Folgefragen im Chat.
* Spezieller Befehl für Zwischenablage-Übersetzung.

## Änderungen in Version 1.5

* Unterstützung für über 20 neue Sprachen.
* Interaktiver Optimierungsdialog für Folgefragen.
* Natives Smart-Diktat-Feature.

## Änderungen in Version 1.0

* Erstveröffentlichung.

## Übersetzung

Übersetzt von **BFW Würzburg** im Rahmen des Projekts "NVDA Nachhaltig"