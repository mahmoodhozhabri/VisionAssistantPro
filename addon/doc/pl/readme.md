# Vision Assistant Pro - Dokumentacja

**Vision Assistant Pro** to zaawansowany, wielomodalny asystent AI dla NVDA. Wykorzystuje modele Gemini od Google, zapewniając inteligentne odczytywanie ekranu, tłumaczenie, głosowe dyktowanie oraz analizę dokumentów.

*Ten dodatek został udostępniony społeczności z okazji Międzynarodowego Dnia Osób z Niepełnosprawnościami.*

## 1. Instalacja i konfiguracja

Przejdź do **Menu NVDA > Ustawienia > Opcje > Vision Assistant Pro**.

- **Klucz API:** Wymagany. Można wprowadzić wiele kluczy (oddzielając je przecinkami lub nowym wierszem). Asystent będzie automatycznie przełączać się między nimi po wyczerpaniu limitu.
- **Model AI:** Wybierz między modelami Flash (najszybszy/darmowy), Lite lub Pro (wysoka inteligencja).
- **URL proxy:** Opcjonalnie. Użyj, jeśli Google jest zablokowany w Twoim regionie. Musi to być adres internetowy pełniący funkcję pomostu do API Gemini.
- **Silnik OCR:** Wybierz między Chrome (szybki) dla szybkich wyników lub Gemini (sformatowany) dla lepszego zachowania układu strony i rozpoznawania tabel.
- **Głos TTS:** Wybierz preferowany styl głosu do generowania plików audio ze stron dokumentów.
- **Inteligentna zamiana (Smart Swap):** Automatycznie zamienia języki miejscami, jeśli tekst źródłowy odpowiada językowi docelowemu.
- **Bezpośredni wynik (Direct Output):** Pomija okno czatu i natychmiast odczytuje odpowiedź AI przez mowę.
- **Integracja ze schowkiem (Clipboard Integration):** Automatycznie kopiuje odpowiedź AI do schowka.

## 2. Warstwa poleceń i skróty klawiszowe

Aby zapobiec konfliktom klawiszy, ten dodatek wykorzystuje warstwę poleceń (Command Layer).

1. Naciśnij **NVDA + Shift + V** (klawisz główny), aby aktywować warstwę (usłyszysz sygnał dźwiękowy).
2. Zwolnij klawisze, a następnie naciśnij jeden z poniższych klawiszy:

| Klawisz | Funkcja | Opis |
|---|---|---|
| **T** | Inteligentny tłumacz | Tłumaczy tekst pod kursorem nawigatora lub zaznaczenie. |
| **Shift + T** | Tłumaczenie ze schowka | Tłumaczy zawartość znajdującą się w schowku. |
| **R** | Poprawianie tekstu | Podsumuj, popraw gramatykę, wyjaśnij lub uruchom polecenia niestandardowe. |
| **V** | Rozpoznawanie obiektu | Opisuje bieżący obiekt nawigatora. |
| **O** | Rozpoznawanie całego ekranu | Analizuje cały układ i zawartość ekranu. |
| **Shift + V** | Analiza wideo online | Analizuje wideo z YouTube, Instagrama lub Twittera (X) na podstawie URL. |
| **D** | Czytnik dokumentów | Zaawansowany czytnik PDF i obrazów z wyborem zakresu stron. |
| **F** | OCR pliku | Bezpośrednie rozpoznawanie tekstu z wybranych plików graficznych, PDF lub TIFF. |
| **A** | Transkrypcja audio | Transkrybuje pliki MP3, WAV lub OGG na tekst. |
| **C** | Rozwiązywanie CAPTCHA | Przechwytuje i rozwiązuje CAPTCHA na ekranie lub obiekcie nawigatora. |
| **S** | Inteligentne dyktowanie | Zamienia mowę na tekst. Naciśnij, aby rozpocząć nagrywanie; naciśnij ponownie, aby zatrzymać i wpisać. |
| **L** | Raport stanu | Odczytuje bieżący postęp (np. „Skanowanie...", „Bezczynny"). |
| **U** | Sprawdzanie aktualizacji | Ręcznie sprawdza GitHub pod kątem najnowszej wersji dodatku. |
| **H** | Pomoc dotycząca poleceń | Wyświetla listę wszystkich dostępnych skrótów w warstwie poleceń. |

### 2.1. Skróty klawiszowe czytnika dokumentów (wewnątrz okna podglądu)

Po otwarciu dokumentu poleceniem **D**:

- **Ctrl + PageDown:** Przejdź do następnej strony (odczytuje numer strony).
- **Ctrl + PageUp:** Przejdź do poprzedniej strony (odczytuje numer strony).
- **Alt + A:** Otwórz okno czatu, aby zadawać pytania dotyczące dokumentu.
- **Alt + R:** Wymuś ponowne skanowanie bieżącej strony lub wszystkich stron silnikiem Gemini.
- **Alt + G:** Wygeneruj i zapisz wysokiej jakości plik audio (WAV) z zawartości.
- **Alt + S / Ctrl + S:** Zapisz wyodrębniony tekst jako plik TXT lub HTML.

## 3. Prompty niestandardowe i zmienne

Otwórz **Ustawienia > prompty > Zarządzaj promptami...**, aby skonfigurować polecenia systemowe i niestandardowe.

- **Zakładka „prompty domyślne":** edycja wbudowanych promptów. Można zresetować jedno polecenie lub przywrócić wszystkie wartości domyślne.
- **Zakładka „prompty niestandardowe":** dodawanie, edytowanie, usuwanie i zmiana kolejności poleceń użytkownika.
- **Przycisk „Przewodnik po zmiennych":** otwiera okno pomocy ze wszystkimi obsługiwanymi zmiennymi i typami danych wejściowych.

### Dostępne zmienne

| Zmienna | Opis | Typ danych |
|---|---|---|
| `[selection]` | Aktualnie zaznaczony tekst | Tekst |
| `[clipboard]` | Zawartość schowka | Tekst |
| `[screen_obj]` | Zrzut ekranu obiektu nawigatora | Obraz |
| `[screen_full]` | Zrzut całego ekranu | Obraz |
| `[file_ocr]` | Wybierz obraz/PDF/TIFF do wyodrębnienia tekstu | Obraz, PDF, TIFF |
| `[file_read]` | Wybierz dokument do odczytania | TXT, kod, PDF |
| `[file_audio]` | Wybierz plik audio do analizy | MP3, WAV, OGG |

### Przykłady poleceń niestandardowych

- **Szybkie OCR:** `Moje OCR:[file_ocr]`
- **Tłumaczenie obrazu:** `Tłumacz obraz:Wyodrębnij tekst z tego obrazu i przetłumacz na polski. [file_ocr]`
- **Analiza audio:** `Podsumowanie audio:Przesłuchaj to nagranie i podsumuj główne wątki. [file_audio]`
- **Debuger kodu:** `Debuguj:Znajdź błędy w tym kodzie i je wyjaśnij: [selection]`

> **Uwaga:** Do działania wszystkich funkcji AI wymagane jest aktywne połączenie internetowe. Dokumenty wielostronicowe i pliki TIFF są przetwarzane automatycznie.

## Historia zmian

### Zmiany w wersji 4.5

- **Zaawansowany menedżer poleceń:** Wprowadzono dedykowane okno dialogowe zarządzania w ustawieniach, umożliwiające dostosowywanie domyślnych poleceń systemowych i zarządzanie poleceniami użytkownika z pełnym wsparciem dla dodawania, edytowania, zmiany kolejności i podglądu.
- **Pełna obsługa proxy:** Rozwiązano problemy z łącznością sieciową, zapewniając ścisłe stosowanie ustawień proxy skonfigurowanych przez użytkownika do wszystkich żądań API, w tym tłumaczenia, OCR i generowania mowy.
- **Automatyczna migracja danych:** Zintegrowano inteligentny system migracji, który automatycznie aktualizuje starsze konfiguracje poleceń do niezawodnego formatu JSON v2 przy pierwszym uruchomieniu, bez utraty danych.
- **Zaktualizowana zgodność (2025.1):** Ustawiono minimalną wymaganą wersję NVDA na 2025.1 ze względu na zależności bibliotek w zaawansowanych funkcjach, takich jak czytnik dokumentów, w celu zapewnienia stabilnego działania.
- **Zoptymalizowany interfejs ustawień:** Uproszczono interfejs ustawień, przenosząc zarządzanie promptami do osobnego okna dialogowego, zapewniając bardziej przejrzysty i dostępny interfejs użytkownika.
- **Przewodnik po zmiennych poleceń:** Dodano wbudowany przewodnik w oknach dialogowych poleceń, ułatwiający użytkownikom identyfikację i używanie zmiennych dynamicznych, takich jak `[selection]`, `[clipboard]` i `[screen_obj]`.

### Zmiany w wersji 4.0.3

- **Ulepszona stabilność sieci:** Dodano mechanizm automatycznego ponawiania prób w celu lepszej obsługi niestabilnych połączeń internetowych i tymczasowych błędów serwera, zapewniając bardziej niezawodne odpowiedzi AI.
- **Okno dialogowe tłumaczenia:** Wprowadzono dedykowane okno wyników tłumaczenia. Użytkownicy mogą teraz wygodnie przeglądać i czytać długie tłumaczenia wiersz po wierszu, podobnie jak wyniki OCR.
- **Zagregowany widok sformatowany:** Funkcja „Widok sformatowany" w czytniku dokumentów wyświetla teraz wszystkie przetworzone strony w jednym zorganizowanym oknie z wyraźnymi nagłówkami stron.
- **Zoptymalizowany przepływ pracy OCR:** Automatyczne pomijanie wyboru zakresu stron dla dokumentów jednostronicowych, dzięki czemu proces rozpoznawania jest szybszy i płynniejszy.
- **Ulepszona stabilność API:** Przejście na bardziej niezawodną metodę uwierzytelniania opartą na nagłówkach, eliminującą potencjalne błędy „Wszystkie klucze API zawiodły" spowodowane konfliktami rotacji kluczy.
- **Poprawki błędów:** Usunięto kilka potencjalnych awarii, w tym problem przy zamykaniu dodatku i błąd fokusu w oknie czatu.

### Zmiany w wersji 4.0.1

- **Zaawansowany czytnik dokumentów:** Nowe, zaawansowane okno podglądu dla PDF i obrazów z wyborem zakresu stron, przetwarzaniem w tle i płynną nawigacją Ctrl+PageUp/Down.
- **Nowe podmenu „Narzędzia":** Dodano dedykowane podmenu „Vision Assistant" w menu „Narzędzia" NVDA dla szybszego dostępu do głównych funkcji, ustawień i dokumentacji.
- **Elastyczna konfiguracja:** Teraz można wybrać preferowany silnik OCR i głos TTS bezpośrednio z panelu ustawień.
- **Obsługa wielu kluczy API:** Dodano obsługę wielu kluczy API Gemini. Klucze można wprowadzać po jednym w wierszu lub oddzielać przecinkami w ustawieniach.
- **Alternatywny silnik OCR:** Wprowadzono nowy silnik OCR zapewniający niezawodne rozpoznawanie tekstu nawet po wyczerpaniu limitu API Gemini.
- **Inteligentna rotacja kluczy API:** Automatyczne przełączanie na najszybszy działający klucz API i zapamiętywanie go w celu obejścia limitów.
- **Eksport dokumentu do MP3/WAV:** Zintegrowana możliwość generowania i zapisywania wysokiej jakości plików audio w formatach MP3 (128 kbps) i WAV bezpośrednio w czytniku.
- **Obsługa Instagram Stories:** Dodano możliwość opisywania i analizowania Instagram Stories za pomocą ich adresów URL.
- **Obsługa TikTok:** Wprowadzono obsługę filmów TikTok, umożliwiającą pełny opis wizualny i transkrypcję audio klipów.
- **Przeprojektowane okno aktualizacji:** Nowy, dostępny interfejs z przewijanym polem tekstowym umożliwiającym zapoznanie się ze zmianami przed instalacją.
- **Ujednolicony status i UX:** Ustandaryzowano okna dialogowe wyboru plików w dodatku i ulepszono polecenie „L" do raportowania postępu w czasie rzeczywistym.

### Zmiany w wersji 3.6.0

- **System pomocy:** Dodano polecenie pomocy (H) w warstwie poleceń, zapewniające łatwo dostępną listę wszystkich skrótów klawiszowych i ich funkcji.
- **Analiza wideo online:** Rozszerzono obsługę o filmy z Twittera (X). Poprawiono również wykrywanie adresów URL i stabilność działania.
- **Wsparcie projektu:** Dodano opcjonalne okno dialogowe darowizn dla użytkowników chcących wesprzeć przyszłe aktualizacje i ciągły rozwój projektu.

### Zmiany w wersji 3.5.0

- **Warstwa poleceń:** Wprowadzono system warstwy poleceń (domyślnie: NVDA+Shift+V) do grupowania skrótów pod jednym klawiszem głównym. Na przykład, zamiast naciskać NVDA+Control+Shift+T w celu tłumaczenia, wystarczy nacisnąć NVDA+Shift+V, a następnie T.
- **Analiza wideo online:** Dodano nową funkcję analizy filmów z YouTube i Instagrama bezpośrednio przez podanie adresu URL.

### Zmiany w wersji 3.1.0

- **Tryb bezpośredniego wyniku (Direct Output):** Dodano opcję pominięcia okna czatu i natychmiastowego odczytywania odpowiedzi AI przez mowę, dla szybszego i płynniejszego korzystania.
- **Integracja ze schowkiem:** Dodano nowe ustawienie automatycznego kopiowania odpowiedzi AI do schowka.

### Zmiany w wersji 3.0

- **Nowe języki:** Dodano tłumaczenia na perski i wietnamski.
- **Rozszerzone modele AI:** Zreorganizowano listę wyboru modeli z czytelnymi prefiksami ([Darmowa], [Pro], [Auto]), ułatwiającymi rozróżnianie modeli darmowych i płatnych z limitem. Dodano obsługę Gemini 3.0 Pro i Gemini 2.0 Flash Lite.
- **Stabilność dyktowania:** Znacząco poprawiono stabilność inteligentnego dyktowania. Dodano kontrolę bezpieczeństwa ignorującą klipy audio krótsze niż 1 sekunda, zapobiegającą „halucynacjom" AI i pustym błędom.
- **Obsługa plików:** Naprawiono problem uniemożliwiający przesyłanie plików o nazwach w językach innych niż angielski.
- **Optymalizacja poleceń:** Poprawiono logikę tłumaczenia i ustrukturyzowano wyniki rozpoznawania.

### Zmiany w wersji 2.9

- Dodano tłumaczenia na francuski i turecki.
- **Widok sformatowany:** Dodano przycisk „Widok sformatowany" w oknach czatu umożliwiający przeglądanie rozmowy z prawidłowym formatowaniem (nagłówki, pogrubienie, kod) w standardowym oknie przeglądania.
- **Ustawienie Markdown:** Dodano nową opcję „Czyść Markdown w czacie" w ustawieniach. Odznaczenie tego pola pozwala widzieć surową składnię Markdown (np. `**`, `#`) w oknie czatu.
- **Zarządzanie oknami:** Naprawiono problem polegający na wielokrotnym otwieraniu lub nieprawidłowym fokusowaniu okien „Popraw tekst" lub czatu.
- **Ulepszenia UX:** Ustandaryzowano tytuły okien dialogowych plików na „Otwórz" i usunięto zbędne komunikaty głosowe (np. „Otwieranie menu...") dla płynniejszego korzystania.

### Zmiany w wersji 2.8

- Dodano tłumaczenie na włoski.
- **Raport stanu:** Dodano nowe polecenie (NVDA+Control+Shift+I) odczytujące bieżący stan dodatku (np. „Przesyłanie...", „Analizowanie...").
- **Eksport HTML:** Przycisk „Zapisz zawartość" w oknach wyników zapisuje teraz dane jako sformatowany plik HTML, zachowując style takie jak nagłówki i pogrubienie.
- **Interfejs ustawień:** Poprawiono układ panelu ustawień z dostępnym grupowaniem.
- **Nowe modele:** Dodano obsługę gemini-flash-latest i gemini-flash-lite-latest.
- **Języki:** Dodano nepalski do obsługiwanych języków.
- **Logika menu poprawiania:** Naprawiono krytyczny błąd, przez który polecenia „Popraw tekst" nie działały, gdy język interfejsu NVDA nie był angielski.
- **Dyktowanie:** Ulepszone wykrywanie ciszy zapobiegające nieprawidłowemu wynikowi tekstowemu przy braku mowy.
- **Ustawienia aktualizacji:** Opcja „Sprawdzaj aktualizacje przy uruchomieniu" jest teraz domyślnie wyłączona, zgodnie z zasadami Sklepu z dodatkami.
- Porządki w kodzie.

### Zmiany w wersji 2.7

- Zmigrowano strukturę projektu do oficjalnego szablonu dodatków NV Access w celu lepszego zachowania standardów.
- Wdrożono logikę automatycznego ponawiania prób dla błędów HTTP 429 (limit szybkości) w celu zapewnienia niezawodności przy dużym obciążeniu.
- Zoptymalizowano polecenia tłumaczenia w celu zwiększenia dokładności i lepszej obsługi logiki inteligentnej zamiany.
- Zaktualizowano tłumaczenie rosyjskie.

### Zmiany w wersji 2.6

- Dodano obsługę tłumaczenia na rosyjski (podziękowania dla nvda-ru).
- Zaktualizowano komunikaty o błędach, zapewniając bardziej opisowe informacje zwrotne dotyczące łączności.
- Zmieniono domyślny język docelowy tłumaczenia na angielski.

### Zmiany w wersji 2.5

- Dodano natywne polecenie OCR pliku (NVDA+Control+Shift+F).
- Dodano przycisk „Zapisz czat" w oknach wyników.
- Wdrożono pełną obsługę lokalizacji (i18n).
- Przeniesiono sygnały dźwiękowe na natywny moduł sygnałów NVDA.
- Przejście na File API Gemini w celu lepszej obsługi plików PDF i audio.
- Naprawiono awarię przy tłumaczeniu tekstu zawierającego nawiasy klamrowe.

### Zmiany w wersji 2.1.1

- Naprawiono problem polegający na nieprawidłowym działaniu zmiennej `[file_ocr]` w poleceniach niestandardowych.

### Zmiany w wersji 2.1

- Wszystkie skróty klawiszowe ustandaryzowano do formatu NVDA+Control+Shift, aby wyeliminować konflikty z układem laptopa NVDA i systemowymi skrótami.

### Zmiany w wersji 2.0

- Wdrożono wbudowany system automatycznych aktualizacji.
- Dodano pamięć podręczną inteligentnego tłumaczenia umożliwiającą natychmiastowe pobieranie wcześniej przetłumaczonego tekstu.
- Dodano pamięć rozmowy umożliwiającą kontekstowe doprecyzowywanie wyników w oknach czatu.
- Dodano dedykowane polecenie tłumaczenia ze schowka (NVDA+Control+Shift+Y).
- Zoptymalizowano polecenia AI w celu ścisłego wymuszania wyniku w języku docelowym.
- Naprawiono awarię spowodowaną znakami specjalnymi w tekście wejściowym.

### Zmiany w wersji 1.5

- Dodano obsługę ponad 20 nowych języków.
- Wdrożono interaktywne okno dialogowe poprawiania tekstu z pytaniami doprecyzowującymi.
- Dodano natywną funkcję inteligentnego dyktowania.
- Dodano kategorię „Vision Assistant" w oknie „Zdarzenia wejścia" NVDA.
- Naprawiono awarie COMError w określonych aplikacjach, takich jak Firefox i Word.
- Dodano mechanizm automatycznego ponawiania prób przy błędach serwera.

### Zmiany w wersji 1.0

- Pierwsze wydanie.