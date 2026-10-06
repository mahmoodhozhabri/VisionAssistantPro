# Dokumentasi Vision Assistant Pro

<!-- DOWNLOAD_COUNT_START --> Total Unduhan: 62.863 <!-- DOWNLOAD_COUNT_END -->

Vision Assistant Pro dilengkapi dengan berbagai alat canggih. Berikut adalah beberapa skenario umum untuk membantu Anda memilih fitur yang tepat: Add-on ini menggunakan mesin AI kelas dunia untuk membaca layar secara cerdas, menerjemahkan, mendikte dengan suara, dan menganalisis dokumen.

_Add-on ini dirilis untuk komunitas dalam rangka memperingati Hari Internasional Penyandang Disabilitas._

## 1. Pengaturan & Konfigurasi

Buka **Menu NVDA > Preferensi > Pengaturan > Vision Assistant Pro**. Dialog pengaturan tersusun dalam 8 tab yang aksesibel: **Koneksi**, **Perilaku AI**, **Bahasa Terjemahan**, **Pembaca Dokumen**, **Video**, **CAPTCHA**, **Prompt**, dan **Lanjutan**. Dialog pengaturan terdiri dari 9 tab yang aksesibel: **Koneksi**, **Asisten Langsung**, **Perilaku AI**, **Bahasa Terjemahan**, **Pembaca Dokumen**, **Video**, **CAPTCHA**, **Prompt**, dan **Lanjutan**.

### 1.1 Tab Koneksi

- **Pengaturan Penyedia Kustom:** Konfigurasikan endpoint lokal atau kustom. Penyedia yang didukung mencakup **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax**, dan **Kustom** (server yang kompatibel dengan OpenAI seperti Ollama, LM Studio, Jan.ai, atau KoboldCPP).
- **Kunci API:** Masukkan satu atau beberapa kunci API (dipisahkan dengan koma atau baris baru) untuk rotasi otomatis.
- **Ambil Model:** Setelah kunci API dimasukkan, tekan tombol ini untuk mengunduh daftar model terbaru dari penyedia.
- **Model AI:** Pilih model utama untuk obrolan umum dan analisis.
- **Perutean Model Lanjutan (Khusus Tugas):** Anda dapat memilih model khusus dari daftar pilihan untuk tugas OCR, STT, TTS, Operator AI, Video, dan Asisten Langsung. Untuk Gemini, model dikelompokkan secara dinamis berdasarkan kemampuan agar daftar tetap rapi.
- **Pengaturan Penyedia Kustom:** Konfigurasikan endpoint lokal atau kustom. Mencakup **Siapkan AI Lokal** (pengaturan sekali klik untuk Ollama, LM Studio, Jan.ai, atau KoboldCPP) dan **Konfigurasi Endpoint Lanjutan**.
- **Konfigurasi Proksi:** Dukungan penuh untuk tunneling dan pengalihan endpoint di seluruh add-on (termasuk Asisten Langsung, Pengamat Lingkungan, dan TTS). Masukkan **URL Proksi** dan pilih **Mode Proksi**:
  - **Deteksi otomatis:** Mendeteksi secara otomatis apakah URL merupakan proksi penerusan atau proksi balik.
  - **Proksi SOCKS5:** Menggunakan tunneling penerusan melalui SOCKS5 dengan autentikasi nama pengguna/kata sandi RFC 1929 dan resolusi nama domain.
  - **Proksi HTTP:** Menggunakan tunneling penerusan melalui proksi HTTP dengan autentikasi Basic.
  - **Proksi Balik:** Mengganti endpoint secara langsung untuk gateway AI kustom dan server mirror yang dihosting sendiri (kredensial dinonaktifkan dalam mode ini).
- **Simpan obrolan ke riwayat:** Menyimpan percakapan Anda dalam daftar Riwayat.
- **Opsi Koneksi & Keluaran:** Atur URL Proksi, pemeriksaan pembaruan saat mulai, Bersihkan Markdown dalam Obrolan, salin respons AI ke papan klip, Keluaran Langsung (Tanpa Jendela Obrolan), dan Keluaran Langsung Asisten Langsung.
- **Simpan Percakapan ke Riwayat:** Menyimpan percakapan Anda dalam daftar Riwayat.

### 1.2 Tab Asisten Langsung

- **Asisten Langsung: Keluaran Langsung (Tanpa Jendela):** Memulai Asisten Langsung tanpa jendela percakapan; buka jendelanya nanti dengan tombol Tampilkan Kembali Hasil Terakhir (`Space`).
- **Tekan untuk Bicara:** Mengaktifkan atau menonaktifkan mode tekan untuk bicara. Saat diaktifkan, mikrofon hanya mengirim audio selama Anda menahan tombol yang ditetapkan.
- **Tombol Tekan untuk Bicara:** Tekan tombol untuk merekam pintasannya (misalnya `F12` atau `Ctrl+F12`) — Anda bahkan dapat menetapkan satu tombol pengubah seperti `Left Ctrl`. Tahan tombol untuk berbicara dan lepaskan untuk selesai; bunyi bip singkat mengonfirmasi setiap penekanan dan pelepasan.

Catatan: Tab ini hanya muncul jika penyedia aktif Anda adalah **Google Gemini** atau penyedia Kustom yang kompatibel dengan Gemini.

### 1.3 Tab Perilaku AI

- **Kreativitas (Temperature):** Mengatur keacakan dan kreativitas AI (dari 0,0 hingga 2,0). Nilai lebih rendah menghasilkan terjemahan dan OCR yang lebih konsisten serta akurat.

### 1.4 Tab Bahasa Terjemahan

- **Bahasa Sumber:** Pilih bahasa masukan bawaan.
- 1.2 Tab Perilaku AI
- **Bahasa Respons AI:** Pilih bahasa untuk respons AI secara umum.
- 1.3 Tab Bahasa Terjemahan

### 1.5 Tab Pembaca Dokumen

- **Mesin OCR:** Pilih **Chrome (Cepat)** untuk hasil cepat atau **AI (Lanjutan)** untuk mempertahankan tata letak dengan lebih baik.
- **Ukuran Batch OCR:** Tentukan jumlah halaman per permintaan (atur ke 0 agar diproses dalam satu permintaan).
- **Deskripsikan Gambar dalam Teks:** Aktifkan deskripsi gambar di antara teks saat mengekstrak teks dokumen.
- **Ekspor Nomor Halaman:** Aktifkan nomor dan pemisah halaman pada keluaran dokumen multihalaman.
- 1.4 Tab Pembaca Dokumen
- **Simpan Dokumen ke Riwayat:** Menyimpan dokumen yang dibuka dalam daftar Riwayat; teks OCR dalam cache dan data untuk melanjutkan proses tetap disimpan.

### 1.6 Tab Video

- **Ukuran Potongan Video:** Tentukan durasi segmen dalam menit untuk pembuatan Deskripsi Audio (atur ke 0 untuk memproses seluruh file).
- **Tambahkan Daftar Karakter:** Tambahkan kamus karakter sebagai entri subtitel pertama.
- **Tambahkan Penafian AI:** Sisipkan penafian AI di awal subtitel SRT video.
- **Kamus Karakter & Pengelolaan Serial:** Tambahkan, edit, impor, atau kelola nama karakter, deskripsi fisik, dan peran per serial — AI otomatis mencocokkan karakter yang ditemukan dengan kamus Anda dan menggabungkan karakter baru saat Anda menganalisis lebih banyak episode. 1.5 Tab Video

### 1.7 Tab CAPTCHA

- **Aktifkan Pemecah CAPTCHA Visual:** Aktifkan pemecahan tantangan visual otomatis (hCaptcha, reCAPTCHA).
- **Metode CAPTCHA Teks:** Pilih antara menangkap **Objek Navigator** atau **Layar Penuh**.

### 1.8 Tab Prompt

- **Kelola Prompt:** Membuka dialog untuk menyesuaikan Prompt sistem bawaan atau membuat, mengedit, mengurutkan ulang, dan mempratinjau Prompt kustom dengan variabel dinamis seperti `[selection]` dan `[screen_fg_obj]`.
- **Pintasan Prompt Kustom:** Tetapkan tombol pintasan khusus untuk prompt kustom langsung di Pengelola Prompt. Tekan tombol untuk merekamnya — tombol tunggal dijalankan dalam Lapisan Perintah (dan secara global sebagai `NVDA + Shift + key`), sedangkan kombinasi seperti `Control + Shift + 1` dapat langsung dijalankan secara global.
- 1.6 Tab CAPTCHA

### 1.9 Tab Lanjutan & Pencatatan Global

Buka tab **Lanjutan** untuk mengatur pencatatan global add-on:

- **Aktifkan file log khusus:** Mencatat semua peristiwa operasional, lalu lintas API, dan error dari seluruh modul add-on ke file terpisah (`vision_assistant.log`).
- **Tingkat Log:** Pilih tingkat perincian antara **Debug (Semua Detail)**, **Info (Informasi Umum)**, **Peringatan (Hanya Peringatan)**, dan **Error (Hanya Error)**.
- 1.7 Tab Prompt
- **Kontrol Pengelolaan Log:** Gunakan **Buka File Log**, **Buka Folder Log**, atau **Bersihkan File Log** untuk memeriksa atau membersihkan data log tanpa memulai ulang NVDA dan tanpa mengganggu log standar NVDA.
- 1.8 Tab Lanjutan & Pencatatan Global

### 1.10 Pencadangan & Pemulihan Pengaturan

Tab **Lanjutan** juga memiliki bagian **Pencadangan dan Pemulihan**:

- **Cadangkan:** Menyimpan konfigurasi Anda ke satu berkas JSON. Saat mengekliknya, Anda dapat memilih data yang disertakan: **Semuanya** (pengaturan, label kustom, progres OCR, dan riwayat) atau **Hanya Pengaturan**.
- **Pulihkan:** Memuat cadangan yang telah disimpan untuk memulihkan konfigurasi dan data Anda kapan saja, di komputer mana pun, atau setelah memasang ulang NVDA. Anda akan diminta mengonfirmasi terlebih dahulu karena pemulihan mengganti seluruh pengaturan dan data saat ini.

## 2. Pengelola Kunci API Gemini

Membuat kunci API Gemini di **aistudio.google.com** sebelumnya merupakan langkah tersulit dalam penggunaan add-on. Halamannya membingungkan saat diakses dengan pembaca layar, dan sebagian orang bahkan tidak dapat membuat kunci sama sekali. **Pengelola Kunci API Gemini** mengatasi masalah tersebut. Tekan **G** pada Lapisan Perintah, atau buka **Menu NVDA > Preferensi > Pengaturan > Vision Assistant > Koneksi**, lalu tekan **Dapatkan Kunci API Gemini...**.

- **Masuk:** Saat Anda membuka pengelola, browser bawaan langsung membuka halaman masuk Google yang aman. Masuk dengan akun Google Anda — tidak diperlukan alat eksternal, SDK, atau pengaturan melalui baris perintah. Akun yang sedang Anda gunakan selalu ditampilkan pada tombol **Keluar**.
- **Membuat kunci:** Setelah masuk, Anda dapat langsung membuat kunci dengan **Proyek dan Kunci Baru** tanpa pengaturan sebelumnya. Jika sudah memiliki proyek, proyek tersebut muncul dalam daftar sederhana. Pilih salah satunya, lalu tekan **Buat Kunci untuk Proyek Terpilih**.
- **Langkah berikutnya:** Kunci baru langsung disalin ke papan klip dan disimpan dalam add-on untuk digunakan nanti. Anda akan ditanya sekali apakah ingin menambahkannya ke daftar kunci add-on. Itu saja yang diperlukan — Anda tidak perlu menelusuri berbagai halaman web.
- **Mengelola kunci:** **Salin Kunci untuk Proyek Terpilih** menyalin kunci proyek yang Anda pilih, **Salin Kunci Terakhir yang Dibuat** menyalin kunci yang baru saja dibuat, dan **Ekspor Kunci Tersimpan ke CSV...** menyimpan semua kunci yang telah dibuat ke sebuah berkas.
- **Menghapus kunci:** **Hapus Kunci...** menampilkan kunci yang ada dalam proyek terpilih, meminta Anda memilih kunci yang akan dihapus, lalu meminta konfirmasi sebelum menghapusnya. Menghapus kunci juga menghilangkannya dari daftar kunci add-on, sehingga tidak ada kunci yang sudah tidak berfungsi tersisa dalam rotasi. Kunci yang dibuat di luar add-on juga dapat dihapus selama akun Anda memiliki izin pada proyek tersebut.
- **Keluar:** **Keluar** menghapus informasi masuk yang tersimpan di komputer, sehingga Anda dapat beralih ke akun lain kapan saja.

## 3. Lapisan Perintah & Pintasan

- Menstandarkan semua pintasan agar memakai NVDA+Control+Shift untuk menghindari konflik dengan layout Laptop NVDA dan hotkey sistem.

1. 1. Tekan **NVDA + Shift + V** untuk masuk ke Lapisan Perintah, lalu tekan **Control + V**.
2. Lepaskan tombol, lalu tekan salah satu tombol tunggal berikut:

| **Alt + Q**                                                                                | Laporan Kunci Kuota Habis                                                                                                                        | Melaporkan jumlah kunci API Gemini yang telah melebihi kuota harian beserta waktu pengaturannya ulang.                                                                                                                                                     |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shift + A**                                                                              | Operator AI                                                                                                                                      | **Operasi Mandiri:** Minta AI melakukan tugas di layar Anda. Tekan lagi untuk langsung membatalkan operasi yang sedang berjalan. Menekannya lagi akan langsung membatalkan operasi yang sedang berjalan.   |
| **E**                                                                                      | **Penjelajah Antarmuka**                                                                                                                         | **E**                                                                                                                                                                                                                                                                      |
| UI Explorer                                                                                | **Klik Interaktif:** Mengenali dan mengklik elemen UI di aplikasi apa pun.                                       | **T**                                                                                                                                                                                                                                                                      |
| Penerjemah Cerdas                                                                          | Menerjemahkan teks di kursor navigator atau teks yang dipilih.                                                                   | **Shift + T**                                                                                                                                                                                                                                                              |
| Penerjemah Papan Klip                                                                      | Menerjemahkan isi papan klip saat ini.                                                                                           | **R**                                                                                                                                                                                                                                                                      |
| Penyempurna Teks                                                                           | Meringkas, memperbaiki tata bahasa, menjelaskan, atau menjalankan **Prompt Kustom**.                                             | **V**                                                                                                                                                                                                                                                                      |
| Visi Objek                                                                                 | Mendeskripsikan Objek Navigator saat ini.                                                                                        | **O**                                                                                                                                                                                                                                                                      |
| Visi Layar Penuh                                                                           | Menganalisis tata letak dan isi seluruh layar.                                                                                   | **Shift + V**                                                                                                                                                                                                                                                              |
| Analisis Video                                                                             | Menganalisis file video lokal atau video online **YouTube**, **Instagram**, **TikTok**, atau **Twitter (X)**. | **Control + V**                                                                                                                                                                                                                                                            |
| Perekaman Video Lokal                                                                      | Merekam video tanpa suara dari layar Anda dan menganalisis tindakan serta tata letaknya.                                         | **D**                                                                                                                                                                                                                                                                      |
| Pembaca Dokumen                                                                            | Pembaca lanjutan untuk PDF dan gambar dengan pilihan rentang halaman.                                                            | **F**                                                                                                                                                                                                                                                                      |
| Tindakan File Cerdas                                                                       | Mengenali konteks dari file gambar, PDF, atau TIFF yang dipilih.                                                                 | **M** Transkripsi dan Sulih Suara Media                                                                                                                                                                                                                                    |
| Mentranskripsikan atau menyulihsuarakan file audio/video ke bahasa target. | **C**                                                                                                                                            | Pemecah CAPTCHA                                                                                                                                                                                                                                                            |
| Menangkap dan memecahkan CAPTCHA.                                          | **Shift + C**                                                                                                                                    | Obrolan Langsung                                                                                                                                                                                                                                                           |
| Membuka antarmuka obrolan berbasis teks secara langsung dengan AI.         | **S**                                                                                                                                            | Dikte Cerdas Mengubah ucapan menjadi teks. Tekan untuk mulai merekam, tekan lagi untuk berhenti dan mengetik hasilnya.                                                                                                                     |
| **Control + T**                                                                            | Terjemahan Suara                                                                                                                                 | Mentranskripsikan, menerjemahkan, lalu mengetik hasil sesuai pengaturan bahasa.                                                                                                                                                                            |
| **Control + L**                                                                            | Asisten Langsung                                                                                                                                 | **Kopilot Real-time (Khusus Gemini):** Memulai atau mengakhiri percakapan suara dan layar langsung dengan asisten AI.                                                                                                   |
| **Control+A**                                                                              | **Operator Langsung**                                                                                                                            | **Kendali Komputer Mandiri (khusus Gemini):** Memulai atau mengakhiri sesi suara langsung, tempat operator melaksanakan permintaan Anda di komputer.                                                                    |
| **G**                                                                                      | **Pengelola Kunci API Gemini**                                                                                                                   | **Buat kunci API tanpa melalui situs web (khusus Gemini):** Membuka pengelola yang menyiapkan kebutuhan komputer, membuka browser untuk masuk, serta membuat, menyalin, atau menghapus kunci untuk proyek pilihan Anda. |
| **I**                                                                                      | Laporan Status                                                                                                                                   | Mengumumkan progres saat ini (misalnya, "Memindai...", "Siaga").                                                                                                                        |
| **L**                                                                                      | Label Objek                                                                                                                                      | **Pelabelan AI Semantik:** Memberi label permanen pada elemen/ikon fokus saat ini.                                                                                                                                                         |
| **Shift + L**                                                                              | Kelola/Pindai Label                                                                                                                              | Membuka Pengelola Label (jika label sudah ada) atau memindai aplikasi untuk elemen tanpa nama.                                                                                                                                          |
| **U**                                                                                      | Pemeriksaan Pembaruan                                                                                                                            | Memeriksa versi terbaru add-on di GitHub secara manual.                                                                                                                                                                                                    |
| **U**                                                                                      | Cek Pembaruan                                                                                                                                    | Mengecek versi terbaru add-on di GitHub secara manual.                                                                                                                                                                                                     |
| **Space**                                                                                  | Buka Hasil Terakhir                                                                                                                              | Menampilkan respons AI terakhir di dialog obrolan untuk ditinjau atau ditindaklanjuti.                                                                                                                                                                     |
| **H**                                                                                      | Bantuan Perintah                                                                                                                                 | Menampilkan daftar semua pintasan yang tersedia.                                                                                                                                                                                                           |
| **Alt + S**                                                                                | Pengaturan                                                                                                                                       | Membuka dialog pengaturan Vision Assistant Pro secara instan.                                                                                                                                                                                              |
| **Alt + Q**                                                                                | Laporan Kunci Kuota Habis                                                                                                                        | Melaporkan jumlah kunci API Gemini yang telah melebihi kuota harian beserta waktu pengaturannya ulang.                                                                                                                                                     |
| **Alt + M**                                                                                | Audit Perutean                                                                                                                                   | Melaporkan model AI yang saat ini dipilih dalam perutean lanjutan.                                                                                                                                                                                         |
| **Up / Down**                                                                              | Navigasi Pengaturan Cepat                                                                                                                        | Berpindah antar kategori Pengaturan Cepat di dalam lapisan. **Left / Right**                                                                                                                                                                               |
| Ubah Pengaturan Cepat                                                                      | Mengubah nilai Pengaturan Cepat yang sedang dipilih.                                                                             | Mengubah nilai pengaturan cepat yang sedang dipilih.                                                                                                                                                                                                       |

## 4. Percakapan & Riwayat

Saat jendela obrolan terbuka (Obrolan Langsung, obrolan dokumen, penyempurnaan teks, dan lainnya), gunakan:

### 3.1 Pintasan Jendela Percakapan

Saat jendela percakapan terbuka (Percakapan Langsung, percakapan dokumen, penyempurnaan teks, dan sejenisnya), Anda dapat meninjau percakapan dengan:

- **Alt + Down:** Membaca pesan berikutnya.
- **Alt + Up:** Membaca pesan sebelumnya.
- **Alt + C:** Menyalin pesan saat ini.

### 3.2 Riwayat (Control + H)

Tekan **Control + H** pada Lapisan Perintah untuk membuka dialog **Riwayat** yang berisi percakapan dan dokumen sebelumnya, dengan filter berdasarkan jenis (Semua / Percakapan / Dokumen). Buka percakapan untuk melanjutkannya — termasuk berkas lampiran yang akan dilampirkan kembali secara otomatis — atau buka dokumen untuk melanjutkan membaca. Tekan **Delete** pada item untuk menghapusnya, atau **Hapus Semua** untuk mengosongkan daftar. Untuk dokumen, Delete menanyakan apakah Anda hanya ingin menghapus entri riwayat atau juga menghapus teks OCR dokumen dari cache agar pemindaian berikutnya dimulai dari awal — tersedia opsi **Jangan tanya lagi** untuk mengingat pilihan Anda.

Anda juga dapat memilih apa yang disimpan dalam daftar. **Simpan percakapan ke riwayat** (tab Koneksi) dan **Simpan dokumen ke riwayat** (tab Pembaca Dokumen) sama-sama diaktifkan secara bawaan, dan keduanya dapat diaktifkan atau dinonaktifkan melalui Pengaturan Cepat. Opsi dokumen hanya memengaruhi entri Riwayat — teks OCR dalam cache dan data untuk melanjutkan proses selalu disimpan.

## 5. Operator AI - Kontrol Komputer Mandiri

**Operator AI** mengubah Vision Assistant Pro dari pembaca pasif menjadi asisten aktif yang dapat berinteraksi dengan komputer atas nama Anda. Anda dapat memintanya mendeskripsikan layar, menjawab pertanyaan tentang apa yang dilihatnya, atau bahkan mengambil kendali—mengeklik tombol, menyeret item, mengetik teks, dan menjelajahi aplikasi dengan perintah bahasa sehari-hari.

Apa keunggulan utamanya? Fitur ini dapat bekerja dengan baik bahkan pada perangkat lunak yang sama sekali tidak aksesibel. Jika Anda mengalami kesulitan pada aplikasi kustom, desktop jarak jauh, atau situs web yang membuat pembaca layar tidak bersuara sama sekali, operator tetap dapat membantu. Karena dapat "melihat" layar secara visual, operator dapat menemukan, membaca, dan berinteraksi dengan elemen yang tidak memiliki label aksesibilitas sama sekali.

### Tindakan yang Didukung

1. 1. Tekan **NVDA + Shift + V**, lalu **Shift + A** (atau gunakan pintasan langsung) untuk membuka dialog Operator AI.
2. 2. Ketik tindakan yang Anda inginkan dengan bahasa biasa, misalnya "Klik tombol Simpan", "Apa isi pesan error?", atau "Ubah nama file menjadi final.pdf".
3. 3. AI akan menganalisis layar, mengenali elemen yang sesuai, lalu menjalankan tindakan atau memberikan jawaban. Jika tugas memerlukan beberapa langkah, Operator AI akan terus bekerja hingga selesai. 4. Tekan **Shift + A** lagi kapan saja untuk langsung membatalkan operasi yang sedang berlangsung.
4. Tekan **Shift + A** lagi kapan saja untuk langsung membatalkan operasi yang sedang berjalan.

### 4.2 Tindakan yang Didukung

**Deskripsikan & Jawab:** "Deskripsikan tata letak layar" atau "Apa isi pesan error?"

- **Jelaskan & Jawab**: "Jelaskan tata letak layar" atau "Apa isi pesan kesalahan tersebut?"
- **Klik**: "Klik tombol Simpan"
- **Klik Kanan**: "Klik kanan file tersebut"
- **Seret & Lepas:** "Seret dokumen ke folder Arsip"
- **Ketik:** "Ketik 'Hello World' di kotak pencarian"
- **Gulir:** "Gulir ke bawah tiga kali"
- **Tekan Tombol:** "Tekan Enter", "Tekan Tab", "Tekan Escape"
- **Tugas Bertahap:** "Buka File Explorer, cari laporan, lalu ubah namanya menjadi final.pdf"
- **Tugas Bertahap**: "Buka File Explorer, cari laporan, dan ubah namanya menjadi final.pdf"

### 4.3 Catatan Penting

- **Peringatan Penggunaan API:** Karena Operator AI perlu "melihat" apa yang terjadi di layar, fitur ini mengirim tangkapan layar beresolusi tinggi pada setiap langkah. Penggunaan yang sering akan menghabiskan kuota API lebih cepat daripada fitur berbasis teks. Penggunaan yang sering akan menghabiskan kuota API jauh lebih cepat dibandingkan fitur standar berbasis teks.
- **Aplikasi Administrator:** Jika NVDA tidak dijalankan dengan hak Administrator, Operator AI mungkin tidak dapat berinteraksi dengan jendela yang memerlukan izin lebih tinggi. Ini adalah batasan keamanan Windows, bukan bug add-on. Ini merupakan batasan keamanan Windows, bukan bug pada add-on.
- **Praktik Terbaik:** Berikan perintah yang jelas dan spesifik. "Klik tombol Kirim berwarna biru di bagian bawah formulir" hampir selalu lebih efektif daripada sekadar "Klik tombol". "Klik tombol Kirim berwarna biru di bagian bawah formulir" hampir selalu lebih efektif daripada hanya "Klik tombolnya".

### 4.4 Operator Langsung (Control+A)

Operator Langsung memungkinkan Asisten Langsung melaksanakan permintaan Anda di komputer sambil Anda berbicara dengannya, termasuk pada aplikasi yang tidak dapat dibaca oleh pembaca layar.
_(Catatan: Fitur ini khusus untuk Google Gemini dan penyedia Kustom yang kompatibel dengan Gemini)._

- **Mengaktifkan:** Tekan **Control+A** pada Lapisan Perintah untuk memulai sesi operator langsung; tekan lagi untuk mengakhirinya.
- **Cara kerja:** Sampaikan permintaan dalam bahasa sehari-hari, misalnya "buka Chrome dan cari situs web" atau "ubah nama berkas ini menjadi final". Operator melihat layar, menjalankan langkah demi langkah, dan terus mengerjakan permintaan bertahap hingga tugas selesai.
- **Pengumuman:** Setiap langkah diucapkan dengan suara Asisten Langsung. Asisten akan memberi tahu Anda saat tugas selesai atau menjelaskan alasan tugas tidak dapat diselesaikan.
- **CAPTCHA:** Jika CAPTCHA muncul, operator mencoba **pemecah CAPTCHA** bawaan terlebih dahulu; jika tidak berhasil, Anda akan diminta menyelesaikan sendiri tantangan yang aksesibel.
- **Menghentikan:** Tekan **Hentikan tindakan operator** di jendela Asisten Langsung untuk membatalkan tugas saat ini.
- **Pengaturan:** Instruksi operator dapat diedit di Pengelola Prompt (bagian **Langsung**, **Instruksi Operator Langsung**). Sakelar **Keluaran Langsung Mode Langsung (Tanpa Jendela)** juga tersedia di Pengaturan Cepat.

## 6. Analisis Video & Deskripsi Audio

> **Catatan:** Fitur Analisis Video dan Deskripsi Audio hanya didukung oleh penyedia **Google Gemini**. Pastikan penyedia aktif di pengaturan add-on adalah Google Gemini.

Vision Assistant Pro menghadirkan kemampuan pemrosesan video yang andal dan dirancang khusus bagi pengguna tunanetra. Fitur ini dapat menganalisis video daring maupun rekaman layar lokal untuk memberikan deskripsi visual yang sangat terperinci dan menghasilkan naskah Deskripsi Audio profesional (SRT).

### 5.1 Perekaman Layar Lokal (Control + V)

Jika ada video tanpa suara, animasi, atau tutorial di layar, Anda dapat merekamnya langsung:

1. Tekan **NVDA + Shift + V** untuk masuk ke Lapisan Perintah, lalu tekan **Control + V**.
2. Add-on akan merekam layar di latar belakang tanpa mengeluarkan suara.
3. Tekan **Control + V** lagi untuk menghentikan perekaman.
4. AI kemudian menganalisis segmen video yang direkam dan memberikan deskripsi yang sangat terperinci tentang adegan, karakter, dan tindakan.

### 5.2 Analisis Video (Shift + V)

Anda dapat menganalisis berkas video lokal maupun video daring. Cukup pilih berkas video lokal di Windows Explorer, atau salin tautan video daring ke papan klip. Anda juga dapat menekan **Shift + V** dari mana saja (misalnya dalam pemutar media) untuk membuka dialog tempat Anda memilih berkas video atau menempelkan URL secara manual.

- **Platform Daring yang Didukung:** YouTube, Instagram, TikTok, dan Twitter (X).
- AI akan otomatis mendeteksi berkas lokal atau URL, memproses video, lalu memberikan deskripsi visual menyeluruh dan ringkasan audio.
- **Cache Berkas Video Selama 48 Jam:** Video yang diunggah ke Gemini disimpan dalam cache selama 48 jam! Anda dapat membuat ulang keluaran SRT atau MP3 untuk video yang sama tanpa mengunggahnya kembali — bahkan setelah NVDA dimulai ulang. Cache mengenali kunci API yang digunakan dan otomatis tidak berlaku lagi saat kunci API Anda berubah.

### 5.3 Pembuatan Deskripsi Audio (SRT)

Untuk hasil yang lebih terstruktur, add-on dapat menghasilkan naskah Deskripsi Audio profesional dalam format SubRip (SRT) standar.

- **Penentuan Waktu Jeda Cerdas:** AI mendengarkan trek audio dan menempatkan deskripsi visual pada jeda alami serta bagian hening agar sesedikit mungkin bertumpang tindih dengan dialog.
- **Pelacakan Karakter:** Mesin melakukan analisis awal untuk mengenali karakter yang berbeda berdasarkan ciri wajah yang tetap. Mesin membuat kamus global untuk melacak dan memberi label karakter secara akurat di berbagai adegan tanpa tertukar. Mesin juga melacak **kemunculan pertama** setiap karakter dan mendeskripsikan penampilan fisiknya hanya sekali — saat pertama kali muncul — lalu hanya menggunakan nama yang telah ditetapkan pada adegan berikutnya agar narasi tetap segar dan alami.
- **OCR Teks Apa Adanya:** Setiap teks yang muncul di layar (papan tanda, ponsel, kredit) dikutip persis seperti aslinya.
- **Cara Menggunakan:** Untuk mendengarkan subtitel yang dihasilkan, letakkan berkas `.srt` dalam folder yang sama dengan berkas video dan beri nama yang persis sama. Kemudian, atur pemutar media (misalnya VLC atau PotPlayer) agar meneruskan teks subtitel langsung ke pembaca layar atau mesin TTS selama pemutaran.
- **Penyimpanan yang Lebih Mudah:** Saat menyimpan berkas SRT atau MP3, dialog berkas kini secara bawaan terbuka di folder video sumber, baik ketika video dibuka melalui dialog berkas maupun dengan Shift+V dari Explorer.

### 5.4 Narasi Audio Tersinkron (Ekspor MP3)

Selain membuat berkas SRT berbasis teks, add-on berfungsi sebagai alat produksi Deskripsi Audio lengkap dengan mengubah deskripsi menjadi ucapan dan mencampurkannya dengan video. Anda kini dapat memilih **Gemini Live TTS** sebagai mesin suara, yang menggunakan Gemini Live API untuk menghasilkan narasi suara yang sangat realistis tanpa batas. Saat membuat MP3 untuk berkas video lokal, tersedia beberapa mode pencampuran:

- **AD Standar (Campur Suara):** Narasi dicampurkan langsung dengan audio video. Anda akan ditanya apakah ingin menerapkan **Peredaman Audio** (menurunkan volume latar belakang selama deskripsi) agar narasi terdengar jelas.
- **AD Diperpanjang (Jeda Audio):** Mesin menjeda audio asli video selama deskripsi, sehingga Anda tidak melewatkan satu kata pun dari dialog asli atau narasi AI. Deteksi keheningan kini menggunakan model neural **Silero VAD** (diunduh otomatis saat pertama kali digunakan, seperti ffmpeg dan eSpeak) untuk menentukan waktu jeda secara akurat — membedakan jeda dialog alami dari musik dan derau latar belakang.
- **Video YouTube:** Untuk sumber YouTube (yang tidak diunduh secara lokal), ekspor MP3 hanya berisi trek suara AI yang tersinkron tanpa audio latar belakang video.

## 7. Transkripsi dan Sulih Suara Media (M)

Pentranskripsi Audio telah dibangun ulang sepenuhnya untuk mendukung berkas audio maupun video (MP3, WAV, MP4, MKV, dan lainnya). Tekan **M** pada Lapisan Perintah untuk memilih berkas media dan salah satu dari 3 mode operasi:

1. **Transkripsikan (Bahasa Asli):** Mentranskripsikan ucapan secara akurat dalam bahasa aslinya.
2. **Transkripsikan dan Terjemahkan (Bahasa Target):** Mentranskripsikan ucapan lalu menerjemahkannya ke bahasa target yang telah Anda atur.
3. **Sulih Suara dan Terjemahkan (Bahasa Target)** _(Khusus Gemini):_ Mentranskripsikan ucapan, menerjemahkannya ke bahasa target, lalu membuat sulih suara dengan mesin TTS add-on.

## 8) Pembaca Dokumen & Gambar Lanjutan

**Pembaca Dokumen** mengubah dokumen menjadi teks yang rapi dan mudah dibaca — agar Anda dapat membaca, menerjemahkan, dan mendengarkan berbagai bahan, mulai dari buku hasil pemindaian hingga kumpulan foto. Fitur ini menangani PDF multihalaman, gambar kompleks, format HEIC iPhone, bahkan berkas teks biasa (`.txt`) dan HTML (`.html`, `.htm`) yang dapat langsung dibuka tanpa pemrosesan OCR atau AI. Pilih beberapa berkas sekaligus untuk menggabungkannya menjadi satu dokumen berkelanjutan sesuai urutan halaman. Tersedia tiga mesin OCR — **Chrome (Cepat)**, **AI (Lanjutan)** untuk mempertahankan tata letak dengan lebih baik, dan **Tanpa OCR (Ekstrak Lapisan Teks)** untuk PDF yang dapat ditelusuri — yang dapat dipilih di Pengaturan → Pembaca Dokumen.

### Cara Kerja

1. Tekan **NVDA + Shift + V**, lalu **D** untuk membuka Pembaca Dokumen — atau sorot berkas di File Explorer terlebih dahulu, lalu tekan **D** / **F** untuk melewati dialog berkas.
2. Pilih satu atau beberapa PDF atau gambar. Add-on memindainya dan mengumumkan jumlah seluruh halaman.
3. Pada dialog **Opsi**, pilih rentang halaman (Dari/Sampai). Anda juga dapat mencentang **Terjemahkan Keluaran** dan memilih bahasa tujuan, mengaktifkan **Deskripsikan gambar dalam teks selama OCR**, atau mengaktifkan **Kompres halaman PDF sebelum diproses** untuk memperkecil dan mengompres ulang halaman hasil pemindaian yang terlalu besar sebelum diunggah.
4. Ekstraksi teks dimulai di latar belakang secara bertahap. Anda dapat menutup jendela kapan saja dan melanjutkannya nanti — tidak ada data yang hilang.
5. Setelah halaman siap, baca di penampil: berpindah antarhalaman, lompat ke halaman tertentu, ajukan pertanyaan kepada AI, simpan teks, atau buat narasi audio.

### 7.1 Pemrosesan Batch & Melanjutkan

Anda tidak perlu membaca dokumen besar sekaligus. Masukkan rentang halaman (misalnya, `1-20`), dan AI akan memproses semua halaman di latar belakang. Jika NVDA crash atau Anda menghentikan pemindaian, add-on akan mengingat progres Anda dan menawarkan untuk **Melanjutkan (Resume)** tepat di tempat Anda berhenti! Pilih rentang halaman (misalnya `1-20`) atau gunakan pilihan bawaan untuk memproses semuanya, dan AI akan mengekstrak seluruh halaman di latar belakang. Jika NVDA berhenti mendadak atau pemindaian Anda hentikan, add-on mengingat progresnya dan menawarkan untuk **Melanjutkan** tepat dari titik terakhir — bahkan setelah NVDA dimulai ulang. Dokumen yang telah selesai juga disimpan dalam cache, sehingga saat dibuka kembali (dari Dokumen Terbaru atau melalui **D**), teks langsung dimuat tanpa menjalankan OCR lagi, kecuali berkas sumber telah berubah.

### 7.2 Tindakan File Cerdas

Anda tidak selalu harus membuka dokumen terlebih dahulu. Di Windows File Explorer, cukup sorot PDF atau gambar dan tekan **D** (Pembaca Dokumen) atau **F** (Tindakan File Cerdas) di dalam Lapisan Perintah. Add-on akan langsung melewati dialog file dan mulai memproses file yang disorot. Di Windows File Explorer, cukup sorot berkas PDF, gambar, atau teks/HTML lalu tekan **D** (Pembaca Dokumen) — atau sorot PDF atau gambar lalu tekan **F** (Tindakan Berkas Cerdas) — dalam Lapisan Perintah. Add-on langsung melewati dialog berkas dan mulai memproses berkas yang disorot. Jika Anda memilih beberapa berkas sekaligus, semuanya diproses bersama sebagai satu dokumen.

### 7.3 Kontrol & Pintasan Penampil Dokumen

Saat jendela Pembaca Dokumen terbuka, Anda dapat menggunakan hal berikut:

#### Pintasan Keyboard

- **Ctrl + PageDown / Ctrl + PageUp:** Pindah ke halaman berikutnya / sebelumnya.
- **Panah Bawah / Atas:** Ketika kursor Anda mencapai baris terakhir dari suatu halaman, tekan **Panah Bawah** untuk melompat ke halaman berikutnya; tekan **Panah Atas** di bagian paling atas halaman untuk kembali ke halaman sebelumnya.
- **Alt + A:** Buka dialog obrolan untuk mengajukan pertanyaan tentang dokumen.
- **Alt + R:** Paksa **Pindai ulang dengan AI** menggunakan penyedia aktif Anda.
- **Alt + G:** Hasilkan dan simpan file audio berkualitas tinggi (WAV/MP3). _(Disembunyikan jika penyedia tidak mendukung TTS)._ **Alt + S / Ctrl + S:** Simpan teks hasil ekstraksi sebagai file TXT atau HTML.
- **Alt + S / Ctrl + S:** Menyimpan teks hasil ekstraksi sebagai berkas TXT atau HTML.

#### Tombol & Kontrol

- **Ke halaman:** Memilih halaman apa pun dari pemilih halaman.
- **Lihat Terformat:** Menampilkan seluruh dokumen sebagai teks terformat yang digabungkan.
- **Coba Lagi Halaman yang Gagal:** Mengulangi hanya kelompok halaman yang gagal akibat kesalahan server sementara (misalnya permintaan tinggi). Tombol ini muncul otomatis saat diperlukan.
- **Suara TTS / Mesin TTS:** Memilih suara, dan pada Gemini, memilih antara **TTS Standar** dan streaming **Gemini Live**.
- **Sebelumnya / Berikutnya:** Berpindah antarhalaman (sama seperti pintasan Ctrl+PageUp/Down).

### 7.4 Dokumen Terbaru (D)

Menekan **D** pada Lapisan Perintah akan menampilkan daftar dokumen yang baru dibaca terlebih dahulu. Pilih dokumen untuk melanjutkan dari halaman terakhir — bahkan jika OCR sudah selesai — atau tekan **Buka Berkas...** (`Ctrl + O`) untuk memilih berkas seperti biasa.

## 9. Pelabelan AI Semantik & UI Explorer

Kesulitan menggunakan aplikasi yang penuh dengan "tombol tanpa label"? Mesin Pelabelan AI Semantik mengatasi masalah ini secara permanen.

### 8.1 Pelabelan Objek Permanen (L)

Fokuskan pembaca layar Anda pada grafik atau tombol tanpa label dan tekan **L** di Lapisan Perintah. AI akan melihat tombol tersebut secara visual, menentukan fungsinya, dan menerapkan label permanen. AI akan melihat tombol secara visual, menentukan fungsinya, dan memberinya label permanen.
_Berbeda dari alat pelabelan pembaca layar sebelumnya, add-on ini menggunakan sistem hibrida "Object Signature" yang canggih (AutomationId/ControlID). Label kustom Anda tetap bertahan meskipun ukuran jendela berubah, monitor berpindah, atau aplikasi diperbarui!_

### 8.2 Pemindaian Aplikasi Penuh (Shift + L)

Tekan **Shift + L** untuk memindai seluruh jendela aktif sekaligus. AI akan menemukan semua elemen tanpa label dan menamainya secara cerdas sekaligus. Anda nantinya dapat mengelola, mengganti nama, atau menghapus label ini secara massal dari Pengelola Label bawaan. AI akan menemukan semua elemen tanpa label dan memberi nama yang sesuai sekaligus. Anda dapat mengelola, mengganti nama, atau menghapus banyak label sekaligus melalui Pengelola Label bawaan.

### 8.3 UI Explorer (E)

Perlu berinteraksi dengan suatu elemen tanpa mencarinya secara manual? Tekan **E** untuk mengaktifkan UI Explorer. AI akan memindai layar dan menghasilkan daftar yang aksesibel dari setiap elemen yang dapat diklik (mengabaikan gangguan sistem seperti taskbar). Pilih item dari daftar, dan add-on akan langsung mengkliknya untuk Anda. Tekan **E** untuk mengaktifkan Penjelajah Antarmuka. AI akan memindai layar dan membuat daftar aksesibel berisi setiap elemen yang dapat diklik (dengan mengabaikan elemen sistem yang tidak relevan seperti bilah tugas). Pilih item dari daftar, dan add-on akan langsung mengekliknya untuk Anda.

## 10. Asisten Suara Langsung

_(Catatan: Fitur ini eksklusif untuk Google Gemini dan penyedia Kustom yang kompatibel dengan Gemini)._
**Aktivasi:** Tekan **Control + L** di Lapisan Perintah untuk membuka dialog Asisten Langsung.

- **Interaksi Real-time:** Bicaralah secara alami melalui mikrofon Anda. AI akan mendengarkan suara Anda dan melihat layar aktif Anda secara bersamaan. Anda dapat mengajukan pertanyaan seperti "Apa yang sedang saya lihat?" atau "Bacakan paragraf ketiga untuk saya."
- **Kustomisasi:** Di dalam dialog, Anda dapat mengubah Gaya Suara AI (misalnya, Profesional, Ramah, Ceria) dan menyesuaikan "Kedalaman Berpikir" (Thinking Depth) untuk mengontrol seberapa mendalam analisisnya sebelum menjawab. AI akan mendengarkan suara Anda sekaligus melihat layar yang sedang aktif. Anda dapat bertanya, misalnya "Apa yang sedang saya lihat?" atau "Bacakan paragraf ketiga untuk saya."
- **Tekan untuk Bicara:** Aktifkan **Tekan untuk Bicara** pada tab pengaturan Asisten Langsung (atau langsung dari jendela Asisten Langsung), lalu tahan tombol yang ditetapkan untuk berbicara dan lepaskan untuk selesai. Dengan begitu, mikrofon tetap dibisukan hingga Anda menekan tombol — cocok untuk lingkungan yang bising.
- **Masukan Kamera Web:** Centang **Gunakan &Kamera Web** di jendela Asisten Langsung untuk mengirim tayangan kamera ke AI sebagai pengganti layar — Anda dapat bertanya tentang objek fisik, dokumen cetak, atau keadaan sekitar. Jika ffmpeg belum terpasang, mencentang kotak ini akan mengunduhnya sekali dengan izin Anda; opsi dinonaktifkan jika tidak ada kamera yang terdeteksi atau pengaturan privasi Windows memblokir akses kamera.
- **Penyesuaian:** Di dalam dialog, Anda dapat mengubah Gaya Suara AI (misalnya Profesional, Ramah, Bersemangat) dan mengatur "Kedalaman Berpikir" untuk menentukan seberapa mendalam AI menalar sebelum menjawab.

## 11. Pengamat Lingkungan (Asisten Latar Belakang)

Pengamat Lingkungan menjadikan Vision Assistant Pro sebagai mata Anda di latar belakang tanpa perlu percakapan: fitur ini terus mendengarkan dan mengamati saat Anda bekerja, melaporkan perubahan, dan tetap diam saat tidak ada aktivitas.
_(Catatan: Fitur ini khusus untuk Google Gemini dan penyedia Kustom yang kompatibel dengan Gemini)._

- **Mengaktifkan:** Tekan **Shift+O** pada Lapisan Perintah untuk membuka dialog Pengamat Lingkungan; tekan lagi untuk menghentikan pengamat.
- **Mode:** **Hanya Terjemahan Audio** menerjemahkan suara yang terdengar, **Hanya Pemantau Layar** melaporkan perubahan layar, dan **Hanya Pemantau Kamera Web** membuka jendela Asisten Langsung dengan kamera serta Tekan untuk Bicara agar Anda dapat bertanya tentang apa yang dilihat kamera.
- **Sumber Audio:** Dalam mode audio, pilih apakah akan menerjemahkan suara dari **Mikrofon** atau **Audio Sistem (Loopback)**. Pustaka loopback berukuran kecil diunduh sekali saat pertama digunakan, dengan izin Anda.
- **Konteks:** Untuk mode layar dan kamera web, Anda dapat memilih opsi **Tentang kegiatan saya** (misalnya menonton film, mengikuti rapat atau panggilan, membaca label, atau memeriksa penampilan) agar laporan lebih terarah; Anda juga dapat mengetik konteks sendiri.
- **Pelaporan:** Add-on membandingkan setiap bingkai baru dengan bingkai sebelumnya dan hanya mengirimnya ke AI jika gambar benar-benar berubah, sehingga layar yang diam tidak menghabiskan permintaan. AI kemudian hanya melaporkan hal baru tanpa mengulang informasi.
- **Pesan Sambutan:** Kecuali dalam mode terjemahan, pengamat akan menyapa singkat saat dimulai agar Anda tahu bahwa fitur ini sedang mendengarkan.
- **Pengaturan:** Di **Pengaturan > Asisten Langsung**, atur **Mode Pengamat**, **Interval Bingkai** (1 hingga 10 detik), dan **Gaya Pelaporan** (ringkas atau terperinci). Instruksi pengamat dan setiap teks konteks dapat diedit di Pengelola Prompt (bagian **Lingkungan**).

## 12. Prompt Kustom & Variabel

Anda dapat mengelola prompt di **Pengaturan > Prompt > Kelola Prompt...**.

- **Filter:** Tab **Prompt Bawaan** memiliki daftar **Filter** di atas daftar prompt untuk menampilkan **Semua** prompt atau satu bagian saja (misalnya **Lingkungan**), sehingga daftar panjang tetap mudah ditelusuri.

### Pintasan Prompt Kustom

Tetapkan tombol pintasan khusus untuk setiap prompt kustom langsung di Pengelola Prompt, lalu jalankan seketika dengan pilihan atau konteks saat ini:

- **Tombol tunggal** (misalnya `1`, `p`, atau `F3`): Berfungsi dalam Lapisan Perintah, dan juga secara global sebagai `NVDA + Shift + key`.
- **Kombinasi tombol** (misalnya `Control + Shift + 1`, `Alt + P`, atau `Insert + 1`): Dapat langsung dijalankan secara global.

### Variabel yang Didukung

Setiap prompt kustom dapat menentukan cara penyampaian keluarannya sendiri:

- **Pengaturan global:** Mengikuti pengaturan keluaran umum pada tab Koneksi (Keluaran Langsung atau Jendela percakapan).
- **Salin ke papan klip:** Menyalin respons AI langsung ke papan klip tanpa membuka jendela.
- **Keluaran Langsung (pesan NVDA):** Menyampaikan respons AI secara langsung melalui ucapan atau braille NVDA.
- **Salin ke papan klip dan Keluaran Langsung:** Menyalin respons ke papan klip dan langsung membacakannya.
- **Jendela percakapan:** Selalu membuka hasil dalam jendela percakapan interaktif.

### Variabel yang Didukung

- `[selection]`: Teks yang dipilih saat ini.
- `[clipboard]`: Konten papan klip.
- `[clipboard_image]`: Gambar di papan klip saat ini.
- `[screen_obj]`: Tangkapan layar dari objek navigator.
- `[screen_fg_obj]`: Tangkapan layar jendela aktif di latar depan.
- `[screen_full]`: Tangkapan layar seluruh layar.
- `[file_ocr]`: Pilih file gambar/PDF untuk ekstraksi teks.
- `[file_read]`: Pilih dokumen untuk dibaca (TXT, Kode, PDF).
- `[file_audio]`: Pilih file audio untuk analisis (MP3, WAV, OGG).
- `{target_lang}`: Bahasa target saat ini.
- `[file_audio]`: Memilih berkas audio untuk dianalisis (MP3, WAV, OGG).
- `[ambient_screen]`: Memulai sesi Pengamat Layar secara terus-menerus di latar belakang.
- `[ambient_webcam]`: Memulai sesi Pengamat Kamera Web secara terus-menerus di latar belakang (memeriksa opsi Tekan untuk Bicara dari pengaturan).
- `[ambient_audio]`: Memulai sesi terjemahan langsung Pengamat Audio.
- `[loopback]`: Menggunakan audio yang diputar sistem sebagai sumber suara (untuk `[ambient_audio]`).
- `[mic]`: Menggunakan mikrofon sebagai sumber suara (untuk `[ambient_audio]` dan `[ambient_webcam]`).
- `[brief]`: Mengatur gaya pelaporan pengamat menjadi ringkas (satu kalimat).
- `[detailed]`: Mengatur gaya pelaporan pengamat menjadi terperinci (2-3 kalimat).
- `[lang:code]`: Menentukan kode bahasa tujuan untuk terjemahan audio (misalnya `[lang:fa]`, `[lang:en]`).
- `{target_lang}`: Bahasa tujuan saat ini.
- `{source_lang}`: Bahasa sumber saat ini.
- `{response_lang}`: Bahasa respons AI saat ini.
- `{swap_target}`: Bahasa alternatif untuk terjemahan pertukaran cerdas.
- `{swap_instruction}`: Blok instruksi terjemahan pertukaran cerdas.

_Catatan tentang Prompt Lingkungan:_ Prompt yang memuat variabel lingkungan berfungsi sebagai sakelar — menekan pintasan saat sesi aktif akan langsung menghentikannya. Kombinasi yang tidak kompatibel (seperti menggabungkan variabel tangkapan layar statis seperti `[screen_full]` dengan mode pengamat lingkungan, menggabungkan beberapa mode lingkungan, atau menambahkan instruksi prompt ke `[ambient_audio]`) diperiksa secara ketat dan dicegah saat disimpan.

## 13. Contoh Penggunaan Sehari-hari (Fitur mana yang sebaiknya digunakan?)

Vision Assistant Pro dilengkapi berbagai alat canggih. Berikut beberapa situasi umum untuk membantu Anda memilih fitur yang tepat:

- **Skenario: Anda ingin memahami tata letak lengkap dari jendela yang rumit atau aplikasi yang tidak aksesibel.** _Solusi:_ Tekan **O** (Visi Layar Penuh). AI akan menganalisis seluruh layar dan mendeskripsikan secara tepat di mana elemen, teks, dan tombol diposisikan.

- **Skenario: Anda menemukan gambar di halaman web atau grafik tanpa label di dokumen.** _Solusi:_ Pindahkan objek navigator Anda ke grafik tersebut dan tekan **V** (Visi Objek). AI akan mendeskripsikan secara spesifik apa isi gambar tersebut.

- **Skenario: Anda ingin menonton film atau klip video dengan deskripsi audio.** _Solusi:_ Tekan **Shift + V** pada video Anda dan pilih **"Buat Deskripsi Audio (File SRT)"**. Setelah selesai, klik **"Buat Narasi Tersinkron (MP3)"** dan pilih **"AD Diperpanjang"**. Add-on akan membuat trek audio yang menjeda dialog film secara cerdas untuk mendeskripsikan adegan visual. Add-on akan membuat trek audio yang menjeda dialog film secara cerdas untuk mendeskripsikan adegan visual.

- **Skenario: Anda menemukan aplikasi yang penuh dengan "tombol tanpa label".** _Solusi:_ Tekan **L** untuk memberi label pada tombol tertentu menggunakan AI secara permanen. Atau, tekan **Shift + L** untuk memindai dan memberi label pada seluruh jendela sekaligus. Jika Anda hanya ingin mengklik sesuatu dengan cepat, tekan **E** (UI Explorer) untuk mendapatkan daftar semua item yang dapat diklik. Jika hanya ingin mengeklik sesuatu dengan cepat, tekan **E** (Penjelajah Antarmuka) untuk mendapatkan daftar semua item yang dapat diklik.

- **Skenario: Anda perlu melewati CAPTCHA yang tidak aksesibel.** _Solusi:_ Tekan **C** (Pemecah CAPTCHA). AI akan secara otomatis menangkap CAPTCHA, memecahkannya, dan memasukkan jawabannya ke kolom yang benar.

- **Skenario: Anda ingin membaca dokumen PDF panjang sebanyak 50 halaman.** _Solusi:_ Tekan **D** (Pembaca Dokumen), atur penyedia Anda ke Google Gemini, dan masukkan rentang halaman `1-50`. Add-on akan mengekstrak teks secara akurat di latar belakang.

- **Skenario: Anda sedang menonton tutorial video tanpa suara atau animasi di layar Anda.** _Solusi:_ Tekan **Control + V** untuk mulai merekam layar. Biarkan tutorial berjalan, lalu tekan **Control + V** lagi. AI akan menjelaskan dengan tepat apa yang didemonstrasikan. AI akan menjelaskan secara tepat apa yang diperagakan.

- **Skenario: Anda menemukan error tak terduga, kegagalan koneksi API, atau ingin mendiagnosis masalah pada server lokal kustom.** _Solusi:_ Buka **Pengaturan > Lanjutan**, centang **"Aktifkan file log khusus"**, lalu atur **Tingkat Log** ke **"Debug"**. Ulangi tindakan yang bermasalah, kemudian pilih **"Buka File Log"** untuk memeriksa detail teknis atau melampirkan `vision_assistant.log` pada laporan dukungan.

***

**Catatan:** Semua fitur AI memerlukan koneksi internet aktif. Dokumen multihalaman diproses secara otomatis.

## 14. Dukungan & Komunitas

Ikuti berita, fitur, dan rilis terbaru:

- **Kanal Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Untuk laporan bug dan permintaan fitur.

### Perubahan untuk 2026.07.15

Saat membuat issue di GitHub atau meminta dukungan, sertakan informasi tentang penyedia AI yang aktif, model, dan versi NVDA Anda. Jika mengalami masalah koneksi atau aplikasi berhenti mendadak, aktifkan berkas log khusus di **Pengaturan > Lanjutan**, ulangi langkah yang memicu masalah, lalu lampirkan berkas `vision_assistant.log` agar kami dapat mengatasinya lebih cepat.

## 15. Pendukung Proyek

Terima kasih sebesar-besarnya kepada anggota komunitas yang mendukung pengembangan dan pemeliharaan proyek ini melalui kontribusi finansial yang murah hati:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**
- **leonardo0216**
- **Sergei Fleytin**
- **Arne Siebert**
- **Schalkefan**
- **Rainer Brell**
- **[avalai.org](https://avalai.org)**

_Jika ingin mendukung proyek secara finansial dan melihat nama Anda di sini, gunakan opsi **Donasi** pada menu Alat NVDA (submenu Vision Assistant) atau saat proses pengaturan setelah instalasi._

---

## Perubahan pada 2026.10.15

- **Perbaikan yang Paling Banyak Diminta — Membuat Kunci API Gemini Kini Mudah**: Mendapatkan kunci API di **aistudio.google.com** sebelumnya merupakan langkah tersulit. Halamannya membingungkan saat diakses dengan pembaca layar, dan sebagian orang bahkan tidak dapat membuat kunci sama sekali. Masalah tersebut kini diselesaikan langsung di dalam add-on. Tekan **G** pada Lapisan Perintah (atau gunakan **Dapatkan Kunci API Gemini...** di Pengaturan), masuk melalui browser bawaan tanpa pengaturan eksternal, dan kunci Anda akan dibuat serta dikonfigurasi dengan satu konfirmasi — bahkan jika Anda belum pernah memiliki proyek.
- **Pengamat Lingkungan**: Asisten latar belakang kini hadir. Tekan **Shift+O** pada Lapisan Perintah untuk memulainya, lalu tekan lagi untuk menghentikannya. Asisten ini dapat menerjemahkan suara yang didengarnya (dari mikrofon atau audio sistem), memantau layar dan memberi tahu perubahan yang terjadi, atau membuka Asisten Langsung dengan kamera web dan Tekan untuk Bicara agar Anda dapat bertanya tentang apa pun yang dilihat kamera. Gambar hanya dikirim ketika benar-benar ada perubahan, sehingga layar yang diam tidak menghabiskan biaya, dan asisten tetap diam saat tidak ada aktivitas. Anda juga dapat menjalankan serta mengaktifkan atau menonaktifkan pengamat langsung melalui Prompt Kustom dan pintasan khusus menggunakan `[ambient_screen]`, `[ambient_webcam]`, atau `[ambient_audio]` bersama pengubah (`[loopback]`, `[mic]`, `[brief]`, `[detailed]`, `[lang:code]`), dengan validasi otomatis untuk kombinasi variabel yang saling bertentangan.
- **Operator Langsung**: Asisten Langsung kini dapat melaksanakan permintaan Anda di komputer sambil Anda berbicara dengannya. Tekan **Control+A** pada Lapisan Perintah untuk memulai sesi operator langsung, lalu sampaikan permintaan dengan bahasa sehari-hari. Operator menangani permintaan bertahap, mengucapkan setiap langkah dengan suara Asisten Langsung, menjalankan kombinasi tombol yang diperlukan, dan menentukan sendiri kapan tugas selesai. **Keluaran Langsung Mode Langsung (Tanpa Jendela)** juga tersedia di Pengaturan Cepat.
- **Kamus Karakter & Pengelolaan Serial**: Dialog Analisis Video kini menyertakan sistem **Kamus Karakter** yang andal! Tambahkan, edit, impor, atau kelola nama karakter, deskripsi fisik, dan peran per serial — AI secara otomatis mencocokkan karakter yang ditemukan dengan kamus Anda dan menggabungkan karakter baru saat Anda menganalisis lebih banyak episode. Catatan manual Anda selalu dipertahankan dan diutamakan dibandingkan pembaruan AI, sementara deskripsi fisik terus diperbarui antarepisode. Kamus disimpan per serial dan digunakan kembali untuk setiap video dalam serial tersebut. Pada daftar karakter, tekan **F2** untuk mengedit karakter terpilih dan **Delete** untuk menghapusnya.
- **Dukungan SOCKS5, HTTP, dan Proksi Balik dengan Pengujian Latensi**: Atasi pembatasan jaringan dengan dukungan proksi lengkap di seluruh add-on — termasuk Asisten Langsung, Pengamat Lingkungan, dan pembuatan TTS! Pilih salah satu dari 4 mode operasi di pengaturan Umum: **Deteksi otomatis**, **Proksi SOCKS5**, **Proksi HTTP**, atau **Proksi Balik**. SOCKS5 mendukung autentikasi nama pengguna/kata sandi RFC 1929 dan tunneling domain; proksi HTTP mendukung autentikasi Basic. Tombol **Uji Koneksi Proksi** yang baru bekerja di latar belakang dan mengumumkan latensi koneksi Anda dalam milidetik.
- **Cache Berkas Video Selama 48 Jam**: Video yang diunggah ke Gemini kini disimpan dalam cache selama 48 jam! Anda dapat membuat ulang keluaran SRT atau MP3 untuk video yang sama tanpa mengunggahnya kembali — bahkan setelah NVDA dimulai ulang. Cache mengenali kunci API yang digunakan dan otomatis tidak berlaku lagi saat kunci API Anda berubah.
- **Deteksi Keheningan Berbasis AI (Silero VAD)**: AD Diperpanjang kini menggunakan model neural Silero VAD untuk mendeteksi keheningan secara akurat — membedakan jeda dialog alami dari musik dan derau latar belakang. Model diunduh secara otomatis saat pertama kali digunakan (dengan izin Anda), seperti ffmpeg dan eSpeak.
- **Video Kamera Web untuk Asisten Langsung**: Jendela Asisten Langsung kini memiliki kotak centang **Gunakan &Kamera Web** untuk mengirim tayangan kamera web ke AI sebagai pengganti layar — cocok untuk bertanya tentang objek fisik, dokumen, atau keadaan sekitar. Jika ffmpeg belum terpasang, mencentang kotak ini akan mengunduhnya (sekali saja, dengan izin Anda). Opsi dinonaktifkan ketika tidak ada kamera yang terdeteksi atau pengaturan privasi Windows memblokir akses kamera, dengan tombol untuk membuka pengaturan privasi kamera. Jika kamera diaktifkan tetapi tidak menghasilkan bingkai, masalah tersebut dicatat dalam log NVDA untuk diagnosis, alih-alih diam-diam beralih kembali ke layar.
- **Pemilihan Perangkat Keluaran Audio**: Anda kini dapat memilih perangkat keluaran audio khusus untuk Asisten Langsung dan Pengamat Lingkungan. Pilih keluaran bawaan NVDA, Windows Sound Mapper, atau kartu suara fisik yang terhubung (seperti headphone USB atau pengeras suara eksternal) pada tab Pengaturan Mode Langsung, langsung dalam dialog Asisten Langsung, atau kapan saja melalui Pengaturan Cepat (NVDA+Shift+V lalu Up/Down/Left/Right).
- **Pengelola Prompt**: Tab Prompt Bawaan kini memiliki daftar **Filter**, sehingga Anda dapat menampilkan semua prompt atau hanya satu bagian (misalnya **Lingkungan**). Anda juga dapat mengedit teks konteks pengamat dan **Instruksi Operator Langsung** yang baru di sana.
- **Penyaringan Model Cerdas pada Perutean Lanjutan**: Daftar pilihan Perutean Model Lanjutan kini mengelompokkan model Gemini secara dinamis berdasarkan kemampuan agar tetap rapi. Asisten Langsung hanya menampilkan model langsung dua arah dan audio native yang sesungguhnya, TTS hanya menampilkan model khusus sintesis ucapan, STT memprioritaskan model Transcribe dan multimodal, sedangkan Analisis Video, OCR, dan Operator AI menyaring model utilitas untuk satu tujuan saja (seperti model pembuatan gambar, pembuatan video, dan embedding). Model mendatang dideteksi secara otomatis berdasarkan kemampuan tanpa memerlukan pembaruan versi.
- **Pelacakan Kemunculan Pertama Karakter**: AI kini mendeskripsikan penampilan fisik setiap karakter hanya sekali — pada kemunculan pertamanya dalam video. Kemunculan berikutnya hanya menggunakan nama, menghilangkan deskripsi berulang antarsegmen sekaligus menjaga narasi tetap segar dan alami.
- **Direktori Data Terpadu**: Semua berkas data add-on (riwayat, serial, label, progres OCR, cache, dan log) telah dipindahkan ke satu folder `VisionAssistant` di dalam direktori konfigurasi NVDA Anda — agar semuanya tertata dan pencadangan manual menjadi mudah.
- **Penyimpanan Video yang Lebih Baik**: Saat menyimpan berkas SRT atau MP3, dialog berkas kini secara bawaan terbuka di folder video sumber, baik ketika video dibuka melalui dialog berkas maupun dengan Shift+V dari Explorer.
- **Menghapus Dokumen Dengan atau Tanpa Teks dalam Cache**: Dialog Riwayat (`Control + H`) kini menawarkan dua cara untuk menghapus dokumen — tekan Delete dan pilih **Hapus hanya dari riwayat** atau **Hapus dari riwayat dan teks dalam cache**. Opsi kedua menghapus teks OCR dokumen tersebut dari cache, sehingga saat dibuka kembali dokumen dipindai ulang dari awal — berguna setelah hasil pemindaian yang buruk. Kotak centang **Jangan tanya lagi** mengingat pilihan Anda untuk penghapusan berikutnya. Data untuk melanjutkan operasi yang terputus tidak pernah diubah.
- **Cache OCR per Mesin yang Digabungkan dalam Pembaca Dokumen**: Teks OCR dalam cache kini disimpan per mesin OCR, sehingga pergantian mesin OCR selalu memindai ulang dengan mesin baru alih-alih menampilkan hasil lama. Membuka kembali dokumen akan menampilkan lagi dialog rentang halaman (terisi dengan pilihan terakhir Anda), langsung menggunakan kembali halaman yang sudah dipindai dan hanya memindai halaman yang belum tersedia — cache digabungkan halaman demi halaman, bukan diganti, sehingga setiap rentang yang Anda baca disimpan untuk digunakan nanti.
- **Kompresi PDF dalam Pembaca Dokumen**: Menambahkan pengaturan opsional **Kompres halaman PDF sebelum diproses** pada dialog rentang halaman Pembaca Dokumen. Saat mengunggah dokumen PDF hasil pemindaian berukuran besar atau beresolusi tinggi ke Gemini atau Mistral, halaman secara otomatis diperkecil dan dikompres ulang untuk mengurangi ukuran data unggahan secara signifikan, mempercepat pemrosesan, serta mencegah habisnya waktu tunggu jaringan. Opsi ini dinonaktifkan secara bawaan dan otomatis disembunyikan saat menggunakan mesin Chrome atau penyedia gambar berbasis base64.
- **Penyesuaian Perilaku Umpan Balik per Prompt**: Sesuaikan cara setiap prompt kustom menyampaikan keluarannya secara terpisah! Di editor prompt kustom, pilih **Pengaturan global**, **Salin ke papan klip**, **Keluaran Langsung (pesan NVDA)**, **Salin ke papan klip dan Keluaran Langsung**, atau **Jendela percakapan**. Dengan demikian, prompt tertentu dapat berbicara langsung tanpa membuka jendela, sementara prompt lainnya membuka percakapan lengkap.
- **Variabel Prompt Dinamis Baru (`[currentURL]` & `[text]`)**: Prompt Kustom kini mendukung `[currentURL]` untuk mengambil URL dokumen aktif di Google Chrome, Mozilla Firefox, dan Microsoft Edge, serta `[text]` untuk menyisipkan secara dinamis seluruh isi teks dari bidang edit yang sedang difokuskan (dengan mengabaikan kotak kata sandi yang dilindungi).
- **Perombakan Pengunduh Video Twitter/X**: Memulihkan pengunduhan dan analisis video Twitter/X setelah kegagalan scraper pada layanan hulu. Ekstraksi video kini menggunakan API FixTweet yang andal untuk mengambil aliran MP4 berkualitas tertinggi langsung dari CDN Twitter, lengkap dengan peralihan otomatis ke TwitSave sebagai alternatif dan dukungan proksi.
- **Perbaikan Pengunduh Video Instagram**: Memulihkan pengunduhan dan analisis Instagram Reels serta URL video setelah perubahan formulir pada layanan pengunduh.
- **Perbaikan & Kinerja**: Tekan untuk Bicara merespons begitu Anda menekan tombol, Asisten Langsung tidak lagi mulai menjawab di tengah kalimat, pengamat tidak lagi melaporkan gambar sebelumnya, dan daftar Kedalaman Berpikir hanya menawarkan pilihan yang benar-benar didukung model Anda. Operator AI juga dapat menggulir ke kiri dan kanan. Memperbaiki `AttributeError` saat menganalisis video daring, dan mencegah prompt kustom tanpa teks terpilih menyisipkan judul jendela latar belakang secara tidak sengaja ke dalam permintaan AI.

## Perubahan pada 2026.09.01

- **Riwayat (Control + H)**: Lapisan Perintah kini memiliki dialog **Riwayat** (`Control + H`) yang menampilkan percakapan dan dokumen sebelumnya, dengan filter Semua, Percakapan, dan Dokumen. Buka kembali percakapan beserta seluruh isinya — berkas lampiran dilampirkan ulang secara otomatis — atau buka kembali dokumen untuk melanjutkan membaca. Tekan **Delete** pada item untuk menghapusnya, atau hapus semuanya sekaligus.
- **Dokumen Terbaru dalam Pembaca**: Menekan **D** pada Lapisan Perintah kini menampilkan dokumen yang baru dibaca terlebih dahulu. Pilih dokumen untuk melanjutkan dari halaman terakhir — bahkan jika OCR sudah selesai — atau tekan **Buka Berkas...** (`Ctrl + O`) untuk memilih berkas seperti biasa.
- **Tekan untuk Bicara pada Asisten Langsung**: Kendalikan sepenuhnya percakapan langsung Anda! Aktifkan **Tekan untuk Bicara** pada tab pengaturan Asisten Langsung yang baru dan tetapkan tombol apa pun — bahkan satu tombol pengubah seperti `Left Ctrl` — untuk berbicara. Tahan tombol untuk berbicara dan lepaskan saat selesai. Bunyi bip singkat akan terdengar setiap kali tombol ditekan atau dilepas. Sakelar yang sama juga tersedia langsung di jendela Asisten Langsung, sehingga Anda dapat beralih antara mode tekan untuk bicara dan mikrofon terbuka tanpa meninggalkan percakapan.
- **Gemini 2.5 Flash Native Audio**: Asisten Langsung kini mendukung model audio native Gemini 2.5 Flash (`gemini-2.5-flash-native-audio-preview-12-2025`) untuk percakapan suara alami dengan latensi rendah. Anda dapat beralih ke model tersebut melalui **Pengaturan → Perutean Model Lanjutan → Model Asisten Langsung (khusus Gemini)**, atau tetap memilih "Otomatis" untuk menggunakan model yang direkomendasikan.
- **Pencadangan & Pemulihan Pengaturan**: Menambahkan sistem pencadangan dan pemulihan yang andal pada tab **Lanjutan**! Anda kini dapat menyimpan seluruh pengaturan add-on — termasuk kunci API, model, prompt kustom, dan preferensi — ke satu berkas JSON, lalu memulihkannya secara lengkap kapan saja, di komputer mana pun, atau setelah memasang ulang NVDA. Saat mencadangkan, pilih data yang akan disertakan: **Semuanya** (pengaturan, label kustom, progres OCR, dan riwayat) atau **Hanya Pengaturan**.
- **Pembacaan Teks & HTML Langsung**: Pembaca Dokumen kini dapat langsung membuka berkas teks biasa (`.txt`) dan HTML (`.html`, `.htm`)! Fitur ini otomatis mendeteksi pengodean berkas, menghapus skrip serta format yang mengganggu, dan membagi isi menjadi halaman yang mudah dibaca — bahkan dapat mengimpor kembali berkas hasil ekspornya sendiri sambil mempertahankan struktur halaman — sehingga Anda dapat langsung membacanya tanpa pemrosesan OCR atau AI!
- **Gemini Live TTS untuk Pembaca Dokumen**: Tombol "Buat Audio" kini mendukung Gemini Live — mesin teks ke ucapan streaming berkualitas tinggi dengan tempo alami! Saat Gemini menjadi penyedia aktif, Anda dapat memilih TTS Standar atau Gemini Live langsung di pembaca, dan pilihan Anda akan diingat untuk penggunaan berikutnya!
- **Pintasan Prompt Kustom**: Anda kini dapat menetapkan tombol pintasan untuk prompt kustom langsung dari Pengelola Prompt! Berikan tombol atau kombinasi tombol khusus pada setiap prompt agar dapat dijalankan seketika, dengan mengambil pilihan atau konteks saat ini secara otomatis tanpa langkah tambahan!
- **Navigasi Pesan Percakapan**: Tinjau percakapan tanpa perlu menggunakan mouse! Di jendela percakapan mana pun (Percakapan Langsung, percakapan dokumen, penyempurnaan teks, dan lainnya), tekan `Alt + Down` untuk mendengar pesan berikutnya dan `Alt + Up` untuk pesan sebelumnya — dengan awalan "Anda" / "AI" yang jelas serta pengumuman batas "Pesan pertama" / "Pesan terakhir" saat menelusurinya.
- **Salin Pesan Percakapan (Alt + C)**: Saat meninjau percakapan dengan `Alt + Up/Down`, tekan `Alt + C` untuk menyalin pesan saat ini ke papan klip — sesuai pengaturan Bersihkan Markdown — disertai konfirmasi suara.
- **Prompt Sistem Percakapan Langsung**: Percakapan Langsung (`Shift+C`) kini memiliki prompt sistem tersendiri yang dapat diedit — "Instruksi Percakapan Langsung" — untuk menetapkan persona asisten dan bahasa respons pada setiap percakapan. Anda dapat menyesuaikannya dari tab Prompt Bawaan di Pengelola Prompt.
- **Navigasi Halaman dengan Kursor pada Pembaca Dokumen**: Membaca dokumen multihalaman kini semakin lancar! Di Penampil Dokumen, saat kursor mencapai baris terakhir halaman dan Anda menekan `Down`, pembaca otomatis berpindah ke halaman berikutnya. Menekan `Up` di awal halaman akan langsung membawa Anda ke halaman sebelumnya — tidak perlu lagi mengganti halaman secara manual saat membaca!
- **Sakelar Pengaturan Cepat Baru**: Salin respons AI ke papan klip, Keluaran Langsung (tanpa jendela percakapan), Bersihkan Markdown dalam Percakapan, dan Pertukaran Cerdas kini dapat diaktifkan atau dinonaktifkan seketika melalui Pengaturan Cepat pada Lapisan Perintah!
- **Tab Pengaturan Asisten Langsung**: Asisten Langsung kini memiliki tab pengaturan khusus! Opsi "Asisten Langsung: Keluaran Langsung (Tanpa Jendela)" dipindahkan ke sini dari tab Koneksi. Tab ini hanya muncul saat Google Gemini (atau penyedia Kustom yang kompatibel dengan Gemini) menjadi penyedia aktif.

## Perubahan untuk 2026.08.06

- **Pelabelan di UI Explorer**: Kini Anda dapat menambahkan label langsung ke elemen yang ditemukan di UI Explorer. Tombol baru "Tambahkan Label" telah tersedia. Antarmuka tetap terbuka dan mempertahankan fokus, sehingga Anda dapat memberi label pada beberapa objek dengan cepat tanpa gangguan.
- **Peningkatan Lapisan Pengaturan Cepat**: Lapisan Vision Assistant (`Insert+Shift+V`) kini tetap aktif dan sangat interaktif. Gunakan panah `Up/Down` untuk berpindah di antara Pengaturan Cepat (Penyedia, Model, Bahasa Respons AI, Model TTS), dan panah `Left/Right` untuk langsung mengubah nilainya dengan umpan balik suara yang ringkas dan cerdas. Pilihan langsung diterapkan, termasuk mengaktifkan Perutean Model Lanjutan secara otomatis bila diperlukan, dan lapisan tetap aktif selama Anda melakukan konfigurasi.
- **Obrolan Langsung (`Shift+C`)**: Menambahkan perintah baru ke lapisan. Tekan `Shift+C` untuk langsung membuka jendela "Obrolan Langsung". Antarmuka percakapan berbasis teks yang bersih ini memungkinkan Anda langsung mengobrol dengan AI tanpa harus memulai dari gambar atau dokumen.
- **Pemanggilan Riwayat Obrolan yang Andal**: Memperbaiki bug besar yang membuat riwayat obrolan lanjutan hilang ketika `Space` ditekan untuk membuka hasil terakhir. Kini add-on melacak percakapan secara global. Jika Anda mengobrol, menutup dialog, lalu menekan `Space`, seluruh riwayat percakapan dua arah akan dipulihkan dengan sempurna. Fitur ini berlaku untuk Obrolan Langsung, Analisis Visi, Obrolan Dokumen, dan Terjemahan.
- **Deskripsi Gambar dalam Teks OCR**: Menambahkan fitur opsional untuk mendeskripsikan gambar di antara teks selama OCR dokumen. Anda dapat mengubah pengaturan ini di pengaturan OCR add-on, di opsi Pembaca Dokumen sebelum ekstraksi, atau secara cepat melalui lapisan Pengaturan Cepat.
- **Terjemahan Suara (`Control+T`)**: Menambahkan fitur baru yang canggih. Diktekan ucapan untuk langsung menerjemahkan dan mengetik hasilnya dengan AI berdasarkan bahasa sumber dan target yang telah Anda atur.
- **Peningkatan Pengunduh Pembaruan**: Dialog pengunduhan pembaruan kini menampilkan progres dalam persentase dengan benar. Bug yang memunculkan pesan semu "Mengunduh pembaruan" setelah instalasi dibatalkan juga telah diperbaiki.
- **Peningkatan Pengunduh eSpeak-NG**: Menambahkan pelacakan progres dalam persentase untuk unduhan eSpeak-NG.
- **Ketahanan OCR Batch**: Memperbaiki masalah pada OCR PDF batch yang menghentikan proses jika kuota kunci API aktif habis di tengah jalan. Kini add-on otomatis beralih ke kunci berikutnya yang tersedia dan melanjutkan proses.
- **Dukungan CAPTCHA Visual**: Menambahkan dukungan yang andal untuk memecahkan CAPTCHA visual. Add-on mencoba memecahkan tantangan gambar kompleks seperti hCaptcha dan reCAPTCHA secara otomatis, sehingga formulir web yang sulit menjadi jauh lebih aksesibel.
- **Perombakan Transkripsi Audio**: Modul Transkripsi Audio telah dibangun ulang sepenuhnya dan kini mendukung file audio maupun video. Tersedia 3 mode operasi: "Transkripsikan (Bahasa Asli)", "Transkripsikan dan Terjemahkan (Bahasa Target)", serta opsi baru "Sulih Suara dan Terjemahkan (Bahasa Target)" khusus Gemini yang membuat sulih suara terjemahan dari ucapan asli.
- **Nomor Halaman Opsional di Pembaca Dokumen**: Menambahkan pengaturan untuk mengaktifkan atau menonaktifkan nomor dan pemisah halaman pada keluaran dokumen multihalaman. Opsi ini dapat dikelola dari pengaturan utama atau diubah langsung melalui lapisan Pengaturan Cepat. Fitur berlaku untuk ekspor file teks/HTML dan jendela "Tampilkan Terformat", sehingga dokumen gabungan dapat dibaca dengan lancar.
- **Gemini Live TTS Tanpa Batas untuk Deskripsi Video**: Kini Anda dapat memilih "Gemini Live TTS" sebagai mesin suara saat membuat Narasi Audio Tersinkron (MP3) untuk video. Gemini Live API menghasilkan Deskripsi Audio berkualitas tinggi tanpa batas karakter atau durasi.
- **Modularisasi Basis Kode**: Struktur add-on dirombak dari satu file menjadi arsitektur modular dengan beberapa file agar lebih mudah dipelihara.
- **Desain Ulang Antarmuka Pengaturan**: Dialog Pengaturan didesain ulang sepenuhnya dengan antarmuka modern berbasis tab, menggantikan tata letak berkelompok. Susunan baru lebih teratur dan mudah dinavigasi tanpa menghilangkan opsi yang sudah ada.
- **Pencatatan Global & File Khusus**: Menambahkan sistem pencatatan global opsional di tab pengaturan "Lanjutan" yang baru. Sistem ini otomatis mencatat peristiwa operasional, lalu lintas API, dan error dari seluruh modul add-on ke file khusus (`vision_assistant.log`). Tersedia tingkat perincian log yang dapat diatur (Debug, Info, Peringatan, Error), masa penyimpanan otomatis (1 jam hingga 90 hari), serta kontrol untuk membuka atau membersihkan log langsung dari pengaturan tanpa memengaruhi performa atau log NVDA.
- **Pelacakan Progres Unggahan Gemini**: Menambahkan pengumuman progres persentase secara real-time saat mengunggah file besar (video, audio, dokumen) ke Google Gemini API.

## Perubahan untuk 2026.07.15

- **Penyaringan Model API Cerdas**: Perombakan total sistem penyaringan model untuk menggunakan pendekatan blacklist murni alih-alih whitelist. Menambahkan kata kunci penyaringan yang lebih kuat (`embedding`, `bison`, `gecko`, `audio`, `realtime`, `babbage`, `moderation`, `deep`, `antigravity`, `computer`) untuk memastikan menu dropdown model obrolan utama tetap bersih dan tahan masa depan, sementara tetap menjaga semua model khusus dapat diakses di bagian Perutean Lanjutan.
- **Pencarian Perutean Lanjutan**: Semua dropdown Perutean Model Lanjutan (OCR, STT, TTS, Operator, Video, Live) dan pemilih Varian eSpeak sekarang sepenuhnya dapat dicari. Anda dapat mengetik dengan cepat untuk menyaring dan menemukan model atau varian yang Anda inginkan.
- **Pintasan Lapisan Perintah Baru**:
  - **Pengaturan (`Alt + S`)**: Membuka dialog pengaturan Vision Assistant Pro secara instan.
  - **Laporan Kunci Kuota Habis (`Alt + Q`)**: Melaporkan jumlah persis kunci API Gemini yang telah melebihi kuota harian mereka, mengidentifikasi model spesifik mana yang kuotanya habis, dan mengumumkan waktu reset persisnya.
  - **Audit Perutean (`Alt + M`)**: Mengaudit dan mengumumkan konfigurasi Perutean Lanjutan Anda saat ini, membacakan model mana yang aktif dipilih untuk tugas-tugas khusus (melewati pengaturan default).
- **Perombakan Total Penganalisis Video**: Penganalisis Video telah diubah sepenuhnya! Sebelumnya, fitur ini hanya menyediakan deskripsi dasar untuk video online. Sekarang, fitur ini adalah paket pemrosesan video komprehensif yang dirancang untuk pengguna tunanetra:
  - **Perekaman Layar Lokal (`Control+V`)**: Anda sekarang dapat merekam video tanpa suara langsung dari layar Anda. AI akan menganalisis segmen yang direkam dan memberikan deskripsi yang sangat rinci tentang pemandangan, tata letak, dan tindakan.
  - **Pembuatan Deskripsi Audio (SRT)**: Add-on sekarang dapat menghasilkan skrip Deskripsi Audio yang sangat mendetail (dalam format SRT standar) untuk video, lengkap dengan waktu jeda cerdas untuk menambatkan deskripsi secara cerdas ke jeda alami di trek audio, dan OCR verbatim untuk teks apa pun yang ada di layar.
  - **Narasi Audio Tersinkron (MP3)**: Selain subtitel berbasis teks, add-on dapat mengubah Deskripsi Audio menjadi ucapan, mencampurnya secara otomatis dengan trek audio asli video, menerapkan Peredaman Audio, dan mengekspor hasil akhir yang tersinkron sebagai file MP3.
  - **Aksi File Video Cerdas**: Jika Anda memfokuskan pada file video lokal dan menekan pintasan video, add-on akan secara otomatis mendeteksinya dan memproses file tersebut secara langsung.
  - **Pelacakan Karakter Lanjutan**: AI sekarang melakukan ekstraksi karakter tahap pertama. Ini membangun kamus karakter global dan melacak karakter secara akurat segmen demi segmen tanpa membingungkan identitas.
  - **Konfigurasi Analisis Video**: Menambahkan pengaturan baru untuk mengontrol ukuran potongan SRT, subtitel karakter, dan penafian.
  - **Perutean Model Diperluas**: Anda sekarang dapat memilih model video khusus (`gemini_video_model`, `custom_video_model`) secara eksplisit di pengaturan Perutean Model Lanjutan.
- **Manajemen Kuota API Cerdas**: Penanganan kesalahan 429 (Batas Harian) yang ditingkatkan dengan melacak kuota per model. Jika sebuah kunci mencapai batas hariannya pada satu model, ia akan dikarantina secara cerdas hanya untuk model tersebut, membiarkan kunci tersebut tetap tersedia untuk digunakan dengan model lainnya.

## Perubahan untuk 7.0.0

- **Melanjutkan Pemindaian yang Belum Selesai**: Menambahkan fitur lanjutkan untuk Pembaca Dokumen dan Tindakan File Cerdas. Jika pemindaian terputus, sekarang Anda dapat melanjutkan dari titik terakhir alih-alih memulai lagi dari awal.
- **Variabel `[screen_fg_obj]` Baru**: Menambahkan variabel prompt kustom untuk mengambil tangkapan layar hanya dari jendela aktif di latar depan, bukan seluruh layar.
- **Coba Ulang Cerdas & Rotasi Kunci**: Add-on kini diam-diam mencoba ulang hingga 5 kali pada kunci yang sama saat terjadi beban server sementara, seperti "permintaan tinggi" atau respons tidak valid. Jika percobaan ulang gagal, add-on otomatis beralih ke kunci API berikutnya dalam daftar Anda.
- **Deteksi Screen Curtain**: Menambahkan pemeriksaan untuk mencegah pengambilan tangkapan layar saat Screen Curtain aktif, baik aktif permanen maupun dinyalakan sementara dengan hotkey. Add-on akan memperingatkan Anda dan berhenti, sehingga Anda tidak mengirim gambar hitam dan membuang token API.
- **Penyempurnaan Pembaca Dokumen**: Dialog rentang PDF kini otomatis memilih bahasa target default dari pengaturan add-on. Penanganan thread juga ditingkatkan agar tugas latar belakang berhenti dengan bersih saat pembaca ditutup.
- **Integrasi OCR Mistral Bawaan**: Mengintegrasikan API Document OCR bawaan Mistral. Dokumen multi-halaman otomatis digabung, diunggah, dan diproses secara batch memakai endpoint khusus `/v1/ocr` milik Mistral, sedangkan gambar satu halaman diproses langsung tanpa konversi PDF yang tidak perlu [1].
- **Penangan URL Kustom Dinamis**: Mengubah URL API Kustom kini langsung menghapus cache daftar model dan mengembalikan kotak teks entri model manual. Ini memastikan kompatibilitas penuh dengan endpoint kustom, seperti Cloudflare AI Gateway, yang tidak mendukung endpoint daftar `/v1/models` standar.
- **Mesin Input Operator AI Dirombak**: Sistem simulasi mouse dan keyboard dasar untuk Operator AI ditulis ulang sepenuhnya. API lama `mouse_event` diganti dengan API Windows modern `SendInput`, sehingga kompatibilitas dengan aplikasi modern, jendela yang dilindungi UAC, dan tampilan high-DPI jauh lebih baik.
- **Operasi Seret & Lepas Diperbaiki**: Aksi seret dan lepas di Operator AI kini jauh lebih stabil dan andal. Mesin baru memakai kurva "easing" yang natural, posisi kursor presisi, timing yang dioptimalkan, dan teknik "nudge" cerdas agar Windows dan aplikasi mengenali serta menjalankan gestur seret-dan-lepas dengan benar tanpa gagal di tengah jalan.
- **Dukungan Multi-Monitor**: Operator AI kini mendukung penuh setup multi-monitor. Gerakan dan klik mouse bekerja benar di semua monitor memakai flag `MOUSEEVENTF_VIRTUALDESK`, sehingga posisi tetap akurat di monitor mana pun aplikasi target berada.
- **Simulasi Keyboard Ditingkatkan**: Injeksi tombol ditingkatkan agar mendukung penuh "Extended Keys", seperti tombol panah, Home, End, Page Up/Down, Insert, Delete, dan F1-F12. Ini memastikan navigasi dan perintah pintasan yang dikirim Operator AI berjalan lancar di semua aplikasi.
- **Dukungan Gambar HEIC/HEIF**: Menambahkan dukungan bawaan untuk format foto iPhone. Sekarang Anda dapat langsung memilih file `.heic` dan `.heif` untuk deskripsi AI, OCR, atau Pembacaan Dokumen tanpa konversi lebih dulu.

## Perubahan untuk 6.5.0

- **Asisten Langsung**: Menambahkan fitur asisten suara dan layar secara real-time, tersedia secara eksklusif untuk penyedia Google Gemini (atau penyedia kustom yang kompatibel dengan Gemini). Termasuk kustomisasi suara interaktif dan kedalaman berpikir langsung di dalam dialog, dengan rekoneksi otomatis setelah mengubah pengaturan.
- **Penyedia AI MiniMax**: Mengintegrasikan MiniMax sebagai penyedia setara dengan dukungan multimodal penuh (obrolan, visi, OCR), TTS kustom menggunakan lebih dari 300+ suara dinamis, dan penghapusan blok penalaran secara otomatis (misalnya, `<think>...</think>`) dari keluaran. response\`) dari keluaran.
- **Terjemahan Penampil Dokumen**: Memperbaiki kegagalan terjemahan diam-diam untuk pengguna NVDA non-Inggris dengan memastikan kode bahasa 2 huruf standar dikirim ke Google Translate alih-alih nama bahasa yang dilokalkan.
- **Coba Lagi Pemindaian Batch PDF**: Mengimplementasikan logika coba lagi yang sangat dioptimalkan, terpisah, dan diam-diam untuk pemindaian batch dokumen PDF guna mencegah pengunggahan berulang dan menghindari popup kesalahan yang mengganggu selama proses coba lagi.
- **Status Penampil Dokumen**: Memperbaiki bug di mana status keseluruhan plugin (diperiksa melalui `I`) tetap macet di "Pemrosesan Batch Dimulai" selama pemindaian dokumen yang panjang.
- **Perbaikan Crash Threading**: Memperbaiki crash pernyataan thread `IsMain() failed in wxTimerImpl` yang parah saat membuka dokumen dari thread latar belakang dengan memindahkan antrean callback GUI ke `wx.CallAfter`.

## Perubahan untuk 6.1.2

- **Pemeriksaan Awal Label Duplikat**: Memperbaiki masalah pada pelabelan tunggal ketika pemeriksaan duplikat masih memakai kunci koordinat lama, sehingga NVDA membuat permintaan AI ganda untuk objek yang sudah diberi label alih-alih mengumumkan label yang ada.
- **Obrolan Dokumen untuk Penyedia Non-Gemini**: Memperbaiki pemeriksaan kunci API yang terlalu ketat di Obrolan Dokumen (`on_ask`) agar pengguna OpenAI, Groq, atau penyedia Kustom lokal seperti Ollama dapat mengobrol dengan dokumen tanpa diblokir.
- **Terjemahan OCR Chrome Cepat**: Mengembalikan API terjemahan gratis tanpa kunci untuk OCR Chrome. Terjemahan teks hasil ekstraksi kini melewati AI Gemini, sehingga kuota API lebih hemat dan proses terjemahan lebih cepat.
- **Filter Alfanumerik CAPTCHA**: Memperbaiki logika filter di pemecah CAPTCHA agar karakter non-alfanumerik dibersihkan dengan benar dalam semua situasi.
- **Pembaruan Bantuan Lapisan Perintah**: Memperbaiki pintasan pengumuman status di menu bantuan dari `L` menjadi `I`, dan menambahkan kedua perintah pelabelan (`L` dan `Shift+L`) ke daftar.

## Perubahan untuk 6.1.1

- **Perbaikan Output Thinking Gemma 4**: Memperbaiki masalah pada model Gemma 4 ketika seluruh proses berpikir internal ditampilkan sebagai respons akhir, atau ketika menonaktifkan thinking menghasilkan respons kosong. Add-on kini memisahkan dan mengambil hanya teks akhir yang bersih.
- **OCR Batch dari File Explorer**: Anda kini dapat memilih beberapa foto atau PDF langsung di Windows File Explorer dan mengekstrak teks atau menganalisisnya secara batch. Add-on akan otomatis memfilter dan memproses hanya format file yang didukung.

## Perubahan untuk 6.1.0

- **Integrasi AI Lokal Universal (Siapkan AI Lokal)**: Menambahkan tombol **"Siapkan AI Lokal"** baru di Pengaturan Penyedia Kustom. Pengguna kini dapat mengonfigurasi mesin AI lokal seperti **Ollama**, **LM Studio**, **Jan.ai**, dan **KoboldCPP** secara otomatis dan instan.
- **Bypass Proksi Lokal Cerdas**: Logika koneksi dibangun ulang dengan mekanisme bypass proksi lanjutan. Add-on kini dapat melewati proksi sistem Windows sepenuhnya untuk koneksi loopback lokal, sehingga koneksi AI lokal tetap stabil meskipun VPN atau mode TUN sedang aktif.
- **Pelabelan AI Sangat Stabil (v2)**: Kunci berbasis koordinat layar absolut diganti dengan sistem **Object Signature** hibrida yang lebih canggih. Label kini mengandalkan pengenal programatik seperti UIA **AutomationId** atau Win32 **ControlID**, serta koordinat relatif jendela, sehingga label kustom tahan terhadap perubahan ukuran atau posisi jendela, perpindahan monitor, dan scaling.
- **Migrasi Label Otomatis yang Mulus**: Proses upgrade berjalan transparan. Add-on akan memigrasikan label lama berbasis koordinat ke format sidik jari baru yang stabil di latar belakang saat fokus pertama kali, tanpa kehilangan data.

## Perubahan untuk 6.0

- **Memperkenalkan Pelabelan AI Semantik**: Pengguna kini dapat memberi label permanen pada tombol dan ikon tanpa nama menggunakan AI. Tekan **L** untuk memberi label pada objek navigator saat ini (mendukung fokus Tab dan navigasi objek), atau **Shift+L** untuk memindai dan memberi label seluruh aplikasi sekaligus.
- **Pengelolaan Label Cerdas**: Menambahkan dialog Pengelola Label baru yang sepenuhnya aksesibel (melalui **Shift+L** jika label sudah ada) untuk melihat, mengganti nama, atau menghapus banyak label kustom sekaligus.
- **Analisis File Langsung (Tanpa Dialog File)**: Add-on kini dapat mendeteksi saat fokus berada pada file PDF atau gambar di Windows File Explorer. Menekan **F (Tindakan File Cerdas)** atau **D (Pembaca Dokumen)** pada file yang disorot akan langsung memprosesnya, tanpa membuka dialog "Buka" standar.

## Perubahan untuk 5.6

- **Menambahkan Mesin OCR "Tanpa OCR (Ekstrak Lapisan Teks)"**: Pengguna kini dapat mengambil teks langsung dari PDF yang sudah memiliki lapisan teks tanpa memakai kredit AI. Ini membuat proses lebih cepat dan lebih privat untuk dokumen berbasis teks.
- **Akurasi UI Explorer Ditingkatkan**: Prompt UI Explorer diperbaiki agar lebih tepat mengenali jenis elemen, seperti item daftar, dan melaporkan status seperti "(Dicentang)", "(Dipilih)", atau "(Diperluas)", sambil mengabaikan komponen sistem Windows seperti Taskbar dan Jam.
- **Pengingat Pengaturan Setelah Instalasi**: Menambahkan notifikasi setelah instalasi untuk mengarahkan pengguna ke menu pengaturan agar dapat mengonfigurasi kunci API dan preferensi.

## Perubahan untuk 5.5 (Pembaruan Otomasi)

- **Operator AI (Kontrol Mandiri - Shift+A):** Ini adalah fitur utama di v5.5. Vision Assistant Pro berkembang dari asisten pasif menjadi **Operator AI** pribadi Anda. Add-on ini tidak hanya mendeskripsikan layar, tetapi juga dapat mengambil tindakan.
- **Visual UI Explorer (E):** Lelah menghadapi "tombol tanpa label"? Tekan **E** untuk mengaktifkan UI Explorer. AI akan memindai seluruh jendela dan membuat daftar semua elemen yang bisa diklik, termasuk ikon, grafik, dan menu. Pilih item dari daftar, lalu Operator AI akan mengkliknya untuk Anda. Anggap saja seperti lapisan aksesibilitas tambahan di atas aplikasi apa pun.
- **Tindakan File Cerdas Berbasis Konteks (F):** Tombol **F** dirombak total. Fitur ini tidak lagi menganggap Anda selalu ingin OCR. Saat Anda memilih satu gambar, add-on akan menanyakan tujuan Anda: pilih **Deskripsi Visual Terperinci** untuk memahami isi gambar, atau **Ekstraksi Teks Terstruktur (OCR)** untuk membaca teks. Menu akan menyesuaikan secara dinamis berdasarkan jenis file dan mesin AI yang aktif.

## Perubahan pada 5.5 (Pembaruan Otomasi)

- **Operator AI (Kendali Mandiri - Shift+A):** Inilah fitur unggulan v5.5. Vision Assistant Pro telah berkembang dari asisten pasif menjadi **Operator AI** pribadi Anda. Fitur ini tidak hanya mendeskripsikan layar—tetapi juga mengambil kendali.
  - _Cara kerja:_ Anda kini dapat memberikan instruksi dengan bahasa sehari-hari untuk mengoperasikan PC. Misalnya, dalam aplikasi yang sama sekali tidak aksesibel sehingga pembaca layar tidak bersuara, tekan **Shift+A** lalu ketik: _"Klik tombol Pengaturan"_ atau _"Cari kolom pencarian, ketik 'Berita Terbaru', lalu tekan enter."_ AI mengenali elemen secara visual, menggerakkan mouse, dan menjalankan tugas untuk Anda.
  - _Catatan Kinerja:_ Fitur ini dioptimalkan untuk **Gemini 3.0 Flash (Preview)**, dengan respons yang sangat cepat dan cerdas untuk menangani tata letak antarmuka yang paling rumit sekalipun.
  - **⚠️ Peringatan Penggunaan API:** Agar dapat bekerja secara akurat, Operator AI perlu "melihat" dengan jelas apa yang terjadi, sehingga tangkapan layar beresolusi tinggi dikirim pada setiap langkah. Perlu diingat bahwa penggunaan yang sering akan menghabiskan kuota API jauh lebih cepat dibandingkan tugas standar berbasis teks.
- **Penjelajah Antarmuka Visual (E):** Lelah menelusuri "tombol tanpa label"? Tekan **E** untuk mengaktifkan Penjelajah Antarmuka. AI akan memindai seluruh jendela dan membuat daftar semua elemen yang dapat diklik—termasuk ikon, grafik, dan menu. Cukup pilih item dari daftar, dan Operator AI akan mengekliknya untuk Anda. Rasanya seperti memiliki "lapisan aksesibel" di atas aplikasi apa pun.
- **Tindakan Berkas Cerdas Berbasis Konteks (F):** Tombol "F" telah dirombak sepenuhnya. Fitur ini tidak lagi menganggap Anda hanya ingin menggunakan OCR. Saat Anda memilih satu gambar, fitur ini kini menanyakan tujuan Anda: pilih **Deskripsi Visual Terperinci** untuk memahami adegan, atau **Ekstraksi Teks Terstruktur (OCR)** untuk membaca teks. Menu menyesuaikan secara dinamis berdasarkan jenis berkas dan mesin AI yang aktif.
- **Optimasi Inti:** Kami telah membersihkan logika internal add-on secara menyeluruh dengan menghapus fungsi lama yang tidak terpakai serta kode berulang yang tidak diperlukan. Hasilnya, add-on menjadi lebih ringan, cepat, dan andal bagi semua pengguna.

## Perubahan untuk 5.0

- **Arsitektur Multi-Penyedia**: Menambahkan dukungan penuh untuk **OpenAI**, **Groq**, dan **Mistral** selain Google Gemini. Pengguna kini dapat memilih backend AI yang diinginkan.
- **Perutean Model Lanjutan**: Pengguna penyedia bawaan seperti Gemini dan OpenAI kini dapat memilih model tertentu dari daftar dropdown untuk berbagai tugas, seperti OCR, STT, dan TTS. kini dapat memilih model tertentu dari daftar pilihan untuk berbagai tugas (OCR, STT, TTS).
- **Konfigurasi Titik Akhir Lanjutan**: Pengguna penyedia kustom dapat memasukkan URL dan nama model tertentu secara manual untuk kontrol lebih rinci atas server lokal atau layanan pihak ketiga.
- **Visibilitas Fitur Cerdas**: Menu pengaturan dan antarmuka Pembaca Dokumen kini otomatis menyembunyikan fitur yang tidak didukung, seperti TTS, berdasarkan penyedia yang dipilih.
- **Pengambilan Model Dinamis**: Add-on kini mengambil daftar model yang tersedia langsung dari API penyedia, sehingga tetap kompatibel dengan model baru segera setelah dirilis.
- **OCR & Terjemahan Hybrid**: Logika dioptimalkan agar memakai Google Translate untuk kecepatan saat menggunakan Chrome OCR, dan terjemahan berbasis AI saat memakai mesin Gemini, Groq, atau OpenAI.
- **"Pindai ulang dengan AI" Universal**: Fitur pindai ulang di Pembaca Dokumen tidak lagi terbatas pada Gemini. Fitur ini memakai penyedia AI apa pun yang sedang aktif untuk memproses ulang halaman.

## Perubahan untuk 4.6

- **Pembukaan Ulang Hasil Interaktif:** Menambahkan tombol **Space** pada Lapisan Perintah, sehingga pengguna bisa langsung membuka kembali respons AI terakhir di jendela obrolan untuk pertanyaan lanjutan, bahkan saat mode "Keluaran Langsung" aktif.
- **Pusat Komunitas Telegram:** Menambahkan tautan "Kanal Telegram Resmi" di menu Tools NVDA, agar pengguna lebih cepat mengikuti kabar, fitur, dan rilis terbaru.
- **Stabilitas Respons Ditingkatkan:** Mengoptimalkan logika inti fitur Terjemahan, OCR, dan Visi agar performa lebih andal dan pengalaman output suara langsung lebih mulus.
- **Panduan Antarmuka Ditingkatkan:** Deskripsi pengaturan dan dokumentasi diperbarui agar sistem pembukaan ulang hasil terakhir lebih mudah dipahami, termasuk cara kerjanya bersama pengaturan output langsung.

## Perubahan untuk 4.5

- **Pengelola Prompt Lanjutan:** Menambahkan dialog khusus di pengaturan untuk menyesuaikan prompt sistem bawaan dan mengelola prompt buatan pengguna, termasuk tambah, edit, urut ulang, dan pratinjau.
- **Dukungan Proksi Menyeluruh:** Memperbaiki masalah koneksi dengan memastikan proksi yang diatur pengguna diterapkan secara ketat ke semua permintaan API, termasuk terjemahan, OCR, dan pembuatan suara.
- **Migrasi Data Otomatis:** Menambahkan sistem migrasi cerdas untuk memperbarui konfigurasi prompt lama ke format JSON v2 yang lebih kuat saat pertama kali dijalankan, tanpa kehilangan data.
- **Kompatibilitas Diperbarui (2025.1):** Menetapkan NVDA versi minimum 2025.1 karena ketergantungan pustaka pada fitur lanjutan seperti Pembaca Dokumen.
- **Antarmuka Pengaturan Dioptimalkan:** Pengaturan dibuat lebih rapi dengan memindahkan manajemen prompt ke dialog terpisah, sehingga pengalaman pengguna lebih bersih dan aksesibel.
- **Panduan Variabel Prompt:** Menambahkan panduan bawaan di dialog prompt agar pengguna mudah mengenali dan memakai variabel dinamis seperti [selection], [clipboard], dan [screen_obj].

## Perubahan untuk 4.0.3

- **Ketahanan Jaringan Ditingkatkan:** Menambahkan mekanisme coba ulang otomatis untuk menangani koneksi internet tidak stabil dan error server sementara, sehingga respons AI lebih andal.
- **Dialog Terjemahan Visual:** Menambahkan jendela khusus untuk hasil terjemahan. Pengguna dapat menelusuri dan membaca terjemahan panjang baris demi baris, mirip hasil OCR.
- **Tampilan Terformat Gabungan:** Fitur "View Formatted" di Pembaca Dokumen kini menampilkan semua halaman yang diproses dalam satu jendela terstruktur dengan header halaman yang jelas.
- **Alur OCR Dioptimalkan:** Pemilihan rentang halaman otomatis dilewati untuk dokumen satu halaman, sehingga proses pengenalan lebih cepat dan mulus.
- **Stabilitas API Ditingkatkan:** Beralih ke metode autentikasi berbasis header yang lebih kuat untuk mengatasi potensi error "All API Keys failed" akibat konflik rotasi kunci.
- **Perbaikan Bug:** Memperbaiki beberapa potensi crash, termasuk masalah saat add-on dihentikan dan error fokus di dialog obrolan.

## Perubahan untuk 4.0.1

- **Pembaca Dokumen Lanjutan:** Penampil baru yang kuat untuk PDF dan gambar, dengan pilihan rentang halaman, pemrosesan latar belakang, dan navigasi `Ctrl+PageUp/Down` yang mulus.
- **Submenu Tools Baru:** Menambahkan submenu khusus "Vision Assistant" di menu Tools NVDA untuk akses cepat ke fitur utama, pengaturan, dan dokumentasi.
- **Kustomisasi Fleksibel:** Anda kini dapat memilih mesin OCR dan suara TTS langsung dari panel pengaturan.
- **Dukungan Multi Kunci API:** Menambahkan dukungan beberapa kunci API Gemini. Anda dapat memasukkan satu kunci per baris atau memisahkannya dengan koma di pengaturan.
- **Mesin OCR Alternatif:** Menambahkan mesin OCR baru agar pengenalan teks tetap andal saat kuota Gemini API habis.
- **Rotasi Kunci API Cerdas:** Add-on otomatis beralih ke kunci API yang berfungsi paling cepat dan mengingatnya untuk melewati batas kuota.
- **Dokumen ke MP3/WAV:** Menambahkan kemampuan membuat dan menyimpan file audio berkualitas tinggi dalam format MP3 (128kbps) dan WAV langsung dari pembaca.
- **Dukungan Instagram Stories:** Menambahkan kemampuan untuk mendeskripsikan dan menganalisis Instagram Stories melalui URL.
- **Dukungan TikTok:** Menambahkan dukungan video TikTok untuk deskripsi visual lengkap dan transkripsi audio klip.
- **Dialog Pembaruan Didesain Ulang:** Menghadirkan antarmuka baru yang aksesibel dengan kotak teks yang dapat digulir, sehingga perubahan versi mudah dibaca sebelum instalasi.
- **Status & UX Diseragamkan:** Menyeragamkan dialog file di seluruh add-on dan meningkatkan perintah 'L' agar dapat melaporkan progres secara real-time.

## Perubahan untuk 3.6.0

- **Sistem Bantuan:** Menambahkan perintah bantuan (`H`) di dalam Lapisan Perintah untuk menampilkan daftar pintasan dan fungsinya dengan mudah.
- **Analisis Video Online:** Dukungan diperluas ke video **Twitter (X)**. Deteksi URL dan stabilitas juga ditingkatkan agar lebih andal.
- **Kontribusi Proyek:** Menambahkan dialog donasi opsional bagi pengguna yang ingin mendukung pembaruan dan perkembangan proyek di masa depan.

## Perubahan untuk 3.5.0

\* \*\*Lapisan Perintah:\*\* Memperkenalkan sistem Lapisan Perintah (bawaan: `NVDA+Shift+V`) untuk mengelompokkan pintasan di bawah satu tombol utama. Misalnya, untuk menerjemahkan, Anda kini menekan `NVDA+Shift+V` diikuti `T`, alih-alih `NVDA+Control+Shift+T`.
\* \*\*Analisis Video Daring:\*\* Menambahkan fitur untuk menganalisis video YouTube dan Instagram langsung dengan memasukkan URL.

## Perubahan untuk 3.1.0

- **Mode Keluaran Langsung:** Menambahkan opsi untuk melewati dialog obrolan dan mendengar respons AI langsung melalui suara, agar lebih cepat dan mulus.
- **Integrasi Papan Klip:** Menambahkan pengaturan baru untuk menyalin respons AI ke papan klip secara otomatis.

## Perubahan untuk 3.0

- **Bahasa Baru:** Menambahkan terjemahan **Persia** dan **Vietnam**.
- **Model AI Diperluas:** Daftar pilihan model ditata ulang dengan awalan yang jelas (`[Free]`, `[Pro]`, `[Auto]`) agar pengguna dapat membedakan model gratis dan model berbayar atau terbatas kuota. Dukungan untuk **Gemini 3.0 Pro** dan **Gemini 2.0 Flash Lite** juga ditambahkan.
- **Stabilitas Dikte:** Stabilitas Dikte Cerdas ditingkatkan secara signifikan. Klip audio yang lebih pendek dari 1 detik kini diabaikan untuk mencegah halusinasi AI dan error kosong.
- **Penanganan File:** Memperbaiki masalah yang membuat unggahan file dengan nama non-Inggris gagal.
- **Optimasi Prompt:** Memperbaiki logika terjemahan dan menyusun hasil fitur visi agar lebih terstruktur.

## Perubahan untuk 2.9

- **Menambahkan terjemahan Prancis dan Turki.**
- **Tampilan Terformat:** Menambahkan tombol "View Formatted" di dialog obrolan untuk melihat percakapan dengan format yang benar, seperti heading, teks tebal, dan kode, di jendela standar yang dapat dijelajahi.
- **Pengaturan Markdown:** Menambahkan opsi "Clean Markdown in Chat" di Pengaturan. Jika opsi ini tidak dicentang, pengguna dapat melihat sintaks Markdown mentah, misalnya `**` dan `#`, di jendela obrolan.
- **Manajemen Dialog:** Memperbaiki masalah yang membuat jendela "Refine Text" atau obrolan terbuka berkali-kali atau gagal mendapatkan fokus.
- **Peningkatan UX:** Menyeragamkan judul dialog file menjadi "Open" dan menghapus pengumuman suara yang tidak perlu, seperti "Opening menu...", agar pengalaman lebih mulus. agar penggunaan lebih lancar.

## Perubahan untuk 2.8

- Menambahkan terjemahan bahasa Italia.
- **Laporan Status:** Menambahkan perintah baru (NVDA+Control+Shift+I) untuk mengumumkan status add-on saat ini, misalnya "Uploading..." atau "Analyzing...".
- **Ekspor HTML:** Tombol "Save Content" di dialog hasil kini menyimpan output sebagai file HTML terformat, termasuk gaya seperti heading dan teks tebal.
- **UI Pengaturan:** Tata letak panel pengaturan ditingkatkan dengan pengelompokan yang lebih aksesibel.
- **Model Baru:** Menambahkan dukungan untuk gemini-flash-latest dan gemini-flash-lite-latest.
- **Bahasa:** Menambahkan bahasa Nepal ke daftar bahasa yang didukung.
- **Logika Menu Refine:** Memperbaiki bug penting yang membuat perintah "Refine Text" gagal saat bahasa antarmuka NVDA bukan bahasa Inggris.
- **Dikte:** Meningkatkan deteksi hening agar tidak menghasilkan teks yang salah saat tidak ada ucapan.
- **Pengaturan Pembaruan:** "Check for updates on startup" kini dinonaktifkan secara default agar sesuai dengan kebijakan Add-on Store.
- Pembersihan kode.

## Perubahan untuk 2.7

- Memigrasikan struktur proyek ke Template Add-on resmi NV Access agar lebih sesuai standar.
- Menambahkan logika coba ulang otomatis untuk error HTTP 429 (Rate Limit), agar lebih andal saat trafik tinggi.
- Mengoptimalkan prompt terjemahan untuk akurasi lebih tinggi dan penanganan logika "Smart Swap" yang lebih baik.
- Memperbarui terjemahan Rusia.

## Perubahan untuk 2.6

- Menambahkan dukungan terjemahan Rusia (terima kasih kepada nvda-ru).
- Memperbarui pesan error agar informasi konektivitas lebih jelas.
- Mengubah bahasa target default ke bahasa Inggris.

## Perubahan untuk 2.5

- Menambahkan perintah OCR file bawaan (NVDA+Control+Shift+F).
- Menambahkan tombol "Save Chat" di dialog hasil.
- Menambahkan dukungan lokalisasi penuh (i18n).
- Memigrasikan umpan balik audio ke modul tones bawaan NVDA.
- Beralih ke Gemini File API untuk menangani PDF dan file audio dengan lebih baik.
- Memperbaiki crash saat menerjemahkan teks yang berisi kurung kurawal.

## Perubahan untuk 2.1

- Menstandarkan semua pintasan agar memakai NVDA+Control+Shift untuk menghindari konflik dengan layout Laptop NVDA dan hotkey sistem.

## Perubahan pada 2.1

- Menyeragamkan semua pintasan menjadi NVDA+Control+Shift untuk menghindari konflik dengan tata letak Laptop NVDA dan pintasan sistem.

## Perubahan untuk 2.0

- Menambahkan sistem Auto-Update bawaan.
- Menambahkan Smart Translation Cache untuk mengambil kembali teks yang pernah diterjemahkan secara instan.
- Menambahkan Conversation Memory untuk menyempurnakan hasil secara kontekstual di dialog obrolan.
- Menambahkan perintah khusus Terjemahan Papan Klip (NVDA+Control+Shift+Y).
- Mengoptimalkan prompt AI agar benar-benar mengikuti bahasa target.
- Memperbaiki crash akibat karakter khusus pada teks masukan.

## Perubahan untuk 1.5

- Menambahkan dukungan untuk lebih dari 20 bahasa baru.
- Menambahkan Dialog Refine Interaktif untuk pertanyaan lanjutan.
- Menambahkan fitur Dikte Cerdas bawaan.
- Menambahkan kategori "Vision Assistant" di dialog Input Gestures NVDA.
- Memperbaiki crash COMError pada aplikasi tertentu seperti Firefox dan Word.
- Menambahkan mekanisme coba ulang otomatis untuk error server.

## Perubahan untuk 1.0

- Rilis awal.
