# Pomoc Vision Assistant Pro

<!-- DOWNLOAD_COUNT_START --> Pobrań łącznie: 61 000+ <!-- DOWNLOAD_COUNT_END -->

**Vision Assistant Pro** to wielomodalny asystent AI dla NVDA. Korzysta z silników AI, żeby odczytywać ekran, tłumaczyć, zapisywać mowę i analizować dokumenty.

_Dodatek trafił do społeczności z okazji Międzynarodowego Dnia Osób z Niepełnosprawnościami._

## 1. Konfiguracja

Przejdź do **menu NVDA > Preferencje > Ustawienia > Vision Assistant Pro**. Okno ustawień jest podzielone na 9 zakładek: **Połączenie**, **Asystent głosowy**, **Zachowanie AI**, **Języki tłumaczenia**, **Czytnik dokumentów**, **Wideo**, **CAPTCHA**, **Polecenia** i **Zaawansowane**.

### 1.1 Zakładka Połączenie
- **Dostawca:** wybór usługi AI. Obsługiwani dostawcy to **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** oraz **Niestandardowy** (serwery zgodne z OpenAI, na przykład Ollama, LM Studio, Jan.ai albo KoboldCPP).
- **Klucz API:** jeden klucz albo kilka (rozdzielonych przecinkami lub nowymi wierszami) do automatycznej rotacji.
- **Pobierz modele:** po wpisaniu klucza ten przycisk pobiera od dostawcy aktualną listę modeli.
- **Model AI:** główny model używany do rozmowy i analizy.
- **Ustawienia niestandardowego dostawcy:** konfiguracja lokalnych i własnych adresów usług. Są tu dwie rzeczy: przycisk **Konfiguracja lokalnej AI**, który jednym kliknięciem ustawia Ollama, LM Studio, Jan.ai albo KoboldCPP, oraz **Adresy usług** do ręcznego wpisania własnego adresu.
- **Osobny model dla każdego zadania:** można wskazać osobne modele dla OCR, STT, TTS, Operatora AI, wideo i asystenta głosowego.
- **Opcje połączenia i wyjścia:** adres proxy, sprawdzanie aktualizacji przy starcie, czyszczenie Markdownu w czacie, kopiowanie odpowiedzi AI do schowka, tryb bezpośredni (nie pokazuje okna czatu) oraz tryb bezpośredni asystenta głosowego.
- **Zapisuj czaty w historii:** decyduje, czy rozmowy trafiają na listę historii.

### 1.2 Zakładka Asystent głosowy
- **Asystent głosowy: tryb bezpośredni (bez okna):** uruchamia asystenta bez okna rozmowy; można je otworzyć później klawiszem przywołania ostatniego wyniku (`Spacja`).
- **Naciśnij i mów:** włącza tryb naciśnij i mów. Gdy jest aktywny, mikrofon wysyła dźwięk tylko wtedy, gdy trzymasz przypisany klawisz.
- **Klawisz funkcji Naciśnij i mów:** naciśnij klawisze, aby zapisać skrót (na przykład `F12` lub `Ctrl+F12`). Możesz przypisać nawet sam modyfikator, taki jak `lewy Ctrl`. Przytrzymaj klawisz, aby mówić, i zwolnij go po zakończeniu; każde naciśnięcie i zwolnienie potwierdza krótki sygnał.

Uwaga: ta zakładka pojawia się tylko wtedy, gdy aktywnym dostawcą jest **Google Gemini** (lub zgodny z Gemini dostawca niestandardowy).

### 1.3 Zakładka Zachowanie AI
- **Kreatywność (temperatura):** steruje losowością odpowiedzi (od 0,0 do 2,0). Niższe wartości dają bardziej przewidywalne odpowiedzi. Nie wpływa na OCR ani na tłumaczenie.

### 1.4 Zakładka Języki tłumaczenia
- **Język źródłowy:** domyślny język wejściowy.
- **Język docelowy:** główny język tłumaczenia.
- **Język odpowiedzi AI:** język ogólnych odpowiedzi AI.
- **Zamiana:** automatycznie zamienia język źródłowy z docelowym na podstawie wykrytego wejścia.

### 1.5 Zakładka Czytnik dokumentów
- **Silnik OCR:** do wyboru **Chrome (szybki)** albo **AI (zaawansowany)**, który lepiej zachowuje układ strony.
- **Porcja OCR:** liczba stron na jedno żądanie (0 wyłącza dzielenie i wysyła wszystko w jednym żądaniu).
- **Wplataj opisy obrazów w tekst:** przy wyodrębnianiu treści dokumentu opis obrazu ląduje dokładnie tam, gdzie w dokumencie znajduje się obraz, a nie osobno na końcu.
- **Numery stron przy eksporcie:** włącza numery stron i separatory w dokumentach wielostronicowych.
- **Głos TTS:** domyślny styl głosu przy generowaniu mowy.
- **Zapisuj dokumenty w historii:** decyduje, czy otwierane dokumenty trafiają na listę historii. Zapamiętany tekst OCR i dane do wznowienia są zapisywane niezależnie od tej opcji.

### 1.6 Zakładka Wideo
- **Rozmiar fragmentu wideo:** długość odcinka w minutach przy generowaniu audiodeskrypcji (0 wyłącza dzielenie i przetwarza cały plik).
- **Dodaj listę postaci:** wstawia listę postaci jako pierwszy napis.
- **Dodaj informację o AI:** wstawia informację o udziale AI na początku napisów SRT do wideo.
- **Słownik postaci i seriale:** można dodawać, edytować, importować i porządkować imiona postaci, ich wygląd i role osobno dla każdego serialu. AI sama dopasowuje rozpoznane postacie do słownika i dopisuje nowe z każdym kolejnym analizowanym odcinkiem. Własne notatki zawsze mają pierwszeństwo przed zmianami wprowadzanymi przez AI, a opisy wyglądu pozostają aktualne między odcinkami.

### 1.7 Zakładka CAPTCHA

Dodatek radzi sobie z **dwoma rodzajami CAPTCHA**, a wybiera między nimi sam. Obsługuje je jeden skrót, **C** w warstwie poleceń, więc nie trzeba z góry wiedzieć, na którą się trafiło.

- **Klasyczna CAPTCHA tekstowa** to zniekształcony ciąg liter i cyfr do przepisania. AI odczytuje znaki z obrazu i wpisuje je za Ciebie.
- **CAPTCHA obrazkowa** to zagadka, w której trzeba klikać w obrazki o zadanych cechach: „zaznacz wszystkie pola z sygnalizatorem świetlnym”, „wybierz koty bez ogona”.

Po naciśnięciu **C** dodatek sprawdza, z czym ma do czynienia. Jeśli wykryje zagadkę obrazkową, mówi o tym i przechodzi w tryb rozwiązywania. To trwa dłużej niż odczytanie kodu. Jeśli obrazkowa jest wyłączona w ustawieniach, usłyszysz o tym.

Ustawienia:
- **Włącz rozwiązywanie CAPTCHA obrazkowej:** włącza i wyłącza obsługę zagadek obrazkowych (hCaptcha, reCAPTCHA). Wyłączenie nie rusza CAPTCHA tekstowej, ta działa dalej.
- **Metoda dla CAPTCHA tekstowej:** przechwytywanie **obiektu nawigatora** albo **całego ekranu**. Dotyczy wyłącznie kodów do przepisania.

### 1.8 Zakładka Polecenia
- **Zarządzaj poleceniami:** otwiera osobne okno, w którym można zmienić domyślne polecenia systemowe albo tworzyć, edytować, porządkować i podglądać własne polecenia ze zmiennymi (na przykład `[selection]`, `[screen_fg_obj]`).

### 1.9 Zakładka Zaawansowane i globalny dziennik
W zakładce **Zaawansowane** konfiguruje się globalny dziennik dodatku:
- **Włącz osobny plik dziennika:** zapisuje zdarzenia, ruch do API i błędy ze wszystkich modułów dodatku do osobnego pliku (`vision_assistant.log`).
- **Poziom szczegółowości dziennika:** **Diagnostyka (wszystkie szczegóły)**, **Informacje (ogólne)**, **Ostrzeżenia (tylko ostrzeżenia)** albo **Błędy (tylko błędy)**.
- **Przechowuj dziennik przez:** automatyczne czyszczenie starszych wpisów, od godziny do 90 dni.
- **Zarządzanie dziennikiem:** **Otwórz plik dziennika**, **Otwórz folder dziennika** i **Wyczyść plik dziennika** pozwalają zajrzeć do danych albo je usunąć bez restartu NVDA i bez mieszania się do standardowego dziennika NVDA.
- **Jeden folder na dane:** wszystkie pliki danych dodatku (historia, seriale, etykiety, postęp OCR, pamięć podręczna i dzienniki) leżą w jednym folderze `VisionAssistant` w katalogu konfiguracji NVDA. Wszystko jest w jednym miejscu, a ręczna kopia zapasowa nie wymaga szukania.

### 1.10 Kopia zapasowa i przywracanie ustawień
Zakładka **Zaawansowane** zawiera także sekcję **Kopia zapasowa i przywracanie**:
- **Kopia zapasowa:** zapisuje konfigurację do pojedynczego pliku JSON. Po kliknięciu wybierasz zakres: **Wszystko** (ustawienia, własne etykiety, postęp OCR i historia) albo **Tylko ustawienia**.
- **Przywróć:** wczytuje wcześniej zapisaną kopię, aby odtworzyć konfigurację i dane w dowolnej chwili, na dowolnym komputerze albo po ponownej instalacji NVDA. Najpierw pojawi się prośba o potwierdzenie, ponieważ przywracanie zastępuje wszystkie bieżące ustawienia i dane.

## 2. Warstwa poleceń i skróty

Aby uniknąć konfliktów skrótów klawiszowych, dodatek używa **warstwy poleceń**.
1. Naciśnij **NVDA + Shift + V** (klawisz główny), żeby włączyć warstwę (usłyszysz sygnał).
2. Puść klawisze, a potem naciśnij jeden z poniższych:

| Klawisz | Funkcja | Opis |
|---------------|--------------------------|-----------------------------------------------------------------------------|
| **Shift + A** | **Operator AI** | **Działanie autonomiczne:** zlecasz AI wykonanie zadania na ekranie. Ponowne naciśnięcie natychmiast przerywa trwającą operację. |
| **E** | **Eksplorator interfejsu** | **Kliknięcie interaktywne:** rozpoznaje i klika elementy interfejsu w dowolnej aplikacji. |
| **T** | Tłumacz | Tłumaczy tekst z obiektu nawigatora albo zaznaczenie. |
| **Shift + T** | Tłumacz schowka | Tłumaczy zawartość schowka. |
| **R** | Poprawianie tekstu | Streszcza, poprawia gramatykę, wyjaśnia albo uruchamia **polecenia niestandardowe**. |
| **V** | Opis obiektu | Opisuje bieżący obiekt nawigatora. |
| **O** | Opis całego ekranu | Analizuje układ i zawartość całego ekranu. |
| **Shift + V** | Analiza wideo | Analizuje lokalne pliki wideo oraz filmy z **YouTube**, **Instagrama**, **TikToka** i **Twittera (X)**. |
| **Control + V** | Nagrywanie ekranu | Nagrywa bezgłośne wideo z ekranu i analizuje przebieg oraz układ. |
| **D** | Czytnik dokumentów | Zaawansowany czytnik PDF i obrazów z wyborem zakresu stron. |
| **F** | **Akcja na pliku** | Rozpoznawanie zależne od kontekstu dla zaznaczonego obrazu, pliku PDF albo TIFF. |
| **M** | Transkrypcja i dubbing mediów | Transkrybuje albo dubbinguje pliki dźwiękowe i wideo (MP3, WAV, MP4 i inne) na język docelowy. |
| **C** | Rozwiązywanie CAPTCHA | Przechwytuje i rozwiązuje CAPTCHA, **tekstową i obrazkową jednym skrótem**. Rodzaj rozpoznaje sam. |
| **Shift + C** | Czat | Otwiera okno rozmowy tekstowej z AI. |
| **S** | Dyktowanie | Zamienia mowę na tekst. Naciśnij, żeby zacząć nagrywanie, i ponownie, żeby zakończyć i wpisać. |
| **Control + T** | Tłumaczenie mowy | Transkrybuje wypowiedź, tłumaczy ją i wpisuje wynik zgodnie z ustawieniami języków. |
| **Control + L** | **Asystent głosowy** | **Rozmowa w czasie rzeczywistym (tylko Gemini):** rozpoczyna albo kończy rozmowę głosową i ekranową z asystentem. |
| **I** | Ogłoś stan | Ogłasza bieżący postęp (na przykład „Skanowanie...”, „Bezczynny”). |
| **L** | **Etykietuj obiekt** | **Etykietowanie semantyczne:** trwale nazywa bieżący element albo ikonę. |
| **Shift + L** | **Zarządzaj/skanuj etykiety** | Otwiera menedżera etykiet (jeśli etykiety istnieją) albo skanuje aplikację w poszukiwaniu nienazwanych elementów. |
| **U** | Sprawdź aktualizację | Ręcznie sprawdza na GitHubie najnowszą wersję dodatku. |
| **Spacja** | Przywołaj ostatni wynik | Pokazuje ostatnią odpowiedź AI w oknie rozmowy do przejrzenia albo dopytania. |
| **H** | Pomoc poleceń | Wyświetla listę wszystkich dostępnych skrótów. |
| **Alt + S** | Ustawienia | Otwiera okno ustawień Vision Assistant Pro. |
| **Alt + Q** | Raport kluczy z wyczerpanym limitem | Podaje liczbę kluczy Gemini, które przekroczyły dzienny limit, wraz z czasem odnowienia. |
| **Alt + M** | Audyt przydziału modeli | Podaje modele AI wybrane obecnie w osobnym przydziale dla zadań. |
| **Góra / Dół** | Nawigacja po szybkich ustawieniach | Przechodzi między kategoriami szybkich ustawień (dostawca, model i inne) w warstwie. |
| **Lewo / Prawo** | Zmiana szybkiego ustawienia | Zmienia wartość wybranego szybkiego ustawienia. |

## 3. Czat i historia

### 3.1 Skróty okna czatu
Gdy okno czatu jest otwarte (czat bezpośredni, czat z dokumentem, dopracowywanie i podobne), możesz przeglądać rozmowę klawiszami:
- **Alt + strzałka w dół:** odczytuje następną wiadomość.
- **Alt + strzałka w górę:** odczytuje poprzednią wiadomość.
- **Alt + C:** kopiuje bieżącą wiadomość.

### 3.2 Historia (Control + H)
Naciśnij **Control + H** w warstwie poleceń, aby otworzyć okno **Historii** z wcześniejszymi czatami i dokumentami, z możliwością filtrowania według typu (Wszystko / Czaty / Dokumenty). Otwórz czat, aby kontynuować rozmowę razem z załączonymi plikami (dołączą się automatycznie), albo otwórz dokument i czytaj dalej. Naciśnij **Delete** na wybranej pozycji, aby ją usunąć, albo **Wyczyść wszystko**, aby opróżnić listę. Przy dokumentach Delete pyta, czy usunąć tylko wpis w historii, czy także zapamiętany tekst OCR tego dokumentu, żeby przy następnym otwarciu dokument zeskanował się od nowa. Pole **Nie pytaj ponownie** zapamiętuje wybór.

Można też zdecydować, co lista zapamiętuje. **Zapisuj czaty w historii** (zakładka Połączenie) i **Zapisuj dokumenty w historii** (zakładka Czytnik dokumentów) są domyślnie włączone i obie można przełączać w szybkich ustawieniach. Opcja dokumentów dotyczy wyłącznie wpisu w historii: zapamiętany tekst OCR i dane do wznowienia są zawsze zachowywane.

## 4. Operator AI: autonomiczne sterowanie komputerem

**Operator AI** zamienia Vision Assistant Pro z czytnika w asystenta, który działa na komputerze w Twoim imieniu. Można poprosić go o opis ekranu, o odpowiedź na pytanie o to, co widzi, albo oddać mu sterowanie: klikanie przycisków, przeciąganie elementów, wpisywanie tekstu i poruszanie się po aplikacjach zwykłym językiem.

Największa zaleta? Działa w oprogramowaniu całkowicie niedostępnym. Jeśli firmowa aplikacja, pulpit zdalny albo strona nie dają się obsłużyć, bo czytnik ekranu przy nich milczy, operatorowi to nie przeszkadza. Ponieważ „widzi” obraz ekranu, potrafi znaleźć, odczytać i obsłużyć elementy pozbawione jakichkolwiek etykiet dostępności.

### Jak to działa
1. Naciśnij **NVDA + Shift + V**, potem **Shift + A** (albo użyj skrótu bezpośredniego), żeby otworzyć okno Operatora AI.
2. Napisz zwykłym językiem, co ma zrobić (na przykład „Kliknij przycisk Zapisz”, „Co mówi komunikat błędu?”, „Zmień nazwę pliku na final.pdf”).
3. AI przeanalizuje ekran, rozpozna właściwe elementy i wykona zadanie albo poda odpowiedź. Jeśli zadanie wymaga kilku kroków, operator pracuje aż do końca.
4. Ponowne **Shift + A** w dowolnym momencie natychmiast przerywa trwającą operację.

### Obsługiwane działania
Operator rozumie między innymi takie polecenia:
- **Opis i odpowiedź**: „Opisz układ ekranu” albo „Co mówi komunikat błędu?”
- **Kliknięcie**: „Kliknij przycisk Zapisz”
- **Kliknięcie prawym przyciskiem**: „Kliknij plik prawym przyciskiem”
- **Dwukrotne kliknięcie**: „Kliknij dwukrotnie dokument”
- **Przeciągnij i upuść**: „Przeciągnij dokument do folderu Archiwum”
- **Wpisywanie**: „Wpisz »Witaj świecie« w polu wyszukiwania”
- **Przewijanie**: „Przewiń trzy razy w dół”
- **Naciśnięcie klawisza**: „Naciśnij Enter”, „Naciśnij Tab”, „Naciśnij Escape”
- **Zadania wieloetapowe**: „Otwórz Eksplorator plików, znajdź raport i zmień jego nazwę na final.pdf”

### Ważne uwagi
- **⚠️ Ostrzeżenie o zużyciu API**: operator musi „widzieć” dokładnie to, co dzieje się na ekranie, więc przy każdym kroku wysyła zrzut ekranu w wysokiej rozdzielczości. Częste korzystanie zużywa limit API dużo szybciej niż zwykłe funkcje tekstowe.
- **Aplikacje administracyjne**: jeśli NVDA nie działa z uprawnieniami administratora, operator może nie obsłużyć okien wymagających podwyższonych uprawnień. To ograniczenie bezpieczeństwa Windows, nie błąd dodatku.
- **Dobre praktyki**: najlepiej działają polecenia konkretne. „Kliknij niebieski przycisk Wyślij na dole formularza” zadziała prawie zawsze lepiej niż samo „Kliknij przycisk”.

## 5. Analiza wideo i audiodeskrypcja

> **Uwaga:** analiza wideo i audiodeskrypcja działają wyłącznie z dostawcą **Google Gemini**. Upewnij się, że w ustawieniach dodatku aktywnym dostawcą jest Google Gemini.

Vision Assistant Pro przetwarza wideo z myślą o osobach niewidomych. Analizuje zarówno filmy online, jak i lokalne nagrania ekranu. Daje szczegółowe opisy wizualne i gotowe skrypty audiodeskrypcji w formacie SRT.

### 5.1 Nagrywanie ekranu (Control + V)
Jeśli trafisz na bezgłośne wideo, animację albo poradnik na ekranie, możesz nagrać go bezpośrednio:
1. Naciśnij **NVDA + Shift + V**, żeby wejść w warstwę poleceń, potem **Control + V**.
2. Dodatek zacznie nagrywać ekran w tle.
3. Ponowne **Control + V** kończy nagrywanie.
4. AI przeanalizuje nagrany fragment i szczegółowo opisze scenę, postacie i przebieg zdarzeń.

### 5.2 Analiza wideo (Shift + V)
Analizować można zarówno lokalne pliki, jak i filmy online. Wystarczy zaznaczyć plik wideo w Eksploratorze Windows albo skopiować link do schowka. Można też nacisnąć **Shift + V** w dowolnym miejscu (na przykład w odtwarzaczu), żeby otworzyć okno, w którym wskazuje się plik albo wkleja adres ręcznie.
- **Obsługiwane serwisy:** YouTube, Instagram, TikTok i Twitter (X).
- Dodatek sam rozpozna plik lokalny albo adres, przetworzy wideo i poda pełny opis wizualny oraz podsumowanie dźwięku.
- **48-godzinna pamięć podręczna plików wideo:** wideo wysłane do Gemini jest pamiętane przez 48 godzin. Można ponownie wygenerować plik SRT albo MP3 dla tego samego wideo bez ponownego wysyłania, nawet po restarcie NVDA. Pamięć podręczna jest powiązana z kluczem API i unieważnia się sama, gdy klucz się zmieni.

### 5.3 Generowanie audiodeskrypcji (SRT)
Dodatek tworzy skrypty audiodeskrypcji w standardowym formacie SubRip (SRT).
- **Dopasowanie do pauz:** AI słucha ścieżki dźwiękowej i zaczepia opisy o naturalne pauzy i ciszę, żeby jak najmniej nachodziły na dialog.
- **Śledzenie postaci:** silnik najpierw wyodrębnia poszczególne postacie po niezmiennych cechach twarzy. Buduje globalny słownik, dzięki czemu rozpoznaje i nazywa te same osoby w różnych scenach bez pomyłek. Silnik zapamiętuje też **pierwsze pojawienie się** każdej postaci: opisuje jej wygląd tylko raz, w chwili gdy pojawia się po raz pierwszy, a w kolejnych scenach używa już samego imienia. Narracja się przez to nie powtarza.
- **Dosłowny OCR tekstu:** tekst widoczny na ekranie, na przykład szyldy, ekrany telefonów czy napisy końcowe, jest cytowany dosłownie.
- **Wygodniejszy zapis:** przy zapisie plików SRT lub MP3 okno zapisu otwiera się domyślnie w folderze wideo źródłowego, niezależnie od tego, czy wideo otwarto przez okno wyboru pliku, czy skrótem Shift+V z Eksploratora.
- **Jak z tego skorzystać:** żeby odsłuchać wygenerowane napisy, umieść plik `.srt` w tym samym folderze co wideo i nadaj mu dokładnie tę samą nazwę. Potem ustaw w odtwarzaczu (na przykład VLC albo PotPlayer) przekazywanie tekstu napisów wprost do czytnika ekranu albo silnika TTS podczas odtwarzania.

### 5.4 Zsynchronizowana narracja dźwiękowa (eksport MP3)
Dodatek nie kończy na plikach SRT. Zamienia opisy na mowę i miksuje je z wideo. Jako silnik głosu można wybrać **Gemini Live TTS**, który przez Gemini Live API tworzy bardzo naturalną narrację bez ograniczeń długości. Przy generowaniu MP3 dla plików lokalnych dostępnych jest kilka trybów miksowania:
- **Standardowa audiodeskrypcja (miks głosu):** narracja nakłada się bezpośrednio na dźwięk wideo. Pojawi się pytanie, czy zastosować **przyciszanie tła** podczas opisów, żeby narracja była wyraźna.
- **Rozszerzona audiodeskrypcja (pauza dźwięku):** silnik zatrzymuje oryginalny dźwięk na czas opisu, dzięki czemu nie umknie ani słowo dialogu, ani narracji. Do wykrywania ciszy służy teraz sieć neuronowa **Silero VAD** (pobierana automatycznie przy pierwszym użyciu, tak samo jak ffmpeg i eSpeak), która precyzyjnie dobiera przerwy i odróżnia naturalne pauzy w dialogu od muzyki i szumu tła.
- **Filmy z YouTube:** dla źródeł z YouTube (które nie są pobierane lokalnie) eksport MP3 zawiera wyłącznie zsynchronizowaną ścieżkę głosu AI, bez dźwięku tła.

## 6. Transkrypcja i dubbing mediów (M)
Moduł transkrypcji został napisany od nowa i obsługuje zarówno pliki dźwiękowe, jak i wideo (MP3, WAV, MP4, MKV i inne). Naciśnij **M** w warstwie poleceń, żeby wybrać plik i jeden z trzech trybów pracy:
1. **Transkrybuj (język oryginału)**: dokładnie transkrybuje wypowiedź w języku oryginału.
2. **Transkrybuj i przetłumacz (język docelowy)**: transkrybuje wypowiedź i tłumaczy ją na ustawiony język docelowy.
3. **Zdubbinguj i przetłumacz (język docelowy)** *(tylko Gemini)*: transkrybuje wypowiedź, tłumaczy ją na język docelowy i tworzy mówioną ścieżkę dźwiękową silnikiem TTS dodatku.

## 7. Zaawansowany czytnik dokumentów i obrazów

**Czytnik dokumentów** zamienia dokumenty w czysty, czytelny tekst. Tak przeczytasz, przetłumaczysz i odsłuchasz wszystko, od zeskanowanej książki po stos zdjęć. Obsługuje wielostronicowe pliki PDF, złożone obrazy, format HEIC z iPhone'a, a nawet zwykłe pliki tekstowe (`.txt`) oraz HTML (`.html`, `.htm`), które otwierają się natychmiast, bez OCR i bez przetwarzania przez AI. Możesz wybrać kilka plików naraz. Zostaną scalone w jeden ciągły dokument w kolejności stron. Dostępne są trzy silniki OCR: **Chrome (szybki)**, **AI (zaawansowany)** dla lepszego zachowania układu oraz **Wyodrębnij tekst (offline)** dla plików PDF z warstwą tekstową; wybiera się je w Ustawieniach → Czytnik dokumentów.

### Jak to działa
1. Naciśnij **NVDA + Shift + V**, a następnie **D**, aby otworzyć czytnik dokumentów. Możesz też najpierw zaznaczyć plik w Eksploratorze plików i nacisnąć **D** lub **F**, żeby pominąć okno wyboru pliku.
2. Wybierz jeden lub więcej plików PDF albo obrazów. Dodatek przeskanuje je i poda łączną liczbę stron.
3. W oknie **Opcje** wybierz zakres stron (Od/Do). Możesz też zaznaczyć **Tłumacz wynik** i wskazać język docelowy albo włączyć **Opisuj obrazy w trakcie OCR**.
4. Wyodrębnianie tekstu rusza w tle, partiami. Okno możesz zamknąć w dowolnej chwili i wrócić później. Nic nie ginie.
5. Gdy strony są gotowe, czytaj je w podglądzie: przechodź między stronami, skocz do dowolnej strony, zadawaj pytania AI, zapisz tekst albo wygeneruj narrację dźwiękową.

### 7.1 Przetwarzanie wsadowe i wznawianie
Nie trzeba czytać wielkiego dokumentu za jednym razem. Podaj zakres stron (na przykład `1-20`), a AI przetworzy je w tle. Jeśli NVDA przestanie działać albo przerwiesz skanowanie, dodatek zapamięta postęp i zaproponuje **wznowienie** dokładnie w miejscu przerwania.

### 7.2 Akcja na pliku
Nie zawsze trzeba najpierw otwierać dokument. W Eksploratorze plików Windows wystarczy zaznaczyć plik PDF albo obraz i w warstwie poleceń nacisnąć **D** (czytnik dokumentów) albo **F** (akcja na pliku). Dodatek pominie okno wyboru pliku i od razu zacznie przetwarzanie zaznaczonego dokumentu.

### 7.3 Skróty czytnika dokumentów
Gdy okno czytnika jest otwarte, działają następujące skróty:
#### Skróty klawiszowe
- **Ctrl + PageDown / Ctrl + PageUp:** przejście do następnej / poprzedniej strony.
- **Strzałka w dół / w górę:** gdy kursor dojdzie do ostatniego wiersza strony, naciśnij **strzałkę w dół**, aby przeskoczyć na następną stronę; naciśnięcie **strzałki w górę** na początku strony wraca do poprzedniej.
- **Alt + A:** okno rozmowy z pytaniami o dokument.
- **Alt + R:** wymuszenie **ponownego skanowania przez AI** aktywnym dostawcą.
- **Alt + G:** wygenerowanie i zapisanie pliku dźwiękowego wysokiej jakości (WAV/MP3). *(Ukryte, jeśli dostawca nie obsługuje TTS).*
- **Alt + S / Ctrl + S:** zapis wyodrębnionego tekstu jako plik TXT albo HTML.

#### Przyciski i elementy sterujące
- **Przejdź do:** wybór dowolnej strony z listy stron.
- **Pokaż sformatowany:** wyświetla cały dokument scalony jako sformatowany tekst.
- **Ponów nieudane strony:** ponawia wyłącznie te partie, które nie powiodły się z powodu tymczasowego błędu serwera (na przykład przy dużym obciążeniu). Przycisk pojawia się automatycznie wtedy, gdy jest potrzebny.
- **Głos syntezy / Silnik syntezy mowy:** wybór głosu, a przy dostawcy Gemini także wybór między **standardową syntezą mowy** a strumieniowym **Gemini Live**.
- **Poprzednia / Następna:** przechodzenie między stronami (to samo co skróty Ctrl+PageUp i Ctrl+PageDown).

### 7.4 Ostatnie dokumenty (D)
Naciśnięcie **D** w warstwie poleceń pokazuje najpierw ostatnio czytane dokumenty. Wybierz jeden, aby kontynuować od strony, na której przerwano czytanie (nawet jeśli OCR już się zakończył), albo naciśnij **Otwórz plik...** (`Ctrl + O`), aby wybrać plik jak zwykle.

## 8. Etykietowanie semantyczne i Eksplorator interfejsu

Aplikacja, w której wszędzie słychać „nieoznaczony przycisk”? Silnik etykietowania semantycznego rozwiązuje to na stałe.

### 8.1 Trwałe etykietowanie obiektu (L)
Ustaw czytnik na nieoznaczonej grafice albo przycisku i naciśnij **L** w warstwie poleceń. AI obejrzy przycisk, rozpozna jego funkcję i nada mu trwałą etykietę.
*W odróżnieniu od starszych narzędzi do etykietowania ten dodatek korzysta z hybrydowego systemu „sygnatury obiektu” (AutomationId/ControlID). Własne etykiety przetrwają zmianę rozmiaru okna, przełączenie monitora i aktualizację aplikacji.*

### 8.2 Skanowanie całej aplikacji (Shift + L)
Naciśnij **Shift + L**, żeby przeskanować całe aktywne okno naraz. AI znajdzie wszystkie nieoznaczone elementy i nazwie je za jednym razem. Etykiety można potem przeglądać, zmieniać i usuwać zbiorczo we wbudowanym menedżerze etykiet.

### 8.3 Eksplorator interfejsu (E)
Chcesz obsłużyć element bez ręcznego docierania do niego? Naciśnij **E**, żeby uruchomić Eksplorator interfejsu. AI przeskanuje ekran i utworzy dostępną listę wszystkich klikalnych elementów (pomijając szum systemowy w rodzaju paska zadań). Wybierz pozycję z listy, a dodatek od razu ją kliknie.

## 9. Asystent głosowy

Asystent głosowy zamienia Vision Assistant Pro w interaktywnego pomocnika działającego w czasie rzeczywistym.
*(Uwaga: funkcja dostępna wyłącznie w Google Gemini i w niestandardowych dostawcach zgodnych z Gemini).*

- **Uruchomienie:** naciśnij **Control + L** w warstwie poleceń, żeby otworzyć okno asystenta głosowego.
- **Rozmowa w czasie rzeczywistym:** mów swobodnie do mikrofonu. AI jednocześnie słucha i patrzy na aktywny ekran. Można pytać na przykład „Na co teraz patrzę?” albo „Przeczytaj mi trzeci akapit”.
- **Naciśnij i mów:** włącz opcję **Naciśnij i mów** w zakładce ustawień asystenta głosowego (albo przełącz ją bezpośrednio w oknie asystenta), a potem przytrzymuj przypisany klawisz, żeby mówić, i zwalniaj go po zakończeniu. Mikrofon pozostaje wyciszony, dopóki nie naciśniesz klawisza. Przydaje się w głośnym otoczeniu.
- **Obraz z kamery:** zaznacz **Użyj kamery** w oknie asystenta głosowego, żeby wysyłać do AI obraz z kamery zamiast ekranu, i pytaj o przedmioty, wydrukowane dokumenty albo otoczenie. Jeśli ffmpeg nie jest jeszcze zainstalowany, zaznaczenie pola pobierze go jednorazowo, za zgodą. Opcja jest niedostępna, gdy nie wykryto kamery albo ustawienia prywatności Windows blokują do niej dostęp.
- **Dostosowanie:** w oknie można zmienić styl głosu AI (na przykład profesjonalny, przyjazny, energiczny) oraz **głębię myślenia**, czyli to, jak dokładnie AI rozważa odpowiedź.

## 10. Polecenia niestandardowe i zmienne

Poleceniami zarządza się w **Ustawienia > Polecenia > Zarządzaj poleceniami...**.

### Skróty poleceń niestandardowych
Nadaj dowolnemu poleceniu niestandardowemu własny skrót klawiszowy bezpośrednio w menedżerze poleceń i uruchamiaj je natychmiast z bieżącym zaznaczeniem lub kontekstem:
- **Pojedynczy klawisz** (na przykład `1`, `p` albo `F3`): działa w warstwie poleceń, a także globalnie jako `NVDA + Shift + klawisz`.
- **Kombinacja klawiszy** (na przykład `Control + Shift + 1`, `Alt + P` albo `Insert + 1`): działa globalnie, bez warstwy poleceń.

### Obsługiwane zmienne
- `[selection]`: zaznaczony tekst.
- `[clipboard]`: zawartość schowka.
- `[clipboard_image]`: obraz w schowku.
- `[screen_obj]`: zrzut obiektu nawigatora.
- `[screen_fg_obj]`: zrzut aktywnego okna pierwszoplanowego.
- `[screen_full]`: zrzut całego ekranu.
- `[file_ocr]`: wybór obrazu albo pliku PDF do wyodrębnienia tekstu.
- `[file_read]`: wybór dokumentu do odczytu (TXT, kod, PDF).
- `[file_audio]`: wybór pliku dźwiękowego do analizy (MP3, WAV, OGG).
- `{target_lang}`: bieżący język docelowy.
- `{source_lang}`: bieżący język źródłowy.
- `{response_lang}`: bieżący język odpowiedzi AI.
- `{swap_target}`: język zapasowy przy tłumaczeniu z zamianą.
- `{swap_instruction}`: blok instrukcji tłumaczenia z zamianą.

## 11. Zastosowania w praktyce (której funkcji użyć?)

Vision Assistant Pro ma dużo narzędzi. Poniżej typowe sytuacje, które pomogą wybrać właściwe:

- **Sytuacja: chcesz zrozumieć układ skomplikowanego okna albo niedostępnej aplikacji.**
  *Rozwiązanie:* naciśnij **O** (opis całego ekranu). AI przeanalizuje ekran i opisze, gdzie dokładnie znajdują się elementy, teksty i przyciski.

- **Sytuacja: na stronie jest obraz albo w dokumencie nieoznaczona grafika.**
  *Rozwiązanie:* ustaw obiekt nawigatora na grafice i naciśnij **V** (opis obiektu). AI opisze, co konkretnie ten obraz przedstawia.

- **Sytuacja: chcesz obejrzeć film z audiodeskrypcją.**
  *Rozwiązanie:* naciśnij **Shift + V** na filmie i wybierz **„Generuj audiodeskrypcję (plik SRT)”**. Po zakończeniu kliknij **„Generuj zsynchronizowaną narrację (MP3)”** i wybierz **„Rozszerzona AD”**. Dodatek utworzy ścieżkę, która zatrzymuje dialog filmu na czas opisu scen.

- **Sytuacja: aplikacja jest pełna „nieoznaczonych przycisków”.**
  *Rozwiązanie:* naciśnij **L**, żeby trwale nazwać konkretny przycisk przy pomocy AI. Albo **Shift + L**, żeby przeskanować i nazwać całe okno naraz. Jeśli chcesz tylko szybko coś kliknąć, naciśnij **E** (Eksplorator interfejsu) po listę wszystkich klikalnych elementów.

- **Sytuacja: musisz przejść przez niedostępną CAPTCHA.**
  *Rozwiązanie:* naciśnij **C** (rozwiązywanie CAPTCHA). To **ten sam skrót niezależnie od rodzaju zagadki**. Przy kodzie do przepisania AI odczyta znaki i wpisze je w pole. Przy zagadce obrazkowej w rodzaju „zaznacz wszystkie sygnalizatory” rozpozna obrazki i sam poklika, co trzeba; usłyszysz wtedy, że wszedł w tryb rozwiązywania, bo to trwa dłużej.

- **Sytuacja: chcesz przeczytać długi, pięćdziesięciostronicowy dokument PDF.**
  *Rozwiązanie:* naciśnij **D** (czytnik dokumentów), ustaw dostawcę na Google Gemini i podaj zakres stron `1-50`. Dodatek dokładnie wyodrębni tekst w tle.

- **Sytuacja: oglądasz bezgłośny poradnik wideo albo animację.**
  *Rozwiązanie:* naciśnij **Control + V**, żeby zacząć nagrywanie ekranu. Pozwól poradnikowi się odtworzyć i naciśnij **Control + V** ponownie. AI wyjaśni dokładnie, co zostało pokazane.

- **Sytuacja: pojawia się nieoczekiwany błąd, nie działa połączenie z API albo chcesz zdiagnozować własny serwer lokalny.**
  *Rozwiązanie:* przejdź do **Ustawienia > Zaawansowane**, zaznacz **„Włącz osobny plik dziennika”** i ustaw **poziom szczegółowości** na **„Diagnostyka”**. Powtórz czynność, a potem kliknij **„Otwórz plik dziennika”**, żeby obejrzeć szczegóły techniczne albo dołączyć `vision_assistant.log` do zgłoszenia.

***
**Uwaga:** wszystkie funkcje AI wymagają aktywnego połączenia z internetem. Dokumenty wielostronicowe są przetwarzane automatycznie.

## 12. Wsparcie i społeczność

Bądź na bieżąco z nowościami, funkcjami i wydaniami:
- **Kanał na Telegramie:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** zgłoszenia błędów i propozycje funkcji.

### Zgłaszanie błędów i dzienniki
Otwierając zgłoszenie na GitHubie albo prosząc o pomoc, podaj aktywnego dostawcę AI, model i wersję NVDA. Jeśli masz problemy z połączeniem albo nieoczekiwane awarie, włącz osobny plik dziennika w **Ustawienia > Zaawansowane**, powtórz sytuację i dołącz plik `vision_assistant.log`. To przyspieszy rozwiązanie problemu.

## 13. Patroni projektu

Serdecznie dziękujemy osobom ze społeczności, które wspierają rozwój i utrzymanie tego projektu swoim wkładem finansowym:

*   **@Alyabani94**
*   **Ali Alamri**
*   **Ilya**
*   **leonardo0216**
*   **Sergei Fleytin**
*   **Arne Siebert**
*   **Schalkefan**
*   **[avalai.org](https://avalai.org)**

*Jeśli chcesz wesprzeć projekt finansowo i zobaczyć tutaj swoje imię, opcję **Wsparcie** znajdziesz w menu Narzędzia NVDA (podmenu Vision Assistant) albo podczas konfiguracji po instalacji.*

---
## Zmiany w wersji 2026.10.01

*   **Słownik postaci i seriale**: okno analizy wideo ma teraz **słownik postaci**. Można dodawać, edytować, importować i porządkować imiona postaci, ich wygląd i role osobno dla każdego serialu. AI sama dopasowuje rozpoznane postacie do słownika i dopisuje nowe z każdym kolejnym analizowanym odcinkiem. Własne notatki zawsze mają pierwszeństwo przed zmianami wprowadzanymi przez AI, a opisy wyglądu pozostają aktualne między odcinkami. Słownik jest zapisywany dla serialu i używany przy każdym wideo z tego serialu. Na liście postaci **F2** edytuje zaznaczoną postać, a **Delete** ją usuwa.
*   **48-godzinna pamięć podręczna plików wideo**: wideo wysłane do Gemini jest teraz pamiętane przez 48 godzin. Można ponownie wygenerować plik SRT albo MP3 dla tego samego wideo bez ponownego wysyłania, nawet po restarcie NVDA. Pamięć podręczna jest powiązana z kluczem API i unieważnia się sama, gdy klucz się zmieni.
*   **Wykrywanie ciszy przez AI (Silero VAD)**: rozszerzona AD korzysta teraz z sieci neuronowej Silero VAD, która dokładnie wykrywa ciszę i odróżnia naturalne pauzy w dialogu od muzyki i szumu tła. Model pobiera się automatycznie przy pierwszym użyciu (za zgodą), tak samo jak ffmpeg i eSpeak.
*   **Opis postaci tylko przy pierwszym pojawieniu się**: AI opisuje wygląd każdej postaci tylko raz, gdy pojawia się w wideo po raz pierwszy. Później podaje już samo imię, więc opisy nie powtarzają się w kolejnych fragmentach, a narracja zostaje świeża i naturalna.
*   **Jeden folder na dane**: wszystkie pliki danych dodatku (historia, seriale, etykiety, postęp OCR, pamięć podręczna i dzienniki) zostały przeniesione do jednego folderu `VisionAssistant` w katalogu konfiguracji NVDA. Wszystko jest w jednym miejscu, a ręczna kopia zapasowa nie wymaga szukania.
*   **Wygodniejszy zapis wideo**: przy zapisie plików SRT lub MP3 okno zapisu otwiera się domyślnie w folderze wideo źródłowego, niezależnie od tego, czy wideo otwarto przez okno wyboru pliku, czy skrótem Shift+V z Eksploratora.
*   **Usuwanie dokumentów z zapamiętanym tekstem lub bez niego**: okno historii (`Control + H`) daje teraz dwa sposoby usunięcia dokumentu. Po naciśnięciu Delete można wybrać **Usuń tylko z historii** albo **Usuń z historii razem z zapamiętanym tekstem**. Druga opcja kasuje zapamiętany tekst OCR tego dokumentu, więc przy następnym otwarciu zostanie on zeskanowany od nowa. To przydaje się po nieudanym skanie. Pole **Nie pytaj ponownie** zapamiętuje wybór na przyszłość. Dane do wznowienia przerwanych operacji nigdy nie są ruszane.
*   **Pamięć podręczna OCR w czytniku dokumentów osobna dla każdego silnika i uzupełniana**: zapamiętany tekst OCR jest teraz przechowywany osobno dla każdego silnika OCR, więc po zmianie silnika dokument zawsze skanuje się nowym silnikiem, zamiast odtwarzać stary wynik. Przy ponownym otwarciu dokumentu znów pojawia się okno zakresu stron (z ostatnim wyborem). Zeskanowane już strony są używane od razu, a skanowane są tylko brakujące. Pamięć podręczna uzupełnia się strona po stronie zamiast się nadpisywać, więc każdy przeczytany zakres zostaje na później.
*   **Obraz z kamery w asystencie głosowym**: okno asystenta głosowego ma teraz pole **Użyj kamery**, które wysyła do AI obraz z kamery zamiast ekranu. Przydaje się przy pytaniach o przedmioty, dokumenty albo otoczenie. Jeśli ffmpeg nie jest jeszcze zainstalowany, zaznaczenie pola go pobiera (jednorazowo, za zgodą). Opcja jest niedostępna, gdy nie wykryto kamery albo ustawienia prywatności Windows blokują do niej dostęp. Wtedy obok jest przycisk otwierający ustawienia prywatności kamery. Jeśli kamera jest włączona, ale nie daje obrazu, problem trafia do dziennika NVDA, zamiast po cichu przełączać się z powrotem na ekran.
*   **Poprawki błędów i stabilności**: naprawiono zawieszanie się generowania MP3 po zamknięciu okna postępu w trakcie pracy, usunięto wyścig przy zapisie słownika postaci, dodano właściwe zgłaszanie błędów kodowania MP3 i poprawiono pętlę oczekiwania czytnika dokumentów, żeby respektowała anulowanie.

## Zmiany w wersji 2026.09.01

*   **Historia (Control + H)**: warstwa poleceń zawiera teraz okno **Historii** (`Control + H`), które wypisuje wcześniejsze czaty i dokumenty, z filtrami Wszystko, Czaty i Dokumenty. Możesz otworzyć ponownie dowolny czat wraz z całą rozmową — załączone pliki dołączają się automatycznie — albo wrócić do dokumentu i czytać dalej. Naciśnij **Delete** na wybranej pozycji, aby ją usunąć, lub wyczyść wszystko naraz.
*   **Ostatnie dokumenty w czytniku**: naciśnięcie **D** w warstwie poleceń pokazuje teraz najpierw ostatnio czytane dokumenty. Wybierz jeden, aby kontynuować od strony, na której skończyłeś — nawet gdy OCR już się zakończył — albo naciśnij **Otwórz plik...** (`Ctrl + O`), aby przeglądać jak dotąd.
*   **Naciśnij i mów w asystencie na żywo**: przejmij pełną kontrolę nad rozmowami na żywo. Włącz opcję **Naciśnij i mów** w nowej karcie ustawień asystenta na żywo i przypisz dowolny klawisz — nawet sam modyfikator, taki jak `lewy Ctrl`. Przytrzymaj klawisz, aby mówić, i zwolnij go po zakończeniu; każdemu naciśnięciu i zwolnieniu towarzyszy krótki sygnał. Odpowiedni przełącznik pojawia się też w samym oknie asystenta, więc możesz przechodzić między trybem naciśnij i mów a otwartym mikrofonem bez opuszczania rozmowy.
*   **Gemini 2.5 Flash z natywnym dźwiękiem**: asystent na żywo obsługuje teraz model natywnego dźwięku Gemini 2.5 Flash (`gemini-2.5-flash-native-audio-preview-12-2025`), zapewniający naturalne rozmowy głosowe o małym opóźnieniu. Możesz go wybrać w **Ustawieniach → Zaawansowane kierowanie modeli → Model asystenta na żywo (tylko Gemini)** albo zostawić \"Auto\", aby korzystać z modelu zalecanego.
*   **Kopia zapasowa i przywracanie ustawień**: w karcie **Zaawansowane** pojawił się rozbudowany system kopii zapasowych. Możesz zapisać wszystkie ustawienia dodatku — w tym klucze API, modele, polecenia niestandardowe i preferencje — do jednego pliku JSON, a potem odtworzyć je w dowolnej chwili, na dowolnym komputerze albo po ponownej instalacji NVDA. Przy tworzeniu kopii wybierasz jej zakres: **Wszystko** (ustawienia, własne etykiety, postęp OCR i historia) albo **Tylko ustawienia**.
*   **Bezpośrednie czytanie plików tekstowych i HTML**: czytnik dokumentów otwiera teraz wprost pliki tekstowe (`.txt`) oraz HTML (`.html`, `.htm`). Automatycznie rozpoznaje kodowanie pliku, usuwa skrypty i zbędne formatowanie oraz dzieli treść na czytelne strony — potrafi też ponownie wczytać własne wyeksportowane pliki z zachowaniem podziału na strony — więc przeczytasz je od razu, bez OCR i bez przetwarzania przez AI.
*   **Gemini Live jako synteza mowy w czytniku**: przycisk \"Generuj dźwięk\" obsługuje teraz Gemini Live, czyli strumieniową syntezę mowy o wysokiej jakości i naturalnym tempie. Gdy aktywnym dostawcą jest Gemini, możesz wybrać w czytniku między standardową syntezą a Gemini Live, a wybór zostanie zapamiętany.
*   **Skróty klawiszowe poleceń niestandardowych**: każdemu własnemu poleceniu możesz teraz przypisać skrót klawiszowy bezpośrednio w menedżerze poleceń. Nadaj poleceniu własny klawisz lub kombinację, aby uruchamiać je natychmiast, automatycznie przechwytując bieżące zaznaczenie lub kontekst, bez żadnych dodatkowych kroków.
*   **Nawigacja po wiadomościach czatu**: przejrzyj każdą rozmowę bez użycia rąk. W dowolnym oknie czatu (czat bezpośredni, czat z dokumentem, dopracowywanie i inne) naciśnij `Alt + strzałka w dół`, aby usłyszeć następną wiadomość, a `Alt + strzałka w górę`, aby usłyszeć poprzednią — z wyraźnymi przedrostkami \"Ty\" i \"AI\" oraz zapowiedzią granic \"Pierwsza wiadomość\" i \"Ostatnia wiadomość\".
*   **Kopiowanie wiadomości czatu (Alt + C)**: przeglądając rozmowę klawiszami `Alt + strzałki`, naciśnij `Alt + C`, aby skopiować bieżącą wiadomość do schowka — z uwzględnieniem ustawienia czyszczenia znaczników Markdown — wraz z potwierdzeniem głosowym.
*   **Instrukcja czatu bezpośredniego**: czat bezpośredni (`Shift+C`) ma teraz własną, edytowalną instrukcję systemową — \"Instrukcja czatu bezpośredniego\" — która ustala osobowość asystenta i język odpowiedzi dla każdej rozmowy. Możesz ją zmienić w karcie poleceń domyślnych w menedżerze poleceń.
*   **Przechodzenie między stronami kursorem w czytniku**: czytanie dokumentów wielostronicowych jest płynniejsze. Gdy w podglądzie dokumentu kursor dojdzie do ostatniego wiersza strony i naciśniesz `strzałkę w dół`, czytnik automatycznie przejdzie do następnej strony. Naciśnięcie `strzałki w górę` na początku strony wraca do poprzedniej — koniec z ręcznym przełączaniem stron podczas czytania.
*   **Nowe przełączniki w szybkich ustawieniach**: kopiowanie odpowiedzi AI do schowka, wyjście bezpośrednie (bez okna czatu), czyszczenie znaczników Markdown w czacie oraz inteligentna zamiana dają się teraz włączać i wyłączać natychmiast z szybkich ustawień w warstwie poleceń.
*   **Karta ustawień asystenta na żywo**: asystent na żywo ma teraz własną kartę ustawień. Opcja \"Asystent na żywo: wyjście bezpośrednie (bez okna)\" przeniosła się tu z karty połączenia, a sama karta pojawia się tylko wtedy, gdy aktywnym dostawcą jest Google Gemini lub zgodny z Gemini dostawca niestandardowy.

## Zmiany w wersji 2026.08.06

*   **Etykietowanie w Eksploratorze interfejsu**: teraz można dodawać etykiety wprost do znalezionych elementów w Eksploratorze interfejsu. Doszedł przycisk „Dodaj etykietę”, a okno zostaje otwarte i utrzymuje fokus, więc kilka obiektów da się opisać jeden po drugim bez przerywania pracy.
*   **Rozbudowana warstwa szybkich ustawień**: warstwa Vision Assistant (`Insert+Shift+V`) jest teraz trwała i w pełni interaktywna. Strzałkami góra i dół przechodzi się między szybkimi ustawieniami (dostawca, model, język odpowiedzi AI, model TTS), a strzałkami lewo i prawo od razu zmienia ich wartości, z krótkim komunikatem głosowym. Wybory działają natychmiast (łącznie z automatycznym włączeniem osobnego modelu dla zadania, jeśli jest potrzebny), a warstwa pozostaje aktywna przez cały czas konfiguracji.
*   **Czat (`Shift+C`)**: nowe polecenie w warstwie. `Shift+C` otwiera okno czatu — czysty interfejs tekstowy do rozmowy z AI, bez potrzeby zaczynania od obrazu czy dokumentu.
*   **Poprawne przywoływanie historii rozmowy**: naprawiony poważny błąd, przez który naciśnięcie `Spacji` w celu przywołania ostatniego wyniku gubiło dalszą historię rozmowy. Dodatek śledzi teraz całą rozmowę globalnie. Po zamknięciu okna i naciśnięciu `Spacji` wraca pełna historia wymiany. Działa dla czatu, analizy obrazu, rozmowy o dokumencie i tłumaczenia.
*   **Opisy obrazów wplecione w tekst przy OCR**: doszła opcja, która przy OCR dokumentu wplata opis obrazu dokładnie tam, gdzie w dokumencie znajduje się ten obraz. Można ją przełączyć w ustawieniach OCR dodatku, w opcjach czytnika dokumentów przed wyodrębnieniem oraz na bieżąco w warstwie szybkich ustawień.
*   **Tłumaczenie mowy (`Control+T`)**: nowa funkcja. Dyktujesz, a AI od razu tłumaczy wypowiedź i wpisuje ją jako tekst, zgodnie z ustawionym językiem źródłowym i docelowym.
*   **Poprawki pobierania aktualizacji**: okno pobierania aktualizacji pokazuje teraz poprawnie postęp w procentach, a błąd, przez który po anulowaniu instalacji pojawiał się fantomowy komunikat „Pobieranie aktualizacji”, został naprawiony.
*   **Poprawki pobierania eSpeak-NG**: doszedł postęp pobierania eSpeak-NG w procentach.
*   **Odporność wsadowego OCR**: naprawiony błąd we wsadowym OCR plików PDF, przez który przetwarzanie zatrzymywało się, gdy aktywny klucz API wyczerpał limit w połowie pracy. Teraz dodatek sam przełącza się na kolejny dostępny klucz i kontynuuje.
*   **Obsługa CAPTCHA obrazkowej**: doszła solidna obsługa rozwiązywania CAPTCHA z obrazu. Dodatek próbuje automatycznie rozwiązywać złożone zagadki obrazkowe w rodzaju hCaptcha i reCAPTCHA, co wyraźnie poprawia dostępność trudnych formularzy internetowych.
*   **Przebudowana transkrypcja dźwięku**: moduł transkrypcji został napisany od nowa i obsługuje teraz zarówno pliki dźwiękowe, jak i wideo. Ma trzy tryby pracy: „Transkrybuj (język oryginału)”, „Transkrybuj i przetłumacz (język docelowy)” oraz nowy „Zdubbinguj i przetłumacz (język docelowy)” — ten ostatni dostępny wyłącznie w Gemini, tworzy przetłumaczoną ścieżkę głosową oryginalnej wypowiedzi.
*   **Numery stron w czytniku dokumentów**: doszło ustawienie, które włącza i wyłącza numery stron oraz separatory w dokumentach wielostronicowych. Opcja jest w ustawieniach głównych i w warstwie szybkich ustawień. Działa zarówno przy eksporcie do pliku tekstowego i HTML, jak i w oknie „Pokaż sformatowane”, dzięki czemu połączone dokumenty czyta się bez przerw.
*   **Gemini Live TTS bez limitu dla opisów wideo**: przy tworzeniu zsynchronizowanej narracji dźwiękowej (MP3) do filmów można teraz wybrać silnik głosu „Gemini Live TTS”. Korzysta on z Gemini Live API i tworzy wysokiej jakości audiodeskrypcję bez ograniczeń długości ani liczby znaków.
*   **Modularyzacja kodu**: struktura dodatku została przebudowana z jednego pliku na architekturę wielomodułową, co ułatwia utrzymanie.
*   **Przeprojektowane ustawienia**: okno ustawień zostało w całości przebudowane na nowoczesny układ z zakładkami zamiast grup. Porządek i nawigacja są wygodniejsze, a wszystkie dotychczasowe opcje zostają.
*   **Globalny dziennik w osobnym pliku**: doszedł opcjonalny globalny dziennik pod nową zakładką ustawień „Zaawansowane”. Zapisuje zdarzenia, ruch do API i błędy ze wszystkich modułów dodatku do osobnego pliku (`vision_assistant.log`). Obsługuje poziomy szczegółowości (diagnostyka, informacje, ostrzeżenia, błędy) i automatyczne przechowywanie (od godziny do 90 dni), a plik można otworzyć lub wyczyścić wprost z ustawień. Bez wpływu na wydajność i bez zaśmiecania dziennika NVDA.
*   **Postęp wysyłania do Gemini**: doszły komunikaty o postępie w procentach przy wysyłaniu dużych plików (wideo, dźwięk, dokumenty) do Google Gemini API.

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
*   **Status czytnika dokumentów**: Naprawiono błąd, przez który ogólny status dodatku (sprawdzany przez `I`) pozostawał zatrzymany na „Rozpoczęto przetwarzanie wsadowe” podczas długiego skanowania dokumentów.
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

*   **Uniwersalna integracja lokalnej AI (Konfiguracja lokalnej AI)**: Dodano nowy przycisk **„Konfiguracja lokalnej AI”** w ustawieniach niestandardowego dostawcy. Teraz można od razu automatycznie skonfigurować lokalne silniki AI, w tym **Ollama**, **LM Studio**, **Jan.ai** i **KoboldCPP**.
*   **Ominięcie lokalnego proxy**: Przebudowano logikę połączenia z zaawansowanym mechanizmem omijania proxy. Dodatek całkowicie omija systemowe proxy Windows przy połączeniach lokalnych, dzięki czemu połączenie z lokalną AI jest stabilne nawet przy aktywnym VPN lub trybie TUN.
*   **Awaryjne zatrzymanie Operatora AI (Shift+A)**: Dodano wyzwalacz zatrzymania. Naciśnięcie polecenia Operatora AI (**Shift+A** w warstwie poleceń) podczas trwającej operacji autonomicznej natychmiast przerywa pętlę i ogłasza *„Operator AI zatrzymany.”*
*   **Bardzo stabilne etykietowanie AI (v2)**: Zastąpiono klucze oparte na bezwzględnych współrzędnych ekranu zaawansowanym, hybrydowym systemem **sygnatur obiektów**. Etykiety opierają się teraz na identyfikatorach programowych (UIA **AutomationId** lub Win32 **ControlID**) oraz współrzędnych względem okna, dzięki czemu są one całkowicie odporne na zmianę rozmiaru, przesuwanie, zmianę monitora czy skalowanie okna.
*   **Płynna automatyczna migracja etykiet**: Aktualizacja jest całkowicie przezroczysta. Dodatek automatycznie przeniesie starsze etykiety oparte na współrzędnych do nowego, stabilnego formatu sygnatur w tle przy pierwszym ustawieniu fokusu, bez utraty danych.

---
## Zmiany w wersji 6.0

*   **etykietowanie AI**: Teraz można trwale nadawać etykiety nienazwanym przyciskom i ikonom za pomocą AI. Naciśnij **L**, by oznaczyć bieżący obiekt nawigatora (obsługa zarówno fokusu Tab, jak i nawigacji obiektowej), lub **Shift+L**, by przeskanować i oznaczyć całą aplikację naraz.
*   **Zarządzanie etykietami**: Nowe, w pełni dostępne okno Menedżer etykiet (przez **Shift+L**, jeśli etykiety istnieją) pozwala przeglądać, zmieniać nazwy i zbiorczo usuwać etykiety.
*   **Bezpośrednia analiza pliku (z pominięciem okna dialogowego)**: Dodatek wykrywa, czy fokus znajduje się na pliku PDF lub graficznym w Eksploratorze Windows. Naciśnięcie **F (Akcja na pliku)** lub **D (Czytnik dokumentów)** na zaznaczonym pliku natychmiast go przetworzy, pomijając standardowe okno „Otwórz”.

## Zmiany w wersji 5.6

* **Dodano silnik OCR „Wyodrębnij tekst (offline)”:** Teraz można wyodrębniać tekst bezpośrednio z plików PDF z warstwą tekstową, bez zużywania kredytów AI, co daje znaczne przyspieszenie i większą prywatność dokumentów tekstowych.
* **Lepsza dokładność Eksploratora interfejsu:** Ulepszono prompt eksploratora, by trafniej rozpoznawał typy elementów (np. element listy) i precyzyjnie raportował stany takie jak „(zaznaczony)”, „(wybrany)” albo „(rozwinięty)”, pomijając jednocześnie komponenty systemu Windows jak pasek zadań i zegar.
* **Przypomnienie o konfiguracji po instalacji:** Dodano powiadomienie po instalacji, które prowadzi do menu ustawień, by skonfigurować klucze API i preferencje.

## Zmiany w wersji 5.5.2

* **Naprawa błędu wpisywania w Operatorze AI:** Rozwiązano błąd, w którym litera „v” była wpisywana zamiast wklejania tekstu na niektórych systemach. Poprawka usuwa konflikty czasowe występujące przy dużym obciążeniu systemu.
* **Większa stabilność:** Dodano solidną obsługę błędów dla operacji na schowku, aby zapobiec awariom dodatku, gdy schowek systemowy jest tymczasowo zablokowany przez inne aplikacje.
* **Optymalizacja czasu reakcji:** Dostosowano wewnętrzne opóźnienia zdarzeń klawiatury w celu zapewnienia większej niezawodności na różnych prędkościach systemowych i lepszej zgodności z zewnętrznymi menedżerami schowka.

## Zmiany w wersji 5.5 (Aktualizacja automatyzacji)

* **Operator AI (Sterowanie autonomiczne - Shift+A):** To perła w koronie wersji 5.5. Vision Assistant Pro przeszedł z biernego asystenta w Twojego osobistego **Operatora AI**. Nie tylko opisuje ekran, lecz przejmuje sterowanie.
    * *Jak to działa:* Możesz teraz wydawać AI instrukcje słowne, aby obsługiwała Twój komputer. Na przykład w całkowicie niedostępnej aplikacji, gdzie czytnik ekranu milczy, możesz nacisnąć **Shift+A** i wpisać: *„Kliknij przycisk Ustawienia”* lub *„Znajdź pole wyszukiwania, wpisz 'Najnowsze wiadomości' i naciśnij enter.”* AI wizualnie identyfikuje elementy, przesuwa kursor i wykonuje zadanie za Ciebie.
    * *Uwaga o wydajności:* Funkcja jest zoptymalizowana dla **Gemini 3.0 Flash (Preview)**, dostarczając niezwykle szybkich i inteligentnych odpowiedzi, które poradzą sobie nawet z najbardziej złożonymi układami interfejsu.
    * **⚠️ Ostrzeżenie o zużyciu API:** Ponieważ Operator AI musi „widzieć” dokładnie to, co się dzieje, aby działać precyzyjnie, wysyła zrzut ekranu w wysokiej rozdzielczości na każdym kroku. Częste używanie znacznie szybciej zużyje Twój limit API niż standardowe zadania tekstowe.
* **Wizualny Eksplorator interfejsu (E):** Zmęczony nawigacją po „nieoznaczonych przyciskach”? Naciśnij **E**, aby uruchomić Eksplorator interfejsu. AI przeskanuje całe okno i wygeneruje listę każdego klikalnego elementu, jaki widzi: ikon, grafik i menu. Wybierz element z listy, a Operator AI kliknie go za Ciebie. To jak „warstwa dostępności” nałożona na dowolną aplikację.
* **Akcja na pliku zależna od kontekstu (F):** Klawisz „F” został gruntownie przebudowany. Nie zakłada już, że chcesz tylko OCR. Gdy wybierzesz pojedynczy obraz, zapyta o Twoją intencję: możesz wybrać **Szczegółowy opis wizualny**, aby zrozumieć scenę, lub **Strukturalne wyodrębnienie tekstu (OCR)** do czytania. Menu dostosowuje się dynamicznie do typu pliku i aktywnego silnika AI.
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
* **Zbiorczy podgląd sformatowany:** Funkcja „Podgląd sformatowany” w czytniku dokumentów wyświetla teraz wszystkie przetworzone strony w jednym uporządkowanym oknie z nagłówkami stron.
* **Szybszy OCR:** Dla dokumentów jednostronicowych pomijany jest wybór zakresu stron, co przyspiesza proces rozpoznawania.
* **Stabilność API:** Zmieniono metodę uwierzytelniania na opartą o nagłówki HTTP, eliminując błędy „Wszystkie klucze API zawiodły” powodowane przez konflikty rotacji kluczy.
* **Poprawki błędów:** Naprawiono kilka potencjalnych awarii, w tym problem przy zamykaniu dodatku oraz błąd fokusu w oknie czatu.

## Zmiany w wersji 4.0.1
* **Czytnik dokumentów:** Nowa przeglądarka PDF i obrazów z wyborem zakresu stron, przetwarzaniem w tle i nawigacją Ctrl+PageUp/Down.
* **Podmenu Narzędzia:** Dodano podmenu „Vision Assistant” w menu Narzędzia NVDA, umożliwiające szybki dostęp do głównych funkcji, ustawień i dokumentacji.
* **Konfiguracja:** Teraz można wybrać preferowany silnik OCR i głos TTS bezpośrednio w panelu ustawień.
* **Wiele kluczy API:** Dodano obsługę wielu kluczy API Gemini. Klucze można podać po jednym w wierszu lub rozdzielone przecinkami.
* **Alternatywny silnik OCR:** Dodano nowy silnik OCR, zapewniający niezawodne rozpoznawanie tekstu nawet po przekroczeniu limitów API Gemini.
* **Rotacja kluczy API:** Automatyczne przełączanie na najszybszy działający klucz API, aby obejść limity.
* **Eksport audio:** Możliwość generowania i zapisywania plików audio w formatach MP3 (128 kbps) i WAV bezpośrednio z czytnika.
* **Instagram Stories:** Dodano możliwość opisu i analizy Instagram Stories za pomocą adresów URL.
* **TikTok:** Dodano obsługę filmów TikTok, umożliwiając opis wizualny i transkrypcję audio.
* **Okno aktualizacji:** Nowy dostępny interfejs z polem tekstowym do przejrzenia zmian przed instalacją.
* **Ujednolicenie interfejsu:** Ustandaryzowano okna dialogowe plików w całym dodatku i rozszerzono polecenie „L” o raportowanie postępu w czasie rzeczywistym.

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
* **Podgląd sformatowany:** Dodano przycisk „Podgląd sformatowany” w oknach czatu, umożliwiający wyświetlenie rozmowy z prawidłowym formatowaniem (nagłówki, pogrubienie, kod) w standardowym oknie przeglądarki.
* **Ustawienie Markdown:** Dodano opcję „Czyść Markdown w czacie” w ustawieniach. Odznaczenie pozwala widzieć surową składnię Markdown (np. `**`, `#`) w oknie czatu.
* **Zarządzanie oknami:** Naprawiono problem z wielokrotnym otwieraniem okien „Poprawianie tekstu” lub czatu.
* **Usprawnienia interfejsu:** Ujednolicono tytuły okien dialogowych plików na „Otwórz” i usunięto zbędne komunikaty głosowe (np. „Otwieranie menu...”).

## Zmiany w wersji 2.8
* Dodano tłumaczenie na włoski.
* **Raport stanu:** Dodano polecenie (NVDA+Control+Shift+I) odczytujące bieżący stan dodatku (np. „Przesyłanie...”, „Analizowanie...”).
* **Eksport HTML:** Przycisk „Zapisz treść” w oknach wyników zapisuje teraz dane jako sformatowany plik HTML, zachowując style takie jak nagłówki i pogrubienia.
* **Interfejs ustawień:** Poprawiono układ panelu ustawień z dostępnym grupowaniem.
* **Nowe modele:** Dodano obsługę gemini-flash-latest i gemini-flash-lite-latest.
* **Języki:** Dodano nepalski do obsługiwanych języków.
* **Poprawianie tekstu:** Naprawiono błąd, przez który polecenia „Poprawianie tekstu” nie działały, gdy język interfejsu NVDA nie był angielski.
* **Dyktowanie:** Poprawiono wykrywanie ciszy, aby zapobiec błędnemu rozpoznawaniu tekstu przy braku mowy.
* **Ustawienia aktualizacji:** Opcja „Sprawdzaj aktualizacje przy uruchomieniu” jest teraz domyślnie wyłączona, zgodnie z polityką Add-on Store.
* Porządki w kodzie.

## Zmiany w wersji 2.7
* Przeniesiono strukturę projektu na oficjalny szablon dodatków NV Access, zapewniając zgodność ze standardami.
* Dodano automatyczne ponawianie prób przy błędach HTTP 429 (limit zapytań), poprawiając niezawodność w okresach dużego ruchu.
* Zoptymalizowano polecenia tłumaczenia dla wyższej dokładności i lepszej obsługi logiki „Zamień języki”.
* Zaktualizowano tłumaczenie rosyjskie.

## Zmiany w wersji 2.6
* Dodano tłumaczenie na rosyjski (podziękowania dla nvda-ru).
* Zaktualizowano komunikaty o błędach, aby lepiej informowały o problemach z łącznością.
* Zmieniono domyślny język docelowy na angielski.

## Zmiany w wersji 2.5
* Dodano polecenie OCR pliku (NVDA+Control+Shift+F).
* Dodano przycisk „Zapisz czat” w oknach wyników.
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
* Dodano kategorię „Vision Assistant” w oknie Zdarzenia wejścia NVDA.
* Naprawiono awarie COMError w niektórych aplikacjach, takich jak Firefox i Word.
* Dodano mechanizm automatycznego ponawiania prób przy błędach serwera.

## Zmiany w wersji 1.0
* Pierwsze wydanie.
