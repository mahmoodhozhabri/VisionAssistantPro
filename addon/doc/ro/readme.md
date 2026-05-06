# Documentație Vision Assistant Pro

**Vision Assistant Pro** este un asistent IA avansat, multimodal, pentru NVDA. Folosește motoare IA de nivel înalt pentru citire inteligentă a ecranului, traducere, dictare vocală și analiză de documente.

_Acest supliment a fost lansat pentru comunitate în onoarea Zilei Internaționale a Persoanelor cu Dizabilități._

## 1. Configurare

Mergi la **Meniul NVDA > Preferințe > Setări > Vision Assistant Pro**.

### 1.1 Setări de conexiune
- **Furnizor:** Selectează serviciul IA preferat. Furnizorii acceptați includ **Google Gemini**, **OpenAI**, **Mistral**, **Groq** și **Personalizat** (servere compatibile OpenAI, precum Ollama/LM Studio).
- **Notă importantă:** Recomandăm **Google Gemini** pentru cea mai bună performanță și acuratețe, mai ales pentru analiza imaginilor și fișierelor.
- **Cheie API:** Obligatorie. Poți introduce mai multe chei, separate prin virgule sau linii noi, pentru rotație automată.
- **Preia modelele:** După introducerea cheii API, apasă acest buton ca să descarci cea mai recentă listă de modele disponibile de la furnizor.
- **Model IA:** Selectează modelul principal folosit pentru chat general și analiză.

### 1.2 Rutare avansată a modelelor
*Disponibilă pentru toți furnizorii, inclusiv Gemini, OpenAI, Groq, Mistral și Personalizat.*

> **⚠️ Avertisment:** Aceste setări sunt destinate doar utilizatorilor avansați. Dacă nu știi sigur ce face un model anume, lasă opțiunea **debifată**. Selectarea unui model incompatibil cu o sarcină, de exemplu un model doar text pentru Viziune, va produce erori și va opri funcționarea suplimentului.

Bifează **"Rutare avansată a modelelor (specifică sarcinii)"** pentru a activa controlul detaliat. Astfel poți selecta modele specifice din lista derulantă pentru sarcini diferite:
- **Model OCR / Viziune:** Alege un model specializat pentru analiza imaginilor.
- **Speech-to-Text (STT):** Alege un model specific pentru dictare.
- **Text-to-Speech (TTS):** Alege un model pentru generarea audio.
- **Model Operator IA:** Selectează un model specific pentru sarcini autonome de operare a computerului.
*Notă: Funcțiile neacceptate, de exemplu TTS pentru Groq, vor fi ascunse automat.*

### 1.3 Configurare avansată a endpointurilor (Furnizor personalizat)
*Disponibilă doar când este selectat "Personalizat".*

> **⚠️ Avertisment:** Această secțiune permite configurarea manuală a API-ului și este creată pentru utilizatori experimentați care rulează servere locale sau proxy-uri. URL-urile sau numele de modele greșite vor întrerupe conectivitatea. Dacă nu știi exact ce sunt aceste endpointuri, lasă opțiunea **debifată**.

Bifează **"Configurare avansată a endpointurilor"** pentru a introduce manual detaliile serverului. Spre deosebire de furnizorii nativi, aici trebuie să **tastezi** URL-urile specifice și numele modelelor:
- **URL listă modele:** Endpointul folosit pentru preluarea modelelor disponibile.
- **URL endpoint OCR/STT/TTS:** URL-uri complete pentru servicii specifice, de exemplu `http://localhost:11434/v1/audio/speech`.
- **Modele personalizate:** Tastează manual numele modelului, de exemplu `llama3:8b`, pentru fiecare sarcină.

### 1.4 Preferințe generale
- **Motor OCR:** Alege între **Chrome (Rapid)** pentru rezultate rapide sau **IA (Avansat)** pentru păstrarea mai bună a structurii paginii.
    - *Notă:* Dacă selectezi "IA (Avansat)", dar furnizorul tău este setat la OpenAI/Groq, suplimentul va direcționa inteligent imaginea către modelul de viziune al furnizorului activ.
- **Voce TTS:** Selectează stilul de voce preferat. Această listă se actualizează dinamic în funcție de furnizorul activ.
- **Creativitate (temperatură):** Controlează aleatorietatea IA. Valorile mai mici sunt mai bune pentru traducere și OCR precise.
- **URL proxy:** Configurează această opțiune dacă serviciile IA sunt restricționate în regiunea ta. Acceptă proxy-uri locale precum `127.0.0.1` sau URL-uri de tip bridge.

## 2. Strat de comenzi și scurtături

Pentru a evita conflictele de taste, acest supliment folosește un **Strat de comenzi**.
1. Apasă **NVDA + Shift + V** (tasta principală) pentru a activa stratul. Vei auzi un bip.
2. Eliberează tastele, apoi apasă una dintre tastele de mai jos:

| Tastă         | Funcție                  | Descriere                                                                   |
|---------------|--------------------------|-----------------------------------------------------------------------------|
| **Shift + A** | **Operator IA**          | **Operare autonomă:** Spune-i IA să efectueze o sarcină pe ecranul tău.      |
| **E**         | **Explorator UI**        | **Clic interactiv:** Identifică și apasă elemente UI din orice aplicație.    |
| **T**         | Traducător inteligent    | Traduce textul de sub cursorul navigator sau selecția.                       |
| **Shift + T** | Traducător clipboard     | Traduce conținutul aflat în prezent în clipboard.                            |
| **R**         | Rafinare text            | Rezumă, corectează gramatica, explică sau rulează **prompturi personalizate**.|
| **V**         | Viziune obiect           | Descrie obiectul navigator curent.                                           |
| **O**         | Viziune ecran complet    | Analizează structura și conținutul întregului ecran.                         |
| **Shift + V** | Analiză video online     | Analizează videoclipuri **YouTube**, **Instagram**, **TikTok** sau **Twitter (X)**. |
| **D**         | Cititor de documente     | Cititor avansat pentru PDF și imagini, cu selecție de interval de pagini.    |
| **F**         | **Acțiune fișier inteligentă** | Recunoaștere sensibilă la context din imagini, PDF-uri sau fișiere TIFF selectate. |
| **A**         | Transcriere audio        | Transcrie fișiere MP3, WAV sau OGG în text.                                  |
| **C**         | Rezolvator CAPTCHA       | Capturează și rezolvă CAPTCHA-uri. Acceptă portaluri guvernamentale.         |
| **S**         | Dictare inteligentă      | Convertește vorbirea în text. Apasă pentru pornire, apoi din nou pentru oprire sau tastare. |
| **L**         | Raportare stare          | Anunță progresul curent, de exemplu "Se scanează...", "Inactiv".          |
| **U**         | Verificare actualizări   | Verifică manual pe GitHub cea mai recentă versiune a suplimentului.          |
| **Space**     | Reapelează ultimul rezultat | Afișează ultimul răspuns IA într-un dialog de chat pentru revizuire sau continuare. |
| **H**         | Ajutor comenzi           | Afișează lista tuturor scurtăturilor disponibile.                            |

### 2.1 Scurtături pentru Cititorul de documente (în vizualizator)
- **Ctrl + PageDown:** Treci la pagina următoare.
- **Ctrl + PageUp:** Treci la pagina anterioară.
- **Alt + A:** Deschide un dialog de chat pentru întrebări despre document.
- **Alt + R:** Forțează o **rescanare cu IA** folosind furnizorul activ.
- **Alt + G:** Generează și salvează un fișier audio de calitate ridicată (WAV/MP3). *Ascuns dacă furnizorul nu acceptă TTS.*
- **Alt + S / Ctrl + S:** Salvează textul extras ca fișier TXT sau HTML.

## 3. Prompturi personalizate și variabile

Poți gestiona prompturile în **Setări > Prompturi > Gestionează prompturi...**.

### Variabile acceptate
- `[selection]`: Textul selectat în prezent.
- `[clipboard]`: Conținutul clipboardului.
- `[screen_obj]`: Captură de ecran a obiectului navigator.
- `[screen_full]`: Captură de ecran complet.
- `[file_ocr]`: Selectează fișier imagine/PDF pentru extragerea textului.
- `[file_read]`: Selectează document pentru citire (TXT, Cod, PDF).
- `[file_audio]`: Selectează fișier audio pentru analiză (MP3, WAV, OGG).

***
**Notă:** Pentru toate funcțiile IA este necesară o conexiune activă la internet. Documentele cu mai multe pagini sunt procesate automat.

## 4. Suport și comunitate

Rămâi la curent cu cele mai recente noutăți, funcții și lansări:
- **Canal Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Probleme GitHub:** Pentru raportări de erori și cereri de funcții.

---

## Modificări pentru 5.5 (Actualizarea pentru automatizare)

*   **Operator IA (control autonom, Shift+A):** Aceasta este funcția centrală din v5.5. Vision Assistant Pro a trecut de la un asistent pasiv la un **Operator IA** personal. Nu doar descrie ecranul, ci preia controlul.
    *   *Cum funcționează:* Acum poți da instrucțiuni verbale pentru operarea PC-ului. De exemplu, într-o aplicație complet inaccesibilă, unde cititorul de ecran rămâne tăcut, poți apăsa **Shift+A** și poți tasta: *"Clic pe butonul Setări"* sau *"Găsește câmpul de căutare, tastează 'Ultimele știri' și apasă Enter."* IA identifică vizual elementele, mișcă mouse-ul și execută sarcina pentru tine.
    *   *Notă de performanță:* Această funcție este optimizată pentru **Gemini 3.0 Flash (Preview)** și oferă răspunsuri foarte rapide și inteligente, care pot gestiona chiar și interfețe complexe.
    *   **⚠️ Avertisment privind utilizarea API:** Deoarece Operatorul IA trebuie să „vadă” exact ce se întâmplă pentru a fi precis, trimite o captură de ecran de rezoluție înaltă la fiecare pas. Folosirea frecventă va consuma cota API mult mai repede decât sarcinile standard bazate pe text.
*   **Explorator UI vizual (E):** Te-ai săturat să navighezi prin „butoane fără etichetă”? Apasă **E** pentru a activa Exploratorul UI. IA va scana întreaga fereastră și va genera o listă cu fiecare element clicabil pe care îl vede, inclusiv pictograme, elemente grafice și meniuri. Alege un element din listă, iar Operatorul IA va da clic pe el pentru tine. Este ca un strat accesibil peste orice aplicație.
*   **Acțiune inteligentă pentru fișiere, sensibilă la context (F):** Tasta „F” a fost refăcută complet. Nu mai presupune că vrei doar OCR. Când selectezi o singură imagine, acum te întreabă inteligent care este intenția ta: poți alege o **descriere vizuală detaliată** pentru a înțelege scena sau o **extragere structurată a textului (OCR)** pentru citire. Meniul se adaptează dinamic în funcție de tipul fișierului și de motorul IA activ.
*   **Optimizare de bază:** Am făcut o curățare profundă a logicii interne a suplimentului, eliminând funcții vechi nefolosite și cod redundant. Rezultatul este o experiență mai suplă, mai rapidă și mai fiabilă pentru toți utilizatorii.

## Modificări pentru 5.0

* **Arhitectură cu mai mulți furnizori:** S-a adăugat suport complet pentru **OpenAI**, **Groq** și **Mistral**, pe lângă Google Gemini. Utilizatorii pot alege acum backendul IA preferat.
* **Rutare avansată a modelelor:** Utilizatorii furnizorilor nativi, precum Gemini și OpenAI, pot selecta acum modele specifice dintr-o listă derulantă pentru sarcini diferite, cum ar fi OCR, STT și TTS.
* **Configurare avansată a endpointurilor:** Utilizatorii furnizorului personalizat pot introduce manual URL-uri specifice și nume de modele pentru control detaliat asupra serverelor locale sau terțe.
* **Vizibilitate inteligentă a funcțiilor:** Meniul de setări și interfața Cititorului de documente ascund acum automat funcțiile neacceptate, precum TTS, în funcție de furnizorul selectat.
* **Preluare dinamică a modelelor:** Suplimentul preia acum lista de modele disponibile direct din API-ul furnizorului, asigurând compatibilitate cu modelele noi imediat după lansare.
* **OCR și traducere hibridă:** Logica a fost optimizată ca să folosească Google Translate pentru viteză când se utilizează Chrome OCR și traducere bazată pe IA când se utilizează motoare Gemini/Groq/OpenAI.
* **„Rescanare cu IA” universală:** Funcția de rescanare din Cititorul de documente nu mai este limitată la Gemini. Acum folosește orice furnizor IA activ pentru reprocesarea paginilor.

## Modificări pentru 4.6
* **Reapelare interactivă a rezultatului:** S-a adăugat tasta **Space** în stratul de comenzi, permițând utilizatorilor să redeschidă instantaneu ultimul răspuns IA într-o fereastră de chat pentru întrebări ulterioare, chiar și când modul "Ieșire directă" este activ.
* **Hub comunitar Telegram:** S-a adăugat un link către "Canalul Telegram oficial" în meniul Instrumente NVDA, oferind o cale rapidă de a rămâne la curent cu noutățile, funcțiile și lansările.
* **Stabilitate îmbunătățită a răspunsurilor:** Logica de bază pentru funcțiile Traducere, OCR și Viziune a fost optimizată pentru performanță mai fiabilă și experiență mai fluidă când se folosește ieșirea vocală directă.
* **Ghidare îmbunătățită a interfeței:** Descrierile setărilor și documentația au fost actualizate pentru a explica mai bine noul sistem de reapelare și modul în care funcționează împreună cu setările de ieșire directă.

## Modificări pentru 4.5
* **Manager avansat de prompturi:** S-a introdus un dialog dedicat de gestionare în setări, pentru personalizarea prompturilor implicite de sistem și gestionarea prompturilor definite de utilizator, cu suport complet pentru adăugare, editare, reordonare și previzualizare.
* **Suport proxy complet:** S-au rezolvat problemele de conectivitate la rețea prin aplicarea strictă a setărilor proxy configurate de utilizator pentru toate cererile API, inclusiv traducere, OCR și generare vocală.
* **Migrare automată a datelor:** S-a integrat un sistem inteligent de migrare pentru actualizarea automată a configurațiilor vechi de prompturi la un format JSON v2 robust la prima rulare, fără pierderi de date.
* **Compatibilitate actualizată (2025.1):** Versiunea minimă NVDA necesară a fost setată la 2025.1 din cauza dependențelor de biblioteci din funcțiile avansate, precum Cititorul de documente, pentru performanță stabilă.
* **Interfață de setări optimizată:** Interfața de setări a fost simplificată prin mutarea gestionării prompturilor într-un dialog separat, oferind o experiență mai curată și mai accesibilă.
* **Ghid pentru variabilele prompturilor:** S-a adăugat un ghid integrat în dialogurile de prompturi pentru a ajuta utilizatorii să identifice și să folosească variabile dinamice precum [selection], [clipboard] și [screen_obj].

## Modificări pentru 4.0.3
*   **Rezistență rețea îmbunătățită:** S-a adăugat un mecanism de reîncercare automată pentru gestionarea mai bună a conexiunilor instabile la internet și a erorilor temporare de server, asigurând răspunsuri IA mai fiabile.
*   **Dialog vizual pentru traducere:** S-a introdus o fereastră dedicată pentru rezultatele traducerii. Utilizatorii pot naviga și citi ușor traduceri lungi, linie cu linie, similar rezultatelor OCR.
*   **Vizualizare formatată agregată:** Funcția "Vezi formatat" din Cititorul de documente afișează acum toate paginile procesate într-o singură fereastră organizată, cu antete clare pentru pagini.
*   **Flux OCR optimizat:** Se omite automat selecția intervalului de pagini pentru documentele cu o singură pagină, ceea ce face recunoașterea mai rapidă și mai fluidă.
*   **Stabilitate API îmbunătățită:** S-a trecut la o metodă de autentificare mai robustă, bazată pe antete, rezolvând posibile erori de tip "Toate cheile API au eșuat" cauzate de conflicte la rotația cheilor.
*   **Remedieri de erori:** S-au rezolvat mai multe blocări posibile, inclusiv o problemă la închiderea suplimentului și o eroare de focus în dialogul de chat.

## Modificări pentru 4.0.1
*   **Cititor de documente avansat:** Un vizualizator nou și puternic pentru PDF și imagini, cu selecție de interval de pagini, procesare în fundal și navigare fluidă cu `Ctrl+PageUp/Down`.
*   **Submeniu nou Instrumente:** S-a adăugat un submeniu dedicat "Vision Assistant" în meniul Instrumente al NVDA, pentru acces mai rapid la funcțiile principale, setări și documentație.
*   **Personalizare flexibilă:** Acum poți alege motorul OCR și vocea TTS preferate direct din panoul de setări.
*   **Suport pentru mai multe chei API:** S-a adăugat suport pentru mai multe chei API Gemini. Poți introduce câte o cheie pe linie sau le poți separa prin virgule în setări.
*   **Motor OCR alternativ:** S-a introdus un motor OCR nou pentru recunoaștere fiabilă a textului chiar și când sunt atinse limitele cotei API Gemini.
*   **Rotație inteligentă a cheilor API:** Comută automat la cea mai rapidă cheie API funcțională și o reține, pentru a evita limitele de cotă.
*   **Document în MP3/WAV:** S-a integrat capacitatea de a genera și salva fișiere audio de calitate ridicată în formatele MP3 (128kbps) și WAV direct din cititor.
*   **Suport pentru Instagram Stories:** S-a adăugat capacitatea de a descrie și analiza Instagram Stories folosind URL-urile lor.
*   **Suport TikTok:** S-a introdus suport pentru videoclipuri TikTok, cu descriere vizuală completă și transcriere audio a clipurilor.
*   **Dialog de actualizare reproiectat:** Oferă o interfață nouă și accesibilă, cu o casetă de text derulabilă, pentru citirea clară a modificărilor versiunii înainte de instalare.
*   **Stare și experiență unificate:** Dialogurile de fișiere au fost standardizate în tot suplimentul, iar comanda 'L' a fost îmbunătățită pentru raportarea progresului în timp real.

## Modificări pentru 3.6.0
*   **Sistem de ajutor:** S-a adăugat o comandă de ajutor (`H`) în Strat de comenzi, pentru o listă ușor accesibilă cu toate scurtăturile și funcțiile lor.
*   **Analiză video online:** Suportul a fost extins pentru a include videoclipuri **Twitter (X)**. Au fost îmbunătățite și detectarea URL-urilor și stabilitatea, pentru o experiență mai fiabilă.
*   **Contribuție la proiect:** S-a adăugat un dialog opțional de donație pentru utilizatorii care doresc să sprijine actualizările viitoare și creșterea continuă a proiectului.

## Modificări pentru 3.5.0
\*   \*\*Strat de comenzi:\*\* S-a introdus un sistem de Strat de comenzi (implicit: `NVDA+Shift+V`) pentru gruparea scurtăturilor sub o singură tastă principală. De exemplu, în loc să apeși `NVDA+Control+Shift+T` pentru traducere, acum apeși `NVDA+Shift+V`, apoi `T`.
\*   \*\*Analiză video online:\*\* S-a adăugat o funcție nouă pentru analizarea directă a videoclipurilor YouTube și Instagram prin furnizarea unui URL.

## Modificări pentru 3.1.0
*   **Mod ieșire directă:** S-a adăugat o opțiune pentru a sări peste dialogul de chat și a auzi răspunsurile IA direct prin voce, pentru o experiență mai rapidă și mai fluidă.
*   **Integrare clipboard:** S-a adăugat o setare nouă pentru copierea automată a răspunsurilor IA în clipboard.

## Modificări pentru 3.0

*   **Limbi noi:** S-au adăugat traduceri în **persană** și **vietnameză**.
*   **Modele IA extinse:** Lista de selecție a modelelor a fost reorganizată cu prefixe clare (`[Free]`, `[Pro]`, `[Auto]`) pentru a ajuta utilizatorii să distingă între modele gratuite și modele cu limită de rată sau plătite. S-a adăugat suport pentru **Gemini 3.0 Pro** și **Gemini 2.0 Flash Lite**.
*   **Stabilitatea dictării:** Stabilitatea Dictării inteligente a fost îmbunătățită semnificativ. S-a adăugat o verificare de siguranță pentru ignorarea clipurilor audio mai scurte de o secundă, prevenind halucinațiile IA și erorile goale.
*   **Gestionarea fișierelor:** S-a remediat o problemă în care încărcarea fișierelor cu nume care nu erau în engleză eșua.
*   **Optimizare prompturi:** S-au îmbunătățit logica Traducerii și rezultatele structurate de Viziune.

## Modificări pentru 2.9

*   **S-au adăugat traduceri în franceză și turcă.**
*   **Vizualizare formatată:** S-a adăugat un buton "Vezi formatat" în dialogurile de chat, pentru vizualizarea conversației cu formatare corectă, precum titluri, bold și cod, într-o fereastră standard navigabilă.
*   **Setare Markdown:** S-a adăugat opțiunea nouă "Curăță Markdown în chat" în Setări. Debifarea acesteia permite utilizatorilor să vadă sintaxa Markdown brută, de exemplu `**` și `#`, în fereastra de chat.
*   **Gestionarea dialogurilor:** S-a remediat o problemă în care ferestrele "Rafinare text" sau de chat se deschideau de mai multe ori sau nu primeau focus corect.
*   **Îmbunătățiri UX:** Titlurile dialogurilor de fișiere au fost standardizate la "Deschide" și au fost eliminate anunțurile vocale redundante, de exemplu "Se deschide meniul...", pentru o experiență mai fluidă.

## Modificări pentru 2.8
* S-a adăugat traducerea în italiană.
* **Raportare stare:** S-a adăugat o comandă nouă (NVDA+Control+Shift+I) pentru anunțarea stării curente a suplimentului, de exemplu "Se încarcă..." sau "Se analizează...".
* **Export HTML:** Butonul "Salvează conținutul" din dialogurile de rezultate salvează acum ieșirea ca fișier HTML formatat, păstrând stiluri precum titlurile și textul bold.
* **Interfață setări:** S-a îmbunătățit aspectul panoului de setări prin grupare accesibilă.
* **Modele noi:** S-a adăugat suport pentru gemini-flash-latest și gemini-flash-lite-latest.
* **Limbi:** S-a adăugat limba nepaleză la limbile acceptate.
* **Logica meniului de rafinare:** S-a remediat o eroare critică în care comenzile "Rafinare text" eșuau dacă limba interfeței NVDA nu era engleza.
* **Dictare:** Detectarea tăcerii a fost îmbunătățită pentru a preveni afișarea unui text incorect când nu este detectată vorbire.
* **Setări de actualizare:** "Verifică actualizările la pornire" este acum dezactivată implicit pentru respectarea politicilor Add-on Store.
* Curățare cod.

## Modificări pentru 2.7
* Structura proiectului a fost migrată la șablonul oficial NV Access pentru suplimente, pentru respectarea mai bună a standardelor.
* S-a implementat o logică de reîncercare automată pentru erorile HTTP 429 (limită de rată), pentru fiabilitate în perioade cu trafic ridicat.
* Prompturile de traducere au fost optimizate pentru acuratețe mai mare și gestionare mai bună a logicii "Schimb inteligent".
* S-a actualizat traducerea în rusă.

## Modificări pentru 2.6
* S-a adăugat suport pentru traducerea în rusă (mulțumiri nvda-ru).
* Mesajele de eroare au fost actualizate pentru feedback mai descriptiv privind conectivitatea.
* Limba țintă implicită a fost schimbată în engleză.

## Modificări pentru 2.5
* S-a adăugat comanda nativă OCR pentru fișiere (NVDA+Control+Shift+F).
* S-a adăugat butonul "Salvează chatul" în dialogurile de rezultate.
* S-a implementat suport complet pentru localizare (i18n).
* Feedbackul audio a fost migrat la modulul nativ de tonuri al NVDA.
* S-a trecut la Gemini File API pentru gestionarea mai bună a fișierelor PDF și audio.
* S-a remediat blocarea la traducerea textului care conține acolade.

## Modificări pentru 2.1.1
* S-a remediat o problemă în care variabila [file_ocr] nu funcționa corect în Prompturi personalizate.

## Modificări pentru 2.1
* Toate scurtăturile au fost standardizate pentru a folosi NVDA+Control+Shift, ca să se elimine conflictele cu aspectul Laptop al NVDA și cu tastele rapide de sistem.

## Modificări pentru 2.0
* S-a implementat sistemul integrat de actualizare automată.
* S-a adăugat cache de traducere inteligentă pentru recuperarea instantanee a textului tradus anterior.
* S-a adăugat memorie de conversație pentru rafinarea contextuală a rezultatelor în dialogurile de chat.
* S-a adăugat comanda dedicată de traducere din clipboard (NVDA+Control+Shift+Y).
* Prompturile IA au fost optimizate pentru impunerea strictă a limbii țintă la ieșire.
* S-a remediat blocarea cauzată de caractere speciale în textul introdus.

## Modificări pentru 1.5
* S-a adăugat suport pentru peste 20 de limbi noi.
* S-a implementat dialogul interactiv de rafinare pentru întrebări ulterioare.
* S-a adăugat funcția nativă de Dictare inteligentă.
* S-a adăugat categoria "Vision Assistant" în dialogul Gesturi de intrare al NVDA.
* S-au remediat blocări COMError în aplicații specifice precum Firefox și Word.
* S-a adăugat mecanism de reîncercare automată pentru erori de server.

## Modificări pentru 1.0
* Lansare inițială.
