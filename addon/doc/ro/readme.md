# Documentația Vision Assistant Pro

<!-- DOWNLOAD_COUNT_START --> Total descărcări: 75.451 <!-- DOWNLOAD_COUNT_END -->

**Vision Assistant Pro** este un asistent AI avansat, multimodal, pentru NVDA. Folosește motoare AI de clasă mondială pentru a oferi citire inteligentă a ecranului, traducere, dictare vocală și analiză de documente.

_Acest add-on a fost lansat comunității în onoarea Zilei Internaționale a Persoanelor cu Dizabilități._

## 1. Instalare și configurare

Mergi la **Meniul NVDA > Preferințe > Setări > Vision Assistant Pro**. Dialogul de setări este organizat în 9 file accesibile: **Conexiune**, **Asistent live**, **Comportament AI**, **Limbi de traducere**, **Cititor de documente**, **Video**, **CAPTCHA**, **Prompturi** și **Avansat**.

### 1.1 Fila Conexiune

- **Furnizor:** Selectează serviciul AI preferat. Furnizorii acceptați includ **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** și **Personalizat** (servere compatibile OpenAI, precum Ollama, LM Studio, Jan.ai sau KoboldCPP).
- **Cheie API:** Introdu una sau mai multe chei API (separate prin virgule sau linii noi) pentru rotație automată.
- **Preia modelele:** Apasă acest buton după introducerea cheii API pentru a descărca cea mai recentă listă de modele disponibile de la furnizor.
- **Model AI:** Selectează modelul principal folosit pentru chat general și analiză.
- **Rutare avansată a modelelor (specifică sarcinilor):** Opțional, selectează modele dedicate din liste derulante pentru sarcini OCR, STT, TTS, AI Operator, Video și Asistent live. Pentru Gemini, modelele sunt clasificate dinamic după capabilități, fără a aglomera listele.
- **Setări furnizor personalizat:** Configurează endpointuri locale sau personalizate. Include **Configurare AI local** (configurare dintr-o singură acțiune pentru Ollama, LM Studio, Jan.ai sau KoboldCPP) și **Configurare avansată a endpointului**.
- **Configurare proxy:** Suport complet pentru tunelare și redirecționarea endpointurilor în întregul add-on (inclusiv Asistentul live, Observatorul ambiental și TTS). Introdu **URL-ul proxy** și selectează **modul proxy**:
  - **Detectare automată:** Detectează automat dacă URL-ul reprezintă un proxy de redirecționare sau un proxy invers.
  - **Proxy SOCKS5:** Impune tunelarea prin SOCKS5, cu autentificare prin nume de utilizator/parolă conform RFC 1929 și rezolvarea numelor de domeniu.
  - **Proxy HTTP:** Impune tunelarea printr-un proxy HTTP cu autentificare Basic.
  - **Proxy invers:** Înlocuirea directă a endpointului pentru gateway-uri AI personalizate și servere oglindă găzduite de tine (datele de autentificare sunt dezactivate în acest mod).
- **Testează conexiunea proxy:** Un buton care testează conectivitatea în fundal, fără a bloca interfața, și măsoară latența serverului în milisecunde (anunțată de NVDA).
- **Opțiuni de conexiune și ieșire:** Configurează verificările de actualizare la pornire, curățarea Markdown în chat, copierea răspunsurilor AI în clipboard și ieșirea directă (fără fereastră de chat).
- **Salvează chaturile în istoric:** Păstrează conversațiile tale de chat în lista Istoric.

### 1.2 Fila Asistent live

- **Asistent live: ieșire directă (fără fereastră):** Pornește Asistentul live fără fereastra sa de conversație; o poți deschide ulterior cu tasta Reapelează ultimul rezultat (`Space`).
- **Apasă pentru a vorbi:** Activează/dezactivează modul Apasă pentru a vorbi. Când este activat, microfonul transmite sunet numai cât timp ții apăsată tasta atribuită.
- **Tasta pentru Apasă pentru a vorbi:** Apasă tastele pentru a înregistra scurtătura (de exemplu, `F12` sau `Ctrl+F12`) — poți atribui chiar și un singur modificator, precum `Left Ctrl`. Ține tasta apăsată pentru a vorbi și elibereaz-o când ai terminat; un bip scurt confirmă fiecare apăsare și eliberare.

Notă: Această filă apare numai când furnizorul activ este **Google Gemini** (sau un furnizor personalizat compatibil Gemini).

### 1.3 Fila Comportament AI

- **Creativitate (temperatură):** Controlează aleatorietatea și creativitatea AI-ului (de la 0,0 la 2,0). Valorile mai mici produc rezultate mai deterministe și mai exacte pentru traducere/OCR.

### 1.4 Fila Limbi de traducere

- **Limba sursă:** Selectează limba implicită de intrare.
- **Limba țintă:** Selectează limba principală în care vrei traducerea.
- **Limba răspunsului AI:** Selectează limba pentru răspunsurile AI generale.
- **Schimbare inteligentă:** Inversează automat limbile sursă și țintă pe baza textului detectat.

### 1.5 Fila Cititor de documente

- **Motor OCR:** Alege între **Chrome (rapid)** pentru rezultate rapide sau **AI (avansat)** pentru păstrarea superioară a layoutului.
- **Dimensiune lot OCR:** Specifică numărul de pagini per cerere (setează 0 pentru procesare într-o singură cerere).
- **Descrie imagini în linie:** Activează/dezactivează descrierile de imagini în linie în timpul extragerii textului din documente.
- **Export numere pagini:** Activează/dezactivează numerele de pagină și separatoarele în rezultatele documentelor cu mai multe pagini.
- **Voce TTS:** Selectează stilul vocal implicit pentru generarea audio.
- **Salvează documentele în istoric:** Păstrează documentele deschise în lista Istoric; textul OCR din cache și datele pentru reluare sunt salvate în continuare.

### 1.6 Fila Video

- **Dimensiune segment video:** Durata segmentelor în minute pentru generarea descrierilor audio (setează 0 pentru a procesa întregul fișier).
- **Adaugă listă de personaje:** Opțiune pentru adăugarea dicționarului de personaje ca prima intrare de subtitrare.
- **Adaugă avertisment AI:** Opțiune pentru inserarea unui avertisment AI la începutul subtitrărilor SRT video.
- **Dicționar de personaje și gestionarea serialelor:** Adaugă, editează, importă sau gestionează numele, descrierile fizice și rolurile personajelor pentru fiecare serial — AI-ul asociază automat personajele descoperite cu cele din dicționar și adaugă personajele noi pe măsură ce analizezi mai multe episoade. Notele tale introduse manual sunt întotdeauna păstrate și au prioritate față de actualizările AI, iar descrierile fizice sunt actualizate de la un episod la altul.

### 1.7 Fila CAPTCHA

- **Activează rezolvitorul CAPTCHA vizual:** Activează/dezactivează rezolvarea automată a provocărilor vizuale (hCaptcha, reCAPTCHA).
- **Metodă CAPTCHA text:** Alege între capturarea **obiectului navigator** sau a **ecranului complet**.

### 1.8 Fila Prompturi

- **Gestionează prompturi:** Deschide un dialog dedicat pentru personalizarea prompturilor de sistem implicite sau pentru crearea, editarea, reordonarea și previzualizarea prompturilor personalizate definite de utilizator, cu variabile dinamice (de exemplu, `[selection]`, `[screen_fg_obj]`, `[currentURL]`, `[text]`).
- **Scurtături pentru prompturi personalizate:** Atribuie o scurtătură dedicată oricărui prompt personalizat direct din Managerul de prompturi. Apasă tastele pentru a le înregistra — tastele individuale funcționează în stratul de comenzi (și global sub forma `NVDA + Shift + key`), iar combinații precum `Control + Shift + 1` funcționează direct la nivel global.
- **Comportamentul de ieșire pentru fiecare prompt:** Alege separat cum este prezentat rezultatul fiecărui prompt (Setare globală, Copiază în clipboard, Ieșire directă / mesaj NVDA, Copiază în clipboard + ieșire directă sau Fereastră de chat).

### 1.9 Fila Avansat și jurnalizarea globală

Navighează la fila **Avansat** pentru a configura jurnalizarea globală a add-on-ului:

- **Activează fișierul jurnal dedicat:** Activează jurnalizarea tuturor evenimentelor operaționale, traficului API și erorilor din toate modulele add-on-ului într-un fișier separat (`vision_assistant.log`).
- **Nivel jurnal:** Selectează nivelul de detaliu între **Debug (toate detaliile)**, **Info (informații generale)**, **Avertisment (doar avertismente)** și **Eroare (doar erori)**.
- **Păstrează jurnalele timp de:** Setează perioade automate de păstrare pentru curățarea intrărilor vechi din jurnal (de la 1 oră până la 90 de zile).
- **Controale pentru gestionarea jurnalelor:** Folosește **Deschide fișierul jurnal**, **Deschide folderul jurnalelor** sau **Golește fișierul jurnal** pentru a inspecta sau șterge datele jurnalului direct, fără repornirea NVDA și fără interferențe cu jurnalele standard NVDA.
- **Folder unic pentru date:** Toate fișierele de date ale add-on-ului (istoric, seriale, etichete, progres OCR, cache-uri și jurnale) sunt stocate într-un singur folder `VisionAssistant` din folderul de configurare NVDA — totul rămâne organizat, iar copiile de rezervă manuale sunt ușor de făcut.

### 1.10 Copie de rezervă și restaurarea setărilor

Fila **Avansat** include și o secțiune **Copie de rezervă și restaurare**:

- **Creează o copie de rezervă...:** Salvează configurația într-un singur fișier JSON. Când apeși butonul, alegi ce să incluzi: **Totul** (setări, etichete personalizate, progres OCR și istoric) sau **Doar setările**.
- **Restaurează...:** Încarcă o copie de rezervă salvată anterior pentru a restaura configurația și datele oricând, pe orice computer sau după reinstalarea NVDA. Mai întâi ți se va cere confirmarea, deoarece restaurarea înlocuiește toate setările și datele actuale.

## 2. Manager de chei API Gemini

Crearea unei chei API Gemini pe **aistudio.google.com** era cel mai dificil pas în utilizarea add-on-ului. Cu un cititor de ecran, paginile erau greu de înțeles, iar unii utilizatori pur și simplu nu reușeau deloc să creeze o cheie. **Managerul de chei API Gemini** rezolvă această problemă. Apasă **G** în stratul de comenzi sau deschide **Meniul NVDA > Preferințe > Setări > Vision Assistant > Conexiune** și apasă **Obține o cheie API Gemini...**.

- **Autentificare:** În manager, apasă **Autentifică-te și deschide browserul...** pentru a deschide în browserul implicit pagina securizată de autentificare Google. Autentifică-te cu contul tău Google — nu sunt necesare instrumente externe, SDK-uri sau configurări din linia de comandă. Contul cu care ești autentificat este afișat întotdeauna pe butonul **Deconectează-te**.
- **Crearea unei chei:** După autentificare, poți crea imediat o cheie cu **Proiect și cheie noi**, fără configurare prealabilă. Dacă ai deja proiecte, acestea apar într-o listă simplă din care poți selecta unul și apăsa **Creează o cheie pentru proiectul selectat**.
- **Ce urmează:** Noua cheie este copiată imediat în clipboard, salvată în add-on pentru mai târziu și ești întrebat o singură dată dacă vrei să o adaugi în lista de chei a add-on-ului. Asta este tot — nu mai trebuie să cauți prin pagini web.
- **Gestionarea cheilor:** **Copiază cheia selectată** copiază cheia selectată, **Copiază ultima cheie creată** copiază cheia pe care tocmai ai creat-o, iar **Exportă cheile salvate...** salvează cheile într-un fișier CSV cu toate detaliile sau într-un fișier text cu câte o cheie pe linie.
- **Ștergerea unei chei:** Selectează cheia pe care vrei să o elimini, apasă **Șterge cheia** și confirmă ștergerea. Ștergerea unei chei o elimină și din lista de chei a add-on-ului, astfel încât în rotație să nu rămână chei nefuncționale. Poți șterge și chei create în afara add-on-ului, dacă ai permisiunile necesare asupra proiectului respectiv.
- **Deconectare:** **Deconectează-te** elimină informațiile de autentificare stocate pe computer, astfel încât să poți trece oricând la alt cont.

## 3. Strat de comenzi și scurtături

Pentru a preveni conflictele de taste, acest add-on folosește un **strat de comenzi**.

1. Apasă **NVDA + Shift + V** (tasta principală) pentru a activa stratul (vei auzi un bip).
2. Eliberează tastele, apoi apasă una dintre următoarele taste individuale:

| Tastă            | Funcție                                | Descriere                                                                                                                                                                                                                                                                        |
| ---------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shift + A**    | **AI Operator**                        | **Operare autonomă:** Spune-i AI-ului să efectueze o sarcină pe ecran. Apăsarea din nou oprește instant operațiile active.                                                                                                       |
| **E**            | **UI Explorer**                        | **Clic interactiv:** Identifică și apasă elemente UI în orice aplicație.                                                                                                                                                                         |
| **T**            | Traducător inteligent                  | Traduce textul de sub cursorul navigator sau selecția.                                                                                                                                                                                                           |
| **Shift + T**    | Traducător clipboard                   | Traduce conținutul aflat în prezent în clipboard.                                                                                                                                                                                                                |
| **R**            | Rafinator de text                      | Rezumă, corectează gramatica, explică sau rulează **prompturi personalizate**.                                                                                                                                                                                   |
| **V**            | Viziune obiect                         | Descrie obiectul navigator curent.                                                                                                                                                                                                                               |
| **O**            | Viziune ecran complet                  | Analizează întregul layout și conținut al ecranului.                                                                                                                                                                                                             |
| **Shift + V**    | Analiză video                          | Analizează fișiere video locale sau videoclipuri online de pe **YouTube**, **Instagram**, **TikTok** sau **Twitter (X)**.                                                                                                                     |
| **Control + V**  | Înregistrare video locală              | Înregistrează un videoclip silențios al ecranului și analizează acțiunile și layoutul.                                                                                                                                                                           |
| **D**            | Cititor de documente                   | Cititor avansat pentru PDF, imagini și fișiere text simplu/HTML, cu selecție interval de pagini.                                                                                                                                                                 |
| **F**            | **Acțiune inteligentă pentru fișiere** | Recunoaștere contextuală din fișiere imagine, PDF sau TIFF selectate.                                                                                                                                                                                            |
| **M**            | Transcriere și dublare media           | Transcrie sau dublează fișiere audio/video (MP3, WAV, MP4 etc.) în limba ta țintă.                                                                                                                                            |
| **C**            | Rezolvitor CAPTCHA                     | Capturează și rezolvă CAPTCHA-uri.                                                                                                                                                                                                                               |
| **Shift + C**    | Chat direct                            | Deschide o interfață de chat direct, bazată pe text, cu AI-ul.                                                                                                                                                                                                   |
| **S**            | Dictare inteligentă                    | Convertește vorbirea în text. Apasă pentru a începe înregistrarea, apoi din nou pentru oprire/tastare.                                                                                                                                           |
| **Control+T**    | Traducere vocală                       | Transcrie, traduce și tastează rezultatul pe baza setărilor tale de limbă.                                                                                                                                                                                       |
| **Control+L**    | **Asistent live**                      | **Copilot în timp real (doar Gemini):** Pornește sau oprește o conversație vocală și de ecran în direct cu asistentul AI.                                                                                                     |
| **Control+A**    | **Operator live**                      | **Control autonom al computerului (doar Gemini):** Pornește sau oprește o sesiune vocală în direct în care operatorul îți îndeplinește cererile pe computer.                                                                  |
| **G**            | **Manager de chei API Gemini**         | **Creează cheia API fără a naviga pe web (doar Gemini):** Deschide managerul care pregătește cele necesare pe computer, deschide browserul pentru autentificare și creează, copiază sau șterge o cheie pentru proiectul ales. |
| **I**            | Raportare stare                        | Anunță progresul curent (de exemplu, „Se scanează...”, „Inactiv”).                                                                                                                            |
| **L**            | **Etichetează obiectul**               | **Etichetare AI semantică:** Etichetează permanent elementul/pictograma focalizată curentă.                                                                                                                                                      |
| **Shift + L**    | **Gestionează/scanează etichete**      | Deschide Managerul de etichete (dacă există etichete) sau scanează aplicația pentru elemente fără nume.                                                                                                                                       |
| **U**            | Verificare actualizări                 | Verifică manual pe GitHub cea mai recentă versiune a add-on-ului.                                                                                                                                                                                                |
| **Space**        | Reapelează ultimul rezultat            | Afișează ultimul răspuns AI într-un dialog de chat pentru revizuire sau întrebări suplimentare.                                                                                                                                                                  |
| **H**            | Ajutor comenzi                         | Afișează o listă cu toate scurtăturile disponibile.                                                                                                                                                                                                              |
| **Control + H**  | **Istoric**                            | Deschide dialogul Istoric cu conversațiile și documentele anterioare, filtre după tip și opțiuni de ștergere/golire.                                                                                                                                             |
| **Alt + S**      | Setări                                 | Deschide dialogul de setări Vision Assistant Pro.                                                                                                                                                                                                                |
| **Alt + Q**      | Raport chei cu cotă epuizată           | Raportează numărul de chei API Gemini care și-au depășit cota zilnică și ora lor de resetare.                                                                                                                                                                    |
| **Alt + M**      | Audit rutare                           | Raportează modelele AI selectate în prezent în rutarea avansată.                                                                                                                                                                                                 |
| **Up / Down**    | Navigare setări rapide                 | Navighează între categoriile de setări rapide (furnizor, model etc.) în strat.                                                                                                                                                |
| **Left / Right** | Schimbă setarea rapidă                 | Schimbă valoarea setării rapide selectate curent.                                                                                                                                                                                                                |

## 4. Chat și istoric

Ferestrele de chat și dialogul Istoric sunt disponibile pentru toate funcțiile, astfel încât să poți revedea conversațiile și să continui exact de unde ai rămas.

### 4.1 Scurtături în fereastra de chat

Când este deschisă o fereastră de chat (Chat direct, chat despre document, rafinare și altele similare), poți revedea conversația folosind:

- **Alt + Down:** Citește mesajul următor.
- **Alt + Up:** Citește mesajul anterior.
- **Alt + C:** Copiază mesajul curent.

### 4.2 Istoric (Control + H)

Apasă **Control + H** în stratul de comenzi pentru a deschide dialogul **Istoric** cu conversațiile și documentele anterioare, pe care le poți filtra după tip (Toate / Conversații / Documente). Deschide un chat pentru a continua conversația — inclusiv fișierele sale atașate, care sunt reatașate automat — sau deschide un document și continuă lectura. Apasă **Delete** pe orice element pentru a-l elimina sau **Șterge tot** pentru a goli lista. Pentru documente, Delete te întreabă dacă vrei să elimini doar intrarea din istoric sau și textul OCR al documentului din cache, astfel încât la următoarea deschidere să fie scanat din nou de la zero — cu opțiunea **Nu mai întreba** pentru a reține alegerea.

Poți alege și ce păstrează lista. **Salvează chaturile în istoric** (fila Conexiune) și **Salvează documentele în istoric** (fila Cititor de documente) sunt ambele activate implicit și pot fi activate/dezactivate din Setări rapide. Opțiunea pentru documente afectează numai intrarea din Istoric — textul OCR din cache și datele pentru reluare sunt păstrate întotdeauna.

## 5. AI Operator - Control autonom al computerului

**AI Operator** transformă Vision Assistant Pro dintr-un cititor pasiv într-un asistent activ care poate interacționa cu computerul în numele tău. Îi poți cere să descrie ecranul, să răspundă la întrebări despre ce vede sau chiar să preia controlul—apăsând butoane, trăgând elemente, tastând text și navigând prin aplicații folosind comenzi în limbaj natural.

Cel mai mare avantaj? Funcționează perfect în software complet inaccesibil. Dacă ești blocat într-o aplicație personalizată, un desktop remote sau un site web în care cititorul tău de ecran rămâne complet tăcut, operatorul nu este deranjat. Pentru că „vede” ecranul vizual, poate găsi, citi și interacționa cu elemente care nu au deloc etichete de accesibilitate.

### 5.1 Cum funcționează

1. Apasă **NVDA + Shift + V**, apoi apasă **Shift + A** (sau folosește scurtătura directă) pentru a deschide dialogul AI Operator.
2. Tastează ce vrei să faci în limbaj simplu (de exemplu, „Apasă butonul Salvează”, „Ce spune mesajul de eroare?” sau „Redenumește fișierul în final.pdf”).
3. AI-ul va analiza ecranul, va identifica elementele relevante și va executa acțiunea sau va oferi răspunsul. Dacă o sarcină necesită mai mulți pași, operatorul va continua să lucreze până când este completă.
4. Apasă din nou **Shift + A** oricând pentru a opri instant o operație în desfășurare.

### 5.2 Acțiuni acceptate

Operatorul înțelege o gamă largă de comenzi:

- **Descriere și răspuns**: „Descrie layoutul ecranului” sau „Ce spune mesajul de eroare?”
- **Clic**: „Apasă butonul Salvează”
- **Clic dreapta**: „Dă clic dreapta pe fișier”
- **Dublu clic**: „Dă dublu clic pe document”
- **Tragere și plasare**: „Trage documentul în folderul Arhivă”
- **Tastare**: „Tastează «Hello World» în caseta de căutare”
- **Derulare**: „Derulează în jos de trei ori”
- **Apăsare de tastă**: „Apasă Enter”, „Apasă Tab”, „Apasă Escape”
- **Sarcini cu mai mulți pași**: „Deschide File Explorer, găsește raportul și redenumește-l în final.pdf”

### 5.3 Note importante

- **⚠️ Avertisment privind utilizarea API**: Deoarece operatorul trebuie să „vadă” exact ce se întâmplă pe ecran, trimite o captură de ecran la rezoluție înaltă la fiecare pas. Utilizarea frecventă îți va consuma cota API mult mai repede decât funcțiile standard bazate pe text.
- **Aplicații cu drepturi de administrator**: Dacă NVDA nu rulează cu privilegii de administrator, operatorul poate să nu poată interacționa cu ferestre care necesită permisiuni ridicate. Aceasta este o limitare de securitate Windows, nu o eroare a add-on-ului.
- **Recomandări**: Pentru rezultate mai bune, dă comenzi clare și specifice. „Apasă butonul albastru Trimite din partea de jos a formularului” va funcționa aproape întotdeauna mai bine decât doar „Apasă butonul”.

### 5.4 Operator live (Control+A)

Operatorul live îi permite Asistentului live să îndeplinească ceea ce îi ceri pe computer în timp ce vorbești cu el, inclusiv în aplicații pe care cititorul de ecran nu le poate citi.
_(Notă: Această funcție este exclusivă pentru Google Gemini și furnizorii personalizați compatibili Gemini)._

- **Activare:** Apasă **Control+A** în stratul de comenzi pentru a începe o sesiune cu operatorul live; apasă din nou pentru a o încheia.
- **Cum funcționează:** Cere ce dorești în limbaj simplu, de exemplu „deschide Chrome și caută un site web” sau „redenumește acest fișier în final”. Operatorul privește ecranul, execută pașii unul câte unul și continuă să lucreze la cererile cu mai mulți pași până când sarcina este finalizată.
- **Anunțuri:** Fiecare pas este rostit cu vocea Asistentului live, iar acesta îți spune când sarcina s-a încheiat sau de ce nu a putut fi realizată.
- **CAPTCHA:** Dacă apare un CAPTCHA, operatorul încearcă mai întâi **rezolvitorul CAPTCHA** integrat; dacă nu reușește, îți cere să rezolvi singur provocarea accesibilă.
- **Oprire:** Apasă **Oprește acțiunea operatorului** în fereastra Asistentului live pentru a anula sarcina curentă.
- **Setări:** Instrucțiunea proprie a operatorului poate fi editată în Managerul de prompturi (secțiunea **Live**, **Instrucțiuni pentru operatorul live**). Opțiunea **Ieșire directă live (fără fereastră)** este disponibilă și în Setări rapide.

## 6. Analiză video și descriere audio

> **Notă:** Funcțiile Analiză video și Descriere audio sunt alimentate strict de furnizorul **Google Gemini**. Asigură-te că furnizorul activ din setările add-on-ului este setat la Google Gemini.

Vision Assistant Pro introduce capabilități puternice de procesare video, concepute special pentru utilizatorii nevăzători. Poate analiza atât videoclipuri online, cât și înregistrări locale ale ecranului, pentru a oferi descrieri vizuale foarte detaliate și pentru a genera scripturi profesionale de descriere audio (SRT).

### 6.1 Înregistrare locală a ecranului (Control + V)

Dacă întâlnești un videoclip tăcut, o animație sau un tutorial pe ecran, îl poți captura direct:

1. Apasă **NVDA + Shift + V** pentru a intra în stratul de comenzi, apoi apasă **Control + V**.
2. Add-on-ul va înregistra silențios ecranul în fundal.
3. Apasă din nou **Control + V** pentru a opri înregistrarea.
4. AI-ul va analiza apoi segmentul video înregistrat și va oferi o descriere foarte detaliată a scenei, personajelor și acțiunilor.

### 6.2 Analiză video (Shift + V)

Poți analiza atât fișiere video locale, cât și videoclipuri online. Selectează pur și simplu un fișier video local în Windows Explorer sau copiază un link video online în clipboard. Poți apăsa și **Shift + V** oriunde (de exemplu, într-un player media) pentru a deschide un dialog unde poți căuta un fișier video sau lipi manual un URL.

- **Platforme online acceptate:** YouTube, Instagram, TikTok și Twitter (X).
- AI-ul va detecta automat fișierul local sau URL-ul, va procesa videoclipul și va oferi o descriere vizuală cuprinzătoare și un rezumat audio.
- **Păstrarea fișierelor video în cache timp de 48 de ore:** Videoclipurile încărcate în Gemini sunt păstrate în cache timp de 48 de ore! Poți genera din nou fișiere SRT sau MP3 pentru același videoclip fără a-l reîncărca — chiar și după repornirea NVDA. Cache-ul ține cont de cheia folosită și este invalidat automat când cheia API se schimbă.

### 6.3 Generare descriere audio (SRT)

Pentru o experiență mai structurată, add-on-ul poate genera scripturi profesionale de descriere audio în formatul standard SubRip (SRT).

- **Sincronizare inteligentă pe pauze:** AI-ul ascultă pista audio și ancorează descrierile vizuale în mod specific în pauzele naturale și golurile de liniște, pentru a minimiza inteligent suprapunerea peste dialog.
- **Urmărirea personajelor:** Motorul efectuează o analiză preliminară pentru a extrage personaje distincte pe baza trăsăturilor faciale neschimbătoare. Creează un dicționar global pentru a urmări și eticheta precis personajele în diferite scene, fără confuzie. Urmărește și **prima apariție** a fiecărui personaj, descriindu-i aspectul fizic o singură dată — în momentul în care apare pentru prima oară — și folosind numai numele stabilite în scenele ulterioare, pentru a menține narațiunea variată și naturală.
- **OCR text mot-à-mot:** Orice text care apare pe ecran (semne, telefoane, generice) este citat strict mot-à-mot.
- **Cum se folosește:** Pentru a asculta subtitrarea generată, plasează pur și simplu fișierul `.srt` în același folder cu fișierul video și dă-i exact același nume. Apoi configurează playerul media (de exemplu, VLC sau PotPlayer) să trimită textul subtitrării direct către cititorul tău de ecran sau motorul TTS în timpul redării.
- **Salvare îmbunătățită:** Când salvezi fișiere SRT sau MP3, dialogul de fișiere se deschide acum implicit în folderul videoclipului sursă, indiferent dacă ai deschis videoclipul din dialogul de fișiere sau cu Shift+V din Explorer.

### 6.4 Narațiune audio sincronizată (export MP3)

Dincolo de crearea fișierelor SRT bazate pe text, add-on-ul funcționează ca un instrument complet de producție pentru descriere audio, sintetizând descrierile în vorbire și mixându-le cu videoclipul. Acum poți alege **Gemini Live TTS** ca motor vocal, care folosește API-ul Gemini Live pentru a genera narațiune vocală foarte realistă și nelimitată. Când generezi un MP3 pentru fișiere video locale, ai mai multe moduri de mixare:

- **AD standard (mixare voce):** Narațiunea este suprapusă direct peste sunetul videoclipului. Vei fi întrebat dacă vrei să aplici **Audio Ducking** (reducerea volumului de fundal în timpul descrierilor) pentru a te asigura că narațiunea este clară.
- **AD extins (pauză audio):** Motorul pune pe pauză sunetul original al videoclipului în timpul descrierilor, asigurându-se că nu pierzi niciun cuvânt din dialogul original sau din narațiunea AI. Detectarea pauzelor folosește acum modelul neuronal **Silero VAD** (descărcat automat la prima utilizare, la fel ca ffmpeg și eSpeak) pentru sincronizarea precisă cu pauzele — distingând pauzele naturale din dialog de muzică și zgomotul de fundal.
- **Videoclipuri YouTube:** Pentru sursele YouTube (care nu sunt descărcate local), exportul MP3 va conține strict pista vocală AI sincronizată, fără sunetul de fundal al videoclipului.

## 7. Transcriere și dublare media (M)

Transcriptorul audio a fost reconstruit complet pentru a accepta atât fișiere audio, cât și fișiere video (MP3, WAV, MP4, MKV etc.). Apasă **M** în stratul de comenzi pentru a selecta un fișier media și alege unul dintre cele 3 moduri de operare distincte:

1. **Transcrie (limba originală)**: Transcrie cu acuratețe vorbirea în limba sa originală.
2. **Transcrie și tradu (limba țintă)**: Transcrie vorbirea și o traduce în limba țintă configurată.
3. **Dublează și tradu (limba țintă)** _(doar Gemini)_: O funcție nouă puternică ce transcrie vorbirea, o traduce în limba ta țintă și sintetizează o dublare audio vorbită folosind motorul TTS al add-on-ului.

## 8) Cititor avansat de documente și imagini

**Cititorul de documente** transformă documentele în text curat, ușor de citit — astfel încât să poți citi, traduce și asculta orice, de la o carte scanată la un teanc de fotografii. Acceptă PDF-uri cu mai multe pagini, imagini complexe, formate iPhone HEIC și chiar fișiere text simplu (`.txt`) și HTML (`.html`, `.htm`), care se deschid instantaneu, fără OCR sau procesare AI. Selectează mai multe fișiere simultan, iar acestea vor fi reunite într-un singur document continuu, în ordinea paginilor. Sunt disponibile trei motoare OCR — **Chrome (rapid)**, **AI (avansat)** pentru păstrarea superioară a layoutului și **Niciunul (extrage stratul de text)** pentru PDF-uri în care se poate căuta text — pe care le alegi din Setări → Cititor de documente.

### Cum funcționează

1. Apasă **NVDA + Shift + V**, apoi **D** pentru a deschide Cititorul de documente — sau evidențiază mai întâi un fișier în File Explorer și apasă **D** / **F** pentru a omite complet dialogul de fișiere.
2. Alege unul sau mai multe PDF-uri ori imagini. Add-on-ul le scanează și anunță numărul total de pagini.
3. În dialogul **Opțiuni**, alege intervalul de pagini (De la/Până la). Poți și să bifezi **Tradu ieșirea** și să alegi limba țintă, să activezi/dezactivezi **Descrie imaginile în linie în timpul OCR** sau **Comprimă paginile PDF înainte de procesare**, pentru a micșora și recomprima paginile scanate supradimensionate înainte de încărcare.
4. Extragerea textului începe în fundal, în loturi. Poți închide fereastra oricând și continua mai târziu — nu se pierde nimic.
5. După ce paginile sunt gata, citește-le în vizualizator: treci de la o pagină la alta, sari la orice pagină, pune întrebări AI-ului, salvează textul sau generează o narațiune audio.

### 8.1 Procesare în lot și reluare

Nu trebuie să citești un document masiv dintr-o singură dată. Alege un interval de pagini (de exemplu, `1-20`) sau păstrează valorile implicite pentru a procesa totul, iar AI-ul extrage toate paginile în fundal. Dacă NVDA se blochează sau întrerupi scanarea, add-on-ul îți reține progresul și îți oferă opțiunea de **reluare** exact de unde a rămas — chiar și după repornire. Documentele finalizate sunt păstrate și în cache, astfel încât redeschiderea lor (din Documente recente sau prin **D**) încarcă textul instantaneu, fără a repeta OCR-ul, dacă fișierele sursă nu s-au schimbat.

### 8.2 Acțiune inteligentă pentru fișiere

Nu trebuie întotdeauna să deschizi mai întâi documentul. În Windows File Explorer, evidențiază pur și simplu un PDF, o imagine sau un fișier text/HTML și apasă **D** (Cititor de documente) — sau evidențiază un PDF ori o imagine și apasă **F** (Acțiune inteligentă pentru fișiere) — în stratul de comenzi. Add-on-ul ocolește instant dialogul de fișiere și începe procesarea fișierului evidențiat. Dacă selectezi mai multe fișiere simultan, acestea sunt procesate împreună ca un singur document.

### 8.3 Controale și scurtături în vizualizatorul de documente

Când fereastra Cititorului de documente este deschisă, poți folosi următoarele:

#### Scurtături de la tastatură

- **Ctrl + PageDown / Ctrl + PageUp:** Mută-te la pagina următoare / anterioară.
- **Săgeată în jos / în sus:** Când cursorul ajunge pe ultima linie a unei pagini, apasă **Jos** pentru a trece la pagina următoare; apasă **Sus** la începutul unei pagini pentru a reveni la cea anterioară.
- **Alt + A:** Deschide un dialog de chat pentru a pune întrebări despre document.
- **Alt + R:** Forțează o **rescanare cu AI** folosind furnizorul activ.
- **Alt + G:** Generează și salvează un fișier audio de calitate înaltă (WAV/MP3). _(Ascuns dacă furnizorul nu acceptă TTS)._
- **Alt + S / Ctrl + S:** Salvează textul extras ca fișier TXT sau HTML.

#### Butoane și controale

- **Mergi la:** Alege orice pagină din selectorul de pagini.
- **Vizualizează formatat:** Vezi întregul document reunit ca text formatat.
- **Încearcă din nou:** Reîncearcă numai loturile care au eșuat din cauza unei erori temporare a serverului (de exemplu, suprasolicitare). Acest buton apare automat când este necesar.
- **Voce TTS / Motor TTS:** Alege vocea și, pentru Gemini, alege între **TTS standard** și transmiterea în flux prin **Gemini Live**.
- **Anterior / Următor:** Treci de la o pagină la alta (la fel ca scurtăturile Ctrl+PageUp/Down).

### 8.4 Documente recente (D)

Apăsarea tastei **D** în stratul de comenzi afișează mai întâi documentele citite recent. Alege unul pentru a continua de la pagina la care ai rămas — chiar dacă OCR-ul s-a încheiat deja — sau apasă **Deschide fișier...** (`Ctrl + O`) pentru a căuta un fișier ca de obicei.

## 9. Etichetare AI semantică și UI Explorer

Te-ai blocat într-o aplicație în care peste tot apare „buton fără etichetă”? Motorul de etichetare AI semantică rezolvă permanent acest lucru.

### 9.1 Etichetare permanentă a obiectelor (L)

Mută focusul cititorului de ecran pe un grafic sau buton fără etichetă și apasă **L** în stratul de comenzi. AI-ul va privi vizual butonul, îi va determina funcția și va aplica o etichetă permanentă.
_Spre deosebire de instrumentele mai vechi de etichetare pentru cititoare de ecran, acest add-on folosește un sistem hibrid avansat de „semnătură a obiectului” (AutomationId/ControlID). Etichetele tale personalizate vor supraviețui redimensionării ferestrelor, schimbării monitorului și actualizărilor aplicației!_

### 9.2 Scanarea completă a aplicației (Shift + L)

Apasă **Shift + L** pentru a scana întreaga fereastră activă dintr-o dată. AI-ul va găsi toate elementele fără etichetă și le va denumi inteligent într-o singură operație. Ulterior, poți gestiona, redenumi sau șterge în lot aceste etichete din Managerul de etichete integrat.

### 9.3 UI Explorer (E)

Ai nevoie să interacționezi cu un element fără să navighezi manual până la el? Apasă **E** pentru a activa UI Explorer. AI-ul va scana ecranul și va genera o listă accesibilă cu fiecare element pe care se poate face clic (ignorând zgomotul de sistem precum bara de activități). Alege un element din listă, iar add-on-ul îl va apăsa instant pentru tine.

## 10. Asistent vocal live

Asistentul live transformă Vision Assistant Pro într-un copilot interactiv în timp real.
_(Notă: Această funcție este exclusivă pentru Google Gemini și furnizorii personalizați compatibili Gemini)._

- **Activare:** Apasă **Control + L** în stratul de comenzi pentru a deschide dialogul Asistentului live.
- **Interacțiune în timp real:** Vorbește natural prin microfon. AI-ul îți va asculta simultan vocea și va privi ecranul activ. Poți pune întrebări precum „La ce mă uit?” sau „Citește-mi al treilea paragraf.”
- **Apasă pentru a vorbi:** Activează **Apasă pentru a vorbi** în fila de setări Asistent live (sau direct în fereastra Asistentului live), apoi ține apăsată tasta atribuită pentru a vorbi și elibereaz-o când ai terminat. Microfonul rămâne dezactivat până când apeși tasta — ideal pentru medii zgomotoase.
- **Intrare de la camera web:** Bifează **Folosește camera &web** în fereastra Asistentului live pentru a trimite AI-ului imaginea camerei în locul ecranului — pune întrebări despre obiecte fizice, documente tipărite sau împrejurimi. Dacă ffmpeg nu este încă instalat, bifarea opțiunii îl descarcă o singură dată, cu permisiunea ta; opțiunea este dezactivată dacă nu este detectată nicio cameră sau dacă setările de confidențialitate Windows blochează accesul la cameră.
- **Personalizare:** În interiorul dialogului, poți schimba stilul vocal al AI-ului (de exemplu, Profesional, Prietenos, Energic) și îi poți ajusta „profunzimea gândirii” pentru a controla cât de profund raționează înainte de a răspunde.

## 11. Observator ambiental (asistent în fundal)

Observatorul ambiental transformă Vision Assistant Pro într-un asistent care vede pentru tine în fundal, fără conversație: continuă să asculte și să privească în timp ce lucrezi, anunță ce se schimbă și rămâne tăcut când nu se întâmplă nimic.
_(Notă: Această funcție este exclusivă pentru Google Gemini și furnizorii personalizați compatibili Gemini)._

- **Activare:** Apasă **Shift+O** în stratul de comenzi pentru a deschide dialogul Observatorului ambiental; apasă din nou pentru a opri observatorul.
- **Moduri:** **Doar traducere audio** traduce ceea ce aude, **Doar monitorizarea ecranului** anunță schimbările de pe ecran, iar **Doar monitorizarea camerei web** deschide fereastra Asistentului live cu camera ta și modul Apasă pentru a vorbi, astfel încât să poți pune întrebări despre ceea ce vede camera.
- **Sursă audio:** În modul audio, alege dacă vrei să traduci sunetul de la **Microfon** sau **Sunetul sistemului (Loopback)**. Mica bibliotecă pentru captarea sunetului sistemului este descărcată o singură dată, la prima utilizare, cu permisiunea ta.
- **Context:** Pentru modurile ecran și cameră web, alege opțional un element din **Despre ceea ce fac** (de exemplu, urmărești un film, o ședință sau un apel, citești o etichetă ori îți verifici aspectul) pentru a orienta anunțurile; poți introduce și propriul context.
- **Raportare:** Add-on-ul compară fiecare cadru nou cu cel anterior și îl trimite AI-ului numai când imaginea s-a schimbat cu adevărat, astfel încât un ecran static nu consumă cereri. AI-ul raportează apoi numai noutățile și nu se repetă.
- **Mesaj de întâmpinare:** Cu excepția modului de traducere, observatorul te salută pe scurt când pornește, ca să știi că ascultă.
- **Setări:** În **Setări > Asistent live**, configurează **Mod de observare**, **Interval între cadre** (de la 1 la 10 secunde) și **Stil de raportare** (concis sau detaliat). Instrucțiunea observatorului și fiecare text de context pot fi editate în Managerul de prompturi (secțiunea **Ambiental**).

## 12. Prompturi personalizate și variabile

Poți gestiona prompturile în **Setări > Prompturi > Gestionează prompturi...**.

- **Filtru:** Fila **Prompturi implicite** are o listă **Filtru** deasupra listei de prompturi, care afișează **Toate** prompturile sau doar câte o secțiune (de exemplu, **Ambiental**), astfel încât listele lungi să rămână ușor de parcurs.

### Scurtături pentru prompturi personalizate

Atribuie oricărui prompt personalizat propria scurtătură direct în Managerul de prompturi și execută-l instantaneu cu selecția sau contextul curent:

- **Tastă individuală** (de exemplu, `1`, `p` sau `F3`): Funcționează în stratul de comenzi și global sub forma `NVDA + Shift + key`.
- **Combinație de taste** (de exemplu, `Control + Shift + 1`, `Alt + P` sau `Insert + 1`): Funcționează direct la nivel global.

### Comportamentul de ieșire pentru fiecare prompt

Fiecare prompt personalizat poate avea propriul mod de prezentare a rezultatului:

- **Setare globală:** Urmează setarea generală de ieșire din fila Conexiune (Ieșire directă sau Fereastră de chat).
- **Copiază în clipboard:** Copiază răspunsul AI direct în clipboard, fără a deschide o fereastră.
- **Ieșire directă (mesaj NVDA):** Prezintă răspunsul AI direct prin voce și braille folosind NVDA.
- **Copiază în clipboard și ieșire directă:** Copiază răspunsul în clipboard și îl rostește direct.
- **Fereastră de chat:** Deschide întotdeauna rezultatul într-o fereastră de conversație interactivă.

### Variabile acceptate

- `[selection]`: Textul selectat curent.
- `[text]`: Întregul conținut textual al câmpului de editare focalizat în prezent (ignoră automat câmpurile de parolă protejate).
- `[currentURL]`: URL-ul paginii web sau al documentului din browserele web acceptate (Chrome, Edge, Firefox).
- `[clipboard]`: Conținutul clipboardului.
- `[clipboard_image]`: Imaginea aflată în prezent în clipboard.
- `[screen_obj]`: Captură de ecran a obiectului navigator.
- `[screen_fg_obj]`: Captură de ecran a ferestrei active din prim-plan.
- `[screen_full]`: Captură de ecran completă.
- `[file_ocr]`: Selectează fișier imagine/PDF pentru extragerea textului.
- `[file_read]`: Selectează document pentru citire (TXT, cod, PDF).
- `[file_audio]`: Selectează fișier audio pentru analiză (MP3, WAV, OGG).
- `[ambient_screen]`: Pornește o sesiune continuă de observare a ecranului în fundal.
- `[ambient_webcam]`: Pornește o sesiune continuă de observare a camerei web în fundal (verifică opțiunea Apasă pentru a vorbi din setări).
- `[ambient_audio]`: Pornește o sesiune de traducere audio în direct a observatorului.
- `[loopback]`: Folosește sunetul redat de sistem ca sursă audio (pentru `[ambient_audio]`).
- `[mic]`: Folosește microfonul ca sursă audio (pentru `[ambient_audio]` și `[ambient_webcam]`).
- `[brief]`: Setează stilul de raportare al observatorului la concis (o singură propoziție).
- `[detailed]`: Setează stilul de raportare al observatorului la detaliat (2-3 propoziții).
- `[lang:code]`: Specifică codul limbii țintă pentru traducerea audio (de exemplu, `[lang:fa]`, `[lang:en]`).
- `{target_lang}`: Limba țintă curentă.
- `{source_lang}`: Limba sursă curentă.
- `{response_lang}`: Limba curentă a răspunsului AI.
- `{swap_target}`: Limba de rezervă pentru traducerea cu schimbare inteligentă.
- `{swap_instruction}`: Blocul de instrucțiuni pentru traducerea cu schimbare inteligentă.

_Notă despre prompturile ambientale:_ Prompturile care conțin variabile ambientale funcționează ca un comutator — apăsarea scurtăturii în timp ce sesiunea este activă o oprește imediat. Combinațiile incompatibile (precum folosirea variabilelor pentru capturi de ecran statice, cum ar fi `[screen_full]`, împreună cu modurile observatorului ambiental, combinarea mai multor moduri ambientale sau adăugarea de instrucțiuni de prompt la `[ambient_audio]`) sunt verificate strict și blocate la salvare.

## 13. Cazuri reale de utilizare (Ce funcție ar trebui să folosesc?)

Vision Assistant Pro este plin de instrumente avansate. Iată câteva scenarii comune care te ajută să alegi funcția potrivită:

- **Scenariu: Vrei să înțelegi layoutul complet al unei ferestre complicate sau al unei aplicații inaccesibile.**
  _Soluție:_ Apasă **O** (Viziune ecran complet). AI-ul va analiza întregul ecran și va descrie exact unde sunt poziționate elementele, textele și butoanele.

- **Scenariu: Ai găsit o imagine pe o pagină web sau un grafic fără etichetă într-un document.**
  _Soluție:_ Mută obiectul navigator pe grafic și apasă **V** (Viziune obiect). AI-ul va descrie precis ce conține acea imagine.

- **Scenariu: Vrei să urmărești un film sau un videoclip cu descrieri audio.**
  _Soluție:_ Apasă **Shift + V** pe videoclip și alege **„Generează descriere audio (fișier SRT)”**. Când se termină, apasă **„Generează narațiune sincronizată (MP3)”** și selectează **„AD extins”**. Add-on-ul va crea o pistă audio care pune inteligent pe pauză dialogul filmului pentru a descrie scenele vizuale.

- **Scenariu: Ai întâlnit o aplicație plină de „butoane fără etichetă”.**
  _Soluție:_ Apasă **L** pentru a eticheta permanent butonul respectiv folosind AI. Sau apasă **Shift + L** pentru a scana și eticheta întreaga fereastră dintr-o dată. Dacă vrei doar să apeși ceva rapid, apasă **E** (UI Explorer) pentru a primi o listă cu toate elementele pe care se poate face clic.

- **Scenariu: Trebuie să treci de un CAPTCHA inaccesibil.**
  _Soluție:_ Apasă **C** (Rezolvitor CAPTCHA). AI-ul va captura automat CAPTCHA-ul, îl va rezolva și va introduce răspunsul în câmpul corect.

- **Scenariu: Vrei să citești un document PDF lung, de 50 de pagini.**
  _Soluție:_ Apasă **D** (Cititor de documente), setează furnizorul la Google Gemini și introdu intervalul de pagini `1-50`. Add-on-ul va extrage textul cu acuratețe în fundal.

- **Scenariu: Urmărești un tutorial video tăcut sau o animație pe ecran.**
  _Soluție:_ Apasă **Control + V** pentru a începe înregistrarea ecranului. Lasă tutorialul să ruleze, apoi apasă din nou **Control + V**. AI-ul va explica exact ce a fost demonstrat.

- **Scenariu: Întâlnești o eroare neașteptată, o problemă de conexiune API sau vrei să diagnostichezi probleme cu servere locale personalizate.**
  _Soluție:_ Mergi la **Setări > Avansat**, bifează **„Activează fișierul jurnal dedicat”** și setează **Nivel jurnal** la **„Debug”**. Execută acțiunea din nou, apoi apasă **„Deschide fișierul jurnal”** pentru a inspecta detaliile tehnice sau atașează fișierul `vision_assistant.log` la un tichet de suport.

***

**Notă:** Pentru toate funcțiile AI este necesară o conexiune activă la internet. Documentele cu mai multe pagini sunt procesate automat.

## 14. Suport și comunitate

Rămâi la curent cu cele mai recente noutăți, funcții și lansări:

- **Canal Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Issue-uri GitHub:** Pentru raportări de erori și cereri de funcții.

### Raportarea erorilor și jurnale

Când deschizi un issue pe GitHub sau ceri suport, te rog include detalii despre furnizorul AI activ, model și versiunea NVDA. Dacă ai probleme de conexiune sau blocări neașteptate, activează fișierul jurnal dedicat din **Setări > Avansat**, recreează problema și atașează fișierul `vision_assistant.log` pentru a ne ajuta să rezolvăm problema mai repede.

## 15. Susținătorii proiectului

Mulțumiri sincere membrilor comunității care susțin dezvoltarea și mentenanța continuă a acestui proiect prin contribuțiile lor financiare generoase:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**
- **leonardo0216**
- **Sergei Fleytin**
- **Arne Siebert**
- **Schalkefan**
- **Rainer Brell**
- **[avalai.org](https://avalai.org)**

_Dacă dorești să susții financiar proiectul și să îți vezi numele aici, poți găsi opțiunea **Donate** în meniul Instrumente NVDA (submeniul Vision Assistant) sau în timpul procesului de configurare de după instalare._

---

## Modificări pentru 2026.10.15

- **Cea mai cerută îmbunătățire — crearea unei chei API Gemini este în sfârșit ușoară**: Obținerea unei chei API pe **aistudio.google.com** era cel mai dificil pas. Cu un cititor de ecran, paginile erau greu de înțeles, iar unii utilizatori pur și simplu nu reușeau deloc să creeze o cheie. Această problemă este acum rezolvată direct în add-on. Apasă **G** în stratul de comenzi (sau folosește **Obține o cheie API Gemini...** din Setări), autentifică-te prin browserul implicit, fără nicio configurare externă, iar cheia este creată și configurată cu o singură confirmare — chiar dacă nu ai mai avut niciodată un proiect.
- **Observator ambiental**: Asistentul în fundal este aici. Apasă **Shift+O** în stratul de comenzi pentru a-l porni și apasă din nou pentru a-l opri. Poate traduce ceea ce aude (microfonul tău sau sunetul sistemului), poate urmări ecranul și îți poate spune ce s-a schimbat sau poate deschide Asistentul live cu camera web și modul Apasă pentru a vorbi, astfel încât să poți pune întrebări despre orice vede camera. Trimite o imagine numai când ceva s-a schimbat cu adevărat, astfel încât un ecran nemișcat nu consumă nimic, și rămâne tăcut când nu se întâmplă nimic. Poți și să pornești sau să oprești observatorul direct prin prompturi personalizate și scurtături dedicate, folosind `[ambient_screen]`, `[ambient_webcam]` sau `[ambient_audio]` împreună cu modificatori (`[loopback]`, `[mic]`, `[brief]`, `[detailed]`, `[lang:code]`), cu verificarea automată a combinațiilor de variabile incompatibile.
- **Operator live**: Asistentul live poate acum să îndeplinească ceea ce îi ceri pe computer în timp ce vorbești cu el. Apasă **Control+A** în stratul de comenzi pentru a începe o sesiune cu operatorul live, apoi cere ce dorești în limbaj simplu. Rezolvă cereri cu mai mulți pași, anunță fiecare pas cu vocea Asistentului live, gestionează combinațiile de taste necesare și decide singur când sarcina este încheiată. **Ieșire directă live (fără fereastră)** este disponibilă și în Setări rapide.
- **Dicționar de personaje și gestionarea serialelor**: Dialogul Analiză video include acum un sistem puternic de **Dicționar de personaje**! Adaugă, editează, importă sau gestionează numele, descrierile fizice și rolurile personajelor pentru fiecare serial — AI-ul asociază automat personajele descoperite cu cele din dicționar și adaugă personajele noi pe măsură ce analizezi mai multe episoade. Notele tale introduse manual sunt întotdeauna păstrate și au prioritate față de actualizările AI, iar descrierile fizice sunt actualizate de la un episod la altul. Dicționarul este salvat pentru fiecare serial și reutilizat pentru toate videoclipurile din acel serial. În lista de personaje, apasă **F2** pentru a edita personajul selectat și **Delete** pentru a-l elimina.
- **Suport pentru SOCKS5, HTTP și proxy invers, cu testarea latenței**: Depășește ușor restricțiile de rețea cu suport complet pentru proxy în întregul add-on — inclusiv Asistentul live, Observatorul ambiental și generarea TTS! Alege dintre 4 moduri de funcționare din setările generale: **Detectare automată**, **Proxy SOCKS5**, **Proxy HTTP** sau **Proxy invers**. SOCKS5 acceptă autentificarea prin nume de utilizator/parolă conform RFC 1929 și tunelarea conexiunilor către domenii; proxy-ul HTTP acceptă autentificarea Basic. Un nou buton **Testează conexiunea proxy** rulează în fundal și anunță latența conexiunii în milisecunde.
- **Păstrarea fișierelor video în cache timp de 48 de ore**: Videoclipurile încărcate în Gemini sunt acum păstrate în cache timp de 48 de ore! Poți genera din nou fișiere SRT sau MP3 pentru același videoclip fără a-l reîncărca — chiar și după repornirea NVDA. Cache-ul ține cont de cheia folosită și este invalidat automat când cheia API se schimbă.
- **Detectarea pauzelor cu AI (Silero VAD)**: AD extins folosește acum modelul neuronal Silero VAD pentru detectarea precisă a tăcerii — distingând pauzele naturale din dialog de muzică și zgomotul de fundal. Modelul este descărcat automat la prima utilizare (cu permisiunea ta), la fel ca ffmpeg și eSpeak.
- **Imagine de la camera web pentru Asistentul live**: Fereastra Asistentului live are acum o casetă de bifat **Folosește camera &web**, care trimite AI-ului imaginea camerei web în locul ecranului — ideală pentru întrebări despre obiecte fizice, documente sau împrejurimi. Dacă ffmpeg nu este încă instalat, bifarea opțiunii îl descarcă (o singură dată, cu permisiunea ta). Opțiunea este dezactivată dacă nu este detectată nicio cameră sau dacă setările de confidențialitate Windows blochează accesul la cameră; există și un buton pentru deschiderea setărilor de confidențialitate ale camerei. Dacă este activată camera, dar nu transmite cadre, problema este înregistrată în jurnalul NVDA pentru diagnosticare, în loc să se treacă înapoi la ecran fără notificare.
- **Selectarea dispozitivului de ieșire audio**: Poți selecta acum un dispozitiv de ieșire audio dedicat pentru Asistentul live și Observatorul ambiental. Alege între ieșirea implicită NVDA, Windows Sound Mapper sau orice placă de sunet fizică conectată (precum căști USB sau difuzoare externe), din fila de setări live, direct din dialogul Asistentului live sau din mers prin Setări rapide (NVDA+Shift+V, apoi Sus/Jos/Stânga/Dreapta).
- **Manager de prompturi**: Fila Prompturi implicite are acum o listă **Filtru**, astfel încât să poți afișa toate prompturile sau doar o secțiune (de exemplu, **Ambiental**). Tot acolo poți edita textele de context ale observatorului și noul prompt **Instrucțiuni pentru operatorul live**.
- **Filtrarea inteligentă a modelelor în rutarea avansată**: Listele derulante din Rutare avansată a modelelor clasifică acum dinamic modelele Gemini după capabilități, fără aglomerare. Asistentul live afișează numai modele cu interacțiune bidirecțională în timp real și modele audio native, TTS afișează numai modele dedicate sintezei vocale, STT acordă prioritate modelelor Transcribe și multimodale, iar Analiză video, OCR și AI Operator exclud modelele specializate pentru alte sarcini (precum generarea de imagini, generarea video și modelele de reprezentare vectorială). Modelele viitoare sunt detectate automat după capabilități, fără a necesita actualizări de versiune.
- **Urmărirea primei apariții a personajelor**: AI-ul descrie acum aspectul fizic al fiecărui personaj o singură dată — la prima sa apariție în videoclip. Aparițiile ulterioare folosesc numai numele, eliminând descrierile repetitive între segmente și menținând narațiunea variată și naturală.
- **Folder unic pentru date**: Toate fișierele de date ale add-on-ului (istoric, seriale, etichete, progres OCR, cache-uri și jurnale) au fost mutate într-un singur folder `VisionAssistant` din folderul de configurare NVDA — totul rămâne organizat, iar copiile de rezervă manuale sunt ușor de făcut.
- **Salvarea îmbunătățită a rezultatelor video**: Când salvezi fișiere SRT sau MP3, dialogul de fișiere se deschide acum implicit în folderul videoclipului sursă, indiferent dacă deschizi videoclipul din dialogul de fișiere sau cu Shift+V din Explorer.
- **Ștergerea documentelor cu sau fără textul din cache**: Dialogul Istoric (`Control + H`) oferă acum două moduri de a șterge un document — apasă Delete și alege **Șterge doar din istoric** sau **Șterge intrarea din istoric și textul din cache**. A doua opțiune elimină textul OCR al documentului din cache, astfel încât la următoarea deschidere să fie scanat din nou de la zero — ideal după o scanare nereușită. Caseta de bifat **Nu mai întreba** reține alegerea pentru ștergerile viitoare. Datele pentru reluarea operațiunilor întrerupte nu sunt modificate niciodată.
- **Cache OCR separat pe motoare, cu reunirea paginilor în Cititorul de documente**: Textul OCR din cache este acum stocat separat pentru fiecare motor OCR, astfel încât schimbarea motorului OCR declanșează întotdeauna o scanare cu noul motor, în loc să afișeze rezultatul vechi. Redeschiderea unui document afișează din nou dialogul pentru intervalul de pagini (completat cu ultima alegere), reutilizând instantaneu paginile deja scanate și scanând numai paginile lipsă — cache-ul este completat pagină cu pagină, în loc să fie înlocuit, astfel încât fiecare interval citit este păstrat pentru mai târziu.
- **Comprimarea PDF-urilor în Cititorul de documente**: A fost adăugată setarea opțională **Comprimă paginile PDF înainte de procesare** în dialogul pentru intervalul de pagini al Cititorului de documente. Când încarci în Gemini sau Mistral documente PDF scanate mari sau la rezoluție înaltă, paginile sunt micșorate și recomprimate automat pentru a reduce semnificativ volumul datelor încărcate, a accelera procesarea și a preveni expirarea conexiunilor de rețea. Opțiunea este dezactivată implicit și ascunsă automat când folosești motorul Chrome sau furnizori care primesc imagini codificate în base64.
- **Personalizarea comportamentului de ieșire pentru fiecare prompt**: Personalizează separat modul în care fiecare prompt personalizat își prezintă rezultatul! În editorul de prompturi personalizate, alege între **Setare globală**, **Copiază în clipboard**, **Ieșire directă (mesaj NVDA)**, **Copiază în clipboard și ieșire directă** sau **Fereastră de chat**. Astfel, anumite prompturi pot rosti direct rezultatul fără a deschide o fereastră, în timp ce altele deschid un chat complet.
- **Variabile dinamice noi pentru prompturi (`[currentURL]` și `[text]`)**: Prompturile personalizate acceptă acum `[currentURL]` pentru a prelua URL-ul documentului activ din Google Chrome, Mozilla Firefox și Microsoft Edge și `[text]` pentru a insera dinamic întregul conținut textual al câmpului de editare focalizat în prezent (ignorând câmpurile de parolă protejate).
- **Refacerea sistemului de descărcare a videoclipurilor Twitter/X**: Descărcarea și analiza videoclipurilor Twitter/X funcționează din nou după problemele apărute la serviciul extern de extragere. Extragerea video folosește acum API-ul robust FixTweet pentru a prelua direct fluxuri MP4 la cea mai înaltă calitate din CDN-ul Twitter, cu trecere automată la TwitSave ca soluție de rezervă și suport pentru proxy.
- **Corectarea descărcării videoclipurilor Instagram**: Descărcarea și analiza clipurilor Instagram Reels și a URL-urilor video funcționează din nou după modificările formularului serviciului extern de descărcare.
- **Corectări și performanță**: Modul Apasă pentru a vorbi reacționează imediat ce apeși tasta, Asistentul live nu mai începe un răspuns la mijlocul unei propoziții, observatorul nu mai raportează imaginea precedentă, iar lista Profunzimea gândirii oferă numai opțiunile acceptate efectiv de modelul tău. AI Operator poate derula și la stânga și la dreapta. A fost corectată o eroare `AttributeError` la analiza videoclipurilor online, iar prompturile personalizate fără text selectat nu mai introduc accidental titlurile ferestrelor din fundal în cererile către AI.

## Modificări pentru 2026.09.01

- **Istoric (Control + H)**: Stratul de comenzi include acum un dialog **Istoric** (`Control + H`) care afișează conversațiile și documentele anterioare, cu filtre pentru Toate, Conversații și Documente. Redeschide orice chat cu întreaga conversație — fișierele atașate sunt reatașate automat — sau redeschide un document și continuă lectura. Apasă **Delete** pe orice element pentru a-l elimina sau șterge totul dintr-o dată.
- **Documente recente în cititor**: Apăsarea tastei **D** în stratul de comenzi afișează acum mai întâi documentele citite recent. Alege unul pentru a continua de la pagina la care ai rămas — chiar dacă OCR-ul s-a încheiat deja — sau apasă **Deschide fișier...** (`Ctrl + O`) pentru a căuta un fișier ca de obicei.
- **Apasă pentru a vorbi în Asistentul live**: Preia controlul deplin asupra conversațiilor în direct! Activează **Apasă pentru a vorbi** în noua filă de setări Asistent live și atribuie orice tastă — sau chiar un singur modificator, precum `Left Ctrl` — pentru a vorbi. Ține tasta apăsată ca să vorbești și elibereaz-o când ai terminat, cu un bip scurt la fiecare apăsare și eliberare. O opțiune echivalentă apare și direct în fereastra Asistentului live, astfel încât să poți comuta între modul Apasă pentru a vorbi și microfonul permanent deschis fără a părăsi conversația.
- **Gemini 2.5 Flash Native Audio**: Asistentul live acceptă acum modelul audio nativ Gemini 2.5 Flash (`gemini-2.5-flash-native-audio-preview-12-2025`) pentru conversații vocale naturale, cu latență redusă. Îl poți selecta din **Setări → Rutare avansată a modelelor → Model Asistent live (doar Gemini)** sau poți păstra „Auto” pentru a folosi în continuare modelul recomandat.
- **Copie de rezervă și restaurarea setărilor**: A fost adăugat un sistem puternic de copii de rezervă și restaurare în fila **Avansat**! Poți salva acum toate setările add-on-ului — inclusiv cheile API, modelele, prompturile personalizate și preferințele — într-un singur fișier JSON și le poți restaura integral oricând, pe orice computer sau după reinstalarea NVDA. La crearea copiei de rezervă, alegi ce să incluzi: **Totul** (setări, etichete personalizate, progres OCR și istoric) sau **Doar setările**.
- **Citirea directă a fișierelor text și HTML**: Cititorul de documente poate acum deschide direct fișiere text simplu (`.txt`) și HTML (`.html`, `.htm`)! Detectează automat codarea fișierului, elimină scripturile și elementele de formatare inutile și împarte inteligent conținutul în pagini ușor de citit — poate chiar reimporta propriile fișiere exportate, păstrând structura paginilor — astfel încât să le poți citi instantaneu, fără OCR sau procesare AI!
- **Gemini Live TTS pentru Cititorul de documente**: Butonul „Generează audio” acceptă acum Gemini Live — un motor de sinteză vocală în flux, de înaltă calitate, cu ritm natural! Când Gemini este furnizorul activ, poți alege între TTS standard și Gemini Live direct din cititor, iar alegerea este reținută pentru data viitoare!
- **Scurtături pentru prompturi personalizate**: Poți atribui acum o scurtătură oricărui prompt personalizat direct din Managerul de prompturi! Atribuie fiecărui prompt o tastă sau o combinație de taste dedicată pentru a-l executa instantaneu, preluând automat selecția sau contextul curent, fără pași suplimentari!
- **Navigarea între mesajele de chat**: Reascultă orice conversație cu ușurință! În orice fereastră de chat (Chat direct, chat despre document, rafinare și altele), apasă `Alt + Down` pentru a auzi mesajul următor și `Alt + Up` pentru a-l auzi pe cel anterior — cu prefixele clare „Tu” / „AI” și limitele „Primul mesaj” / „Ultimul mesaj” anunțate pe parcurs.
- **Copierea mesajelor de chat (Alt + C)**: Când revezi o conversație cu `Alt + Up/Down`, apasă `Alt + C` pentru a copia mesajul curent în clipboard — respectând setarea de curățare Markdown — cu o confirmare vocală.
- **Prompt de sistem pentru Chat direct**: Chat direct (`Shift+C`) are acum propriul prompt de sistem editabil — „Instrucțiuni pentru chatul direct” — care stabilește personalitatea asistentului și limba de răspuns pentru fiecare conversație. Îl poți personaliza din fila Prompturi implicite a Managerului de prompturi.
- **Navigarea între pagini cu cursorul în Cititorul de documente**: Citirea documentelor cu mai multe pagini a devenit mai cursivă! În Vizualizatorul de documente, când cursorul ajunge pe ultima linie a unei pagini și apeși `Down`, cititorul trece automat la pagina următoare. Apăsarea tastei `Up` la începutul unei pagini te aduce imediat înapoi la pagina anterioară — nu mai trebuie să schimbi manual paginile în timp ce citești!
- **Opțiuni noi în Setări rapide**: Copierea răspunsurilor AI în clipboard, Ieșire directă (fără fereastră de chat), Curăță Markdown în chat și Schimbare inteligentă pot fi acum activate și dezactivate instantaneu din Setări rapide ale stratului de comenzi!
- **Fila de setări Asistent live**: Asistentul live are acum propria filă de setări dedicată! Opțiunea „Asistent live: ieșire directă (fără fereastră)” a fost mutată aici din fila Conexiune, iar fila apare numai când furnizorul activ este Google Gemini (sau un furnizor personalizat compatibil Gemini).

## Modificări pentru 2026.08.06

- **Etichetare în UI Explorer**: Acum poți adăuga etichete direct elementelor găsite în UI Explorer! A fost adăugat un nou buton „Adaugă etichetă”, iar interfața rămâne deschisă și păstrează focusul în mod inteligent, ca să poți eticheta rapid mai multe obiecte fără întrerupere.
- **Îmbunătățire a stratului de setări rapide**: Stratul Vision Assistant (`Insert+Shift+V`) este acum persistent și foarte interactiv! Poți folosi săgețile `Sus/Jos` pentru a naviga între setările rapide (furnizor, model, limba răspunsului AI, model TTS) și săgețile `Stânga/Dreapta` pentru a le schimba instant valorile, cu feedback vocal inteligent și concis. Selecțiile tale se aplică imediat (inclusiv activarea automată a rutării avansate atunci când este necesar), iar stratul rămâne activ cât timp configurezi.
- **Chat direct (`Shift+C`)**: A fost adăugată o comandă nouă în strat! Apasă `Shift+C` pentru a deschide instant o fereastră „Chat direct”. Aceasta oferă imediat o interfață conversațională curată, bazată pe text, cu AI-ul, fără să fie nevoie de o imagine sau de un document ca punct de pornire.
- **Reapelare impecabilă a istoricului conversației**: A fost corectată o eroare majoră prin care apăsarea tastei `Space` pentru reapelarea ultimului rezultat pierdea istoricul conversației ulterioare. Acum, add-on-ul urmărește conversația la nivel global. Dacă discuți, închizi dialogul și apeși `Space` pentru a-l reapela, întregul istoric dus-întors este restaurat perfect! Funcționează pentru Chat direct, analiză vizuală, chat pe documente și traducere.
- **Descrieri de imagini inline în OCR**: A fost adăugată o funcție opțională pentru descrierea imaginilor în linie în timpul OCR pentru documente. Poți comuta această setare din setările OCR ale add-on-ului, din opțiunile Cititorului de documente înainte de extragere și rapid, din mers, prin stratul de setări rapide.
- **Traducere vocală (`Control+T`)**: A fost adăugată o funcție nouă puternică! Dictează vorbirea, apoi tradu și tastează instant rezultatul cu AI, pe baza limbilor sursă și țintă configurate.
- **Îmbunătățiri ale descărcătorului de actualizări**: Dialogul de descărcare a actualizării afișează acum corect progresul în procente, iar o eroare prin care apărea un mesaj fantomă „Se descarcă actualizarea” după anularea instalării a fost corectată.
- **Îmbunătățiri ale descărcătorului eSpeak-NG**: A fost adăugată urmărirea progresului în procente pentru descărcările eSpeak-NG.
- **Reziliență pentru OCR în lot**: A fost corectată o problemă în OCR-ul PDF în lot prin care procesul se oprea dacă cheia API activă își atingea cota la mijlocul operației; acum se comută automat la următoarea cheie disponibilă și procesul continuă.
- **Suport pentru CAPTCHA vizual**: A fost adăugat suport robust pentru rezolvarea CAPTCHA-urilor vizuale. Încearcă să rezolve automat provocări complexe bazate pe imagini, precum hCaptcha și reCAPTCHA, îmbunătățind semnificativ accesibilitatea formularelor web dificile.
- **Restructurarea transcriptorului audio**: Modulul Transcriptor audio a fost reconstruit complet și acceptă acum atât fișiere audio, cât și fișiere video. Include 3 moduri de operare distincte: „Transcrie (limba originală)”, „Transcrie și tradu (limba țintă)” și noua opțiune puternică „Dublează și tradu (limba țintă)” (exclusiv pentru Gemini), care generează o dublare audio tradusă a vorbirii originale.
- **Numere de pagină opționale în Cititorul de documente**: A fost adăugată o setare nouă pentru includerea numerelor de pagină și a separatoarelor în rezultatele documentelor cu mai multe pagini. Poți gestiona ușor această opțiune din setările principale sau o poți comuta din mers prin stratul de setări rapide. Funcția se aplică atât exporturilor în fișiere text/HTML, cât și ferestrei „Vizualizare formatată” în linie, permițându-ți să citești documente combinate fără întreruperi.
- **Gemini Live TTS nelimitat pentru descrieri video**: Acum poți selecta „Gemini Live TTS” ca motor vocal atunci când generezi narațiune audio sincronizată (MP3) pentru videoclipuri. Acesta folosește API-ul Gemini Live pentru a sintetiza descrieri audio de calitate înaltă, fără limite de caractere sau restricții de lungime.
- **Modularizarea bazei de cod**: Structura add-on-ului a fost refactorizată dintr-un singur fișier într-o arhitectură modulară cu mai multe fișiere, pentru mentenanță îmbunătățită.
- **Redesign al interfeței de setări**: Dialogul de setări a fost reproiectat complet pentru a folosi o interfață modernă pe file în locul unui layout grupat, oferind organizare mai bună și navigare mai ușoară, păstrând toate opțiunile existente.
- **Jurnalizare globală și fișier jurnal dedicat**: A fost adăugat un sistem opțional de jurnalizare globală în fișier, în noua filă „Avansat”. Capturează automat evenimente operaționale, trafic API și erori din toate modulele add-on-ului într-un fișier dedicat (`vision_assistant.log`). Acceptă niveluri configurabile de detaliu pentru jurnal (Debug, Info, Avertisment, Eroare), perioade automate de păstrare (de la 1 oră până la 90 de zile) și deschiderea sau golirea directă a jurnalului din setări, fără impact asupra performanței și fără interferențe cu jurnalul NVDA.
- **Urmărire progres încărcări Gemini**: Au fost adăugate anunțuri în timp real ale progresului procentual la încărcarea fișierelor mari (video, audio, documente) în API-ul Google Gemini.

## Modificări pentru 2026.07.15

- **Filtrare inteligentă a modelelor API**: Sistemul de filtrare a modelelor a fost refăcut complet pentru a folosi o abordare bazată strict pe listă neagră în loc de liste albe. Au fost adăugate cuvinte-cheie de filtrare mai puternice (`embedding`, `bison`, `gecko`, `audio`, `realtime`, `babbage`, `moderation`, `deep`, `antigravity`, `computer`) pentru ca lista derulantă a modelului principal de chat să rămână perfect curată și pregătită pentru viitor, păstrând în același timp toate modelele specializate accesibile în secțiunea Rutare avansată.
- **Căutare în rutarea avansată**: Toate listele derulante din Rutarea avansată a modelelor (OCR, STT, TTS, Operator, Video, Live) și selectorul de variante eSpeak pot fi acum căutate complet. Poți tasta rapid pentru a filtra și găsi modelul sau varianta dorită.
- **Scurtături noi în stratul de comenzi**:
  - **Setări (`Alt + S`)**: Deschide instant dialogul de setări Vision Assistant Pro.
  - **Raport chei cu cotă epuizată (`Alt + Q`)**: Raportează numărul exact de chei API Gemini care și-au depășit cota zilnică, identifică modelul specific pe care sunt epuizate și anunță ora exactă de resetare.
  - **Audit rutare (`Alt + M`)**: Auditează și anunță configurația curentă de Rutare avansată, citind modelele selectate activ pentru sarcini specializate și ignorând setările implicite.
- **Revizuire completă a Analizatorului video**: Analizatorul video a fost transformat complet! Înainte oferea doar o descriere de bază a videoclipurilor online. Acum este o suită completă de procesare video, adaptată pentru utilizatorii nevăzători:
  - **Înregistrare locală a ecranului (`Control+V`)**: Acum poți înregistra videoclipuri fără sunet direct de pe ecran. AI-ul va analiza segmentul înregistrat și va furniza o descriere foarte detaliată a scenei, structurii și acțiunilor.
  - **Generare descriere audio (SRT)**: Add-on-ul poate genera acum scripturi de descriere audio foarte detaliate, în format SRT standard, pentru videoclipuri, cu temporizare inteligentă pe pauze, pentru a ancora descrierile în pauzele naturale ale pistei audio, și cu OCR verbatim pentru orice text de pe ecran.
  - **Narațiune audio sincronizată (export MP3)**: Dincolo de subtitrările text, add-on-ul poate sintetiza descrierea audio în vorbire, o poate mixa automat cu pista audio originală a videoclipului, poate aplica atenuare audio (reducerea volumului de fundal în timpul descrierilor) și poate exporta rezultatul final sincronizat ca fișier MP3!
  - **Acțiune inteligentă pentru fișiere video**: Dacă focalizezi un fișier video local și apeși scurtătura video, add-on-ul îl va detecta automat și va procesa fișierul direct.
  - **Urmărire avansată a personajelor**: AI-ul face acum o trecere preliminară pentru extragerea personajelor. Construiește un dicționar global de personaje și urmărește personajele cu acuratețe, segment cu segment, fără a confunda identitățile.
  - **Configurare analiză video**: Au fost adăugate setări noi pentru controlul dimensiunii segmentelor SRT, subtitrarea personajelor și avertismente.
  - **Rutare extinsă a modelelor**: Acum poți selecta explicit modele video specializate (`gemini_video_model`, `custom_video_model`) în setările de Rutare avansată a modelelor.
- **Gestionare inteligentă a cotelor API**: Gestionarea erorilor 429 (limită zilnică) a fost îmbunătățită prin urmărirea cotelor pe fiecare model. Dacă o cheie își atinge limita zilnică pe un model, aceasta este carantinată inteligent doar pentru acel model, rămânând disponibilă pentru alte modele.

## Modificări pentru 7.0.0

- **Reluarea scanărilor neterminate**: A fost adăugată o funcție de reluare atât pentru Cititorul de documente, cât și pentru Acțiunile inteligente pentru fișiere. Dacă o scanare este întreruptă, acum poți continua de unde s-a oprit în loc să o iei de la început.
- **Variabila nouă `[screen_fg_obj]`**: A fost adăugată o variabilă de prompt personalizat pentru capturarea unei capturi de ecran doar a ferestrei active din prim-plan, în locul întregului ecran.
- **Reîncercări inteligente și rotația cheilor**: Add-on-ul reîncearcă acum în mod silențios de până la 5 ori cu aceeași cheie când apar supraîncărcări temporare ale serverului, cum ar fi „cerere ridicată” sau răspunsuri formatate incorect. Dacă reîncercările eșuează, trece automat la următoarea cheie API din listă.
- **Detectarea Perdelei ecranului**: A fost adăugată o verificare care împiedică realizarea capturilor de ecran când Perdeaua ecranului este activă, indiferent dacă este activată permanent sau temporar cu scurtătura. Vei fi avertizat, iar operația se va opri, împiedicând trimiterea imaginilor negre și risipirea tokenilor API.
- **Ajustări pentru Cititorul de documente**: Dialogul intervalului PDF preselectează acum automat limba țintă implicită din setările add-on-ului. De asemenea, gestionarea firelor de execuție a fost îmbunătățită pentru a asigura oprirea corectă a sarcinilor din fundal când cititorul este închis.
- **Integrare nativă Mistral OCR**: A fost integrat API-ul nativ Document OCR de la Mistral. Documentele cu mai multe pagini sunt îmbinate, încărcate și procesate automat în loturi prin endpointul specializat `/v1/ocr` al Mistral, iar imaginile cu o singură pagină sunt procesate direct, fără conversii inutile în PDF [1].
- **Gestionare dinamică a URL-urilor personalizate**: Modificarea URL-ului API personalizat șterge acum instantaneu lista de modele din cache și restaurează caseta de text pentru introducerea manuală a modelului. Astfel se asigură compatibilitate completă cu endpointuri personalizate, precum Cloudflare AI Gateway, care nu acceptă endpointul standard de listare `/v1/models`.
- **Motor de intrare AI Operator reproiectat**: Sistemul de simulare a mouse-ului și tastaturii folosit de AI Operator a fost rescris complet. API-ul vechi `mouse_event` a fost înlocuit cu API-ul modern Windows `SendInput`, oferind compatibilitate mult mai bună cu aplicațiile moderne, ferestrele protejate prin UAC și ecranele cu DPI ridicat.
- **Operații drag-and-drop remediate**: Acțiunile de tragere și plasare din AI Operator sunt acum complet stabile și fiabile. Noul motor folosește curbe naturale de accelerare și decelerare („easing”), poziționare precisă a cursorului, temporizare optimizată și o tehnică inteligentă de „nudge”, astfel încât Windows și aplicațiile să recunoască și să execute corect gesturile de tragere și plasare fără eșecuri la jumătatea acțiunii.
- **Suport pentru mai multe monitoare**: AI Operator acceptă acum complet configurațiile cu mai multe monitoare. Mișcările și clicurile mouse-ului funcționează corect pe toate monitoarele folosind indicatorul `MOUSEEVENTF_VIRTUALDESK`, asigurând poziționarea precisă indiferent de monitorul pe care se află aplicația țintă.
- **Simulare îmbunătățită a tastaturii**: Injectarea tastelor a fost îmbunătățită pentru a accepta complet „tastele extinse”, precum tastele săgeți, Home, End, Page Up/Down, Insert, Delete și F1-F12. Astfel, comenzile de navigare și scurtăturile trimise de AI Operator funcționează impecabil în toate aplicațiile.
- **Suport pentru imagini HEIC/HEIF**: A fost adăugat suport nativ pentru formatele foto de iPhone. Acum poți selecta direct fișiere `.heic` și `.heif` pentru descriere AI, OCR sau citire în Cititorul de documente, fără conversie prealabilă.

## Modificări pentru 6.5.0

- **Asistent live**: A fost adăugată o funcție de asistent vocal și de ecran în timp real, disponibilă exclusiv pentru furnizorul Google Gemini sau pentru furnizori personalizați compatibili cu Gemini. Include personalizarea interactivă a vocii și a profunzimii de gândire direct în dialog, cu reconectare automată când se modifică setările.
- **Furnizor AI MiniMax**: MiniMax a fost integrat ca furnizor cu drepturi egale, cu suport multimodal complet (chat, viziune, OCR), TTS personalizat folosind peste 300 de voci dinamice și eliminarea automată a blocurilor de raționament (de exemplu, ` thinking... response`) din rezultate.
- **Traducerea în vizualizatorul de documente**: A fost corectată o eroare silențioasă de traducere pentru utilizatorii NVDA în alte limbi decât engleza, asigurând trimiterea codului standard de limbă din 2 litere către Google Translate în locul numelui localizat al limbii.
- **Reîncercare pentru scanarea PDF în lot**: A fost implementată o logică de reîncercare foarte optimizată, separată și silențioasă pentru scanarea documentelor PDF în lot, pentru a preveni încărcările redundante și pentru a evita popup-urile de eroare deranjante în timpul reîncercărilor.
- **Starea vizualizatorului de documente**: A fost remediată o eroare prin care starea generală a add-on-ului, verificată cu `I`, rămânea blocată pe „Procesarea lotului a început” în timpul scanărilor lungi de documente.
- **Blocare de threading rezolvată**: A fost remediată o blocare severă cauzată de aserțiunea de fir `IsMain() failed in wxTimerImpl` la deschiderea documentelor dintr-un fir de fundal, prin trecerea cozii de callback-uri GUI la `wx.CallAfter`.

## Modificări pentru 6.1.2

- **Preverificare pentru etichete duplicate**: A fost remediată o problemă în etichetarea individuală, unde verificarea duplicatelor folosea chei vechi bazate pe coordonate, făcând NVDA să trimită cereri AI duplicate pentru obiecte deja etichetate în loc să anunțe eticheta existentă.
- **Chat pentru documente cu furnizori non-Gemini**: A fost remediată o verificare strictă a cheii API în Chatul pentru documente (`on_ask`), astfel încât utilizatorii cu OpenAI, Groq sau furnizori personalizați locali, precum Ollama, să poată discuta cu documentele fără să fie blocați.
- **Traducere rapidă pentru Chrome OCR**: A fost restaurat API-ul gratuit de traducere, fără cheie, pentru Chrome OCR. Traducerea textului extras ocolește acum AI-ul Gemini, economisind cotele API și accelerând procesul de traducere.
- **Filtru alfanumeric pentru CAPTCHA**: A fost corectată logica de filtrare din rezolvatorul CAPTCHA, pentru a se asigura că caracterele non-alfanumerice sunt curățate corect în toate situațiile.
- **Actualizare ajutor pentru stratul de comenzi**: A fost corectată scurtătura pentru anunțarea stării din meniul de ajutor, de la `L` la `I`, și au fost adăugate în listă ambele comenzi de etichetare (`L` și `Shift+L`).

## Modificări pentru 6.1.1

- **Remediere pentru rezultatul de gândire Gemma 4**: A fost remediată o problemă cu modelele Gemma 4, în care întregul proces intern de gândire era afișat ca răspuns final sau în care dezactivarea gândirii producea răspunsuri goale. Add-on-ul izolează și extrage acum corect doar răspunsul final curat.
- **OCR în lot din File Explorer**: Acum poți selecta mai multe fotografii sau PDF-uri direct în Windows File Explorer și poți extrage textul sau le poți analiza în lot. Add-on-ul va filtra și procesa automat doar formatele de fișier acceptate.

## Modificări pentru 6.1.0

- **Integrare universală cu AI local (Configurează AI local)**: A fost adăugat un nou buton **„Configurează AI local”** în Setările furnizorului personalizat. Utilizatorii pot configura automat și instant motoare AI locale, inclusiv **Ollama**, **LM Studio**, **Jan.ai** și **KoboldCPP**.
- **Ocolire inteligentă a proxy-ului local**: Logica de conexiune a fost reconstruită cu un mecanism avansat de ocolire a proxy-ului. Add-on-ul poate acum ocoli complet proxy-urile de sistem Windows pentru conexiunile locale de tip loopback, asigurând conexiuni stabile cu AI local chiar și când VPN-ul sau proxy-ul în modul TUN este activ.
- **Etichetare AI ultra-stabilă (v2)**: Cheile bazate pe coordonate absolute de ecran au fost înlocuite cu un sistem avansat, hibrid, de **Semnătură a obiectului**. Etichetele se bazează acum pe identificatori programatici (UIA **AutomationId** sau Win32 **ControlID**) și pe coordonate relative la fereastră, făcând etichetele tale personalizate rezistente la redimensionarea, mutarea sau scalarea ferestrei și la schimbarea monitorului.
- **Migrare automată fără întreruperi a etichetelor**: Actualizarea este complet transparentă. Add-on-ul va migra automat etichetele tale vechi, bazate pe coordonate moștenite, în noul format stabil de amprentă în fundal, la prima focalizare, fără pierdere de date.

## Modificări pentru 6.0

- **Introducerea etichetării AI semantice**: Utilizatorii pot eticheta permanent butoane și pictograme fără nume folosind AI. Apasă **L** pentru a eticheta obiectul curent al navigatorului, cu suport pentru focalizarea prin Tab și navigarea pe obiecte, sau **Shift+L** pentru a scana și eticheta întreaga aplicație dintr-o singură acțiune.
- **Gestionare inteligentă a etichetelor**: A fost adăugat un dialog nou, complet accesibil, Manager de etichete, prin **Shift+L** dacă există etichete, pentru vizualizarea, redenumirea sau ștergerea în lot a etichetelor personalizate.
- **Analiză directă a fișierelor, fără dialogul de fișiere**: Add-on-ul poate detecta acum dacă focalizezi un fișier PDF sau imagine în Windows File Explorer. Când apeși **F (Acțiune inteligentă pentru fișiere)** sau **D (Cititor de documente)** pe un fișier evidențiat, acesta va fi procesat imediat, fără dialogul standard „Deschide”.

## Modificări pentru 5.6

- **A fost adăugat motorul OCR „Niciunul (extrage stratul de text)”**: Utilizatorii pot extrage acum textul direct din PDF-uri cu text selectabil fără a consuma credite AI, îmbunătățind semnificativ viteza și confidențialitatea pentru documentele bazate pe text.
- **A fost rafinată acuratețea UI Explorer**: Promptul UI Explorer a fost îmbunătățit pentru a identifica mai bine tipurile de elemente, cum ar fi elementele de listă, și pentru a raporta corect stări precum „(Bifat)”, „(Selectat)” sau „(Extins)”, ignorând componentele de sistem Windows precum bara de activități și ceasul.
- **Memento pentru configurare după instalare**: A fost adăugată o notificare după instalare pentru a ghida utilizatorii către meniul de setări, unde își pot configura cheile API și preferințele.

## Modificări pentru 5.5.2

- **A fost remediată problema de tastare din AI Operator:** A fost rezolvată o eroare prin care litera „v” era tastată în loc să se lipească textul pe anumite sisteme. Remedierea rezolvă conflictele de sincronizare care apăreau când sistemul era foarte solicitat.
- **Stabilitate îmbunătățită:** A fost adăugată gestionare robustă a erorilor pentru operațiile cu clipboardul, pentru a preveni blocarea add-on-ului când clipboardul sistemului este blocat temporar de alte aplicații.
- **Optimizare de sincronizare:** Au fost ajustate întârzierile interne pentru evenimentele de tastatură, pentru fiabilitate mai mare pe sisteme cu viteze diferite și compatibilitate mai bună cu manageri de clipboard terți.

## Modificări pentru 5.5 (actualizarea pentru automatizare)

- **AI Operator (control autonom, Shift+A):** Aceasta este funcția principală din v5.5. Vision Assistant Pro a trecut de la rolul de asistent pasiv la rolul de **AI Operator** personal. Nu descrie doar ecranul, ci execută comenzi.
  - _Cum funcționează:_ Acum poți da instrucțiuni verbale pentru a opera calculatorul. De exemplu, într-o aplicație complet inaccesibilă, unde cititorul tău de ecran nu spune nimic, poți apăsa **Shift+A** și poți tasta: _„Apasă butonul Setări”_ sau _„Găsește câmpul de căutare, scrie 'Latest News' și apasă Enter.”_ AI-ul identifică vizual elementele, mută mouse-ul și execută sarcina pentru tine.
  - _Notă de performanță:_ Această funcție este optimizată pentru **Gemini 3.0 Flash (Preview)** și oferă răspunsuri rapide și inteligente, capabile să gestioneze chiar și structuri UI complexe.
  - **⚠️ Avertisment privind utilizarea API:** Pentru ca AI Operator să fie precis, trebuie să „vadă” exact ce se întâmplă, deci trimite o captură de ecran de înaltă rezoluție la fiecare pas. Folosirea frecventă va consuma cota API mult mai repede decât sarcinile standard bazate pe text.
- **Visual UI Explorer (E):** Te-ai săturat să navighezi prin „butoane fără etichetă”? Apasă **E** pentru a activa UI Explorer. AI-ul va scana întreaga fereastră și va genera o listă cu fiecare element pe care îl poate apăsa, inclusiv pictograme, grafice și meniuri. Alegi un element din listă, iar AI Operator îl va apăsa pentru tine. Funcționează ca un strat accesibil peste orice aplicație.
- **Acțiune inteligentă pentru fișiere, adaptată contextului (F):** Tasta „F” a fost refăcută complet. Nu mai presupune că vrei doar OCR. Când selectezi o singură imagine, acum îți cere intenția: poți alege o **descriere vizuală detaliată** pentru a înțelege scena sau o **extragere structurată a textului (OCR)** pentru citire. Meniul se adaptează dinamic în funcție de tipul de fișier și motorul AI activ.
- **Optimizare de bază:** Am curățat în profunzime logica internă a add-on-ului, eliminând funcții vechi nefolosite și cod redundant. Rezultatul este o experiență mai rapidă și mai fiabilă pentru utilizatori.

## Modificări pentru 5.0

- **Arhitectură cu mai mulți furnizori**: A fost adăugat suport complet pentru **OpenAI**, **Groq** și **Mistral**, alături de Google Gemini. Utilizatorii pot alege acum backendul AI preferat.
- **Rutare avansată a modelelor**: Utilizatorii furnizorilor nativi, precum Gemini sau OpenAI, pot selecta acum modele specifice dintr-o listă derulantă pentru sarcini diferite (OCR, STT, TTS).
- **Configurare avansată a endpointurilor**: Utilizatorii furnizorului personalizat pot introduce manual URL-uri și nume de modele pentru control detaliat asupra serverelor locale sau terțe.
- **Vizibilitate inteligentă a funcțiilor**: Meniul de setări și interfața cititorului de documente ascund acum automat funcțiile neacceptate, cum ar fi TTS, în funcție de furnizorul selectat.
- **Preluare dinamică a modelelor**: Add-on-ul preia acum lista de modele disponibile direct din API-ul furnizorului, pentru compatibilitate cu modele noi imediat după lansare.
- **OCR și traducere hibridă**: A fost optimizată logica pentru a folosi Google Translate pentru viteză când este folosit Chrome OCR și traducere prin AI când sunt folosite motoarele Gemini/Groq/OpenAI.
- **„Rescanare cu AI” universală**: Funcția de rescanare din cititorul de documente nu mai este limitată la Gemini. Acum folosește furnizorul AI activ pentru a reprocesa paginile.

## Modificări pentru 4.6

- **Reafișare interactivă a rezultatului:** A fost adăugată tasta **Space** în stratul de comenzi, permițând utilizatorilor să redeschidă imediat ultimul răspuns AI într-o fereastră de chat pentru întrebări suplimentare, chiar și când modul „Ieșire directă” este activ.
- **Hub pentru comunitatea Telegram:** A fost adăugat un link „Canal Telegram oficial” în meniul Instrumente al NVDA, pentru acces rapid la cele mai recente noutăți, funcții și lansări.
- **Stabilitate îmbunătățită a răspunsurilor:** Logica principală pentru funcțiile de traducere, OCR și Vision a fost optimizată pentru performanță mai fiabilă și experiență mai fluidă când se folosește ieșirea vocală directă.
- **Ghidare îmbunătățită în interfață:** Descrierile din setări și documentația au fost actualizate pentru a explica mai bine noul sistem de reafișare și modul în care funcționează împreună cu setările pentru ieșire directă.

## Modificări pentru 4.5

- **Manager avansat de prompturi:** A fost introdus un dialog dedicat de administrare în setări, pentru personalizarea prompturilor de sistem implicite și gestionarea prompturilor definite de utilizator, cu suport complet pentru adăugare, editare, reordonare și previzualizare.
- **Suport proxy complet:** Au fost rezolvate problemele de conexiune la rețea prin aplicarea strictă a setărilor proxy configurate de utilizator pentru toate cererile API, inclusiv traducere, OCR și generare vocală.
- **Migrare automată a datelor:** A fost integrat un sistem inteligent de migrare, care actualizează automat configurațiile vechi ale prompturilor la un format JSON v2 robust la prima rulare, fără pierdere de date.
- **Compatibilitate actualizată (2025.1):** Versiunea minimă necesară de NVDA a fost setată la 2025.1, din cauza dependențelor de bibliotecă din funcții avansate precum cititorul de documente, pentru performanță stabilă.
- **Interfață de setări optimizată:** Interfața de setări a fost simplificată prin reorganizarea gestionării prompturilor într-un dialog separat, oferind o experiență mai curată și mai accesibilă.
- **Ghid pentru variabilele prompturilor:** A fost adăugat un ghid integrat în dialogurile de prompturi pentru a ajuta utilizatorii să identifice și să folosească ușor variabile dinamice precum [selection], [clipboard] și [screen_obj].

## Modificări pentru 4.0.3

- **Rezistență îmbunătățită a rețelei:** A fost adăugat un mecanism automat de reîncercare pentru a gestiona mai bine conexiunile instabile la internet și erorile temporare de server, asigurând răspunsuri AI mai fiabile.
- **Dialog vizual pentru traduceri:** A fost introdusă o fereastră dedicată pentru rezultatele traducerii. Utilizatorii pot naviga și citi ușor traduceri lungi linie cu linie, similar cu rezultatele OCR.
- **Vizualizare formatată agregată:** Funcția „Vizualizare formatată” din cititorul de documente afișează acum toate paginile procesate într-o singură fereastră organizată, cu antete clare pentru pagini.
- **Flux OCR optimizat:** Selectarea intervalului de pagini este omisă automat pentru documentele cu o singură pagină, făcând procesul de recunoaștere mai rapid.
- **Stabilitate API îmbunătățită:** S-a trecut la o metodă mai robustă de autentificare bazată pe antete, rezolvând posibile erori „All API Keys failed” cauzate de conflicte la rotația cheilor.
- **Remedieri de erori:** Au fost rezolvate mai multe blocări posibile, inclusiv o problemă la închiderea add-on-ului și o eroare de focalizare în dialogul de chat.

## Modificări pentru 4.0.1

- **Cititor de documente avansat:** Un vizualizator nou pentru PDF și imagini, cu selectare a intervalului de pagini, procesare în fundal și navigare fluentă cu `Ctrl+PageUp/Down`.
- **Submeniu nou în Instrumente:** A fost adăugat un submeniu dedicat „Vision Assistant” în meniul Instrumente al NVDA, pentru acces mai rapid la funcțiile principale, setări și documentație.
- **Personalizare flexibilă:** Acum poți alege motorul OCR și vocea TTS preferate direct din panoul de setări.
- **Suport pentru mai multe chei API:** A fost adăugat suport pentru mai multe chei API Gemini. Poți introduce o cheie pe linie sau le poți separa prin virgulă în setări.
- **Motor OCR alternativ:** A fost introdus un motor OCR nou pentru a asigura recunoaștere fiabilă a textului chiar și când sunt atinse limitele de cotă Gemini API.
- **Rotație inteligentă a cheilor API:** Comută automat la cea mai rapidă cheie API funcțională și o reține, pentru a evita limitele de cotă.
- **Document în MP3/WAV:** A fost integrată capacitatea de a genera și salva fișiere audio de calitate înaltă în formatele MP3 (128kbps) și WAV direct în cititor.
- **Suport pentru Instagram Stories:** A fost adăugată capacitatea de a descrie și analiza Instagram Stories folosind URL-urile lor.
- **Suport TikTok:** A fost introdus suport pentru videoclipuri TikTok, permițând descriere vizuală completă și transcriere audio a clipurilor.
- **Dialog de actualizare reproiectat:** Include o interfață accesibilă nouă, cu o casetă text derulabilă pentru citirea clară a modificărilor de versiune înainte de instalare.
- **Stare și UX unificate:** Dialogurile de fișiere au fost standardizate în tot add-on-ul, iar comanda „L” a fost îmbunătățită pentru raportarea progresului în timp real.

## Modificări pentru 3.6.0

- **Sistem de ajutor:** A fost adăugată o comandă de ajutor (`H`) în stratul de comenzi, pentru a oferi o listă ușor accesibilă cu toate scurtăturile și funcțiile lor.
- **Analiză video online:** Suportul a fost extins pentru a include videoclipuri **Twitter (X)**. Detectarea URL-urilor și stabilitatea au fost îmbunătățite pentru o experiență mai fiabilă.
- **Contribuție la proiect:** A fost adăugat un dialog opțional de donație pentru utilizatorii care vor să susțină actualizările viitoare și creșterea continuă a proiectului.

## Modificări pentru 3.5.0

\*   \*\*Strat de comenzi:\*\* A fost introdus un sistem de strat de comenzi, implicit `NVDA+Shift+V`, pentru a grupa scurtăturile sub o singură tastă principală. De exemplu, în loc să apeși `NVDA+Control+Shift+T` pentru traducere, acum apeși `NVDA+Shift+V`, apoi `T`.
\*   \*\*Analiză video online:\*\* A fost adăugată o funcție nouă pentru analiza videoclipurilor YouTube și Instagram direct prin introducerea unui URL.

## Modificări pentru 3.1.0

- **Mod ieșire directă:** A fost adăugată o opțiune pentru a omite dialogul de chat și a auzi răspunsurile AI direct prin vorbire, pentru o experiență mai rapidă.
- **Integrare cu clipboardul:** A fost adăugată o setare nouă pentru copierea automată a răspunsurilor AI în clipboard.

## Modificări pentru 3.0

- **Limbi noi:** Au fost adăugate traduceri în **persană** și **vietnameză**.
- **Modele AI extinse:** Lista de selectare a modelelor a fost reorganizată cu prefixe clare (`[Free]`, `[Pro]`, `[Auto]`), pentru a ajuta utilizatorii să distingă modelele gratuite de cele cu frecvență limitată a cererilor (plătite). A fost adăugat suport pentru **Gemini 3.0 Pro** și **Gemini 2.0 Flash Lite**.
- **Stabilitate pentru dictare:** Stabilitatea dictării inteligente a fost îmbunătățită mult. A fost adăugată o verificare de siguranță care ignoră clipurile audio mai scurte de 1 secundă, prevenind halucinațiile AI și erorile goale.
- **Gestionarea fișierelor:** A fost remediată o problemă prin care încărcarea fișierelor cu nume non-englezești eșua.
- **Optimizarea prompturilor:** Logica de traducere și rezultatele Vision structurate au fost îmbunătățite.

## Modificări pentru 2.9

- **Au fost adăugate traduceri în franceză și turcă.**
- **Vizualizare formatată:** A fost adăugat un buton „Vizualizare formatată” în dialogurile de chat, pentru a vedea conversația cu stilizare corectă, cum ar fi titluri, bold și cod, într-o fereastră standard navigabilă.
- **Setare Markdown:** A fost adăugată o opțiune nouă „Curăță Markdown în chat” în Setări. Debifarea acesteia permite utilizatorilor să vadă sintaxa Markdown brută, de exemplu `**` sau `#`, în fereastra de chat.
- **Gestionarea dialogurilor:** A fost remediată o problemă prin care ferestrele „Rafinează textul” sau chat se deschideau de mai multe ori sau nu primeau focalizarea corect.
- **Îmbunătățiri UX:** Titlurile dialogurilor de fișiere au fost standardizate la „Deschide” și au fost eliminate anunțurile vocale redundante, de exemplu „Se deschide meniul...”, pentru o experiență mai fluidă.

## Modificări pentru 2.8

- A fost adăugată traducerea în italiană.
- **Raportare stare:** A fost adăugată o comandă nouă (NVDA+Control+Shift+I) pentru anunțarea stării curente a add-on-ului, de exemplu „Se încarcă...” sau „Se analizează...”.
- **Export HTML:** Butonul „Salvează conținutul” din dialogurile de rezultat salvează acum ieșirea ca fișier HTML formatat, păstrând stiluri precum titluri și text bold.
- **Interfață de setări:** Aspectul panoului Setări a fost îmbunătățit cu grupare accesibilă.
- **Modele noi:** A fost adăugat suport pentru gemini-flash-latest și gemini-flash-lite-latest.
- **Limbi:** A fost adăugată nepaleza la limbile acceptate.
- **Logica meniului de rafinare:** A fost remediată o eroare critică prin care comenzile „Rafinează textul” eșuau dacă limba interfeței NVDA nu era engleza.
- **Dictare:** Detectarea tăcerii a fost îmbunătățită pentru a preveni ieșiri text incorecte când nu este detectată vorbire.
- **Setări de actualizare:** „Caută actualizări la pornire” este acum dezactivată implicit pentru respectarea politicilor Add-on Store.
- Curățare cod.

## Modificări pentru 2.7

- Structura proiectului a fost migrată la șablonul oficial NV Access Add-on Template, pentru conformitate mai bună cu standardele.
- A fost implementată logica de reîncercare automată pentru erori HTTP 429 (limită de rată), pentru fiabilitate în perioade cu trafic ridicat.
- Prompturile de traducere au fost optimizate pentru acuratețe mai mare și gestionare mai bună a logicii „Smart Swap”.
- Traducerea în rusă a fost actualizată.

## Modificări pentru 2.6

- A fost adăugat suport pentru traducerea în rusă, mulțumiri nvda-ru.
- Mesajele de eroare au fost actualizate pentru feedback mai descriptiv privind conectivitatea.
- Limba țintă implicită a fost schimbată în engleză.

## Modificări pentru 2.5

- A fost adăugată comanda nativă OCR pentru fișiere (NVDA+Control+Shift+F).
- A fost adăugat butonul „Salvează chatul” în dialogurile de rezultat.
- A fost implementat suport complet pentru localizare (i18n).
- Feedbackul audio a fost migrat la modulul nativ de tonuri al NVDA.
- S-a trecut la Gemini File API pentru gestionarea mai bună a fișierelor PDF și audio.
- A fost remediată blocarea la traducerea textului care conține acolade.

## Modificări pentru 2.1.1

- A fost remediată o problemă prin care variabila [file_ocr] nu funcționa corect în prompturile personalizate.

## Modificări pentru 2.1

- Toate scurtăturile au fost standardizate pentru a folosi NVDA+Control+Shift, pentru a elimina conflictele cu aspectul Laptop al NVDA și tastele rapide de sistem.

## Modificări pentru 2.0

- A fost implementat sistemul integrat de actualizare automată.
- A fost adăugat cache inteligent pentru traduceri, pentru recuperarea instantanee a textului tradus anterior.
- A fost adăugată memorie conversațională pentru rafinarea contextuală a rezultatelor în dialogurile de chat.
- A fost adăugată o comandă dedicată pentru traducerea clipboardului (NVDA+Control+Shift+Y).
- Prompturile AI au fost optimizate pentru a impune strict ieșirea în limba țintă.
- A fost remediată blocarea cauzată de caractere speciale în textul de intrare.

## Modificări pentru 1.5

- A fost adăugat suport pentru peste 20 de limbi noi.
- A fost implementat dialogul interactiv de rafinare pentru întrebări suplimentare.
- A fost adăugată funcția nativă de dictare inteligentă.
- A fost adăugată categoria „Vision Assistant” în dialogul Gesturi de intrare al NVDA.
- Au fost remediate blocările COMError în aplicații specifice precum Firefox și Word.
- A fost adăugat mecanismul automat de reîncercare pentru erori de server.

## Modificări pentru 1.0

- Lansare inițială.
