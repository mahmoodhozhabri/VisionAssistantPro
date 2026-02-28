# Pomoc Vision Assistant Pro

**Vision Assistant Pro** to wielofunkcyjny asystent AI dla NVDA. Wykorzystuje silniki AI do odczytywania ekranu, tłumaczenia, dyktowania głosowego i analizy dokumentów.

_Ten dodatek został udostępniony społeczności z okazji Międzynarodowego Dnia Osób z Niepełnosprawnościami._

## 1. Konfiguracja

Przejdź do **Menu NVDA > Preferencje > Ustawienia > Vision Assistant Pro**.

### 1.1 Ustawienia połączenia
- **Dostawca:** Najpierw Wybierz usługę AI. Obsługiwani dostawcy to **Google Gemini**, **OpenAI**, **Mistral**, **Groq** oraz **Niestandardowy** (serwery zgodne z OpenAI, np. Ollama/LM Studio).
- **Ważne:** Zalecamy korzystanie z **Google Gemini**, który zapewnia najlepszą jakość (szczególnie przy analizie obrazów i plików).
- **Klucz API:** Wymagany. Można podać wiele kluczy (rozdzielonych przecinkami lub w osobnych wierszach), aby dodatek rotował je automatycznie.
- **Pobierz modele:** Po wprowadzeniu klucza API naciśnij ten przycisk, aby pobrać aktualną listę dostępnych modeli od dostawcy.
- **Model AI:** Wybierz główny model używany do czatu i analizy.

### 1.2 Osobny model dla każdego zadania
*Dostępne dla Gemini, OpenAI, Groq i Mistral.*

> **⚠️ Uwaga:** Te ustawienia są przeznaczone dla **doświadczonych użytkowników**. Jeśli nie wiesz, do czego służy dany model, zostaw tę opcję **odznaczoną**. Wybranie nieodpowiedniego modelu (np. modelu tekstowego do rozpoznawania obrazów) spowoduje błędy.

Zaznacz **„Osobny model dla każdego zadania"**. Pozwala to wybrać konkretne modele z listy rozwijanej:
- **Model dla OCR / rozpoznawania obrazów:** Model do analizy obrazów.
- **Rozpoznawanie mowy (STT):** Model do dyktowania.
- **Synteza mowy (TTS):** Model do generowania audio.
*Uwaga: Nieobsługiwane funkcje (np. TTS dla Groq) zostaną automatycznie ukryte.*

### 1.3 Adresy usług (niestandardowy dostawca)
*Dostępne tylko przy wybranym dostawcy „Niestandardowy".*

> **⚠️ Uwaga:** Ta sekcja umożliwia ręczną konfigurację API i jest przeznaczona dla **użytkowników prowadzących lokalne serwery lub proxy**. Błędne adresy URL lub nazwy modeli uniemożliwią połączenie. Jeśli nie wiesz, do czego służą te pola, zostaw tę opcję **odznaczoną**.

Zaznacz **„Adresy usług"**, aby ręcznie podać dane serwera. W przeciwieństwie do natywnych dostawców, tutaj trzeba **wpisać** konkretne adresy URL i nazwy modeli:
- **URL listy modeli:** Adres do pobrania dostępnych modeli.
- **URL dla OCR/STT/TTS:** Pełne adresy usług (np. `http://localhost:11434/v1/audio/speech`).
- **Niestandardowe modele:** Wpisz ręcznie nazwę modelu (np. `llama3:8b`) dla każdego zadania.

### 1.4 Preferencje ogólne
- **Silnik OCR:** Wybierz między **Chrome (szybki)** a **Gemini (formatowany)**, który lepiej zachowuje układ strony.
    - *Uwaga:* Jeśli wybierzesz „Gemini (formatowany)", ale dostawcą jest np. OpenAI/Groq, dodatek automatycznie skieruje obraz do modelu rozpoznawania aktywnego dostawcy.
- **Głos TTS:** Wybierz preferowany styl głosu. Lista aktualizuje się automatycznie na podstawie aktywnego dostawcy.
- **Kreatywność (temperatura):** Kontroluje losowość odpowiedzi AI. Niższe wartości są lepsze dla tłumaczenia i OCR.
- **URL serwera proxy:** Skonfiguruj, jeśli usługi AI są ograniczone w twoim regionie (obsługuje lokalne proxy, np. `127.0.0.1`, oraz adresy pośredniczące).

## 2. Warstwa poleceń i skróty

Aby uniknąć konfliktów z innymi skrótami, dodatek korzysta z **warstwy poleceń**.
1. Naciśnij **NVDA + Shift + V** (klawisz główny), aby aktywować warstwę (usłyszysz sygnał dźwiękowy).
2. Puść klawisze, a następnie naciśnij jeden z poniższych:

| Klawisz       | Funkcja                  | Opis                                                                        |
|---------------|--------------------------|-----------------------------------------------------------------------------|
| **T**         | Tłumacz                  | Tłumaczy tekst pod kursorem nawigatora lub zaznaczenie.                     |
| **Shift + T** | Tłumaczenie schowka      | Tłumaczy zawartość schowka.                                                |
| **R**         | Poprawianie tekstu       | Podsumuj, popraw gramatykę, wyjaśnij lub uruchom **niestandardowe polecenie**. |
| **V**         | Opis obiektu             | Opisuje bieżący obiekt nawigatora.                                          |
| **O**         | Rozpoznawanie ekranu     | Analizuje układ i zawartość całego ekranu.                                  |
| **Shift + V** | Analiza wideo online     | Analizuj filmy z **YouTube**, **Instagrama**, **TikToka** lub **Twittera (X)**. |
| **D**         | Czytnik dokumentów       | Czytnik PDF i obrazów z wyborem zakresu stron.                              |
| **F**         | OCR pliku                | Rozpoznawanie tekstu z wybranego obrazu, PDF lub TIFF.                      |
| **A**         | Transkrypcja audio       | Transkrybuje pliki MP3, WAV lub OGG na tekst.                              |
| **C**         | Rozwiązywanie CAPTCHA    | Przechwytuje i rozwiązuje CAPTCHA.              |
| **S**         | Dyktowanie               | Zamienia mowę na tekst. Naciśnij raz, aby nagrywać, ponownie, aby zakończyć.  |
| **L**         | Raport stanu             | Odczytuje bieżący postęp (np. „Skanowanie...", „Bezczynny").               |
| **U**         | Sprawdzanie aktualizacji | Ręcznie sprawdza najnowszą wersję dodatku na GitHubie.                     |
| **Spacja**    | Ostatnia odpowiedź AI    | Wyświetla ostatnią odpowiedź AI w oknie czatu do przeglądu lub kontynuacji. |
| **H**         | Pomoc poleceń            | Wyświetla listę wszystkich dostępnych skrótów w warstwie poleceń.           |

### 2.1 Skróty czytnika dokumentów (wewnątrz przeglądarki)
- **Ctrl + PageDown:** Przejdź do następnej strony.
- **Ctrl + PageUp:** Przejdź do poprzedniej strony.
- **Alt + A:** Otwórz okno czatu, aby zadać pytanie o dokument.
- **Alt + R:** Wymuś **ponowne skanowanie AI** przy użyciu aktywnego dostawcy.
- **Alt + G:** Wygeneruj i zapisz plik audio (WAV/MP3). *Ukryte, jeśli dostawca nie obsługuje TTS.*
- **Alt + S / Ctrl + S:** Zapisz wyodrębniony tekst jako plik TXT lub HTML.

## 3. Polecenia niestandardowe i zmienne

Zarządzaj poleceniami w **Ustawienia > Polecenia > Zarządzaj poleceniami...**.

### Obsługiwane zmienne
- `[selection]`: Aktualnie zaznaczony tekst.
- `[clipboard]`: Zawartość schowka.
- `[screen_obj]`: Zrzut ekranu obiektu nawigatora.
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

---

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
