# KI Assistent pro Dokumentation

**KI Assistent pro** ist ein fortschrittlicher, multimodaler KI-Assistent für NVDA. Er nutzt erstklassige KI-Engines, um intelligentes Screenreading, Übersetzungen, Sprachdiktate und Dokumentenanalysen zu ermöglichen.

*Dieses Add-on wurde zu Ehren des Internationalen Tages der Menschen mit Behinderungen für die Community veröffentlicht.*

## 1. Einrichtung & Konfiguration

Gehen Sie zu **NVDA-Menü > Optionen > Einstellungen > KI Assistent pro**.

### 1.1 Verbindungseinstellungen

* **Anbieter:** Wählen Sie Ihren bevorzugten KI-Dienst. Unterstützte Anbieter sind **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** und **Benutzerdefiniert** (OpenAI-kompatible Server wie Ollama, LM Studio, Jan.ai oder KoboldCPP).
* **Wichtiger Hinweis:** Wir empfehlen dringend die Verwendung von **Google Gemini** für die beste Leistung und Genauigkeit (insbesondere bei der Bild-/Dateianalyse).
* **API-Schlüssel:** Erforderlich. Sie können mehrere Schlüssel eingeben (getrennt durch Kommas oder neue Zeilen), um eine automatische Rotation zu ermöglichen.
* **Modelle abrufen:** Nachdem Sie Ihren API-Schlüssel eingegeben haben, drücken Sie diese Schaltfläche, um die aktuelle Liste der verfügbaren Modelle vom Anbieter herunterzuladen.
* **KI-Modell:** Wählen Sie das Hauptmodell aus, das für den allgemeinen Chat und die Analysen verwendet werden soll.

### 1.2 Erweitertes Modell-Routing

*Verfügbar für alle Anbieter einschließlich Gemini, OpenAI, Groq, Mistral und Benutzerdefiniert.*

> **⚠️ Warnung:** Diese Einstellungen sind **nur für fortgeschrittene Benutzer** gedacht. Wenn Sie sich unsicher sind, was ein bestimmtes Modell bewirkt, lassen Sie dies bitte **deaktiviert**. Die Auswahl eines inkompatiblen Modells für eine Aufgabe (z. B. ein reines Textmodell für Vision-Aufgaben) führt zu Fehlern und stoppt die Funktion des Add-ons.

Aktivieren Sie **"Erweitertes Modell-Routing (Aufgabenspezifisch)"**, um detaillierte Steuerungsmöglichkeiten freizuschalten. Dies ermöglicht es Ihnen, spezifische Modelle aus der Dropdown-Liste für verschiedene Aufgaben auszuwählen:

* **OCR / Vision-Modell:** Wählen Sie ein spezialisiertes Modell für die Analyse von Bildern.
* **Speech-to-Text (STT):** Wählen Sie ein spezifisches Modell für das Diktat.
* **Text-to-Speech (TTS):** Wählen Sie ein Modell zur Generierung von Audio.
* **KI-Operator-Modell:** Wählen Sie ein spezifisches Modell für autonome Computersteuerungsaufgaben.
*Hinweis: Nicht unterstützte Funktionen (z. B. TTS für Groq) werden automatisch ausgeblendet.*

### 1.3 Erweiterte Endpunkt-Konfiguration (Benutzerdefinierter Anbieter)

*Nur verfügbar, wenn "Benutzerdefiniert" ausgewählt ist.*

> **⚠️ Warnung:** Dieser Abschnitt ermöglicht die manuelle API-Konfiguration und ist für **Power-User** konzipiert, die lokale Server oder Proxys betreiben. Falsche URLs oder Modellnamen unterbrechen die Konnektivität. Wenn Sie nicht genau wissen, was diese Endpunkte sind, lassen Sie dies **deaktiviert**.

Aktivieren Sie **"Erweiterte Endpunkt-Konfiguration"**, um Serverdetails manuell einzugeben. Im Gegensatz zu nativen Anbietern müssen Sie hier die spezifischen URLs und Modellnamen **tippen**:

* **Modelllisten-URL:** Der Endpunkt zum Abrufen verfügbarer Modelle.
* **OCR/STT/TTS Endpunkt-URL:** Vollständige URLs für spezifische Dienste (z. B. `http://localhost:11434/v1/audio/speech`).
* **Benutzerdefinierte Modelle:** Geben Sie den Modellnamen (z. B. `llama3:8b`) für jede Aufgabe manuell ein.

### 1.3.1 Lokale KI einrichten (Ein-Klick-Konfiguration)

Um die lokale, vollständig serverunabhängige KI-Integration extrem zu vereinfachen, steht in den Einstellungen für benutzerdefinierte Anbieter eine dedizierte Schaltfläche **"Lokale KI einrichten"** zur Verfügung.

Wenn Sie einen lokalen KI-Modellserver auf Ihrem Computer ausführen:

1. Wählen Sie **Benutzerdefiniert** als Ihren Anbieter.
2. Drücken Sie die Schaltfläche **Lokale KI einrichten**.
3. Wählen Sie Ihre lokale KI-Engine aus dem barrierefreien Dialog aus:
* **Ollama** (Standard: `http://127.0.0.1:11434`)
* **LM Studio** (Standard: `http://127.0.0.1:1234`)
* **Jan.ai** (Standard: `http://127.0.0.1:1337`)
* **KoboldCPP** (Standard: `http://127.0.0.1:5001`)


4. Das Add-on konfiguriert sofort die korrekte lokale URL sowie den API-Typ und ruft automatisch Ihre aktiven Offline-Modelle ab, um das Auswahlfeld **KI-Modell** zu füllen.

*Hinweis zu Netzwerk & Proxies:* Diese lokale Verbindung verfügt über einen fortschrittlichen Proxy-Bypass-Mechanismus. Selbst wenn Sie ein aktives System-VPN oder einen Proxy im TUN-Modus nutzen, werden Ihre lokalen KI-Anfragen vollständig daran vorbeigeleitet. Dies gewährleistet stabile Offline-Verbindungen ohne "502 Bad Gateway"-Fehler.

### 1.4 Allgemeine Einstellungen

* **OCR-Engine:** Wählen Sie zwischen **Chrome (Schnell)** für schnelle Ergebnisse oder **KI (Erweitert)** für eine überlegene Beibehaltung des Layouts.
* *Hinweis:* Wenn Sie "KI (Erweitert)" wählen, Ihr Anbieter aber auf OpenAI/Groq eingestellt ist, leitet das Add-on das Bild intelligent an das Vision-Modell Ihres aktiven Anbieters weiter.


* **TTS-Stimme:** Wählen Sie Ihren bevorzugten Stimmenstil. Diese Liste wird dynamisch basierend auf Ihrem aktiven Anbieter aktualisiert.
* **Kreativität (Temperatur):** Steuert die Zufälligkeit der KI. Niedrigere Werte sind besser für genaue Übersetzungen/OCR.
* **Proxy-URL:** Konfigurieren Sie dies, falls KI-Dienste in Ihrer Region eingeschränkt sind (unterstützt lokale Proxys wie `127.0.0.1` oder Bridge-URLs).

## 2. Befehlsebene & Tastenkombinationen

Um Tastaturkonflikte zu vermeiden, verwendet dieses Add-on eine **Befehlsebene**.

1. Drücken Sie **NVDA + Umschalt + V** (Haupttaste), um die Ebene zu aktivieren (Sie hören einen Signalton).
2. Lassen Sie die Tasten los und drücken Sie dann eine der folgenden Einzeltasten:

| Taste | Funktion | Beschreibung |
| --- | --- | --- |
| **Umschalt+A** | **KI-Operator** | **Autonome Steuerung:** Weisen Sie die KI an, eine Aufgabe auf Ihrem Bildschirm auszuführen. Erneutes Drücken bricht die Aktion sofort ab. |
| **E** | **UI-Explorer** | **Interaktiver Klick:** Identifiziert und klickt auf UI-Elemente in jeder Anwendung. |
| **T** | Intelligenter Übersetzer | Übersetzt Text unter dem Navigator-Objekt oder der Markierung. |
| **Umschalt+T** | Zwischenablage-Übersetzer | Übersetzt den aktuellen Inhalt der Zwischenablage. |
| **R** | Text-Optimierer | Zusammenfassen, Grammatik korrigieren, Erklären oder **Eigene Prompts**. |
| **V** | Objekt-Vision | Beschreibt das aktuelle Navigator-Objekt. |
| **O** | Vollbild-Vision | Analysiert das gesamte Bildschirmlayout und den Inhalt. |
| **Umschalt+V** | Online-Videoanalyse | Analysiert **YouTube**, **Instagram**, **TikTok** oder **Twitter (X)** Videos. |
| **D** | Dokumentenleser | Fortgeschrittener Leser für PDF und Bilder mit Seitenbereichsauswahl. |
| **F** | **Smarte Datei-Aktion** | Kontextabhängige Erkennung aus ausgewählten Bild-, PDF- oder TIFF-Dateien. |
| **A** | Audio-Transkription | Transkribiert MP3-, WAV- oder OGG-Dateien in Text. |
| **C** | CAPTCHA-Löser | Erfasst und löst CAPTCHAs (Unterstützt Regierungsportale). |
| **S** | Intelligentes Diktat | Wandelt Sprache in Text um. Drücken zum Starten, erneut drücken zum Stoppen. |
| **Strg+L** | **Live-Assistent** | **Echtzeit-Copilot (nur Gemini):** Startet oder beendet ein Live-Sprach- und Bildschirmgespräch mit dem KI-Assistenten. |
| **I** | Statusbericht | Meldet den aktuellen Fortschritt (z. B. "Scannen...", "Bereit"). |
| **L** | **Objekt beschriften** | **Semantische KI-Beschriftung:** Beschriftet das aktuell fokussierte Element/Symbol dauerhaft. |
| **Umschalt+L** | **Beschriftungen verwalten/scannen** | Öffnet den Beschriftungs-Manager (falls Beschriftungen existieren) oder scannt die App nach unbenannten Elementen. |
| **U** | Update-Prüfung | Prüft manuell auf GitHub nach der neuesten Version des Add-ons. |
| **Leertaste** | Letztes Ergebnis abrufen | Zeigt die letzte KI-Antwort in einem Chat-Dialog zur Überprüfung an. |
| **H** | Befehlshilfe | Zeigt eine Liste aller verfügbaren Kürzel innerhalb der Befehlsebene an. |

### 2.1 Tastenkombinationen im Dokumentenleser (Innerhalb des Viewers)

* **Strg + BildAb:** Zur nächsten Seite wechseln.
* **Strg + BildAuf:** Zur vorherigen Seite wechseln.
* **Alt + A:** Öffnet einen Chat-Dialog, um Fragen zum Dokument te stellen.
* **Alt + R:** Erzwingt einen **erneuten Scan mit KI** über Ihren aktiven Anbieter.
* **Alt + G:** Erzeugt und speichert eine hochwertige Audiodatei (WAV/MP3). *Ausgeblendet, wenn der Anbieter kein TTS unterstützt.*
* **Alt + S / Strg + S:** Speichert den extrahierten Text als TXT- oder HTML-Datei.

## 3. Eigene Prompts & Variables

Sie können Prompts unter **Einstellungen > Prompts > Prompts verwalten...** verwalten.

### Unterstützte Variablen

* `[selection]`: Aktuell markierter Text.
* `[clipboard]`: Inhalt der Zwischenablage.
* `[screen_obj]`: Screenshot des Navigator-Objekts.
* `[screen_full]`: Vollbild-Screenshot.
* `[file_ocr]`: Bild-/PDF-Datei für Textextraktion auswählen.
* `[file_read]`: Dokument zum Lesen auswählen (TXT, Code, PDF).
* `[file_audio]`: Audiodatei zur Analyse auswählen (MP3, WAV, OGG).

---

**Hinweis:** Für alle KI-Funktionen ist eine active Internetverbindung erforderlich. Mehrseitige Dokumente werden automatisch verarbeitet.

## 4. Support & Community

Bleiben Sie auf dem Laufenden über Neuigkeiten, Funktionen und Veröffentlichungen:

* **Telegram-Kanal:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
* **GitHub Issues:** Für Fehlermeldungen und Funktionsanfragen.

## 5. Projekt-Unterstützer

Ein herzliches Dankeschön an unsere Community-Mitglieder, die die kontinuierliche Entwicklung und Pflege dieses Projekts durch ihre großzügigen finanziellen Beiträge unterstützen:

* **@Alyabani94**
* **Ali Alamri**
* **Ilya**
* **Anonymer Unterstützer** (`UQDd...CnMY`)
* **leonardo0216**

*Wenn Sie das Projekt finanziell unterstützen und Ihren Namen hier sehen möchten, finden Sie die Option **Spenden** im NVDA-Werkzeuge-Menü (Untermenü KI-Assistent) oder während des Einrichtungsprozesses nach der Installation.*

---

## Änderungen in 6.5.0

* **Live-Assistent**: Echtzeit-Sprach- und Bildschirmassistent hinzugefügt, der exklusiv für Google Gemini (oder Gemini-kompatible benutzerdefinierte Anbieter) verfügbar ist. Beinhaltet eine interaktive Anpassung von Stimme und Denktiefe direkt im Dialog, mit automatischer Wiederverbindung nach Einstellungsänderungen.
* **MiniMax KI-Anbieter**: MiniMax wurde als gleichwertiger Anbieter mit vollständiger multimodaler Unterstützung (Chat, Vision, OCR), benutzerdefiniertem TTS mit über 300+ dynamischen Stimmen und automatischem Entfernen von Denkblöcken (z. B. `<think>...</think>`) aus den Ausgaben integriert.
* **Übersetzung im Dokumentenleser**: Ein stiller Übersetzungsfehler für nicht-englische NVDA-Benutzer wurde behoben, indem sichergestellt wird, dass der standardmäßige zweistellige Sprachcode an Google Translate gesendet wird anstelle des lokalisierten Sprachnamens.
* **PDF-Stapelscan-Wiederholung**: Eine hochoptimierte, separate und stille Wiederholungslogik für das Scannen von PDF-Dokumentenstapeln wurde implementiert, um redundante Uploads zu vermeiden und störende Fehler-Popups während der Wiederholungen zu verhindern.
* **Status des Dokumentenlesers**: Ein Fehler wurde behoben, bei dem der Gesamtstatus des Plugins (überprüft mit `I`) während langer Dokumentenscans auf „Stapelverarbeitung gestartet“ hängen blieb.
* **Threading-Absturz behoben**: Ein schwerwiegender Thread-Assertion-Absturz (`IsMain() failed in wxTimerImpl`) beim Öffnen von Dokumenten aus einem Hintergrund-Thread wurde behoben, indem die GUI-Callback-Warteschlange auf `wx.CallAfter` umgestellt wurde.

## Änderungen in 6.1.2

* **Vorabprüfung auf doppelte Beschriftungen**: Ein Problem bei der Einzelbeschriftung wurde behoben, bei dem die Prüfung auf Duplikate alte Koordinatenschlüssel verwendete. Dies führte dazu, dass NVDA doppelte KI-Anfragen für bereits beschriftete Objekte stellte, anstatt die vorhandene Beschriftung anzusagen.
* **Dokumenten-Chat für Nicht-Gemini-Anbieter**: Eine strikte API-Schlüsselprüfung im Dokumenten-Chat (`on_ask`) wurde korrigiert, um sicherzustellen, dass Benutzer von OpenAI, Groq oder lokalen benutzerdefinierten Anbietern (wie Ollama) erfolgreich mit Dokumenten chatten können, ohne blockiert zu werden.
* **Schnelle Chrome-OCR-Übersetzung**: Die kostenlose, schlüssellose Übersetzungs-API für Chrome-OCR wurde wiederhergestellt. Das Übersetzen von extrahiertem Text umgeht nun Gemini-KI, was API-Kontingente spart und den Übersetzungsprozess beschleunigt.
* **Alphanumerischer Filter für CAPTCHAs**: Die Filterlogik im CAPTCHA-Löser wurde korrigiert, um sicherzustellen, dass nicht-alphanumerische Zeichen in allen Situationen ordnungsgemäß bereinigt werden.
* **Aktualisierung der Hilfe für die Befehlsebene**: Die Tastenkombination für die Statusansage im Hilfemenü wurde von `L` auf `I` korrigiert und beide Beschriftungsbefehle (`L` und `Umschalt+L`) wurden zur Liste hinzugefügt.

## Änderungen in 6.1.1

* **Korrektur der Denkausgabe bei Gemma 4**: Ein Problem mit Gemma 4-Modellen wurde behoben, bei dem der gesamte interne Denkprozess als endgültige Antwort angezeigt wurde oder das Deaktivieren des Denkens zu leeren Antworten führte. Das Add-on isoliert und extrahiert nun korrekt nur die finale, bereinigte Textantwort.
* **Stapel-OCR aus dem Datei-Explorer**: Sie können nun mehrere Fotos oder PDFs direkt im Windows Datei-Explorer auswählen und als Stapel Text extrahieren oder analysieren lassen. Das Add-on filtert und verarbeitet automatisch nur die unterstützten Dateiformate.

## Änderungen in 6.1.0

* **Universelle lokale KI-Integration (Lokale KI einrichten)**: Eine neue Schaltfläche **"Lokale KI einrichten"** wurde in den Einstellungen für benutzerdefinierte Anbieter hinzugefügt. Benutzer können nun lokale KI-Engines wie **Ollama**, **LM Studio**, **Jan.ai** und **KoboldCPP** sofort automatisch konfigurieren.
* **Intelligenter loker Proxy-Bypass**: Die Verbindungslogik wurde mit einem fortschrittlichen Proxy-Bypass-Mechanismus neu aufgebaut. Das Add-on ist nun intelligent genug, um Windows-System-Proxys für lokale Loopback-Verbindungen vollständig zu umgehen, was stabile lokale KI-Verbindungen gewährleistet, selbst wenn Ihr VPN/TUN-Modus aktiv ist.
* **Ultra-stabile KI-Beschriftung (v2)**: Absolute Bildschirmkoordinatenschlüssel wurden durch ein fortschrittliches, hybrides **Objektsignatur-System** ersetzt. Beschriftungen basieren nun auf programmgesteuerten Identifikatoren (UIA **AutomationId** oder Win32 **ControlID**) und fensterrelativen Koordinaten. Dadurch sind Ihre benutzerdefinierten Beschriftungen völlig resistent gegen das Ändern der Fenstergröße, Verschieben, Monitorwechsel oder Skalierungen.
* **Nahtlose automatische Beschriftungsmigration**: Das Upgrade erfolgt völlig transparent. Das Add-on migriert Ihre älteren, auf Legacy-Koordinaten basierenden Beschriftungen beim ersten Fokussieren automatisch im Hintergrund in das neue, stabile Fingerabdruckformat – ganz ohne Datenverlust.

## Änderungen in 6.0

* **Einführung der semantischen KI-Beschriftung**: Benutzer können nun unbenannte Schaltflächen und Symbole mithilfe von KI dauerhaft beschriften. Drücken Sie **L**, um das aktuelle Navigator-Objekt zu beschriften (unterstützt sowohl den Tab-Fokus als auch die Objektnavigation), oder **Umschalt+L**, um die gesamte Anwendung auf einmal zu scannen und zu beschriften.
* **Intelligente Beschriftungsverwaltung**: Ein neuer, vollständig barrierefreier Beschriftungs-Manager-Dialog wurde hinzugefügt (erreichbar über **Umschalt+L**, falls Beschriftungen existieren), um benutzerdefinierte Beschriftungen anzuzeigen, umzubenennen oder im Stapel zu löschen.
* **Direkte Dateianalyse (Dateidialog umgehen)**: Das Add-on ist nun intelligent genug, um zu erkennen, ob Sie gerade eine PDF- oder Bilddatei im Windows Datei-Explorer fokussieren. Das Drücken von **F (Smarte Datei-Aktion)** oder **D (Dokumentenleser)** auf einer markierten Datei verarbeitet diese sofort und umgeht den Standard-"Öffnen"-Dialog komplett.

## Änderungen in 5.6

* **OCR-Engine "Keine (Textschicht extrahieren)" hinzugefügt**: Benutzer können nun Text direkt aus durchsuchbaren PDFs extrahieren, ohne KI-Guthaben zu verbrauchen, was die Geschwindigkeit und den Datenschutz bei textbasierten Dokumenten erheblich verbessert.
* **Verfeinerte UI-Explorer-Genauigkeit**: Die UI-Explorer-Eingabeaufforderung wurde verbessert, um Elementtypen (wie Listeneinträge) besser zu identifizieren und Zustände wie „(Aktiviert)“, „(Ausgewählt)“ oder „(Erweitert)“ korrekt zu melden, während Windows-Systemkomponenten wie die Taskleiste und die Uhr ignoriert werden.
* **Installations-Einrichtungshinweis**: Nach der Installation wurde eine Benachrichtigung hinzugefügt, um Benutzer zum Einstellungsmenü zu führen, damit sie ihre API-Schlüssel und Präferenzen konfigurieren können.

## Änderungen in 5.5.2

* **Problem beim Tippen des KI-Operators behoben**: Ein Fehler wurde behoben, bei dem auf bestimmten Systemen der Buchstabe 'v' getippt wurde, anstatt Text einzufügen. Diese Korrektur behebt Timing-Konflikte, die bei hoher Systemlast auftraten.
* **Erhöhte Stabilität**: Es wurde eine robuste Fehlerbehandlung für Zwischenablage-Operationen hinzugefügt, um Abstürze des Add-ons zu verhindern, wenn die Systemzwischenablage vorübergehend durch andere Anwendungen gesperrt ist.
* **Timing-Optimierung**: Interne Verzögerungen für Tastaturereignisse wurden angepasst, um eine höhere Zuverlässigkeit bei unterschiedlichen Systemgeschwindigkeiten und eine bessere Kompatibilität mit Zwischenablage-Managern von Drittanbietern zu gewährleisten.

## Änderungen in 5.5 (Das Automatisierungs-Update)

* **KI-Operator (Autonome Steuerung - Umschalt+A):** Dies ist das Herzstück von v5.5. KI Assistent pro hat sich von einem passiven Assistenten zu Ihrem persönlichen **KI-Operator** weiterentwickelt. Er beschreibt nicht mehr nur den Bildschirm – er übernimmt das Kommando.
* *Wie es funktioniert:* Sie können jetzt sprachliche oder schriftliche Anweisungen geben, um Ihren PC zu steuern. In einer völlig unzugänglichen Anwendung, in der Ihr Screenreader stumm bleibt, können Sie beispielsweise **Umschalt+A** drücken und eingeben: *„Klicke auf die Schaltfläche Einstellungen“* oder *„Suche das Suchfeld, tippe 'Aktuelle Nachrichten' ein und drücke Enter.“* Die KI identifiziert die Elemente visuell, bewegt die Maus und führt die Aufgabe für Sie aus.
* *Leistungshinweis:* Diese Funktion ist für **Gemini 3.0 Flash (Preview)** optimiert und liefert unglaublich schnelle und intelligente Antworten, die selbst mit komplexesten UI-Layouts umgehen können.
* **⚠️ Warnung zur API-Nutzung:** Da der KI-Operator genau „sehen“ muss, was passiert, um präzise zu sein, sendet er bei jedem Schritt einen hochauflösenden Screenshot. Bitte beachten Sie, dass eine häufige Nutzung Ihr API-Kontingent viel schneller verbraucht als standardmäßige textbasierte Aufgaben.


* **Visueller UI-Explorer (E):** Müde davon, durch „unbenannte Schaltflächen“ zu navigieren? Drücken Sie **E**, um den UI-Explorer zu aktivieren. Die KI scannt das gesamte Fenster und erstellt eine Liste aller anklickbaren Elemente, die sie sieht – einschließlich Symbolen, Grafiken und Menüs. Wählen Sie einfach ein Element aus der Liste aus, und der KI-Operator klickt es für Sie an. Es ist wie eine „barrierefreie Schicht“ über jeder App.
* **Kontextabhängige smarte Datei-Aktion (F):** Die Taste „F“ wurde komplett überarbeitet. Sie geht nicht mehr pauschal davon aus, dass Sie nur OCR möchten. Wenn Sie eine einzelne Bilddatei auswählen, fragt sie nun intelligent nach Ihrer Absicht: Sie können eine **Detaillierte visuelle Beschreibung** wählen, um die Szene zu verstehen, oder eine **Strukturierte Textextraktion (OCR)** zum Lesen. Das Menü passt sich dynamisch an den Dateityp und Ihre aktive KI-Engine an.
* **Kernoptimierung:** Wir haben die interne Logik des Add-ons gründlich bereinigt, ungenutzte Legacy-Funktionen und redundanten Code entfernt. Dies führt zu einer schlankeren, schnelleren und zuverlässigeren Benutzererfahrung für alle.

## Änderungen in 5.0

* **Multi-Anbieter-Architektur**: Volle Unterstützung für **OpenAI**, **Groq** und **Mistral** neben Google Gemini hinzugefügt. Benutzer können nun ihr bevorzugtes KI-Backend wählen.
* **Erweitertes Modell-Routing**: Benutzer nativer Anbieter (Gemini, OpenAI etc.) können nun spezifische Modelle für verschiedene Aufgaben (OCR, STT, TTS) aus einer Liste wählen.
* **Erweiterte Endpunkt-Konfiguration**: Benutzerdefinierte Anbieter können URLs und Modellnamen manuell eingeben, um die volle Kontrolle über lokale oder Drittanbieter-Server zu haben.
* **Intelligente Sichtbarkeit von Funktionen**: Das Einstellungsmenü und die Benutzeroberfläche des Dokumentenlesers blenden nicht unterstützte Funktionen (wie TTS) basierend auf dem gewählten Anbieter automatisch aus.
* **Dynamisches Abrufen von Modellen**: Das Add-on ruft die Liste der verfügbaren Modelle nun direkt über die API des Anbieters ab, um Kompatibilität mit neuen Modellen sofort nach deren Erscheinen sicherzustellen.
* **Hybrid-OCR & Übersetzung**: Die Logik wurde optimiert, um Google Translate für Geschwindigkeit bei Chrome-OCR zu nutzen und KI-basierte Übersetzung bei Gemini/Groq/OpenAI-Engines zu verwenden.
* **Universelles "Erneuter Scan mit KI"**: Die Re-Scan-Funktion des Dokumentenlesers ist nicht mehr auf Gemini schwieriger zugänglich beschränkt. Sie nutzt nun den jeweils aktiven KI-Anbieter zur Neuverarbeitung von Seiten.

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

* **Verbesserte Netzwerk-Resilienz:** Automatischer Wiederholungsmechanismus bei instabilen Verbindungen hinzugefügt.
* **Visueller Übersetzungsdialog:** Neues Fenster für Übersetzungsergebnisse, das zeilenweises Lesen langer Texte ermöglicht.
* **Aggregierte formatierte Ansicht:** Die Funktion "Formatiert anzeigen" im Dokumentenleser zeigt nun alle verarbeiteten Seiten in einem einzigen, organisierten Fenster an.
* **Optimierter OCR-Workflow:** Überspringt die Seitenbereichsauswahl bei einseitigen Dokumenten automatisch.
* **Verbesserte API-Stabilität:** Umstellung auf Header-basierte Authentifizierung zur Vermeidung von Fehlern bei der Schlüsselrotation.

## Änderungen in 4.0.1

* **Fortgeschrittener Dokumentenleser:** Neuer Viewer für PDF und Bilder mit Seitenbereichsauswahl und Hintergrundverarbeitung.
* **Neues Werkzeuge-Untermenü:** Untermenü "KI Assistent" unter NVDA-Werkzeuge für schnelleren Zugriff hinzugefügt.
* **Flexible Anpassung:** OCR-Engine und TTS-Stimme direkt in den Einstellungen wählbar.
* **Unterstützung mehrerer API-Schlüssel:** Unterstützung für mehrere Gemini-Schlüssel (einer pro Zeile oder durch Komma getrennt).
* **Alternative OCR-Engine:** Neue Engine zur Texterkennung hinzugefügt, falls das Gemini-Kontingent erschöpft ist.
* **Dokument zu MP3/WAV:** Fähigkeit zur Erzeugung hochwertiger Audiodateien direkt im Reader integriert.
* **Instagram Stories & TikTok Support:** Analyse von Stories und TikTok-Videos über deren URLs hinzugefügt.

## Änderungen in 3.6.0

* **Hilfesystem:** Hilfe-Befehl (`H`) innerhalb der Befehlsebene hinzugefügt.
* **Online-Videoanalyse:** Unterstützung für **Twitter (X)** Videos hinzugefügt sowie URL-Erkennung verbessert.

## Änderungen in 3.5.0

* **Befehlsebene:** Einführung der Befehlsebene (Standard: `NVDA+Umschalt+V`), um Kürzel unter einer Haupttaste zu gruppieren.
* **Online-Videoanalyse:** Neue Funktion zur Analyse von YouTube- und Instagram-Videos per URL.

## Änderungen in 3.1.0

* **Direkter Ausgabemodus:** Option zum Überspringen des Chat-Dialogs, um KI-Antworten sofort per Sprache zu hören.
* **Zwischenablage-Integration:** Einstellung zum automatischen Kopieren von KI-Antworten in die Zwischenablage.

## Änderungen in 3.0

* **Neue Sprachen:** Persisch und Vietnamesisch hinzugefügt.
* **Erweiterte KI-Modelle:** Modellliste mit Präfixen (`[Free]`, `[Pro]`, `[Auto]`) neu organisiert. Unterstützung für **Gemini 3.0 Pro** und **Gemini 2.0 Flash Lite**.
* **Diktat-Stabilität:** Ignoriert nun Audioclips unter 1 Sekunde, um Halluzinationen zu vermeiden.
* **Dateihandlung:** Fehler beim Hochladen von Dateien mit nicht-englischen Namen behoben.

## Änderungen in 2.9

* **Französische und türkische Übersetzungen hinzugefügt.**
* **Formatierte Ansicht:** Schaltfläche "Formatiert anzeigen" in Chat-Dialogen hinzugefügt (Überschriften, Fettdruck, Code).
* **Markdown-Einstellung:** Option "Bereinigtes Markdown im Chat" hinzugefügt.

## Änderungen in 2.8

* Italienische Übersetzung hinzugefügt.
* **Statusbericht:** Neuer Befehl (NVDA+Strg+Umschalt+I) zum Ansagen des aktuellen Status.
* **HTML-Export:** Speichern-Schaltfläche exportiert nun als formatiertes HTML.
* **Sprachen:** Nepali hinzugefügt.

## Änderungen in 2.7

* Projektstruktur auf die offizielle NV Access Vorlage migriert.
* Automatisches Retry bei HTTP 429 (Rate Limit) Fehlern.
* Optimierte Übersetzungs-Prompts.

## Änderungen in 2.6

* Russische Übersetzung hinzugefügt.
* Standard-Zielsprache auf Englisch geändert.

## Änderungen in 2.5

* Native Datei-OCR (NVDA+Strg+Umschalt+F) hinzugefügt.
* "Chat保存" Schaltfläche hinzugefügt.
* Umstellung auf Gemini File API für bessere PDF- und Audio-Handhabung.

## Änderungen in 2.1

* Standardisierung aller Kürzel auf NVDA+Strg+Umschalt, um Konflikte mit dem Laptop-Layout zu vermeiden.

## Änderungen in 2.0

* Integriertes Auto-Update-System.
* Intelligenter Übersetzungscache hinzugefügt.
* Konversationsgedächtnis für Kontext im Chat hinzugefügt.
* Separater Befehl für Zwischenablage-Übersetzung (NVDA+Strg+Umschalt+Y).

## Änderungen in 1.5

* Unterstützung für über 20 neue Sprachen.
* Interaktiver Optimierungs-Dialog für Folgefragen.
* Native "Intelligentes Diktat" Funktion.

## Änderungen in 1.0

* Erstveröffentlichung.

## Übersetzung

* Übersetzt von **BFW Würzburg** im Rahmen des Projekts "NVDA Nachhaltig"