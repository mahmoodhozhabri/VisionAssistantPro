# Documentația Vision Assistant Pro

**Vision Assistant Pro** este un asistent AI multimodal avansat pentru NVDA. Folosește motoare AI de top pentru citire inteligentă a ecranului, traducere, dictare vocală și analiză de documente.

_Acest add-on a fost lansat pentru comunitate cu ocazia Zilei Internaționale a Persoanelor cu Dizabilități._

## 1. Instalare și configurare

Mergi la **Meniul NVDA > Preferințe > Setări > Vision Assistant Pro**.

### 1.1 Setări de conexiune
- **Furnizor:** Selectează serviciul AI preferat. Furnizorii acceptați includ **Google Gemini**, **OpenAI**, **Mistral**, **Groq** și **Personalizat** (servere compatibile OpenAI, cum ar fi Ollama, LM Studio, Jan.ai sau KoboldCPP).
- **Notă importantă:** Recomandăm **Google Gemini** pentru cea mai bună performanță și acuratețe, mai ales pentru analiza imaginilor și fișierelor.
- **Cheie API:** Obligatorie. Poți introduce mai multe chei, separate prin virgulă sau pe linii diferite, pentru rotație automată.
- **Preia modelele:** După ce introduci cheia API, apasă acest buton pentru a descărca lista recentă de modele disponibile de la furnizor.
- **Model AI:** Selectează modelul principal folosit pentru chat general și analiză.

### 1.2 Rutare avansată a modelelor
*Disponibilă pentru toți furnizorii, inclusiv Gemini, OpenAI, Groq, Mistral și Personalizat.*

> **⚠️ Avertisment:** Aceste setări sunt destinate doar utilizatorilor avansați. Dacă nu știi sigur ce face un anumit model, lasă această opțiune **nebifată**. Selectarea unui model incompatibil pentru o sarcină, de exemplu un model doar text pentru Vision, va produce erori și va opri funcționarea add-on-ului.

Bifează **"Rutare avansată a modelelor (specifică sarcinii)"** pentru a debloca un control detaliat. Această opțiune îți permite să selectezi modele specifice din lista derulantă pentru diferite sarcini:
- **Model OCR / Vision:** Alege un model specializat pentru analiza imaginilor.
- **Speech-to-Text (STT):** Alege un model specific pentru dictare.
- **Text-to-Speech (TTS):** Alege un model pentru generarea sunetului.
- **Model AI Operator:** Selectează un model specific pentru sarcini autonome de operare a calculatorului.
*Notă: Funcțiile neacceptate, de exemplu TTS pentru Groq, vor fi ascunse automat.*

### 1.3 Configurare avansată a endpointurilor (furnizor personalizat)
*Disponibilă doar când este selectat „Personalizat”.*

> **⚠️ Avertisment:** Această secțiune permite configurarea manuală a API-ului și este proiectată pentru **utilizatori experimentați** care rulează servere locale sau proxy-uri. URL-urile sau numele de modele greșite vor întrerupe conexiunea. Dacă nu știi exact ce sunt aceste endpointuri, lasă această opțiune **nebifată**.

Bifează **"Configurare avansată a endpointurilor"** pentru a introduce manual detaliile serverului. Spre deosebire de furnizorii nativi, aici trebuie să **tastezi** URL-urile și numele de modele specifice:
- **URL listă de modele:** Endpointul pentru preluarea modelelor disponibile.
- **URL endpoint OCR/STT/TTS:** URL-uri complete pentru servicii specifice, de exemplu `http://localhost:11434/v1/audio/speech`.
- **Modele personalizate:** Tastează manual numele modelului, de exemplu `llama3:8b`, pentru fiecare sarcină.

### 1.3.1 Configurare AI local (configurare dintr-o singură acțiune)
Pentru a face integrarea AI locală, complet offline, foarte simplă, un buton dedicat **„Configurează AI local”** este disponibil în Setările furnizorului personalizat.

Dacă rulezi un server de modele AI local pe computer:
1. Selectează **Personalizat** ca furnizor.
2. Apasă butonul **Configurează AI local**.
3. Alege motorul AI local din dialogul accesibil:
   - **Ollama** (implicit `http://127.0.0.1:11434`)
   - **LM Studio** (implicit `http://127.0.0.1:1234`)
   - **Jan.ai** (implicit `http://127.0.0.1:1337`)
   - **KoboldCPP** (implicit `http://127.0.0.1:5001`)
4. Add-on-ul configurează instant URL-ul local corect, tipul API și preia automat modelele tale offline active pentru a completa caseta de selecție **Model AI**.

*Notă despre rețea și proxy-uri:* Acest motor de conexiune locală include un mecanism avansat de ocolire a proxy-ului. Chiar dacă rulezi un VPN de sistem activ sau un proxy în modul TUN, solicitările tale către AI local îl vor ocoli complet, asigurând conexiuni offline stabile fără erori 502 Bad Gateway.

### 1.4 Preferințe generale
- **Motor OCR:** Alege între **Chrome (Rapid)** pentru rezultate rapide sau **AI (Avansat)** pentru păstrarea mai bună a structurii.
    - *Notă:* Dacă selectezi „AI (Avansat)”, dar furnizorul tău este setat la OpenAI/Groq, add-on-ul va direcționa inteligent imaginea către modelul Vision al furnizorului activ.
- **Voce TTS:** Selectează stilul de voce preferat. Această listă se actualizează dinamic în funcție de furnizorul activ.
- **Creativitate (Temperature):** Controlează nivelul de aleatoriu al AI-ului. Valorile mai mici sunt mai bune pentru traduceri și OCR exacte.
- **URL proxy:** Configurează această opțiune dacă serviciile AI sunt restricționate în regiunea ta. Acceptă proxy-uri locale, cum ar fi `127.0.0.1`, sau URL-uri bridge.

## 2. Strat de comenzi și scurtături

Pentru a preveni conflictele de tastatură, acest add-on folosește un **strat de comenzi**.
1. Apasă **NVDA + Shift + V** (tasta principală) pentru a activa stratul. Vei auzi un bip.
2. Eliberează tastele, apoi apasă una dintre următoarele taste simple:

| Tastă         | Funcție                  | Descriere                                                                   |
|---------------|--------------------------|-----------------------------------------------------------------------------|
| **Shift + A** | **AI Operator**          | **Operare autonomă:** Spune-i AI-ului să execute o sarcină pe ecranul tău. Dacă o apeși din nou, oprește instant operațiile active. |
| **E**         | **UI Explorer**          | **Click interactiv:** Identifică și apasă elemente UI în orice aplicație.    |
| **T**         | Traducător inteligent    | Traduce textul de sub cursorul navigatorului sau selecția.                  |
| **Shift + T** | Traducător clipboard     | Traduce conținutul aflat acum în clipboard.                                 |
| **R**         | Rafinator de text        | Rezumă, corectează gramatica, explică sau rulează **prompturi personalizate**. |
| **V**         | Vision pentru obiect     | Descrie obiectul curent al navigatorului.                                   |
| **O**         | Vision pentru ecran complet | Analizează structura și conținutul întregului ecran.                    |
| **Shift + V** | Analiză video online     | Analizează videoclipuri **YouTube**, **Instagram**, **TikTok** sau **Twitter (X)**. |
| **D**         | Cititor de documente     | Cititor avansat pentru PDF și imagini, cu selectare a intervalului de pagini. |
| **F**         | **Acțiune inteligentă pentru fișiere** | Recunoaștere adaptată contextului din imagini, PDF-uri sau fișiere TIFF selectate. |
| **A**         | Transcriere audio        | Transcrie fișiere MP3, WAV sau OGG în text.                                 |
| **C**         | Rezolvare CAPTCHA        | Capturează și rezolvă CAPTCHA-uri. Acceptă portaluri guvernamentale.         |
| **S**         | Dictare inteligentă      | Convertește vorbirea în text. Apasă pentru a porni înregistrarea, apasă din nou pentru a opri și scrie textul. |
| **I**         | Raportare stare          | Anunță progresul curent, de exemplu „Se scanează...” sau „Inactiv”.          |
| **L**         | **Etichetează obiectul** | **Etichetare AI semantică:** Etichetează permanent elementul sau pictograma focalizată curent. |
| **Shift + L** | **Gestionează/scanează etichetele** | Deschide Managerul de etichete, dacă există etichete, sau scanează aplicația pentru elemente fără nume. |
| **U**         | Verificare actualizări   | Verifică manual pe GitHub cea mai recentă versiune a add-on-ului.            |
| **Space**     | Reafișează ultimul rezultat | Arată ultimul răspuns AI într-un dialog de chat pentru revizuire sau continuare. |
| **H**         | Ajutor comenzi           | Afișează lista tuturor scurtăturilor disponibile.                           |

### 2.1 Scurtături pentru cititorul de documente (în vizualizator)
- **Ctrl + PageDown:** Mută-te la pagina următoare.
- **Ctrl + PageUp:** Mută-te la pagina anterioară.
- **Alt + A:** Deschide un dialog de chat pentru a pune întrebări despre document.
- **Alt + R:** Forțează o **rescanare cu AI** folosind furnizorul activ.
- **Alt + G:** Generează și salvează un fișier audio de calitate înaltă (WAV/MP3). *Ascuns dacă furnizorul nu acceptă TTS.*
- **Alt + S / Ctrl + S:** Salvează textul extras ca fișier TXT sau HTML.

## 3. Prompturi personalizate și variabile

Poți gestiona prompturile în **Setări > Prompturi > Gestionează prompturile...**.

### Variabile acceptate
- `[selection]`: Textul selectat în prezent.
- `[clipboard]`: Conținutul clipboardului.
- `[screen_obj]`: Captură de ecran a obiectului navigatorului.
- `[screen_full]`: Captură de ecran complet.
- `[file_ocr]`: Selectează un fișier imagine/PDF pentru extragerea textului.
- `[file_read]`: Selectează un document pentru citire (TXT, cod, PDF).
- `[file_audio]`: Selectează un fișier audio pentru analiză (MP3, WAV, OGG).

***
**Notă:** Este necesară o conexiune activă la internet pentru toate funcțiile AI. Documentele cu mai multe pagini sunt procesate automat.

## 4. Suport și comunitate

Rămâi la curent cu cele mai recente noutăți, funcții și lansări:
- **Canal Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Probleme GitHub:** Pentru raportări de erori și cereri de funcții.

## 5. Susținătorii proiectului

Le mulțumim membrilor comunității care susțin dezvoltarea și întreținerea continuă a acestui proiect prin contribuții financiare generoase:

*   **@Alyabani94**
*   **Ali Alamri**
*   **Ilya**

*Dacă vrei să susții financiar proiectul și să îți vezi numele aici, poți găsi opțiunea **Donează** în meniul Instrumente al NVDA, în submeniul Vision Assistant, sau în timpul configurării după instalare.*


---
## Modificări pentru 6.1.0

*   **Integrare universală cu AI local (Configurează AI local)**: A fost adăugat un nou buton **„Configurează AI local”** în Setările furnizorului personalizat. Utilizatorii pot configura automat și instant motoare AI locale, inclusiv **Ollama**, **LM Studio**, **Jan.ai** și **KoboldCPP**.
*   **Ocolire inteligentă a proxy-ului local**: Logica de conexiune a fost reconstruită cu un mecanism avansat de ocolire a proxy-ului. Add-on-ul poate acum ocoli complet proxy-urile de sistem Windows pentru conexiunile locale de tip loopback, asigurând conexiuni stabile cu AI local chiar și când VPN-ul sau proxy-ul în modul TUN este activ.
*   **Etichetare AI ultra-stabilă (v2)**: Cheile bazate pe coordonate absolute de ecran au fost înlocuite cu un sistem avansat, hibrid, de **Semnătură a obiectului**. Etichetele se bazează acum pe identificatori programatici (UIA **AutomationId** sau Win32 **ControlID**) și pe coordonate relative la fereastră, făcând etichetele tale personalizate rezistente la redimensionarea, mutarea sau scalarea ferestrei și la schimbarea monitorului.
*   **Migrare automată fără întreruperi a etichetelor**: Actualizarea este complet transparentă. Add-on-ul va migra automat etichetele tale vechi, bazate pe coordonate moștenite, în noul format stabil de amprentă în fundal, la prima focalizare, fără pierdere de date.

## Modificări pentru 6.0

*   **Introducerea etichetării AI semantice**: Utilizatorii pot eticheta permanent butoane și pictograme fără nume folosind AI. Apasă **L** pentru a eticheta obiectul curent al navigatorului, cu suport pentru focalizarea prin Tab și navigarea pe obiecte, sau **Shift+L** pentru a scana și eticheta întreaga aplicație dintr-o singură acțiune.
*   **Gestionare inteligentă a etichetelor**: A fost adăugat un dialog nou, complet accesibil, Manager de etichete, prin **Shift+L** dacă există etichete, pentru vizualizarea, redenumirea sau ștergerea în lot a etichetelor personalizate.
*   **Analiză directă a fișierelor, fără dialogul de fișiere**: Add-on-ul poate detecta acum dacă focalizezi un fișier PDF sau imagine în Windows File Explorer. Când apeși **F (Acțiune inteligentă pentru fișiere)** sau **D (Cititor de documente)** pe un fișier evidențiat, acesta va fi procesat imediat, fără dialogul standard „Deschide”.

## Modificări pentru 5.6

*   **A fost adăugat motorul OCR „None (Extract Text Layer)”**: Utilizatorii pot extrage acum text direct din PDF-uri căutabile fără a folosi credite AI. Acest lucru îmbunătățește mult viteza și confidențialitatea pentru documentele bazate pe text.
*   **A fost rafinată acuratețea UI Explorer**: Promptul UI Explorer a fost îmbunătățit pentru a identifica mai bine tipurile de elemente, cum ar fi elementele de listă, și pentru a raporta corect stări precum „(Bifat)”, „(Selectat)” sau „(Extins)”, ignorând componentele de sistem Windows precum bara de activități și ceasul.
*   **Memento pentru configurare după instalare**: A fost adăugată o notificare după instalare pentru a ghida utilizatorii către meniul de setări, unde își pot configura cheile API și preferințele.

## Modificări pentru 5.5.2

*   **A fost remediată problema de tastare din AI Operator:** A fost rezolvată o eroare prin care litera „v” era tastată în loc să se lipească textul pe anumite sisteme. Remedierea rezolvă conflictele de sincronizare care apăreau când sistemul era foarte solicitat.
*   **Stabilitate îmbunătățită:** A fost adăugată gestionare robustă a erorilor pentru operațiile cu clipboardul, pentru a preveni blocarea add-on-ului când clipboardul sistemului este blocat temporar de alte aplicații.
*   **Optimizare de sincronizare:** Au fost ajustate întârzierile interne pentru evenimentele de tastatură, pentru fiabilitate mai mare pe sisteme cu viteze diferite și compatibilitate mai bună cu manageri de clipboard terți.

## Modificări pentru 5.5 (actualizarea pentru automatizare)

*   **AI Operator (control autonom, Shift+A):** Aceasta este funcția principală din v5.5. Vision Assistant Pro a trecut de la rolul de asistent pasiv la rolul de **AI Operator** personal. Nu descrie doar ecranul, ci execută comenzi.
    *   *Cum funcționează:* Acum poți da instrucțiuni verbale pentru a opera calculatorul. De exemplu, într-o aplicație complet inaccesibilă, unde cititorul tău de ecran nu spune nimic, poți apăsa **Shift+A** și poți tasta: *„Apasă butonul Setări”* sau *„Găsește câmpul de căutare, scrie 'Latest News' și apasă Enter.”* AI-ul identifică vizual elementele, mută mouse-ul și execută sarcina pentru tine.
    *   *Notă de performanță:* Această funcție este optimizată pentru **Gemini 3.0 Flash (Preview)** și oferă răspunsuri rapide și inteligente, capabile să gestioneze chiar și structuri UI complexe.
    *   **⚠️ Avertisment privind utilizarea API:** Pentru ca AI Operator să fie precis, trebuie să „vadă” exact ce se întâmplă, deci trimite o captură de ecran de înaltă rezoluție la fiecare pas. Folosirea frecventă va consuma cota API mult mai repede decât sarcinile standard bazate pe text.
*   **Visual UI Explorer (E):** Te-ai săturat să navighezi prin „butoane fără etichetă”? Apasă **E** pentru a activa UI Explorer. AI-ul va scana întreaga fereastră și va genera o listă cu fiecare element pe care îl poate apăsa, inclusiv pictograme, grafice și meniuri. Alegi un element din listă, iar AI Operator îl va apăsa pentru tine. Funcționează ca un strat accesibil peste orice aplicație.
*   **Acțiune inteligentă pentru fișiere, adaptată contextului (F):** Tasta „F” a fost refăcută complet. Nu mai presupune că vrei doar OCR. Când selectezi o singură imagine, acum îți cere intenția: poți alege o **descriere vizuală detaliată** pentru a înțelege scena sau o **extragere structurată a textului (OCR)** pentru citire. Meniul se adaptează dinamic în funcție de tipul de fișier și motorul AI activ.
*   **Optimizare de bază:** Am curățat în profunzime logica internă a add-on-ului, eliminând funcții vechi nefolosite și cod redundant. Rezultatul este o experiență mai rapidă și mai fiabilă pentru utilizatori.

## Modificări pentru 5.0

* **Arhitectură cu mai mulți furnizori**: A fost adăugat suport complet pentru **OpenAI**, **Groq** și **Mistral**, alături de Google Gemini. Utilizatorii pot alege acum backendul AI preferat.
* **Rutare avansată a modelelor**: Utilizatorii furnizorilor nativi, precum Gemini sau OpenAI, pot selecta acum modele specifice dintr-o listă derulantă pentru sarcini diferite (OCR, STT, TTS).
* **Configurare avansată a endpointurilor**: Utilizatorii furnizorului personalizat pot introduce manual URL-uri și nume de modele pentru control detaliat asupra serverelor locale sau terțe.
* **Vizibilitate inteligentă a funcțiilor**: Meniul de setări și interfața cititorului de documente ascund acum automat funcțiile neacceptate, cum ar fi TTS, în funcție de furnizorul selectat.
* **Preluare dinamică a modelelor**: Add-on-ul preia acum lista de modele disponibile direct din API-ul furnizorului, pentru compatibilitate cu modele noi imediat după lansare.
* **OCR și traducere hibridă**: A fost optimizată logica pentru a folosi Google Translate pentru viteză când este folosit Chrome OCR și traducere prin AI când sunt folosite motoarele Gemini/Groq/OpenAI.
* **„Rescanare cu AI” universală**: Funcția de rescanare din cititorul de documente nu mai este limitată la Gemini. Acum folosește furnizorul AI activ pentru a reprocesa paginile.

## Modificări pentru 4.6
* **Reafișare interactivă a rezultatului:** A fost adăugată tasta **Space** în stratul de comenzi, permițând utilizatorilor să redeschidă imediat ultimul răspuns AI într-o fereastră de chat pentru întrebări suplimentare, chiar și când modul „Ieșire directă” este activ.
* **Hub pentru comunitatea Telegram:** A fost adăugat un link „Canal Telegram oficial” în meniul Instrumente al NVDA, pentru acces rapid la cele mai recente noutăți, funcții și lansări.
* **Stabilitate îmbunătățită a răspunsurilor:** Logica principală pentru funcțiile de traducere, OCR și Vision a fost optimizată pentru performanță mai fiabilă și experiență mai fluidă când se folosește ieșirea vocală directă.
* **Ghidare îmbunătățită în interfață:** Descrierile din setări și documentația au fost actualizate pentru a explica mai bine noul sistem de reafișare și modul în care funcționează împreună cu setările pentru ieșire directă.

## Modificări pentru 4.5
* **Manager avansat de prompturi:** A fost introdus un dialog dedicat de administrare în setări, pentru personalizarea prompturilor de sistem implicite și gestionarea prompturilor definite de utilizator, cu suport complet pentru adăugare, editare, reordonare și previzualizare.
* **Suport proxy complet:** Au fost rezolvate problemele de conexiune la rețea prin aplicarea strictă a setărilor proxy configurate de utilizator pentru toate cererile API, inclusiv traducere, OCR și generare vocală.
* **Migrare automată a datelor:** A fost integrat un sistem inteligent de migrare, care actualizează automat configurațiile vechi ale prompturilor la un format JSON v2 robust la prima rulare, fără pierdere de date.
* **Compatibilitate actualizată (2025.1):** Versiunea minimă necesară de NVDA a fost setată la 2025.1, din cauza dependențelor de bibliotecă din funcții avansate precum cititorul de documente, pentru performanță stabilă.
* **Interfață de setări optimizată:** Interfața de setări a fost simplificată prin reorganizarea gestionării prompturilor într-un dialog separat, oferind o experiență mai curată și mai accesibilă.
* **Ghid pentru variabilele prompturilor:** A fost adăugat un ghid integrat în dialogurile de prompturi pentru a ajuta utilizatorii să identifice și să folosească ușor variabile dinamice precum [selection], [clipboard] și [screen_obj].

## Modificări pentru 4.0.3
*   **Rezistență îmbunătățită a rețelei:** A fost adăugat un mecanism automat de reîncercare pentru a gestiona mai bine conexiunile instabile la internet și erorile temporare de server, asigurând răspunsuri AI mai fiabile.
*   **Dialog vizual pentru traduceri:** A fost introdusă o fereastră dedicată pentru rezultatele traducerii. Utilizatorii pot naviga și citi ușor traduceri lungi linie cu linie, similar cu rezultatele OCR.
*   **Vizualizare formatată agregată:** Funcția „Vizualizare formatată” din cititorul de documente afișează acum toate paginile procesate într-o singură fereastră organizată, cu antete clare pentru pagini.
*   **Flux OCR optimizat:** Selectarea intervalului de pagini este omisă automat pentru documentele cu o singură pagină, făcând procesul de recunoaștere mai rapid.
*   **Stabilitate API îmbunătățită:** S-a trecut la o metodă mai robustă de autentificare bazată pe antete, rezolvând posibile erori „All API Keys failed” cauzate de conflicte la rotația cheilor.
*   **Remedieri de erori:** Au fost rezolvate mai multe blocări posibile, inclusiv o problemă la închiderea add-on-ului și o eroare de focalizare în dialogul de chat.

## Modificări pentru 4.0.1
*   **Cititor de documente avansat:** Un vizualizator nou pentru PDF și imagini, cu selectare a intervalului de pagini, procesare în fundal și navigare fluentă cu `Ctrl+PageUp/Down`.
*   **Submeniu nou în Instrumente:** A fost adăugat un submeniu dedicat „Vision Assistant” în meniul Instrumente al NVDA, pentru acces mai rapid la funcțiile principale, setări și documentație.
*   **Personalizare flexibilă:** Acum poți alege motorul OCR și vocea TTS preferate direct din panoul de setări.
*   **Suport pentru mai multe chei API:** A fost adăugat suport pentru mai multe chei API Gemini. Poți introduce o cheie pe linie sau le poți separa prin virgulă în setări.
*   **Motor OCR alternativ:** A fost introdus un motor OCR nou pentru a asigura recunoaștere fiabilă a textului chiar și când sunt atinse limitele de cotă Gemini API.
*   **Rotație inteligentă a cheilor API:** Comută automat la cea mai rapidă cheie API funcțională și o reține, pentru a evita limitele de cotă.
*   **Document în MP3/WAV:** A fost integrată capacitatea de a genera și salva fișiere audio de calitate înaltă în formatele MP3 (128kbps) și WAV direct în cititor.
*   **Suport pentru Instagram Stories:** A fost adăugată capacitatea de a descrie și analiza Instagram Stories folosind URL-urile lor.
*   **Suport TikTok:** A fost introdus suport pentru videoclipuri TikTok, permițând descriere vizuală completă și transcriere audio a clipurilor.
*   **Dialog de actualizare reproiectat:** Include o interfață accesibilă nouă, cu o casetă text derulabilă pentru citirea clară a modificărilor de versiune înainte de instalare.
*   **Stare și UX unificate:** Dialogurile de fișiere au fost standardizate în tot add-on-ul, iar comanda „L” a fost îmbunătățită pentru raportarea progresului în timp real.

## Modificări pentru 3.6.0
*   **Sistem de ajutor:** A fost adăugată o comandă de ajutor (`H`) în stratul de comenzi, pentru a oferi o listă ușor accesibilă cu toate scurtăturile și funcțiile lor.
*   **Analiză video online:** Suportul a fost extins pentru a include videoclipuri **Twitter (X)**. Detectarea URL-urilor și stabilitatea au fost îmbunătățite pentru o experiență mai fiabilă.
*   **Contribuție la proiect:** A fost adăugat un dialog opțional de donație pentru utilizatorii care vor să susțină actualizările viitoare și creșterea continuă a proiectului.

## Modificări pentru 3.5.0
\*   \*\*Strat de comenzi:\*\* A fost introdus un sistem de strat de comenzi, implicit `NVDA+Shift+V`, pentru a grupa scurtăturile sub o singură tastă principală. De exemplu, în loc să apeși `NVDA+Control+Shift+T` pentru traducere, acum apeși `NVDA+Shift+V`, apoi `T`.
\*   \*\*Analiză video online:\*\* A fost adăugată o funcție nouă pentru analiza videoclipurilor YouTube și Instagram direct prin introducerea unui URL.

## Modificări pentru 3.1.0
*   **Mod ieșire directă:** A fost adăugată o opțiune pentru a omite dialogul de chat și a auzi răspunsurile AI direct prin vorbire, pentru o experiență mai rapidă.
*   **Integrare cu clipboardul:** A fost adăugată o setare nouă pentru copierea automată a răspunsurilor AI în clipboard.

## Modificări pentru 3.0

*   **Limbi noi:** Au fost adăugate traduceri în **persană** și **vietnameză**.
*   **Modele AI extinse:** Lista de selectare a modelelor a fost reorganizată cu prefixe clare (`[Free]`, `[Pro]`, `[Auto]`), pentru a ajuta utilizatorii să distingă modelele gratuite de cele limitate prin rată sau plătite. A fost adăugat suport pentru **Gemini 3.0 Pro** și **Gemini 2.0 Flash Lite**.
*   **Stabilitate pentru dictare:** Stabilitatea dictării inteligente a fost îmbunătățită mult. A fost adăugată o verificare de siguranță care ignoră clipurile audio mai scurte de 1 secundă, prevenind halucinațiile AI și erorile goale.
*   **Gestionarea fișierelor:** A fost remediată o problemă prin care încărcarea fișierelor cu nume non-englezești eșua.
*   **Optimizarea prompturilor:** Logica de traducere și rezultatele Vision structurate au fost îmbunătățite.
## Modificări pentru 2.9

*   **Au fost adăugate traduceri în franceză și turcă.**
*   **Vizualizare formatată:** A fost adăugat un buton „Vizualizare formatată” în dialogurile de chat, pentru a vedea conversația cu stilizare corectă, cum ar fi titluri, bold și cod, într-o fereastră standard navigabilă.
*   **Setare Markdown:** A fost adăugată o opțiune nouă „Curăță Markdown în chat” în Setări. Debifarea acesteia permite utilizatorilor să vadă sintaxa Markdown brută, de exemplu `**` sau `#`, în fereastra de chat.
*   **Gestionarea dialogurilor:** A fost remediată o problemă prin care ferestrele „Rafinează textul” sau chat se deschideau de mai multe ori sau nu primeau focalizarea corect.
*   **Îmbunătățiri UX:** Titlurile dialogurilor de fișiere au fost standardizate la „Deschide” și au fost eliminate anunțurile vocale redundante, de exemplu „Se deschide meniul...”, pentru o experiență mai fluidă.

## Modificări pentru 2.8
* A fost adăugată traducerea în italiană.
* **Raportare stare:** A fost adăugată o comandă nouă (NVDA+Control+Shift+I) pentru anunțarea stării curente a add-on-ului, de exemplu „Se încarcă...” sau „Se analizează...”.
* **Export HTML:** Butonul „Salvează conținutul” din dialogurile de rezultat salvează acum ieșirea ca fișier HTML formatat, păstrând stiluri precum titluri și text bold.
* **Interfață de setări:** Aspectul panoului Setări a fost îmbunătățit cu grupare accesibilă.
* **Modele noi:** A fost adăugat suport pentru gemini-flash-latest și gemini-flash-lite-latest.
* **Limbi:** A fost adăugată nepaleza la limbile acceptate.
* **Logica meniului de rafinare:** A fost remediată o eroare critică prin care comenzile „Rafinează textul” eșuau dacă limba interfeței NVDA nu era engleza.
* **Dictare:** Detectarea tăcerii a fost îmbunătățită pentru a preveni ieșiri text incorecte când nu este detectată vorbire.
* **Setări de actualizare:** „Caută actualizări la pornire” este acum dezactivată implicit pentru respectarea politicilor Add-on Store.
* Curățare cod.

## Modificări pentru 2.7
* Structura proiectului a fost migrată la șablonul oficial NV Access Add-on Template, pentru conformitate mai bună cu standardele.
* A fost implementată logica de reîncercare automată pentru erori HTTP 429 (limită de rată), pentru fiabilitate în perioade cu trafic ridicat.
* Prompturile de traducere au fost optimizate pentru acuratețe mai mare și gestionare mai bună a logicii „Smart Swap”.
* Traducerea în rusă a fost actualizată.

## Modificări pentru 2.6
* A fost adăugat suport pentru traducerea în rusă, mulțumiri nvda-ru.
* Mesajele de eroare au fost actualizate pentru feedback mai descriptiv privind conectivitatea.
* Limba țintă implicită a fost schimbată în engleză.

## Modificări pentru 2.5
* A fost adăugată comanda nativă OCR pentru fișiere (NVDA+Control+Shift+F).
* A fost adăugat butonul „Salvează chatul” în dialogurile de rezultat.
* A fost implementat suport complet pentru localizare (i18n).
* Feedbackul audio a fost migrat la modulul nativ de tonuri al NVDA.
* S-a trecut la Gemini File API pentru gestionarea mai bună a fișierelor PDF și audio.
* A fost remediată blocarea la traducerea textului care conține acolade.

## Modificări pentru 2.1.1
* A fost remediată o problemă prin care variabila [file_ocr] nu funcționa corect în prompturile personalizate.

## Modificări pentru 2.1
* Toate scurtăturile au fost standardizate pentru a folosi NVDA+Control+Shift, pentru a elimina conflictele cu aspectul Laptop al NVDA și tastele rapide de sistem.

## Modificări pentru 2.0
* A fost implementat sistemul integrat de actualizare automată.
* A fost adăugat cache inteligent pentru traduceri, pentru recuperarea instantanee a textului tradus anterior.
* A fost adăugată memorie conversațională pentru rafinarea contextuală a rezultatelor în dialogurile de chat.
* A fost adăugată o comandă dedicată pentru traducerea clipboardului (NVDA+Control+Shift+Y).
* Prompturile AI au fost optimizate pentru a impune strict ieșirea în limba țintă.
* A fost remediată blocarea cauzată de caractere speciale în textul de intrare.

## Modificări pentru 1.5
* A fost adăugat suport pentru peste 20 de limbi noi.
* A fost implementat dialogul interactiv de rafinare pentru întrebări suplimentare.
* A fost adăugată funcția nativă de dictare inteligentă.
* A fost adăugată categoria „Vision Assistant” în dialogul Gesturi de intrare al NVDA.
* Au fost remediate blocările COMError în aplicații specifice precum Firefox și Word.
* A fost adăugat mecanismul automat de reîncercare pentru erori de server.

## Modificări pentru 1.0
* Lansare inițială.
