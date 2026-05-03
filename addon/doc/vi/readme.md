# Tài liệu hướng dẫn Vision Assistant Pro

**Vision Assistant Pro** là một trợ lý AI đa phương thức, nâng cao dành cho NVDA. Nó tận dụng các công cụ AI hàng đầu thế giới để cung cấp khả năng đọc màn hình thông minh, dịch thuật, đọc chính tả bằng giọng nói và phân tích tài liệu.

*Add-on này được phát hành cho cộng đồng nhằm tôn vinh Ngày Quốc tế Người khuyết tật.*

## 1. Thiết lập & Cấu hình

Đi tới **Menu NVDA > Tùy chọn > Cài đặt > Vision Assistant Pro**.

### 1.1 Cài đặt kết nối
- **Nhà cung cấp (Provider):** Chọn dịch vụ AI bạn ưu tiên. Các nhà cung cấp được hỗ trợ bao gồm **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, và **Tùy chỉnh** (các máy chủ tương thích OpenAI như Ollama/LM Studio).
- **Lưu ý quan trọng:** Chúng tôi khuyên bạn nên sử dụng **Google Gemini** để có hiệu suất và độ chính xác tốt nhất (đặc biệt là đối với phân tích hình ảnh/tệp).
- **Khóa API (API Key):** Bắt buộc. Bạn có thể nhập nhiều khóa (phân tách bằng dấu phẩy hoặc xuống dòng) để tự động luân phiên.
- **Tải mô hình (Fetch Models):** Sau khi nhập khóa API, nhấn nút này để tải xuống danh sách các mô hình mới nhất hiện có từ nhà cung cấp.
- **Mô hình AI:** Chọn mô hình chính được sử dụng cho trò chuyện và phân tích chung.

### 1.2 Định tuyến mô hình nâng cao (Advanced Model Routing)
*Khả dụng cho tất cả các nhà cung cấp bao gồm Gemini, OpenAI, Groq, Mistral và Tùy chỉnh.*

> **⚠️ Cảnh báo:** Các cài đặt này chỉ dành cho **người dùng nâng cao**. Nếu bạn không chắc chắn một mô hình cụ thể làm gì, vui lòng để trống phần này. Việc chọn một mô hình không tương thích cho một tác vụ (ví dụ: chọn mô hình chỉ có văn bản cho Thị giác) sẽ gây ra lỗi và khiến add-on ngừng hoạt động.

Chọn **"Định tuyến mô hình nâng cao (Theo tác vụ)"** để mở khóa quyền kiểm soát chi tiết. Điều này cho phép bạn chọn các mô hình cụ thể từ danh sách thả xuống cho các tác vụ khác nhau:
- **Mô hình OCR / Thị giác:** Chọn một mô hình chuyên dụng để phân tích hình ảnh.
- **Chuyển giọng nói thành văn bản (STT):** Chọn một mô hình cụ thể để đọc chính tả.
- **Chuyển văn bản thành giọng nói (TTS):** Chọn một mô hình để tạo âm thanh.
- **Mô hình AI Operator:** Chọn một mô hình cụ thể cho các tác vụ điều khiển máy tính tự động.
*Lưu ý: Các tính năng không được hỗ trợ (ví dụ: TTS cho Groq) sẽ tự động bị ẩn.*

### 1.3 Cấu hình Endpoint nâng cao (Nhà cung cấp tùy chỉnh)
*Chỉ khả dụng khi chọn "Tùy chỉnh".*

> **⚠️ Cảnh báo:** Phần này cho phép cấu hình API thủ công và được thiết kế cho **người dùng chuyên sâu** đang chạy các máy chủ cục bộ hoặc proxy. URL hoặc tên mô hình không chính xác sẽ làm mất kết nối. Nếu bạn không biết chính xác các endpoint này là gì, hãy để trống.

Chọn **"Cấu hình Endpoint nâng cao"** để nhập chi tiết máy chủ theo cách thủ công. Không giống như các nhà cung cấp gốc, tại đây bạn phải **tự nhập** các URL và Tên mô hình cụ thể:
- **URL danh sách mô hình (Models List URL):** Endpoint để tải các mô hình hiện có.
- **URL Endpoint OCR/STT/TTS:** URL đầy đủ cho các dịch vụ cụ thể (ví dụ: `http://localhost:11434/v1/audio/speech`).
- **Mô hình tùy chỉnh:** Nhập thủ công tên mô hình (ví dụ: `llama3:8b`) cho từng tác vụ.

### 1.4 Tùy chọn chung
- **Công cụ OCR:** Chọn giữa **Chrome (Fast)** để có kết quả nhanh hoặc **AI (Advanced)** để nhận dạng bố cục vượt trội.
    - *Lưu ý:* Nếu bạn chọn "AI (Advanced)" nhưng nhà cung cấp được đặt là OpenAI/Groq, add-on sẽ thông minh tự chuyển hình ảnh đến mô hình thị giác của nhà cung cấp đó.
- **Giọng nói TTS:** Chọn kiểu giọng nói ưu thích của bạn. Danh sách này cập nhật động dựa trên nhà cung cấp đang hoạt động.
- **Độ sáng tạo (Temperature):** Kiểm soát tính ngẫu nhiên của AI. Giá trị thấp hơn sẽ tốt hơn cho độ chính xác của dịch thuật/OCR.
- **URL Proxy:** Cấu hình nếu các dịch vụ AI bị hạn chế ở khu vực của bạn (hỗ trợ proxy cục bộ như `127.0.0.1` hoặc các URL cầu nối).

## 2. Lớp lệnh & Phím tắt

Để ngăn ngừa xung đột bàn phím, add-on này sử dụng một **Lớp lệnh (Command Layer)**.
1. Nhấn **NVDA + Shift + V** (Phím chính) để kích hoạt lớp lệnh (bạn sẽ nghe thấy tiếng bíp).
2. Nhả các phím, sau đó nhấn một trong các phím đơn sau:

| Phím | Chức năng | Mô tả |
| --- | --- | --- |
| **Shift + A** | **AI Operator** | **Điều khiển tự động:** Yêu cầu AI thực hiện một tác vụ trực tiếp trên màn hình của bạn. |
| **E** | **UI Explorer** | **Click tương tác:** Nhận diện và click vào các thành phần giao diện trong bất kỳ ứng dụng nào. |
| **T** | Dịch thông minh | Dịch văn bản dưới con trỏ navigator hoặc vùng đang chọn. |
| **Shift + T** | Dịch Clipboard | Dịch nội dung hiện có trong clipboard. |
| **R** | Tinh chỉnh văn bản | Tóm tắt, Sửa ngữ pháp, Giải thích hoặc chạy các **Prompt tùy chỉnh**. |
| **V** | Thị giác đối tượng | Mô tả đối tượng navigator hiện tại. |
| **O** | Thị giác toàn màn hình | Phân tích toàn bộ bố cục và nội dung màn hình. |
| **Shift + V** | Phân tích Video trực tuyến | Phân tích video trên **YouTube**, **Instagram**, **TikTok**, hoặc **Twitter (X)**. |
| **D** | Trình đọc tài liệu | Trình đọc nâng cao cho PDF và hình ảnh với tùy chọn chọn phạm vi trang. |
| **F** | **Hành động tệp thông minh** | Nhận diện theo ngữ cảnh từ các tệp hình ảnh, PDF hoặc TIFF được chọn. |
| **A** | Chuyển biên âm thanh | Chuyển biên các tệp MP3, WAV hoặc OGG thành văn bản. |
| **C** | Giải CAPTCHA | Chụp và giải mã CAPTCHA trên màn hình hoặc đối tượng navigator. |
| **S** | Đọc chính tả thông minh | Chuyển đổi giọng nói thành văn bản. Nhấn để bắt đầu ghi âm, nhấn lần nữa để dừng/gõ văn bản. |
| **L** | Thông báo trạng thái | Thông báo tiến trình hiện tại (ví dụ: "Đang quét...", "Nhàn rỗi"). |
| **U** | Kiểm tra cập nhật | Kiểm tra thủ công trên GitHub để tìm phiên bản mới nhất của add-on. |
| **Space** | Gọi lại kết quả cuối | Hiển thị phản hồi cuối cùng của AI trong hộp thoại trò chuyện để xem lại hoặc hỏi tiếp. |
| **H** | Trợ giúp lệnh | Hiển thị danh sách tất cả các phím tắt có sẵn trong lớp lệnh. |

### 2.1 Phím tắt Trình đọc tài liệu (Bên trong Trình xem)
- **Ctrl + PageDown:** Chuyển đến trang tiếp theo.
- **Ctrl + PageUp:** Chuyển đến trang trước đó.
- **Alt + A:** Mở hộp thoại trò chuyện để đặt câu hỏi về tài liệu.
- **Alt + R:** Buộc **Quét lại bằng AI** bằng nhà cung cấp hiện tại của bạn.
- **Alt + G:** Tạo và lưu tệp âm thanh chất lượng cao (WAV/MP3). *Ẩn nếu nhà cung cấp không hỗ trợ TTS.*
- **Alt + S / Ctrl + S:** Lưu văn bản được trích xuất dưới dạng tệp TXT hoặc HTML.

## 3. Prompt tùy chỉnh & Biến

Bạn có thể quản lý các prompt trong **Cài đặt > Prompts > Manage Prompts...**.

### Các biến được hỗ trợ
- `[selection]`: Văn bản hiện đang được chọn.
- `[clipboard]`: Nội dung clipboard.
- `[screen_obj]`: Ảnh chụp màn hình của đối tượng navigator.
- `[screen_full]`: Ảnh chụp toàn bộ màn hình.
- `[file_ocr]`: Chọn tệp hình ảnh/PDF để trích xuất văn bản.
- `[file_read]`: Chọn tài liệu để đọc (TXT, Code, PDF).
- `[file_audio]`: Chọn tệp âm thanh để phân tích (MP3, WAV, OGG).

***
**Lưu ý:** Cần có kết nối internet đang hoạt động cho tất cả các tính năng AI. Tài liệu nhiều trang được xử lý tự động.

## 4. Hỗ trợ & Cộng đồng

Cập nhật những tin tức, tính năng và bản phát hành mới nhất:
- **Kênh Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Dành cho báo cáo lỗi và yêu cầu tính năng.

---

## Những thay đổi trong phiên bản 5.5 (Bản cập nhật Tự động hóa)

* **AI Operator (Điều khiển tự động - Shift+A):** Đây là tính năng sáng giá nhất của v5.5. Vision Assistant Pro đã nâng cấp từ một trợ lý thụ động thành **AI Operator** cá nhân của bạn. Nó không chỉ mô tả màn hình mà còn thực sự nắm quyền điều khiển.
    * *Cách thức hoạt động:* Giờ đây bạn có thể đưa ra các chỉ dẫn bằng văn bản để vận hành máy tính. Ví dụ, trong một ứng dụng hoàn toàn không tiếp cận được nơi trình đọc màn hình im lặng, bạn có thể nhấn **Shift+A** và nhập: *"Click vào nút Cài đặt"* hoặc *"Tìm ô tìm kiếm, nhập 'Tin tức mới nhất' rồi nhấn enter."* AI sẽ nhận diện các thành phần bằng hình ảnh, di chuyển chuột và thực hiện tác vụ cho bạn.
    * *Lưu ý về hiệu suất:* Tính năng này được tối ưu hóa cho **Gemini 3.0 Flash (Bản xem trước)**, mang lại phản hồi cực nhanh và thông minh, có thể xử lý cả những bố cục giao diện phức tạp nhất.
    * **⚠️ Cảnh báo sử dụng API:** Vì AI Operator cần "nhìn" chính xác những gì đang diễn ra để đảm bảo độ chính xác, nó sẽ gửi ảnh chụp màn hình độ phân giải cao sau mỗi bước. Lưu ý rằng việc sử dụng thường xuyên sẽ tiêu tốn hạn ngạch API nhanh hơn nhiều so với các tác vụ văn bản thông thường.
* **Trình thám hiểm giao diện (UI Explorer - E):** Bạn mệt mỏi vì phải điều hướng qua các "nút không nhãn"? Nhấn **E** để kích hoạt UI Explorer. AI sẽ quét toàn bộ cửa sổ và tạo danh sách mọi thành phần có thể click mà nó thấy—bao gồm cả icon, đồ họa và menu. Chỉ cần chọn một mục từ danh sách và AI Operator sẽ click giúp bạn. Nó giống như việc thêm một "lớp tiếp cận" lên trên bất kỳ ứng dụng nào.
* **Hành động tệp thông minh theo ngữ cảnh (F):** Phím "F" đã được đại tu hoàn toàn. Nó không còn mặc định là bạn chỉ muốn OCR nữa. Khi bạn chọn một hình ảnh, nó sẽ hỏi ý định của bạn: bạn có thể chọn **Mô tả hình ảnh chi tiết** để hiểu bối cảnh hoặc **Trích xuất văn bản có cấu trúc (OCR)** để đọc. Menu sẽ thay đổi linh hoạt dựa trên loại tệp và công cụ AI bạn đang dùng.
* **Tối ưu hóa cốt lõi:** Chúng tôi đã dọn dẹp sâu logic nội bộ của add-on, loại bỏ các hàm cũ không còn sử dụng và mã dư thừa. Điều này giúp add-on nhẹ hơn, nhanh hơn và hoạt động ổn định hơn cho tất cả người dùng.

## Những thay đổi trong phiên bản 5.0

* **Kiến trúc đa nhà cung cấp**: Bổ sung hỗ trợ đầy đủ cho **OpenAI**, **Groq**, và **Mistral** bên cạnh Google Gemini. Người dùng hiện có thể chọn backend AI ưa thích của mình.
* **Định tuyến mô hình nâng cao**: Người dùng các nhà cung cấp gốc (Gemini, OpenAI, v.v.) hiện có thể chọn các mô hình cụ thể từ danh sách thả xuống cho các tác vụ khác nhau (OCR, STT, TTS).
* **Cấu hình Endpoint nâng cao**: Người dùng nhà cung cấp tùy chỉnh có thể nhập thủ công các URL và tên mô hình cụ thể để kiểm soát chi tiết các máy chủ cục bộ hoặc bên thứ ba.
* **Hiển thị tính năng thông minh**: Menu cài đặt và giao diện Trình đọc tài liệu giờ đây tự động ẩn các tính năng không được hỗ trợ (như TTS) dựa trên nhà cung cấp đã chọn.
* **Tìm nạp mô hình động**: Add-on hiện tìm nạp danh sách mô hình có sẵn trực tiếp từ API của nhà cung cấp, đảm bảo khả năng tương thích với các mô hình mới ngay khi chúng được phát hành.
* **Kết hợp OCR & Dịch thuật**: Tối ưu hóa logic để sử dụng Google Dịch nhằm tăng tốc độ khi dùng Chrome OCR, và dịch thuật bằng AI khi dùng các công cụ Gemini/Groq/OpenAI.
* **"Quét lại bằng AI" toàn cầu**: Tính năng quét lại của Trình đọc tài liệu không còn bị giới hạn ở Gemini. Giờ đây, tính năng này sử dụng bất kỳ nhà cung cấp AI nào đang hoạt động để xử lý lại các trang.

## Những thay đổi trong phiên bản 4.6
* **Gọi lại kết quả tương tác:** Đã thêm phím **Space** vào lớp lệnh, cho phép người dùng mở lại ngay lập tức phản hồi cuối cùng của AI trong cửa sổ trò chuyện để đặt câu hỏi tiếp theo, ngay cả khi chế độ "Đầu ra trực tiếp" đang hoạt động.
* **Cộng đồng Telegram:** Đã thêm liên kết "Kênh Telegram chính thức" vào menu Công cụ của NVDA, cung cấp một cách nhanh chóng để cập nhật những tin tức, tính năng và bản phát hành mới nhất.
* **Tăng cường độ ổn định của phản hồi:** Tối ưu hóa logic cốt lõi cho các tính năng Dịch thuật, OCR và Thị giác để đảm bảo hiệu suất đáng tin cậy hơn và trải nghiệm mượt mà hơn khi sử dụng đầu ra giọng nói trực tiếp.
* **Cải thiện hướng dẫn giao diện:** Đã cập nhật các mô tả cài đặt và tài liệu hướng dẫn để giải thích rõ hơn về hệ thống gọi lại mới và cách thức hoạt động của nó cùng với các cài đặt đầu ra trực tiếp.

## Những thay đổi trong phiên bản 4.5
* **Trình quản lý Prompt nâng cao:** Giới thiệu một hộp thoại quản lý chuyên dụng trong cài đặt để tùy chỉnh các prompt hệ thống mặc định và quản lý các prompt do người dùng xác định với hỗ trợ đầy đủ cho việc thêm, sửa, sắp xếp lại và xem trước.
* **Hỗ trợ Proxy toàn diện:** Đã giải quyết các sự cố kết nối mạng bằng cách đảm bảo rằng các cài đặt proxy do người dùng định cấu hình được áp dụng nghiêm ngặt cho tất cả các yêu cầu API, bao gồm dịch thuật, OCR và tạo giọng nói.
* **Di chuyển dữ liệu tự động:** Tích hợp hệ thống di chuyển thông minh để tự động nâng cấp các cấu hình prompt cũ sang định dạng v2 JSON mạnh mẽ trong lần chạy đầu tiên mà không làm mất dữ liệu.
* **Cập nhật khả năng tương thích (2025.1):** Đặt phiên bản NVDA yêu cầu tối thiểu thành 2025.1 do sự phụ thuộc thư viện trong các tính năng nâng cao như Trình đọc tài liệu để đảm bảo hiệu suất ổn định.
* **Tối ưu hóa giao diện cài đặt:** Sắp xếp hợp lý giao diện cài đặt bằng cách tổ chức lại việc quản lý prompt thành một hộp thoại riêng biệt, mang lại trải nghiệm người dùng rõ ràng và dễ tiếp cận hơn.
* **Hướng dẫn về biến Prompt:** Đã thêm hướng dẫn tích hợp trong các hộp thoại prompt để giúp người dùng dễ dàng xác định và sử dụng các biến động như `[selection]`, `[clipboard]`, và `[screen_obj]`.

## Những thay đổi trong phiên bản 4.0.3
* **Tăng cường độ ổn định mạng:** Đã thêm cơ chế thử lại tự động để xử lý tốt hơn các kết nối internet không ổn định và lỗi máy chủ tạm thời, đảm bảo phản hồi AI đáng tin cậy hơn.
* **Hộp thoại dịch trực quan:** Giới thiệu một cửa sổ dành riêng cho kết quả dịch. Người dùng giờ đây có thể dễ dàng điều hướng và đọc các bản dịch dài theo từng dòng, tương tự như kết quả OCR.
* **Chế độ xem định dạng tổng hợp:** Tính năng "View Formatted" trong Trình đọc tài liệu hiện hiển thị tất cả các trang đã xử lý trong một cửa sổ duy nhất, được tổ chức với các tiêu đề trang rõ ràng.
* **Tối ưu hóa quy trình OCR:** Tự động bỏ qua việc chọn phạm vi trang đối với các tài liệu chỉ có một trang, giúp quá trình nhận dạng diễn ra nhanh chóng và liền mạch hơn.
* **Cải thiện độ ổn định API:** Chuyển sang phương thức xác thực dựa trên header mạnh mẽ hơn, giải quyết các lỗi "All API Keys failed" tiềm ẩn do xung đột khi luân phiên khóa.
* **Sửa lỗi:** Đã giải quyết một số sự cố treo có thể xảy ra, bao gồm sự cố trong quá trình tắt add-on và lỗi tiêu điểm trong hộp thoại trò chuyện.

## Những thay đổi trong phiên bản 4.0.1
* **Trình đọc tài liệu nâng cao:** Một trình xem mới, mạnh mẽ dành cho PDF và hình ảnh với khả năng chọn phạm vi trang, xử lý nền và điều hướng liền mạch bằng `Ctrl+PageUp/Down`.
* **Menu con Tools mới:** Đã thêm một menu con "Vision Assistant" chuyên dụng bên dưới menu Tools của NVDA để truy cập nhanh hơn vào các tính năng cốt lõi, cài đặt và tài liệu hướng dẫn.
* **Tùy chỉnh linh hoạt:** Giờ đây, bạn có thể chọn công cụ OCR và giọng nói TTS ưa thích trực tiếp từ bảng cài đặt.
* **Hỗ trợ nhiều khóa API:** Đã thêm hỗ trợ cho nhiều khóa API Gemini. Bạn có thể nhập một khóa trên mỗi dòng hoặc phân tách chúng bằng dấu phẩy trong cài đặt.
* **Công cụ OCR thay thế:** Giới thiệu một công cụ OCR mới để đảm bảo nhận dạng văn bản đáng tin cậy ngay cả khi đạt đến giới hạn hạn ngạch của Gemini API.
* **Luân phiên Khóa API thông minh:** Tự động chuyển sang và ghi nhớ khóa API hoạt động nhanh nhất để vượt qua giới hạn hạn ngạch.
* **Tài liệu sang MP3/WAV:** Tích hợp khả năng tạo và lưu các tệp âm thanh chất lượng cao ở cả định dạng MP3 (128kbps) và WAV trực tiếp trong trình đọc.
* **Hỗ trợ Instagram Stories:** Đã thêm khả năng mô tả và phân tích Instagram Stories bằng URL của chúng.
* **Hỗ trợ TikTok:** Giới thiệu hỗ trợ cho các video TikTok, cho phép mô tả hình ảnh đầy đủ và chuyển biên âm thanh của các đoạn clip.
* **Hộp thoại cập nhật được thiết kế lại:** Cung cấp một giao diện mới, dễ tiếp cận với hộp văn bản có thể cuộn để đọc rõ các thay đổi của phiên bản trước khi cài đặt.
* **Trạng thái & UX thống nhất:** Chuẩn hóa các hộp thoại tệp trên toàn bộ add-on và cải tiến lệnh 'L' để báo cáo tiến trình theo thời gian thực.

## Những thay đổi trong phiên bản 3.6.0

* **Hệ thống trợ giúp:** Đã thêm lệnh trợ giúp (`H`) trong Lớp lệnh để cung cấp một danh sách dễ truy cập gồm tất cả các phím tắt và chức năng của chúng.
* **Phân tích Video trực tuyến:** Mở rộng hỗ trợ để bao gồm các video trên **Twitter (X)**. Đồng thời cải thiện khả năng phát hiện URL và độ ổn định để có trải nghiệm đáng tin cậy hơn.
* **Đóng góp cho dự án:** Đã thêm hộp thoại quyên góp tùy chọn cho những người dùng muốn ủng hộ các bản cập nhật trong tương lai và sự phát triển liên tục của dự án.

## Những thay đổi trong phiên bản 3.5.0

* **Lớp lệnh:** Giới thiệu hệ thống Lớp lệnh (mặc định: `NVDA+Shift+V`) để nhóm các phím tắt dưới một phím chính duy nhất. Ví dụ: thay vì nhấn `NVDA+Control+Shift+T` để dịch, giờ đây bạn nhấn `NVDA+Shift+V` theo sau là `T`.
* **Phân tích Video trực tuyến:** Đã thêm tính năng mới để phân tích trực tiếp các video trên YouTube và Instagram bằng cách cung cấp URL.

## Những thay đổi trong phiên bản 3.1.0

* **Chế độ Đầu ra trực tiếp:** Đã thêm tùy chọn để bỏ qua hộp thoại trò chuyện và nghe thẳng các phản hồi của AI qua giọng nói để có trải nghiệm nhanh chóng và liền mạch hơn.
* **Tích hợp Clipboard:** Đã thêm một cài đặt mới để tự động sao chép các phản hồi của AI vào clipboard.

## Những thay đổi trong phiên bản 3.0

* **Ngôn ngữ mới:** Đã thêm bản dịch tiếng **Ba Tư** và tiếng **Việt**.
* **Mở rộng mô hình AI:** Tổ chức lại danh sách chọn mô hình với các tiền tố rõ ràng (`[Free]`, `[Pro]`, `[Auto]`) để giúp người dùng phân biệt giữa các mô hình miễn phí và giới hạn tốc độ (trả phí). Đã thêm hỗ trợ cho **Gemini 3.0 Pro** và **Gemini 2.0 Flash Lite**.
* **Độ ổn định khi Đọc chính tả:** Cải thiện đáng kể độ ổn định của tính năng Đọc chính tả thông minh. Đã thêm kiểm tra an toàn để bỏ qua các đoạn âm thanh ngắn hơn 1 giây, ngăn chặn hiện tượng AI "ảo giác" và các lỗi trống.
* **Xử lý tệp:** Đã sửa lỗi tải lên các tệp có tên không phải tiếng Anh bị thất bại.
* **Tối ưu hóa Prompt:** Cải thiện logic Dịch thuật và cấu trúc lại kết quả của Thị giác.

## Những thay đổi trong phiên bản 2.9

* **Đã thêm bản dịch tiếng Pháp và tiếng Thổ Nhĩ Kỳ.**
* **Chế độ xem định dạng:** Đã thêm nút "View Formatted" trong các hộp thoại trò chuyện để xem cuộc hội thoại với định dạng chuẩn (Tiêu đề, In đậm, Code) trong một cửa sổ có thể duyệt qua tiêu chuẩn.
* **Cài đặt Markdown:** Đã thêm tùy chọn mới "Clean Markdown in Chat" trong phần Cài đặt. Bỏ chọn tùy chọn này cho phép người dùng xem cú pháp Markdown gốc (ví dụ: `**`, `#`) trong cửa sổ trò chuyện.
* **Quản lý hộp thoại:** Đã sửa sự cố trong đó cửa sổ "Refine Text" hoặc cửa sổ trò chuyện sẽ mở nhiều lần hoặc không lấy được tiêu điểm chính xác.
* **Cải tiến UX:** Chuẩn hóa các tiêu đề hộp thoại tệp thành "Open" và loại bỏ các thông báo giọng nói dư thừa (ví dụ: "Opening menu...") để có trải nghiệm mượt mà hơn.

## Những thay đổi trong phiên bản 2.8

* Đã thêm bản dịch tiếng Ý.
* **Thông báo trạng thái:** Đã thêm một lệnh mới (NVDA+Control+Shift+I) để thông báo trạng thái hiện tại của add-on (ví dụ: "Uploading...", "Analyzing...").
* **Xuất HTML:** Nút "Save Content" trong các hộp thoại kết quả hiện lưu đầu ra dưới dạng tệp HTML được định dạng, giữ nguyên các kiểu như tiêu đề và chữ in đậm.
* **Giao diện Cài đặt:** Cải thiện bố cục bảng Cài đặt với các nhóm dễ tiếp cận hơn.
* **Các mô hình mới:** Đã thêm hỗ trợ cho gemini-flash-latest và gemini-flash-lite-latest.
* **Ngôn ngữ:** Đã thêm tiếng Nepal vào các ngôn ngữ được hỗ trợ.
* **Logic menu Refine:** Đã sửa một lỗi nghiêm trọng khiến các lệnh "Refine Text" bị lỗi nếu ngôn ngữ giao diện NVDA không phải là tiếng Anh.
* **Đọc chính tả:** Cải thiện tính năng phát hiện khoảng lặng để ngăn chặn đầu ra văn bản không chính xác khi không có giọng nói được nhập vào.
* **Cài đặt cập nhật:** Tính năng "Check for updates on startup" hiện bị tắt theo mặc định để tuân thủ các chính sách của Add-on Store.
* Dọn dẹp mã nguồn.

## Những thay đổi trong phiên bản 2.7

* Chuyển đổi cấu trúc dự án sang Mẫu Add-on chính thức của NV Access để tuân thủ các tiêu chuẩn tốt hơn.
* Đã triển khai logic thử lại tự động cho các lỗi HTTP 429 (Rate Limit) để đảm bảo độ tin cậy trong thời gian lưu lượng truy cập cao.
* Tối ưu hóa các prompt dịch thuật để có độ chính xác cao hơn và xử lý logic "Smart Swap" tốt hơn.
* Đã cập nhật bản dịch tiếng Nga.

## Những thay đổi trong phiên bản 2.6

* Đã thêm hỗ trợ bản dịch tiếng Nga (Cảm ơn nvda-ru).
* Cập nhật các thông báo lỗi để cung cấp phản hồi mang tính mô tả cao hơn về vấn đề kết nối.
* Thay đổi ngôn ngữ đích mặc định thành tiếng Anh.

## Những thay đổi trong phiên bản 2.5

* Đã thêm lệnh Native File OCR (NVDA+Control+Shift+F).
* Đã thêm nút "Save Chat" vào các hộp thoại kết quả.
* Đã triển khai hỗ trợ bản địa hóa đầy đủ (i18n).
* Đã chuyển các phản hồi âm thanh sang mô-đun tones gốc của NVDA.
* Chuyển sang sử dụng Gemini File API để xử lý tốt hơn các tệp PDF và âm thanh.
* Đã sửa lỗi treo khi dịch văn bản có chứa dấu ngoặc nhọn.

## Những thay đổi trong phiên bản 2.1.1

* Đã sửa sự cố trong đó biến `[file_ocr]` không hoạt động bình thường trong Custom Prompts.

## Những thay đổi trong phiên bản 2.1

* Chuẩn hóa tất cả các phím tắt để sử dụng NVDA+Control+Shift nhằm loại bỏ xung đột với bố cục Bàn phím Laptop của NVDA và các phím nóng hệ thống.

## Những thay đổi trong phiên bản 2.0

* Đã triển khai hệ thống Tự động cập nhật tích hợp sẵn.
* Đã thêm Bộ nhớ đệm Dịch thông minh để truy xuất tức thì các văn bản đã dịch trước đó.
* Đã thêm Bộ nhớ hội thoại để tinh chỉnh kết quả theo ngữ cảnh trong các hộp thoại trò chuyện.
* Đã thêm Lệnh dịch Clipboard chuyên dụng (NVDA+Control+Shift+Y).
* Tối ưu hóa các prompt AI để thực thi nghiêm ngặt đầu ra ngôn ngữ đích.
* Đã sửa lỗi treo do các ký tự đặc biệt trong văn bản đầu vào.

## Những thay đổi trong phiên bản 1.5

* Đã thêm hỗ trợ cho hơn 20 ngôn ngữ mới.
* Đã triển khai Hộp thoại Tinh chỉnh Tương tác cho các câu hỏi tiếp theo.
* Đã thêm tính năng Đọc chính tả thông minh gốc.
* Đã thêm danh mục "Vision Assistant" vào hộp thoại Input Gestures của NVDA.
* Đã sửa các lỗi treo COMError trong một số ứng dụng cụ thể như Firefox và Word.
* Đã thêm cơ chế tự động thử lại đối với các lỗi máy chủ.

## Những thay đổi trong phiên bản 1.0

* Phát hành lần đầu.