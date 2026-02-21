# Vision Assistant Pro - Dokumentacja

**Vision Assistant Pro** to zaawansowany, wielomodalny asystent AI dla NVDA. Wykorzystuje modele Gemini od Google, umożliwiając odczytywanie ekranu, tłumaczenie, dyktowanie oraz analizę dokumentów.

*Ten dodatek został udostępniony społeczności z okazji Międzynarodowego Dnia Osób z Niepełnosprawnościami.*

## 1. Instalacja i konfiguracja

Przejdź do **Menu NVDA > Ustawienia > Opcje > Vision Assistant Pro**.

- **Klucz API:** Jest wymagany do działania dodatku. Można wprowadzić wiele kluczy (oddzielając je przecinkami lub nowym wierszem). Asystent będzie automatycznie przełączać się między nimi po wyczerpaniu limitu.
- **Model AI:** Wybierz między modelami **Flash** (najszybszy/darmowy), **Lite** lub **Pro** (wysoka inteligencja).
- **URL proxy:** Opcjonalnie. Użyj, jeśli Google jest zablokowany w Twoim regionie. Musi to być adres internetowy pełniący funkcję pomostu do API Gemini.
- **Silnik OCR:** Wybierz między **Chrome (szybki)** dla szybkich odpowiedzi lub **Gemini (sformatowany)** dla lepszego zachowania układu strony i rozpoznawania tabel.
- **Głos TTS:** Wybierz preferowany styl głosu do generowania plików audio ze stron dokumentów.
- **Inteligentna zamiana (Smart Swap):** Automatycznie zamienia języki miejscami, jeśli tekst źródłowy odpowiada językowi docelowemu.
- **Tryb bezpośredni (Direct Output):** Pomija okno czatu i natychmiast odczytuje odpowiedź AI przez mowę. **Uwaga:** Nawet w tym trybie możesz nacisnąć **Spację** w warstwie poleceń, aby ponownie otworzyć ostatni wynik w oknie czatu.
- **Integracja ze schowkiem (Clipboard Integration):** Automatycznie kopiuje odpowiedź AI do schowka.

## 2. Warstwa poleceń i skróty klawiszowe

Aby zapobiec konfliktom klawiszy, ten dodatek wykorzystuje **warstwę poleceń** (Command Layer).

1. Naciśnij **NVDA + Shift + V** (klawisz główny), aby aktywować warstwę (usłyszysz sygnał dźwiękowy).
2. Zwolnij klawisze, a następnie naciśnij jeden z poniższych klawiszy:

| Klawisz | Funkcja | Opis |
|---|---|---|
| **T** | Inteligentny tłumacz | Tłumaczy tekst pod kursorem nawigatora lub zaznaczenie. |
| **Shift + T** | Tłumaczenie ze schowka | Tłumaczy zawartość znajdującą się w schowku. |
| **R** | Poprawianie tekstu | Podsumuj, popraw gramatykę, wyjaśnij lub uruchom polecenia niestandardowe. |
| **V** | rozpoznawanie obiektu | Opisuje bieżący obiekt nawigatora. |
| **O** | rozpoznawanie pełnego ekranu | Analizuje cały układ i zawartość ekranu. |
| **Shift + V** | Analiza wideo online | Analizuj filmy z **YouTube**, **Instagram**, **TikTok** lub **Twitter (X)**. |
| **D** | Czytnik dokumentów | Zaawansowany czytnik plików PDF i obrazów z wyborem zakresu stron. |
| **F** | OCR pliku | Bezpośrednie rozpoznawanie tekstu z wybranych plików graficznych, PDF lub TIFF. |
| **A** | Transkrypcja audio | Transkrybuj pliki MP3, WAV lub OGG na tekst. |
| **C** | Rozwiązywanie CAPTCHA | Przechwytuje i rozwiązuje CAPTCHA na ekranie lub obiekcie nawigatora. |
| **S** | Inteligentne dyktowanie | Zamienia mowę na tekst. Naciśnij, aby rozpocząć nagrywanie, naciśnij ponownie, aby zatrzymać i wpisać. |
| **L** | Raportowanie stanu | Odczytuje bieżący postęp (np. „Skanowanie...", „Bezczynność"). |
| **U** | Sprawdzanie aktualizacji | Ręczne sprawdzanie najnowszej wersji dodatku na GitHubie. |
| **Spacja** | Przywołanie ostatniego wyniku | Wyświetla ostatnią odpowiedź AI w oknie czatu do przeglądu lub zadawania dodatkowych pytań. |
| **H** | Pomoc poleceń | Wyświetla listę wszystkich dostępnych skrótów w warstwie poleceń. |

### 2.1 Skróty czytnika dokumentów (w przeglądarce)

Po otwarciu dokumentu poleceniem **D**:

- **Ctrl + PageDown:** Przejdź do następnej strony (odczytuje numer strony).
- **Ctrl + PageUp:** Przejdź do poprzedniej strony (odczytuje numer strony).
- **Alt + A:** Otwórz okno czatu, aby zadawać pytania dotyczące dokumentu.
- **Alt + R:** Wymuś ponowne skanowanie bieżącej strony lub wszystkich stron za pomocą silnika Gemini.
- **Alt + G:** Wygeneruj i zapisz plik audio wysokiej jakości (WAV) z zawartości.
- **Alt + S / Ctrl + S:** Zapisz wyodrębniony tekst jako plik TXT lub HTML.

## 3. Polecenia niestandardowe i zmienne

Otwórz **Ustawienia > Prompty > Zarządzaj promptami...** aby skonfigurować prompty systemowe i niestandardowe.

- **Karta promptów domyślnych:** edycja wbudowanych promptów. Można zresetować pojedynczy prompt lub przywrócić wszystkie domyślne.
- **Karta promptów niestandardowych:** dodawanie, edytowanie, usuwanie i zmiana kolejności promptów niestandardowych.
- **Przycisk przewodnika po zmiennych:** otwiera okno pomocy ze wszystkimi obsługiwanymi zmiennymi i typami danych wejściowych.

### Dostępne zmienne

| Zmienna | Opis | Typ danych wejściowych |
|---|---|---|
| `[selection]` | Aktualnie zaznaczony tekst | Tekst |
| `[clipboard]` | Zawartość schowka | Tekst |
| `[screen_obj]` | Zrzut ekranu obiektu nawigatora | Obraz |
| `[screen_full]` | Zrzut pełnego ekranu | Obraz |
| `[file_ocr]` | Wybierz plik graficzny/PDF do wyodrębnienia tekstu | Obraz, PDF, TIFF |
| `[file_read]` | Wybierz dokument do odczytu | TXT, Kod, PDF |
| `[file_audio]` | Wybierz plik audio do analizy | MP3, WAV, OGG |

### Przykładowe polecenia niestandardowe

- **Szybki OCR:** `My OCR:[file_ocr]`
- **Tłumaczenie obrazu:** `Translate Img:Extract text from this image and translate to English. [file_ocr]`
- **Analiza audio:** `Summarize Audio:Listen to this recording and summarize the main points. [file_audio]`
- **Debuger kodu:** `Debug:Find bugs in this code and explain them: [selection]`

***
**Uwaga:** Do działania wszystkich funkcji AI wymagane jest aktywne połączenie internetowe. Dokumenty wielostronicowe i pliki TIFF są przetwarzane automatycznie.

## 4. Wsparcie i społeczność

Bądź na bieżąco z najnowszymi wiadomościami, funkcjami i wydaniami:

- **Kanał Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Zgłaszanie błędów i propozycje nowych funkcji.

## Zmiany w wersji 4.6

* **Możliwość wymuszenia trybu interaktywnego czatu:** Dodano klawisz **Spacja** do warstwy poleceń, umożliwiający natychmiastowe ponowne otwarcie ostatniej odpowiedzi AI w oknie czatu w celu zadawania dodatkowych pytań, nawet gdy aktywny jest tryb Bezpośredni.
* **Hub społeczności na Telegramie:** Dodano link do „Oficjalnego kanału na Telegramie" w menu Narzędzia NVDA, zapewniający szybki dostęp do najnowszych wiadomości, funkcji i wydań.
* **Zwiększona stabilność odpowiedzi:** Zoptymalizowano główną logikę funkcji tłumaczenia, OCR i przetwarzania obrazu, aby umożliwić bardziej niezawodne działanie i płynniejsze korzystanie z trybu bezpośredniego.
* **Ulepszone wskazówki interfejsu:** Zaktualizowano opisy ustawień i dokumentację.

## Zmiany w wersji 4.5

* **Zaawansowany menedżer promptów:** Wprowadzono dedykowane okno zarządzania w ustawieniach do dostosowywania domyślnych promptów systemowych i zarządzania promptami użytkownika z pełną obsługą dodawania, edytowania, zmiany kolejności i podglądu.
* **Kompleksowa obsługa proxy:** Rozwiązano problemy z łącznością sieciową, zapewniając ścisłe stosowanie skonfigurowanych przez użytkownika ustawień proxy do wszystkich żądań API, w tym tłumaczenia, OCR i generowania mowy.
* **Automatyczna migracja danych:** Zintegrowano inteligentny system migracji automatycznie aktualizujący starsze konfiguracje promptów do formatu JSON v2 przy pierwszym uruchomieniu bez utraty danych.
* **Zaktualizowana kompatybilność (2025.1):** Ustawiono minimalną wymaganą wersję NVDA na 2025.1 ze względu na zależności bibliotek w zaawansowanych funkcjach, takich jak czytnik dokumentów, aby zapewnić stabilne działanie.
* **Zoptymalizowany interfejs ustawień:** Uproszczono interfejs ustawień poprzez przeniesienie zarządzania promptami do osobnego okna, zapewniając czystsze i bardziej dostępne środowisko użytkownika.
* **Przewodnik po zmiennych promptów:** Dodano wbudowany przewodnik w oknach promptów, pomagający użytkownikom łatwo identyfikować i używać dynamicznych zmiennych, takich jak [selection], [clipboard] i [screen_obj].

## Zmiany w wersji 4.0.3

* **Zwiększona odporność sieciowa:** Dodano mechanizm automatycznego ponawiania prób w celu lepszej obsługi niestabilnych połączeń internetowych i tymczasowych błędów serwera, zapewniając bardziej niezawodne odpowiedzi AI.
* **Okno tłumaczenia:** Wprowadzono dedykowane okno wyników tłumaczenia. Użytkownicy mogą teraz łatwo nawigować i czytać długie tłumaczenia wiersz po wierszu, podobnie jak wyniki OCR.
* **Zagregowany widok sformatowany:** Funkcja „Widok sformatowany" w czytniku dokumentów wyświetla teraz wszystkie przetworzone strony w jednym, uporządkowanym oknie z wyraźnymi nagłówkami stron.
* **Zoptymalizowany przepływ pracy OCR:** Automatyczne pomijanie wyboru zakresu stron dla dokumentów jednostronicowych, co przyspiesza i usprawnia proces rozpoznawania.
* **Poprawiona stabilność API:** Przejście na bardziej niezawodną metodę uwierzytelniania opartą na nagłówkach, rozwiązujące potencjalne błędy „All API Keys failed" spowodowane konfliktami rotacji kluczy.
* **Poprawki błędów:** Rozwiązano kilka potencjalnych awarii, w tym problem podczas kończenia pracy dodatku oraz błąd fokusa w oknie czatu.

## Zmiany w wersji 4.0.1

* **Zaawansowany czytnik dokumentów:** Nowa, zaawansowana przeglądarka plików PDF i obrazów z wyborem zakresu stron, przetwarzaniem w tle i płynną nawigacją Ctrl+PageUp/Down.
* **Nowe podmenu Narzędzia:** Dodano dedykowane podmenu „Vision Assistant" w menu Narzędzia NVDA dla szybszego dostępu do głównych funkcji, ustawień i dokumentacji.
* **Elastyczna konfiguracja:** Możliwość wyboru preferowanego silnika OCR i głosu TTS bezpośrednio z panelu ustawień.
* **Obsługa wielu kluczy API:** Dodano obsługę wielu kluczy API Gemini. Można wprowadzić jeden klucz w wierszu lub oddzielać je przecinkami w ustawieniach.
* **Alternatywny silnik OCR:** Wprowadzono nowy silnik OCR zapewniający niezawodne rozpoznawanie tekstu nawet po wyczerpaniu limitów API Gemini.
* **Inteligentna rotacja kluczy API:** Automatyczne przełączanie na najszybszy działający klucz API i zapamiętywanie go w celu obejścia limitów.
* **Dokument do MP3/WAV:** Zintegrowano możliwość generowania i zapisywania plików audio wysokiej jakości w formatach MP3 (128 kbps) i WAV bezpośrednio w czytniku.
* **Obsługa Instagram Stories:** Dodano możliwość opisywania i analizowania Instagram Stories za pomocą adresów URL.
* **Obsługa TikTok:** Wprowadzono obsługę filmów TikTok, umożliwiając pełny opis wizualny i transkrypcję audio klipów.
* **Przeprojektowane okno aktualizacji:** Nowy, dostępny interfejs z przewijanym polem tekstowym do wyraźnego odczytania zmian wersji przed instalacją.
* **Ujednolicony stan i UX:** Standaryzacja okien dialogowych plików w całym dodatku oraz ulepszenie polecenia „L" do raportowania postępu w czasie rzeczywistym.

## Zmiany w wersji 3.6.0

* **System pomocy:** Dodano polecenie pomocy (`H`) w warstwie poleceń, zapewniające łatwy dostęp do listy wszystkich skrótów i ich funkcji.
* **Analiza wideo online:** Rozszerzono obsługę o filmy z **Twitter (X)**. Poprawiono również wykrywanie adresów URL i stabilność działania.
* **Wkład w projekt:** Dodano opcjonalne okno donacji dla użytkowników chcących wesprzeć przyszłe aktualizacje i ciągły rozwój projektu.

## Zmiany w wersji 3.5.0

* **Warstwa poleceń:** Wprowadzono system warstwy poleceń (domyślnie: `NVDA+Shift+V`) grupujący skróty pod jednym klawiszem głównym. Na przykład zamiast `NVDA+Control+Shift+T` do tłumaczenia, teraz naciskasz `NVDA+Shift+V`, a następnie `T`.
* **Analiza wideo online:** Dodano nową funkcję analizy filmów z YouTube i Instagram bezpośrednio poprzez podanie adresu URL.

## Zmiany w wersji 3.1.0

* **Tryb bezpośredniego wyjścia:** Dodano opcję pomijania okna czatu i bezpośredniego odczytywania odpowiedzi AI przez mowę, zapewniając szybsze i płynniejsze działanie.
* **Integracja ze schowkiem:** Dodano nowe ustawienie automatycznego kopiowania odpowiedzi AI do schowka.

## Zmiany w wersji 3.0

* **Nowe języki:** Dodano tłumaczenia na **perski** i **wietnamski**.
* **Rozszerzone modele AI:** Przeorganizowano listę wyboru modeli z wyraźnymi prefiksami (`[Free]`, `[Pro]`, `[Auto]`), aby pomóc użytkownikom odróżnić modele darmowe od płatnych (z limitem). Dodano obsługę **Gemini 3.0 Pro** i **Gemini 2.0 Flash Lite**.
* **Stabilność dyktowania:** Znacząco poprawiono stabilność inteligentnego dyktowania. Dodano kontrolę bezpieczeństwa ignorującą klipy audio krótsze niż 1 sekunda, zapobiegając halucynacjom AI i pustym błędom.
* **Obsługa plików:** Naprawiono problem z przesyłaniem plików o nazwach w językach innych niż angielski.
* **Optymalizacja promptów:** Poprawiono logikę tłumaczenia i ustrukturyzowano wyniki wizji.

## Zmiany w wersji 2.9

* **Dodano tłumaczenia na francuski i turecki.**
* **Widok sformatowany:** Dodano przycisk „Widok sformatowany" w oknach czatu do przeglądania rozmowy z odpowiednim formatowaniem (nagłówki, pogrubienie, kod) w standardowym oknie przeglądarki.
* **Ustawienie Markdown:** Dodano nową opcję „Czyść Markdown w czacie" w ustawieniach. Odznaczenie pozwala użytkownikom widzieć surową składnię Markdown (np. `**`, `#`) w oknie czatu.
* **Zarządzanie oknami:** Naprawiono problem powodujący wielokrotne otwieranie lub nieprawidłowe ustawianie fokusa okien „Popraw tekst" lub czatu.
* **Usprawnienia UX:** Ustandaryzowano tytuły okien dialogowych plików na „Otwórz" i usunięto zbędne komunikaty głosowe (np. „Otwieranie menu...") dla płynniejszego działania.

## Zmiany w wersji 2.8

* Dodano tłumaczenie na włoski.
* **Raportowanie stanu:** Dodano nowe polecenie (NVDA+Control+Shift+I) do odczytywania bieżącego stanu dodatku (np. „Przesyłanie...", „Analizowanie...").
* **Eksport HTML:** Przycisk „Zapisz zawartość" w oknach wyników zapisuje teraz dane jako sformatowany plik HTML, zachowując style takie jak nagłówki i pogrubiony tekst.
* **Interfejs ustawień:** Poprawiono układ panelu ustawień z dostępnym grupowaniem.
* **Nowe modele:** Dodano obsługę gemini-flash-latest i gemini-flash-lite-latest.
* **Języki:** Dodano nepalski do obsługiwanych języków.
* **Logika menu poprawiania:** Naprawiono krytyczny błąd powodujący niepowodzenie poleceń „Popraw tekst", gdy język interfejsu NVDA nie był angielski.
* **Dyktowanie:** Poprawiono wykrywanie ciszy, aby zapobiec nieprawidłowemu wyjściu tekstowemu przy braku mowy na wejściu.
* **Ustawienia aktualizacji:** Opcja „Sprawdzaj aktualizacje przy uruchomieniu" jest teraz domyślnie wyłączona, zgodnie z zasadami Add-on Store.
* Oczyszczenie kodu.

## Zmiany w wersji 2.7

* Przeniesiono strukturę projektu na oficjalny szablon dodatku NV Access w celu lepszej zgodności ze standardami.
* Wdrożono logikę automatycznego ponawiania prób dla błędów HTTP 429 (limit szybkości) w celu zapewnienia niezawodności przy dużym obciążeniu.
* Zoptymalizowano polecenia tłumaczenia w celu zwiększenia dokładności i lepszej obsługi logiki inteligentnej zamiany.
* Zaktualizowano tłumaczenie rosyjskie.

## Zmiany w wersji 2.6

* Dodano obsługę tłumaczenia na rosyjski (podziękowania dla nvda-ru).
* Zaktualizowano komunikaty o błędach, zapewniając bardziej opisowe informacje zwrotne dotyczące łączności.
* Zmieniono domyślny język docelowy tłumaczenia na angielski.

## Zmiany w wersji 2.5

* Dodano natywne polecenie OCR pliku (NVDA+Control+Shift+F).
* Dodano przycisk „Zapisz czat" w oknach wyników.
* Wdrożono pełną obsługę lokalizacji (i18n).
* Przeniesiono sygnały dźwiękowe na natywny moduł sygnałów NVDA.
* Przejście na File API Gemini w celu lepszej obsługi plików PDF i audio.
* Naprawiono awarię przy tłumaczeniu tekstu zawierającego nawiasy klamrowe.

## Zmiany w wersji 2.1.1

* Naprawiono problem polegający na nieprawidłowym działaniu zmiennej `[file_ocr]` w poleceniach niestandardowych.

## Zmiany w wersji 2.1

* Wszystkie skróty klawiszowe ustandaryzowano do formatu NVDA+Control+Shift, aby wyeliminować konflikty z układem laptopa NVDA i systemowymi skrótami.

## Zmiany w wersji 2.0

* Wdrożono wbudowany system automatycznych aktualizacji.
* Dodano pamięć podręczną inteligentnego tłumaczenia umożliwiającą natychmiastowe pobieranie wcześniej przetłumaczonego tekstu.
* Dodano pamięć rozmowy umożliwiającą kontekstowe doprecyzowywanie wyników w oknach czatu.
* Dodano dedykowane polecenie tłumaczenia ze schowka (NVDA+Control+Shift+Y).
* Zoptymalizowano polecenia AI w celu ścisłego wymuszania wyniku w języku docelowym.
* Naprawiono awarię spowodowaną znakami specjalnymi w tekście wejściowym.

## Zmiany w wersji 1.5

* Dodano obsługę ponad 20 nowych języków.
* Wdrożono interaktywne okno dialogowe poprawiania tekstu z pytaniami doprecyzowującymi.
* Dodano natywną funkcję inteligentnego dyktowania.
* Dodano kategorię „Vision Assistant" w oknie „Zdarzenia wejścia" NVDA.
* Naprawiono awarie COMError w określonych aplikacjach, takich jak Firefox i Word.
* Dodano mechanizm automatycznego ponawiania prób przy błędach serwera.

## Zmiany w wersji 1.0

* Pierwsze wydanie.
