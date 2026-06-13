# Profesyonel Görsel Asistan Belgeleri

**Profesyonel Görsel Asistan**, NVDA için gelişmiş, çok modlu bir yapay zekâ asistanıdır. Akıllı ekran okuma, çeviri, sesli dikte ve belge analizi sağlamak için dünya çapında yapay zekâ motorlarından yararlanır.

**Bu eklenti, Dünya Engelliler Günü onuruna topluluğa sunulmuştur.**

## 1. Kurulum ve Yapılandırma

**NVDA Menüsü > Tercihler > Ayarlar > Profesyonel Görsel Asistan** yolunu izleyin.

### 1.1 Bağlantı Ayarları

* **Sağlayıcı:** Tercih ettiğiniz yapay zekâ hizmetini seçin. Desteklenen sağlayıcılar: **Google Gemini**, **OpenAI**, **Mistral**, **Groq** ve **Özel** (Ollama / LM Studio gibi OpenAI uyumlu sunucular).
* **Önemli Not:** En iyi performans ve doğruluk için (**özellikle resim/dosya analizi** konusunda) **Google Gemini** kullanmanızı şiddetle öneririz.
* **API Anahtarı:** Zorunludur. Otomatik döndürme için birden fazla anahtar (virgül veya yeni satırla ayrılmış) girebilirsiniz.
* **Modelleri Al:** API anahtarınızı girdikten sonra, sağlayıcıdan mevcut en güncel model listesini indirmek için bu düğmeye basın.
* **Yapay Zekâ Modeli:** Genel sohbet ve analiz için kullanılacak ana modeli seçin.

### 1.2 Gelişmiş Model Yönlendirme (Yerel Sağlayıcılar)

*Gemini, OpenAI, Groq ve Mistral için kullanılabilir.*

> **⚠️ Uyarı:** Bu ayarlar **yalnızca ileri düzey kullanıcılar** içindir. Belirli bir modelin ne yaptığından emin değilseniz, lütfen bunu **işaretlemeyin**. Bir görev için uyumsuz bir model seçmek (örneğin Görsel analiz için yalnızca metin modeli) hatalara yol açar ve eklentinin çalışmasını durdurur.

Ayrıntılı denetimi açmak için **“Gelişmiş Model Yönlendirme (Göreve özgü)”** seçeneğini işaretleyin. Bu, farklı görevler için açılır listeden belirli modeller seçmenize olanak tanır:

* **OCR / Görsel Model:** Görselleri analiz etmek için özel bir model seçin.
* **Konuşmadan Metne (STT):** Dikte için belirli bir model seçin.
* **Metinden Konuşmaya (TTS):** Ses üretimi için bir model seçin.
* **Yapay Zeka Operatör Modeli:** Otonom bilgisayar operasyon görevleri için belirli bir model seçin.
  *Not: Desteklenmeyen özellikler (ör. Groq için TTS) otomatik olarak gizlenir.*

### 1.3 Gelişmiş Uç Nokta Yapılandırması (Özel Sağlayıcı)

*Yalnızca “Özel” seçildiğinde kullanılabilir.*

> **⚠️ Uyarı:** Bu bölüm manuel API yapılandırmasına izin verir ve yerel sunucular veya proxy’ler çalıştıran **ileri seviye kullanıcılar** için tasarlanmıştır. Hatalı URL’ler veya model adları bağlantıyı bozacaktır. Bu uç noktaların ne olduğunu tam olarak bilmiyorsanız, bunu **işaretlemeden bırakın**.

**“Gelişmiş Uç Nokta Yapılandırması”** seçeneğini işaretleyerek sunucu ayrıntılarını manuel olarak girin. Yerel sağlayıcılardan farklı olarak burada belirli URL’leri ve model adlarını **manuel olarak yazmanız** gerekir:

* **Model Listesi URL’si:** Mevcut modelleri almak için kullanılan uç nokta.
* **OCR/STT/TTS Uç Nokta URL’si:** Belirli hizmetler için tam URL’ler (ör. `http://localhost:11434/v1/audio/speech`).
* **Özel Modeller:** Her görev için model adını manuel olarak yazın (ör. `llama3:8b`).

### 1.3.1 Yerel YZ'yı Kurma (Tek Adımlı Yapılandırma)
Yerel ve tamamen çevrimdışı YZ entegrasyonunu son derece basit hale getirmek için, Özel Sağlayıcı Ayarları içinde özel bir **“Yerel YZ'yı Kur”** düğmesi bulunmaktadır.

Bilgisayarınızda yerel bir YZ modeli sunucusu çalıştırıyorsanız:
1. Sağlayıcı olarak **Özel**'i seçin.
2. **Yerel YZ'yı Kur** düğmesine basın.
3. Açılan iletişim kutusundan yerel YZ motorunuzu seçin:
   - **Ollama** (varsayılan olarak `http://127.0.0.1:11434`)
   - **LM Studio** (varsayılan olarak `http://127.0.0.1:1234`)
   - **Jan.ai** (varsayılan olarak `http://127.0.0.1:1337`)
   - **KoboldCPP** (varsayılan olarak `http://127.0.0.1:5001`)
4. Eklenti, doğru yerel URL'yi ve API türünü anında yapılandıracak ve **YZ Model** seçim kutusunu doldurmak için aktif çevrimdışı modellerinizi otomatik olarak getirecektir.

*Ağ ve Proxy'ler Hakkında Not:* Bu yerel bağlantı motoru, gelişmiş bir proxy atlama mekanizmasına sahiptir. Aktif bir sistem VPN'i veya TUN modu proxy'si çalıştırıyor olsanız bile, yerel AI istekleriniz bunu tamamen atlayarak 502 Bad Gateway hataları olmadan istikrarlı çevrimdışı bağlantılar sağlar.

### 1.4 Genel Tercihler

* **OCR Motoru:** Hızlı sonuçlar için **Chrome (Hızlı)** veya üstün düzen koruması için **Gemini (Biçimlendirilmiş)** seçeneklerinden birini seçin.

  * *Not:* “Gemini (Biçimlendirilmiş)” seçiliyken sağlayıcı OpenAI/Groq ise, eklenti görseli akıllıca etkin sağlayıcının görsel modeline yönlendirir.
* **TTS Sesi:** Tercih ettiğiniz ses stilini seçin. Bu liste etkin sağlayıcıya göre dinamik olarak güncellenir.
* **Yaratıcılık (Sıcaklık):** Yapay zekânın rastgeleliğini kontrol eder. Düşük değerler doğru çeviri/OCR için daha uygundur.
* **Proxy URL’si:** Bölgenizde yapay zekâ hizmetleri kısıtlıysa yapılandırın ( `127.0.0.1` gibi yerel proxy’ler veya köprü URL’leri desteklenir).

## 2. Komut Katmanı ve Kısayollar

Klavye çakışmalarını önlemek için bu eklenti bir **Komut Katmanı** kullanır.

1. Katmanı etkinleştirmek için **NVDA + Shift + V** (Ana Tuş) kombinasyonuna basın (bir bip sesi duyarsınız).
2. Tuşları bırakın ve ardından aşağıdaki tek tuşlardan birine basın:

| Tuş           | İşlev                    | Açıklama                                                                              |
| ------------- | ------------------------ | ------------------------------------------------------------------------------------- |
| **Shift + A** | **Yapay Zeka Operatörü**         | **Otonom Operasyon:** Yapay zekaya ekranınızda bir görev gerçekleştirmesini söyleyin.      |
| **E**         | **Kullanıcı Arayüzü Gezgini**          | **Etkileşimli Tıklama:** Herhangi bir uygulamadaki kullanıcı arayüzü öğelerini tanımlar ve tıklar.        |
| **T**         | Akıllı Çeviri          | Dolaşım imleci altındaki metni veya seçimi çevirir.                                    |
| **Shift + T** | Panodan Çeviri           | Panodaki içeriği çevirir.                                                             |
| **R**         | Metin İyileştirici       | Özetleme, dilbilgisi düzeltme, açıklama veya **Özel İstemler** çalıştırır.            |
| **V**         | Nesne Görsel Analizi     | Geçerli Dolaşım nesnesini betimler.                                                     |
| **O**         | Tam Ekran Görsel Analizi | Tüm ekran düzenini ve içeriğini analiz eder.                                          |
| **Shift + V** | Çevrim İçi Video Analizi | **YouTube**, **Instagram**, **TikTok** veya **Twitter (X)** videolarını analiz eder.  |
| **D**         | Belge Okuyucu            | Sayfa aralığı seçimi olan PDF ve görseller için gelişmiş okuyucu.                     |
| **F**         | **Akıllı Dosya Eylemi**    | Seçilen görüntü, PDF veya TIFF dosyalarından bağlama duyarlı tanıma.          |
| **A**         | Ses Dökümü               | MP3, WAV veya OGG dosyalarını metne dönüştürür.                                       |
| **C**         | CAPTCHA Çözücü           | CAPTCHA’ları yakalar ve çözer (Kamu portalları desteklenir).                          |
| **S**         | Akıllı Dikte             | Konuşmayı metne dönüştürür. Başlatmak için basın, durdurmak/yazmak için tekrar basın. |
| **I**         | Durumu Seslendir          | Geçerli durumu bildirir (ör. “Taranıyor…”, “Boşta”).                                  |
| **L**         | **Nesne Etiketleme**         | **Anlamsal Yapay Zeka Etiketleme:** Odaklanılan geçerli öğeyi/simgeyi kalıcı olarak etiketler. |
| **Shift + L** | **Etiketleri Yönet/Tara**   | Etiket Yöneticisini açar (etiketler varsa) veya uygulamayı adsız öğelere karşı tarar. |
| **U**         | Güncellemeleri Denetle      | Eklentinin en son sürümü için GitHub’ı manuel olarak kontrol eder.                    |
| **Boşluk Çubuğu**     | Son Sonucu Çağır         | Son yapay zekâ yanıtını inceleme veya devam için sohbet penceresinde gösterir.        |
| **H**         | Komut Yardımı            | Komut katmanındaki tüm kısayolların listesini gösterir.                               |

### 2.1 Belge Okuyucu Kısayolları (Görüntüleyici İçinde)

* **Ctrl + Sayfa Aşağı:** Sonraki sayfaya gider.
* **Ctrl + Sayfa Yukarı:** Önceki sayfaya gider.
* **Alt + A:** Belge hakkında soru sormak için sohbet penceresi açar.
* **Alt + R:** Etkin sağlayıcıyı kullanarak **Yapay Zekâ ile Yeniden Tarar**.
* **Alt + G:** Yüksek kaliteli bir ses dosyası (WAV/MP3) oluşturur ve kaydeder. *Sağlayıcı TTS desteklemiyorsa gizlenir.*
* **Alt + S / Ctrl + S:** Çıkarılan metni TXT veya HTML olarak kaydeder.

## 3. Özel İstemler ve Değişkenler

İstemleri **Ayarlar > İstemler > İstemleri Yönet…** yolundan yönetebilirsiniz.

### Desteklenen Değişkenler

* `[selection]`: Geçerli seçili metin.
* `[clipboard]`: Pano içeriği.
* `[screen_obj]`: Gezgin nesnesinin ekran görüntüsü.
* `[screen_full]`: Tam ekran görüntüsü.
* `[file_ocr]`: Metin çıkarımı için görsel/PDF dosyası seç.
* `[file_read]`: Okuma için belge seç (TXT, Kod, PDF).
* `[file_audio]`: Analiz için ses dosyası seç (MP3, WAV, OGG).

---

**Not:** Tüm yapay zekâ özellikleri için etkin bir internet bağlantısı gereklidir. Çok sayfalı belgeler otomatik olarak işlenir.

## 4. Destek ve Topluluk

En son haberler, özellikler ve sürümlerden haberdar olun:

* **Telegram Kanalı:** [https://t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
* **GitHub Issues:** Hata bildirimleri ve özellik istekleri için.

## 5. Proje Destekçileri

Cömert mali katkılarıyla bu projenin sürekli geliştirilmesini ve sürdürülmesini destekleyen topluluk üyelerimize yürekten teşekkür ederiz:

* **@Alyabani94**
*   **Ali Alamri**
*   **Ilya**
*Projeye finansal olarak destek olmak istiyorsanız ve adınızı burada görmek istiyorsanız, **Bağış Yap** seçeneğini NVDA Araçlar menüsünde (Profesyonel Görsel Asistan alt menüsü) veya kurulum sonrasında kurulum sürecinde bulabilirsiniz.*


---

## 6.1.0 Sürümündeki Değişiklikler

*   **Evrensel Yerel YZ Entegrasyonu (Yerel YZ'yı Kur)**: Özel Sağlayıcı Ayarları'na yeni bir **“Yerel AI'yı Kur”** düğmesi eklendi. Kullanıcılar artık **Ollama**, **LM Studio**, **Jan.ai** ve **KoboldCPP** dahil olmak üzere yerel AI motorlarını anında otomatik olarak yapılandırabilir.
*   **Akıllı Yerel Proxy Atlama**: Bağlantı mantığı, gelişmiş bir proxy atlama mekanizmasıyla yeniden oluşturuldu. Eklenti artık yerel loopback bağlantıları için Windows sistem proxy'lerini tamamen atlayacak kadar akıllıdır ve VPN/TUN modu etkin olsa bile istikrarlı yerel AI bağlantıları sağlar.
*   **Yapay Zeka Operatörü Acil Durum İptali (Shift+A)**: Çok talep edilen bir durdurma/iptal güvenlik tetikleyicisi eklendi. Otonom bir işlem çalışırken AI Operatörü komutuna (komut katmanı içinde **Shift+A**) basıldığında döngü anında iptal edilir ve *"AI Operatörü durduruldu"* duyurusu yapılır.
*   **Ultra Kararlı YZ Etiketleme (v2)**: Mutlak ekran koordinat anahtarları, gelişmiş, hibrit bir **Nesne İmzası** sistemi ile değiştirildi. Etiketler artık programlama tanımlayıcılarına (UIA **AutomationId** veya Win32 **ControlID**) ve pencereye göre koordinatlara dayanıyor; bu sayede özel etiketleriniz pencere boyutlandırma, taşıma, monitör değiştirme veya ölçeklendirmeye karşı tamamen dayanıklı hale geliyor.
*   **Sorunsuz Otomatik Etiket Taşıma**: Yükseltme işlemi tamamen şeffaftır. Eklenti, ilk odaklandığında eski koordinat tabanlı etiketlerinizi arka planda yeni kararlı parmak izi formatına otomatik olarak taşır ve veri kaybı yaşanmaz.
## 6.0 Sürümündeki Değişiklikler

*   **Anlamsal YZ Etiketleme Özelliği**: Kullanıcılar artık YZ kullanarak isimsiz düğmeleri ve simgeleri kalıcı olarak etiketleyebilir. **L** tuşuna basarak mevcut gezgin nesnesini etiketleyebilir (hem Sekme tuşuyla odaklanma hem de nesne gezintisi desteklenir) veya **Shift+L** tuşlarına basarak tüm uygulamayı tek seferde tarayıp etiketleyebilirsiniz.
*   **Akıllı Etiket Yönetimi**: Özel etiketleri görüntülemek, yeniden adlandırmak veya toplu olarak silmek için yeni, tamamen erişilebilir bir Etiket Yöneticisi iletişim kutusu eklendi (etiketler varsa **Shift+L** tuşlarıyla erişilebilir).
*   **Doğrudan Dosya Analizi (Dosya İletişim Kutusunu Atla)**: Eklenti artık, Windows Dosya Gezgini'nde bir PDF veya görüntü dosyasına odaklandığınızı algılayacak kadar akıllıdır. Vurgulanan bir dosya üzerinde **F (Akıllı Dosya Eylemi)** veya **D (Belge Okuyucu)** tuşuna basıldığında, standart “Aç” iletişim kutusu tamamen atlanarak dosya hemen işlenir.

## 5.6 İçin Değişiklikler

*   **“Yok (Metin Katmanını Ayıkla)” OCR Motoru eklendi**: Kullanıcılar artık YZ kredisi kullanmadan aranabilir PDF'lerden doğrudan metin ayıklayabilir; bu da metin tabanlı belgelerde hızı ve gizliliği önemli ölçüde artırır.
*   **UI Gezgini Doğruluğu İyileştirildi**: UI Gezgini istemini, öğe türlerini (Liste Öğeleri gibi) daha iyi tanımlayacak ve Görev Çubuğu ve Saat gibi Windows sistem bileşenlerini yok sayarak “(İşaretli)”, “(Seçili)” veya “(Genişletilmiş)” gibi durumları doğru bir şekilde bildirecek şekilde iyileştirildi.
*   **Kurulum Ayarları Hatırlatıcısı**: Kurulumdan sonra, kullanıcıları API anahtarlarını ve tercihlerini yapılandırmak için ayarlar menüsüne yönlendiren bir bildirim eklendi.

## 5.5.2 için değişiklikler

* **Yapay Zeka Operatörü Yazma Sorunu Düzeltildi:** Belirli sistemlerde metin yapıştırmak yerine 'v' harfinin yazılmasına neden olan bir hata çözüldü. Bu düzeltme, yüksek sistem yükü sırasında meydana gelen zamanlama çakışmalarını giderir.
* **Gelişmiş Kararlılık:** Sistem panosu diğer uygulamalar tarafından geçici olarak kilitlendiğinde eklentilerin çökmesini önlemek amacıyla pano işlemlerine yönelik güçlü hata yönetimi eklendi.
* **Zamanlama Optimizasyonu:** Farklı sistem hızlarında daha yüksek güvenilirlik ve üçüncü taraf Pano Yöneticileriyle daha iyi uyumluluk sağlamak amacıyla klavye olaylarına yönelik dahili gecikmeler ayarlandı.

## 5.5 İçin Değişiklikler (Otomasyon Güncellemesi)

*   **Yapay Zeka Operatörü (Otonom Kontrol - Shift+A):** Bu, v5.5'in en önemli özelliğidir. Profesyonel Görsel Asistan, pasif bir asistan olmaktan çıkıp kişisel **Yapay Zeka Operatörünüz** haline geldi. Yalnızca ekranı betimlemez; komut gerektirir.
   * *Nasıl çalışır:* Artık bilgisayarınızı çalıştırmak için sözlü talimatlar verebilirsiniz. Örneğin, ekran okuyucunuzun sessiz kaldığı, tamamen erişilemeyen bir uygulamada **Shift+A** tuşlarına basıp şunu yazabilirsiniz: *"Ayarlar düğmesine tıklayın"* veya *"Arama alanını bulun, 'Son Haberler' yazın ve enter tuşuna basın."* Yapay zeka, öğeleri görsel olarak betimler, fareyi hareket ettirir ve görevi sizin için yürütür.
    *   *Performans Notu:* Bu özellik **Gemini 3.0 Flash (Önizleme)** için optimize edilmiştir ve en karmaşık kullanıcı arayüzü düzenlerini bile işleyebilecek inanılmaz derecede hızlı ve akıllı yanıtlar sunar.
    *   **⚠️ API Kullanım Uyarısı:** Yapay Zeka Operatörünün doğru olması için tam olarak ne olduğunu "görmesi" gerektiğinden, her adımda yüksek çözünürlüklü bir ekran görüntüsü gönderir. Sık kullanımın API kotanızı standart metin tabanlı görevlere göre çok daha hızlı tüketeceğini lütfen unutmayın.
*   **Görsel Kullanıcı Arayüz Gezgini (E):** "Etiketlenmemiş düğmeler" arasında gezinmekten bıktınız mı? UI Explorer'ı etkinleştirmek için **E** tuşuna basın. Yapay zeka tüm pencereyi tarayacak ve simgeler, grafikler ve menüler dahil gördüğü her tıklanabilir öğenin bir listesini oluşturacaktır. Listeden bir öğe seçmeniz yeterlidir; yapay zeka Operatörü sizin için o öğeye tıklayacaktır. Bu, herhangi bir uygulamanın üstünde "erişilebilir bir katmana" sahip olmak gibidir.
*   **Bağlama Duyarlı Akıllı Dosya Eylemi (F):** "F" tuşu tamamen elden geçirildi. Artık yalnızca OCR istediğinizi varsaymıyor. Tek bir görsel seçtiğinizde artık akıllı bir şekilde amacınızı soruyor: Sahneyi anlamak için **Ayrıntılı Görsel Açıklama** veya okumak için **Yapılandırılmış Metin Çıkarma (OCR)** seçebilirsiniz. Menü, dosya türüne ve aktif AI motorunuza göre dinamik olarak uyarlanır.
*   **Çekirdek Optimizasyonu:** Eklentinin dahili mantığında derinlemesine bir temizlik gerçekleştirdik, kullanılmayan eski işlevleri ve gereksiz kodları kaldırdık. Bu, tüm kullanıcılar için daha yalın, daha hızlı ve daha güvenilir bir deneyimle sonuçlanır.

## 5.0 için Değişiklikler

* **Çoklu Sağlayıcı Mimarisi**: Google Gemini’ye ek olarak **OpenAI**, **Groq** ve **Mistral** için tam destek eklendi. Kullanıcılar artık tercih ettikleri yapay zekâ arka ucunu seçebilir.
* **Gelişmiş Model Yönlendirme**: Yerel sağlayıcı kullanıcıları (Gemini, OpenAI vb.) artık farklı görevler (OCR, STT, TTS) için açılır listeden belirli modelleri seçebilir.
* **Gelişmiş Uç Nokta Yapılandırması**: Özel sağlayıcı kullanıcıları, yerel veya üçüncü taraf sunucular üzerinde ayrıntılı denetim için belirli URL’leri ve model adlarını manuel olarak girebilir.
* **Akıllı Özellik Görünürlüğü**: Ayarlar menüsü ve Belge Okuyucu arayüzü, seçilen sağlayıcıya göre desteklenmeyen özellikleri (TTS gibi) otomatik olarak gizler.
* **Dinamik Model Getirme**: Eklenti, mevcut model listesini doğrudan sağlayıcının API’sinden alır; böylece yeni modeller yayınlanır yayınlanmaz uyumluluk sağlanır.
* **Hibrit OCR ve Çeviri**: Chrome OCR kullanılırken hız için Google Translate, Gemini/Groq/OpenAI motorları kullanılırken yapay zekâ destekli çeviri tercih edecek şekilde mantık optimize edildi.
* **Evrensel “Yapay Zekâ ile Yeniden Tara”**: Belge Okuyucu’nun yeniden tarama özelliği artık yalnızca Gemini ile sınırlı değil; etkin olan herhangi bir yapay zekâ sağlayıcısını kullanır.

## 4.6 için Değişiklikler

* **Etkileşimli Sonuç Geri Çağırma:** Komut katmanına **Boşluk** tuşu eklendi; böylece “Doğrudan Çıktı” modu etkin olsa bile son yapay zekâ yanıtı takip soruları için anında yeniden açılabilir.
* **Telegram Topluluk Merkezi:** NVDA Araçlar menüsüne “Resmî Telegram Kanalı” bağlantısı eklendi.
* **Yanıt Kararlılığı Artışı:** Çeviri, OCR ve Görsel analiz özelliklerinin çekirdek mantığı optimize edildi.
* **Geliştirilmiş Arayüz Yönlendirmesi:** Ayar açıklamaları ve belgeler, yeni geri çağırma sistemini daha iyi anlatacak şekilde güncellendi.

## 4.5 için Değişiklikler

* **Gelişmiş İstem Yöneticisi:** Varsayılan sistem istemlerini ve kullanıcı tanımlı istemleri yönetmek için özel bir iletişim kutusu eklendi.
* **Kapsamlı Proxy Desteği:** Kullanıcı tarafından yapılandırılan proxy ayarlarının tüm API isteklerine eksiksiz uygulanması sağlandı.
* **Otomatik Veri Geçişi:** Eski istem yapılandırmaları, ilk çalıştırmada veri kaybı olmadan v2 JSON formatına otomatik yükseltilir.
* **Güncellenmiş Uyumluluk (2025.1):** Belge Okuyucu gibi gelişmiş özellikler nedeniyle minimum NVDA sürümü 2025.1 olarak ayarlandı.
* **Ayarlar Arayüzü Optimizasyonu:** İstem yönetimi ayrı bir iletişim kutusuna taşındı.
* **İstem Değişkenleri Rehberi:** [selection], [clipboard] gibi değişkenleri tanıtan yerleşik rehber eklendi.

## 4.0.3 için Değişiklikler

* **Geliştirilmiş Ağ Dayanıklılığı:** Kararsız bağlantılar için otomatik yeniden deneme mekanizması eklendi.
* **Görsel Çeviri Penceresi:** Uzun çevirileri satır satır okumaya uygun yeni pencere eklendi.
* **Birleştirilmiş Biçimlendirilmiş Görünüm:** İşlenen tüm sayfalar tek bir pencerede, net başlıklarla gösterilir.
* **OCR İş Akışı Optimizasyonu:** Tek sayfalı belgelerde sayfa aralığı seçimi atlanır.
* **API Kararlılığı İyileştirmeleri:** Daha sağlam kimlik doğrulama yöntemine geçildi.
* **Hata Düzeltmeleri:** Eklenti kapanışı ve sohbet penceresi odak sorunları giderildi.

## 4.0.1 için Değişiklikler

* **Gelişmiş Belge Okuyucu:** PDF ve görseller için sayfa aralığı seçimi ve arka plan işleme.
* **Yeni Araçlar Alt Menüsü:** NVDA Araçlar menüsüne “Vision Assistant” alt menüsü eklendi.
* **Esnek Özelleştirme:** OCR motoru ve TTS sesi ayarlardan seçilebilir.
* **Çoklu API Anahtarı Desteği:** Birden fazla Gemini anahtarı desteği.
* **Alternatif OCR Motoru:** Kota sınırlarında güvenilir tanıma.
* **Akıllı API Anahtarı Döndürme:** En hızlı çalışan anahtara otomatik geçiş.
* **Belgeden MP3/WAV:** Okuyucu içinde ses dosyası oluşturma.
* **Instagram Hikâyeleri Desteği**
* **TikTok Desteği**
* **Yeniden Tasarlanan Güncelleme Penceresi**
* **Birleşik Durum ve UX**

## 3.6.0 için Değişiklikler

* **Yardım Sistemi:** Komut katmanına (`H`) yardım eklendi.
* **Çevrim İçi Video Analizi:** **Twitter (X)** videoları desteği eklendi.
* **Projeye Katkı:** Bağış iletişim kutusu eklendi.

## 3.5.0 için Değişiklikler

* **Komut Katmanı:** Varsayılan `NVDA+Shift+V`.
* **Çevrim İçi Video Analizi:** YouTube ve Instagram URL analizi.

## 3.1.0 için Değişiklikler

* **Doğrudan Çıktı Modu**
* **Pano Entegrasyonu**

## 3.0 için Değişiklikler

* **Yeni Diller:** **Farsça** ve **Vietnamca**
* **Genişletilmiş Yapay Zekâ Modelleri**
* **Dikte Kararlılığı İyileştirmeleri**
* **Dosya İşleme Düzeltmeleri**
* **İstem Optimizasyonu**

## 2.9 için Değişiklikler

* **Fransızca ve Türkçe çeviriler eklendi.**
* **Biçimlendirilmiş Görünüm**
* **Markdown Ayarı**
* **İletişim Kutusu Yönetimi**
* **Kullanıcı Deneyimi İyileştirmeleri**

## 2.8 için Değişiklikler

* İtalyanca çeviri eklendi.
* **Durum Bildirimi**
* **HTML Dışa Aktarma**
* **Ayarlar Arayüzü İyileştirmeleri**
* **Yeni Modeller**
* **Yeni Diller**
* **Dikte İyileştirmeleri**
* **Güncelleme Ayarları**
* Kod temizliği.

## 2.7 için Değişiklikler

* Resmî NV Access Eklenti Şablonuna geçiş.
* HTTP 429 için otomatik yeniden deneme.
* Çeviri istemleri optimizasyonu.
* Rusça çeviri güncellemesi.

## 2.6 için Değişiklikler

* Rusça çeviri desteği.
* Hata iletileri güncellendi.
* Varsayılan hedef dil İngilizce yapıldı.

## 2.5 için Değişiklikler

* Yerel Dosya OCR Komutu.
* “Sohbeti Kaydet” düğmesi.
* Tam yerelleştirme desteği.
* NVDA ton modülüne geçiş.
* Gemini Dosya API’sine geçiş.
* Süslü parantez hatası düzeltildi.

## 2.1.1 için Değişiklikler

* [file_ocr] değişkeni düzeltildi.

## 2.1 için Değişiklikler

* Tüm kısayollar NVDA+Control+Shift standardına alındı.

## 2.0 için Değişiklikler

* Otomatik güncelleme sistemi.
* Akıllı çeviri önbelleği.
* Sohbet belleği.
* Panoya özel çeviri komutu.
* Yapay zekâ istemleri optimizasyonu.
* Özel karakter çökmesi düzeltildi.

## 1.5 için Değişiklikler

* 20’den fazla yeni dil desteği.
* Etkileşimli iyileştirme penceresi.
* Akıllı dikte.
* NVDA Girdi Hareketleri kategorisi.
* COMError çökme düzeltmeleri.
* Otomatik yeniden deneme.

## 1.0 için Değişiklikler

* İlk sürüm.
