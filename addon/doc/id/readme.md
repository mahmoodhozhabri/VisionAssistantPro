# Dokumentasi Vision Assistant Pro

**Vision Assistant Pro** adalah asisten AI multimodal canggih untuk NVDA. Add-on ini memanfaatkan model Gemini dari Google untuk menyediakan pembacaan layar cerdas, terjemahan, dikte suara, dan analisis dokumen.

_Add-on ini dirilis untuk komunitas dalam rangka memperingati Hari Internasional Penyandang Disabilitas._

## 1. Pengaturan & Konfigurasi

Buka **Menu NVDA > Preferensi > Pengaturan > Vision Assistant Pro**.

- **API Key:** Wajib. Anda bisa memasukkan beberapa kunci (dipisahkan koma atau baris baru). Asisten akan otomatis berpindah kunci saat kuota salah satu kunci habis.
- **AI Model:** Pilih model **Flash** (Tercepat/Gratis), **Lite**, atau **Pro** (Kecerdasan Tinggi).
- **Proxy URL:** Opsional. Gunakan jika Google diblokir di wilayah Anda. Harus berupa alamat web yang menjadi perantara ke Gemini API.
- **OCR Engine:** Pilih **Chrome (Cepat)** untuk hasil cepat atau **Gemini (Terformat)** untuk menjaga tata letak dan pengenalan tabel yang lebih baik.
- **TTS Voice:** Pilih gaya suara untuk membuat file audio dari halaman dokumen.
- **Smart Swap:** Menukar bahasa otomatis jika teks sumber sama dengan bahasa target.
- **Direct Output:** Melewati jendela obrolan dan langsung membacakan respons AI. **Catatan:** Dalam mode ini, Anda tetap bisa menekan **Space** di lapisan perintah untuk membuka lagi hasil terakhir ke dialog obrolan.
- **Clipboard Integration:** Menyalin respons AI ke papan klip secara otomatis.

## 2. Lapisan Perintah & Pintasan

Untuk mencegah konflik keyboard, add-on ini menggunakan **Lapisan Perintah**.
1. Tekan **NVDA + Shift + V** (Tombol Utama) untuk mengaktifkan lapisan (akan terdengar bunyi bip).
2. Lepaskan tombol, lalu tekan salah satu tombol berikut:

| Tombol        | Fungsi                | Deskripsi                                                                  |
|---------------|-----------------------|----------------------------------------------------------------------------|
| **T**         | Penerjemah Cerdas     | Menerjemahkan teks di kursor navigator atau teks yang dipilih.            |
| **Shift + T** | Terjemah Papan Klip   | Menerjemahkan isi papan klip saat ini.                                    |
| **R**         | Penyempurna Teks      | Meringkas, memperbaiki tata bahasa, menjelaskan, atau menjalankan **Prompt Kustom**. |
| **V**         | Visi Objek            | Mendeskripsikan objek navigator saat ini.                                  |
| **O**         | Visi Layar Penuh      | Menganalisis tata letak dan isi seluruh layar.                            |
| **Shift + V** | Analisis Video Online | Menganalisis video **YouTube**, **Instagram**, **TikTok**, atau **Twitter (X)**. |
| **D**         | Pembaca Dokumen       | Pembaca lanjutan untuk PDF dan gambar dengan pilihan rentang halaman.     |
| **F**         | OCR Berkas            | Mengenali teks langsung dari file gambar, PDF, atau TIFF yang dipilih.    |
| **A**         | Transkripsi Audio     | Mentranskripsikan file MP3, WAV, atau OGG ke teks.                        |
| **C**         | Pemecah CAPTCHA       | Menangkap dan memecahkan CAPTCHA di layar atau pada objek navigator.      |
| **S**         | Dikte Cerdas          | Mengubah suara menjadi teks. Tekan sekali untuk mulai rekam, tekan lagi untuk berhenti/ketik. |
| **L**         | Laporan Status        | Mengumumkan progres saat ini (misalnya, "Memindai...", "Diam").           |
| **U**         | Cek Pembaruan         | Mengecek versi add-on terbaru di GitHub secara manual.                    |
| **Space**     | Buka Hasil Terakhir   | Menampilkan respons AI terakhir di dialog obrolan untuk ditinjau atau ditindaklanjuti. |
| **H**         | Bantuan Perintah      | Menampilkan daftar semua pintasan dalam lapisan perintah.                 |

### 2.1 Pintasan Pembaca Dokumen (Di Dalam Penampil)
Setelah dokumen dibuka lewat perintah **D**:
- **Ctrl + PageDown:** Pindah ke halaman berikutnya (mengumumkan nomor halaman).
- **Ctrl + PageUp:** Pindah ke halaman sebelumnya (mengumumkan nomor halaman).
- **Alt + A:** Buka dialog obrolan untuk bertanya tentang dokumen.
- **Alt + R:** Paksa pemindaian ulang halaman saat ini atau semua halaman dengan mesin Gemini.
- **Alt + G:** Buat dan simpan file audio berkualitas tinggi (WAV) dari konten.
- **Alt + S / Ctrl + S:** Simpan teks hasil ekstraksi sebagai file TXT atau HTML.

## 3. Prompt Kustom & Variabel

Buka **Pengaturan > Prompt > Kelola Prompt...** untuk mengatur prompt sistem dan prompt kustom.

- **Tab Default Prompts:** mengubah prompt bawaan. Anda bisa reset satu prompt atau reset semua prompt bawaan.
- **Tab Custom Prompts:** menambah, mengubah, menghapus, dan mengurutkan ulang prompt kustom.
- **Tombol Variables Guide:** membuka jendela bantuan berisi semua variabel dan tipe input yang didukung.

### Variabel Tersedia

| Variabel       | Deskripsi                                    | Tipe Input        |
|----------------|----------------------------------------------|-------------------|
| `[selection]`  | Teks yang sedang dipilih                     | Teks              |
| `[clipboard]`  | Isi papan klip                               | Teks              |
| `[screen_obj]` | Tangkapan layar objek navigator              | Gambar            |
| `[screen_full]`| Tangkapan layar penuh                        | Gambar            |
| `[file_ocr]`   | Pilih file gambar/PDF untuk ekstraksi teks  | Gambar, PDF, TIFF |
| `[file_read]`  | Pilih dokumen untuk dibaca                   | TXT, Kode, PDF    |
| `[file_audio]` | Pilih file audio untuk dianalisis            | MP3, WAV, OGG     |

### Contoh Prompt Kustom

- **Quick OCR:** `My OCR:[file_ocr]`
- **Translate Image:** `Translate Img:Extract text from this image and translate to English. [file_ocr]`
- **Analyze Audio:** `Summarize Audio:Listen to this recording and summarize the main points. [file_audio]`
- **Code Debugger:** `Debug:Find bugs in this code and explain them: [selection]`

***
**Catatan:** Semua fitur AI memerlukan koneksi internet aktif. Dokumen multi-halaman dan TIFF diproses otomatis.

## 4. Dukungan & Komunitas

Ikuti kabar fitur dan rilis terbaru:
- **Kanal Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Untuk laporan bug dan permintaan fitur.

## Perubahan untuk 4.6
* **Pembukaan Ulang Hasil Interaktif:** Menambahkan tombol **Space** pada lapisan perintah, sehingga pengguna bisa langsung membuka kembali respons AI terakhir dalam jendela obrolan untuk pertanyaan lanjutan, termasuk saat mode "Direct Output" aktif.
* **Pusat Komunitas Telegram:** Menambahkan tautan "Official Telegram Channel" di menu Tools NVDA agar pengguna lebih cepat mendapatkan kabar fitur dan rilis terbaru.
* **Stabilitas Respons Lebih Baik:** Logika inti fitur Terjemahan, OCR, dan Visi dioptimalkan agar performa lebih andal dan pengalaman output suara langsung lebih mulus.
* **Panduan Antarmuka Ditingkatkan:** Deskripsi pengaturan dan dokumentasi diperbarui agar sistem pembukaan hasil terbaru lebih jelas dipahami.

## Perubahan untuk 4.5
* **Pengelola Prompt Lanjutan:** Menambahkan dialog khusus di pengaturan untuk mengelola prompt sistem bawaan dan prompt buatan pengguna, termasuk tambah, edit, urut ulang, dan pratinjau.
* **Dukungan Proxy Menyeluruh:** Memperbaiki masalah konektivitas dengan memastikan proxy yang diatur pengguna diterapkan ke semua permintaan API, termasuk terjemahan, OCR, dan pembuatan suara.
* **Migrasi Data Otomatis:** Menambahkan sistem migrasi cerdas untuk memperbarui konfigurasi prompt lama ke format JSON v2 saat pertama kali dijalankan tanpa kehilangan data.
* **Kompatibilitas Diperbarui (2025.1):** Versi minimum NVDA kini 2025.1 karena ketergantungan pustaka pada fitur lanjutan seperti Pembaca Dokumen.
* **Antarmuka Pengaturan Dioptimalkan:** Tata letak pengaturan disederhanakan dengan memisahkan manajemen prompt ke dialog tersendiri agar lebih rapi dan mudah diakses.
* **Panduan Variabel Prompt:** Menambahkan panduan bawaan di dialog prompt agar pengguna mudah memakai variabel dinamis seperti [selection], [clipboard], dan [screen_obj].

## Perubahan untuk 4.0.3
* **Ketahanan Jaringan Ditingkatkan:** Menambahkan mekanisme coba ulang otomatis untuk menangani koneksi internet tidak stabil dan error server sementara.
* **Dialog Terjemahan Visual:** Menambahkan jendela khusus hasil terjemahan agar pengguna mudah menelusuri hasil panjang baris demi baris, mirip hasil OCR.
* **Tampilan Terformat Gabungan:** Fitur "View Formatted" pada Pembaca Dokumen kini menampilkan semua halaman yang diproses dalam satu jendela terstruktur dengan header halaman yang jelas.
* **Alur OCR Dioptimalkan:** Pemilihan rentang halaman otomatis dilewati untuk dokumen satu halaman sehingga proses lebih cepat.
* **Stabilitas API Ditingkatkan:** Beralih ke metode autentikasi berbasis header yang lebih kuat untuk mengatasi potensi error "All API Keys failed" akibat konflik rotasi kunci.
* **Perbaikan Bug:** Memperbaiki beberapa potensi crash, termasuk saat add-on dihentikan dan masalah fokus di dialog obrolan.

## Perubahan untuk 4.0.1
* **Pembaca Dokumen Lanjutan:** Penampil baru untuk PDF dan gambar dengan pemilihan rentang halaman, pemrosesan latar belakang, dan navigasi `Ctrl+PageUp/Down` yang mulus.
* **Submenu Tools Baru:** Menambahkan submenu "Vision Assistant" di menu Tools NVDA untuk akses cepat ke fitur utama, pengaturan, dan dokumentasi.
* **Kustomisasi Fleksibel:** Kini Anda bisa memilih mesin OCR dan suara TTS langsung dari panel pengaturan.
* **Dukungan Multi API Key:** Menambahkan dukungan beberapa API key Gemini. Anda dapat memasukkan satu key per baris atau dipisahkan koma.
* **Mesin OCR Alternatif:** Menambahkan mesin OCR baru agar pengenalan teks tetap andal saat kuota Gemini API habis.
* **Rotasi API Key Cerdas:** Add-on otomatis beralih dan mengingat API key yang bekerja paling cepat untuk melewati batas kuota.
* **Dokumen ke MP3/WAV:** Menambahkan kemampuan membuat dan menyimpan file audio berkualitas tinggi dalam format MP3 (128kbps) dan WAV langsung dari pembaca.
* **Dukungan Instagram Stories:** Menambahkan kemampuan deskripsi dan analisis Instagram Stories lewat URL.
* **Dukungan TikTok:** Menambahkan dukungan video TikTok untuk deskripsi visual penuh dan transkripsi audio klip.
* **Dialog Pembaruan Didesain Ulang:** Antarmuka baru yang lebih aksesibel dengan kotak teks gulir untuk membaca perubahan versi sebelum memasang pembaruan.
* **Status & UX Terpadu:** Menyeragamkan dialog file di seluruh add-on dan meningkatkan perintah 'L' untuk laporan progres real-time.

## Perubahan untuk 3.6.0
* **Sistem Bantuan:** Menambahkan perintah bantuan (`H`) di Lapisan Perintah untuk melihat daftar semua pintasan beserta fungsinya.
* **Analisis Video Online:** Dukungan diperluas untuk video **Twitter (X)** serta peningkatan deteksi URL dan stabilitas.
* **Kontribusi Proyek:** Menambahkan dialog donasi opsional bagi pengguna yang ingin mendukung perkembangan proyek.

## Perubahan untuk 3.5.0
* **Lapisan Perintah:** Menambahkan sistem Lapisan Perintah (default: `NVDA+Shift+V`) untuk mengelompokkan pintasan di bawah satu tombol utama.
* **Analisis Video Online:** Menambahkan fitur analisis video YouTube dan Instagram langsung dari URL.

## Perubahan untuk 3.1.0
* **Mode Output Langsung:** Menambahkan opsi untuk melewati dialog obrolan dan langsung mendengar respons AI.
* **Integrasi Papan Klip:** Menambahkan pengaturan untuk menyalin respons AI ke papan klip secara otomatis.

## Perubahan untuk 3.0
* **Bahasa Baru:** Menambahkan terjemahan **Persia** dan **Vietnam**.
* **Model AI Diperluas:** Daftar model ditata ulang dengan awalan (`[Free]`, `[Pro]`, `[Auto]`) untuk membedakan model gratis dan model terbatas/rate-limited (berbayar). Juga menambahkan dukungan **Gemini 3.0 Pro** dan **Gemini 2.0 Flash Lite**.
* **Stabilitas Dikte:** Meningkatkan stabilitas Dikte Cerdas secara signifikan. Klip audio di bawah 1 detik kini diabaikan untuk mencegah halusinasi AI dan error kosong.
* **Penanganan Berkas:** Memperbaiki kegagalan unggah berkas dengan nama non-Inggris.
* **Optimasi Prompt:** Memperbaiki logika terjemahan dan menata hasil fitur visi agar lebih terstruktur.

## Perubahan untuk 2.9
* **Menambahkan terjemahan Prancis dan Turki.**
* **Tampilan Terformat:** Menambahkan tombol "View Formatted" di dialog obrolan untuk melihat percakapan dengan format yang benar (Heading, Bold, Code).
* **Pengaturan Markdown:** Menambahkan opsi "Clean Markdown in Chat" di pengaturan. Jika dinonaktifkan, sintaks Markdown mentah (misalnya `**`, `#`) tetap terlihat di jendela obrolan.
* **Manajemen Dialog:** Memperbaiki masalah jendela "Refine Text" atau obrolan yang bisa terbuka berkali-kali atau gagal fokus.
* **Peningkatan UX:** Menyeragamkan judul dialog file menjadi "Open" dan menghapus pengumuman suara yang tidak perlu.

## Perubahan untuk 2.8
* Menambahkan terjemahan bahasa Italia.
* **Laporan Status:** Menambahkan perintah baru (NVDA+Control+Shift+I) untuk mengumumkan status add-on saat ini.
* **Ekspor HTML:** Tombol "Save Content" kini menyimpan output sebagai HTML terformat.
* **UI Pengaturan:** Tata letak panel pengaturan ditingkatkan dengan pengelompokan yang lebih aksesibel.
* **Model Baru:** Menambahkan dukungan untuk `gemini-flash-latest` dan `gemini-flash-lite-latest`.
* **Bahasa:** Menambahkan bahasa Nepal ke daftar bahasa yang didukung.
* **Logika Menu Refine:** Memperbaiki bug kritis saat bahasa antarmuka NVDA bukan Inggris.
* **Dikte:** Meningkatkan deteksi keheningan agar tidak muncul teks salah saat tidak ada ucapan.
* **Pengaturan Pembaruan:** "Check for updates on startup" kini nonaktif secara default agar sesuai kebijakan Add-on Store.
* Pembersihan kode.

## Perubahan untuk 2.7
* Migrasi struktur proyek ke Template Add-on resmi NV Access agar lebih sesuai standar.
* Menambahkan logika coba ulang otomatis untuk error HTTP 429 (Rate Limit).
* Mengoptimalkan prompt terjemahan untuk akurasi lebih tinggi dan logika "Smart Swap" yang lebih baik.
* Memperbarui terjemahan Rusia.

## Perubahan untuk 2.6
* Menambahkan dukungan terjemahan Rusia (terima kasih kepada nvda-ru).
* Memperbarui pesan error agar informasi konektivitas lebih jelas.
* Mengubah bahasa target default ke Inggris.

## Perubahan untuk 2.5
* Menambahkan perintah OCR berkas bawaan (NVDA+Control+Shift+F).
* Menambahkan tombol "Save Chat" di dialog hasil.
* Menambahkan dukungan lokalisasi penuh (i18n).
* Memigrasikan umpan balik audio ke modul tones bawaan NVDA.
* Beralih ke Gemini File API untuk penanganan PDF dan audio yang lebih baik.
* Memperbaiki crash saat menerjemahkan teks dengan kurung kurawal.

## Perubahan untuk 2.1.1
* Memperbaiki masalah variabel [file_ocr] yang tidak berfungsi benar dalam Prompt Kustom.

## Perubahan untuk 2.1
* Menstandarkan semua pintasan ke NVDA+Control+Shift untuk menghindari konflik dengan layout laptop NVDA dan hotkey sistem.

## Perubahan untuk 2.0
* Menambahkan sistem Auto-Update bawaan.
* Menambahkan Smart Translation Cache untuk mengambil hasil terjemahan lama secara instan.
* Menambahkan Conversation Memory untuk penyempurnaan hasil obrolan berbasis konteks.
* Menambahkan perintah terjemah papan klip khusus (NVDA+Control+Shift+Y).
* Mengoptimalkan prompt AI agar ketat menggunakan bahasa target.
* Memperbaiki crash karena karakter khusus pada teks masukan.

## Perubahan untuk 1.5
* Menambahkan dukungan lebih dari 20 bahasa baru.
* Menambahkan dialog refine interaktif untuk pertanyaan lanjutan.
* Menambahkan fitur Dikte Cerdas bawaan.
* Menambahkan kategori "Vision Assistant" di dialog Input Gestures NVDA.
* Memperbaiki crash COMError pada aplikasi tertentu seperti Firefox dan Word.
* Menambahkan mekanisme coba ulang otomatis untuk error server.

## Perubahan untuk 1.0
* Rilis awal.
