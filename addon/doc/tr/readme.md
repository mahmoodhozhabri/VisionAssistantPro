# Profesyonel Görsel Asistan Belgeleri

<!-- DOWNLOAD_COUNT_START --> Toplam indirme: 75,451 <!-- DOWNLOAD_COUNT_END -->

**Profesyonel Görsel Asistan**, NVDA için gelişmiş, çok modlu bir yapay zekâ asistanıdır. Akıllı ekran okuma, çeviri, sesli dikte ve belge analizi sağlamak için dünya çapında yapay zekâ motorlarından yararlanır.

Bu eklenti, Uluslararası Engelliler Günü onuruna topluluğun kullanımına sunulmuştur

## 1. Kurulum ve Yapılandırma

**NVDA Menüsü > Tercihler > Ayarlar > Profesyonel Görsel Asistan** yolunu izleyin. Ayarlar iletişim kutusu, erişilebilir 8 sekmeden oluşur: **Bağlantı**, **Yapay Zekâ Davranışı**, **Çeviri Dilleri**, **Belge Okuyucu**, **Video**, **CAPTCHA**, **İstemler** ve **Gelişmiş**.

### 1.1 Bağlantı Sekmesi

- **Sağlayıcı:** Tercih ettiğiniz yapay zekâ hizmetini seçin. Desteklenen sağlayıcılar arasında **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** ve **Özel** (Ollama, LM Studio, Jan.ai veya KoboldCPP gibi OpenAI uyumlu sunucular) bulunur.
- **API Anahtarı:** Otomatik dönüşümlü kullanım için tek bir API anahtarı veya birden fazla API anahtarı girin (virgül ya da yeni satır ile ayrılmış).
- **Modelleri Al:** API anahtarınızı girdikten sonra, sağlayıcıdan en güncel kullanılabilir model listesini indirmek için bu düğmeye basın.
- **Yapay Zekâ Modeli:** Genel sohbet ve analiz için kullanılacak ana modeli seçin.
- **Gelişmiş Model Yönlendirme (Göreve Özel):** İsteğe bağlı olarak OCR, STT, TTS, AI Operator, Video ve Canlı Asistan görevleri için açılır listelerden özel modeller seçin. Gemini'de modeller, karmaşa yaratmadan yeteneklerine göre dinamik olarak kategorize edilir.
- **Özel Sağlayıcı Ayarları:** Yerel veya özel uç noktaları yapılandırın. **Yerel Yapay Zekâyı Kur** (Ollama, LM Studio, Jan.ai veya KoboldCPP için tek tıklamayla kurulum) ve **Gelişmiş Uç Nokta Yapılandırması** seçeneklerini içerir.
- **Proxy Yapılandırması:** Eklentinin tamamında (Canlı Asistan, Ortam Gözlemcisi ve Metin Okuma dahil) tünelleme ve uç nokta yönlendirme için tam destek. **Proxy URL'nizi** girin ve **Proxy Modunuzu** seçin:
  - **Otomatik algılama:** URL'nin ileri proxy mi yoksa ters proxy mi olduğunu otomatik olarak algılar.
  - **SOCKS5 Proxy:** RFC 1929 kullanıcı adı/şifre kimlik doğrulaması ve alan adı çözümlemesi ile SOCKS5 üzerinden ileri tünellemeyi zorlar.
  - **HTTP Proxy:** İleri tünelleme işlemini Temel kimlik doğrulama ile bir HTTP proxy'si üzerinden zorlar.
  - **Ters Proxy:** Özel yapay zeka ağ geçitleri ve kendi kendine barındırılan aynalar için doğrudan uç nokta değiştirme (bu modda kimlik bilgileri devre dışı bırakılır).
- **Proxy Bağlantısını Test Et:** Bağlantıyı test eden ve sunucu gecikmesini milisaniye cinsinden (NVDA aracılığıyla sesli olarak) ölçen, engellemeyen bir düğme.
- **Bağlantı ve Çıktı Seçenekleri:** Proxy URL'si, başlangıçta güncelleme denetimi, Sohbette Markdown'ı Temizle, Yapay zekâ yanıtlarını panoya kopyala, Doğrudan Çıktı (Sohbet Penceresi Yok) seçeneklerini yapılandırın.
- **Sohbetleri Geçmişe Kaydet:** Sohbetlerinizi Geçmiş listesinde saklayın.

### 1.2 Canlı Asistan Sekmesi

- **Canlı Asistan: Doğrudan Çıktı (Penceresiz):** Canlı Asistan’ı konuşma penceresi olmadan başlatın; daha sonra “Son Sonucu Çağır” tuşuyla (`Boşluk`) açabilirsiniz.
- **Bas-Konuş:** Bas-konuş modunu etkinleştirin veya devre dışı bırakın. Etkinleştirildiğinde, mikrofonunuz yalnızca atanmış tuşu basılı tuttuğunuz sürece ses gönderir.
- **Bas Konuş Tuşu:** Kısayolu kaydetmek için tuşlara basın (örneğin `F12` veya `Ctrl+F12`) — hatta `Sol Ctrl` gibi tek bir değiştirici tuş atayabilirsiniz. Konuşmak için tuşu basılı tutun ve bırakın...

Not: Bu sekme yalnızca **Google Gemini** (veya Gemini uyumlu bir Özel sağlayıcı) etkin sağlayıcınız olduğunda görünür.

### 1.3 Yapay Zeka Davranışı Sekmesi

- **Yaratıcılık (Temperature):** Yapay zekânın rastgelelik ve yaratıcılık düzeyini kontrol eder (0,0 ile 2,0 arasında). Daha düşük değerler, daha tutarlı ve daha doğru çeviri/OCR sonuçları üretir.

### 1.4 Çeviri Dilleri Sekmesi

- **Kaynak Dil:** Varsayılan giriş dilinizi seçin.
- **Hedef Dil:** Birincil hedef çeviri dilinizi seçin.
- **Yapay Zekâ Yanıt Dili:** Genel yapay zekâ yanıtları için kullanılacak dili seçin.
- **Akıllı Değişim:** Algılanan giriş diline göre kaynak ve hedef dilleri otomatik olarak değiştirir.

### 1.5 Belge Okuyucu Sekmesi

- **OCR Motoru:** Hızlı sonuçlar için **Chrome (Hızlı)** veya üstün düzen koruması için **YZ (Gelişmiş)** seçeneklerinden birini seçin.
- **OCR Toplu İşlem Boyutu:** İstek başına işlenecek sayfa sayısını belirtin (tek istekle işleme için 0 olarak ayarlayın).
- **Satır İçi Görsel Betimlemeleri:** Belge metni çıkarılırken görseller için satır içi açıklamaları açıp kapatın.
- **Sayfa Numaralarını Dışa Aktar:** Çok sayfalı belge çıktılarında sayfa numaralarını ve ayırıcıları eklemeyi açıp kapatın.
- **TTS Sesi:** Ses oluşturma için kullanılacak varsayılan ses stilini seçin.
- **Belgeleri Geçmişe Kaydet:** Açık belgeleri Geçmiş listesinde saklayın; önbelleğe alınmış OCR metni ve devam verileri kaydedilmeye devam eder.

### 1.6 Video Sekmesi

- **Video Parça Boyutu:** Sesli Betimleme oluşturulurken kullanılacak bölüm süresini dakika cinsinden belirleyin (tüm dosyayı işlemek için 0 olarak ayarlayın).
- **Karakter Listesi Ekle:** Karakter sözlüğünü ilk altyazı girdisi olarak ekleme seçeneği.
- **Yapay Zekâ Sorumluluk Reddi Ekle:** Video SRT altyazılarının başına yapay zekâ tarafından oluşturulduğunu belirten bir sorumluluk reddi metni ekleme seçeneği.
- **Karakter Sözlüğü ve Dizi Yönetimi:** Dizi başına karakter adlarını, fiziksel tanımlarını ve rollerini ekleyin, düzenleyin, içe aktarın veya yönetin — yapay zeka, keşfedilen karakterleri otomatik olarak sözlüğünüzle eşleştirir ve daha fazla bölüm analiz ettikçe yenilerini birleştirir. Manuel notlarınız her zaman yapay zeka güncellemelerine göre öncelikli olarak korunurken, fiziksel betimlemeler bölümler arasında güncel kalır.

### 1.7 CAPTCHA Sekmesi

- **Görsel CAPTCHA Çözücüyü Etkinleştir:** Görsel doğrulama sınamalarının (hCaptcha, reCAPTCHA) otomatik olarak çözülmesini açıp kapatın.
- **Metin CAPTCHA Yöntemi:** **Gezgin Nesnesi (Navigator Object)** veya **Tam Ekran** yakalama yöntemlerinden birini seçin.

### 1.8 İstemler (Prompts) Sekmesi

- **İstemleri Yönet:** Varsayılan sistem istemlerini özelleştirebileceğiniz veya dinamik değişkenler (ör. `[selection]`, `[screen_fg_obj]`) kullanarak kullanıcı tanımlı istemler oluşturabileceğiniz, düzenleyebileceğiniz, yeniden sıralayabileceğiniz ve önizleyebileceğiniz özel bir iletişim kutusunu açar.
- **Özel İstem Kısayolları:** Doğrudan İstem Yöneticisi'nde herhangi bir özel istem için özel bir kısayol tuşu atayın. Bunları kaydetmek için tuşlara basın; tek tuşlar Komut Katmanı içinde (ve genel olarak "NVDA + Shift + tuş" olarak) çalıştırılırken, "Kontrol + Shift + 1" gibi kombinasyonlar genel olarak kendi başlarına çalışır.
- **İstem Başına Geri Bildirim Davranışı:** Her bir isteğin sonucunu nasıl göstereceğini ayrı ayrı seçin (Genel ayar, Panoya kopyala, Doğrudan Çıktı / NVDA mesajı, Panoya kopyala + Doğrudan Çıktı veya Sohbet penceresi).

### 1.9 Gelişmiş Sekmesi ve Genel Günlük Kaydı

Genel eklenti günlük kaydı ayarlarını yapılandırmak için **Gelişmiş** sekmesine gidin:

- **Özel günlük dosyasını etkinleştir:** Eklentinin tüm modüllerindeki işlemler, API trafiği ve hataların ayrı bir dosyaya (`vision_assistant.log`) kaydedilmesini açıp kapatır.
- **Günlük Düzeyi:** Ayrıntı düzeyini **Hata Ayıklama (Tüm Ayrıntılar)**, **Bilgi (Genel Bilgiler)**, **Uyarı (Yalnızca Uyarılar)** ve **Hata (Yalnızca Hatalar)** seçenekleri arasından belirleyin.
- **Günlükleri Saklama Süresi:** Eski günlük kayıtlarının otomatik olarak temizlenmesi için saklama süresini ayarlayın (1 saat ile 90 gün arasında).
- **Günlük Yönetim Denetimleri:** NVDA'yı yeniden başlatmadan veya standart NVDA günlüklerine müdahale etmeden günlük verilerini incelemek ya da temizlemek için **Günlük Dosyasını Aç**, **Günlük Klasörünü Aç** veya **Günlük Dosyasını Temizle** seçeneklerini kullanın.
- **Birleşik Veri Dizini:** Tüm eklenti veri dosyaları (geçmiş, seriler, etiketler, OCR ilerlemesi, önbellekler ve günlükler) NVDA yapılandırma dizininizdeki tek bir `VisionAssistant` klasöründe saklanır; bu da her şeyi düzenli tutar ve manuel yedeklemeleri zahmetsiz hale getirir.

### 1.10 Ayarları Yedekleme ve Geri Yükleme

**Gelişmiş** sekmesi aynı zamanda **Yedekle ve Geri Yükle** bölümünü de içerir:

- **Yedekleme:** Yapılandırmanızı tek bir JSON dosyasına kaydeder. Tıkladığınızda nelerin dahil edileceğini seçersiniz: **Her şey** (ayarlar, özel etiketler, OCR ilerleme durumu ve geçmiş) veya **Yalnızca Ayarlar**.
- **Geri Yükle:** Yapılandırmanızı ve verilerinizi istediğiniz zaman, herhangi bir makineye veya NVDA'yı yeniden yükledikten sonra geri yüklemek için önceden kaydedilmiş bir yedeklemeyi yükler. Geri yükleme işlemi tüm mevcut ayarlarınızın ve verilerinizin yerini alacağından, önce sizden onaylamanız istenecektir.

## 2. Gemini API Anahtar Yöneticisi

**aistudio.google.com** adresinde bir Gemini API anahtarı oluşturmak, eklentinin en zor adımıydı. Ekran okuyucu kullanıldığında sayfalar kafa karıştırıcıydı ve bazı kişiler hiç anahtar oluşturamıyordu. **Gemini API Anahtar Yöneticisi** bu sorunu çözüyor. Komut Katmanında **G** tuşuna basın veya **NVDA Menüsü > Tercihler > Ayarlar > Profesyonel Görsel Asistan > Bağlantı** yolunu izleyerek **Gemini API Anahtarı Al...** seçeneğine tıklayın.

- **Giriş Yapma:** Yöneticiyi açtığınızda, varsayılan tarayıcınız doğrudan Google'ın güvenli giriş sayfasına yönlendirilecektir. Google hesabınızla oturum açın; harici araçlara, SDK'lara veya komut satırı kurulumlarına gerek yoktur. Oturum açtığınız hesap her zaman **Çıkış Yap** düğmesinde gösterilir.
- **Anahtar Oluşturma:** Giriş yaptıktan sonra, önceden herhangi bir kurulum yapmanıza gerek kalmadan **Yeni Proje ve Anahtar** seçeneğiyle hemen bir anahtar oluşturabilirsiniz. Eğer halihazırda mevcut projeleriniz varsa, bunlar basit bir listede görünür; buradan birini seçip **Seçilen Proje için Anahtar Oluştur** düğmesine basabilirsiniz.
- **Sonrasında neler olur:** Yeni tuş hemen panoya kopyalanır, daha sonra kullanılmak üzere eklentiye kaydedilir ve bir kez eklentinin tuş listesine eklenip eklenmeyeceği sorulur. İhtiyacınız olan tek şey bu; aramanız gereken hiçbir web sayfası yok.
- **Anahtarlarınızla Çalışma:** **Seçilen Proje için Anahtarı Kopyala** seçtiğiniz projenin anahtarını kopyalar, **Son Oluşturulan Anahtarı Kopyala** az önce oluşturduğunuz anahtarı kopyalar ve **Kaydedilen Anahtarları CSV'ye Aktar...** oluşturduğunuz her şeyi bir dosyaya kaydeder.
- **Anahtar silme:** **Anahtar Sil...** seçeneği, seçilen projede bulunan anahtarları gösterir, hangisini kaldırmak istediğinizi sorar ve silmeden önce onayınızı ister. Bir tuşu silmek, o tuşu eklentinin tuş listesinden de kaldırır, böylece hiçbir bozuk tuş kullanım listesinde kalmaz. Eklenti dışında oluşturulan anahtarlar da, hesabınızın ilgili projede yetkiye sahip olması koşuluyla silinebilir.
- **Oturum Kapatma:** **Oturum Kapatma**, bilgisayarınızda kayıtlı oturum açma bilgilerini siler, böylece istediğiniz zaman başka bir hesaba geçebilirsiniz.

## 3. Komut Katmanı ve Kısayollar

Klavye çakışmalarını önlemek için bu eklenti bir **Komut Katmanı** kullanır.

1. Katmanı etkinleştirmek için **NVDA + Shift + V** (Ana Tuş) kombinasyonuna basın (bir bip sesi duyarsınız).
2. Tuşları bırakın ve ardından aşağıdaki tek tuşlardan birine basın:

| Anahtar            | İşlev                                                  | Açıklama                                                                                                                                                                                                                                                                                                 |
| ------------------ | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shift + A**      | **Anonim Destekçi** (`UQDd...CnMY`) | **Otonom Operasyon:** Yapay zekaya ekranınızda bir görev gerçekleştirmesini söyleyin. Tekrar basıldığında devam eden işlemler anında durdurulur.                                                                                                         |
| **E**              | **Kullanıcı Arayüzü Gezgini**                          | **Etkileşimli Tıklama:** Herhangi bir uygulamadaki kullanıcı arayüzü öğelerini tanımlar ve tıklar.                                                                                                                                                                       |
| **T**              | Akıllı Çeviri                                          | Dolaşım imleci altındaki metni veya seçimi çevirir.                                                                                                                                                                                                                                      |
| **Shift + T**      | Panodan Çeviri                                         | Panodaki içeriği çevirir.                                                                                                                                                                                                                                                                |
| **R**              | Metin İyileştirici                                     | Özetleme, dilbilgisi düzeltme, açıklama veya **Özel İstemler** çalıştırır.                                                                                                                                                                                                               |
| **V**              | Nesne Görsel Analizi                                   | Mevcut dolaşım nesnesini betimler.                                                                                                                                                                                                                                                       |
| **O**              | Tam Ekran Görsel Analizi                               | Tüm ekran düzenini ve içeriğini analiz eder.                                                                                                                                                                                                                                             |
| **Shift + V**      | Çevrim İçi Video Analizi                               | **YouTube**, **Instagram**, **TikTok** veya **Twitter (X)** videolarını analiz eder.                                                                                                                                                                                  |
| **Control + V**    | Yerel Video Kaydı                                      | Ekranınızın sessiz bir videosunu kaydeder ve eylemleri ve düzeni analiz eder.                                                                                                                                                                                                            |
| **D**              | Belge Okuyucu                                          | Sayfa aralığı seçimi olan PDF ve görseller için gelişmiş okuyucu.                                                                                                                                                                                                                        |
| **F**              | **Akıllı Dosya Eylemi**                                | Seçilen görüntü, PDF veya TIFF dosyalarından bağlama duyarlı tanıma.                                                                                                                                                                                                                     |
| **M**              | Medya Yazıya Dökme ve Dublaj                           | Ses/video dosyalarını (MP3, WAV, MP4 vb.) hedef dilinize yazıya döker veya dublajını oluşturur.                                                                                                                                                       |
| **C**              | CAPTCHA Çözücü                                         | CAPTCHA’ları yakalar ve çözer (Kamu portalları desteklenir).                                                                                                                                                                                                          |
| **Shift + C**      | Doğrudan Sohbet                                        | Yapay zekâ ile doğrudan metin tabanlı bir sohbet arayüzü açar.                                                                                                                                                                                                                           |
| **S**              | Akıllı Dikte                                           | Konuşmayı metne dönüştürür. Başlatmak için basın, durdurmak/yazmak için tekrar basın.                                                                                                                                                                                    |
| **Control + T**    | Sesli Çeviri                                           | Dil ayarlarınıza göre konuşmayı yazıya döker, çevirir ve sonucu yazar.                                                                                                                                                                                                                   |
| **Kontrol+L**      | **Live Assistant**                                     | **Gerçek Zamanlı Yardımcı Pilot (yalnızca Gemini):** Yapay zeka asistanıyla canlı sesli ve ekran görüşmesini başlatır veya bitirir.                                                                                                                   |
| **Control+A**      | **Canlı Operatör**                                     | **Otonom Bilgisayar Kontrolü (Yalnızca Gemini):** Ekranınızı ve eylemlerinizi yapay zekaya devretmek için canlı bir operatör oturumu başlatır veya sonlandırır.                                                                                       |
| **G**              | **Gemini API Anahtar Yöneticisi**                      | **Web bağlantısı olmadan API anahtarınızı oluşturun (yalnızca Gemini):** Bilgisayarınızın ihtiyaç duyduğu şeyleri ayarlayan, oturum açmak için tarayıcıyı açan ve seçtiğiniz proje için bir anahtar oluşturan, kopyalayan veya silen yöneticiyi açar. |
| **I**              | Durum Raporlaması                                      | Geçerli durumu bildirir (ör. "Taranıyor...", "Boşta").                                                                                                                                                |
| **L**              | **Nesne Etiketleme**                                   | **Anlamsal Yapay Zekâ Etiketleme:** Odaklanılan geçerli nesneyi veya simgeyi kalıcı olarak etiketler.                                                                                                                                                                    |
| **Shift + L**      | **Etiketleri Yönet/Tara**                              | Etiket Yöneticisini açar (etiketler varsa) veya uygulamayı adsız öğelere karşı tarar.                                                                                                                                                                                 |
| **U**              | Güncellemeleri Denetle                                 | Eklentinin en son sürümü için GitHub'ı manuel olarak kontrol eder.                                                                                                                                                                                                                       |
| **Aralık**         | Son Sonucu Çağır                                       | Son yapay zekâ yanıtını inceleme veya devam için sohbet penceresinde gösterir.                                                                                                                                                                                                           |
| **H**              | Komut Yardımı                                          | Komut katmanındaki tüm kısayolların listesini gösterir.                                                                                                                                                                                                                                  |
| **Kontrol + H**    | **Geçmiş**                                             | Tür filtreleri ve Sil/Temizle seçenekleriyle geçmiş sohbetlerinizi ve belgelerinizi listeleyen Geçmiş iletişim kutusunu açar.                                                                                                                                                            |
| **Alt + S**        | Ayarlar                                                | Profesyonel Görsel Asistan Ayarları iletişim kutusunu açar.                                                                                                                                                                                                                              |
| **Alt + Q**        | Tükenen Kota Anahtarları Raporu                        | Günlük kotasını aşan Gemini API anahtarlarının sayısını, hangi modellerin etkilendiğini ve sıfırlanma sürelerini bildirir.                                                                                                                                                               |
| **Alt + M**        | Yönlendirme Denetimi                                   | Özel görevler için gelişmiş yönlendirmede o anda seçili olan yapay zeka modellerini bildirir (varsayılanları atlar).                                                                                                                                                  |
| **Yukarı / Aşağı** | Hızlı Ayarlar Gezintisi                                | Hızlı ayar kategorileri arasında geçiş yapar (Sağlayıcı, Model, Çıktı)... arasında dolaşır.                                                                                                                           |
| **Sol / Sağ**      | Hızlı Ayarı Değiştir                                   | O anda seçili olan hızlı ayarın değerini değiştirir.                                                                                                                                                                                                                                     |

## 4. Sohbet ve Geçmiş

Sohbet pencereleri ve Geçmiş iletişim kutusu tüm özelliklerde çalışır; böylece konuşmaları gözden geçirebilir ve kaldığınız yerden devam edebilirsiniz.

### 3.1 Sohbet Penceresi Kısayolları

Bir sohbet penceresi açıkken (Doğrudan Sohbet, belge sohbeti, hassaslaştırma ve benzeri), konuşmayı aşağıdakilerle inceleyebilirsiniz:

- **Alt + Aşağı:** Sonraki mesajı okuyun.
- **Alt + Yukarı:** Önceki mesajı okuyun.
- **Alt + C:** Geçerli mesajı kopyalayın.

### 3.2 Geçmiş (Kontrol + H)

Türe göre filtrelenebilen (Tümü / Sohbetler / Belgeler) geçmiş sohbetlerinizi ve belgelerinizi içeren **Geçmiş** iletişim kutusunu açmak için Komut Katmanında **Control + H** tuşlarına basın. Otomatik olarak yeniden eklenen ekli dosyalar da dahil olmak üzere sohbete devam etmek için bir sohbet açın veya bir belge açıp okumaya devam edin. Herhangi bir öğeyi kaldırmak için **Sil**'e veya listeyi boşaltmak için **Tümünü Temizle**'ye basın. Belgeler için Sil, yalnızca geçmiş kaydını mı yoksa belgenin önbelleğe alınmış OCR metnini de temizleyip bir sonraki açılışta sıfırdan taramasını mı istediğinizi sorar; seçiminizi hatırlamak için **Bir daha sorma** seçeneği bulunur.

Listede nelerin hatırlanacağını da seçebilirsiniz. **Sohbetleri geçmişe kaydet** (Bağlantı sekmesi) ve **Belgeleri geçmişe kaydet** (Belge Okuyucu sekmesi) seçenekleri varsayılan olarak açıktır ve her ikisi de Hızlı Ayarlar'da değiştirilebilir. Belge seçeneği yalnızca Geçmiş girişini etkiler; önbelleğe alınmış OCR metni ve devam verileri her zaman saklanır.

## 5. Yapay Zekâ Operatörü - Otonom Bilgisayar Kontrolü

**Yapay Zekâ Operatörü**, Profesyonel Görsel Asistan'ı pasif bir okuyucudan bilgisayarınızla sizin adınıza etkileşim kurabilen aktif bir asistana dönüştürür. Ekranı betimlemesini isteyebilir, gördükleri hakkında sorular sorabilir veya hatta kontrolü devralmasını sağlayabilirsiniz; düğmelere tıklayabilir, öğeleri sürükleyebilir, metin yazabilir ve doğal dil komutlarını kullanarak uygulamalar arasında dolaşabilir.

En büyük avantajı ne mi? Tamamen erişilemez yazılımlarda kusursuz şekilde çalışır. Özel bir uygulamada, uzak masaüstünde veya ekran okuyucunuzun tamamen sustuğu bir web sitesinde takılıp kaldıysanız, operatör için bu bir sorun değildir. Çünkü ekranı görsel olarak "gördüğü" için erişilebilirlik etiketi bulunmayan öğeleri bulabilir, okuyabilir ve onlarla etkileşim kurabilir.

### 4.1 Nasıl Çalışır

1. **NVDA + Shift + V** tuşlarına basın, ardından Yapay Zekâ Operatörü iletişim kutusunu açmak için **Shift + A** tuşuna basın (veya doğrudan kısayolu kullanın).
2. Yapmak istediğiniz işlemi düz bir dille yazın (örneğin, "Kaydet düğmesine tıkla", "Hata iletisinde ne yazıyor?" veya "Dosyanın adını final.pdf olarak değiştir").
3. Yapay zekâ ekranınızı analiz edecek, ilgili öğeleri belirleyecek ve işlemi gerçekleştirecek veya yanıtı sağlayacaktır. Bir görev birden fazla adım gerektiriyorsa, operatör görev tamamlanana kadar çalışmaya devam eder.
4. Devam eden bir işlemi anında durdurmak için istediğiniz zaman tekrar **Shift + A** tuşuna basın.

### 4.2 Desteklenen Eylemler

Operatör çok çeşitli komutları anlayabilir:

- **Betimleme ve Yanıtlama:** "Ekran düzenini Betimle" veya "Hata iletisinde ne yazıyor?"
- **Tıklama:** "Kaydet düğmesine tıkla"
- **Sağ Tıklama:** "Dosyaya sağ tıkla"
- **Çift Tıklama:** "Belgeye çift tıkla"
- **Sürükle ve Bırak:** "Belgeyi Arşiv klasörüne sürükle"
- **Yazma:** "Arama kutusuna 'Merhaba Dünya' yaz"
- **Kaydırma:** "Üç kez aşağı kaydır"
- **Tuş Basımı:** "Enter tuşuna bas", "Tab tuşuna bas", "Escape tuşuna bas"
- **Çok Adımlı Görevler:** "Dosya Gezgini'ni aç, raporu bul ve adını final.pdf olarak değiştir"

### 4.3 Önemli Notlar

- **⚠️ API Kullanım Uyarısı:** Operatörün ekranda tam olarak neler olduğunu "görebilmesi" gerektiğinden, her adımda yüksek çözünürlüklü bir ekran görüntüsü gönderilir. Sık kullanım, standart metin tabanlı özelliklere kıyasla API kotanızı çok daha hızlı tüketecektir.
- **Yönetici Uygulamaları:** NVDA yönetici ayrıcalıklarıyla çalışmıyorsa, operatör yükseltilmiş izinler gerektiren pencerelerle etkileşim kuramayabilir. Bu, Windows'un güvenlik sınırlamasıdır, eklentideki bir hata değildir.
- **En İyi Uygulamalar:** En iyi sonuçlar için açık ve belirgin komutlar verin. "Formun altındaki mavi Gönder düğmesine tıkla" komutu, yalnızca "Düğmeye tıkla" demekten neredeyse her zaman daha iyi sonuç verir.

### 4.4 Canlı Operatör (Kontrol+A)

Canlı Asistan, Profesyonel Görsel Asistan'ı gerçek zamanlı, etkileşimli bir yardımcı pilota dönüştürür.
_(Not: Bu özellik yalnızca Google Gemini ve Gemini uyumlu Özel sağlayıcılara özeldir.)_

- **Etkinleştirme:** Canlı operatör oturumunu başlatmak için Komut Katmanında **Ctrl+A** tuşlarına basın; sonlandırmak için tekrar basın.
- **Nasıl çalışır:** Basit bir dille istekte bulunun, örneğin "Chrome'u açın ve bir web sitesi arayın" veya "bu dosyayı final olarak yeniden adlandırın". Operatör ekrana bakar, adımları tek tek uygular ve görev tamamlanana kadar çok adımlı istekleri işlemeye devam eder.
- **Duyurular:** Her adım Canlı Asistan'ın kendi sesiyle söylenir ve görevin ne zaman tamamlandığını veya neden yapılamadığını size bildirir.
- **CAPTCHA:** Bir CAPTCHA görünürse, operatör önce yerleşik **CAPTCHA çözücünüzü** dener; çözemezse, erişilebilir olan doğrulama işlemini sizin tamamlamanızı ister.
- **Durdurma:** Geçerli görevi iptal etmek için Canlı Asistan penceresinde **Operatör eylemini durdur** düğmesine basın.
- **Ayarlar:** Operatörün kendi talimatı, Komut Yöneticisi'nde (**Canlı**, **Canlı Operatör Talimatı** bölümü) düzenlenebilir. **Canlı Doğrudan Çıktı (Penceresiz)** seçeneği Hızlı Ayarlar'da da mevcuttur.

## 6. Video Analizi ve Sesli Betimleme

> **Not:** Video Analizi ve Sesli Betimleme özellikleri yalnızca **Google Gemini** sağlayıcısı tarafından desteklenmektedir. Eklenti ayarlarında etkin sağlayıcınızın Google Gemini olarak ayarlandığından emin olun.

Profesyonel Görsel Asistan, özellikle kör kullanıcılar için tasarlanmış güçlü video işleme yetenekleri sunar. Hem çevrim içi videoları hem de yerel ekran kayıtlarını analiz ederek son derece ayrıntılı görsel betimlemeler sağlayabilir ve profesyonel Sesli Betimleme betikleri (SRT) oluşturabilir.

### 5.1 Yerel Ekran Kaydı (Kontrol + V)

Ekranınızda sessiz bir video, animasyon veya eğitim videosuyla karşılaşırsanız, bunu doğrudan kaydedebilirsiniz:

1. Komut Katmanına girmek için **NVDA + Shift + V** tuşlarına basın, ardından **Control + V** tuşlarına basın.
2. Eklenti ekranınızı arka planda sessizce kaydetmeye başlayacaktır.
3. Kaydı durdurmak için tekrar **Control + V** tuşlarına basın.
4. Yapay zekâ daha sonra kaydedilen video bölümünü analiz edecek ve sahne, karakterler ve eylemler hakkında son derece ayrıntılı bir betimleme sunacaktır.

### 5.2 Video Analizi (Shift + V)

Hem yerel video dosyalarını hem de çevrim içi videoları analiz edebilirsiniz. Windows Gezgini'nde bir yerel video dosyası seçin veya çevrim içi bir video bağlantısını panonuza kopyalayın. Ayrıca herhangi bir yerde (örneğin bir medya oynatıcısının içinde) **Shift + V** tuşlarına basarak bir video dosyası seçebileceğiniz veya bir URL'yi el ile yapıştırabileceğiniz bir iletişim kutusu açabilirsiniz.

- **Desteklenen Çevrim İçi Platformlar:** YouTube, Instagram, TikTok ve Twitter (X).
- Yapay zekâ yerel dosyayı veya URL'yi otomatik olarak algılayacak, videoyu işleyecek ve kapsamlı bir görsel betimleme ile sesli özet sunacaktır.
- **48 Saatlik Video Dosyası Önbellekleme**: Gemini'ye yüklenen videolar artık 48 saat boyunca önbelleğe alınır! Aynı videoyu yeniden yüklemeden SRT veya MP3 çıktıları oluşturabilirsiniz; NVDA'yı yeniden başlattıktan sonra bile. Önbellek API anahtarına göre tutulur ve API anahtarınız değiştiğinde otomatik olarak geçersiz kılınır.

### 5.3 Sesli Betimleme Oluşturma (SRT)

Daha yapılandırılmış bir deneyim için eklenti, standart SubRip (SRT) biçiminde profesyonel Sesli Betimleme betikleri oluşturabilir.

- **Akıllı Boşluk Zamanlaması:** Yapay zekâ ses parçasını dinler ve görsel açıklamalarını özellikle doğal duraklamalara ve sessiz boşluklara yerleştirerek diyalog çakışmalarını akıllıca en aza indirir.
- **Karakter Takibi:** Motor, değişmeyen yüz özelliklerine göre farklı karakterleri çıkarmak için ön analiz gerçekleştirir. Farklı sahnelerde karakterleri karışıklık olmadan doğru şekilde takip edip etiketlemek için genel bir sözlük oluşturur. Ayrıca her karakterin **ilk görünüşünü** de takip eder, fiziksel görünümlerini yalnızca bir kez -ilk ortaya çıktıkları anda- betimler ve anlatıyı taze ve doğal tutmak için bilinen isimleri yalnızca daha sonraki sahnelerde kullanır.
- **Bire Bir Metin OCR:** Ekranda görünen tüm metinler (tabelalar, telefonlar, jenerikler) bire bir alıntılanır.
- **Nasıl Kullanılır:** Oluşturulan altyazıyı dinlemek için `.srt` dosyasını video dosyanızla aynı klasöre yerleştirin ve tam olarak aynı adı verin. Ardından medya oynatıcınızı (örneğin VLC veya PotPlayer), oynatma sırasında altyazı metnini doğrudan ekran okuyucunuza veya TTS motorunuza yönlendirecek şekilde yapılandırın.
- **Geliştirilmiş Video Kaydetme Deneyimi**: SRT veya MP3 dosyalarını kaydederken dosya iletişim kutusu artık videoyu ister dosya iletişim kutusundan ister Dosya Gezgininden **Shift+V** ile açmış olun, varsayılan olarak kaynak videonun klasöründe açılıyor.

### 5.4 Senkronize Sesli Anlatım (MP3 Dışa Aktarma)

Eklenti yalnızca metin tabanlı SRT dosyaları oluşturmakla kalmaz, aynı zamanda betimlemeleri konuşmaya dönüştürüp videoyla birleştirerek eksiksiz bir Sesli Betimleme üretim aracı olarak çalışır. Artık, son derece gerçekçi ve sınırsız sesli anlatım oluşturmak için Gemini Live API'sini kullanan **Gemini Live TTS**'yi ses motoru olarak seçebilirsiniz. Yerel video dosyaları için MP3 oluştururken birden fazla karıştırma modu kullanılabilir:

- **Standart AD (Sesi Karıştır):** Betimleme doğrudan videonun sesi üzerine eklenir. Betimlemenin net olmasını sağlamak için **Ses Bastırma (Audio Ducking)** uygulanmasını isteyip istemediğiniz sorulacaktır (betimlemeler sırasında arka plan sesinin azaltılması).
- **Genişletilmiş AD (Sesi Duraklat):** Motor, betimlemeler sırasında videonun orijinal sesini duraklatır ve böylece ne orijinal diyaloğun ne de yapay zekâ anlatımının tek bir kelimesini bile kaçırmazsınız. Sessizlik tespiti artık, doğal diyalog duraklamalarını müzik ve arka plan gürültüsünden ayırt etmek için hassas zamanlama sağlayan **Silero VAD** nöral modelini kullanıyor (tıpkı ffmpeg ve eSpeak gibi, ilk kullanımda otomatik olarak indiriliyor).
- **YouTube Videoları:** YouTube kaynakları için (yerel olarak indirilmeyen videolar), MP3 dışa aktarma yalnızca eşzamanlı yapay zekâ ses parçasını içerir, arka plan video sesi bulunmaz.

## 7. Medya Yazıya Dökme ve Dublaj (M)

Ses Yazıya Dökme özelliği, hem ses hem de video dosyalarını (MP3, WAV, MP4, MKV vb.) destekleyecek şekilde tamamen yeniden geliştirilmiştir. Bir medya dosyası seçmek ve aşağıdaki 3 farklı çalışma modundan birini kullanmak için Komut Katmanında **M** tuşuna basın:

1. **Yazıya Dök (Özgün Dil):** Konuşmayı özgün dilinde yüksek doğrulukla yazıya döker.
2. **Yazıya Dök ve Çevir (Hedef Dil):** Konuşmayı yazıya döker ve yapılandırılmış hedef dilinize çevirir.
3. **Dublaj Yap ve Çevir (Hedef Dil)** _(Yalnızca Gemini)_: Konuşmayı yazıya döken, hedef dilinize çeviren ve eklentinin TTS motorunu kullanarak sesli bir dublaj oluşturan güçlü yeni bir özelliktir.

## 8) Gelişmiş Belge ve Görüntü Okuyucu

**Belge Okuyucu** belgelerinizi temiz, okunabilir metne dönüştürür; böylece taranmış bir kitaptan bir yığın fotoğrafa kadar her şeyi okuyabilir, çevirebilir ve dinleyebilirsiniz. Çok sayfalı PDF'leri, karmaşık görüntüleri, iPhone HEIC formatlarını ve hatta OCR veya AI işlemine gerek kalmadan anında açılan düz metin ('.txt') ve HTML ('.html', '.htm') dosyalarını yönetir. Aynı anda birkaç dosya seçin ve bunlar sayfa sırasına göre tek bir sürekli belgede birleştirilir. Üç OCR motoru mevcuttur — üstün düzen koruması için **Chrome (Hızlı)**, **YZ (Gelişmiş)** ve aranabilir PDF'ler için **Yok (Metin Katmanını Çıkart)** — Ayarlar → Belge Okuyucu'da seçilir.

### Nasıl Çalışır

1. Belge Okuyucuyu açmak için **NVDA + Shift + V** ve ardından **D** tuşlarına basın — veya önce Dosya Gezgini'nde bir dosyayı seçili hale getirin ve dosya iletişim kutusunu tamamen atlamak için **D** / **F** tuşlarına basın.
2. Bir veya daha fazla PDF veya resim seçin. Eklenti bunları tarar ve toplam sayfa sayısını duyurur.
3. **Seçenekler** iletişim kutusunda sayfa aralığını seçin (Hangi aralıktan 2/4). Ayrıca **Çıktıyı Çevir** seçeneğini işaretleyebilir ve hedef dili seçebilir veya **OCR sırasında görüntüleri satır içi olarak Betimle** seçeneğini etkinleştirebilirsiniz.
4. Metin çıkarma arka planda toplu olarak başlar. Pencereyi istediğiniz zaman kapatabilir ve daha sonra devam edebilirsiniz; hiçbir şey kaybolmaz.
5. Sayfalar hazır olduğunda bunları görüntüleyicide okuyun: sayfalar arasında geçiş yapın, herhangi bir sayfaya geçin, AI sorularını sorun, metni kaydedin veya sesli anlatım oluşturun.

### 7.1 Toplu İşleme ve Devam Etme

Büyük bir belgeyi tek seferde okumak zorunda değilsiniz. Bir sayfa aralığı seçin (örneğin, `1-20`) veya her şeyi işlemek için varsayılan ayarları koruyun; yapay zeka arka planda tüm sayfaları çıkaracaktır. NVDA çökerse veya taramayı yarıda keserseniz, eklenti ilerlemenizi hatırlar ve yeniden başlatmalar arasında bile tam olarak kaldığınız yerden **Devam Etme** seçeneği sunar. Belge seçeneği, önbelleğe alınmış OCR metnine veya yarım kalan işlemlerin devam verilerine hiçbir şekilde dokunmaz. Bu sayede belgeler yeniden taranmadan açılabilir ve tamamlanmamış çıkarma işlemleri kaldığı yerden sürdürülebilir. Her iki seçenek de varsayılan olarak etkindir ve Hızlı Ayarlar üzerinden de değiştirilebilir.

### 7.2 Akıllı Dosya Eylemi

Belgeyi her zaman önce açmanız gerekmez. Windows Dosya Gezgini'nde bir PDF veya görüntü dosyasını seçin ve Komut Katmanında **D** (Belge Okuyucu) veya **F** (Akıllı Dosya İşlemi) tuşuna basın. Eklenti dosya iletişim kutusunu anında atlayacak ve seçili dosyayı işlemeye başlayacaktır. Birden fazla dosyayı aynı anda seçmek, bunların tek bir belge olarak işlenmesini sağlar.

### 7.3 Belge Görüntüleyici Denetimleri ve Kısayolları

Belge Okuyucu penceresi açıkken aşağıdakileri kullanabilirsiniz:

#### Klavye Kısayolları

- **Ctrl + Sayfa Yukarı:** Önceki sayfaya gider.
- **Aşağı / Yukarı Ok:** İmleç bir sayfanın son satırına ulaştığında, sonraki sayfaya atlamak için**Aşağı** tuşuna basın; Bir önceki sayfaya dönmek için sayfanın üst kısmındaki **Yukarı** tuşuna basın.
- **Alt + A:** Belge hakkında soru sormak için sohbet penceresi açar.
- **Alt + R:** Etkin sağlayıcıyı kullanarak **Yapay Zekâ ile Yeniden Tarar**.
- **Alt + G:** Yüksek kaliteli bir ses dosyası (WAV/MP3) oluşturur ve kaydeder. _Sağlayıcı TTS desteklemiyorsa gizlenir._
- **Alt + S / Ctrl + S:** Çıkarılan metni TXT veya HTML olarak kaydeder.

#### Düğmeler ve Kontroller

- **Git:** Sayfa seçiciden herhangi bir sayfayı seçin.
- **Biçimlendirilmiş Görüntüle:** Belgenin tamamını biçimlendirilmiş metin olarak birleştirilmiş olarak görün.
- **Başarısız Sayfaları Yeniden Dene:** Yalnızca geçici sunucu hatası (ör. yüksek talep) nedeniyle başarısız olan grupları yeniden deneyin. Bu düğme ihtiyaç duyulduğunda otomatik olarak görünür.
- **TTS Sesi / TTS Motoru:** Sesi seçin ve Gemini'de **Standart TTS** ve **Gemini Live** akışı arasında seçim yapın.
- **Önceki / Sonraki:** Sayfalar arasında geçiş yapın (Ctrl+PageUp/Down kısayollarıyla aynıdır).

### 7.4 Son Belgeler (D)

Komut Katmanında **D** tuşuna bastığınızda, en son okuduğunuz belgeler ilk önce listelenir. OCR zaten bitmiş olsa bile, bulunduğunuz sayfadan devam etmek için birini seçin veya bir dosyaya her zamanki gibi göz atmak için **Dosya Aç...** (`Ctrl + O`) tuşuna basın.

## 9. Anlamsal Yapay Zekâ Etiketleme ve Arayüz Gezgini

Her yerde "etiketsiz düğme" bulunan bir uygulamada mı takıldınız? Anlamsal Yapay Zekâ Etiketleme motoru bunu kalıcı olarak çözer.

### 8.1 Kalıcı Nesne Etiketleme (L)

Ekran okuyucunuzun odağını etiketsiz bir grafik veya düğme üzerine getirin ve Komut Katmanında **L** tuşuna basın. Yapay zekâ düğmeye görsel olarak bakacak, işlevini belirleyecek ve kalıcı bir etiket uygulayacaktır.
_Eski ekran okuyucu etiketleme araçlarının aksine, bu eklenti gelişmiş hibrit bir "Nesne İmzası" sistemi (AutomationId/ControlID) kullanır. Özel etiketleriniz pencere boyutu değişikliklerinden, monitör değiştirmeden ve uygulama güncellemelerinden etkilenmeden korunacaktır!_

### 8.2 Tam Uygulama Taraması (Shift + L)

Tüm etkin pencereyi tek seferde taramak için **Shift + L** tuşuna basın. Yapay zekâ tüm etiketsiz öğeleri bulacak ve hepsini tek seferde akıllıca adlandıracaktır. Daha sonra bu etiketleri yerleşik Etiket Yöneticisi üzerinden yönetebilir, yeniden adlandırabilir veya toplu olarak silebilirsiniz.

### 8.3 Kullanıcı Arayüzü Gezgini (E)

Bir öğeyle ona el ile gitmeden etkileşim kurmanız mı gerekiyor? Arayüz Gezginini etkinleştirmek için **E** tuşuna basın. Yapay zekâ ekranı tarayacak ve tıklanabilir tüm öğelerin erişilebilir bir listesini oluşturacaktır (görev çubuğu gibi sistem gürültülerini yok sayarak). Listeden bir öğe seçin; eklenti sizin için anında o öğeye tıklayacaktır.

## 10. Canlı Sesli Asistan

Canlı Asistan, Profesyonel Görsel Asistan'ı gerçek zamanlı, etkileşimli bir yardımcı pilota dönüştürüyor.
_(Not: Bu özellik yalnızca Google Gemini ve Gemini uyumlu özel sağlayıcılara özeldir.)_

- **Etkinleştirme:** Canlı Asistan iletişim kutusunu açmak için Komut Katmanında **Control + L** tuşlarına basın.
- **Gerçek Zamanlı Etkileşim:** Mikrofonunuz aracılığıyla doğal şekilde konuşun. Yapay zekâ aynı anda hem sesinizi dinleyecek hem de etkin ekranınıza bakacaktır. "Şu anda neye bakıyorum?" veya "Üçüncü paragrafı bana oku." gibi sorular sorabilirsiniz.
- **Bas Konuş:** Canlı Asistan ayarları sekmesinde **Bas Konuş** özelliğini etkinleştirin (veya doğrudan Canlı Asistan penceresinin içinde açıp kapatın), ardından konuşmak için size atanmış tuşu basılı tutun ve konuşmayı bitirmek için bırakın. Bu, tuşa basana kadar mikrofonun sesinin kapalı kalmasını sağlar; gürültülü ortamlar için idealdir.
- **Web Kamerası Girişi:** Canlı Asistan penceresinde **Web Kamerası Kullan** seçeneğini işaretleyerek kamera görüntünüzü ekranınız yerine yapay zekaya gönderebilirsiniz; böylece fiziksel nesneler, basılı belgeler veya çevreniz hakkında sorular sorabilirsiniz. Eğer ffmpeg henüz yüklü değilse, kutuyu işaretlemek izninizle bir kez indirilmesini sağlar; kamera algılanmadığında veya Windows gizlilik ayarları kamera erişimini engellediğinde bu seçenek devre dışı bırakılır.
- **Özelleştirme:** İletişim kutusu içinde yapay zekânın Ses Stilini (örneğin Profesyonel, Samimi, Enerjik) değiştirebilir ve yanıt vermeden önce ne kadar derin düşündüğünü kontrol etmek için "Düşünme Derinliğini" ayarlayabilirsiniz.

## 11. Ortam Gözlemcisi (Arka Plan Asistanı)

Ortam Gözlemcisi, Profesyonel Görsel Asistan'ı konuşma gerektirmeden arka plandaki gözleriniz haline getirir: Siz çalışırken dinlemeye ve izlemeye devam eder, değişiklikleri rapor eder ve hiçbir şey olmadığında sessiz kalır.
_(Not: Bu özellik yalnızca Google Gemini ve Gemini uyumlu özel sağlayıcılara özeldir.)_

- **Ctrl + Sayfa Aşağı:** Sonraki sayfaya gider.
- **Modlar:** **Yalnızca Ses Çevirisi** duyduklarını çevirir, **Yalnızca Ekran İzleyici** ekran değişikliklerini bildirir ve **Yalnızca Web Kamerası İzleyici** kameranız ve Bas Konuş özelliğiyle Canlı Asistan penceresini açarak kameranın gördükleri hakkında sorular sormanıza olanak tanır.
- **Ses Kaynağı:** Ses modunda, **Mikrofonunuzu** mı yoksa **Sistem Sesini (Geri Döngü)** mü çevireceğinizi seçin. Küçük loopback kütüphanesi, izniniz alındıktan sonra ilk kullanımda bir kez indirilir.
- **Bağlam:** Ekran ve web kamerası modları için, raporları odaklamak üzere isteğe bağlı bir **Ne yapıyorum** seçeneği (örneğin film izlemek, toplantı veya görüşme takip etmek, etiket okumak veya görünümünüzü kontrol etmek) belirleyebilirsiniz; ayrıca kendi bağlamınızı da yazabilirsiniz.
- **Raporlama:** Eklenti, her yeni kareyi bir öncekiyle karşılaştırır ve yalnızca resim gerçekten değiştiğinde yapay zekaya gönderir; bu nedenle statik bir ekran size asla istek maliyeti getirmez. Yapay zeka daha sonra yalnızca yeni olanı rapor eder ve asla kendini tekrar etmez.
- **Hoş Geldiniz Mesajı:** Çeviri modu dışında, gözlemci çalışmaya başladığında sizi kısaca selamlar, böylece sizi dinlediğini anlarsınız.
- **Ayarlar:** **Ayarlar > Canlı Asistan** bölümünde, **Gözlemci Modu**, **Kare Aralığı** (1 ila 10 saniye) ve **Raporlama Stili** (kısa veya detaylı) seçeneklerini belirleyin. Gözlemci talimatı ve her bir bağlam metni, İstem Yöneticisi'nde (**Ortam** bölümü) düzenlenebilir.

## 12. Özel İstemler ve Değişkenler

İstemleri **Ayarlar > İstemler > İstemleri Yönet…** yolundan yönetebilirsiniz.

- **Filtre:** **Varsayılan İstemler** sekmesinde, istem listesinin üstünde, **Tüm** istemleri veya yalnızca bir bölümü (örneğin **Ortam**) aynı anda gösteren bir **Filtre** listesi bulunur; böylece uzun listelerde gezinmek kolaylaşır.

### Özel İstem Kısayolları

İstem Yöneticisi'nde istediğiniz özel istemlere doğrudan kendi kısayol tuşlarını atayın ve mevcut seçiminiz veya bağlamınızla anında çalıştırın:

- **Tek tuş** (ör. `1`, `p` veya `F3`): Komut Katmanı içinde ve ayrıca global olarak `NVDA + Shift + tuş` şeklinde çalışır.
- **Tuş kombinasyonu** (örneğin, `Control + Shift + 1`, `Alt + P` veya `Insert + 1`): Tek başına global olarak çalışır.

### İsteme Başına Geri Bildirim Davranışı

Her özel komut istemi, çıktı sunma davranışını ayrı ayrı tanımlayabilir:

- **Genel ayar:** Genel Bağlantı çıktı ayarını (Doğrudan Çıktı veya Sohbet penceresi) takip eder.
- **Panoya Kopyala:** Yapay zeka yanıtını pencere açmadan doğrudan panoya kopyalar.
- **Doğrudan Çıktı (NVDA mesajı):** Yapay zekanın yanıtını doğrudan NVDA konuşma sistemi aracılığıyla sesli/braille olarak iletir.
- **Panoya Kopyala ve Doğrudan Sesli Mesaj Gönder:** Yanıtı panoya kopyalar ve doğrudan sesli olarak iletir.
- Etkileşimli iyileştirme penceresi.

### Desteklenen Değişkenler

- `[selection]`: Geçerli seçili metin.
- `[text]`: Şu anda odaklanılan düzenleme alanının tam metin içeriği (korumalı parola kutularını otomatik olarak yok sayar).
- `[currentURL]`: Desteklenen web tarayıcılarından (Chrome, Edge, Firefox) web sayfası veya belge URL'si.
- `[clipboard]`: Pano içeriği.
- `[clipboard_image]`: Şu anda panoda olan resim.
- `[screen_obj]`: Gezgin nesnesinin ekran görüntüsü.
- `[screen_fg_obj]`: Etkin ön plan penceresinin ekran görüntüsü.
- `[screen_full]`: Tam ekran görüntüsü.
- `[file_ocr]`: Metin çıkarımı için görsel/PDF dosyası seç.
- `[file_read]`: Okuma için belge seç (TXT, Kod, PDF).
- `[file_audio]`: Analiz için ses dosyası seç (MP3, WAV, OGG).
- `[ambient_screen]`: Sürekli Ekran Gözlemcisi arka plan oturumunu başlatır.
- `[ambient_webcam]`: Sürekli Web Kamerası Gözlemcisi arka plan oturumunu başlatır (ayarlardan Bas Konuş seçeneğini kontrol eder).
- `[ambient_audio]`: Canlı Ses Gözlemcisi çeviri oturumunu başlatır.
- `[loopback]`: Ses kaynağı olarak sistem ses varsayılanını kullanır (`[ambient_audio]` için).
- `[mic]`: Ses kaynağı olarak mikrofonu kullanır (`[ambient_audio]` ve `[ambient_webcam]` için).
- `[brief]`: Gözlemci raporlama stilini kısa (tek cümle) olarak ayarlar.
- `[detailed]`: Gözlemci raporlama stilini detaylı (2-3 cümle) olarak ayarlar.
- `[lang:code]`: Sesli çeviri için hedef dil kodunu belirtir (ör. `[lang:fa]`, `[lang:en]`).
- `{target_lang}`: Geçerli hedef dil.
- `{source_lang}`: Geçerli kaynak dil.
- `{response_lang}`: Mevcut YZ yanıt dili.
- `{swap_target}`: Akıllı takas çevirisi için yedek dil.
- `{swap_instruction}`: Akıllı takas çeviri talimat bloğu.

_Ortam Değişkenleri Hakkında Not:_ Ortam değişkenleri içeren komutlar bir açma/kapama düğmesi gibi davranır; etkin durumdayken kısayola basmak oturumu anında durdurur. Uyumsuz kombinasyonlar (örneğin, `[screen_full]` gibi statik ekran görüntüsü değişkenlerini ortam gözlemci modlarıyla birleştirmek, birden fazla ortam modunu birleştirmek veya `[ambient_audio]`'ya uyarı talimatları eklemek gibi) kaydedilirken kesinlikle doğrulanır ve engellenir.

## 13. Gerçek Dünya Kullanım Senaryoları (Hangi özelliği kullanmalıyım?)

Profesyonel Görsel Asistan gelişmiş araçlarla doludur. Doğru özelliği seçmenize yardımcı olmak için işte bazı yaygın senaryolar:

- **Senaryo: Karmaşık bir pencerenin veya erişilemeyen bir uygulamanın tüm düzenini anlamak istiyorsunuz.**
  _Çözüm:_ **O** tuşuna basın (Tam Ekran Görüşü). Yapay zekâ tüm ekranı analiz edecek ve öğelerin, metinlerin ve düğmelerin tam olarak nerede bulunduğunu açıklayacaktır.

- **Senaryo: Bir web sayfasında bir resim veya bir belgede etiketsiz bir grafik buldunuz.**
  _Çözüm:_ Gezgin nesnenizi grafiğin üzerine getirin ve **V** tuşuna basın (Nesne Görüşü). Yapay zekâ bu görüntünün tam olarak neler içerdiğini açıklayacaktır.

- **Senaryo: Bir filmi veya video klibi sesli betimlemeyle izlemek istiyorsunuz.**
  _Çözüm:_ Videonuz üzerinde **Shift + V** tuşlarına basın ve **"Sesli Betimleme Oluştur (SRT Dosyası)"** seçeneğini seçin. İşlem tamamlandığında **"Eşzamanlı Anlatım Oluştur (MP3)"** seçeneğine tıklayın ve **"Genişletilmiş AD"** seçeneğini belirleyin. Eklenti, görsel sahneleri açıklamak için filmin diyaloglarını akıllıca duraklatan bir ses parçası oluşturacaktır.

- **Senaryo: Tamamı "etiketsiz düğmelerle" dolu bir uygulamayla karşılaştınız.**
  _Çözüm:_ Belirli düğmeyi yapay zekâ kullanarak kalıcı olarak etiketlemek için **L** tuşuna basın. Ya da tüm pencereyi tek seferde tarayıp etiketlemek için **Shift + L** tuşlarına basın. Yalnızca hızlıca bir öğeye tıklamak istiyorsanız, tıklanabilir tüm öğelerin listesini almak için **E** tuşuna basın (Arayüz Gezgini).

- **Senaryo: Erişilemeyen bir CAPTCHA'yı aşmanız gerekiyor.**
  _Çözüm:_ **C** tuşuna basın (CAPTCHA Çözücü). Yapay zekâ CAPTCHA'yı otomatik olarak yakalayacak, çözecek ve yanıtı doğru alana girecektir.

- **Senaryo: 50 sayfalık uzun bir PDF belgesini okumak istiyorsunuz.**
  _Çözüm:_ **D** tuşuna basın (Belge Okuyucu), sağlayıcınızı Google Gemini olarak ayarlayın ve `1-50` sayfa aralığını girin. Eklenti metni arka planda doğru şekilde çıkaracaktır.

- **Senaryo: Ekranınızda sessiz bir eğitim videosu veya animasyon izliyorsunuz.**
  _Çözüm:_ Ekran kaydını başlatmak için **Control + V** tuşlarına basın. Eğitimin oynatılmasına izin verin, ardından tekrar **Control + V** tuşlarına basın. Yapay zekâ tam olarak nelerin gösterildiğini açıklayacaktır.

- **Senaryo: Beklenmeyen bir hatayla karşılaşıyorsunuz, API bağlantı hatası oluşuyor veya özel yerel sunucularla ilgili sorunları teşhis etmek istiyorsunuz.**
  _Çözüm:_ **Ayarlar > Gelişmiş** bölümüne gidin, **"Özel günlük dosyasını etkinleştir"** seçeneğini işaretleyin ve **Günlük Düzeyi**'ni **"Hata Ayıklama"** olarak ayarlayın. İşlemi tekrar gerçekleştirin, ardından teknik ayrıntıları incelemek için **"Günlük Dosyasını Aç"** seçeneğine tıklayın veya `vision_assistant.log` dosyasını bir destek talebine ekleyin.

***

**Not:** Tüm yapay zekâ özellikleri için etkin bir internet bağlantısı gereklidir. Çok sayfalı belgeler otomatik olarak işlenir.

## 14. Destek ve Topluluk

En son haberler, özellikler ve sürümlerden haberdar olun:

- **Telegram Kanalı:** [https://t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Hata bildirimleri ve özellik istekleri için.

### Hataları ve Günlükleri Raporlama

GitHub konusunu açarken veya destek isterken lütfen aktif AI sağlayıcınız, modeliniz ve NVDA sürümünüz hakkındaki ayrıntıları ekleyin. Bağlantı sorunları veya beklenmeyen çökmeler yaşıyorsanız **Ayarlar > Gelişmiş** bölümünde özel günlük dosyasını etkinleştirin, sorunu yeniden oluşturun ve sorunu daha hızlı çözmemize yardımcı olması için "vision_assistant.log" dosyanızı ekleyin.

## 15. Proje Destekçileri

Cömert mali katkılarıyla bu projenin sürekli geliştirilmesini ve sürdürülmesini destekleyen topluluk üyelerimize yürekten teşekkür ederiz:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**
- **leonardo0216**
- **Sergei Fleytin**
- **Durum Bildirimi**
- **Suman Gayen**
- **Yeni Diller**
- **[avalai.org](https://avalai.org)**

_Projeye finansal olarak destek olmak istiyorsanız ve adınızı burada görmek istiyorsanız, **Bağış Yap** seçeneğini NVDA Araçlar menüsünde (Profesyonel Görsel Asistan alt menüsü) veya kurulum sonrasında kurulum sürecinde bulabilirsiniz._

---

## 2026.10.15 İçin Değişiklikler

- **En Çok Talep Edilen Düzeltme — Gemini API Anahtarı Oluşturmak Nihayet Kolaylaştı**: **aistudio.google.com** adresinden API anahtarı almak eskiden en zor adımdı. Ekran okuyucu kullanıldığında sayfalar kafa karıştırıcıydı ve bazı kişiler hiç anahtar oluşturamıyordu. Bu sorun artık doğrudan eklenti içerisinde çözüldü. Komut Katmanında **G** tuşuna basın (veya Ayarlar'da **Gemini API Anahtarı Al...** seçeneğini kullanın), varsayılan tarayıcınız üzerinden harici kurulum gerektirmeden giriş yapın ve anahtarınız tek bir onay ile oluşturulup yapılandırılsın; daha önce hiç projeniz olmamış olsa bile.
- **Ortam Gözlemcisi**: Arka plan asistanı burada. Komut Katmanında **Shift+O** tuşlarına basarak başlatın ve tekrar basarak durdurun. Duyduklarını (mikrofonunuzdan veya sistemin sesinden) tercüme edebilir, ekranı izleyip nelerin değiştiğini size söyleyebilir veya web kameranız ve Bas Konuş özelliğiyle Canlı Asistan'ı açarak kameranın gördüğü her şey hakkında soru sorabilirsiniz. Yalnızca gerçekten bir değişiklik olduğunda resim gönderir, bu nedenle hareketsiz bir ekran size hiçbir maliyet getirmez ve hiçbir şey olmadığında sessiz kalır. Ayrıca, `[ambient_screen]`, `[ambient_webcam]` veya `[ambient_audio]` seçeneklerini değiştiricilerle (`[loopback]`, `[mic]`, `[brief]`, `[detailed]`, `[lang:code]`) birlikte kullanarak, çakışan değişken kombinasyonlarına karşı otomatik doğrulama ile gözlemciyi doğrudan Özel İstemler ve özel kısayol tuşları aracılığıyla başlatabilir ve açıp kapatabilirsiniz.
- **Canlı Operatör**: Canlı Asistan artık siz onunla konuşurken bilgisayarınızda isteklerinizi yerine getirebilir. Komut Katmanında **Ctrl+A** tuşlarına basarak canlı operatör oturumu başlatın, ardından sorunuzu anlaşılır bir dille sorun. Çok adımlı istekleri işler, her adımı Canlı Asistan'ın kendi sesiyle söyler, gerekli tuş kombinasyonlarını halleder ve görevin ne zaman bittiğine kendisi karar verir. **Canlı Doğrudan Çıktı (Penceresiz)** seçeneği de Hızlı Ayarlar'da yer almaktadır.
- **Karakter Sözlüğü ve Dizi Yönetimi**: Video Analizi iletişim kutusuna güçlü bir **Karakter Sözlüğü** sistemi eklendi! Dizi bazında karakter adlarını, fiziksel açıklamaları ve rollerini ekleyebilir, düzenleyebilir, içe aktarabilir veya yönetebilirsiniz. Yapay zekâ, keşfedilen karakterleri otomatik olarak sözlüğünüzdeki karakterlerle eşleştirir ve daha fazla bölüm analiz ettikçe yeni karakterleri birleştirir. Manuel olarak eklediğiniz notlar her zaman korunur ve yapay zekâ güncellemelerine göre önceliklidir; fiziksel açıklamalar ise bölümler arasında güncel tutulur. Sözlük dizi bazında kaydedilir ve o dizideki her videoda yeniden kullanılır. Karakter listesinde seçili karakteri düzenlemek için **F2**, silmek için **Delete** tuşuna basın.
- **SOCKS5, HTTP ve Ters Proxy Desteği ve Gecikme Testi**: Canlı Asistan, Ortam Gözlemcisi ve Metin Okuma (TTS) oluşturma dahil olmak üzere eklentinin tamamında eksiksiz proxy desteğiyle ağ kısıtlamalarını sorunsuz bir şekilde aşın! Genel ayarlar bölümünde 4 çalışma modundan birini seçin: **Otomatik algılama**, **SOCKS5 Proxy**, **HTTP Proxy** veya **Ters Proxy**. SOCKS5, RFC 1929 kullanıcı adı/şifre kimlik doğrulamasını ve alan adı tünellemesini destekler; HTTP proxy'si Temel kimlik doğrulamasını destekler. Arka planda çalışan yeni **Proxy Bağlantısını Test Et** düğmesi, bağlantı gecikmenizi milisaniye cinsinden bildirir.
- **48 Saatlik Video Dosyası Önbellekleme:** Gemini'ye yüklenen videolar 48 saat boyunca önbelleğe alınır! NVDA'yı yeniden başlattıktan sonra bile, aynı video için yeniden yükleme yapmadan SRT veya MP3 çıktıları oluşturabilirsiniz. Önbellek anahtar duyarlıdır ve API anahtarınız değiştiğinde otomatik olarak geçersiz kılınır.
- **Yapay Zekâ Destekli Sessizlik Algılama (Silero VAD)**: Genişletilmiş AD artık hassas sessizlik algılama için Silero VAD sinir ağı modelini kullanıyor; doğal diyalog duraklamalarını müzik ve arka plan gürültüsünden ayırt ediyor. Model, ilk kullanımda izniniz alınarak ffmpeg ve eSpeak'te olduğu gibi otomatik olarak indirilir.
- **Canlı Asistan için Web Kamerası Videosu**: Canlı Asistan penceresine artık ekranınız yerine web kameranızın görüntüsünü yapay zekâya göndermenizi sağlayan **Web Kamerasını Kullan** onay kutusu eklendi. Fiziksel nesneler, belgeler veya çevreniz hakkında soru sormak için idealdir. Ffmpeg henüz kurulu değilse, kutuyu işaretlediğinizde izniniz alınarak bir kez indirilir. Kamera algılanmadığında veya Windows gizlilik ayarları kamera erişimini engellediğinde bu seçenek devre dışı bırakılır ve kamera gizlilik ayarlarını açmak için bir düğme sunulur. Kamera etkin olmasına rağmen görüntü karesi alınamıyorsa sorun, sessizce ekrana geri dönmek yerine tanılama amacıyla NVDA günlüğüne kaydedilir.
- **Ses Çıkış Aygıtı Seçimi**: Artık Canlı Asistan ve Ortam Gözlemcisi için özel bir ses çıkış aygıtı seçebilirsiniz. Canlı Ayarlar sekmesinde, doğrudan Canlı Asistan iletişim kutusunun içinde veya Hızlı Ayarlar (NVDA+Shift+V ardından Yukarı/Aşağı/Sol/Sağ) aracılığıyla anında NVDA'nın varsayılan çıkışı, Windows Ses Eşleyici veya bağlı herhangi bir fiziksel ses kartı (USB kulaklık veya harici hoparlör gibi) arasında seçim yapabilirsiniz.
- **İstem Yöneticisi**: Varsayılan İstekler sekmesinde artık bir **Filtre** listesi bulunuyor, böylece tüm istekleri veya yalnızca bir bölümü (örneğin **Ortam**) gösterebilirsiniz. Oradan gözlemcinin bağlam metinlerini ve yeni **Canlı Operatör Talimatı**nı da düzenleyebilirsiniz.
- **Gelişmiş Yönlendirmede Akıllı Model Filtreleme**: Gelişmiş Model Yönlendirme açılır menüleri artık Gemini modellerini karmaşa yaratmadan yeteneklerine göre dinamik olarak kategorize ediyor. Canlı Asistan yalnızca gerçek çift yönlü canlı ve yerel ses modellerini görüntüler, Metin Çevirisi (TTS) yalnızca özel konuşma sentezi modellerini görüntüler, Konuşmadan Sese Dönüştürme (STT) ise Transkripsiyon ve çok modlu modellere öncelik verir ve Video Analizi, OCR ve Yapay Zeka Operatörü tek amaçlı yardımcı modelleri (görüntü oluşturma, video oluşturma ve yerleştirme modelleri gibi) temiz bir şekilde filtreler. Gelecek modeller, sürüm güncellemesi gerektirmeden yeteneklerine göre otomatik olarak tespit edilir.
- **Karakterlerin İlk Görünümünün Takibi**: Yapay zekâ artık her karakterin fiziksel görünümünü videodaki ilk görünümünde yalnızca bir kez betimliyor. Sonraki görünümlerde yalnızca karakter adları kullanılıyor; böylece bölümler arasındaki tekrarlanan betimlemeler ortadan kaldırılırken anlatımın doğal ve akıcı olması sağlanıyor.
- **Birleşik Veri Dizini**: Tüm eklenti veri dosyaları (geçmiş, diziler, etiketler, OCR ilerleme verileri, önbellekler ve günlükler) NVDA yapılandırma dizininizin içindeki tek bir `VisionAssistant` klasörüne taşındı. Böylece her şey düzenli tutuluyor ve manuel yedekleme kolaylaşıyor.
- **Geliştirilmiş Kaydetme Deneyimi:** SRT veya MP3 dosyalarını kaydederken, dosya iletişim kutusu artık varsayılan olarak kaynak videonun klasöründe açılır; bu, videoyu dosya iletişim kutusu aracılığıyla veya Explorer'dan Shift+V ile açmış olmanızdan bağımsızdır.
- **Belgeleri Önbelleğe Alınmış Metinleriyle veya Metinleri Olmadan Silme**: Geçmiş iletişim kutusu (**Control + H**) artık bir belgeyi silmek için iki seçenek sunuyor. **Delete** tuşuna basarak **Yalnızca geçmişten sil** veya **Geçmişten ve önbelleğe alınmış metinden sil** seçeneklerinden birini seçebilirsiniz. İkinci seçenek, belgenin önbelleğe alınmış OCR metnini de temizler; böylece belge bir sonraki açılışta baştan taranır. **Bunu Bir daha sorma** onay kutusu seçiminizi sonraki silme işlemleri için hatırlar. Kesintiye uğrayan işlemlerinize ilişkin verilerinize asla dokunulmaz.
- **Belge Okuyucuda Motor Bilincine Sahip ve Birleştirmeli OCR Önbelleği**: Önbelleğe alınan OCR metni artık OCR motoru bazında saklanıyor. Böylece OCR motorunu değiştirdiğinizde eski sonuç yeniden kullanılmak yerine belge her zaman yeni motorla yeniden taranıyor. Bir belgeyi yeniden açtığınızda sayfa aralığı iletişim kutusu tekrar gösteriliyor (son seçiminiz önceden doldurulmuş olarak) ve daha önce taranmış sayfalar anında önbellekten kullanılırken yalnızca eksik sayfalar taranıyor. Önbellek değiştirilmek yerine sayfa sayfa birleştiriliyor; böylece okuduğunuz her aralık daha sonra kullanılmak üzere korunuyor.
- **Belge Okuyucuda PDF Sıkıştırma**: Belge Okuyucunun sayfa aralığı iletişim kutusuna isteğe bağlı **İşlemden önce PDF sayfalarını sıkıştır** ayarı eklendi. Gemini veya Mistral'e büyük veya yüksek çözünürlüklü taranmış PDF belgeleri yüklerken, sayfalar otomatik olarak küçültülür ve yeniden sıkıştırılır; bu da yükleme veri boyutunu önemli ölçüde azaltır, işlemeyi hızlandırır ve ağ zaman aşımını önler. Bu seçenek varsayılan olarak devre dışıdır ve Chrome motoru veya base64 tabanlı resim sağlayıcıları kullanılırken otomatik olarak gizlenir.
- **İstem Başına Geri Bildirim Davranışı Özelleştirme**: Her bir özel isteğin çıktısını nasıl vereceğini ayrı ayrı özelleştirin! Özel komut istemi düzenleyicisinde, **Genel ayar**, **Panoya kopyala**, **Doğrudan Çıktı (NVDA mesajı)**, **Panoya kopyala ve Doğrudan Çıktı** veya **Sohbet penceresi** seçeneklerinden birini seçin. Bu özellik, belirli kişilerin pencere açmadan doğrudan konuşmasına olanak tanırken, diğerlerinin tam bir sohbet penceresi açmasını sağlar.
- **Yeni Dinamik İstem Değişkenleri (`[currentURL]` ve `[text]`)**: Özel İstemler artık Google Chrome, Mozilla Firefox ve Microsoft Edge'de etkin belge URL'sini yakalamak için `[currentURL]` ve şu anda odaklanılan düzenleme alanının tam metin içeriğini dinamik olarak eklemek için `[text]` değişkenlerini desteklemektedir (korumalı parola kutuları hariç).
- **Twitter/X Video İndirici Yenilemesi**: Yukarı akış kazıyıcı arızalarının ardından Twitter/X videolarının indirilmesi ve analizi yeniden sağlandı. Video çıkarma işlemi artık, otomatik TwitSave yedekleme ve proxy desteğiyle birlikte, Twitter'ın CDN'sinden en yüksek kalitede MP4 akışlarını doğrudan almak için güçlü FixTweet API'sini kullanıyor.
- **Instagram Video İndirici Düzeltmesi**: İndirici hizmetindeki yukarı akış form değişikliklerinin ardından Instagram Reels ve video URL'lerinin indirilmesi ve analizi yeniden sağlandı.
- **Düzeltmeler ve Performans İyileştirmeleri**: Bas Konuş özelliği tuşa bastığınız anda yanıt veriyor, Canlı Asistan artık cümlenin ortasında yanıt vermeye başlamıyor, gözlemci artık önceki resmi raporlamıyor ve Düşünme Derinliği listesi yalnızca modelinizin gerçekten desteklediği özellikleri sunuyor. Yapay zeka operatörü sola ve sağa da kaydırma yapabiliyor. Çevrimiçi videoları analiz ederken oluşan bir `AttributeError` hatası düzeltildi ve metin seçimi yapılmayan özel istemlerin arka plan pencere başlıklarını yanlışlıkla yapay zeka isteklerine eklemesi engellendi.

## 2026.09.01 İçin Değişiklikler

- **Geçmiş (Kontrol + H)**: Komut Katmanı artık Geçmiş iletişim kutusunu (`Kontrol + H`) içeriyor; bu iletişim kutusu Tümü, Sohbetler ve Belgeler filtreleriyle geçmiş sohbetlerinizi ve belgelerinizi listeliyor. Herhangi bir sohbeti tüm konuşmasıyla yeniden açın - ekli dosyalar otomatik olarak yeniden eklenir - veya bir belgeyi yeniden açın ve okumaya devam edin. Herhangi bir öğeyi kaldırmak için üzerinde **Delete** tuşuna basın veya her şeyi tek seferde temizleyin.
- **Okuyucudaki Son Belgeler**: Komut Katmanı'nda **D** tuşuna basmak artık ilk olarak yakın zamanda okuduğunuz belgeleri gösteriyor. Üzerinde bulunduğunuz sayfadan devam etmek için birini seçin - OCR zaten tamamlanmış olsa bile - veya her zamanki gibi göz atmak için **Dosya Aç...** (`Ctrl + O`) seçeneğine basın.
- **Canlı Asistan için Bas Konuş**: Canlı konuşmalarınızın tam kontrolünü elinize alın! Yeni Canlı Asistan ayarları sekmesinde **Bas Konuş** özelliğini etkinleştirin ve konuşmak için herhangi bir tuşu - hatta `Sol Ctrl` gibi tek başına bir değiştirici tuşu bile - atayın. Konuşmak için tuşa basılı tutun ve işiniz bittiğinde bırakın; her basışta ve bırakışta kısa bir bip sesi duyulur. Eşleşen bir geçiş de doğrudan Canlı Asistan penceresinde görünür, böylece konuşmadan ayrılmadan Bas Konuş ve açık mikrofon kipi arasında geçiş yapabilirsiniz.
- **Gemini 2.5 Flash Yerel Ses**: Canlı Asistan artık düşük gecikmeli, doğal sesli konuşmalar için Gemini 2.5 Flash'ın yerel ses modelini (`gemini-2.5-flash-native-audio-preview-12-2025`) destekliyor. **Ayarlar → Gelişmiş Model Yönlendirme → Canlı Asistan Modeli (yalnızca Gemini)** üzerinden bu modele geçebilir veya önerilen modelde kalmak için "Otomatik" seçeneğini kullanmaya devam edebilirsiniz.
- **Ayarları Yedekleme ve Geri Yükleme**: **Gelişmiş** sekmesine güçlü bir yedekleme ve geri yükleme sistemi eklendi! Artık API anahtarları, modeller, özel istemler ve tercihler dahil tüm eklenti ayarlarınızı tek bir JSON dosyasına kaydedebilir ve bunları herhangi bir zamanda, herhangi bir makinede veya NVDA'yı yeniden yükledikten sonra kusursuz bir şekilde geri yükleyebilirsiniz. Yedekleme yaparken neyin dahil edileceğini seçersiniz: **Her şey** (ayarlar, özel etiketler, OCR ilerlemesi ve geçmiş) veya **Yalnızca Ayarlar**.
- **Doğrudan Metin ve HTML Okuma**: Belge Okuyucu artık düz metin (`.txt`) ve HTML (`.html`, `.htm`) dosyalarını doğrudan açabiliyor! Dosya kodlamasını otomatik olarak algılıyor, betikleri ve biçimlendirme karmaşasını kaldırıyor ve içeriği okunabilir sayfalara akıllıca bölüyor - hatta sayfa yapısını koruyarak kendi dışa aktardığı dosyaları yeniden içe aktarabiliyor - böylece herhangi bir OCR veya YZ işlemi olmadan anında okuyabilirsiniz!
- **Belge Okuyucu için Gemini Canlı TTS**: "Ses Oluştur" düğmesi artık Gemini Canlı - yüksek kaliteli, doğal tempolu akış metinden sese motorunu - destekliyor! Gemini etkin sağlayıcınız olduğunda, okuyucunun içinden Standart TTS ve Gemini Canlı arasında seçim yapabilir ve seçiminiz bir sonraki sefer için hatırlanır!
- **Özel İstem Kısayolları**: Artık özel istemlerinizden herhangi birine doğrudan İstem Yöneticisi'nden bir kısayol tuşu atayabilirsiniz! Her isteme anında çalıştırmak için kendine özel bir tuş veya tuş kombinasyonu verin; mevcut seçiminizi veya bağlamınızı hiçbir ekstra adım olmadan otomatik olarak yakalar!
- **Sohbet Mesajı dolaşımı**: Herhangi bir konuşmayı eller serbest şekilde tarayın! Herhangi bir sohbet penceresinin içinde (Doğrudan Sohbet, belge sohbeti, iyileştirme ve daha fazlası), sonraki mesajı duymak için `Alt + Aşağı`, önceki mesajı duymak için `Alt + Yukarı` tuşlarına basın - ilerledikçe net "Siz" / "AI" ön ekleri ve "İlk mesaj" / "Son mesaj" sınırları duyurulur.
- **Sohbet Mesajını Kopyala (Alt + C)**: `Alt + Yukarı/Aşağı` ile bir konuşmayı gözden geçirirken, bulunduğunuz mesajı panoya kopyalamak için `Alt + C` tuşlarına basın - Temiz Markdown ayarınıza uygun şekilde - ve sesli bir onay alın.
- **Doğrudan Sohbet Sistem İstemi**: Doğrudan Sohbet (`Shift+C`) artık kendi düzenlenebilir sistem istemine - her konuşma için asistanın kişiliğini ve yanıt dilini belirleyen "Doğrudan Sohbet Talimatı"na - sahip. Bunu İstem Yöneticisi'nin Varsayılan İstemler sekmesinden özelleştirebilirsiniz.
- **Belge Okuyucu İmleç Sayfa Dolaşımı**: Çok sayfalı belgeleri okumak artık daha akıcı! Belge Görüntüleyici'de imleciniz bir sayfanın son satırına ulaştığında ve `Aşağı` tuşuna bastığınızda, okuyucu otomatik olarak sonraki sayfaya geçer. Bir sayfanın başında `Yukarı` tuşuna basmak sizi sorunsuz bir şekilde önceki sayfaya geri götürür - okurken artık elle sayfa değiştirmeye gerek yok!
- **Yeni Hızlı Ayarlar Geçişleri**: YZ yanıtlarını panoya kopyalama, Doğrudan Çıktı (sohbet penceresi yok), Sohbette Temiz Markdown ve Akıllı Değiştirme artık komut katmanının Hızlı Ayarlarından anında açılıp kapatılabilir!
- **Canlı Asistan Ayarları Sekmesi**: Canlı Asistan artık kendine ait özel bir ayarlar sekmesine sahip! "Canlı Asistan: Doğrudan Çıktı (Pencere Yok)" seçeneği Bağlantı sekmesinden buraya taşındı ve sekme yalnızca etkin sağlayıcınız Google Gemini (veya Gemini uyumlu bir Özel sağlayıcı) olduğunda görünür.

## 2026.08.06 İçin Değişiklikler

- **Arayüz Gezgini Etiketleme:** Artık Arayüz Gezgini içinde bulunan öğelere doğrudan etiket ekleyebilirsiniz! Yeni bir **"Etiket Ekle"** düğmesi eklendi. Ayrıca arayüz açık kalır ve odağı korur; böylece birden fazla nesneyi kesintisiz ve hızlı bir şekilde etiketleyebilirsiniz.
- **Hızlı Ayarlar Katmanı Geliştirmesi**: Görsel Asistan katmanı (`Insert+Shift+V`) artık kalıcı ve son derece etkileşimli! `Yukarı/Aşağı` ok tuşlarıyla hızlı ayarlar (Sağlayıcı, Model, Yapay Zekâ Yanıt Dili, TTS Modeli) arasında dolaşabilir, `Sol/Sağ` ok tuşlarıyla ise kısa ve anlaşılır sesli geri bildirim eşliğinde değerlerini anında değiştirebilirsiniz. Seçimleriniz hemen uygulanır (gerektiğinde gelişmiş yönlendirme de otomatik olarak etkinleştirilir) ve yapılandırma sırasında katman etkin kalmaya devam eder.
- **Doğrudan Sohbet (`Shift+C`):** Komut Katmanına yeni bir komut eklendi! `Shift+C` tuşlarına basarak anında bir **"Doğrudan Sohbet"** penceresi açabilirsiniz. Böylece bir görsel veya belgeyle başlamaya gerek kalmadan, yapay zekâ ile doğrudan metin tabanlı bir sohbet başlatabilirsiniz.
- **Kusursuz Sohbet Geçmişi Geri Yükleme:** `Boşluk` çubuğuyla son sonucu geri çağırırken sonraki sohbet geçmişinin kaybolmasına neden olan önemli bir hata giderildi. Artık eklenti konuşmalarınızı genel olarak takip eder. Eğer sohbeti kapatıp, iletişim kutusunu kapatıp, ardından "Boşluk" tuşuna basarak sohbeti geri çağırırsanız, tüm karşılıklı yazışmalarınız eksiksiz olarak geri yüklenir! Bu özellik Doğrudan Sohbet, Görsel Analizi, Belge Sohbeti ve Çeviri için çalışır.
- **OCR'de Satır İçi Görsel Betimleme:** Belge OCR işlemi sırasında görselleri satır içinde betimleyen isteğe bağlı bir özellik eklendi. Bu ayarı eklentinin OCR ayarlarından, metin çıkarma öncesinde Belge Okuyucu seçeneklerinden veya Hızlı Ayarlar Katmanından anlık olarak açıp kapatabilirsiniz.
- **Sesli Çeviri (`Control+T`):** Güçlü yeni bir özellik eklendi! Konuşmanızı dikte edin; yapay zekâ, yapılandırılmış kaynak ve hedef dillerinizi kullanarak konuşmayı anında çevirsin ve sonucu yazsın.
- **Güncelleme İndirici İyileştirmeleri:** Güncelleme indirme iletişim kutusu artık indirme ilerlemesini yüzde olarak doğru şekilde gösterir. Ayrıca kurulum iptal edildiğinde görünen hatalı **"Güncelleme indiriliyor"** iletisi sorunu giderildi.
- **eSpeak-NG İndirici İyileştirmeleri:** eSpeak-NG indirmeleri için yüzde tabanlı ilerleme takibi eklendi.
- **Toplu OCR Dayanıklılığı:** Toplu PDF OCR işlemi sırasında etkin API anahtarının kotası dolduğunda işlemin durmasına neden olan sorun giderildi. Artık eklenti otomatik olarak kullanılabilir sonraki API anahtarına geçerek işleme kaldığı yerden devam eder.
- **Görsel CAPTCHA Desteği:** Görsel CAPTCHA çözümü için güçlü destek eklendi. Bu Eklenti, hCaptcha ve reCAPTCHA gibi karmaşık görüntü tabanlı zorlukları otomatik olarak çözmeyi amaçlayarak, zorlu web formlarında erişilebilirliği önemli ölçüde artırır.
- **Ses Yazıya Dökme Modülü Yenilendi:** Ses Yazıya Dökme modülü tamamen yeniden geliştirildi ve artık hem ses hem de video dosyalarını destekliyor. Üç farklı çalışma modu sunar: **"Yazıya Dök (Özgün Dil)"**, **"Yazıya Dök ve Çevir (Hedef Dil)"** ve yalnızca Gemini'ye özel olan, özgün konuşmanın çevrilmiş seslendirmesini oluşturan güçlü yeni **"Dublaj Yap ve Çevir (Hedef Dil)"** seçeneği.
- **Belge Okuyucuda İsteğe Bağlı Sayfa Numaraları:** Çok sayfalı belge çıktılarında sayfa numaraları ve ayırıcıların eklenmesini açıp kapatmaya yarayan yeni bir ayar eklendi. Bu seçenek ana ayarlardan veya Hızlı Ayarlar Katmanından anında yönetilebilir. Özellik hem TXT/HTML dışa aktarımlarında hem de satır içi **"Biçimlendirilmiş Görünüm"** penceresinde geçerlidir ve birleştirilmiş belgeleri kesintisiz okumanızı sağlar.
- **Video Betimlemeleri için Sınırsız Gemini Live TTS:** Videolar için Eşzamanlı Sesli Anlatım (MP3) oluştururken artık ses motoru olarak **Gemini Live TTS** seçilebilir. Bu özellik, Google Gemini Live API'sini kullanarak karakter veya süre sınırlaması olmaksızın yüksek kaliteli sesli betimlemeler üretir.
- **Kod Tabanının Modülerleştirilmesi:** Eklentinin yapısı, bakımını kolaylaştırmak amacıyla tek dosyalı yapıdan çok dosyalı modüler mimariye dönüştürüldü.
- **Ayarlar Arayüzü Yeniden Tasarlandı:** Ayarlar iletişim kutusu tamamen yenilenerek gruplandırılmış düzen yerine modern, sekmeli bir arayüz kullanılmaya başlandı. Böylece mevcut tüm seçenekler korunurken daha iyi organizasyon ve daha kolay dolaşım sağlandı.
- **Genel ve Ayrı Günlük Dosyası Kaydı:** Yeni **"Gelişmiş"** sekmesi altında isteğe bağlı genel günlük kayıt sistemi eklendi. Tüm eklenti modüllerindeki işlemleri, API trafiğini ve hataları otomatik olarak özel bir günlük dosyasına (`vision_assistant.log`) kaydeder. Yapılandırılabilir günlük düzeylerini (Hata Ayıklama, Bilgi, Uyarı, Hata), otomatik saklama sürelerini (1 saat–90 gün) ve ayarlar üzerinden günlük dosyasını doğrudan açma veya temizleme işlemlerini performansı etkilemeden ve NVDA günlüklerine müdahale etmeden destekler.
- **Gemini Yükleme İlerleme Takibi:** Büyük dosyalar (video, ses ve belgeler) Google Gemini API'sine yüklenirken gerçek zamanlı yüzde ilerleme bildirimleri eklendi.

## 2026.07.15 için değişiklikler

- **Akıllı API Model Filtreleme**: Model filtreleme sistemi, beyaz liste yaklaşımı yerine tamamen kara liste yaklaşımını kullanacak şekilde baştan sona yenilendi. Ana sohbet modeli açılır listesinin kusursuz şekilde temiz ve geleceğe hazır kalmasını sağlamak için daha güçlü filtreleme anahtar sözcükleri (`embedding`, `bison`, `gecko`, `audio`, `realtime`, `babbage`, `moderation`, `deep`, `antigravity`, `computer`) eklendi.
- **Gelişmiş Yönlendirme Araması**: Tüm Gelişmiş Model Yönlendirme açılır listeleri (OCR, STT, TTS, Operatör, Video, Canlı) ile eSpeak Varyant seçicisi artık tamamen aranabilir. İstediğiniz modeli veya varyantı hızlıca bulmak için yazmaya başlayarak filtreleme yapabilirsiniz.
- **Yeni Komut Katmanı Kısayolları**:
  - **Ayarlar (`Alt + S`)**: Profesyonel Görsel Asistan ayarlar iletişim kutusunu anında açar.
  - **Kotası Tükenen Anahtarları Bildir (`Alt + Q`)**: Günlük kotasını aşmış Gemini API anahtarlarının tam sayısını bildirir, hangi modelde kotalarının tükendiğini belirtir ve tam sıfırlanma zamanlarını sesli olarak duyurur.
  - **Yönlendirme Denetimi (`Alt + M`)**: Mevcut Gelişmiş Yönlendirme yapılandırmanızı denetler ve varsayılan ayarlar atlanarak, uzmanlaşmış görevler için etkin olarak seçilmiş modelleri sesli olarak bildirir.
- **Video Analizi Tamamen Yenilendi**: Video Analizi baştan sona dönüştürüldü! Daha önce yalnızca çevrimiçi videoların temel bir betimlemesini sunuyordu. Şimdi ise, görme engelli kullanıcılar için özel olarak tasarlanmış kapsamlı bir video işleme paketidir:
  - **Yerel Ekran Kaydı (`Control+V`)**: Artık ekranınızdan doğrudan sessiz videolar kaydedebilirsiniz. Yapay zekâ, kaydedilen bölümü analiz ederek sahneyi, yerleşimi ve gerçekleşen eylemleri son derece ayrıntılı şekilde betimler.
  - **Sesli Betimleme Oluşturma (SRT)**: Eklenti artık videolar için son derece ayrıntılı Sesli Betimleme metinleri (standart SRT biçiminde) oluşturabilir. Bu işlem, betimlemeleri ses parçasındaki doğal duraklamalara akıllıca yerleştiren akıllı boşluk zamanlaması ile ekrandaki tüm metinler için birebir OCR çıktısını içerir.
  - **Senkronize Sesli Betimleme (MP3 Dışa Aktarma)**: Metin tabanlı altyazıların ötesinde, bu eklenti Sesli Açıklamayı konuşmaya dönüştürebilir, otomatik olarak videonun orijinal ses parçasıyla karıştırabilir, ses kısma (açıklamalar sırasında arka plan sesini düşürme) uygulayabilir ve son senkronize sonucu MP3 dosyası olarak dışa aktarabilir!
  - **Akıllı Video Dosyası Eylemi**: Yerel bir video dosyasına odaklanıp video kısayoluna bastığınızda, eklenti bunu otomatik olarak algılar ve dosyayı doğrudan işler.
  - **Gelişmiş Karakter Takibi**: Yapay zekâ artık ön işlem olarak karakter çıkarımı gerçekleştirir. Genel bir karakter sözlüğü oluşturur ve karakterleri bölüm bölüm kimliklerini karıştırmadan doğru şekilde takip eder.
  - **Video Analizi Yapılandırması**: SRT parça boyutlarını, karakter altyazılamasını ve sorumluluk reddi bildirimlerini denetlemek için yeni ayarlar eklendi.
  - **Genişletilmiş Model Yönlendirmesi**: Artık Gelişmiş Model Yönlendirme ayarlarından video için özelleşmiş modelleri (`gemini_video_model`, `custom_video_model`) açıkça seçebilirsiniz.
- **Akıllı API Kota Yönetimi**: 429 (Günlük Limit) hatalarının işlenmesi, model bazında kota takibi yapacak şekilde geliştirildi. Bir API anahtarı belirli bir modelde günlük limitine ulaştığında, yalnızca o model için akıllıca karantinaya alınır; böylece aynı anahtar diğer modellerle kullanılmaya devam edebilir.

## 7.0.0 için değişiklikler

- **Yarım Kalan Taramaları Sürdürme**: Belge Okuyucu ve Akıllı Dosya İşlemleri için devam ettirme özelliği eklendi. Bir tarama herhangi bir nedenle kesintiye uğrarsa, artık baştan başlamak yerine kaldığı yerden devam edebilirsiniz.
- **Yeni `[screen_fg_obj]` Değişkeni**: Tüm ekran yerine yalnızca etkin ön plan penceresinin ekran görüntüsünü alabilen yeni bir özel istem değişkeni eklendi.
- **Akıllı Yeniden Deneme ve API Anahtarı Değiştirme**: Sunucuda geçici yoğunluk (örneğin "high demand") veya hatalı yanıtlar oluştuğunda eklenti artık aynı API anahtarıyla sessizce en fazla 5 kez yeniden deneme yapar. Bu denemeler başarısız olursa, listedeki bir sonraki API anahtarına otomatik olarak geçer.
- **Ekran Perdesi Algılama**: Ekran Perdesi etkin durumdayken (kalıcı olarak açık ya da kısayol tuşuyla geçici olarak etkinleştirilmiş olsa bile) ekran görüntüsü alınmasını engelleyen bir kontrol eklendi. Böylece siyah ekran görüntülerinin gönderilmesi ve API belirteçlerinin (token) boşa harcanması önlenir.
- **Belge Okuyucu İyileştirmeleri**: PDF sayfa aralığı iletişim kutusu artık varsayılan hedef dili eklenti ayarlarınızdan otomatik olarak seçer. Ayrıca, Belge Okuyucu kapatıldığında arka planda çalışan görevlerin düzgün şekilde sonlandırılmasını sağlamak için iş parçacığı (thread) yönetimi iyileştirildi.
- **Yerleşik Mistral OCR Entegrasyonu**: Mistral'ın yerleşik Belge OCR API'si entegre edildi. Çok sayfalı belgeler artık otomatik olarak birleştirilir, yüklenir ve Mistral'ın özel `/v1/ocr` uç noktası kullanılarak toplu olarak işlenir. Tek sayfalı görseller ise gereksiz PDF dönüştürmeleri yapılmadan doğrudan işlenir.
- **Dinamik Özel URL İşleyicileri**: Özel API URL'si değiştirildiğinde önbelleğe alınmış model listesi anında temizlenir ve manuel model giriş kutusu yeniden etkinleştirilir. Bu sayede standart `/v1/models` uç noktasını desteklemeyen özel servislerle (örneğin Cloudflare AI Gateway) tam uyumluluk sağlanır.
- **Yapay Zekâ Operatörü Girdi Motoru Baştan Yazıldı**: AI Operator için kullanılan fare ve klavye benzetim sistemi tamamen yeniden geliştirildi. Eski `mouse_event` API'si yerine modern Windows `SendInput` API'si kullanılarak güncel uygulamalar, UAC korumalı pencereler ve yüksek DPI ekranlarla çok daha yüksek uyumluluk sağlandı.
- **Sürükle ve Bırak İşlemleri Düzeltildi**: AI Operator'deki sürükle ve bırak işlemleri artık tamamen kararlı ve güvenilir çalışmaktadır. Yeni motor; doğal hareket eğrileri (easing), hassas imleç konumlandırması, optimize edilmiş zamanlama ve akıllı bir "nudge" tekniği kullanarak Windows'un ve uygulamaların sürükle-bırak hareketlerini doğru şekilde algılamasını ve işlemin yarıda kesilmeden tamamlanmasını sağlar.
- **Çoklu Monitör Desteği**: YZ Operatör artık çoklu monitör kurulumlarını tam olarak desteklemektedir. `MOUSEEVENTF_VIRTUALDESK` bayrağı kullanılarak fare hareketleri ve tıklamalar tüm monitörlerde doğru şekilde çalışır; böylece hedef uygulama hangi monitörde olursa olsun imleç doğru konumlandırılır.
- **Geliştirilmiş Klavye taklidi**: Tuş gönderme sistemi, Genişletilmiş Tuşları (Extended Keys) tam olarak destekleyecek şekilde geliştirildi. Buna yön tuşları, Home, End, Page Up, Page Down, Insert, Delete ve F1-F12 tuşları dahildir. Böylece YZ Operatör tarafından gönderilen gezinme ve kısayol komutları tüm uygulamalarda sorunsuz çalışır.
- **HEIC/HEIF Görsel Desteği**: iPhone fotoğraf biçimleri için yerel destek eklendi. Artık `.heic` ve `.heif` dosyalarını önceden dönüştürmeye gerek kalmadan doğrudan yapay zekâ ile görsel açıklama, OCR veya Belge Okuyucu işlemleri için seçebilirsiniz.

## 6.5.0 Sürümündeki Değişiklikler

- **Live Assistant**: Yalnızca Google Gemini sağlayıcısı (veya Gemini uyumlu özel sağlayıcılar) için kullanılabilen bir gerçek zamanlı sesli ve ekran asistanı özelliği eklendi. Bu özellik, ayarların değiştirilmesi durumunda otomatik yeniden bağlanma ile birlikte, doğrudan diyalog içinde etkileşimli ses ve düşünme derinliği özelleştirme seçeneklerini içerir.
- **MiniMax AI Sağlayıcı**: MiniMax, tam multimodal destek (sohbet, görme, OCR), 300'den fazla dinamik ses kullanan özel TTS ve çıktılardan akıl yürütme bloklarının (ör. `<think>...</think>`) otomatik olarak çıkarılması özellikleriyle eş sağlayıcı olarak entegre edildi. çıktılardan gelen yanıt\`).
- **Belge Görüntüleyici Çevirisi**: Yerelleştirilmiş dil adı yerine standart 2 harfli dil kodunun Google Translate'e gönderilmesini sağlayarak, İngilizce olmayan NVDA kullanıcıları için sessiz çeviri hatası düzeltildi.
- **PDF Toplu Tarama Yeniden Denemesi**: Gereksiz yüklemeleri önlemek ve yeniden denemeler sırasında rahatsız edici hata pencerelerinin açılmasını engellemek için, PDF belge toplu taraması için yüksek düzeyde optimize edilmiş, ayrı ve sessiz bir yeniden deneme mantığı uygulandı.
- **Belge Görüntüleyici Durumu**: Uzun belge taramaları sırasında eklentinin genel durumunun (`I` ile kontrol edilir) “Toplu İşleme Başladı” durumunda takılı kalmasına neden olan bir hata düzeltildi.
- **İş Parçacığı Çökmesi Çözüldü**: Arka plan iş parçacığından belgeler açılırken ortaya çıkan ciddi bir `IsMain() failed in wxTimerImpl` iş parçacığı onaylama çökmesi, GUI geri arama kuyruğunun `wx.CallAfter`'a geçirilmesiyle düzeltildi.

## 1.3 Yapay Zekâ Davranışı Sekmesi

- **Çift Etiket Ön Kontrolü**: Tek etiketlemede, çift kontrolün eski koordinat anahtarlarını kullanması ve NVDA'nın mevcut etiketi duyurmak yerine zaten etiketlenmiş nesneler için çift AI isteği yapmasına neden olan bir sorun düzeltildi.
- **Gemini Dışı Sağlayıcılar için Belge Sohbeti**: OpenAI, Groq veya yerel Özel sağlayıcılar (Ollama gibi) kullanan kullanıcıların belgelerle başarılı bir şekilde sohbet edebilmeleri ve engellenmemesi için Belge Sohbeti'ndeki (`on_ask`) katı API anahtarı kontrolü düzeltildi.
- **Hızlı Chrome OCR Çevirisi**: Chrome OCR için ücretsiz, anahtarsız çeviri API'si geri getirildi. Çıkarılan metnin çevirisi artık Gemini AI'yı atlayarak gerçekleştiriliyor, böylece API kotalarından tasarruf sağlanıyor ve çeviri süreci hızlanıyor.
- **CAPTCHA Alfanümerik Filtresi**: CAPTCHA çözücüsündeki filtreleme mantığı, alfanümerik olmayan karakterlerin her durumda düzgün bir şekilde temizlenmesini sağlayacak şekilde düzeltildi.
- **Komut Katmanı Yardım Güncellemesi**: Yardım menüsündeki durum bildirim kısayolu `L`'den `I`'ye düzeltildi ve listeye her iki etiketleme komutu (`L` ve `Shift+L`) eklendi.

## 6.1.0 Sürümündeki Değişiklikler

- **Gemma 4 Düşünme Çıktısı Düzeltmesi**: Gemma 4 modellerinde, tüm içsel düşünme sürecinin nihai yanıt olarak gösterilmesi veya düşünmenin devre dışı bırakılmasının boş yanıtlarla sonuçlanması sorunu düzeltildi. Eklenti artık yalnızca nihai, temiz metin yanıtını doğru şekilde izole edip çıkarıyor.
- **Dosya Gezgini'nden Toplu OCR İşlemi**: Artık Windows Dosya Gezgini'nde birden fazla fotoğraf veya PDF dosyasını doğrudan seçebilir ve bunları toplu olarak metin çıkarabilir veya analiz edebilirsiniz. Bu eklenti, yalnızca desteklenen dosya biçimlerini otomatik olarak filtreleyecek ve işleyecektir.

## 6.1.0 için değişiklikler

- **Evrensel Yerel YZ Entegrasyonu (Yerel YZ'yı Kur)**: Özel Sağlayıcı Ayarları'na yeni bir **“Yerel AI'yı Kur”** düğmesi eklendi. Kullanıcılar artık **Ollama**, **LM Studio**, **Jan.ai** ve **KoboldCPP** dahil olmak üzere yerel AI motorlarını anında otomatik olarak yapılandırabilir.
- **Akıllı Yerel Proxy Atlama**: Bağlantı mantığı, gelişmiş bir proxy atlama mekanizmasıyla yeniden oluşturuldu. Eklenti artık yerel loopback bağlantıları için Windows sistem proxy'lerini tamamen atlayacak kadar akıllıdır ve VPN/TUN modu etkin olsa bile istikrarlı yerel AI bağlantıları sağlar.
- **Ultra Kararlı YZ Etiketleme (v2)**: Mutlak ekran koordinat anahtarları, gelişmiş, hibrit bir **Nesne İmzası** sistemi ile değiştirildi. Etiketler artık programlama tanımlayıcılarına (UIA **AutomationId** veya Win32 **ControlID**) ve pencereye göre koordinatlara dayanıyor; bu sayede özel etiketleriniz pencere boyutlandırma, taşıma, monitör değiştirme veya ölçeklendirmeye karşı tamamen dayanıklı hale geliyor.
- **Sorunsuz Otomatik Etiket Taşıma**: Yükseltme işlemi tamamen şeffaftır. Eklenti, ilk odaklandığında eski koordinat tabanlı etiketlerinizi arka planda yeni kararlı parmak izi formatına otomatik olarak taşır ve veri kaybı yaşanmaz.

## 6.0 Sürümündeki Değişiklikler

- **Anlamsal YZ Etiketleme Özelliği**: Kullanıcılar artık YZ kullanarak isimsiz düğmeleri ve simgeleri kalıcı olarak etiketleyebilir. **L** tuşuna basarak mevcut gezgin nesnesini etiketleyebilir (hem Sekme tuşuyla odaklanma hem de nesne gezintisi desteklenir) veya **Shift+L** tuşlarına basarak tüm uygulamayı tek seferde tarayıp etiketleyebilirsiniz.
- **Akıllı Etiket Yönetimi**: Özel etiketleri görüntülemek, yeniden adlandırmak veya toplu olarak silmek için yeni, tamamen erişilebilir bir Etiket Yöneticisi iletişim kutusu eklendi (etiketler varsa **Shift+L** tuşlarıyla erişilebilir).
- **Doğrudan Dosya Analizi (Dosya İletişim Kutusunu Atla)**: Eklenti artık, Windows Dosya Gezgini'nde bir PDF veya görüntü dosyasına odaklandığınızı algılayacak kadar akıllıdır. Vurgulanan bir dosya üzerinde **F (Akıllı Dosya Eylemi)** veya **D (Belge Okuyucu)** tuşuna basıldığında, standart “Aç” iletişim kutusu tamamen atlanarak dosya hemen işlenir.

## 5.6 İçin Değişiklikler

- **“Yok (Metin Katmanını Ayıkla)” OCR Motoru eklendi**: Kullanıcılar artık YZ kredisi kullanmadan aranabilir PDF'lerden doğrudan metin ayıklayabilir; bu da metin tabanlı belgelerde hızı ve gizliliği önemli ölçüde artırır.
- **UI Gezgini Doğruluğu İyileştirildi**: UI Gezgini istemini, öğe türlerini (Liste Öğeleri gibi) daha iyi tanımlayacak ve Görev Çubuğu ve Saat gibi Windows sistem bileşenlerini yok sayarak “(İşaretli)”, “(Seçili)” veya “(Genişletilmiş)” gibi durumları doğru bir şekilde bildirecek şekilde iyileştirildi.
- **Kurulum Ayarları Hatırlatıcısı**: Kurulumdan sonra, kullanıcıları API anahtarlarını ve tercihlerini yapılandırmak için ayarlar menüsüne yönlendiren bir bildirim eklendi.

## 5.5.2 için değişiklikler

- **Yapay Zeka Operatörü Yazma Sorunu Düzeltildi:** Belirli sistemlerde metin yapıştırmak yerine 'v' harfinin yazılmasına neden olan bir hata çözüldü. Bu düzeltme, yüksek sistem yükü sırasında meydana gelen zamanlama çakışmalarını giderir.
- **Gelişmiş Kararlılık:** Sistem panosu diğer uygulamalar tarafından geçici olarak kilitlendiğinde eklentilerin çökmesini önlemek amacıyla pano işlemlerine yönelik güçlü hata yönetimi eklendi.
- **Zamanlama Optimizasyonu:** Farklı sistem hızlarında daha yüksek güvenilirlik ve üçüncü taraf Pano Yöneticileriyle daha iyi uyumluluk sağlamak amacıyla klavye olaylarına yönelik dahili gecikmeler ayarlandı.

## 5.5 İçin Değişiklikler (Otomasyon Güncellemesi)

- **Yapay Zeka Operatörü (Otonom Kontrol - Shift+A):** Bu, v5.5'in en önemli özelliğidir. Profesyonel Görsel Asistan, pasif bir asistan olmaktan çıkıp kişisel **Yapay Zeka Operatörünüz** haline geldi. Yalnızca ekranı betimlemez; komut gerektirir.
  - _Nasıl çalışır:_ Artık bilgisayarınızı çalıştırmak için sözlü talimatlar verebilirsiniz. Örneğin, ekran okuyucunuzun sessiz kaldığı, tamamen erişilemeyen bir uygulamada **Shift+A** tuşlarına basıp şunu yazabilirsiniz: _"Ayarlar düğmesine tıklayın"_ veya _"Arama alanını bulun, 'Son Haberler' yazın ve enter tuşuna basın."_ Yapay zeka, öğeleri görsel olarak betimler, fareyi hareket ettirir ve görevi sizin için yürütür.
  - _Performans Notu:_ Bu özellik, en karmaşık kullanıcı arayüzü düzenlerini bile işleyebilen inanılmaz derecede hızlı ve akıllı yanıtlar sunan **Gemini 3.0 Flash (Önizleme)** için optimize edilmiştir.
  - - **⚠️ API Kullanım Uyarısı:** Yapay Zeka Operatörünün doğru olması için tam olarak ne olduğunu "görmesi" gerektiğinden, her adımda yüksek çözünürlüklü bir ekran görüntüsü gönderir. Sık kullanımın API kotanızı standart metin tabanlı görevlere göre çok daha hızlı tüketeceğini lütfen unutmayın.
- **Görsel Kullanıcı Arayüz Gezgini (E):** "Etiketlenmemiş düğmeler" arasında gezinmekten bıktınız mı? UI Explorer'ı etkinleştirmek için **E** tuşuna basın. Yapay zeka tüm pencereyi tarayacak ve simgeler, grafikler ve menüler dahil gördüğü her tıklanabilir öğenin bir listesini oluşturacaktır. Listeden bir öğe seçmeniz yeterlidir; yapay zeka Operatörü sizin için o öğeye tıklayacaktır. Bu, herhangi bir uygulamanın üstünde "erişilebilir bir katmana" sahip olmak gibidir.
- **Bağlama Duyarlı Akıllı Dosya Eylemi (F):** "F" tuşu tamamen elden geçirildi. Artık yalnızca OCR istediğinizi varsaymıyor. Tek bir görsel seçtiğinizde artık akıllı bir şekilde amacınızı soruyor: Sahneyi anlamak için **Ayrıntılı Görsel Açıklama** veya okumak için **Yapılandırılmış Metin Çıkarma (OCR)** seçebilirsiniz. Menü, dosya türüne ve aktif AI motorunuza göre dinamik olarak uyarlanır.
- **Çekirdek Optimizasyonu:** Eklentinin dahili mantığında derinlemesine bir temizlik gerçekleştirdik, kullanılmayan eski işlevleri ve gereksiz kodları kaldırdık. Bu, tüm kullanıcılar için daha yalın, daha hızlı ve daha güvenilir bir deneyimle sonuçlanır.

## 5.0 için Değişiklikler

- **Çoklu Sağlayıcı Mimarisi**: Google Gemini’ye ek olarak **OpenAI**, **Groq** ve **Mistral** için tam destek eklendi. Kullanıcılar artık tercih ettikleri yapay zekâ arka ucunu seçebilir.
- **Gelişmiş Model Yönlendirme**: Yerel sağlayıcı kullanıcıları (Gemini, OpenAI vb.) artık farklı görevler (OCR, STT, TTS) için açılır listeden belirli modelleri seçebilir.
- **Gelişmiş Uç Nokta Yapılandırması**: Özel sağlayıcı kullanıcıları, yerel veya üçüncü taraf sunucular üzerinde ayrıntılı denetim için belirli URL’leri ve model adlarını manuel olarak girebilir.
- **Akıllı Özellik Görünürlüğü**: Ayarlar menüsü ve Belge Okuyucu arayüzü, seçilen sağlayıcıya göre desteklenmeyen özellikleri (TTS gibi) otomatik olarak gizler.
- **Dinamik Model Getirme**: Eklenti, mevcut model listesini doğrudan sağlayıcının API’sinden alır; böylece yeni modeller yayınlanır yayınlanmaz uyumluluk sağlanır.
- **Hibrit OCR ve Çeviri**: Chrome OCR kullanılırken hız için Google Translate, Gemini/Groq/OpenAI motorları kullanılırken yapay zekâ destekli çeviri tercih edecek şekilde mantık optimize edildi.
- **Evrensel “Yapay Zekâ ile Yeniden Tara”**: Belge Okuyucu’nun yeniden tarama özelliği artık yalnızca Gemini ile sınırlı değil; etkin olan herhangi bir yapay zekâ sağlayıcısını kullanır. Şu anda sayfaları yeniden işlemek için aktif olan yapay zeka sağlayıcısını kullanıyor.

## 4.6 için Değişiklikler

- **Etkileşimli Sonuç Geri Çağırma:** Komut katmanına **Boşluk** tuşu eklendi; böylece “Doğrudan Çıktı” modu etkin olsa bile son yapay zekâ yanıtı takip soruları için anında yeniden açılabilir.
- **Telegram Topluluk Merkezi:** NVDA Araçlar menüsüne “Resmî Telegram Kanalı” bağlantısı eklendi.
- **Geliştirilmiş Yanıt Kararlılığı:** Doğrudan konuşma çıktısı kullanılırken daha güvenilir performans ve daha akıcı bir deneyim sağlamak için Çeviri, OCR ve Görsel özelliklerinin temel mantığı optimize edildi.
- **Geliştirilmiş Arayüz Yönlendirmesi:** Ayar açıklamaları ve belgeler, yeni geri çağırma sistemini daha iyi anlatacak şekilde güncellendi.

## 4.5 için Değişiklikler

- **Gelişmiş İstem Yöneticisi:** Varsayılan sistem istemlerini ve kullanıcı tanımlı istemleri yönetmek için özel bir iletişim kutusu eklendi.
- **Kapsamlı Proxy Desteği:** Kullanıcı tarafından yapılandırılan proxy ayarlarının tüm API isteklerine eksiksiz uygulanması sağlandı.
- **Otomatik Veri Geçişi:** Eski istem yapılandırmaları, ilk çalıştırmada veri kaybı olmadan v2 JSON formatına otomatik yükseltilir.
- **Güncellenmiş Uyumluluk (2025.1):** Belge Okuyucu gibi gelişmiş özellikler nedeniyle minimum NVDA sürümü 2025.1 olarak ayarlandı.
- **Ayarlar Arayüzü Optimizasyonu:** İstem yönetimi ayrı bir iletişim kutusuna taşındı.
- **İstem Değişkenleri Rehberi:** [selection], [clipboard] gibi değişkenleri tanıtan yerleşik rehber eklendi.

## 4.0.3 için Değişiklikler

- **Geliştirilmiş Ağ Dayanıklılığı:** Kararsız bağlantılar için otomatik yeniden deneme mekanizması eklendi.
- **Görsel Çeviri Diyaloğu:** Çeviri sonuçları için özel bir pencere eklendi. Kullanıcılar artık OCR sonuçlarına benzer şekilde, uzun çevirileri satır satır kolayca dolaşabilir ve okuyabilirler.
- **Birleştirilmiş Biçimlendirilmiş Görünüm:** İşlenen tüm sayfalar tek bir pencerede, net başlıklarla gösterilir.
- **OCR İş Akışı Optimizasyonu:** Tek sayfalı belgelerde sayfa aralığı seçimi atlanır.
- **Geliştirilmiş API Kararlılığı:** Daha sağlam bir başlık tabanlı kimlik doğrulama yöntemine geçildi, böylece anahtar döndürme çakışmalarından kaynaklanan olası "Tüm API Anahtarları başarısız oldu" hataları çözüldü.
- **Hata Düzeltmeleri:** Eklenti kapanışı ve sohbet penceresi odak sorunları giderildi.

## 4.0.1 için Değişiklikler

- **Gelişmiş Belge Okuyucu:** PDF ve görseller için sayfa aralığı seçimi ve arka plan işleme.
- **Yeni Araçlar Alt Menüsü:** NVDA Araçlar menüsüne “Vision Assistant” alt menüsü eklendi.
- **Esnek Özelleştirme:** OCR motoru ve TTS sesi ayarlardan seçilebilir.
- **Çoklu API Anahtarı Desteği:** Birden fazla Gemini API anahtarı için destek eklendi. Ayarlar bölümünden her satıra bir anahtar girebilir veya tuşları virgülle ayırabilirsiniz.
- **Alternatif OCR Motoru:** Kota sınırlarında güvenilir tanıma.
- **Akıllı API Anahtarı Döndürme:** En hızlı çalışan anahtara otomatik geçiş.
- **Belgeden MP3/WAV:** Okuyucu içinde ses dosyası oluşturma.
- **Instagram Hikayeleri Desteği:** Instagram Hikayelerini URL'lerini kullanarak tanımlama ve analiz etme özelliği eklendi.
- **TikTok Desteği:** TikTok videoları için destek eklendi; bu sayede videoların tam görsel açıklaması ve sesli transkripsiyonu sağlanabiliyor.
- **Yeniden Tasarlanmış Güncelleme Diyaloğu:** Yüklemeden önce sürüm değişikliklerini net bir şekilde okuyabilmeniz için kaydırılabilir metin kutusuna sahip yeni, erişilebilir bir arayüz sunar.
- **Birleşik Durum ve Kullanıcı Deneyimi:** Eklenti genelinde dosya iletişim kutuları standartlaştırıldı ve 'L' komutu gerçek zamanlı ilerlemeyi bildirecek şekilde geliştirildi.

## 3.6.0 için Değişiklikler

- **Yardım Sistemi:** Komut Katmanı'na, tüm kısayolların ve işlevlerinin kolay erişilebilir bir listesini sağlayan bir yardım komutu (`H`) eklendi.
- **Çevrim İçi Video Analizi:** **Twitter (X)** videoları desteği eklendi. Ayrıca daha güvenilir bir deneyim için URL algılama ve kararlılık da iyileştirildi.
- **Projeye Katkı:** Bağış iletişim kutusu eklendi.

## 3.5.0 için Değişiklikler

**Komut Katmanı:** Kısayolları tek bir ana tuş altında gruplandırmak için bir Komut Katmanı sistemi (varsayılan: `NVDA+Shift+V`) tanıtıldı. Örneğin, çeviri için `NVDA+Control+Shift+T` tuşlarına basmak yerine artık `NVDA+Shift+V` tuşlarına ve ardından `T` tuşuna basıyorsunuz.
**Çevrim İçi Video Analizi:** YouTube ve Instagram URL analizi.

## 3.1.0 için Değişiklikler

- **Doğrudan Çıktı Modu:** Daha hızlı ve sorunsuz bir deneyim için sohbet diyalogunu atlayıp yapay zeka yanıtlarını doğrudan ses yoluyla duyma seçeneği eklendi.
- **Pano Entegrasyonu:** Yapay zeka yanıtlarını otomatik olarak panoya kopyalamak için yeni bir ayar eklendi.

## 3.0 için Değişiklikler

- **Yeni Diller:** **Farsça** ve **Vietnamca**.
- **Genişletilmiş Yapay Zeka Modelleri:** Kullanıcıların ücretsiz ve kullanım oranı sınırlı (ücretli) modelleri ayırt etmelerine yardımcı olmak için model seçim listesi net ön eklerle (`[Ücretsiz]`, `[Profesyonel]`, `[Otomatik]`) yeniden düzenlendi. **Gemini 3.0 Pro** ve **Gemini 2.0 Flash Lite** için destek eklendi.
- **Dikte Kararlılığı:** Akıllı Dikte kararlılığında önemli ölçüde iyileşme sağlandı. Yapay zekâ yanılgılarını ve boş sonuçları önlemek için 1 saniyeden kısa ses kliplerini yok sayan bir güvenlik kontrolü eklendi.
- **Dosya İşleme:** İngilizce olmayan isimlere sahip dosyaların yüklenmesinin başarısız olmasına neden olan bir sorun düzeltildi.
- **İstem Optimizasyonu:** Geliştirilmiş çeviri mantığı ve yapılandırılmış görüntü sonuçları.

## 2.9 için Değişiklikler

- **Fransızca ve Türkçe çeviriler eklendi.**
- **Biçimlendirilmiş Görünüm:** Sohbet diyaloglarına, konuşmayı standart bir göz atılabilir pencerede uygun biçimlendirme (Başlıklar, Kalın Yazı, Kod) ile görüntülemek için "Biçimlendirilmiş Görünüm" düğmesi eklendi.
- **Markdown Ayarları:** Ayarlara "Sohbetlerde Markdown'ı Temizle" adlı yeni bir seçenek eklendi. Bu seçeneğin işaretini kaldırmak, kullanıcıların sohbet penceresinde ham Markdown sözdizimini (örneğin, `**`, `#`) görmelerini sağlar.
- **Görsel Çeviri Penceresi:** Uzun çevirileri satır satır okumaya uygun yeni pencere eklendi.
- **Kullanıcı Deneyimi İyileştirmeleri:** Dosya iletişim kutusu başlıkları "Aç" olarak standartlaştırıldı ve gereksiz sesli duyurular kaldırıldı (örneğin, "Menü açılıyor..."). daha sorunsuz bir deneyim için.

## 2.8 için Değişiklikler

- İtalyanca çeviri eklendi.
- **Durum Raporlama:** Eklentinin mevcut durumunu (örneğin, "Yükleniyor...", "Analiz ediliyor...") bildirmek için yeni bir komut (NVDA+Control+Shift+I) eklendi.
- **HTML Olarak Dışa Aktarma:** Sonuç iletişim kutularındaki "İçeriği Kaydet" düğmesi artık çıktıyı başlıklar ve kalın metin gibi stilleri koruyarak biçimlendirilmiş bir HTML dosyası olarak kaydediyor.
- **Ayarlar Arayüzü:** Ayarlar panelinin düzeni, erişilebilir gruplandırma ile iyileştirildi.
- **Yeni Modeller:** gemini-flash-latest ve gemini-flash-lite-latest için destek eklendi.
- **Diller:** Desteklenen dillere Nepalce eklendi.
- **Menü Mantığını İyileştirme:** NVDA arayüz dili İngilizce değilse "Metni İyileştir" komutlarının başarısız olmasına neden olan kritik bir hata düzeltildi.
- **Dikte:** Konuşma girişi olmadığında yanlış metin çıktısını önlemek için geliştirilmiş sessizlik algılama özelliği.
- **Güncelleme Ayarları:** Eklenti Mağazası politikalarına uymak için "Başlangıçta güncellemeleri kontrol et" seçeneği artık varsayılan olarak devre dışı bırakılmıştır.
- Kod temizliği.

## 2.7 için Değişiklikler

- Resmî NV Access Eklenti Şablonuna geçiş.
- HTTP 429 için otomatik yeniden deneme.
- Daha yüksek doğruluk ve daha iyi "Akıllı Değiştirme" mantığı işleme için optimize edilmiş çeviri istemleri.
- Rusça çeviri güncellemesi.

## 2.6 için Değişiklikler

- Rusça çeviri desteği.
- Bağlantı sorunlarıyla ilgili daha açıklayıcı geri bildirim sağlamak için hata mesajları güncellendi.
- Varsayılan hedef dil İngilizce yapıldı.

## 2.5 için Değişiklikler

- Yerel Dosya OCR Komutu Eklendi (NVDA+Control+Shift+F).
- Sonuç diyaloglarına "Sohbeti Kaydet" düğmesi eklendi.
- Tam yerelleştirme desteği.
- NVDA ton modülüne geçiş.
- PDF ve ses dosyalarının daha iyi işlenmesi için Gemini Dosya API'sine geçildi.
- Süslü parantez içeren metinlerin çevrilmesi sırasında oluşan çökme sorunu düzeltildi.

## 2.1.1 için Değişiklikler

- Özel İstemlerde [file_ocr] değişkeninin doğru çalışmaması sorunu giderildi.

## 2.1 için Değişiklikler

- Tüm kısayollar NVDA+Control+Shift standardına alındı.

## 2.0 için Değişiklikler

- Otomatik güncelleme sistemi.
- Daha önce çevrilmiş metinlerin anında alınması için Akıllı Çeviri Önbelleği eklendi.
- Sohbet diyaloglarında sonuçları bağlamsal olarak iyileştirmek için Konuşma Belleği özelliği eklendi.
- Panodan Çeviri için özel komut eklendi (NVDA+Control+Shift+Y).
- Hedef dil çıktısının kesin olarak uygulanmasını sağlamak için optimize edilmiş yapay zeka uyarıları.
- Özel karakter çökmesi düzeltildi.

## 1.5 için Değişiklikler

- 20’den fazla yeni dil desteği.
- Takip soruları için etkileşimli filtreleme iletişim kutusu uygulandı.
- Yerleşik Akıllı Dikte özelliği eklendi.
- NVDA Girdi Hareketleri iletişim kutusuna "Görsel Asistan" kategorisi eklendi.
- Firefox ve Word gibi belirli uygulamalardaki COMError çökmeleri düzeltildi.
- Sunucu hataları için otomatik yeniden deneme mekanizması eklendi.

## 1.0 için Değişiklikler

- İlk sürüm.
