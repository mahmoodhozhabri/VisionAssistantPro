# Dokumentasi Vision Assistant Pro

**Vision Assistant Pro** adalah asisten AI multimodal tingkat lanjut untuk NVDA. Add-on ini memakai mesin AI kelas dunia untuk membantu pembacaan layar cerdas, penerjemahan, dikte suara, dan analisis dokumen.

_Add-on ini dirilis untuk komunitas dalam rangka memperingati Hari Internasional Penyandang Disabilitas._

## 1. Pengaturan & Konfigurasi

Buka **Menu NVDA > Preferensi > Pengaturan > Vision Assistant Pro**.

### 1.1 Pengaturan Koneksi
- **Penyedia:** Pilih layanan AI yang ingin Anda gunakan. Penyedia yang didukung meliputi **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax**, dan **Kustom** (server yang kompatibel dengan OpenAI seperti Ollama, LM Studio, Jan.ai, atau KoboldCPP).
- **Catatan penting:** Kami sangat menyarankan **Google Gemini** untuk performa dan akurasi terbaik, terutama untuk analisis gambar dan file.
- **Kunci API:** Wajib diisi. Anda dapat memasukkan beberapa kunci sekaligus, dipisahkan dengan koma atau baris baru, agar add-on bisa melakukan rotasi otomatis.
- **Ambil Model:** Setelah kunci API dimasukkan, tekan tombol ini untuk mengunduh daftar model terbaru dari penyedia.
- **Model AI:** Pilih model utama untuk obrolan umum dan analisis.

### 1.2 Perutean Model Lanjutan
*Tersedia untuk semua penyedia, termasuk Gemini, OpenAI, Groq, Mistral, dan Kustom.*

> **Peringatan:** Pengaturan ini ditujukan untuk **pengguna tingkat lanjut**. Jika Anda belum yakin fungsi sebuah model, biarkan opsi ini **tidak dicentang**. Memilih model yang tidak cocok untuk suatu tugas, misalnya model khusus teks untuk fitur visi, dapat menyebabkan error dan menghentikan kerja add-on.

Centang **"Perutean Model Lanjutan (Khusus Tugas)"** untuk membuka kontrol yang lebih rinci. Dengan opsi ini, Anda dapat memilih model berbeda dari daftar dropdown untuk tiap tugas:
- **Model OCR / Visi:** Pilih model khusus untuk menganalisis gambar.
- **Speech-to-Text (STT):** Pilih model khusus untuk dikte atau transkripsi suara.
- **Text-to-Speech (TTS):** Pilih model untuk membuat audio.
- **Model Operator AI:** Pilih model khusus untuk tugas pengoperasian komputer secara otomatis.
*Catatan: Fitur yang tidak didukung, misalnya TTS untuk Groq, akan disembunyikan otomatis.*

### 1.3 Konfigurasi Titik Akhir Lanjutan (Penyedia Kustom)
*Hanya tersedia saat penyedia "Kustom" dipilih.*

> **Peringatan:** Bagian ini digunakan untuk konfigurasi API manual dan ditujukan bagi pengguna mahir yang menjalankan server lokal atau proksi. URL atau nama model yang salah dapat memutus koneksi. Jika Anda belum benar-benar memahami titik akhir ini, biarkan opsi ini **tidak dicentang**.

Centang **"Konfigurasi Titik Akhir Lanjutan"** untuk mengisi detail server secara manual. Berbeda dengan penyedia bawaan, di sini Anda harus **mengetik** URL dan nama model secara spesifik:
- **URL Daftar Model:** Titik akhir untuk mengambil daftar model yang tersedia.
- **URL Titik Akhir OCR/STT/TTS:** URL lengkap untuk layanan tertentu, misalnya `http://localhost:11434/v1/audio/speech`.
- **Model Kustom:** Ketik nama model secara manual, misalnya `llama3:8b`, untuk setiap tugas.

### 1.3.1 Siapkan AI Lokal (Konfigurasi Satu Tindakan)
Untuk memudahkan integrasi AI lokal yang sepenuhnya offline, tersedia tombol khusus **"Siapkan AI Lokal"** di dalam Pengaturan Penyedia Kustom.

Jika Anda menjalankan server model AI lokal di komputer:
1. Pilih **Kustom** sebagai Penyedia.
2. Tekan tombol **Siapkan AI Lokal**.
3. Pilih mesin AI lokal dari dialog yang aksesibel:
   - **Ollama** (bawaan `http://127.0.0.1:11434`)
   - **LM Studio** (bawaan `http://127.0.0.1:1234`)
   - **Jan.ai** (bawaan `http://127.0.0.1:1337`)
   - **KoboldCPP** (bawaan `http://127.0.0.1:5001`)
4. Add-on akan langsung mengatur URL lokal, jenis API, dan mengambil model offline yang aktif untuk mengisi kotak pilihan **Model AI**.

*Catatan tentang Jaringan & Proksi:* Mesin koneksi lokal ini memiliki mekanisme bypass proksi lanjutan. Walaupun VPN sistem atau proksi mode TUN sedang aktif, permintaan AI lokal akan melewatinya sepenuhnya, sehingga koneksi offline tetap stabil tanpa error 502 Bad Gateway.

### 1.4 Preferensi Umum
- **Mesin OCR:** Pilih **Chrome (Cepat)** untuk hasil cepat, atau **AI (Lanjutan)** untuk mempertahankan tata letak dengan lebih baik.
    - *Catatan:* Jika Anda memilih "AI (Lanjutan)" tetapi penyedia aktif adalah OpenAI atau Groq, add-on akan mengarahkan gambar ke model visi dari penyedia aktif tersebut.
- **Suara TTS:** Pilih gaya suara yang Anda inginkan. Daftar ini diperbarui secara dinamis berdasarkan penyedia aktif.
- **Kreativitas (Temperature):** Mengatur seberapa acak jawaban AI. Nilai rendah lebih baik untuk terjemahan dan OCR yang akurat.
- **URL Proksi:** Atur ini jika layanan AI dibatasi di wilayah Anda. Mendukung proksi lokal seperti `127.0.0.1` atau URL bridge.

## 2. Lapisan Perintah & Pintasan

Untuk mencegah konflik tombol keyboard, add-on ini memakai **Lapisan Perintah**.
1. Tekan **NVDA + Shift + V** (Tombol Utama) untuk mengaktifkan lapisan. Anda akan mendengar bunyi bip.
2. Lepaskan tombol, lalu tekan salah satu tombol tunggal berikut:

| Tombol        | Fungsi                 | Deskripsi                                                                  |
|---------------|------------------------|----------------------------------------------------------------------------|
| **Shift + A** | **Operator AI**        | **Operasi otomatis:** Minta AI melakukan tugas di layar Anda. Tekan lagi untuk langsung membatalkan operasi yang sedang berjalan. |
| **E**         | **UI Explorer**        | **Klik interaktif:** Mengenali dan mengklik elemen UI di aplikasi apa pun. |
| **T**         | Penerjemah Cerdas      | Menerjemahkan teks di kursor navigator atau teks yang dipilih.             |
| **Shift + T** | Penerjemah Papan Klip  | Menerjemahkan isi papan klip saat ini.                                     |
| **R**         | Penyempurna Teks       | Meringkas, memperbaiki tata bahasa, menjelaskan, atau menjalankan **Prompt Kustom**. |
| **V**         | Visi Objek             | Mendeskripsikan objek navigator saat ini.                                  |
| **O**         | Visi Layar Penuh       | Menganalisis tata letak dan isi seluruh layar.                             |
| **Shift + V** | Analisis Video Online  | Menganalisis video **YouTube**, **Instagram**, **TikTok**, atau **Twitter (X)**. |
| **D**         | Pembaca Dokumen        | Pembaca lanjutan untuk PDF dan gambar, lengkap dengan pilihan rentang halaman. |
| **F**         | **Aksi File Cerdas**   | Mengenali konteks dari file gambar, PDF, atau TIFF yang dipilih.           |
| **A**         | Transkripsi Audio      | Mengubah file MP3, WAV, atau OGG menjadi teks.                             |
| **C**         | Pemecah CAPTCHA        | Menangkap dan memecahkan CAPTCHA, termasuk pada portal pemerintah.         |
| **S**         | Dikte Cerdas           | Mengubah ucapan menjadi teks. Tekan untuk mulai merekam, tekan lagi untuk berhenti dan mengetik hasilnya. |
| **Control+L** | **Asisten Langsung**   | **Kopilot real-time (khusus Gemini):** Memulai atau mengakhiri percakapan suara dan layar langsung dengan asisten AI. |
| **I**         | Laporan Status         | Mengumumkan progres saat ini, misalnya "Memindai..." atau "Diam".         |
| **L**         | **Label Objek**        | **Pelabelan AI semantik:** Memberi label permanen pada elemen atau ikon yang sedang fokus. |
| **Shift + L** | **Kelola/Pindai Label** | Membuka Pengelola Label jika label sudah ada, atau memindai aplikasi untuk elemen tanpa nama. |
| **U**         | Cek Pembaruan          | Mengecek versi terbaru add-on di GitHub secara manual.                     |
| **Space**     | Buka Hasil Terakhir    | Menampilkan respons AI terakhir di dialog obrolan untuk ditinjau atau ditindaklanjuti. |
| **H**         | Bantuan Perintah       | Menampilkan daftar semua pintasan yang tersedia.                           |

### 2.1 Pintasan Pembaca Dokumen (Di Dalam Penampil)
- **Ctrl + PageDown:** Pindah ke halaman berikutnya.
- **Ctrl + PageUp:** Pindah ke halaman sebelumnya.
- **Alt + A:** Membuka dialog obrolan untuk bertanya tentang dokumen.
- **Alt + R:** Memaksa **Pindai ulang dengan AI** memakai penyedia aktif.
- **Alt + G:** Membuat dan menyimpan file audio berkualitas tinggi (WAV/MP3). *Disembunyikan jika penyedia tidak mendukung TTS.*
- **Alt + S / Ctrl + S:** Menyimpan teks hasil ekstraksi sebagai file TXT atau HTML.

## 3. Operator AI - Kontrol Komputer Mandiri

**Operator AI** mengubah Vision Assistant Pro dari pembaca pasif menjadi asisten aktif yang dapat berinteraksi dengan komputer atas nama Anda. Anda dapat memintanya mendeskripsikan layar, menjawab pertanyaan tentang apa yang terlihat, atau bahkan mengambil kendali: mengklik tombol, menyeret item, mengetik teks, dan menavigasi aplikasi memakai perintah bahasa alami.

Keuntungan terbesarnya adalah fitur ini tetap bekerja pada software yang sama sekali tidak aksesibel. Jika Anda terjebak di aplikasi kustom, remote desktop, atau situs web yang membuat pembaca layar tidak memberi informasi apa pun, Operator AI tetap bisa membantu. Karena ia "melihat" layar secara visual, ia dapat menemukan, membaca, dan berinteraksi dengan elemen yang tidak memiliki label aksesibilitas.

### Cara Kerja
1. Tekan **NVDA + Shift + V**, lalu tekan **Shift + A** (atau gunakan pintasan langsung) untuk membuka dialog Operator AI.
2. Ketik apa yang ingin Anda lakukan dengan bahasa biasa, misalnya "Klik tombol Simpan", "Apa isi pesan error ini?", atau "Ubah nama file menjadi final.pdf".
3. AI akan menganalisis layar, mengenali elemen yang relevan, lalu menjalankan tindakan atau memberikan jawaban. Jika tugas memerlukan beberapa langkah, operator akan terus bekerja sampai selesai.
4. Tekan **Shift + A** lagi kapan saja untuk langsung membatalkan operasi yang sedang berjalan.

### Tindakan yang Didukung
Operator memahami banyak jenis perintah:
- **Deskripsikan & Jawab**: "Deskripsikan tata letak layar" atau "Apa isi pesan error ini?"
- **Klik**: "Klik tombol Simpan"
- **Klik Kanan**: "Klik kanan file itu"
- **Klik Ganda**: "Klik ganda dokumen itu"
- **Seret & Lepas**: "Seret dokumen ke folder Arsip"
- **Ketik**: "Ketik 'Halo Dunia' di kotak pencarian"
- **Gulir**: "Gulir ke bawah tiga kali"
- **Tekan Tombol**: "Tekan Enter", "Tekan Tab", "Tekan Escape"
- **Tugas Multi-Langkah**: "Buka File Explorer, cari laporan, lalu ubah namanya menjadi final.pdf"

### Catatan Penting
- **Peringatan Penggunaan API**: Karena operator perlu "melihat" persis apa yang terjadi di layar, ia mengirim tangkapan layar resolusi tinggi pada setiap langkah. Penggunaan yang sering akan menghabiskan kuota API jauh lebih cepat daripada fitur berbasis teks biasa.
- **Aplikasi Administrator**: Jika NVDA tidak berjalan dengan hak Administrator, operator mungkin tidak dapat berinteraksi dengan jendela yang memerlukan izin lebih tinggi. Ini adalah batasan keamanan Windows, bukan bug pada add-on.
- **Praktik Terbaik**: Untuk hasil terbaik, berikan perintah yang jelas dan spesifik. "Klik tombol Kirim berwarna biru di bagian bawah formulir" hampir selalu lebih baik daripada hanya "Klik tombol".

## 4. Prompt Kustom & Variabel

Anda dapat mengelola prompt di **Pengaturan > Prompt > Kelola Prompt...**.

### Variabel yang Didukung
- `[selection]`: Teks yang sedang dipilih.
- `[clipboard]`: Isi papan klip.
- `[screen_obj]`: Tangkapan layar objek navigator.
- `[screen_fg_obj]`: Tangkapan layar jendela aktif di latar depan.
- `[screen_full]`: Tangkapan layar penuh.
- `[file_ocr]`: Memilih file gambar/PDF untuk ekstraksi teks.
- `[file_read]`: Memilih dokumen untuk dibaca (TXT, kode, PDF).
- `[file_audio]`: Memilih file audio untuk dianalisis (MP3, WAV, OGG).

***
**Catatan:** Koneksi internet aktif diperlukan untuk semua fitur AI. Dokumen multi-halaman akan diproses otomatis.

## 5. Dukungan & Komunitas

Ikuti kabar terbaru, fitur baru, dan rilis terbaru:
- **Kanal Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Untuk laporan bug dan permintaan fitur.

## 6. Pendukung Proyek

Terima kasih sebesar-besarnya kepada anggota komunitas yang mendukung pengembangan dan pemeliharaan proyek ini melalui kontribusi finansial:

*   **@Alyabani94**
*   **Ali Alamri**
*   **Ilya**
*   **Anonymous Supporter** (`UQDd...CnMY`)
*   **leonardo0216**
*   **Sergei Fleytin**

*Jika Anda ingin mendukung proyek secara finansial dan ingin nama Anda ditampilkan di sini, buka opsi **Donasi** di menu Tools NVDA (submenu Vision Assistant) atau pada proses pengaturan setelah instalasi.*


---
## Perubahan untuk 7.0.0

*   **Melanjutkan Pemindaian yang Belum Selesai**: Menambahkan fitur lanjutkan untuk Pembaca Dokumen dan Aksi File Cerdas. Jika pemindaian terputus, sekarang Anda dapat melanjutkan dari titik terakhir alih-alih memulai lagi dari awal.
*   **Variabel `[screen_fg_obj]` Baru**: Menambahkan variabel prompt kustom untuk mengambil tangkapan layar hanya dari jendela aktif di latar depan, bukan seluruh layar.
*   **Coba Ulang Cerdas & Rotasi Kunci**: Add-on kini diam-diam mencoba ulang hingga 5 kali pada kunci yang sama saat terjadi beban server sementara, seperti "permintaan tinggi" atau respons tidak valid. Jika percobaan ulang gagal, add-on otomatis beralih ke kunci API berikutnya dalam daftar Anda.
*   **Deteksi Screen Curtain**: Menambahkan pemeriksaan untuk mencegah pengambilan tangkapan layar saat Screen Curtain aktif, baik aktif permanen maupun dinyalakan sementara dengan hotkey. Add-on akan memperingatkan Anda dan berhenti, sehingga Anda tidak mengirim gambar hitam dan membuang token API.
*   **Penyempurnaan Pembaca Dokumen**: Dialog rentang PDF kini otomatis memilih bahasa target default dari pengaturan add-on. Penanganan thread juga ditingkatkan agar tugas latar belakang berhenti dengan bersih saat pembaca ditutup.
*   **Integrasi OCR Mistral Bawaan**: Mengintegrasikan API Document OCR bawaan Mistral. Dokumen multi-halaman otomatis digabung, diunggah, dan diproses secara batch memakai endpoint khusus `/v1/ocr` milik Mistral, sedangkan gambar satu halaman diproses langsung tanpa konversi PDF yang tidak perlu [1].
*   **Penangan URL Kustom Dinamis**: Mengubah URL API Kustom kini langsung menghapus cache daftar model dan mengembalikan kotak teks entri model manual. Ini memastikan kompatibilitas penuh dengan endpoint kustom, seperti Cloudflare AI Gateway, yang tidak mendukung endpoint daftar `/v1/models` standar.
*   **Mesin Input Operator AI Dirombak**: Sistem simulasi mouse dan keyboard dasar untuk Operator AI ditulis ulang sepenuhnya. API lama `mouse_event` diganti dengan API Windows modern `SendInput`, sehingga kompatibilitas dengan aplikasi modern, jendela yang dilindungi UAC, dan tampilan high-DPI jauh lebih baik.
*   **Operasi Seret & Lepas Diperbaiki**: Aksi seret dan lepas di Operator AI kini jauh lebih stabil dan andal. Mesin baru memakai kurva "easing" yang natural, posisi kursor presisi, timing yang dioptimalkan, dan teknik "nudge" cerdas agar Windows dan aplikasi mengenali serta menjalankan gestur seret-dan-lepas dengan benar tanpa gagal di tengah jalan.
*   **Dukungan Multi-Monitor**: Operator AI kini mendukung penuh setup multi-monitor. Gerakan dan klik mouse bekerja benar di semua monitor memakai flag `MOUSEEVENTF_VIRTUALDESK`, sehingga posisi tetap akurat di monitor mana pun aplikasi target berada.
*   **Simulasi Keyboard Ditingkatkan**: Injeksi tombol ditingkatkan agar mendukung penuh "Extended Keys", seperti tombol panah, Home, End, Page Up/Down, Insert, Delete, dan F1-F12. Ini memastikan navigasi dan perintah pintasan yang dikirim Operator AI berjalan lancar di semua aplikasi.
*   **Dukungan Gambar HEIC/HEIF**: Menambahkan dukungan bawaan untuk format foto iPhone. Sekarang Anda dapat langsung memilih file `.heic` dan `.heif` untuk deskripsi AI, OCR, atau Pembacaan Dokumen tanpa konversi lebih dulu.

## Perubahan untuk 6.5.0

*   **Asisten Langsung**: Menambahkan fitur asisten suara dan layar secara real-time, tersedia secara eksklusif untuk penyedia Google Gemini (atau penyedia kustom yang kompatibel dengan Gemini). Termasuk kustomisasi suara interaktif dan kedalaman berpikir langsung di dalam dialog, dengan rekoneksi otomatis setelah mengubah pengaturan.
*   **Penyedia AI MiniMax**: Mengintegrasikan MiniMax sebagai penyedia setara dengan dukungan multimodal penuh (obrolan, visi, OCR), TTS kustom menggunakan lebih dari 300+ suara dinamis, dan penghapusan blok penalaran secara otomatis (misalnya, `<think>...</think>`) dari keluaran.
*   **Terjemahan Penampil Dokumen**: Memperbaiki kegagalan terjemahan diam-diam untuk pengguna NVDA non-Inggris dengan memastikan kode bahasa 2 huruf standar dikirim ke Google Translate alih-alih nama bahasa yang dilokalkan.
*   **Coba Lagi Pemindaian Batch PDF**: Mengimplementasikan logika coba lagi yang sangat dioptimalkan, terpisah, dan diam-diam untuk pemindaian batch dokumen PDF guna mencegah pengunggahan berulang dan menghindari popup kesalahan yang mengganggu selama proses coba lagi.
*   **Status Penampil Dokumen**: Memperbaiki bug di mana status keseluruhan plugin (diperiksa melalui `I`) tetap macet di "Pemrosesan Batch Dimulai" selama pemindaian dokumen yang panjang.
*   **Perbaikan Crash Threading**: Memperbaiki crash pernyataan thread `IsMain() failed in wxTimerImpl` yang parah saat membuka dokumen dari thread latar belakang dengan memindahkan antrean callback GUI ke `wx.CallAfter`.

## Perubahan untuk 6.1.2

*   **Pemeriksaan Awal Label Duplikat**: Memperbaiki masalah pada pelabelan tunggal ketika pemeriksaan duplikat masih memakai kunci koordinat lama, sehingga NVDA membuat permintaan AI ganda untuk objek yang sudah diberi label alih-alih mengumumkan label yang ada.
*   **Obrolan Dokumen untuk Penyedia Non-Gemini**: Memperbaiki pemeriksaan kunci API yang terlalu ketat di Obrolan Dokumen (`on_ask`) agar pengguna OpenAI, Groq, atau penyedia Kustom lokal seperti Ollama dapat mengobrol dengan dokumen tanpa diblokir.
*   **Terjemahan OCR Chrome Cepat**: Mengembalikan API terjemahan gratis tanpa kunci untuk OCR Chrome. Terjemahan teks hasil ekstraksi kini melewati AI Gemini, sehingga kuota API lebih hemat dan proses terjemahan lebih cepat.
*   **Filter Alfanumerik CAPTCHA**: Memperbaiki logika filter di pemecah CAPTCHA agar karakter non-alfanumerik dibersihkan dengan benar dalam semua situasi.
*   **Pembaruan Bantuan Lapisan Perintah**: Memperbaiki pintasan pengumuman status di menu bantuan dari `L` menjadi `I`, dan menambahkan kedua perintah pelabelan (`L` dan `Shift+L`) ke daftar.

## Perubahan untuk 6.1.1

*   **Perbaikan Output Thinking Gemma 4**: Memperbaiki masalah pada model Gemma 4 ketika seluruh proses berpikir internal ditampilkan sebagai respons akhir, atau ketika menonaktifkan thinking menghasilkan respons kosong. Add-on kini memisahkan dan mengambil hanya teks akhir yang bersih.
*   **OCR Batch dari File Explorer**: Anda kini dapat memilih beberapa foto atau PDF langsung di Windows File Explorer dan mengekstrak teks atau menganalisisnya secara batch. Add-on akan otomatis memfilter dan memproses hanya format file yang didukung.

## Perubahan untuk 6.1.0

*   **Integrasi AI Lokal Universal (Siapkan AI Lokal)**: Menambahkan tombol **"Siapkan AI Lokal"** baru di Pengaturan Penyedia Kustom. Pengguna kini dapat mengonfigurasi mesin AI lokal seperti **Ollama**, **LM Studio**, **Jan.ai**, dan **KoboldCPP** secara otomatis dan instan.
*   **Bypass Proksi Lokal Cerdas**: Logika koneksi dibangun ulang dengan mekanisme bypass proksi lanjutan. Add-on kini dapat melewati proksi sistem Windows sepenuhnya untuk koneksi loopback lokal, sehingga koneksi AI lokal tetap stabil meskipun VPN atau mode TUN sedang aktif.
*   **Pelabelan AI Sangat Stabil (v2)**: Kunci berbasis koordinat layar absolut diganti dengan sistem **Object Signature** hibrida yang lebih canggih. Label kini mengandalkan pengenal programatik seperti UIA **AutomationId** atau Win32 **ControlID**, serta koordinat relatif jendela, sehingga label kustom tahan terhadap perubahan ukuran atau posisi jendela, perpindahan monitor, dan scaling.
*   **Migrasi Label Otomatis yang Mulus**: Proses upgrade berjalan transparan. Add-on akan memigrasikan label lama berbasis koordinat ke format sidik jari baru yang stabil di latar belakang saat fokus pertama kali, tanpa kehilangan data.

## Perubahan untuk 6.0

*   **Memperkenalkan Pelabelan AI Semantik**: Pengguna kini dapat memberi label permanen pada tombol dan ikon tanpa nama menggunakan AI. Tekan **L** untuk memberi label pada objek navigator saat ini (mendukung fokus Tab dan navigasi objek), atau **Shift+L** untuk memindai dan memberi label seluruh aplikasi sekaligus.
*   **Pengelolaan Label Cerdas**: Menambahkan dialog Pengelola Label baru yang sepenuhnya aksesibel (melalui **Shift+L** jika label sudah ada) untuk melihat, mengganti nama, atau menghapus banyak label kustom sekaligus.
*   **Analisis File Langsung (Tanpa Dialog File)**: Add-on kini dapat mendeteksi saat fokus berada pada file PDF atau gambar di Windows File Explorer. Menekan **F (Aksi File Cerdas)** atau **D (Pembaca Dokumen)** pada file yang disorot akan langsung memprosesnya, tanpa membuka dialog "Open" standar.

## Perubahan untuk 5.6

*   **Menambahkan Mesin OCR "Tidak Ada (Ambil Lapisan Teks)"**: Pengguna kini dapat mengambil teks langsung dari PDF yang sudah memiliki lapisan teks tanpa memakai kredit AI. Ini membuat proses lebih cepat dan lebih privat untuk dokumen berbasis teks.
*   **Akurasi UI Explorer Ditingkatkan**: Prompt UI Explorer diperbaiki agar lebih tepat mengenali jenis elemen, seperti item daftar, dan melaporkan status seperti "(Dicentang)", "(Dipilih)", atau "(Diperluas)", sambil mengabaikan komponen sistem Windows seperti Taskbar dan Jam.
*   **Pengingat Pengaturan Setelah Instalasi**: Menambahkan notifikasi setelah instalasi untuk mengarahkan pengguna ke menu pengaturan agar dapat mengonfigurasi kunci API dan preferensi.

## Perubahan untuk 5.5.2

*   **Masalah Pengetikan Operator AI Diperbaiki:** Memperbaiki bug yang membuat huruf 'v' diketik alih-alih menempelkan teks pada sistem tertentu. Perbaikan ini mengatasi konflik timing yang muncul saat beban sistem tinggi.
*   **Stabilitas Ditingkatkan:** Menambahkan penanganan error yang lebih kuat untuk operasi papan klip agar add-on tidak crash saat papan klip sistem sedang dikunci sementara oleh aplikasi lain.
*   **Optimasi Timing:** Menyesuaikan jeda internal untuk event keyboard agar lebih andal di berbagai kecepatan sistem dan lebih kompatibel dengan Clipboard Manager pihak ketiga.

## Perubahan untuk 5.5 (Pembaruan Otomasi)

*   **Operator AI (Kontrol Mandiri - Shift+A):** Ini adalah fitur utama di v5.5. Vision Assistant Pro berkembang dari asisten pasif menjadi **Operator AI** pribadi Anda. Add-on ini tidak hanya mendeskripsikan layar, tetapi juga dapat mengambil tindakan.
    *   *Cara kerja:* Anda kini dapat memberi instruksi lisan atau tertulis untuk mengoperasikan PC. Misalnya, di aplikasi yang sama sekali tidak aksesibel dan pembaca layar tidak memberi informasi, tekan **Shift+A** lalu ketik: *"Klik tombol Pengaturan"* atau *"Cari kolom pencarian, ketik 'Berita Terbaru', lalu tekan enter."* AI akan mengenali elemen secara visual, menggerakkan mouse, dan menjalankan tugas tersebut.
    *   *Catatan performa:* Fitur ini dioptimalkan untuk **Gemini 3.0 Flash (Preview)** sehingga responsnya sangat cepat dan cerdas, bahkan untuk tata letak antarmuka yang rumit.
    *   **Peringatan penggunaan API:** Agar Operator AI bisa bekerja akurat, ia perlu "melihat" kondisi layar dan mengirim tangkapan layar resolusi tinggi pada setiap langkah. Penggunaan yang sering akan menghabiskan kuota API jauh lebih cepat daripada tugas berbasis teks biasa.
*   **Visual UI Explorer (E):** Lelah menghadapi "tombol tanpa label"? Tekan **E** untuk mengaktifkan UI Explorer. AI akan memindai seluruh jendela dan membuat daftar semua elemen yang bisa diklik, termasuk ikon, grafik, dan menu. Pilih item dari daftar, lalu Operator AI akan mengkliknya untuk Anda. Anggap saja seperti lapisan aksesibilitas tambahan di atas aplikasi apa pun.
*   **Aksi File Cerdas Berbasis Konteks (F):** Tombol **F** dirombak total. Fitur ini tidak lagi menganggap Anda selalu ingin OCR. Saat Anda memilih satu gambar, add-on akan menanyakan tujuan Anda: pilih **Deskripsi Visual Terperinci** untuk memahami isi gambar, atau **Ekstraksi Teks Terstruktur (OCR)** untuk membaca teks. Menu akan menyesuaikan secara dinamis berdasarkan jenis file dan mesin AI yang aktif.
*   **Optimasi Inti:** Logika internal add-on dibersihkan secara menyeluruh dengan menghapus fungsi lama yang tidak dipakai dan kode yang berulang. Hasilnya adalah pengalaman yang lebih ringan, cepat, dan andal untuk semua pengguna.

## Perubahan untuk 5.0

* **Arsitektur Multi-Penyedia**: Menambahkan dukungan penuh untuk **OpenAI**, **Groq**, dan **Mistral** selain Google Gemini. Pengguna kini dapat memilih backend AI yang diinginkan.
* **Perutean Model Lanjutan**: Pengguna penyedia bawaan seperti Gemini dan OpenAI kini dapat memilih model tertentu dari daftar dropdown untuk berbagai tugas, seperti OCR, STT, dan TTS.
* **Konfigurasi Titik Akhir Lanjutan**: Pengguna penyedia kustom dapat memasukkan URL dan nama model tertentu secara manual untuk kontrol lebih rinci atas server lokal atau layanan pihak ketiga.
* **Visibilitas Fitur Cerdas**: Menu pengaturan dan antarmuka Pembaca Dokumen kini otomatis menyembunyikan fitur yang tidak didukung, seperti TTS, berdasarkan penyedia yang dipilih.
* **Pengambilan Model Dinamis**: Add-on kini mengambil daftar model yang tersedia langsung dari API penyedia, sehingga tetap kompatibel dengan model baru segera setelah dirilis.
* **OCR & Terjemahan Hybrid**: Logika dioptimalkan agar memakai Google Translate untuk kecepatan saat menggunakan Chrome OCR, dan terjemahan berbasis AI saat memakai mesin Gemini, Groq, atau OpenAI.
* **"Pindai ulang dengan AI" Universal**: Fitur pindai ulang di Pembaca Dokumen tidak lagi terbatas pada Gemini. Fitur ini memakai penyedia AI apa pun yang sedang aktif untuk memproses ulang halaman.

## Perubahan untuk 4.6
* **Pembukaan Ulang Hasil Interaktif:** Menambahkan tombol **Space** pada Lapisan Perintah, sehingga pengguna bisa langsung membuka kembali respons AI terakhir di jendela obrolan untuk pertanyaan lanjutan, bahkan saat mode "Output Langsung" aktif.
* **Pusat Komunitas Telegram:** Menambahkan tautan "Kanal Telegram Resmi" di menu Tools NVDA, agar pengguna lebih cepat mengikuti kabar, fitur, dan rilis terbaru.
* **Stabilitas Respons Ditingkatkan:** Mengoptimalkan logika inti fitur Terjemahan, OCR, dan Visi agar performa lebih andal dan pengalaman output suara langsung lebih mulus.
* **Panduan Antarmuka Ditingkatkan:** Deskripsi pengaturan dan dokumentasi diperbarui agar sistem pembukaan ulang hasil terakhir lebih mudah dipahami, termasuk cara kerjanya bersama pengaturan output langsung.

## Perubahan untuk 4.5
* **Pengelola Prompt Lanjutan:** Menambahkan dialog khusus di pengaturan untuk menyesuaikan prompt sistem bawaan dan mengelola prompt buatan pengguna, termasuk tambah, edit, urut ulang, dan pratinjau.
* **Dukungan Proksi Menyeluruh:** Memperbaiki masalah koneksi dengan memastikan proksi yang diatur pengguna diterapkan secara ketat ke semua permintaan API, termasuk terjemahan, OCR, dan pembuatan suara.
* **Migrasi Data Otomatis:** Menambahkan sistem migrasi cerdas untuk memperbarui konfigurasi prompt lama ke format JSON v2 yang lebih kuat saat pertama kali dijalankan, tanpa kehilangan data.
* **Kompatibilitas Diperbarui (2025.1):** Menetapkan NVDA versi minimum 2025.1 karena ketergantungan pustaka pada fitur lanjutan seperti Pembaca Dokumen.
* **Antarmuka Pengaturan Dioptimalkan:** Pengaturan dibuat lebih rapi dengan memindahkan manajemen prompt ke dialog terpisah, sehingga pengalaman pengguna lebih bersih dan aksesibel.
* **Panduan Variabel Prompt:** Menambahkan panduan bawaan di dialog prompt agar pengguna mudah mengenali dan memakai variabel dinamis seperti [selection], [clipboard], dan [screen_obj].

## Perubahan untuk 4.0.3
*   **Ketahanan Jaringan Ditingkatkan:** Menambahkan mekanisme coba ulang otomatis untuk menangani koneksi internet tidak stabil dan error server sementara, sehingga respons AI lebih andal.
*   **Dialog Terjemahan Visual:** Menambahkan jendela khusus untuk hasil terjemahan. Pengguna dapat menelusuri dan membaca terjemahan panjang baris demi baris, mirip hasil OCR.
*   **Tampilan Terformat Gabungan:** Fitur "View Formatted" di Pembaca Dokumen kini menampilkan semua halaman yang diproses dalam satu jendela terstruktur dengan header halaman yang jelas.
*   **Alur OCR Dioptimalkan:** Pemilihan rentang halaman otomatis dilewati untuk dokumen satu halaman, sehingga proses pengenalan lebih cepat dan mulus.
*   **Stabilitas API Ditingkatkan:** Beralih ke metode autentikasi berbasis header yang lebih kuat untuk mengatasi potensi error "All API Keys failed" akibat konflik rotasi kunci.
*   **Perbaikan Bug:** Memperbaiki beberapa potensi crash, termasuk masalah saat add-on dihentikan dan error fokus di dialog obrolan.

## Perubahan untuk 4.0.1
*   **Pembaca Dokumen Lanjutan:** Penampil baru yang kuat untuk PDF dan gambar, dengan pilihan rentang halaman, pemrosesan latar belakang, dan navigasi `Ctrl+PageUp/Down` yang mulus.
*   **Submenu Tools Baru:** Menambahkan submenu khusus "Vision Assistant" di menu Tools NVDA untuk akses cepat ke fitur utama, pengaturan, dan dokumentasi.
*   **Kustomisasi Fleksibel:** Anda kini dapat memilih mesin OCR dan suara TTS langsung dari panel pengaturan.
*   **Dukungan Multi Kunci API:** Menambahkan dukungan beberapa kunci API Gemini. Anda dapat memasukkan satu kunci per baris atau memisahkannya dengan koma di pengaturan.
*   **Mesin OCR Alternatif:** Menambahkan mesin OCR baru agar pengenalan teks tetap andal saat kuota Gemini API habis.
*   **Rotasi Kunci API Cerdas:** Add-on otomatis beralih ke kunci API yang berfungsi paling cepat dan mengingatnya untuk melewati batas kuota.
*   **Dokumen ke MP3/WAV:** Menambahkan kemampuan membuat dan menyimpan file audio berkualitas tinggi dalam format MP3 (128kbps) dan WAV langsung dari pembaca.
*   **Dukungan Instagram Stories:** Menambahkan kemampuan untuk mendeskripsikan dan menganalisis Instagram Stories melalui URL.
*   **Dukungan TikTok:** Menambahkan dukungan video TikTok untuk deskripsi visual lengkap dan transkripsi audio klip.
*   **Dialog Pembaruan Didesain Ulang:** Menghadirkan antarmuka baru yang aksesibel dengan kotak teks yang dapat digulir, sehingga perubahan versi mudah dibaca sebelum instalasi.
*   **Status & UX Diseragamkan:** Menyeragamkan dialog file di seluruh add-on dan meningkatkan perintah 'L' agar dapat melaporkan progres secara real-time.

## Perubahan untuk 3.6.0
*   **Sistem Bantuan:** Menambahkan perintah bantuan (`H`) di dalam Lapisan Perintah untuk menampilkan daftar pintasan dan fungsinya dengan mudah.
*   **Analisis Video Online:** Dukungan diperluas ke video **Twitter (X)**. Deteksi URL dan stabilitas juga ditingkatkan agar lebih andal.
*   **Kontribusi Proyek:** Menambahkan dialog donasi opsional bagi pengguna yang ingin mendukung pembaruan dan perkembangan proyek di masa depan.

## Perubahan untuk 3.5.0
*   **Lapisan Perintah:** Menambahkan sistem Lapisan Perintah (default: `NVDA+Shift+V`) untuk mengelompokkan pintasan di bawah satu tombol utama. Misalnya, alih-alih menekan `NVDA+Control+Shift+T` untuk menerjemahkan, kini Anda cukup menekan `NVDA+Shift+V`, lalu `T`.
*   **Analisis Video Online:** Menambahkan fitur baru untuk menganalisis video YouTube dan Instagram langsung dari URL.

## Perubahan untuk 3.1.0
*   **Mode Output Langsung:** Menambahkan opsi untuk melewati dialog obrolan dan mendengar respons AI langsung melalui suara, agar lebih cepat dan mulus.
*   **Integrasi Papan Klip:** Menambahkan pengaturan baru untuk menyalin respons AI ke papan klip secara otomatis.

## Perubahan untuk 3.0

*   **Bahasa Baru:** Menambahkan terjemahan **Persia** dan **Vietnam**.
*   **Model AI Diperluas:** Daftar pilihan model ditata ulang dengan awalan yang jelas (`[Free]`, `[Pro]`, `[Auto]`) agar pengguna dapat membedakan model gratis dan model berbayar atau terbatas kuota. Dukungan untuk **Gemini 3.0 Pro** dan **Gemini 2.0 Flash Lite** juga ditambahkan.
*   **Stabilitas Dikte:** Stabilitas Dikte Cerdas ditingkatkan secara signifikan. Klip audio yang lebih pendek dari 1 detik kini diabaikan untuk mencegah halusinasi AI dan error kosong.
*   **Penanganan File:** Memperbaiki masalah yang membuat unggahan file dengan nama non-Inggris gagal.
*   **Optimasi Prompt:** Memperbaiki logika terjemahan dan menyusun hasil fitur visi agar lebih terstruktur.
## Perubahan untuk 2.9

*   **Menambahkan terjemahan Prancis dan Turki.**
*   **Tampilan Terformat:** Menambahkan tombol "View Formatted" di dialog obrolan untuk melihat percakapan dengan format yang benar, seperti heading, teks tebal, dan kode, di jendela standar yang dapat dijelajahi.
*   **Pengaturan Markdown:** Menambahkan opsi "Clean Markdown in Chat" di Pengaturan. Jika opsi ini tidak dicentang, pengguna dapat melihat sintaks Markdown mentah, misalnya `**` dan `#`, di jendela obrolan.
*   **Manajemen Dialog:** Memperbaiki masalah yang membuat jendela "Refine Text" atau obrolan terbuka berkali-kali atau gagal mendapatkan fokus.
*   **Peningkatan UX:** Menyeragamkan judul dialog file menjadi "Open" dan menghapus pengumuman suara yang tidak perlu, seperti "Opening menu...", agar pengalaman lebih mulus.

## Perubahan untuk 2.8
* Menambahkan terjemahan bahasa Italia.
* **Laporan Status:** Menambahkan perintah baru (NVDA+Control+Shift+I) untuk mengumumkan status add-on saat ini, misalnya "Uploading..." atau "Analyzing...".
* **Ekspor HTML:** Tombol "Save Content" di dialog hasil kini menyimpan output sebagai file HTML terformat, termasuk gaya seperti heading dan teks tebal.
* **UI Pengaturan:** Tata letak panel pengaturan ditingkatkan dengan pengelompokan yang lebih aksesibel.
* **Model Baru:** Menambahkan dukungan untuk gemini-flash-latest dan gemini-flash-lite-latest.
* **Bahasa:** Menambahkan bahasa Nepal ke daftar bahasa yang didukung.
* **Logika Menu Refine:** Memperbaiki bug penting yang membuat perintah "Refine Text" gagal saat bahasa antarmuka NVDA bukan bahasa Inggris.
* **Dikte:** Meningkatkan deteksi hening agar tidak menghasilkan teks yang salah saat tidak ada ucapan.
* **Pengaturan Pembaruan:** "Check for updates on startup" kini dinonaktifkan secara default agar sesuai dengan kebijakan Add-on Store.
* Pembersihan kode.

## Perubahan untuk 2.7
* Memigrasikan struktur proyek ke Template Add-on resmi NV Access agar lebih sesuai standar.
* Menambahkan logika coba ulang otomatis untuk error HTTP 429 (Rate Limit), agar lebih andal saat trafik tinggi.
* Mengoptimalkan prompt terjemahan untuk akurasi lebih tinggi dan penanganan logika "Smart Swap" yang lebih baik.
* Memperbarui terjemahan Rusia.

## Perubahan untuk 2.6
* Menambahkan dukungan terjemahan Rusia (terima kasih kepada nvda-ru).
* Memperbarui pesan error agar informasi konektivitas lebih jelas.
* Mengubah bahasa target default ke bahasa Inggris.

## Perubahan untuk 2.5
* Menambahkan perintah OCR file bawaan (NVDA+Control+Shift+F).
* Menambahkan tombol "Save Chat" di dialog hasil.
* Menambahkan dukungan lokalisasi penuh (i18n).
* Memigrasikan umpan balik audio ke modul tones bawaan NVDA.
* Beralih ke Gemini File API untuk menangani PDF dan file audio dengan lebih baik.
* Memperbaiki crash saat menerjemahkan teks yang berisi kurung kurawal.

## Perubahan untuk 2.1.1
* Memperbaiki masalah variabel [file_ocr] yang tidak berfungsi dengan benar di Prompt Kustom.

## Perubahan untuk 2.1
* Menstandarkan semua pintasan agar memakai NVDA+Control+Shift untuk menghindari konflik dengan layout Laptop NVDA dan hotkey sistem.

## Perubahan untuk 2.0
* Menambahkan sistem Auto-Update bawaan.
* Menambahkan Smart Translation Cache untuk mengambil kembali teks yang pernah diterjemahkan secara instan.
* Menambahkan Conversation Memory untuk menyempurnakan hasil secara kontekstual di dialog obrolan.
* Menambahkan perintah khusus Terjemahan Papan Klip (NVDA+Control+Shift+Y).
* Mengoptimalkan prompt AI agar benar-benar mengikuti bahasa target.
* Memperbaiki crash akibat karakter khusus pada teks masukan.

## Perubahan untuk 1.5
* Menambahkan dukungan untuk lebih dari 20 bahasa baru.
* Menambahkan Dialog Refine Interaktif untuk pertanyaan lanjutan.
* Menambahkan fitur Dikte Cerdas bawaan.
* Menambahkan kategori "Vision Assistant" di dialog Input Gestures NVDA.
* Memperbaiki crash COMError pada aplikasi tertentu seperti Firefox dan Word.
* Menambahkan mekanisme coba ulang otomatis untuk error server.

## Perubahan untuk 1.0
* Rilis awal.
