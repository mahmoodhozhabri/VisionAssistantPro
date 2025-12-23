Dokumentasi Vision Assistant Pro

# Vision Assistant Pro

**Vision Assistant Pro** adalah asisten AI multi-modal canggih untuk NVDA. Add-on ini memanfaatkan model Gemini dari Google untuk menyediakan kemampuan pembacaan layar cerdas, penerjemahan, dikte suara, dan analisis dokumen.

_Add-on ini dirilis untuk komunitas sebagai penghormatan terhadap Hari Internasional Penyandang Disabilitas._

## 1. Pengaturan & Konfigurasi

Buka **Menu NVDA > Preferensi > Pengaturan > Vision Assistant Pro**.

- **API Key (Kunci API):** Wajib. Kolom ini disembunyikan secara default demi keamanan (gunakan "Show API Key" untuk melihat isinya). Dapatkan kunci gratis dari [Google AI Studio](https://aistudio.google.com/).
- **Model:** Pilih antara model **Flash** (Tercepat/Gratis) atau **Pro** (Kecerdasan Tinggi) berdasarkan kebutuhan Anda.
- **Languages (Bahasa):** Atur bahasa Sumber, Target, dan Respon AI.
- **Smart Swap:** Secara otomatis menukar bahasa jika teks sumber cocok dengan bahasa target.
- **Direct Output (Output Langsung):** Melewati jendela obrolan dan membacakan respon langsung melalui suara (speech).
- **Clipboard Integration:** Secara otomatis menyalin respon AI ke papan klip (clipboard).

## 2. Layer Perintah & Pintasan

Untuk mencegah konflik pintasan keyboard, add-on ini menggunakan **Layer Perintah**.
1. Tekan **NVDA + Shift + V** (Kunci Utama) untuk mengaktifkan lapisan perintah (Anda akan mendengar bunyi bip).
2. Lepaskan tombol, lalu tekan salah satu tombol tunggal berikut:

| Tombol        | Fungsi                   | Deskripsi                                                                 |
|---------------|--------------------------|---------------------------------------------------------------------------|
| **T**         | Smart Translator         | Menerjemahkan teks di bawah kursor navigator atau teks yang dipilih.      |
| **Shift + T** | Penerjemah Papan Klip | Menerjemahkan konten yang ada di papan klip saat ini.                      |
| **R**         | Text Refiner             | Merangkum, Memperbaiki Tata Bahasa, Menjelaskan, atau menjalankan **Prompt Kustom**.|
| **V**         | Object Vision            | Mendeskripsikan objek navigator saat ini.                                 |
| **O**         | Full Screen Vision       | Menganalisis tata letak dan konten seluruh layar.                         |
| **Shift + V** | Analisis Video Online    | Menganalisis video **YouTube** atau **Instagram** melalui URL.            |
| **D**         | Analisis Dokumen         | tanya jawab tentang file PDF/TXT/MD/PY.                                      |
| **F**         | File OCR                 | OCR langsung dari file gambar/PDF/TIFF (Mendukung TIFF multi-halaman).    |
| **A**         | Transkripsi Audio        | Mentranskrip file MP3/WAV/OGG.                                            |
| **C**         | Pemecah CAPTCHA          | Menangkap dan memecahkan CAPTCHA secara otomatis.                         |
| **S**         | Dikte Cerdas             | Mengubah ucapan menjadi teks. Tekan untuk mulai merekam, tekan lagi untuk berhenti/mengetik.|
| **L**         | Laporan Status           | Mengumumkan status saat ini (misalnya, "Mengunggah...", "Diam").          |
| **U**         | Cek Pembaruan            | Memeriksa GitHub untuk versi terbaru.                                     |

## 3. Prompt Kustom & Variabel

Buat perintah di Pengaturan dengan format: `Nama:Teks Prompt` (pisahkan dengan `|` atau baris baru).

### Variabel yang Tersedia

| Variabel         | Deskripsi                                        | Tipe Input       |
|------------------|--------------------------------------------------|------------------|
| `[selection]`    | Teks yang dipilih saat ini                       | Teks             |
| `[clipboard]`    | Konten clipboard                                 | Teks             |
| `[screen_obj]`   | Tangkapan layar objek navigator                  | Gambar           |
| `[screen_full]`  | Tangkapan layar layar penuh                      | Gambar           |
| `[file_ocr]`     | Pilih gambar/PDF/TIFF (default ke "Ekstrak teks")| Gambar, PDF, TIFF|
| `[file_read]`    | Pilih dokumen teks                               | TXT, Kode, PDF   |
| `[file_audio]`   | Pilih file audio                                 | MP3, WAV, OGG    |

### Contoh Prompt Kustom

- **Quick OCR:** `My OCR:[file_ocr]`
- **Translate Image:** `Translate Img:Ekstrak teks dari gambar ini dan terjemahkan ke bahasa Indonesia. [file_ocr]`
- **Analisis Audio:** `Rangkum Audio:Dengarkan rekaman ini dan rangkum poin-poin utamanya. [file_audio]`
- **Code Debugger:** `Debug:Temukan bug dalam kode ini dan jelaskan: [selection]`

**Catatan:** Koneksi internet aktif diperlukan untuk semua fitur AI. TIFF multi-halaman diproses secara otomatis.

## Perubahan untuk 3.5.0
*   **Layer Perintah:** Memperkenalkan sistem Layer Perintah (default: `NVDA+Shift+V`) untuk mengelompokkan pintasan di bawah satu kunci utama. Misalnya, alih-alih menekan `NVDA+Control+Shift+T` untuk menerjemahkan, sekarang Anda menekan `NVDA+Shift+V` diikuti oleh `T`.
*   **Analisis Video Online:** Menambahkan fitur baru untuk menganalisis video YouTube dan Instagram secara langsung dengan memberikan URL.

## Perubahan untuk 3.1.0
*   **Mode Output Langsung:** Menambahkan opsi untuk melewati dialog obrolan dan mendengar respons AI langsung melalui ucapan untuk pengalaman yang lebih cepat dan mulus.
*   **Integrasi Clipboard:** Menambahkan pengaturan baru untuk secara otomatis menyalin respons AI ke papan klip.

## Perubahan untuk 3.0
*   **Bahasa Baru:** Menambahkan terjemahan **Persia** dan **Vietnam**.
*   **Model AI yang Diperluas:** Mengatur ulang daftar pemilihan model dengan awalan yang jelas (`[Free]`, `[Pro]`, `[Auto]`) untuk membantu pengguna membedakan antara model gratis dan berbayar (terbatas tarif). Menambahkan dukungan untuk **Gemini 3.0 Pro** dan **Gemini 2.0 Flash Lite**.
*   **Stabilitas Dikte:** Meningkatkan stabilitas Dikte Cerdas secara signifikan. Menambahkan pemeriksaan keamanan untuk mengabaikan klip audio yang lebih pendek dari 1 detik, mencegah halusinasi AI dan kesalahan kosong.
*   **Penanganan File:** Memperbaiki masalah di mana mengunggah file dengan nama non-Inggris akan gagal.
*   **Optimasi Prompt:** Meningkatkan logika Terjemahan dan hasil Visi yang terstruktur.

## Perubahan untuk 2.9
*   **Menambahkan terjemahan Prancis dan Turki.**
*   **Tampilan Terformat:** Menambahkan tombol "View Formatted" (Lihat Terformat) di dialog obrolan untuk melihat percakapan dengan gaya yang tepat (Judul, Tebal, Kode) di jendela peramban standar.
*   **Pengaturan Markdown:** Menambahkan opsi baru "Clean Markdown in Chat" (Bersihkan Markdown di Obrolan) di Pengaturan. Menghapus centang ini memungkinkan pengguna melihat sintaks Markdown mentah (misalnya, `**`, `#`) di jendela obrolan.
*   **Manajemen Dialog:** Memperbaiki masalah di mana jendela "Refine Text" atau obrolan akan terbuka beberapa kali atau gagal fokus dengan benar.
*   **Peningkatan UX:** Menstandarisasi judul dialog file menjadi "Open" dan menghapus pengumuman ucapan yang berlebihan (misalnya, "Opening menu...") untuk pengalaman yang lebih lancar.

## Perubahan untuk 2.8
* Menambahkan terjemahan bahasa Italia.
* **Laporan Status:** Menambahkan perintah baru (NVDA+Control+Shift+I) untuk mengumumkan status add-on saat ini (misalnya, "Mengunggah...", "Menganalisis...").
* **Ekspor HTML:** Tombol "Save Content" di dialog hasil sekarang menyimpan output sebagai file HTML yang diformat, mempertahankan gaya seperti judul dan teks tebal.
* **UI Pengaturan:** Meningkatkan tata letak panel Pengaturan dengan pengelompokan yang aksesibel.
* **Model Baru:** Menambahkan dukungan untuk gemini-flash-latest dan gemini-flash-lite-latest.
* **Bahasa:** Menambahkan bahasa Nepal ke bahasa yang didukung.
* **Logika Menu Refine:** Memperbaiki bug kritis di mana perintah "Refine Text" akan gagal jika bahasa antarmuka NVDA bukan bahasa Inggris.
* **Dikte:** Meningkatkan deteksi keheningan untuk mencegah output teks yang salah ketika tidak ada ucapan yang dimasukkan.
* **Pengaturan Pembaruan:** "Check for updates on startup" sekarang dinonaktifkan secara default untuk mematuhi kebijakan Add-on Store.
* Pembersihan Kode.

## Perubahan untuk 2.7
* Migrasi struktur proyek ke Templat Add-on NV Access resmi untuk kepatuhan standar yang lebih baik.
* Mengimplementasikan logika coba lagi otomatis untuk kesalahan HTTP 429 (Batas Tarif) untuk memastikan keandalan selama lalu lintas tinggi.
* Mengoptimalkan prompt terjemahan untuk akurasi yang lebih tinggi dan penanganan logika "Smart Swap" yang lebih baik.
* Memperbarui terjemahan bahasa Rusia.

## Perubahan untuk 2.6
* Menambahkan dukungan terjemahan bahasa Rusia (Terima kasih kepada nvda-ru).
* Memperbarui pesan kesalahan untuk memberikan umpan balik yang lebih deskriptif mengenai konektivitas.
* Mengubah bahasa target default menjadi bahasa Inggris.

## Perubahan untuk 2.5
* Menambahkan Perintah OCR File Asli (NVDA+Control+Shift+F).
* Menambahkan tombol "Save Chat" ke dialog hasil.
* Mengimplementasikan dukungan lokalisasi penuh (i18n).
* Migrasi umpan balik audio ke modul nada asli NVDA.
* Beralih ke Gemini File API untuk penanganan file PDF dan audio yang lebih baik.
* Memperbaiki kerusakan saat menerjemahkan teks yang mengandung kurung kurawal.

## Perubahan untuk 2.1.1
* Memperbaiki masalah di mana variabel [file_ocr] tidak berfungsi dengan benar dalam Prompt Kustom.

## Perubahan untuk 2.1
* Menstandarisasi semua pintasan untuk menggunakan NVDA+Control+Shift untuk menghilangkan konflik dengan tata letak Laptop NVDA dan hotkey sistem.

## Perubahan untuk 2.0
* Mengimplementasikan sistem Pembaruan Otomatis bawaan.
* Menambahkan Cache Terjemahan Cerdas untuk pengambilan instan teks yang diterjemahkan sebelumnya.
* Menambahkan Memori Percakapan untuk menyempurnakan hasil secara kontekstual dalam dialog obrolan.
* Menambahkan perintah Terjemahan Clipboard Khusus (NVDA+Control+Shift+Y).
* Mengoptimalkan prompt AI untuk secara ketat menegakkan output bahasa target.
* Memperbaiki kerusakan yang disebabkan oleh karakter khusus dalam teks input.

## Perubahan untuk 1.5
* Menambahkan dukungan untuk lebih dari 20 bahasa baru.
* Mengimplementasikan Dialog Refine Interaktif untuk pertanyaan tindak lanjut.
* Menambahkan fitur Dikte Cerdas Asli.
* Menambahkan kategori "Vision Assistant" ke dialog Input Gestures NVDA.
* Memperbaiki kerusakan COMError di aplikasi tertentu seperti Firefox dan Word.
* Menambahkan mekanisme coba lagi otomatis untuk kesalahan server.

## Perubahan untuk 1.0
* Rilis awal.
