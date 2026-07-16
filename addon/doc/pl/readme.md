# Pomoc Vision Assistant Pro

**Vision Assistant Pro** to wielofunkcyjny asystent AI dla NVDA wykorzystujący silniki AI do odczytywania ekranu, tłumaczenia, dyktowania głosowego i analizy dokumentów.

_Ten dodatek został udostępniony społeczności z okazji Międzynarodowego Dnia Osób z Niepełnosprawnościami._

## 1. Konfiguracja

Przejdź do **Menu NVDA > Preferencje > Ustawienia > Vision Assistant Pro**.

### 1.1 Ustawienia połączenia
- **Dostawca:** Wybierz preferowaną usługę AI. Obsługiwani dostawcy to **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** oraz **Niestandardowy** (serwery zgodne z OpenAI, np. Ollama/LM Studio).
- **Ważne:** Zalecamy korzystanie z **Google Gemini**, który zapewnia najlepszą jakość (szczególnie przy analizie obrazów i plików).
- **Klucz API:** Wymagany. Można podać wiele kluczy (rozdzielonych przecinkami lub w osobnych wierszach), aby dodatek rotował je automatycznie.
- **Pobierz modele:** Po wprowadzeniu klucza API naciśnij ten przycisk, aby pobrać aktualną listę dostępnych modeli od dostawcy.
- **Model AI:** Wybierz główny model używany do czatu i analizy.

### 1.2 Osobny model dla każdego zadania
*Dostępne dla wszystkich dostawców, w tym Gemini, OpenAI, Groq, Mistral i Niestandardowy.*

> **⚠️ Uwaga:** Te ustawienia są przeznaczone wyłącznie dla **doświadczonych użytkowników**. Jeśli nie wiesz, do czego służy dany model, zostaw tę opcję **odznaczoną**. Wybranie nieodpowiedniego modelu (np. modelu tekstowego dla zadań wizualnych) spowoduje błędy i zatrzyma działanie dodatku.

Zaznacz **„Osobny model dla każdego zadania"**, aby uzyskać szczegółową kontrolę. Pozwala to wybrać konkretne modele z listy rozwijanej dla różnych zadań:
- **Model dla OCR / rozpoznawania obrazów:** Wyspecjalizowany model do analizy obrazów.
- **Rozpoznawanie mowy (STT):** Konkretny model do dyktowania.
- **Synteza mowy (TTS):** Model do generowania audio.
- **Model Operatora AI:** Konkretny model do zadań autonomicznego sterowania komputerem.
*Uwaga: Nieobsługiwane funkcje (np. TTS dla Groq) zostaną automatycznie ukryte.*

### 1.3 Adresy usług (niestandardowy dostawca)
*Dostępne tylko przy wybranym dostawcy „Niestandardowy".*

> **⚠️ Uwaga:** Ta sekcja umożliwia ręczną konfigurację API i jest przeznaczona dla **zaawansowanych użytkowników** prowadzących lokalne serwery lub proxy. Błędne adresy URL lub nazwy modeli uniemożliwią połączenie. Jeśli nie wiesz dokładnie, do czego służą te pola, zostaw tę opcję **odznaczoną**.

Zaznacz **„Adresy usług"**, aby ręcznie podać dane serwera. W przeciwieństwie do natywnych dostawców, tutaj trzeba **wpisać** konkretne adresy URL i nazwy modeli:
- **URL listy modeli:** Adres do pobrania dostępnych modeli.
- **URL dla OCR/STT/TTS:** Pełne adresy usług (np. `http://localhost:11434/v1/audio/speech`).
- **Niestandardowe modele:** Wpisz ręcznie nazwę modelu (np. `llama3:8b`) dla każdego zadania.

### 1.4 Preferencje ogólne
- **Silnik OCR:** Wybierz między **Chrome (szybki)** dla błyskawicznych wyników a **AI (zaawansowany)** dla lepszego zachowania układu strony.
    - *Uwaga:* Jeśli wybierzesz „AI (zaawansowany)", ale dostawcą jest OpenAI/Groq, dodatek inteligentnie skieruje obraz do modelu rozpoznawania obrazów aktywnego dostawcy.
- **Głos TTS:** Wybierz preferowany styl głosu. Lista aktualizuje się automatycznie na podstawie aktywnego dostawcy.
- **Kreatywność (temperatura):** Kontroluje losowość odpowiedzi AI. Niższe wartości są lepsze dla tłumaczenia i OCR.
- **URL serwera proxy:** Skonfiguruj, jeśli usługi AI są ograniczone w twoim regionie (obsługuje lokalne proxy, np. `127.0.0.1`, oraz adresy pośredniczące).

## 2. Warstwa poleceń i skróty

Aby uniknąć konfliktów z innymi skrótami, dodatek korzysta z **warstwy poleceń**.
1. Naciśnij **NVDA + Shift + V** (klawisz główny), aby aktywować warstwę (usłyszysz sygnał dźwiękowy).
2. Puść klawisze, a następnie naciśnij jeden z poniższych:

| Klawisz       | Funkcja                       | Opis                                                                        |
|---------------|-------------------------------|-----------------------------------------------------------------------------|
| **Shift + A** | **Operator AI**               | **Sterowanie autonomiczne:** Powiedz AI, aby wykonała zadanie na ekranie.   |
| **E**         | **Eksplorator interfejsu**    | **Interaktywne klikanie:** Identyfikuje i klika elementy interfejsu w dowolnej aplikacji. |
| **T**         | Tłumacz                       | Tłumaczy tekst pod kursorem nawigatora lub zaznaczenie.                     |
| **Shift + T** | Tłumaczenie schowka           | Tłumaczy zawartość schowka.                                                 |
| **R**         | Poprawianie tekstu            | Podsumuj, popraw gramatykę, wyjaśnij lub uruchom **niestandardowe polecenie**. |
| **V**         | Opis obiektu                  | Opisuje bieżący obiekt nawigatora.                                          |
| **O**         | Rozpoznawanie ekranu          | Analizuje układ i zawartość całego ekranu.                                  |
| **Shift + V** | Analiza wideo online          | Analizuj filmy z **YouTube**, **Instagrama**, **TikToka** lub **Twittera (X)**, a także lokalne pliki wideo. |
| **Control + V** | Nagrywanie ekranu           | **Analiza lokalnego nagrania:** Nagrywa bezgłośny film z ekranu, po czym AI opisuje scenę, układ i akcję. |
| **D**         | Czytnik dokumentów            | Czytnik PDF i obrazów z wyborem zakresu stron.                              |
| **F**         | **Akcja na pliku**            | Rozpoznawanie zależne od kontekstu z wybranego obrazu, PDF lub TIFF.        |
| **A**         | Transkrypcja audio            | Transkrybuje pliki MP3, WAV lub OGG na tekst.                               |
| **C**         | Rozwiązywanie CAPTCHA         | Przechwytuje i rozwiązuje CAPTCHA.                                          |
| **S**         | Dyktowanie                    | Zamienia mowę na tekst. Naciśnij raz, aby nagrywać, ponownie, aby zakończyć. |
| **Control+L** | **Asystent głosowy**          | **W czasie rzeczywistym (tylko Gemini):** Rozpoczyna lub kończy rozmowę głosową i ekranową z asystentem AI. |
| **I**         | Raport stanu                  | Odczytuje bieżący postęp (np. „Skanowanie...", „Bezczynny").                |
| **L**         | **Oznacz obiekt**             | **Semantyczne etykietowanie AI:** Trwale oznacza bieżący element/ikonę.     |
| **Shift + L** | **Zarządzaj / Skanuj etykiety** | Otwiera Menedżer etykiet (jeśli istnieją) lub skanuje aplikację w poszukiwaniu nieoznaczonych elementów. |
| **U**         | Sprawdzanie aktualizacji      | Ręcznie sprawdza najnowszą wersję dodatku na GitHubie.                      |
| **Spacja**    | Ostatnia odpowiedź AI         | Wyświetla ostatnią odpowiedź AI w oknie czatu do przeglądu lub kontynuacji. |
| **H**         | Pomoc poleceń                 | Wyświetla listę wszystkich dostępnych skrótów w warstwie poleceń.           |

### 2.1 Skróty czytnika dokumentów (wewnątrz przeglądarki)
- **Ctrl + PageDown:** Przejdź do następnej strony.
- **Ctrl + PageUp:** Przejdź do poprzedniej strony.
- **Alt + A:** Otwórz okno czatu, aby zadać pytanie o dokument.
- **Alt + R:** Wymuś **ponowne skanowanie AI** przy użyciu aktywnego dostawcy.
- **Alt + G:** Wygeneruj i zapisz plik audio (WAV/MP3). *Ukryte, jeśli dostawca nie obsługuje TTS.*
- **Alt + S / Ctrl + S:** Zapisz wyodrębniony tekst jako plik TXT lub HTML.

## 3. Polecenia niestandardowe i zmienne

Tymi poleceniami można zarządzać w **Ustawienia > Polecenia > Zarządzaj poleceniami...**.

### Obsługiwane zmienne
- `[selection]`: Aktualnie zaznaczony tekst.
- `[clipboard]`: Zawartość schowka.
- `[screen_obj]`: Zrzut ekranu obiektu nawigatora.
- `[screen_fg_obj]`: Zrzut ekranu aktywnego okna pierwszoplanowego.
- `[screen_full]`: Zrzut całego ekranu.
- `[file_ocr]`: Wybierz obraz/PDF do wyodrębnienia tekstu.
- `[file_read]`: Wybierz dokument do odczytu (TXT, kod, PDF).
- `[file_audio]`: Wybierz plik audio do analizy (MP3, WAV, OGG).

***
**Uwaga:** Wszystkie funkcje AI wymagają aktywnego połączenia z internetem. Dokumenty wielostronicowe są przetwarzane automatycznie.

## 4. Wsparcie i społeczność

Bądź na bieżąco z najnowszymi wiadomościami i aktualizacjami:
- **Kanał w Telegramie:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Zgłaszanie błędów i propozycje nowych funkcji.

## 5. Patroni projektu

Serdecznie dziękujemy członkom społeczności, którzy swoimi hojnymi wkładami finansowymi wspierają ciągły rozwój i utrzymanie tego projektu:

*   **@Alyabani94**
*   **Ali Alamri**
*   **Anonimowy wspierający** (`UQDd...CnMY`)
*   **leonardo0216**

*Jeśli chcesz wesprzeć projekt finansowo i zobaczyć tutaj swoje imię, opcję **Wsparcie** znajdziesz w menu Narzędzia NVDA (podmenu Vision Assistant) albo podczas konfiguracji po instalacji.*


---
## Zmiany w wersji 2026.07.15

* **Filtrowanie modeli API:** Przebudowano system filtrowania modeli na czarną listę zamiast białych list, z mocniejszymi słowami kluczowymi, dzięki czemu lista głównego modelu czatu pozostaje czysta, a wszystkie wyspecjalizowane modele są nadal dostępne w sekcji osobnego modelu dla każdego zadania.
* **Wyszukiwanie w przydziale modeli:** Wszystkie listy rozwijane osobnego modelu dla każdego zadania (OCR, STT, TTS, Operator, Wideo, Asystent głosowy) oraz wybór wariantu eSpeak są teraz przeszukiwalne. Wystarczy wpisać frazę, aby przefiltrować i znaleźć żądany model lub wariant.
* **Nowe skróty:** ustawienia (**Alt + S**), raport kluczy z wyczerpanym dziennym limitem wraz z modelem i czasem resetu (**Alt + Q**) oraz audyt bieżącej konfiguracji modeli (**Alt + M**).
* **Całkowita przebudowa analizy wideo:** Analizator wideo, który wcześniej dawał jedynie podstawowy opis filmów online, robi teraz znacznie więcej. Doszło lokalne nagrywanie ekranu (**Control + V**) z szczegółowym opisem sceny, układu i akcji, generowanie audiodeskrypcji w formacie SRT z dopasowaniem opisów do naturalnych pauz i dosłownym OCR tekstu na ekranie, oraz zsynchronizowana narracja dźwiękowa z eksportem do MP3, z automatycznym przyciszaniem tła podczas opisów. Dodano też akcję na lokalnym pliku wideo, śledzenie postaci z globalnym słownikiem postaci oraz osobne modele wideo w przydziale modeli.
* **Zarządzanie limitami API:** Ulepszono obsługę błędów 429 (dzienny limit) przez śledzenie limitów osobno dla każdego modelu. Klucz, który wyczerpie limit na jednym modelu, jest izolowany tylko dla niego i pozostaje dostępny dla pozostałych modeli.

---
## Zmiany w wersji 7.0.0

* **Wznawianie niedokończonych skanów:** Dodano wznawianie w czytniku dokumentów i w akcjach na pliku. Jeśli skan zostanie przerwany, można teraz kontynuować od miejsca zatrzymania zamiast zaczynać od nowa.
* **Nowa zmienna `[screen_fg_obj]`:** Dodano zmienną do poleceń niestandardowych, która przechwytuje zrzut ekranu tylko aktywnego okna pierwszoplanowego zamiast całego ekranu.
* **Ponawianie i rotacja kluczy:** Dodatek ponawia teraz po cichu do 5 razy na tym samym kluczu przy chwilowym przeciążeniu serwera (np. „duży ruch” lub błędne odpowiedzi). Jeśli ponawianie się nie powiedzie, automatycznie przełącza na następny klucz API z listy.
* **Wykrywanie kurtyny ekranowej:** Dodano sprawdzanie, które zapobiega robieniu zrzutów ekranu, gdy kurtyna ekranowa jest aktywna (na stałe albo włączona chwilowo skrótem). Ostrzega i zatrzymuje działanie, chroniąc przed wysyłaniem czarnych obrazów i marnowaniem tokenów API.
* **Poprawki czytnika dokumentów:** Okno zakresu stron PDF wybiera teraz automatycznie domyślny język docelowy z ustawień dodatku. Ulepszono też obsługę wątków, aby zadania w tle zatrzymywały się czysto po zamknięciu czytnika.
* **Natywna integracja Mistral OCR:** Zintegrowano natywne API Document OCR firmy Mistral. Dokumenty wielostronicowe są automatycznie łączone, przesyłane i przetwarzane wsadowo przez wyspecjalizowany endpoint `/v1/ocr` Mistrala, a obrazy jednostronicowe są przetwarzane bezpośrednio, bez zbędnej konwersji do PDF.
* **Dynamiczna obsługa niestandardowych adresów URL:** Zmiana niestandardowego adresu API czyści teraz natychmiast zbuforowaną listę modeli i przywraca pole ręcznego wpisania modelu. Zapewnia to pełną zgodność z niestandardowymi endpointami (np. Cloudflare AI Gateway), które nie obsługują standardowego endpointu listy `/v1/models`.
* **Przebudowany silnik wejścia Operatora AI:** Całkowicie przepisano system symulacji myszy i klawiatury dla Operatora AI. Zastąpiono stare API `mouse_event` nowoczesnym API `SendInput` systemu Windows, co daje znacznie większą zgodność z nowoczesnymi aplikacjami, oknami chronionymi przez UAC i ekranami o wysokim DPI.
* **Naprawiono przeciąganie i upuszczanie:** Przeciąganie i upuszczanie w Operatorze AI jest teraz w pełni stabilne i niezawodne. Nowy silnik używa naturalnych krzywych wygładzania, precyzyjnego pozycjonowania kursora, zoptymalizowanego czasu i techniki muśnięcia kursorem, aby Windows i aplikacje poprawnie rozpoznawały i wykonywały gesty przeciągania bez przerywania w połowie.
* **Obsługa wielu monitorów:** Operator AI w pełni obsługuje teraz zestawy z wieloma monitorami. Ruchy i kliknięcia myszy działają poprawnie na wszystkich monitorach dzięki fladze `MOUSEEVENTF_VIRTUALDESK`, zapewniając dokładne pozycjonowanie niezależnie od tego, na którym monitorze znajduje się docelowa aplikacja.
* **Ulepszona symulacja klawiatury:** Poprawiono wprowadzanie klawiszy, aby w pełni obsługiwać klawisze rozszerzone (strzałki, Home, End, Page Up/Down, Insert, Delete i F1-F12). Zapewnia to bezbłędne działanie poleceń nawigacji i skrótów wysyłanych przez Operatora AI we wszystkich aplikacjach.
* **Obsługa obrazów HEIC/HEIF:** Dodano natywną obsługę formatów zdjęć iPhone. Można teraz bezpośrednio wybierać pliki `.heic` i `.heif` do opisu AI, OCR lub czytania dokumentów bez wcześniejszej konwersji.

## Zmiany w wersji 6.5.0

*   **Asystent głosowy**: Dodano funkcję asystenta głosowego i ekranowego w czasie rzeczywistym, dostępną wyłącznie dla dostawcy Google Gemini (lub zgodnych z Gemini dostawców niestandardowych). Obejmuje interaktywną zmianę głosu i głębi myślenia bezpośrednio w oknie dialogowym, z automatycznym ponownym połączeniem po zmianie ustawień.
*   **Dostawca MiniMax**: Zintegrowano MiniMax jako równorzędnego dostawcę z pełną obsługą multimodalną (czat, obraz, OCR), własnym TTS z ponad 300 dynamicznymi głosami oraz automatycznym usuwaniem bloków rozumowania (np. `<think>...</think>`) z odpowiedzi.
*   **Tłumaczenie w czytniku dokumentów**: Naprawiono ciche niepowodzenie tłumaczenia u osób korzystających z NVDA w językach innych niż angielski, dbając o to, by do Google Translate trafiał standardowy dwuliterowy kod języka zamiast zlokalizowanej nazwy.
*   **Ponawianie skanowania wsadowego PDF**: Wprowadzono zoptymalizowaną, osobną i cichą logikę ponawiania przy skanowaniu wsadowym dokumentów PDF, aby zapobiec zbędnym przesłaniom i uniknąć uciążliwych okienek z błędami podczas ponawiania.
*   **Status czytnika dokumentów**: Naprawiono błąd, przez który ogólny status dodatku (sprawdzany przez `I`) pozostawał zatrzymany na „Rozpoczęto przetwarzanie wsadowe" podczas długiego skanowania dokumentów.
*   **Naprawiona awaria wątkowania**: Naprawiono poważną awarię (`IsMain() failed in wxTimerImpl`) przy otwieraniu dokumentów z wątku działającego w tle, przenosząc kolejkę wywołań GUI na `wx.CallAfter`.

---
## Zmiany w wersji 6.1.2

*   **Wstępne sprawdzanie duplikatów etykiet**: Naprawiono błąd w pojedynczym etykietowaniu, w którym sprawdzanie duplikatów używało starych kluczy współrzędnych, przez co NVDA wysyłał zduplikowane zapytania AI dla już oznaczonych obiektów zamiast odczytać istniejącą etykietę.
*   **Czat z dokumentem dla dostawców innych niż Gemini**: Naprawiono zbyt rygorystyczne sprawdzanie klucza API w czacie z dokumentem (`on_ask`), aby na OpenAI, Groq lub lokalnych dostawcach niestandardowych (jak Ollama) dało się rozmawiać z dokumentami bez blokady.
*   **Szybkie tłumaczenie OCR w Chrome**: Przywrócono darmowe API tłumaczenia bez klucza dla OCR w Chrome. Tłumaczenie wyodrębnionego tekstu pomija teraz Gemini AI, oszczędzając limity API i przyspieszając proces tłumaczenia.
*   **Filtr alfanumeryczny CAPTCHA**: Poprawiono logikę filtrowania w rozwiązywaniu CAPTCHA, aby znaki niealfanumeryczne były prawidłowo usuwane we wszystkich sytuacjach.
*   **Aktualizacja pomocy poleceń**: Poprawiono w menu pomocy skrót do raportowania stanu z `L` na `I` oraz dodano do listy oba polecenia etykietowania (`L` i `Shift+L`).

---
## Zmiany w wersji 6.1.1

*   **Poprawka myślenia w modelach Gemma 4**: Naprawiono błąd w modelach Gemma 4, w którym cały wewnętrzny proces myślenia był wyświetlany jako finalna odpowiedź, lub w którym wyłączenie myślenia skutkowało pustymi odpowiedziami. Dodatek poprawnie wyodrębnia teraz tylko czysty, finalny tekst odpowiedzi.
*   **Wsadowy OCR z Eksploratora plików**: Teraz można zaznaczyć wiele zdjęć lub plików PDF bezpośrednio w Eksploratorze plików Windows i wsadowo wyodrębnić z nich tekst lub je przeanalizować. Dodatek automatycznie odfiltruje i przetworzy tylko obsługiwane formaty plików.

---
## Zmiany w wersji 6.1.0

*   **Uniwersalna integracja lokalnej AI (Konfiguracja lokalnej AI)**: Dodano nowy przycisk **„Konfiguracja lokalnej AI"** w ustawieniach niestandardowego dostawcy. Teraz można od razu automatycznie skonfigurować lokalne silniki AI, w tym **Ollama**, **LM Studio**, **Jan.ai** i **KoboldCPP**.
*   **Ominięcie lokalnego proxy**: Przebudowano logikę połączenia z zaawansowanym mechanizmem omijania proxy. Dodatek całkowicie omija systemowe proxy Windows przy połączeniach lokalnych, dzięki czemu połączenie z lokalną AI jest stabilne nawet przy aktywnym VPN lub trybie TUN.
*   **Awaryjne zatrzymanie Operatora AI (Shift+A)**: Dodano wyzwalacz zatrzymania. Naciśnięcie polecenia Operatora AI (**Shift+A** w warstwie poleceń) podczas trwającej operacji autonomicznej natychmiast przerywa pętlę i ogłasza *„Operator AI zatrzymany."*
*   **Bardzo stabilne etykietowanie AI (v2)**: Zastąpiono klucze oparte na bezwzględnych współrzędnych ekranu zaawansowanym, hybrydowym systemem **sygnatur obiektów**. Etykiety opierają się teraz na identyfikatorach programowych (UIA **AutomationId** lub Win32 **ControlID**) oraz współrzędnych względem okna, dzięki czemu są one całkowicie odporne na zmianę rozmiaru, przesuwanie, zmianę monitora czy skalowanie okna.
*   **Płynna automatyczna migracja etykiet**: Aktualizacja jest całkowicie przezroczysta. Dodatek automatycznie przeniesie starsze etykiety oparte na współrzędnych do nowego, stabilnego formatu sygnatur w tle przy pierwszym ustawieniu fokusu, bez utraty danych.

---
## Zmiany w wersji 6.0

*   **etykietowanie AI**: Teraz można trwale nadawać etykiety nienazwanym przyciskom i ikonom za pomocą AI. Naciśnij **L**, by oznaczyć bieżący obiekt nawigatora (obsługa zarówno fokusu Tab, jak i nawigacji obiektowej), lub **Shift+L**, by przeskanować i oznaczyć całą aplikację naraz.
*   **Zarządzanie etykietami**: Nowe, w pełni dostępne okno Menedżer etykiet (przez **Shift+L**, jeśli etykiety istnieją) pozwala przeglądać, zmieniać nazwy i zbiorczo usuwać etykiety.
*   **Bezpośrednia analiza pliku (z pominięciem okna dialogowego)**: Dodatek wykrywa, czy fokus znajduje się na pliku PDF lub graficznym w Eksploratorze Windows. Naciśnięcie **F (Akcja na pliku)** lub **D (Czytnik dokumentów)** na zaznaczonym pliku natychmiast go przetworzy, pomijając standardowe okno „Otwórz".

## Zmiany w wersji 5.6

* **Dodano silnik OCR „Wyodrębnij tekst (offline)”:** Teraz można wyodrębniać tekst bezpośrednio z plików PDF z warstwą tekstową, bez zużywania kredytów AI, co daje znaczne przyspieszenie i większą prywatność dokumentów tekstowych.
* **Lepsza dokładność Eksploratora interfejsu:** Ulepszono prompt eksploratora, by trafniej rozpoznawał typy elementów (np. element listy) i precyzyjnie raportował stany takie jak „(zaznaczony)”, „(wybrany)” albo „(rozwinięty)”, pomijając jednocześnie komponenty systemu Windows jak pasek zadań i zegar.
* **Przypomnienie o konfiguracji po instalacji:** Dodano powiadomienie po instalacji, które prowadzi do menu ustawień, by skonfigurować klucze API i preferencje.

## Zmiany w wersji 5.5.2

* **Naprawa błędu wpisywania w Operatorze AI:** Rozwiązano błąd, w którym litera „v" była wpisywana zamiast wklejania tekstu na niektórych systemach. Poprawka usuwa konflikty czasowe występujące przy dużym obciążeniu systemu.
* **Większa stabilność:** Dodano solidną obsługę błędów dla operacji na schowku, aby zapobiec awariom dodatku, gdy schowek systemowy jest tymczasowo zablokowany przez inne aplikacje.
* **Optymalizacja czasu reakcji:** Dostosowano wewnętrzne opóźnienia zdarzeń klawiatury w celu zapewnienia większej niezawodności na różnych prędkościach systemowych i lepszej zgodności z zewnętrznymi menedżerami schowka.

## Zmiany w wersji 5.5 (Aktualizacja automatyzacji)

* **Operator AI (Sterowanie autonomiczne - Shift+A):** To perła w koronie wersji 5.5. Vision Assistant Pro przeszedł z biernego asystenta w Twojego osobistego **Operatora AI**. Nie tylko opisuje ekran, lecz przejmuje sterowanie.
    * *Jak to działa:* Możesz teraz wydawać AI instrukcje słowne, aby obsługiwała Twój komputer. Na przykład w całkowicie niedostępnej aplikacji, gdzie czytnik ekranu milczy, możesz nacisnąć **Shift+A** i wpisać: *"Kliknij przycisk Ustawienia"* lub *"Znajdź pole wyszukiwania, wpisz 'Najnowsze wiadomości' i naciśnij enter."* AI wizualnie identyfikuje elementy, przesuwa kursor i wykonuje zadanie za Ciebie.
    * *Uwaga o wydajności:* Funkcja jest zoptymalizowana dla **Gemini 3.0 Flash (Preview)**, dostarczając niezwykle szybkich i inteligentnych odpowiedzi, które poradzą sobie nawet z najbardziej złożonymi układami interfejsu.
    * **⚠️ Ostrzeżenie o zużyciu API:** Ponieważ Operator AI musi „widzieć" dokładnie to, co się dzieje, aby działać precyzyjnie, wysyła zrzut ekranu w wysokiej rozdzielczości na każdym kroku. Częste używanie znacznie szybciej zużyje Twój limit API niż standardowe zadania tekstowe.
* **Wizualny Eksplorator interfejsu (E):** Zmęczony nawigacją po „nieoznaczonych przyciskach"? Naciśnij **E**, aby uruchomić Eksplorator interfejsu. AI przeskanuje całe okno i wygeneruje listę każdego klikalnego elementu, jaki widzi: ikon, grafik i menu. Wybierz element z listy, a Operator AI kliknie go za Ciebie. To jak „warstwa dostępności" nałożona na dowolną aplikację.
* **Akcja na pliku zależna od kontekstu (F):** Klawisz „F" został gruntownie przebudowany. Nie zakłada już, że chcesz tylko OCR. Gdy wybierzesz pojedynczy obraz, zapyta o Twoją intencję: możesz wybrać **Szczegółowy opis wizualny**, aby zrozumieć scenę, lub **Strukturalne wyodrębnienie tekstu (OCR)** do czytania. Menu dostosowuje się dynamicznie do typu pliku i aktywnego silnika AI.
* **Optymalizacja rdzenia:** Wykonaliśmy głębokie czyszczenie wewnętrznej logiki dodatku, usuwając nieużywane funkcje legacy i zbędny kod. Daje to lżejsze, szybsze i bardziej niezawodne działanie.

## Zmiany w wersji 5.0

* **Wielu dostawców**: Dodano pełną obsługę **OpenAI**, **Groq** i **Mistral** obok Google Gemini. Teraz można wybrać preferowany model AI.
* **Przypisywanie modeli do zadań**: Użytkownicy natywnych dostawców (Gemini, OpenAI itp.) mogą teraz wybierać konkretne modele z listy rozwijanej dla różnych zadań (OCR, STT, TTS).
* **Adresy usług**: Użytkownicy niestandardowych dostawców mogą ręcznie wprowadzać konkretne adresy URL i nazwy modeli np. dla skonfigurowania lokalnego modelu.
* **Ukrywanie nieobsługiwanych funkcji**: Menu ustawień i interfejs czytnika dokumentów automatycznie ukrywają nieobsługiwane funkcje (np. TTS) na podstawie wybranego dostawcy.
* **Pobieranie modeli z API**: Dodatek pobiera listę dostępnych modeli bezpośrednio z API dostawcy, co umożliwia obsługę nowych modeli natychmiast po ich wydaniu.
* **Hybrydowe OCR i tłumaczenie**: Zoptymalizowano logikę, aby używać Tłumacza Google dla szybkości przy OCR Chrome oraz tłumaczenia opartego na AI przy silnikach Gemini/Groq/OpenAI.
* **Ponowne skanowanie AI**: Funkcja ponownego skanowania w czytniku dokumentów nie jest już ograniczona do Gemini. Wykorzystuje teraz aktywnego dostawcę AI do ponownego przetwarzania stron.

## Zmiany w wersji 4.6
* **Przywołanie ostatniego wyniku:** Dodano klawisz **Spacja** do warstwy poleceń, umożliwiający natychmiastowe ponowne otwarcie ostatniej odpowiedzi AI w oknie czatu, nawet gdy aktywny jest tryb bezpośredni.
* **Kanał w Telegramie:** Dodano link do oficjalnego kanału Telegram w menu Narzędzia NVDA, umożliwiając szybki dostęp do najnowszych wiadomości i aktualizacji.
* **Stabilność odpowiedzi:** Zoptymalizowano logikę tłumaczenia, OCR i rozpoznawania, aby zapewnić bardziej niezawodne działanie i płynniejsze odczytywanie wyników.
* **Lepsza dokumentacja:** Zaktualizowano opisy ustawień i dokumentację, aby lepiej wyjaśnić system przywoływania wyników i jego współdziałanie z trybem bezpośrednim.

## Zmiany w wersji 4.5
* **Menedżer poleceń:** Dodano dedykowane okno dialogowe w ustawieniach do zarządzania domyślnymi poleceniami systemowymi i poleceniami użytkownika, z pełną obsługą dodawania, edycji, zmiany kolejności i podglądu.
* **Obsługa proxy:** Rozwiązano problemy z łącznością, zapewniając prawidłowe stosowanie ustawień proxy do wszystkich żądań API, w tym tłumaczenia, OCR i generowania mowy.
* **Migracja danych:** Dodano system migracji, który automatycznie aktualizuje starsze konfiguracje poleceń do formatu JSON v2 przy pierwszym uruchomieniu, bez utraty danych.
* **Kompatybilność z NVDA 2025.1:** Ustawiono minimalną wymaganą wersję NVDA na 2025.1 ze względu na zależności biblioteczne w funkcjach czytnika dokumentów.
* **Uproszczony interfejs ustawień:** Uporządkowano interfejs ustawień, przenosząc zarządzanie poleceniami do osobnego okna dialogowego.
* **Przewodnik po zmiennych:** Dodano wbudowany przewodnik w oknach dialogowych poleceń, ułatwiający korzystanie ze zmiennych dynamicznych, takich jak [selection], [clipboard] i [screen_obj].

## Zmiany w wersji 4.0.3
* **Obsługa niestabilnego połączenia:** Dodano mechanizm automatycznych ponownych prób, aby lepiej radzić sobie z chwilowymi błędami serwera i niestabilnym połączeniem.
* **Okno tłumaczenia:** Dodano dedykowane okno dla wyników tłumaczenia. Długie tłumaczenia można teraz przeglądać wiersz po wierszu, podobnie jak wyniki OCR.
* **Zbiorczy podgląd sformatowany:** Funkcja „Podgląd sformatowany" w czytniku dokumentów wyświetla teraz wszystkie przetworzone strony w jednym uporządkowanym oknie z nagłówkami stron.
* **Szybszy OCR:** Dla dokumentów jednostronicowych pomijany jest wybór zakresu stron, co przyspiesza proces rozpoznawania.
* **Stabilność API:** Zmieniono metodę uwierzytelniania na opartą o nagłówki HTTP, eliminując błędy „Wszystkie klucze API zawiodły" powodowane przez konflikty rotacji kluczy.
* **Poprawki błędów:** Naprawiono kilka potencjalnych awarii, w tym problem przy zamykaniu dodatku oraz błąd fokusu w oknie czatu.

## Zmiany w wersji 4.0.1
* **Czytnik dokumentów:** Nowa przeglądarka PDF i obrazów z wyborem zakresu stron, przetwarzaniem w tle i nawigacją Ctrl+PageUp/Down.
* **Podmenu Narzędzia:** Dodano podmenu „Vision Assistant" w menu Narzędzia NVDA, umożliwiające szybki dostęp do głównych funkcji, ustawień i dokumentacji.
* **Konfiguracja:** Teraz można wybrać preferowany silnik OCR i głos TTS bezpośrednio w panelu ustawień.
* **Wiele kluczy API:** Dodano obsługę wielu kluczy API Gemini. Klucze można podać po jednym w wierszu lub rozdzielone przecinkami.
* **Alternatywny silnik OCR:** Dodano nowy silnik OCR, zapewniający niezawodne rozpoznawanie tekstu nawet po przekroczeniu limitów API Gemini.
* **Rotacja kluczy API:** Automatyczne przełączanie na najszybszy działający klucz API, aby obejść limity.
* **Eksport audio:** Możliwość generowania i zapisywania plików audio w formatach MP3 (128 kbps) i WAV bezpośrednio z czytnika.
* **Instagram Stories:** Dodano możliwość opisu i analizy Instagram Stories za pomocą adresów URL.
* **TikTok:** Dodano obsługę filmów TikTok, umożliwiając opis wizualny i transkrypcję audio.
* **Okno aktualizacji:** Nowy dostępny interfejs z polem tekstowym do przejrzenia zmian przed instalacją.
* **Ujednolicenie interfejsu:** Ustandaryzowano okna dialogowe plików w całym dodatku i rozszerzono polecenie „L" o raportowanie postępu w czasie rzeczywistym.

## Zmiany w wersji 3.6.0
* **System pomocy:** Dodano polecenie pomocy (`H`) w warstwie poleceń, wyświetlające listę wszystkich skrótów i ich funkcji.
* **Analiza wideo online:** Rozszerzono obsługę o filmy z **Twittera (X)**. Poprawiono wykrywanie adresów URL i stabilność.
* **Wsparcie projektu:** Dodano opcjonalne okno darowizn dla osób chcących wesprzeć dalszy rozwój projektu.

## Zmiany w wersji 3.5.0
* **Warstwa poleceń:** Wprowadzono system warstwy poleceń (domyślnie: `NVDA+Shift+V`), grupujący skróty pod jednym klawiszem głównym. Na przykład zamiast naciskać `NVDA+Control+Shift+T` do tłumaczenia, wystarczy nacisnąć `NVDA+Shift+V`, a potem `T`.
* **Analiza wideo online:** Dodano nową funkcję analizy filmów z YouTube i Instagrama na podstawie adresu URL.

## Zmiany w wersji 3.1.0
* **Tryb bezpośredni:** Dodano opcję pomijania okna czatu i odczytywania odpowiedzi AI bezpośrednio przez syntezator mowy.
* **Kopiowanie do schowka:** Dodano ustawienie automatycznego kopiowania odpowiedzi AI do schowka.

## Zmiany w wersji 3.0

* **Nowe języki:** Dodano tłumaczenia na **perski** i **wietnamski**.
* **Rozszerzenie modeli AI:** Uporządkowano listę modeli z czytelnymi prefiksami (`[Darmowy]`, `[Pro]`, `[Auto]`), ułatwiając rozróżnienie modeli darmowych i płatnych. Dodano obsługę **Gemini 3.0 Pro** i **Gemini 2.0 Flash Lite**.
* **Stabilność dyktowania:** Znacząco poprawiono stabilność dyktowania. Dodano zabezpieczenie ignorujące nagrania krótsze niż 1 sekunda, zapobiegając halucynacjom AI i pustym błędom.
* **Obsługa plików:** Naprawiono problem z przesyłaniem plików o nazwach zawierających znaki spoza alfabetu łacińskiego.
* **Polecenia:** Poprawiono logikę tłumaczenia i ustrukturyzowano wyniki rozpoznawania.

## Zmiany w wersji 2.9

* **Dodano tłumaczenia na francuski i turecki.**
* **Podgląd sformatowany:** Dodano przycisk „Podgląd sformatowany" w oknach czatu, umożliwiający wyświetlenie rozmowy z prawidłowym formatowaniem (nagłówki, pogrubienie, kod) w standardowym oknie przeglądarki.
* **Ustawienie Markdown:** Dodano opcję „Czyść Markdown w czacie" w ustawieniach. Odznaczenie pozwala widzieć surową składnię Markdown (np. `**`, `#`) w oknie czatu.
* **Zarządzanie oknami:** Naprawiono problem z wielokrotnym otwieraniem okien „Poprawianie tekstu" lub czatu.
* **Usprawnienia interfejsu:** Ujednolicono tytuły okien dialogowych plików na „Otwórz" i usunięto zbędne komunikaty głosowe (np. „Otwieranie menu...").

## Zmiany w wersji 2.8
* Dodano tłumaczenie na włoski.
* **Raport stanu:** Dodano polecenie (NVDA+Control+Shift+I) odczytujące bieżący stan dodatku (np. „Przesyłanie...", „Analizowanie...").
* **Eksport HTML:** Przycisk „Zapisz treść" w oknach wyników zapisuje teraz dane jako sformatowany plik HTML, zachowując style takie jak nagłówki i pogrubienia.
* **Interfejs ustawień:** Poprawiono układ panelu ustawień z dostępnym grupowaniem.
* **Nowe modele:** Dodano obsługę gemini-flash-latest i gemini-flash-lite-latest.
* **Języki:** Dodano nepalski do obsługiwanych języków.
* **Poprawianie tekstu:** Naprawiono błąd, przez który polecenia „Poprawianie tekstu" nie działały, gdy język interfejsu NVDA nie był angielski.
* **Dyktowanie:** Poprawiono wykrywanie ciszy, aby zapobiec błędnemu rozpoznawaniu tekstu przy braku mowy.
* **Ustawienia aktualizacji:** Opcja „Sprawdzaj aktualizacje przy uruchomieniu" jest teraz domyślnie wyłączona, zgodnie z polityką Add-on Store.
* Porządki w kodzie.

## Zmiany w wersji 2.7
* Przeniesiono strukturę projektu na oficjalny szablon dodatków NV Access, zapewniając zgodność ze standardami.
* Dodano automatyczne ponawianie prób przy błędach HTTP 429 (limit zapytań), poprawiając niezawodność w okresach dużego ruchu.
* Zoptymalizowano polecenia tłumaczenia dla wyższej dokładności i lepszej obsługi logiki „Zamień języki".
* Zaktualizowano tłumaczenie rosyjskie.

## Zmiany w wersji 2.6
* Dodano tłumaczenie na rosyjski (podziękowania dla nvda-ru).
* Zaktualizowano komunikaty o błędach, aby lepiej informowały o problemach z łącznością.
* Zmieniono domyślny język docelowy na angielski.

## Zmiany w wersji 2.5
* Dodano polecenie OCR pliku (NVDA+Control+Shift+F).
* Dodano przycisk „Zapisz czat" w oknach wyników.
* Wdrożono pełną obsługę lokalizacji (i18n).
* Przeniesiono sygnały dźwiękowe na natywny moduł NVDA.
* Przejście na Gemini File API dla lepszej obsługi plików PDF i audio.
* Naprawiono awarię przy tłumaczeniu tekstu zawierającego nawiasy klamrowe.

## Zmiany w wersji 2.1.1
* Naprawiono problem z nieprawidłowym działaniem zmiennej [file_ocr] w poleceniach niestandardowych.

## Zmiany w wersji 2.1
* Ustandaryzowano wszystkie skróty na NVDA+Control+Shift, eliminując konflikty z układem laptopowym NVDA i skrótami systemowymi.

## Zmiany w wersji 2.0
* Wbudowany system automatycznych aktualizacji.
* Pamięć podręczna tłumaczeń, umożliwiająca natychmiastowe przywoływanie wcześniej przetłumaczonych tekstów.
* Pamięć kontekstu rozmowy w oknach czatu, umożliwiająca doprecyzowywanie wyników.
* Dedykowane polecenie tłumaczenia schowka (NVDA+Control+Shift+Y).
* Zoptymalizowano polecenia AI, aby ściślej wymuszać język docelowy.
* Naprawiono awarię powodowaną przez znaki specjalne w tekście wejściowym.

## Zmiany w wersji 1.5
* Dodano obsługę ponad 20 nowych języków.
* Dodano okno dialogowe do doprecyzowywania wyników za pomocą pytań uzupełniających.
* Dodano wbudowane dyktowanie.
* Dodano kategorię „Vision Assistant" w oknie Zdarzenia wejścia NVDA.
* Naprawiono awarie COMError w niektórych aplikacjach, takich jak Firefox i Word.
* Dodano mechanizm automatycznego ponawiania prób przy błędach serwera.

## Zmiany w wersji 1.0
* Pierwsze wydanie.
