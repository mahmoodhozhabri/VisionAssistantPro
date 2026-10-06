# Tài liệu hướng dẫn Vision Assistant Pro

<!-- DOWNLOAD_COUNT_START -->Tổng số lượt tải xuống: 75.451<!-- DOWNLOAD_COUNT_END -->

**Vision Assistant Pro** là một trợ lý AI đa phương thức, nâng cao dành cho NVDA. Nó tận dụng các công cụ AI hàng đầu thế giới để cung cấp khả năng đọc màn hình thông minh, dịch thuật, đọc chính tả bằng giọng nói và phân tích tài liệu. Nó tận dụng các công cụ AI đẳng cấp thế giới để cung cấp khả năng đọc, dịch, đọc chính tả bằng giọng nói và phân tích tài liệu thông minh.

_Add-on này được phát hành cho cộng đồng nhằm tôn vinh Ngày Quốc tế Người khuyết tật._

## 1. Thiết lập & Cấu hình

Đi tới **Menu NVDA > Tùy chọn > Cài đặt > Vision Assistant Pro**. Hộp thoại cài đặt được sắp xếp thành 9 tab có thể truy cập: **Kết nối**, **Trợ lý trực tiếp**, **Hành vi AI**, **Ngôn ngữ dịch**, **Trình đọc tài liệu**, **Video**, **CAPTCHA**, **Lời nhắc** và **Nâng cao**.

### 1.1 Cài đặt kết nối

- **Nhà cung cấp:** Chọn dịch vụ AI ưa thích của bạn. Các nhà cung cấp được hỗ trợ bao gồm **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** và **Custom** (các máy chủ tương thích với OpenAI như Ollama, LM Studio, Jan.ai hoặc KoboldCPP).
- **Khóa API:** Nhập một hoặc nhiều khóa API (cách nhau bằng dấu phẩy hoặc dòng mới) để tự động xoay.
- **Tìm nạp mẫu:** Nhấn nút này sau khi nhập khóa API của bạn để tải xuống danh sách mẫu mới nhất hiện có từ nhà cung cấp.
- **Mô hình AI:** Chọn mô hình chính được sử dụng để trò chuyện và phân tích chung.
- **Định tuyến mô hình nâng cao (dành riêng cho nhiệm vụ):** Tùy chọn chọn các mô hình chuyên dụng từ danh sách thả xuống cho các tác vụ OCR, STT, TTS, AI Operator, Video và Trợ lý trực tiếp. Đối với Gemini, các mô hình được phân loại linh hoạt theo khả năng mà không bị lộn xộn.
- **Cài đặt nhà cung cấp tùy chỉnh:** Định cấu hình điểm cuối cục bộ hoặc tùy chỉnh. Bao gồm **Thiết lập AI cục bộ** (thiết lập bằng một cú nhấp chuột cho Ollama, LM Studio, Jan.ai hoặc KoboldCPP) và **Cấu hình điểm cuối nâng cao**.
- **Cấu hình proxy:** Hỗ trợ đầy đủ cho việc chuyển hướng đường hầm và điểm cuối trên toàn bộ tiện ích bổ sung (bao gồm Trợ lý trực tiếp, Trình quan sát xung quanh và TTS). Nhập **URL proxy** của bạn và chọn **Chế độ proxy** của bạn:
  - **Tự động phát hiện:** Tự động phát hiện xem URL là proxy chuyển tiếp hay proxy ngược.
  - **Proxy SOCKS5:** Buộc chuyển tiếp đường hầm qua SOCKS5 với xác thực tên người dùng/mật khẩu RFC 1929 và độ phân giải tên miền.
  - **Proxy HTTP:** Buộc chuyển tiếp đường hầm thông qua proxy HTTP với xác thực Cơ bản.
  - **Proxy ngược:** Thay thế điểm cuối trực tiếp cho các cổng AI tùy chỉnh và máy nhân bản tự lưu trữ (thông tin đăng nhập bị tắt trong chế độ này).
- **Kiểm tra kết nối proxy:** Nút không chặn kiểm tra khả năng kết nối và đo độ trễ của máy chủ tính bằng mili giây (được nói qua NVDA).
- **Tùy chọn kết nối và đầu ra:** Định cấu hình kiểm tra cập nhật khởi động, Đánh dấu sạch trong Trò chuyện, Sao chép phản hồi AI vào bảng nhớ tạm và Đầu ra trực tiếp (Không có cửa sổ trò chuyện).
- **Lưu cuộc trò chuyện vào lịch sử:** Lưu giữ các cuộc trò chuyện của bạn trong danh sách Lịch sử.

### 1.2 Tab Trợ lý trực tiếp

- **Trợ lý trực tiếp: Đầu ra trực tiếp (Không có cửa sổ):** Khởi động Trợ lý trực tiếp mà không có cửa sổ hội thoại; mở nó sau bằng phím Gọi lại kết quả cuối cùng (`Space`).
- **Nhấn để nói:** Chuyển đổi chế độ nhấn để nói. Khi được bật, micrô của bạn chỉ gửi âm thanh khi bạn giữ phím được chỉ định.
- **Phím Nhấn để nói:** Nhấn các phím để ghi phím tắt (ví dụ: `F12` hoặc `Ctrl+F12`) — bạn thậm chí có thể chỉ định một phím bổ trợ duy nhất như `Ctrl trái`. Giữ phím để nói và thả ra để kết thúc; một tiếng bíp ngắn xác nhận mỗi lần nhấn và thả.

Lưu ý: Tab này chỉ xuất hiện khi **Google Gemini** (hoặc nhà cung cấp Tùy chỉnh tương thích với Gemini) là nhà cung cấp đang hoạt động của bạn.

### 1.3 Tab Hành vi AI

- **Sáng tạo (Nhiệt độ):** Kiểm soát tính ngẫu nhiên và khả năng sáng tạo của AI (từ 0,0 đến 2,0). Giá trị thấp hơn tạo ra kết quả dịch/OCR chính xác và xác định hơn.

### 1.4 Tab ngôn ngữ dịch

- **Ngôn ngữ nguồn:** Chọn ngôn ngữ nhập mặc định của bạn.
- **Ngôn ngữ mục tiêu:** Chọn ngôn ngữ dịch mục tiêu chính của bạn.
- **Ngôn ngữ phản hồi AI:** Chọn ngôn ngữ cho phản hồi chung của AI.
- **Hoán đổi thông minh:** Tự động hoán đổi ngôn ngữ nguồn và ngôn ngữ đích dựa trên dữ liệu đầu vào được phát hiện.

### 1.5 Tab Trình đọc tài liệu

- **URL danh sách mô hình (Models List URL):** Endpoint để tải các mô hình hiện có.
- **URL Endpoint OCR/STT/TTS:** URL đầy đủ cho các dịch vụ cụ thể (ví dụ: `http://localhost:11434/v1/audio/speech`).
- **Mô hình tùy chỉnh:** Nhập thủ công tên mô hình (ví dụ: `llama3:8b`) cho từng tác vụ.
- **Xuất số trang:** Chuyển đổi số trang và dấu phân cách ở đầu ra tài liệu nhiều trang.
- **TTS Voice:** Chọn kiểu giọng nói mặc định để tạo âm thanh.
- **Lưu tài liệu vào lịch sử:** Giữ các tài liệu đã mở trong danh sách Lịch sử; văn bản OCR được lưu trong bộ nhớ đệm và dữ liệu sơ yếu lý lịch vẫn được lưu.

### 1.4 Tùy chọn chung

- **Công cụ OCR:** Chọn giữa **Chrome (Fast)** để có kết quả nhanh hoặc **AI (Advanced)** để nhận dạng bố cục vượt trội.
- **Thêm danh sách ký tự:** Tùy chọn thêm từ điển ký tự làm mục phụ đề đầu tiên.
- **Thêm tuyên bố từ chối trách nhiệm AI:** Tùy chọn chèn tuyên bố từ chối trách nhiệm AI vào đầu phụ đề SRT của video.
- **Quản lý bộ truyện & từ điển ký tự:** Thêm, chỉnh sửa, nhập hoặc quản lý tên nhân vật, mô tả ngoại hình và vai trò trên mỗi bộ truyện — AI tự động khớp các ký tự được phát hiện với từ điển của bạn và hợp nhất các ký tự mới khi bạn phân tích nhiều tập hơn. Các ghi chú thủ công của bạn luôn được ưu tiên giữ nguyên so với các bản cập nhật AI, trong khi các mô tả vật lý luôn được cập nhật qua các tập.

### 1.7 Tab CAPTCHA

- **Bật Bộ giải CAPTCHA trực quan:** Chuyển đổi cách giải quyết thách thức trực quan tự động (hCaptcha, reCAPTCHA).
- **Phương pháp CAPTCHA văn bản:** Chọn giữa chụp **Đối tượng điều hướng** hoặc **Toàn màn hình**.

### 1.8 Tab nhắc nhở

- **Quản lý lời nhắc:** Mở hộp thoại chuyên dụng để tùy chỉnh lời nhắc hệ thống mặc định hoặc tạo, chỉnh sửa, sắp xếp lại và xem trước lời nhắc tùy chỉnh do người dùng xác định bằng các biến động (ví dụ: `[selection]`, `[screen_fg_obj]`, `[currentURL]`, `[text]`).
- **Phím tắt lời nhắc tùy chỉnh:** Gán một phím tắt chuyên dụng cho bất kỳ lời nhắc tùy chỉnh nào ngay trong Trình quản lý lời nhắc. Nhấn các phím để ghi lại chúng — các phím đơn chạy bên trong Lớp Lệnh (và trên toàn cầu dưới dạng `NVDA + Shift + key`), trong khi các tổ hợp như `Control + Shift + 1` chạy riêng trên toàn cầu.
- **Hành vi phản hồi theo từng lời nhắc:** Chọn cách mỗi lời nhắc xuất ra kết quả riêng lẻ (Cài đặt chung, Sao chép vào bảng nhớ tạm, Xuất trực tiếp / tin nhắn NVDA, Sao chép vào bảng nhớ tạm + Đầu ra trực tiếp hoặc Cửa sổ trò chuyện).

### 2.1 Phím tắt Trình đọc tài liệu (Bên trong Trình xem)

Điều hướng đến tab **Nâng cao** để định cấu hình ghi nhật ký tiện ích bổ sung toàn cầu:

- **Bật tệp nhật ký chuyên dụng:** Chuyển đổi việc ghi nhật ký tất cả các sự kiện vận hành, lưu lượng API và lỗi trên tất cả các mô-đun tiện ích bổ sung thành một tệp riêng biệt (`vision_assistant.log`).
- **Cấp độ nhật ký:** Chọn mức độ chi tiết giữa **Gỡ lỗi (Tất cả chi tiết)**, **Thông tin (Thông tin chung)**, **Cảnh báo (Chỉ cảnh báo)** và **Lỗi (Chỉ lỗi)**.
- **Giữ nhật ký cho:** Đặt khoảng thời gian lưu giữ tự động để tự động xóa các mục nhật ký cũ hơn (từ 1 giờ đến 90 ngày).
- **Kiểm soát quản lý nhật ký:** Sử dụng **Mở tệp nhật ký**, **Mở thư mục nhật ký** hoặc **Xóa tệp nhật ký** để kiểm tra hoặc xóa dữ liệu nhật ký trực tiếp mà không cần khởi động lại NVDA hoặc can thiệp vào nhật ký NVDA tiêu chuẩn.
- **Thư mục dữ liệu hợp nhất:** Tất cả các tệp dữ liệu bổ trợ (lịch sử, chuỗi, nhãn, tiến trình OCR, bộ nhớ đệm và nhật ký) được lưu trữ trong một thư mục `VisionAssistant` duy nhất bên trong thư mục cấu hình NVDA của bạn — giữ mọi thứ ngăn nắp và thực hiện sao lưu thủ công dễ dàng.

### 1.10 Cài đặt Sao lưu & Khôi phục

Tab **Nâng cao** cũng bao gồm phần **Sao lưu và Khôi phục**:

- **Sao lưu:** Lưu cấu hình của bạn vào một tệp JSON. Khi nhấp vào đó, bạn chọn nội dung cần đưa vào: **Mọi thứ** (cài đặt, nhãn tùy chỉnh, tiến trình OCR và lịch sử) hoặc **Chỉ cài đặt**.
- **Khôi phục:** Tải bản sao lưu đã lưu trước đó để khôi phục cấu hình và dữ liệu của bạn bất kỳ lúc nào, trên bất kỳ máy nào hoặc sau khi cài đặt lại NVDA. Trước tiên, bạn sẽ được yêu cầu xác nhận vì việc khôi phục sẽ thay thế tất cả cài đặt và dữ liệu hiện tại của bạn.

## 2. Trình quản lý khóa API Gemini

Tạo khóa API Gemini trên **aistudio.google.com** từng là bước khó nhất của tiện ích bổ sung. Với trình đọc màn hình, các trang rất khó hiểu và một số người hoàn toàn không thể tạo khóa. **Trình quản lý khóa API Gemini** giải quyết vấn đề đó. Nhấn **G** trong Lớp lệnh, hoặc mở **Menu NVDA > Tùy chọn > Cài đặt > Trợ lý thị giác > Kết nối** và nhấn **Nhận khóa API Gemini...**.

- **Đăng nhập:** Khi bạn mở trình quản lý, trình duyệt mặc định của bạn sẽ mở trực tiếp bằng trang đăng nhập an toàn của Google. Đăng nhập bằng tài khoản Google của bạn — không yêu cầu công cụ bên ngoài, SDK hoặc thiết lập dòng lệnh. Tài khoản bạn đăng nhập luôn được hiển thị trên nút **Đăng xuất**.
- **Tạo khóa:** Sau khi đăng nhập, bạn có thể tạo khóa ngay lập tức bằng **Dự án mới và Khóa** mà không cần thiết lập trước. Nếu bạn đã có dự án hiện có, chúng sẽ xuất hiện trong một danh sách đơn giản nơi bạn có thể chọn một dự án và nhấn **Tạo khóa cho dự án đã chọn**.
- **Điều gì xảy ra tiếp theo:** Khóa mới được sao chép ngay vào bảng nhớ tạm, được lưu bên trong tiện ích bổ sung để sử dụng sau này và bạn sẽ được hỏi một lần xem có thêm khóa đó vào danh sách khóa của tiện ích bổ sung hay không. Đó là tất cả những gì bạn cần — không cần phải tìm kiếm trang web nào cả.
- **Làm việc với các khóa của bạn:** **Sao chép khóa cho dự án đã chọn** sao chép khóa của dự án bạn đã chọn, **Sao chép khóa được tạo lần cuối** sao chép khóa bạn đã tạo cách đây một lúc và **Xuất khóa đã lưu sang CSV...** lưu mọi thứ bạn đã tạo vào một tệp.
- **Xóa khóa:** **Xóa khóa...** hiển thị các khóa tồn tại trên dự án đã chọn, hỏi bạn cần xóa khóa nào và xác nhận trước khi xóa. Việc xóa một khóa cũng sẽ xóa khóa đó khỏi danh sách khóa của tiện ích bổ sung, do đó không còn phím nào bị hỏng trong quá trình xoay. Các khóa được tạo bên ngoài tiện ích bổ sung cũng có thể bị xóa, miễn là tài khoản của bạn có quyền đối với dự án đó.
- **Đăng xuất:** **Đăng xuất** xóa thông tin đăng nhập được lưu trữ khỏi máy tính của bạn, do đó bạn có thể chuyển sang tài khoản khác bất cứ khi nào bạn muốn.

## 3. Lớp lệnh & Phím tắt

- Chuẩn hóa tất cả các phím tắt để sử dụng NVDA+Control+Shift nhằm loại bỏ xung đột với bố cục Bàn phím Laptop của NVDA và các phím nóng hệ thống.

1. 1. Nhấn **NVDA + Shift + V** (Phím chính) để kích hoạt lớp lệnh (bạn sẽ nghe thấy tiếng bíp).
2. Nhả phím, sau đó nhấn một trong các phím đơn sau:

| Phím                                                                            | Chức năng                                                                                                                       | Mô tả                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shift + A**                                                                   | AI Operator                                                                                                                     | **Điều khiển tự động:** Yêu cầu AI thực hiện một tác vụ trực tiếp trên màn hình của bạn. Nhấn lại lần nữa sẽ hủy bỏ ngay lập tức các hoạt động đang hoạt động.                                      |
| **E**                                                                           | **UI Explorer**                                                                                                                 | **E**                                                                                                                                                                                                                                               |
| UI Explorer                                                                     | **Click tương tác:** Nhận diện và click vào các thành phần giao diện trong bất kỳ ứng dụng nào. | **T**                                                                                                                                                                                                                                               |
| Dịch thông minh                                                                 | Dịch văn bản dưới con trỏ navigator hoặc vùng đang chọn.                                                        | **Shift + T**                                                                                                                                                                                                                                       |
| Dịch Clipboard                                                                  | Dịch nội dung hiện có trong clipboard.                                                                          | **R**                                                                                                                                                                                                                                               |
| Tinh chỉnh văn bản                                                              | Tóm tắt, Sửa ngữ pháp, Giải thích hoặc chạy các **Prompt tùy chỉnh**.                                           | **V**                                                                                                                                                                                                                                               |
| Thị giác đối tượng                                                              | Mô tả đối tượng navigator hiện tại.                                                                             | **O**                                                                                                                                                                                                                                               |
| Thị giác toàn màn hình                                                          | Phân tích toàn bộ bố cục và nội dung màn hình.                                                                  | **Shift + V**                                                                                                                                                                                                                                       |
| Phân tích Video trực tuyến                                                      | Phân tích video trên **YouTube**, **Instagram**, **TikTok**, hoặc **Twitter (X)**.           | Ghi lại một video im lặng về màn hình của bạn và phân tích các hành động cũng như bố cục.                                                                                                                                           |
| **D**                                                                           | Trình đọc tài liệu                                                                                                              | **D**                                                                                                                                                                                                                                               |
| Trình đọc tài liệu                                                              | Trình đọc nâng cao cho PDF và hình ảnh với tùy chọn chọn phạm vi trang.                                         | **F**                                                                                                                                                                                                                                               |
| Hành động tệp thông minh                                                        | Nhận diện theo ngữ cảnh từ các tệp hình ảnh, PDF hoặc TIFF được chọn.                                           | Phiên âm hoặc lồng tiếng các tệp âm thanh/video (MP3, WAV, MP4, v.v.) sang ngôn ngữ mục tiêu của bạn.                                                                            |
| **C**                                                                           | **C**                                                                                                                           | Giải CAPTCHA                                                                                                                                                                                                                                        |
| Chụp và giải mã CAPTCHA trên màn hình hoặc đối tượng navigator. | Trò chuyện trực tiếp                                                                                                            | Mở giao diện trò chuyện dựa trên văn bản trực tiếp với AI.                                                                                                                                                                          |
| **S**                                                                           | **S**                                                                                                                           | Đọc chính tả thông minh Chuyển đổi giọng nói thành văn bản. Nhấn để bắt đầu ghi âm, nhấn lần nữa để dừng/gõ văn bản.                                                                                                |
| **Điều khiển+T**                                                                | Dịch giọng nói                                                                                                                  | Phiên âm, dịch và nhập kết quả dựa trên cài đặt ngôn ngữ của bạn.                                                                                                                                                                   |
| **Điều khiển+L**                                                                | **Trợ lý trực tiếp**                                                                                                            | **Phi công phụ thời gian thực (chỉ dành cho Gemini):** Bắt đầu hoặc kết thúc cuộc trò chuyện trực tiếp trên màn hình và giọng nói với trợ lý AI.                                                 |
| **Điều khiển+A**                                                                | **Người điều hành trực tiếp**                                                                                                   | **Điều khiển máy tính tự động (chỉ Gemini):** Bắt đầu hoặc kết thúc phiên thoại trực tiếp trong đó người vận hành thực hiện các yêu cầu của bạn trên máy tính.                                   |
| **G**                                                                           | **Trình quản lý khóa API Gemini**                                                                                               | **Tạo khóa API của bạn mà không cần web (chỉ Gemini):** Mở trình quản lý thiết lập những gì máy tính của bạn cần, mở trình duyệt để đăng nhập và tạo, sao chép hoặc xóa khóa cho dự án bạn chọn. |
| **TÔI**                                                                         | Báo cáo trạng thái                                                                                                              | Thông báo tiến trình hiện tại (ví dụ: "Đang quét...", "Không hoạt động").                                                                        |
| **L**                                                                           | Thông báo trạng thái                                                                                                            | Thông báo tiến trình hiện tại (ví dụ: "Đang quét...", "Nhàn rỗi").                                                                               |
| **Shift + L**                                                                   | **Quản lý/Quét nhãn**                                                                                                           | Mở Trình quản lý nhãn (nếu nhãn tồn tại) hoặc quét ứng dụng để tìm các phần tử chưa được đặt tên.                                                                                                                |
| **U**                                                                           | Kiểm tra cập nhật                                                                                                               | Kiểm tra thủ công GitHub để biết phiên bản mới nhất của tiện ích bổ sung.                                                                                                                                                           |
| **U**                                                                           | Kiểm tra cập nhật                                                                                                               | Kiểm tra thủ công trên GitHub để tìm phiên bản mới nhất của add-on.                                                                                                                                                                 |
| **Space**                                                                       | Gọi lại kết quả cuối                                                                                                            | Hiển thị phản hồi cuối cùng của AI trong hộp thoại trò chuyện để xem lại hoặc hỏi tiếp.                                                                                                                                             |
| **H**                                                                           | Trợ giúp lệnh                                                                                                                   | Hiển thị danh sách tất cả các phím tắt có sẵn trong lớp lệnh.                                                                                                                                                                       |
| **Alt + S**                                                                     | Cài đặt                                                                                                                         | Mở hộp thoại cài đặt Vision Assistant Pro.                                                                                                                                                                                          |
| **Alt + Q**                                                                     | Báo cáo số khóa đã hết hạn ngạch                                                                                                | Báo cáo số lượng khóa API Gemini đã vượt quá hạn mức hàng ngày và thời gian đặt lại của chúng.                                                                                                                                      |
| **Alt + M**                                                                     | Kiểm tra định tuyến                                                                                                             | Báo cáo các mô hình AI hiện được chọn trong định tuyến nâng cao.                                                                                                                                                                    |
| **Lên / Xuống**                                                                 | Điều hướng cài đặt nhanh                                                                                                        | Điều hướng giữa các danh mục cài đặt nhanh (Nhà cung cấp, Kiểu máy, v.v.) trong lớp.                                                                                             |
| **Trái / Phải**                                                                 | Thay đổi cài đặt nhanh                                                                                                          | Thay đổi giá trị của cài đặt nhanh hiện được chọn.                                                                                                                                                                                  |

## 4. Trò chuyện & Lịch sử

_Nếu bạn muốn ủng hộ dự án về mặt tài chính và muốn thấy tên mình ở đây, bạn có thể tìm thấy tùy chọn **Quyên góp** trong menu Công cụ của NVDA (menu con Vision Assistant) hoặc trong quá trình thiết lập sau khi cài đặt._

### 3.1 Phím tắt cửa sổ trò chuyện

Khi cửa sổ trò chuyện mở (Trò chuyện trực tiếp, trò chuyện tài liệu, tinh chỉnh, v.v.), bạn có thể xem lại cuộc trò chuyện bằng:

- **Bổ sung Công cụ OCR "None (Lớp trích xuất văn bản)"**: Người dùng hiện có thể trích xuất văn bản trực tiếp từ các tệp PDF có thể tìm kiếm mà không cần sử dụng hạn ngạch AI, giúp cải thiện đáng kể tốc độ và tính riêng tư cho các tài liệu dạng văn bản.
- **Tinh chỉnh độ chính xác của UI Explorer**: Cải thiện prompt của UI Explorer để nhận diện tốt hơn các loại thành phần (như List Item) và báo cáo chính xác các trạng thái như "(Checked)", "(Selected)", hoặc "(Expanded)" trong khi bỏ qua các thành phần hệ thống của Windows như Thanh tác vụ và Đồng hồ.
- **Nhắc nhở thiết lập cài đặt**: Thêm một thông báo sau khi cài đặt để hướng dẫn người dùng đến menu cài đặt nhằm cấu hình khóa API và các tùy chọn cá nhân của họ.

### Những thay đổi trong phiên bản 5.5.2

Nhấn **Control + H** trong Lớp Lệnh để mở hộp thoại **Lịch sử** với các cuộc trò chuyện và tài liệu trước đây của bạn, có thể lọc theo loại (Tất cả / Trò chuyện / Tài liệu). Mở cuộc trò chuyện để tiếp tục cuộc trò chuyện — bao gồm các tệp đính kèm, được đính kèm lại tự động — hoặc mở tài liệu và tiếp tục đọc. Nhấn **Xóa** trên bất kỳ mục nào để xóa mục đó hoặc **Xóa tất cả** để làm trống danh sách. Đối với tài liệu, Xóa sẽ hỏi xem bạn chỉ muốn xóa mục nhập lịch sử hay xóa văn bản OCR được lưu trong bộ nhớ đệm của tài liệu đó để lần mở tiếp theo sẽ quét lại từ đầu — với tùy chọn **Không hỏi lại** để ghi nhớ lựa chọn của bạn.

Bạn cũng có thể chọn những gì danh sách ghi nhớ. **Lưu cuộc trò chuyện vào lịch sử** (tab Kết nối) và **Lưu tài liệu vào lịch sử** (tab Trình đọc tài liệu) đều được bật theo mặc định và cả hai đều có thể được bật trong Cài đặt nhanh. Tùy chọn tài liệu chỉ ảnh hưởng đến mục nhập Lịch sử - văn bản OCR được lưu trong bộ nhớ đệm và dữ liệu sơ yếu lý lịch luôn được lưu giữ.

## 5. AI Operator - Điều khiển máy tính tự động

**Người vận hành AI** biến Vision Assistant Pro từ một trình đọc thụ động thành một trợ lý tích cực có thể thay mặt bạn tương tác với máy tính. Bạn có thể yêu cầu nó mô tả màn hình, trả lời các câu hỏi về những gì nó nhìn thấy hoặc thậm chí kiểm soát—nhấp vào nút, kéo các mục, nhập văn bản và điều hướng qua các ứng dụng bằng các lệnh ngôn ngữ tự nhiên.

Ưu điểm lớn nhất? Nó hoạt động hoàn hảo trong phần mềm hoàn toàn không thể truy cập được. Nếu bạn bị mắc kẹt trong một ứng dụng tùy chỉnh, một máy tính để bàn từ xa hoặc một trang web mà trình đọc màn hình của bạn hoàn toàn im lặng thì nhà điều hành sẽ không bận tâm. Vì nó "nhìn" màn hình một cách trực quan nên nó có thể tìm, đọc và tương tác với các phần tử không có nhãn trợ năng.

### Những thay đổi trong phiên bản 4.6

1. **Gọi lại kết quả tương tác:** Đã thêm phím **Space** vào lớp lệnh, cho phép người dùng mở lại ngay lập tức phản hồi cuối cùng của AI trong cửa sổ trò chuyện để đặt câu hỏi tiếp theo, ngay cả khi chế độ "Đầu ra trực tiếp" đang hoạt động.
2. **Cộng đồng Telegram:** Đã thêm liên kết "Kênh Telegram chính thức" vào menu Công cụ của NVDA, cung cấp một cách nhanh chóng để cập nhật những tin tức, tính năng và bản phát hành mới nhất.
3. AI sẽ phân tích màn hình của bạn, xác định các yếu tố liên quan và thực hiện hành động hoặc đưa ra câu trả lời. Nếu một tác vụ yêu cầu nhiều bước, người vận hành sẽ tiếp tục làm việc cho đến khi hoàn thành.
4. **Cải thiện hướng dẫn giao diện:** Đã cập nhật các mô tả cài đặt và tài liệu hướng dẫn để giải thích rõ hơn về hệ thống gọi lại mới và cách thức hoạt động của nó cùng với các cài đặt đầu ra trực tiếp.

### Những thay đổi trong phiên bản 4.5

Người vận hành hiểu được nhiều loại lệnh:

- **Mô tả & Trả lời**: "Mô tả bố cục màn hình" hoặc "Thông báo lỗi nói gì?"
- **Nhấp vào**: "Nhấp vào nút Lưu"
- **Nhấp chuột phải**: "Nhấp chuột phải vào tập tin"
- **Nhấp đúp**: "Nhấp đúp vào tài liệu"
- **Kéo & Thả**: "Kéo tài liệu vào thư mục Lưu trữ"
- **Type**: "Gõ 'Hello World' vào hộp tìm kiếm"
- **Cuộn**: "Cuộn xuống ba lần"
- **Nhấn phím**: "Nhấn Enter", "Nhấn Tab", "Nhấn Escape"
- **Nhiệm vụ nhiều bước**: "Mở File Explorer, tìm báo cáo và đổi tên thành Final.pdf"

### 4.3 Lưu ý quan trọng

- **⚠️ Cảnh báo sử dụng API**: Vì người vận hành cần "xem" chính xác những gì đang diễn ra trên màn hình nên sẽ gửi ảnh chụp màn hình có độ phân giải cao theo từng bước. Việc sử dụng thường xuyên sẽ tiêu tốn hạn ngạch API của bạn nhanh hơn nhiều so với các tính năng dựa trên văn bản tiêu chuẩn.
- **Ứng dụng dành cho quản trị viên**: Nếu NVDA không chạy với đặc quyền của Quản trị viên, người vận hành có thể không tương tác được với các cửa sổ yêu cầu quyền nâng cao. Đây là giới hạn bảo mật của Windows, không phải lỗi trong tiện ích bổ sung.
- **Các phương pháp hay nhất**: Để có kết quả tốt nhất, hãy đưa ra các mệnh lệnh rõ ràng và cụ thể. "Nhấp vào nút Gửi màu xanh lam ở cuối biểu mẫu" hầu như luôn hoạt động tốt hơn là chỉ "Nhấp vào nút".

### 4.4 Người vận hành trực tiếp (Control+A)

Người vận hành trực tiếp cho phép Trợ lý trực tiếp thực hiện những gì bạn yêu cầu trên máy tính trong khi bạn nói chuyện với nó, bao gồm cả những ứng dụng mà trình đọc màn hình của bạn không thể đọc được.
_(Lưu ý: Tính năng này chỉ dành riêng cho các nhà cung cấp Tùy chỉnh tương thích với Google Gemini và Gemini)._

- **Hệ thống trợ giúp:** Đã thêm lệnh trợ giúp (`H`) trong Lớp lệnh để cung cấp một danh sách dễ truy cập gồm tất cả các phím tắt và chức năng của chúng.
- **Cách hoạt động:** Hỏi bằng ngôn ngữ đơn giản, ví dụ: "mở Chrome và tìm kiếm trang web" hoặc "đổi tên tệp này thành cuối cùng". Người vận hành nhìn vào màn hình, thực hiện từng bước một và tiếp tục thực hiện các yêu cầu gồm nhiều bước cho đến khi hoàn thành nhiệm vụ.
- **Đóng góp cho dự án:** Đã thêm hộp thoại quyên góp tùy chọn cho những người dùng muốn ủng hộ các bản cập nhật trong tương lai và sự phát triển liên tục của dự án.
- **CAPTCHA:** Nếu CAPTCHA xuất hiện, trước tiên, người vận hành sẽ thử **bộ giải CAPTCHA** tích hợp sẵn của bạn; nếu không thể giải quyết được, nó sẽ yêu cầu bạn tự mình hoàn thành thử thách có thể tiếp cận được.
- **Đang dừng:** Nhấn **Dừng hành động của người vận hành** trong cửa sổ Trợ lý trực tiếp để hủy tác vụ hiện tại.
- **Cài đặt:** Có thể chỉnh sửa hướng dẫn riêng của người vận hành trong Trình quản lý lời nhắc (phần **Trực tiếp**, **Hướng dẫn người vận hành trực tiếp**). Công tắc **Đầu ra trực tiếp trực tiếp (Không có cửa sổ)** cũng có sẵn trong Cài đặt nhanh.

## 6. Phân tích video & Mô tả âm thanh

> **Lưu ý:** Các tính năng Phân tích video và Mô tả âm thanh được cung cấp hoàn toàn bởi nhà cung cấp **Google Gemini**. Đảm bảo rằng nhà cung cấp đang hoạt động của bạn trong cài đặt tiện ích bổ sung được đặt thành Google Gemini.

Vision Assistant Pro giới thiệu khả năng xử lý video mạnh mẽ được thiết kế dành riêng cho người dùng khiếm thị. Nó có thể phân tích cả video trực tuyến và bản ghi màn hình cục bộ để cung cấp mô tả trực quan rất chi tiết và tạo tập lệnh Mô tả âm thanh (SRT) chuyên nghiệp.

### 5.1 Ghi màn hình cục bộ (Control + V)

Nếu bạn gặp một video im lặng, hoạt ảnh hoặc hướng dẫn trên màn hình, bạn có thể quay trực tiếp:

1. **Ngôn ngữ mới:** Đã thêm bản dịch tiếng **Ba Tư** và tiếng **Việt**.
2. Tiện ích bổ sung sẽ âm thầm ghi lại màn hình của bạn ở chế độ nền.
3. Nhấn **Control + V** lần nữa để dừng ghi.
4. **Xử lý tệp:** Đã sửa lỗi tải lên các tệp có tên không phải tiếng Anh bị thất bại.

### Những thay đổi trong phiên bản 2.9

Bạn có thể phân tích cả tệp video cục bộ và video trực tuyến. Chỉ cần chọn tệp video cục bộ trong Windows Explorer hoặc sao chép liên kết video trực tuyến vào bộ nhớ tạm của bạn. Bạn cũng có thể nhấn **Shift + V** ở bất kỳ đâu (như bên trong trình phát đa phương tiện) để mở hộp thoại trong đó bạn có thể duyệt tìm tệp video hoặc dán URL theo cách thủ công.

- **Nền tảng trực tuyến được hỗ trợ:** YouTube, Instagram, TikTok và Twitter (X).
- AI sẽ tự động phát hiện tệp cục bộ hoặc URL, xử lý video và cung cấp mô tả trực quan và tóm tắt âm thanh toàn diện.
- **Bộ nhớ đệm tệp video trong 48 giờ:** Các video tải lên Gemini được lưu trong bộ nhớ đệm trong 48 giờ! Bạn có thể tạo lại đầu ra SRT hoặc MP3 cho cùng một video mà không cần tải lên lại — ngay cả sau khi khởi động lại NVDA. Bộ nhớ đệm nhận biết khóa và tự động vô hiệu hóa khi khóa API của bạn thay đổi.

### 5.3 Tạo mô tả âm thanh (SRT)

Để có trải nghiệm có cấu trúc hơn, tiện ích bổ sung có thể tạo tập lệnh Mô tả âm thanh chuyên nghiệp ở định dạng SubRip (SRT) tiêu chuẩn.

- Chuyển đổi cấu trúc dự án sang Mẫu Add-on chính thức của NV Access để tuân thủ các tiêu chuẩn tốt hơn.
- **Theo dõi ký tự:** Công cụ thực hiện bước chuyển trước để trích xuất các ký tự riêng biệt dựa trên các đặc điểm khuôn mặt không thể thay đổi. Nó xây dựng một từ điển toàn cầu để theo dõi và gắn nhãn chính xác cho các ký tự trên các cảnh khác nhau mà không gây nhầm lẫn. Nó cũng theo dõi **lần xuất hiện đầu tiên** của mỗi nhân vật, mô tả ngoại hình của họ chỉ một lần — tại thời điểm họ xuất hiện lần đầu — và chỉ sử dụng tên đã đặt trong các cảnh sau để giữ cho câu chuyện luôn mới mẻ và tự nhiên.
- Tối ưu hóa các prompt dịch thuật để có độ chính xác cao hơn và xử lý logic "Smart Swap" tốt hơn.
- **Cách sử dụng:** Để nghe phụ đề được tạo, chỉ cần đặt tệp `.srt` vào cùng thư mục với tệp video của bạn và đặt tên giống hệt như vậy. Sau đó, định cấu hình trình phát đa phương tiện của bạn (ví dụ: VLC hoặc PotPlayer) để định tuyến văn bản phụ đề trực tiếp đến trình đọc màn hình hoặc công cụ TTS trong khi phát lại.
- **Trải nghiệm lưu được cải thiện:** Khi lưu tệp SRT hoặc MP3, hộp thoại tệp hiện sẽ mở trong thư mục của video nguồn theo mặc định, cho dù bạn đã mở video qua hộp thoại tệp hay Shift+V từ Explorer.

### Những thay đổi trong phiên bản 2.6

Ngoài việc tạo các tệp SRT dựa trên văn bản, tiện ích bổ sung này còn hoạt động như một công cụ sản xuất Mô tả âm thanh hoàn chỉnh bằng cách tổng hợp các mô tả thành giọng nói và trộn chúng với video. Giờ đây, bạn có thể chọn **Gemini Live TTS** làm công cụ giọng nói, sử dụng API Gemini Live để tạo tường thuật bằng giọng nói không giới hạn, có độ chân thực cao. Khi tạo MP3 cho các tệp video cục bộ, bạn có nhiều chế độ trộn:

- **AD tiêu chuẩn (Giọng trộn):** Lời tường thuật được phủ trực tiếp lên trên âm thanh của video. Bạn sẽ được nhắc có muốn áp dụng **Giảm âm thanh** (giảm âm lượng nền trong khi mô tả) để đảm bảo lời tường thuật rõ ràng hay không.
- **Quảng cáo mở rộng (Tạm dừng âm thanh):** Công cụ tạm dừng âm thanh video gốc trong khi mô tả, đảm bảo bạn không bao giờ bỏ lỡ một từ nào trong đoạn hội thoại gốc hoặc lời tường thuật của AI. Tính năng phát hiện im lặng hiện sử dụng mô hình thần kinh **Silero VAD** (được tải xuống tự động trong lần sử dụng đầu tiên, giống như ffmpeg và eSpeak) để xác định thời gian ngắt quãng chính xác — phân biệt các khoảng dừng đối thoại tự nhiên với âm nhạc và tiếng ồn xung quanh.
- **Video YouTube:** Đối với các nguồn YouTube (không được tải xuống cục bộ), bản xuất MP3 sẽ chỉ chứa đoạn giọng nói AI được đồng bộ hóa mà không có âm thanh video nền.

## 7. Phiên âm và lồng tiếng phương tiện (M)

Bộ chuyển đổi âm thanh đã được xây dựng lại hoàn toàn để hỗ trợ cả tệp âm thanh và video (MP3, WAV, MP4, MKV, v.v.). Nhấn **M** trong Lớp lệnh để chọn tệp phương tiện và chọn một trong 3 chế độ hoạt động riêng biệt:

1. Đã sửa sự cố trong đó biến `[file_ocr]` không hoạt động bình thường trong Custom Prompts.
2. **Phiên âm và dịch (Ngôn ngữ đích)**: Phiên âm lời nói và dịch nó sang ngôn ngữ đích được định cấu hình của bạn.
3. **Lồng tiếng và dịch (Ngôn ngữ đích)** _(Chỉ Gemini)_: Một tính năng mới mạnh mẽ giúp phiên âm lời nói, dịch sang ngôn ngữ đích của bạn và tổng hợp bản lồng tiếng bằng giọng nói bằng công cụ TTS của tiện ích bổ sung.

## 8) Trình đọc tài liệu và hình ảnh nâng cao

**Trình đọc tài liệu** biến tài liệu của bạn thành văn bản rõ ràng, dễ đọc — để bạn có thể đọc, dịch và nghe bất kỳ nội dung nào từ sách được quét đến chồng ảnh. Nó xử lý các tệp PDF nhiều trang, hình ảnh phức tạp, định dạng iPhone HEIC và thậm chí cả các tệp văn bản thuần túy (`.txt`) và HTML (`.html`, `.htm`), được mở ngay lập tức mà không cần xử lý OCR hoặc AI. Chọn nhiều tệp cùng một lúc và chúng được hợp nhất thành một tài liệu liên tục theo thứ tự trang. Hiện có ba công cụ OCR — **Chrome (Nhanh)**, **AI (Nâng cao)** để bảo toàn bố cục ưu việt và **Không (Lớp văn bản trích xuất)** cho các tệp PDF có thể tìm kiếm — được chọn trong Cài đặt → Trình đọc tài liệu.

### Những thay đổi trong phiên bản 2.0

1. Đã triển khai hệ thống Tự động cập nhật tích hợp sẵn.
2. Chọn một hoặc nhiều tệp PDF hoặc hình ảnh. Tiện ích bổ sung sẽ quét chúng và thông báo tổng số trang.
3. Trong hộp thoại **Tùy chọn**, chọn phạm vi trang (Từ/Đến). Bạn cũng có thể chọn **Dịch đầu ra** và chọn ngôn ngữ đích, chuyển đổi **Mô tả hình ảnh nội tuyến trong khi OCR** ​​hoặc chuyển đổi **Nén các trang PDF trước khi xử lý** để thu nhỏ và nén lại các trang được quét quá khổ trước khi tải lên.
4. Quá trình trích xuất văn bản bắt đầu ở chế độ nền theo đợt. Bạn có thể đóng cửa sổ bất kỳ lúc nào và tiếp tục sau - không có gì bị mất.
5. Tối ưu hóa các prompt AI để thực thi nghiêm ngặt đầu ra ngôn ngữ đích.

### Những thay đổi trong phiên bản 1.5

Bạn không cần phải đọc một tài liệu lớn cùng một lúc. Chọn một phạm vi trang (ví dụ: `1-20`) hoặc giữ mặc định để xử lý mọi thứ và AI sẽ trích xuất tất cả các trang ở chế độ nền. Nếu NVDA gặp sự cố hoặc bạn làm gián đoạn quá trình quét, tiện ích bổ sung này sẽ ghi nhớ tiến trình của bạn và đề xuất **Tiếp tục** chính xác ở nơi nó dừng lại — ngay cả khi khởi động lại. Các tài liệu đã hoàn thành cũng được lưu vào bộ nhớ đệm nên việc mở lại chúng (từ Tài liệu gần đây hoặc qua **D**) sẽ tải văn bản ngay lập tức mà không cần chạy lại OCR, trừ khi tệp nguồn đã thay đổi.

### Những thay đổi trong phiên bản 1.0

Không phải lúc nào bạn cũng cần mở tài liệu trước. Trong Windows File Explorer, chỉ cần đánh dấu tệp PDF, hình ảnh hoặc văn bản/HTML và nhấn **D** (Trình đọc tài liệu) — hoặc đánh dấu tệp PDF hoặc hình ảnh và nhấn **F** (Hành động tệp thông minh) — bên trong Lớp lệnh. Tiện ích bổ sung ngay lập tức bỏ qua hộp thoại tệp và bắt đầu xử lý tệp được đánh dấu. Việc chọn nhiều tệp cùng lúc sẽ xử lý chúng cùng nhau dưới dạng một tài liệu.

### 7.3 Phím tắt & Điều khiển Trình xem Tài liệu

Khi cửa sổ Trình đọc tài liệu mở, bạn có thể sử dụng các thao tác sau:

#### Phím tắt

- **Ctrl + PageDown:** Chuyển đến trang tiếp theo.
- **Ctrl + PageUp:** Chuyển đến trang trước đó.
- **Alt + A:** Mở hộp thoại trò chuyện để đặt câu hỏi về tài liệu.
- **Alt + R:** Buộc **Quét lại bằng AI** bằng nhà cung cấp hiện tại của bạn.
- **Alt + G:** Tạo và lưu tệp âm thanh chất lượng cao (WAV/MP3). _Ẩn nếu nhà cung cấp không hỗ trợ TTS._ **Alt + S / Ctrl + S:** Lưu văn bản được trích xuất dưới dạng tệp TXT hoặc HTML.
- **Alt + S / Ctrl + S:** Lưu văn bản được trích xuất dưới dạng tệp TXT hoặc HTML.

#### Nút & Điều khiển

- **Truy cập:** Chọn bất kỳ trang nào từ bộ chọn trang.
- **Xem được định dạng:** Xem toàn bộ tài liệu được kết hợp dưới dạng văn bản được định dạng.
- **Thử lại các trang bị lỗi:** Chỉ thử lại những lô không thành công do lỗi máy chủ tạm thời (ví dụ: nhu cầu cao). Nút này tự động xuất hiện khi cần thiết.
- **TTS Voice / TTS Engine:** Chọn giọng nói và trên Gemini, chọn giữa phát trực tuyến **TTS tiêu chuẩn** và **Gemini Live**.
- **Trước / Tiếp theo:** Di chuyển giữa các trang (giống như phím tắt Ctrl+PageUp/Down).

### 7.4 Tài liệu gần đây (D)

Nhấn **D** trong Lớp lệnh sẽ liệt kê các tài liệu đã đọc gần đây của bạn trước tiên. Chọn một tệp để tiếp tục từ trang bạn đang truy cập — ngay cả khi OCR đã hoàn tất — hoặc nhấn **Mở tệp...** (`Ctrl + O`) để duyệt tệp như bình thường.

## 9. Ghi nhãn ngữ nghĩa AI & Trình khám phá giao diện người dùng

Bạn bị mắc kẹt trong một ứng dụng có "nút không được gắn nhãn" ở mọi nơi? Công cụ Ghi nhãn ngữ nghĩa AI sẽ giải quyết vấn đề này vĩnh viễn.

### 8.1 Ghi nhãn vật thể vĩnh viễn (L)

Tập trung trình đọc màn hình của bạn vào đồ họa hoặc nút không được gắn nhãn và nhấn **L** trong Lớp Lệnh. AI sẽ nhìn vào nút một cách trực quan, xác định chức năng của nó và dán nhãn vĩnh viễn.
_Không giống như các công cụ ghi nhãn của trình đọc màn hình cũ hơn, tiện ích bổ sung này sử dụng hệ thống "Chữ ký đối tượng" kết hợp nâng cao (AutomationId/ControlID). Nhãn tùy chỉnh của bạn sẽ vẫn tồn tại khi thay đổi kích thước cửa sổ, chuyển đổi màn hình và cập nhật ứng dụng!_

### 8.2 Quét toàn bộ ứng dụng (Shift + L)

Nhấn **Shift + L** để quét toàn bộ cửa sổ đang hoạt động cùng một lúc. AI sẽ tìm tất cả các phần tử chưa được gắn nhãn và đặt tên cho chúng một cách thông minh chỉ trong một lần. Sau này, bạn có thể quản lý, đổi tên hoặc xóa hàng loạt các nhãn này khỏi Trình quản lý nhãn tích hợp sẵn.

### Trình khám phá giao diện người dùng 8.3 (E)

Bạn cần tương tác với một phần tử mà không cần điều hướng đến phần tử đó theo cách thủ công? Nhấn **E** để kích hoạt UI Explorer. AI sẽ quét màn hình và tạo danh sách có thể truy cập được của mọi thành phần có thể nhấp vào (bỏ qua tiếng ồn của hệ thống như thanh tác vụ). Chọn một mục từ danh sách và tiện ích bổ sung sẽ ngay lập tức nhấp vào mục đó cho bạn.

## 10. Trợ lý giọng nói trực tiếp

Trợ lý trực tiếp biến Vision Assistant Pro thành một phi công phụ tương tác theo thời gian thực.
_(Lưu ý: Tính năng này chỉ dành riêng cho các nhà cung cấp Tùy chỉnh tương thích với Google Gemini và Gemini)._

- **Kích hoạt:** Nhấn **Control + L** trong Lớp lệnh để mở hộp thoại Trợ lý trực tiếp.
- **Tương tác theo thời gian thực:** Nói chuyện tự nhiên qua micrô của bạn. AI sẽ đồng thời lắng nghe giọng nói của bạn và nhìn vào màn hình đang hoạt động của bạn. Bạn có thể đặt những câu hỏi như "Tôi đang nhìn gì?" hoặc "Đọc đoạn thứ ba cho tôi nghe."
- **Nhấn để nói:** Bật **Nhấn để nói** trong tab cài đặt Trợ lý trực tiếp (hoặc chuyển đổi nút này ngay trong cửa sổ Trợ lý trực tiếp), sau đó giữ phím được chỉ định của bạn để nói và nhả phím để hoàn tất. Điều này giúp tắt tiếng micrô cho đến khi bạn nhấn phím — hoàn hảo trong môi trường ồn ào.
- **Đầu vào webcam:** Đánh dấu vào **Sử dụng &Webcam** trong cửa sổ Trợ lý trực tiếp để gửi nguồn cấp dữ liệu camera của bạn tới AI thay vì màn hình — hỏi về các vật thể thực, tài liệu được in hoặc môi trường xung quanh bạn. Nếu ffmpeg chưa được cài đặt, hãy đánh dấu vào ô tải xuống một lần với sự cho phép của bạn; tùy chọn này bị tắt khi không phát hiện thấy camera hoặc cài đặt quyền riêng tư của Windows chặn quyền truy cập vào camera.
- **Tùy chỉnh:** Bên trong hộp thoại, bạn có thể thay đổi Kiểu giọng nói của AI (ví dụ: Chuyên nghiệp, Thân thiện, Lạc quan) và điều chỉnh "Độ sâu tư duy" của nó để kiểm soát mức độ suy luận sâu sắc của nó trước khi trả lời.

## 11. Người quan sát xung quanh (Trợ lý nền)

Quan sát môi trường biến Vision Assistant Pro thành đôi mắt nền của bạn mà không có bất kỳ cuộc trò chuyện nào: nó tiếp tục lắng nghe và quan sát trong khi bạn làm việc, báo cáo những thay đổi và giữ im lặng khi không có gì xảy ra.
_(Lưu ý: Tính năng này chỉ dành riêng cho các nhà cung cấp Tùy chỉnh tương thích với Google Gemini và Gemini)._

- **Kích hoạt:** Nhấn **Shift+O** trong Lớp Lệnh để mở hộp thoại Quan sát môi trường; nhấn nó một lần nữa để dừng người quan sát.
- **Chế độ:** **Chỉ dịch âm thanh** dịch những gì nghe được, **Chỉ người xem màn hình** báo cáo các thay đổi trên màn hình và **Chỉ người xem webcam** mở cửa sổ Trợ lý trực tiếp bằng máy ảnh của bạn và Nhấn để nói (Push to Talk) để bạn có thể đặt câu hỏi về những gì máy ảnh nhìn thấy.
- **Nguồn âm thanh:** Ở chế độ âm thanh, chọn dịch **Micrô** của bạn hoặc **Âm thanh hệ thống (Loopback)**. Thư viện loopback nhỏ được tải xuống một lần trong lần sử dụng đầu tiên với sự cho phép của bạn.
- **Ngữ cảnh:** Đối với chế độ màn hình và webcam, hãy chọn tùy chọn **Giới thiệu về việc tôi đang làm** (ví dụ: xem phim, theo dõi cuộc họp hoặc cuộc gọi, đọc nhãn hoặc kiểm tra diện mạo của bạn) để tập trung vào các báo cáo; bạn cũng có thể nhập ngữ cảnh của riêng bạn.
- **Báo cáo:** Tiện ích bổ sung so sánh mọi khung hình mới với khung hình trước đó và chỉ gửi khung hình đó cho AI khi hình ảnh thực sự thay đổi, do đó, bạn không bao giờ phải trả phí cho màn hình tĩnh. AI sau đó chỉ báo cáo những gì mới và không bao giờ lặp lại.
- **Thông báo chào mừng:** Ngoại trừ ở chế độ dịch, người quan sát sẽ chào bạn một cách ngắn gọn khi nó bắt đầu, để bạn biết rằng nó đang lắng nghe.
- **Cài đặt:** Trong **Cài đặt > Trợ lý trực tiếp**, đặt **Chế độ quan sát**, **Khoảng thời gian khung** (1 đến 10 giây) và **Phong cách báo cáo** (ngắn gọn hoặc chi tiết). Hướng dẫn quan sát viên và từng văn bản ngữ cảnh có thể được chỉnh sửa trong Trình quản lý lời nhắc (phần **Ambient**).

## 12. Prompt tùy chỉnh & Biến

Bạn có thể quản lý lời nhắc trong **Cài đặt > Lời nhắc > Quản lý lời nhắc...**.

- **Bộ lọc:** Tab **Lời nhắc mặc định** có danh sách **Bộ lọc** phía trên danh sách lời nhắc hiển thị **Tất cả** lời nhắc hoặc chỉ một phần tại một thời điểm (ví dụ **Ambient**), vì vậy, các danh sách dài luôn dễ dàng điều hướng.

### Phím tắt nhắc nhở tùy chỉnh

Cung cấp cho bất kỳ lời nhắc tùy chỉnh nào phím tắt riêng trực tiếp trong Trình quản lý lời nhắc và chạy nó ngay lập tức với lựa chọn hoặc ngữ cảnh hiện tại của bạn:

- **Khóa đơn** (ví dụ: `1`, `p`, hoặc `F3`): Hoạt động bên trong Lớp Lệnh và cũng hoạt động trên toàn cầu dưới dạng `NVDA + Shift + key`.
- **Tổ hợp phím** (ví dụ: `Control + Shift + 1`, `Alt + P` hoặc `Insert + 1`): Tự hoạt động trên toàn cầu.

### Các biến được hỗ trợ

Mỗi lời nhắc tùy chỉnh có thể xác định riêng hành vi phân phối đầu ra của nó:

- **Cài đặt chung:** Tuân theo cài đặt đầu ra Kết nối chung (Cửa sổ đầu ra trực tiếp hoặc trò chuyện).
- **Sao chép vào bảng nhớ tạm:** Sao chép phản hồi AI trực tiếp vào bảng nhớ tạm mà không cần mở cửa sổ.
- **Đầu ra trực tiếp (thông báo NVDA):** Nói/chữ nổi phản hồi của AI trực tiếp thông qua giọng nói của NVDA.
- **Sao chép vào bảng nhớ tạm và Xuất trực tiếp:** Sao chép câu trả lời vào bảng nhớ tạm và nói trực tiếp.
- **Cửa sổ trò chuyện:** Luôn mở kết quả trong cửa sổ trò chuyện tương tác.

### Các biến được hỗ trợ

- `[selection]`: Văn bản hiện đang được chọn.
- `[clipboard]`: Nội dung clipboard.
- `[screen_obj]`: Ảnh chụp màn hình của đối tượng navigator.
- `[screen_full]`: Ảnh chụp toàn bộ màn hình.
- `[file_ocr]`: Chọn tệp hình ảnh/PDF để trích xuất văn bản.
- `[file_read]`: Chọn tài liệu để đọc (TXT, Code, PDF).
- `[file_audio]`: Chọn tệp âm thanh để phân tích (MP3, WAV, OGG).
- ***
- **Lưu ý:** Cần có kết nối internet đang hoạt động cho tất cả các tính năng AI. Tài liệu nhiều trang được xử lý tự động.
- `[file_read]`: Chọn tài liệu để đọc (TXT, Code, PDF).
- `[file_audio]`: Chọn file âm thanh để phân tích (MP3, WAV, OGG).
- `[ambient_screen]`: Bắt đầu phiên nền của Trình quan sát màn hình liên tục.
- `[ambient_webcam]`: Bắt đầu phiên chạy nền của Webcam Observer liên tục (kiểm tra tính năng Đẩy để nói từ cài đặt).
- `[ambient_audio]`: Bắt đầu phiên dịch Audio Observer trực tiếp.
- `[loopback]`: Sử dụng tính năng phát lại âm thanh hệ thống làm nguồn âm thanh (cho `[ambient_audio]`).
- `[mic]`: Sử dụng micrô làm nguồn âm thanh (cho `[ambient_audio]` và `[ambient_webcam]`).
- `[tóm tắt]`: Đặt kiểu báo cáo của người quan sát thành ngắn gọn (câu đơn).
- `[chi tiết]`: Đặt kiểu báo cáo của người quan sát thành chi tiết (2-3 câu).
- `[lang:code]`: Chỉ định mã ngôn ngữ đích cho bản dịch âm thanh (ví dụ: `[lang:fa]`, `[lang:en]`).
- `{target_lang}`: Ngôn ngữ đích hiện tại.
- `{source_lang}`: Ngôn ngữ nguồn hiện tại.
- `{response_lang}`: Ngôn ngữ phản hồi AI hiện tại.
- `{swap_target}`: Ngôn ngữ dự phòng cho bản dịch hoán đổi thông minh.
- `{swap_instruction}`: Khối lệnh dịch hoán đổi thông minh.

_Lưu ý về Lời nhắc xung quanh:_ Lời nhắc chứa các biến xung quanh hoạt động như một nút chuyển đổi — nhấn phím tắt trong khi hoạt động sẽ ngay lập tức dừng phiên. Các kết hợp không tương thích (chẳng hạn như kết hợp các biến ảnh chụp màn hình tĩnh như `[screen_full]` với chế độ quan sát xung quanh, kết hợp nhiều chế độ xung quanh hoặc thêm hướng dẫn nhắc vào `[ambient_audio]`) đều được xác thực và ngăn chặn nghiêm ngặt khi lưu.

## 13. Các trường hợp sử dụng trong thế giới thực (Tôi nên sử dụng tính năng nào?)

Vision Assistant Pro được tích hợp nhiều công cụ tiên tiến. Dưới đây là một số tình huống phổ biến để giúp bạn chọn đúng:

- **Tình huống: Bạn muốn hiểu bố cục hoàn chỉnh của một cửa sổ phức tạp hoặc ứng dụng không thể truy cập.**
  _Giải pháp:_ Nhấn **O** (Nhìn toàn màn hình). AI sẽ phân tích toàn bộ màn hình và mô tả chính xác vị trí của các phần tử, văn bản và nút.

- **Trường hợp: Bạn tìm thấy một hình ảnh trên trang web hoặc một hình ảnh không được gắn nhãn trong tài liệu.**
  _Giải pháp:_ Di chuyển đối tượng điều hướng của bạn đến đồ họa và nhấn **V** (Tầm nhìn đối tượng). AI sẽ mô tả cụ thể hình ảnh đó chứa đựng những gì.

- **Tình huống: Bạn muốn xem phim hoặc video clip có mô tả bằng âm thanh.**
  _Giải pháp:_ Nhấn **Shift + V** trên video của bạn và chọn **"Tạo mô tả âm thanh (Tệp SRT)"**. Khi quá trình hoàn tất, hãy nhấp vào **"Tạo tường thuật được đồng bộ hóa (MP3)"** và chọn **"Quảng cáo mở rộng"**. Tiện ích bổ sung này sẽ tạo một đoạn âm thanh tạm dừng đoạn hội thoại của phim một cách thông minh để mô tả các cảnh trực quan.

- **Tình huống: Bạn gặp phải một ứng dụng chứa đầy "các nút không được gắn nhãn".**
  _Giải pháp:_ Nhấn **L** để gắn nhãn vĩnh viễn cho nút cụ thể bằng AI. Hoặc nhấn **Shift + L** để quét và gắn nhãn cho toàn bộ cửa sổ cùng một lúc. Nếu bạn chỉ muốn nhấp nhanh vào nội dung nào đó, hãy nhấn **E** (UI Explorer) để nhận danh sách tất cả các mục có thể nhấp.

- **Tình huống: Bạn cần bỏ qua CAPTCHA không thể truy cập được.**
  _Giải pháp:_ Nhấn **C** (Bộ giải CAPTCHA). AI sẽ tự động chụp CAPTCHA, giải nó và đưa câu trả lời vào trường chính xác.

- **Kịch bản: Bạn muốn đọc một tài liệu PDF dài 50 trang.**
  _Giải pháp:_ Nhấn **D** (Trình đọc tài liệu), đặt nhà cung cấp của bạn thành Google Gemini và nhập phạm vi trang `1-50`. Tiện ích bổ sung sẽ trích xuất văn bản chính xác trong nền.

- **Tình huống: Bạn đang xem video hướng dẫn hoặc hoạt ảnh không có tiếng động trên màn hình.**
  _Giải pháp:_ Nhấn **Control + V** để bắt đầu quay màn hình. Để phần hướng dẫn phát rồi nhấn **Control + V** lần nữa. AI sẽ giải thích chính xác những gì đã được chứng minh.

- **Tình huống: Bạn gặp phải lỗi không mong muốn, lỗi kết nối API hoặc muốn chẩn đoán sự cố với máy chủ cục bộ tùy chỉnh.**
  _Giải pháp:_ Đi tới **Cài đặt > Nâng cao**, chọn **"Bật tệp nhật ký chuyên dụng"** và đặt **Cấp độ nhật ký** thành **"Gỡ lỗi"**. Thực hiện lại hành động, sau đó nhấp vào **"Mở tệp nhật ký"** để kiểm tra chi tiết kỹ thuật hoặc đính kèm `vision_assistant.log` vào phiếu hỗ trợ.

***

**Lưu ý:** Cần có kết nối Internet đang hoạt động để sử dụng tất cả các tính năng AI. Tài liệu nhiều trang được xử lý tự động.

## 14. Hỗ trợ & Cộng đồng

Luôn cập nhật những tin tức, tính năng và bản phát hành mới nhất:

- **Kênh Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Vấn đề về GitHub:** Dành cho báo cáo lỗi và yêu cầu tính năng.

### Báo cáo lỗi & nhật ký

Khi mở một vấn đề về GitHub hoặc yêu cầu hỗ trợ, vui lòng bao gồm thông tin chi tiết về nhà cung cấp AI, kiểu máy và phiên bản NVDA đang hoạt động của bạn. Nếu bạn gặp sự cố kết nối hoặc sự cố không mong muốn, hãy bật tệp nhật ký chuyên dụng trong **Cài đặt > Nâng cao**, tạo lại sự cố và đính kèm tệp `vision_assistant.log` của bạn để giúp chúng tôi giải quyết sự cố nhanh hơn.

## 15. Người ủng hộ dự án

Xin gửi lời cảm ơn chân thành đến các thành viên cộng đồng của chúng tôi, những người đã hỗ trợ phát triển và duy trì liên tục dự án này thông qua những đóng góp tài chính hào phóng của họ:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**
- **leonardo0216**
- **Sergei Fleytin**
- **Arne Siebert**
- **Schalkefan**
- **Rainer Brell**
- **[avalai.org](https://avalai.org)**

_Nếu bạn muốn hỗ trợ tài chính cho dự án và thấy tên mình ở đây, bạn có thể tìm thấy tùy chọn **Quyên góp** trong menu Công cụ NVDA (menu phụ Vision Assistant) hoặc trong quá trình thiết lập sau khi cài đặt._

---

## Những thay đổi cho ngày 15/10/2026

- **Cách khắc phục được yêu cầu nhiều nhất — Tạo khóa API Gemini cuối cùng cũng dễ dàng**: Lấy khóa API trên **aistudio.google.com** từng là bước khó nhất. Với trình đọc màn hình, các trang rất khó hiểu và một số người hoàn toàn không thể tạo khóa. Vấn đề đó hiện đã được giải quyết trực tiếp bên trong tiện ích bổ sung. Nhấn **G** trong Lớp lệnh (hoặc sử dụng **Nhận khóa API Gemini...** trong Cài đặt), đăng nhập thông qua trình duyệt mặc định của bạn mà không cần thiết lập bên ngoài và khóa của bạn được tạo và định cấu hình chỉ bằng một xác nhận — ngay cả khi bạn chưa từng có dự án trước đây.
- **Quan sát môi trường**: Trợ lý nền đã có mặt. Nhấn **Shift+O** trong Lớp Lệnh để khởi động và nhấn lại để dừng. Nó có thể dịch những gì nó nghe được (micrô của bạn hoặc âm thanh của hệ thống), xem màn hình và cho bạn biết điều gì đã thay đổi hoặc mở Trợ lý trực tiếp bằng webcam và Nhấn để nói (Push to Talk) để bạn có thể hỏi về bất cứ điều gì camera nhìn thấy. Nó chỉ gửi hình ảnh khi có điều gì đó thực sự thay đổi, do đó, màn hình tĩnh sẽ không làm bạn tốn kém và nó sẽ im lặng khi không có gì xảy ra. Bạn cũng có thể khởi chạy và chuyển đổi trực tiếp trình quan sát thông qua Lời nhắc tùy chỉnh và các phím tắt chuyên dụng bằng cách sử dụng `[ambient_screen]`, `[ambient_webcam]` hoặc `[ambient_audio]` cùng với công cụ sửa đổi (`[loopback]`, `[mic]`, `[brief]`, `[detailed]`, `[lang:code]`), với tính năng xác thực tự động đối với các kết hợp biến xung đột.
- **Người vận hành trực tiếp**: Trợ lý trực tiếp giờ đây có thể thực hiện những gì bạn yêu cầu trên máy tính trong khi bạn nói chuyện với nó. Nhấn **Control+A** trong Lớp lệnh để bắt đầu phiên điều hành trực tiếp, sau đó chỉ cần hỏi bằng ngôn ngữ đơn giản. Nó hoạt động thông qua các yêu cầu gồm nhiều bước, nói từng bước bằng giọng nói của Trợ lý trực tiếp, xử lý các tổ hợp phím cần thiết và tự quyết định khi tác vụ hoàn thành. **Đầu ra trực tiếp trực tiếp (Không có cửa sổ)** cũng có trong Cài đặt nhanh.
- **Quản lý bộ truyện & Từ điển ký tự**: Hộp thoại Phân tích video hiện bao gồm hệ thống **Từ điển ký tự** mạnh mẽ! Thêm, chỉnh sửa, nhập hoặc quản lý tên nhân vật, mô tả ngoại hình và vai trò trên mỗi bộ — AI tự động khớp các ký tự được phát hiện với từ điển của bạn và hợp nhất các ký tự mới khi bạn phân tích nhiều tập hơn. Các ghi chú thủ công của bạn luôn được ưu tiên giữ nguyên so với các bản cập nhật AI, trong khi các mô tả vật lý luôn được cập nhật qua các tập. Từ điển được lưu theo từng bộ và được sử dụng lại cho mọi video trong bộ đó. Trong danh sách ký tự, nhấn **F2** để chỉnh sửa ký tự đã chọn và **Xóa** để xóa ký tự đó.
- **Hỗ trợ SOCKS5, HTTP và Reverse Proxy với Kiểm tra độ trễ**: Vượt qua các hạn chế mạng một cách liền mạch với sự hỗ trợ proxy hoàn chỉnh trên toàn bộ tiện ích bổ sung — bao gồm Trợ lý trực tiếp, Trình quan sát xung quanh và thế hệ TTS! Chọn từ 4 chế độ hoạt động trong Cài đặt chung: **Tự động phát hiện**, **Proxy SOCKS5**, **Proxy HTTP** hoặc **Proxy ngược**. SOCKS5 hỗ trợ xác thực tên người dùng/mật khẩu RFC 1929 và đường hầm tên miền; Proxy HTTP hỗ trợ xác thực cơ bản. Nút **Kiểm tra kết nối proxy** mới chạy ở chế độ nền và thông báo độ trễ kết nối của bạn tính bằng mili giây.
- **Bộ nhớ đệm tệp video trong 48 giờ**: Các video được tải lên Gemini hiện được lưu trong bộ nhớ đệm trong 48 giờ! Bạn có thể tạo lại đầu ra SRT hoặc MP3 cho cùng một video mà không cần tải lên lại — ngay cả sau khi khởi động lại NVDA. Bộ nhớ đệm nhận biết khóa và tự động vô hiệu hóa khi khóa API của bạn thay đổi.
- **Phát hiện im lặng được hỗ trợ bởi AI (Silero VAD)**: AD mở rộng hiện sử dụng mô hình thần kinh Silero VAD để phát hiện khoảng lặng chính xác — phân biệt các khoảng dừng đối thoại tự nhiên với âm nhạc và tiếng ồn xung quanh. Mô hình được tải xuống tự động trong lần sử dụng đầu tiên (với sự cho phép của bạn), giống như ffmpeg và eSpeak.
- **Video Webcam dành cho Trợ lý trực tiếp**: Cửa sổ Trợ lý trực tiếp hiện có hộp kiểm **Sử dụng &Webcam** để gửi nguồn cấp dữ liệu webcam của bạn tới AI thay vì màn hình của bạn — hoàn hảo để đặt câu hỏi về các vật thể, tài liệu hoặc môi trường xung quanh bạn. Nếu ffmpeg chưa được cài đặt, hãy đánh dấu vào ô tải xuống (một lần, với sự cho phép của bạn). Tùy chọn này bị tắt khi không phát hiện thấy camera hoặc cài đặt quyền riêng tư của Windows chặn quyền truy cập vào camera, bằng nút để mở cài đặt quyền riêng tư của camera. Nếu máy ảnh được bật nhưng không tạo ra khung hình nào, sự cố sẽ được ghi vào nhật ký NVDA để chẩn đoán thay vì âm thầm chuyển trở lại màn hình.
- **Lựa chọn thiết bị đầu ra âm thanh**: Giờ đây, bạn có thể chọn thiết bị đầu ra âm thanh chuyên dụng cho Trợ lý trực tiếp và Người quan sát xung quanh. Chọn giữa đầu ra mặc định của NVDA, Windows Sound Mapper hoặc bất kỳ card âm thanh vật lý nào được kết nối (như tai nghe USB hoặc loa ngoài) trong tab Cài đặt Trực tiếp, trực tiếp bên trong hộp thoại Trợ lý Trực tiếp hoặc nhanh chóng qua Cài đặt Nhanh (NVDA+Shift+V rồi Lên/Xuống/Trái/Phải).
- **Trình quản lý lời nhắc**: Tab Lời nhắc mặc định hiện có danh sách **Bộ lọc**, vì vậy bạn có thể hiển thị tất cả lời nhắc hoặc chỉ một phần (ví dụ **Ambient**). Bạn cũng có thể chỉnh sửa văn bản ngữ cảnh của người quan sát và **Hướng dẫn người vận hành trực tiếp** mới ở đó.
- **Lọc mô hình thông minh trong Định tuyến nâng cao**: Danh sách thả xuống Định tuyến mô hình nâng cao hiện phân loại động các mô hình Gemini theo khả năng mà không bị lộn xộn. Trợ lý trực tiếp chỉ hiển thị các mô hình âm thanh gốc và trực tiếp hai chiều đích thực, TTS chỉ hiển thị các mô hình tổng hợp giọng nói chuyên dụng, STT ưu tiên các mô hình Chép lời và đa phương thức, còn Phân tích video, OCR và Toán tử AI lọc sạch các mô hình tiện ích đơn mục đích (chẳng hạn như tạo hình ảnh, tạo video và mô hình nhúng). Các mẫu máy trong tương lai được phát hiện tự động dựa trên khả năng mà không yêu cầu cập nhật phiên bản.
- **Theo dõi ngoại hình lần đầu của nhân vật**: AI hiện chỉ mô tả ngoại hình của mỗi nhân vật một lần — ở lần xuất hiện đầu tiên của họ trong video. Những lần xuất hiện tiếp theo chỉ sử dụng tên, loại bỏ các mô tả lặp đi lặp lại giữa các phân đoạn trong khi vẫn giữ cho câu chuyện mới mẻ và tự nhiên.
- **Thư mục dữ liệu hợp nhất**: Tất cả các tệp dữ liệu bổ trợ (lịch sử, chuỗi, nhãn, tiến trình OCR, bộ đệm và nhật ký) đã được di chuyển vào một thư mục `VisionAssistant` duy nhất bên trong thư mục cấu hình NVDA của bạn — giữ mọi thứ ngăn nắp và thực hiện sao lưu thủ công dễ dàng.
- **Trải nghiệm lưu video được cải thiện**: Khi lưu tệp SRT hoặc MP3, hộp thoại tệp hiện sẽ mở trong thư mục của video nguồn theo mặc định, cho dù bạn mở video qua hộp thoại tệp hay Shift+V từ Explorer.
- **Xóa tài liệu có hoặc không có văn bản được lưu trong bộ nhớ đệm**: Hộp thoại Lịch sử (`Control + H`) hiện cung cấp hai cách để xóa tài liệu — nhấn Xóa và chọn **Chỉ xóa khỏi lịch sử** hoặc **Xóa khỏi lịch sử và văn bản được lưu trong bộ nhớ cache**. Tùy chọn thứ hai sẽ xóa văn bản OCR được lưu trong bộ nhớ đệm của tài liệu đó, do đó, lần mở tiếp theo sẽ quét lại từ đầu — lý tưởng sau khi quét kém. Hộp kiểm **Không hỏi lại** ghi nhớ lựa chọn của bạn để xóa trong tương lai. Dữ liệu tiếp tục hoạt động bị gián đoạn của bạn không bao giờ được chạm vào.
- **Nhận biết công cụ, hợp nhất bộ đệm OCR trong trình đọc tài liệu**: Văn bản OCR được lưu trong bộ nhớ đệm hiện được lưu trữ trên mỗi công cụ OCR, do đó, việc chuyển đổi công cụ OCR luôn quét lại bằng công cụ mới thay vì phát lại kết quả cũ. Việc mở lại tài liệu sẽ hiển thị lại hộp thoại phạm vi trang (được điền sẵn với lựa chọn cuối cùng của bạn), ngay lập tức sử dụng lại các trang đã được quét và chỉ quét những trang bị thiếu — bộ đệm sẽ hợp nhất từng trang thay vì bị thay thế, vì vậy mọi phạm vi bạn đọc sẽ được lưu giữ cho sau này.
- **Nén PDF trong Trình đọc Tài liệu**: Đã thêm cài đặt **Nén các trang PDF trước khi xử lý** tùy chọn trong hộp thoại phạm vi trang của Trình đọc Tài liệu. Khi tải các tài liệu PDF được quét có độ phân giải cao hoặc lớn lên Gemini hoặc Mistral, các trang sẽ tự động được thu nhỏ và nén lại để giảm đáng kể kích thước tải trọng tải lên, tăng tốc độ xử lý và ngăn chặn thời gian chờ mạng. Tùy chọn này bị tắt theo mặc định và tự động ẩn khi sử dụng công cụ Chrome hoặc nhà cung cấp hình ảnh dựa trên base64.
- **Tùy chỉnh hành vi phản hồi theo từng lời nhắc**: Tùy chỉnh cách mỗi lời nhắc tùy chỉnh cung cấp đầu ra riêng lẻ! Trong trình chỉnh sửa lời nhắc tùy chỉnh, chọn giữa **Cài đặt chung**, **Sao chép vào bộ nhớ tạm**, **Xuất trực tiếp (tin nhắn NVDA)**, **Sao chép vào bộ nhớ tạm và Xuất trực tiếp** hoặc **Cửa sổ trò chuyện**. Điều này cho phép những lời nhắc cụ thể nói trực tiếp mà không cần mở cửa sổ trong khi những lời nhắc khác mở cuộc trò chuyện đầy đủ.
- **Biến lời nhắc động mới (`[currentURL]` & `[text]`)**: Lời nhắc tùy chỉnh hiện hỗ trợ `[currentURL]` để nắm bắt URL tài liệu đang hoạt động trên Google Chrome, Mozilla Firefox và Microsoft Edge và `[text]` để chèn động nội dung văn bản đầy đủ của trường chỉnh sửa hiện được tập trung (bỏ qua các hộp mật khẩu được bảo vệ).
- **Đại tu Trình tải xuống video Twitter/X**: Đã khôi phục tải xuống và phân tích các video Twitter/X sau lỗi của trình quét ngược dòng. Việc trích xuất video hiện sử dụng API FixTweet mạnh mẽ để tìm nạp trực tiếp các luồng MP4 chất lượng cao nhất từ ​​CDN của Twitter, hoàn chỉnh với hỗ trợ proxy và dự phòng TwitSave tự động.
- **Bản sửa lỗi của Trình tải xuống video trên Instagram**: Đã khôi phục quá trình tải xuống và phân tích các Câu chuyện trên Instagram và URL video sau những thay đổi về biểu mẫu ngược dòng trên dịch vụ trình tải xuống.
- **Sửa lỗi & Hiệu suất**: Nhấn để nói (Push to Talk) trả lời ngay khi bạn nhấn phím, Trợ lý trực tiếp không còn bắt đầu trả lời ở giữa câu, người quan sát không còn báo cáo hình ảnh trước đó nữa và danh sách Chiều sâu tư duy chỉ cung cấp những gì mô hình của bạn thực sự hỗ trợ. Người vận hành AI cũng có thể cuộn sang trái và phải. Đã sửa lỗi `AttributionError` khi phân tích video trực tuyến và ngăn các lời nhắc tùy chỉnh không có lựa chọn văn bản vô tình đưa tiêu đề cửa sổ nền vào các yêu cầu AI.

## Những thay đổi cho ngày 01/09/2026

- **Lịch sử (Control + H)**: Lớp Lệnh hiện bao gồm hộp thoại **Lịch sử** (`Control + H`) liệt kê các cuộc trò chuyện và tài liệu trước đây của bạn với các bộ lọc cho Tất cả, Trò chuyện và Tài liệu. Mở lại bất kỳ cuộc trò chuyện nào với toàn bộ cuộc trò chuyện — các tệp đính kèm được đính kèm lại tự động — hoặc mở lại tài liệu và tiếp tục đọc. Nhấn **Xóa** trên bất kỳ mục nào để xóa mục đó hoặc xóa mọi thứ cùng một lúc.
- **Tài liệu Gần đây trong Trình đọc**: Nhấn **D** trong Lớp Lệnh hiện sẽ hiển thị các tài liệu đã đọc gần đây của bạn trước tiên. Chọn một để tiếp tục từ trang bạn đang truy cập — ngay cả khi OCR đã hoàn tất — hoặc nhấn **Mở tệp...** (`Ctrl + O`) để duyệt như bình thường.
- **Nhấn để nói cho Trợ lý trực tiếp**: Kiểm soát hoàn toàn các cuộc trò chuyện trực tiếp của bạn! Bật **Nhấn để nói** trong tab cài đặt Trợ lý trực tiếp mới và gán bất kỳ phím nào — hoặc thậm chí là một phím bổ trợ duy nhất như `Ctrl trái` — để nói chuyện. Giữ phím để nói và thả phím ra khi bạn nói xong, kèm theo một tiếng bíp ngắn mỗi lần nhấn và thả. Nút chuyển đổi phù hợp cũng xuất hiện ngay trong cửa sổ Trợ lý trực tiếp, vì vậy bạn có thể chuyển đổi giữa chế độ nhấn để nói và mở micrô mà không cần rời khỏi cuộc trò chuyện.
- **Âm thanh gốc của Gemini 2.5**: Trợ lý trực tiếp hiện hỗ trợ mẫu âm thanh gốc của Gemini 2.5 Flash (`gemini-2.5-flash-native-audio-preview-12-2025`) cho các cuộc hội thoại bằng giọng nói tự nhiên, có độ trễ thấp. Bạn có thể chuyển sang chế độ này từ **Cài đặt → Định tuyến mô hình nâng cao → Mô hình trợ lý trực tiếp (chỉ dành cho Gemini)** hoặc giữ "Tự động" để duy trì mô hình được đề xuất.
- **Cài đặt Sao lưu & Khôi phục**: Đã thêm hệ thống sao lưu và khôi phục mạnh mẽ trong tab **Nâng cao**! Giờ đây, bạn có thể lưu tất cả cài đặt tiện ích bổ sung — bao gồm khóa API, mô hình, lời nhắc tùy chỉnh và tùy chọn — vào một tệp JSON duy nhất và khôi phục chúng một cách hoàn hảo bất kỳ lúc nào, trên bất kỳ máy nào hoặc sau khi cài đặt lại NVDA. Khi sao lưu, bạn chọn những gì cần bao gồm: **Mọi thứ** (cài đặt, nhãn tùy chỉnh, tiến trình OCR và lịch sử) hoặc **Chỉ cài đặt**.
- **Đọc văn bản trực tiếp & HTML**: Trình đọc tài liệu giờ đây có thể mở trực tiếp các tệp văn bản thuần túy (`.txt`) và HTML (`.html`, `.htm`)! Nó tự động phát hiện mã hóa tệp, loại bỏ các tập lệnh và định dạng lộn xộn, đồng thời phân chia nội dung thành các trang có thể đọc được một cách thông minh — thậm chí nhập lại các tệp đã xuất của chính tệp đó trong khi vẫn giữ nguyên cấu trúc trang — để bạn có thể đọc chúng ngay lập tức mà không cần xử lý OCR hoặc AI!
- **Gemini Live TTS dành cho Trình đọc tài liệu**: Nút "Tạo âm thanh" hiện hỗ trợ Gemini Live — một công cụ chuyển văn bản thành giọng nói với tốc độ tự nhiên, chất lượng cao! Khi Gemini là nhà cung cấp tích cực của bạn, bạn có thể chọn giữa TTS Tiêu chuẩn và Gemini Live ngay trong trình đọc và lựa chọn của bạn sẽ được ghi nhớ cho lần tiếp theo!
- **Phím tắt lời nhắc tùy chỉnh**: Giờ đây, bạn có thể gán phím tắt cho bất kỳ lời nhắc tùy chỉnh nào của mình ngay từ Trình quản lý lời nhắc! Cung cấp cho mỗi lời nhắc phím hoặc tổ hợp phím chuyên dụng riêng để chạy ngay lập tức, tự động ghi lại lựa chọn hoặc bối cảnh hiện tại của bạn mà không cần thực hiện thêm bước nào!
- **Điều hướng tin nhắn trò chuyện**: Xem lại mọi cuộc trò chuyện rảnh tay! Bên trong bất kỳ cửa sổ trò chuyện nào (Trò chuyện trực tiếp, trò chuyện tài liệu, tinh chỉnh, v.v.), hãy nhấn `Alt + Down` để nghe tin nhắn tiếp theo và `Alt + Up` để nghe tin nhắn trước đó — với tiền tố "Bạn" / "AI" rõ ràng và ranh giới "Tin nhắn đầu tiên" / "Tin nhắn cuối cùng" được thông báo khi bạn tiếp tục.
- **Sao chép tin nhắn trò chuyện (Alt + C)**: Trong khi xem lại cuộc trò chuyện bằng `Alt + Lên/Xuống`, nhấn `Alt + C` để sao chép tin nhắn bạn hiện đang xem vào bảng nhớ tạm — tôn trọng cài đặt Đánh dấu sạch của bạn — bằng xác nhận bằng giọng nói.
- **Lời nhắc hệ thống trò chuyện trực tiếp**: Trò chuyện trực tiếp (`Shift+C`) hiện có lời nhắc hệ thống có thể chỉnh sửa riêng — "Hướng dẫn trò chuyện trực tiếp" — đặt tính cách của trợ lý và ngôn ngữ phản hồi cho mọi cuộc trò chuyện. Bạn có thể tùy chỉnh nó từ tab Lời nhắc mặc định của Trình quản lý lời nhắc.
- **Điều hướng trang bằng con trỏ trình đọc tài liệu**: Đọc tài liệu nhiều trang trở nên mượt mà hơn! Trong Trình xem Tài liệu, khi con trỏ của bạn đến dòng cuối cùng của trang và bạn nhấn `Xuống`, trình đọc sẽ tự động chuyển sang trang tiếp theo. Nhấn `Up` ở đầu trang sẽ đưa bạn trở lại trang trước một cách liền mạch — không còn phải chuyển trang thủ công trong khi đọc!
- **Bật tắt cài đặt nhanh mới**: Sao chép phản hồi AI vào bộ nhớ tạm, Xuất trực tiếp (không có cửa sổ trò chuyện), Đánh dấu rõ ràng trong Trò chuyện và Hoán đổi thông minh giờ đây có thể được bật và tắt ngay lập tức từ Cài đặt nhanh của lớp lệnh!
- **Tab cài đặt Trợ lý trực tiếp**: Trợ lý trực tiếp hiện có tab cài đặt riêng! Tùy chọn "Trợ lý trực tiếp: Đầu ra trực tiếp (Không có cửa sổ)" được chuyển đến đây từ tab Kết nối và tab này chỉ xuất hiện khi Google Gemini (hoặc Nhà cung cấp tùy chỉnh tương thích với Gemini) là nhà cung cấp đang hoạt động của bạn.

## Những thay đổi cho ngày 06/06/2026

- **Gắn nhãn UI Explorer**: Giờ đây, bạn có thể thêm nhãn trực tiếp vào các thành phần được tìm thấy bên trong UI Explorer! Nút "Thêm nhãn" mới đã được thêm vào và giao diện luôn mở thông minh và duy trì tiêu điểm để bạn có thể nhanh chóng gắn nhãn cho nhiều đối tượng mà không bị gián đoạn.
- **Cải tiến lớp cài đặt nhanh**: Lớp Hỗ trợ thị giác (`Insert+Shift+V`) hiện đã ổn định và có tính tương tác cao! Bạn có thể sử dụng mũi tên `Up/Down` để điều hướng giữa các cài đặt nhanh (Nhà cung cấp, Mô hình, Ngôn ngữ phản hồi AI, Mô hình TTS) và mũi tên `Trái/Phải` để thay đổi ngay giá trị của chúng bằng phản hồi bằng giọng nói thông minh, ngắn gọn. Các lựa chọn của bạn sẽ có hiệu lực ngay lập tức (bao gồm cả việc tự động bật định tuyến nâng cao khi cần thiết) và lớp vẫn tồn tại trong khi bạn định cấu hình.
- **Trò chuyện trực tiếp (`Shift+C`)**: Đã thêm lệnh mới vào lớp! Nhấn `Shift+C` để mở ngay cửa sổ "Trò chuyện trực tiếp". Điều này cung cấp giao diện trò chuyện dựa trên văn bản, rõ ràng với AI ngay lập tức mà không cần hình ảnh hoặc tài liệu làm điểm bắt đầu.
- **Gọi lại lịch sử trò chuyện hoàn hảo**: Đã sửa lỗi lớn khi nhấn `Phím cách` để gọi lại kết quả cuối cùng sẽ làm mất lịch sử trò chuyện tiếp theo của bạn. Giờ đây, tiện ích bổ sung này sẽ theo dõi cuộc trò chuyện của bạn trên toàn cầu. Nếu bạn trò chuyện, hãy đóng hộp thoại và nhấn `Space` để gọi lại, toàn bộ lịch sử qua lại của bạn sẽ được khôi phục hoàn hảo! Hoạt động cho Trò chuyện trực tiếp, Phân tích tầm nhìn, Trò chuyện tài liệu và Dịch thuật.
- **Mô tả hình ảnh nội tuyến trong OCR**: Đã thêm tính năng tùy chọn để mô tả hình ảnh nội tuyến trong tài liệu OCR. Bạn có thể chuyển đổi cài đặt này trong cài đặt OCR của tiện ích bổ sung, trong tùy chọn Trình đọc tài liệu trước khi trích xuất và nhanh chóng thông qua lớp Cài đặt nhanh.
- **Dịch giọng nói (`Control+T`)**: Đã thêm một tính năng mới mạnh mẽ! Đọc chính tả lời nói, dịch và nhập ngay lập tức bằng AI dựa trên ngôn ngữ đích và ngôn ngữ nguồn đã định cấu hình của bạn.
- **Cải tiến trình tải xuống bản cập nhật**: Hộp thoại tải xuống bản cập nhật hiện hiển thị chính xác tiến trình tải xuống theo tỷ lệ phần trăm và lỗi xuất hiện thông báo ảo "Đang tải xuống bản cập nhật" khi hủy cài đặt đã được sửa.
- **Cải tiến về trình tải xuống eSpeak-NG**: Đã thêm tính năng theo dõi tiến trình phần trăm cho các lượt tải xuống eSpeak-NG.
- **Khả năng phục hồi OCR hàng loạt**: Đã khắc phục sự cố trong PDF OCR hàng loạt trong đó quá trình sẽ tạm dừng nếu khóa API hoạt động đạt đến hạn ngạch giữa chừng; bây giờ nó sẽ tự động chuyển sang khóa có sẵn tiếp theo và tiếp tục quá trình.
- **Hỗ trợ hình ảnh xác thực trực quan**: Đã thêm hỗ trợ mạnh mẽ cho việc giải hình ảnh xác thực trực quan. Nó cố gắng tự động giải quyết các thách thức hình ảnh phức tạp như hCaptcha và reCAPTCHA, tăng cường đáng kể khả năng truy cập trên các biểu mẫu web đầy thách thức.
- **Đại tu Bộ chuyển đổi âm thanh**: Mô-đun Bộ chuyển đổi âm thanh đã được xây dựng lại hoàn toàn và hiện hỗ trợ cả tệp âm thanh và video. Nó có 3 chế độ hoạt động riêng biệt: "Phiên âm (Ngôn ngữ gốc)", "Phiên âm và dịch (Ngôn ngữ đích)" và tùy chọn "Lồng tiếng và dịch (Ngôn ngữ đích)" mạnh mẽ mới (dành riêng cho Gemini) tạo ra bản lồng tiếng âm thanh đã dịch của bài phát biểu gốc.
- **Số trang tùy chọn trong Trình đọc tài liệu**: Đã thêm cài đặt mới để chuyển đổi việc đưa số trang và dấu phân cách vào đầu ra tài liệu nhiều trang. Bạn có thể dễ dàng quản lý tùy chọn này từ cài đặt chính hoặc chuyển đổi nhanh chóng thông qua lớp Cài đặt nhanh. Tính năng này áp dụng cho cả việc xuất tệp văn bản/HTML và cửa sổ "Xem được định dạng" nội tuyến, cho phép bạn đọc các tài liệu kết hợp một cách liền mạch.
- **TTS trực tiếp Gemini không giới hạn cho mô tả video**: Giờ đây, bạn có thể chọn "TTS trực tiếp Gemini" làm công cụ giọng nói khi tạo Tường thuật âm thanh được đồng bộ hóa (MP3) cho video. Điều này sử dụng API Gemini Live để tổng hợp các mô tả âm thanh chất lượng cao mà không có bất kỳ giới hạn ký tự hoặc giới hạn độ dài nào.
- **Mô-đun hóa cơ sở mã**: Đã tái cấu trúc cấu trúc tiện ích bổ sung từ một tệp duy nhất thành kiến ​​trúc mô-đun nhiều tệp để cải thiện khả năng bảo trì.
- **Thiết kế lại giao diện người dùng cài đặt**: Đã thiết kế lại hoàn toàn hộp thoại Cài đặt để sử dụng giao diện hiện đại, dựa trên tab thay vì bố cục được nhóm, giúp tổ chức tốt hơn và điều hướng dễ dàng hơn trong khi vẫn giữ tất cả các tùy chọn hiện có.
- **Ghi nhật ký tệp toàn cầu và chuyên dụng**: Đã thêm hệ thống ghi tệp toàn cầu tùy chọn trong tab cài đặt "Nâng cao" mới. Tự động ghi lại các sự kiện vận hành, lưu lượng API và lỗi trên tất cả các mô-đun tiện ích bổ sung vào một tệp chuyên dụng (`vision_assistant.log`). Hỗ trợ mức độ chi tiết của nhật ký có thể định cấu hình (Gỡ lỗi, Thông tin, Cảnh báo, Lỗi), thời gian lưu giữ tự động (1 giờ đến 90 ngày) và mở hoặc xóa nhật ký trực tiếp khỏi cài đặt mà không ảnh hưởng đến hiệu suất hoặc nhiễu nhật ký NVDA.
- **Theo dõi tiến trình tải lên của Gemini**: Đã thêm thông báo tiến trình phần trăm theo thời gian thực khi tải các tệp lớn (video, âm thanh, tài liệu) lên API Google Gemini.

## Những thay đổi cho ngày 15/07/2026

- **Lọc mô hình API thông minh**: Sửa chữa hoàn toàn hệ thống lọc mô hình để sử dụng phương pháp tiếp cận danh sách đen thuần túy thay vì danh sách trắng. Đã thêm các từ khóa lọc mạnh hơn (`embedding`, `bison`, `gecko`, `audio`, `realtime`, `babbage`, `moderation`, `deep`, `anti Gravity`, `computer`) để đảm bảo danh sách mô hình trò chuyện chính thả xuống vẫn hoàn toàn sạch sẽ và phù hợp với tương lai, đồng thời vẫn giữ cho tất cả các mô hình chuyên dụng có thể truy cập được trong phần Định tuyến nâng cao.
- **Tìm kiếm định tuyến nâng cao**: Tất cả danh sách thả xuống Định tuyến mô hình nâng cao (OCR, STT, TTS, Toán tử, Video, Trực tiếp) và bộ chọn Biến thể eSpeak hiện có thể tìm kiếm đầy đủ. Bạn có thể nhanh chóng nhập để lọc và tìm mẫu hoặc biến thể mong muốn của mình.
- **Phím tắt lớp lệnh mới**:
  - **Cài đặt (`Alt + S`)**: Mở ngay hộp thoại cài đặt Vision Assistant Pro.
  - **Báo cáo khóa đã hết hạn ngạch (`Alt + Q`)**: Báo cáo chính xác số lượng khóa API Gemini đã vượt quá hạn ngạch hàng ngày, xác định mô hình cụ thể mà chúng đã hết và thông báo thời gian đặt lại chính xác của chúng.
  - **Kiểm tra định tuyến (`Alt + M`)**: Kiểm tra và thông báo cấu hình Định tuyến nâng cao hiện tại của bạn, đọc ra những mô hình nào được chọn tích cực cho các tác vụ chuyên biệt (bỏ qua cài đặt mặc định).
- **Đại tu hoàn chỉnh Trình phân tích video**: Trình phân tích video đã được chuyển đổi hoàn toàn! Trước đây, nó chỉ cung cấp mô tả cơ bản về video trực tuyến. Giờ đây, nó là bộ xử lý video toàn diện được thiết kế riêng cho người dùng khiếm thị:
  - **Ghi màn hình cục bộ (`Control+V`)**: Giờ đây, bạn có thể quay video im lặng trực tiếp từ màn hình của mình. AI sẽ phân tích phân đoạn được ghi lại và cung cấp mô tả rất chi tiết về cảnh, bố cục và hành động.
  - **Tạo mô tả âm thanh (SRT)**: Tiện ích bổ sung hiện có thể tạo các tập lệnh Mô tả âm thanh có độ chi tiết cao (ở định dạng SRT tiêu chuẩn) cho video, hoàn chỉnh với khoảng cách thời gian thông minh để neo mô tả một cách thông minh vào các khoảng dừng tự nhiên trong bản âm thanh và OCR nguyên văn cho mọi văn bản trên màn hình.
  - **Tường thuật âm thanh được đồng bộ hóa (Xuất MP3)**: Ngoài phụ đề dựa trên văn bản, tiện ích bổ sung có thể tổng hợp Mô tả âm thanh thành giọng nói, tự động trộn nó với đoạn âm thanh gốc của video, áp dụng tính năng giảm âm thanh (giảm âm lượng nền trong khi mô tả) và xuất kết quả được đồng bộ hóa cuối cùng dưới dạng tệp MP3!
  - **Hành động tệp video thông minh**: Nếu bạn tập trung vào tệp video cục bộ và nhấn phím tắt video, tiện ích bổ sung sẽ tự động phát hiện tệp đó và xử lý tệp trực tiếp.
  - **Theo dõi ký tự nâng cao**: AI hiện thực hiện quá trình trích xuất ký tự trước. Nó xây dựng một từ điển ký tự toàn cầu và theo dõi các ký tự một cách chính xác theo từng phân đoạn mà không gây nhầm lẫn danh tính.
  - **Cấu hình phân tích video**: Đã thêm cài đặt mới để kiểm soát kích thước đoạn SRT, phụ đề ký tự và tuyên bố từ chối trách nhiệm.
  - **Định tuyến mô hình mở rộng**: Giờ đây, bạn có thể chọn rõ ràng các mô hình video chuyên biệt (`gemini_video_model`, `custom_video_model`) trong cài đặt Định tuyến mô hình nâng cao.
- **Quản lý hạn ngạch API thông minh**: Xử lý nâng cao 429 lỗi (Giới hạn hàng ngày) bằng cách theo dõi hạn ngạch cho mỗi mô hình. Nếu một khóa đạt đến giới hạn hàng ngày trên một kiểu máy, khóa đó sẽ chỉ được cách ly một cách thông minh cho kiểu máy cụ thể đó, để lại khóa có sẵn để sử dụng với các kiểu máy khác.

## Những thay đổi cho 7.0.0

- **Tiếp tục các bản quét chưa hoàn thành**: Đã thêm tính năng tiếp tục cho cả Trình đọc tài liệu và Tác vụ tệp thông minh. Nếu quá trình quét bị gián đoạn, giờ đây bạn có thể tiếp tục từ nơi quá trình quét đã dừng thay vì bắt đầu lại từ đầu.
- **Biến `[screen_fg_obj]` mới**: Đã thêm biến lời nhắc tùy chỉnh để chỉ chụp ảnh màn hình của cửa sổ nền trước đang hoạt động chứ không phải toàn bộ màn hình.
- **Thử lại thông minh & Xoay khóa**: Tiện ích bổ sung hiện thử lại âm thầm tối đa 5 lần trên cùng một khóa khi gặp tình trạng quá tải máy chủ tạm thời (chẳng hạn như "nhu cầu cao" hoặc phản hồi không đúng định dạng). Nếu thử lại không thành công, nó sẽ tự động chuyển sang khóa API tiếp theo trong danh sách của bạn.
- **Phát hiện màn hình**: Đã thêm tính năng kiểm tra để ngăn chụp ảnh màn hình khi Màn hình đang hoạt động (dù được bật vĩnh viễn hay chuyển đổi tạm thời bằng phím nóng). Nó sẽ cảnh báo bạn và dừng lại, ngăn bạn gửi hình ảnh màu đen và lãng phí mã thông báo API.
- **Tinh chỉnh trình đọc tài liệu**: Hộp thoại phạm vi PDF giờ đây tự động chọn trước ngôn ngữ đích mặc định từ cài đặt tiện ích bổ sung của bạn. Đồng thời cải thiện khả năng xử lý luồng để đảm bảo các tác vụ nền sẽ dừng hoàn toàn khi đóng trình đọc.
- **Tích hợp OCR gốc Mistral**: API OCR tài liệu gốc của Mistral được tích hợp. Các tài liệu nhiều trang được tự động hợp nhất, tải lên và xử lý theo lô bằng cách sử dụng điểm cuối `/v1/ocr` chuyên biệt của Mistral, trong khi hình ảnh một trang được xử lý trực tiếp mà không cần chuyển đổi PDF không cần thiết [1].
- **Trình xử lý URL tùy chỉnh động**: Việc sửa đổi URL API tùy chỉnh hiện sẽ xóa ngay lập tức danh sách mô hình được lưu trong bộ nhớ đệm và khôi phục hộp văn bản nhập mô hình thủ công. Điều này đảm bảo khả năng tương thích hoàn toàn với các điểm cuối tùy chỉnh (chẳng hạn như Cloudflare AI Gateway) không hỗ trợ điểm cuối danh sách `/v1/models` tiêu chuẩn.
- **Công cụ đầu vào của người vận hành AI được đại tu**: Viết lại hoàn toàn hệ thống mô phỏng chuột và bàn phím cơ bản cho Người vận hành AI. Đã thay thế API `mouse_event` cũ bằng API `SendInput` hiện đại của Windows, mang lại khả năng tương thích cao hơn đáng kể với các ứng dụng hiện đại, cửa sổ được bảo vệ bằng UAC và màn hình có độ phân giải cao.
- **Đã sửa lỗi thao tác kéo và thả**: Các thao tác kéo và thả trong Toán tử AI hiện hoàn toàn ổn định và đáng tin cậy. Công cụ mới sử dụng các đường cong "nới lỏng" tự nhiên, định vị con trỏ chính xác, thời gian được tối ưu hóa và kỹ thuật "nhích" thông minh để đảm bảo rằng Windows và các ứng dụng nhận dạng và thực hiện chính xác các cử chỉ kéo và thả mà không bị lỗi giữa chừng.
- **Hỗ trợ nhiều màn hình**: AI Operator hiện hỗ trợ đầy đủ các thiết lập nhiều màn hình. Chuyển động và nhấp chuột của chuột hoạt động chính xác trên tất cả các màn hình bằng cách sử dụng cờ `MOUSEEVENTF_VIRTUALDESK`, đảm bảo định vị chính xác bất kể ứng dụng mục tiêu đang bật màn hình nào.
- **Mô phỏng bàn phím nâng cao**: Tính năng nhập tổ hợp phím được cải tiến để hỗ trợ đầy đủ "Phím mở rộng" (chẳng hạn như các phím Mũi tên, Home, End, Page Up/Down, Insert, Delete và F1-F12). Điều này đảm bảo rằng các lệnh điều hướng và phím tắt do Người vận hành AI gửi hoạt động hoàn hảo trên tất cả các ứng dụng.
- **Hỗ trợ hình ảnh HEIC/HEIF**: Đã thêm hỗ trợ gốc cho các định dạng ảnh trên iPhone. Giờ đây, bạn có thể trực tiếp chọn các tệp `.heic` và `.heif` để mô tả AI, OCR hoặc Đọc tài liệu mà không cần chuyển đổi trước.

## Những thay đổi cho 6.5.0

- **Trợ lý trực tiếp**: Đã thêm tính năng trợ lý màn hình và giọng nói theo thời gian thực, chỉ dành riêng cho nhà cung cấp Google Gemini (hoặc nhà cung cấp tùy chỉnh tương thích với Gemini). Bao gồm tùy chỉnh chiều sâu suy nghĩ và giọng nói tương tác ngay bên trong hộp thoại, với khả năng tự động kết nối lại khi thay đổi cài đặt.
- **Nhà cung cấp AI MiniMax**: MiniMax tích hợp làm nhà cung cấp ngang hàng với sự hỗ trợ đa phương thức đầy đủ (trò chuyện, tầm nhìn, OCR), TTS tùy chỉnh sử dụng hơn 300 giọng nói động và tự động loại bỏ các khối lý luận (ví dụ: `suy nghĩ... phản hồi`) từ đầu ra.
- **Bản dịch của Trình xem Tài liệu**: Đã sửa lỗi dịch im lặng cho người dùng NVDA không nói tiếng Anh bằng cách đảm bảo mã ngôn ngữ 2 chữ cái tiêu chuẩn được gửi tới Google Dịch thay vì tên ngôn ngữ được bản địa hóa.
- **Thử lại quét hàng loạt PDF**: Đã triển khai logic thử lại im lặng, riêng biệt và được tối ưu hóa cao để quét hàng loạt tài liệu PDF nhằm ngăn tải lên dư thừa và tránh các cửa sổ bật lên lỗi gây gián đoạn trong quá trình thử lại.
- **Trạng thái trình xem tài liệu**: Đã khắc phục lỗi trong đó trạng thái tổng thể của plugin (được kiểm tra qua `I`) vẫn bị kẹt ở "Đã bắt đầu xử lý hàng loạt" trong quá trình quét tài liệu dài.
- **Đã giải quyết sự cố phân luồng**: Đã khắc phục lỗi `IsMain() nghiêm trọng trong sự cố xác nhận chuỗi wxTimerImpl` khi mở tài liệu từ chuỗi nền bằng cách chuyển hàng đợi gọi lại GUI sang `wx.CallAfter`.

## Những thay đổi cho phiên bản 6.1.2

- **Kiểm tra trước nhãn trùng lặp**: Đã khắc phục sự cố trong ghi nhãn đơn lẻ trong đó kiểm tra trùng lặp sử dụng các phím tọa độ cũ, khiến NVDA thực hiện các yêu cầu AI trùng lặp cho các đối tượng đã được gắn nhãn thay vì thông báo nhãn hiện có.
- **Trò chuyện tài liệu dành cho nhà cung cấp không phải Gemini**: Đã sửa lỗi kiểm tra khóa API nghiêm ngặt trong Trò chuyện tài liệu (`on_ask`) để đảm bảo rằng người dùng trên OpenAI, Groq hoặc nhà cung cấp Tùy chỉnh địa phương (như Ollama) có thể trò chuyện thành công với tài liệu mà không bị chặn.
- **Dịch Chrome OCR nhanh**: Đã khôi phục API dịch miễn phí, không cần khóa cho Chrome OCR. Dịch văn bản được trích xuất hiện bỏ qua Gemini AI, tiết kiệm hạn ngạch API và tăng tốc quá trình dịch.
- **Bộ lọc chữ và số CAPTCHA**: Đã sửa lỗi logic lọc trong bộ giải CAPTCHA để đảm bảo các ký tự không phải chữ và số được làm sạch đúng cách trong mọi tình huống.
- **Cập nhật trợ giúp lớp lệnh**: Đã sửa lối tắt thông báo trạng thái trong menu trợ giúp từ `L` thành `I` và thêm cả hai lệnh ghi nhãn (`L` và `Shift+L`) vào danh sách.

## Những thay đổi cho phiên bản 6.1.1

- **Sửa lỗi đầu ra tư duy Gemma 4**: Đã khắc phục sự cố với các mô hình Gemma 4 trong đó toàn bộ quá trình suy nghĩ bên trong được hiển thị dưới dạng phản hồi cuối cùng hoặc khi việc vô hiệu hóa suy nghĩ dẫn đến phản hồi trống. Tiện ích bổ sung hiện chỉ cách ly và trích xuất chính xác phản hồi văn bản rõ ràng cuối cùng.
- **OCR hàng loạt từ File Explorer**: Giờ đây, bạn có thể chọn nhiều ảnh hoặc tệp PDF trực tiếp trong Windows File Explorer và trích xuất văn bản hoặc phân tích chúng hàng loạt. Tiện ích bổ sung sẽ tự động lọc và chỉ xử lý các định dạng tệp được hỗ trợ.

## Những thay đổi cho 6.1.0

- **Tích hợp AI cục bộ toàn cầu (Thiết lập AI cục bộ)**: Đã thêm nút **"Thiết lập AI cục bộ"** mới trong Cài đặt nhà cung cấp tùy chỉnh. Giờ đây, người dùng có thể tự động định cấu hình các công cụ AI cục bộ, bao gồm **Ollama**, **LM Studio**, **Jan.ai** và **KoboldCPP** ngay lập tức.
- **Bỏ qua proxy cục bộ thông minh**: Xây dựng lại logic kết nối bằng cơ chế bỏ qua proxy nâng cao. Tiện ích bổ sung này hiện đủ thông minh để vượt qua hoàn toàn proxy hệ thống Windows cho các kết nối vòng lặp cục bộ, đảm bảo kết nối AI cục bộ ổn định ngay cả khi chế độ VPN/TUN của bạn đang hoạt động.
- **Ghi nhãn AI siêu ổn định (v2)**: Đã thay thế các phím tọa độ màn hình tuyệt đối bằng hệ thống **Chữ ký đối tượng** lai, tiên tiến. Các nhãn hiện dựa vào số nhận dạng có lập trình (UIA **AutomationId** hoặc Win32 **ControlID**) và tọa độ tương đối với cửa sổ, giúp các nhãn tùy chỉnh của bạn hoàn toàn chống lại việc thay đổi kích thước, di chuyển, chuyển đổi màn hình hoặc chia tỷ lệ cửa sổ.
- **Di chuyển nhãn tự động liền mạch**: Việc nâng cấp hoàn toàn minh bạch. Tiện ích bổ sung này sẽ tự động di chuyển các nhãn dựa trên tọa độ cũ của bạn sang định dạng dấu vân tay ổn định mới ở chế độ nền khi lấy nét lần đầu mà không bị mất dữ liệu.

## Những thay đổi cho 6.0

- **Giới thiệu tính năng gắn nhãn AI theo ngữ nghĩa**: Giờ đây, người dùng có thể gắn nhãn vĩnh viễn cho các nút và biểu tượng chưa được đặt tên bằng AI. Nhấn **L** để gắn nhãn cho đối tượng điều hướng hiện tại (hỗ trợ cả tiêu điểm Tab và điều hướng đối tượng) hoặc **Shift+L** để quét và gắn nhãn cho toàn bộ ứng dụng cùng một lúc.
- **Quản lý nhãn thông minh**: Đã thêm hộp thoại Trình quản lý nhãn mới, có thể truy cập đầy đủ (thông qua **Shift+L** nếu có nhãn) để xem, đổi tên hoặc xóa hàng loạt nhãn tùy chỉnh.
- **Phân tích tệp trực tiếp (Hộp thoại bỏ qua tệp)**: Tiện ích bổ sung hiện đủ thông minh để phát hiện xem bạn hiện có đang tập trung vào tệp PDF hoặc tệp hình ảnh trong Windows File Explorer hay không. Nhấn **F (Thao tác tệp thông minh)** hoặc **D (Trình đọc tài liệu)** trên tệp được đánh dấu sẽ xử lý tệp đó ngay lập tức, bỏ qua hoàn toàn hộp thoại "Mở" tiêu chuẩn.

## Những thay đổi trong phiên bản 5.6

- **Bổ sung Công cụ OCR "None (Lớp trích xuất văn bản)"**: Người dùng hiện có thể trích xuất văn bản trực tiếp từ các tệp PDF có thể tìm kiếm mà không cần sử dụng hạn ngạch AI, giúp cải thiện đáng kể tốc độ và tính riêng tư cho các tài liệu dạng văn bản.
- **Tinh chỉnh độ chính xác của UI Explorer**: Cải thiện prompt của UI Explorer để nhận diện tốt hơn các loại thành phần (như List Item) và báo cáo chính xác các trạng thái như "(Checked)", "(Selected)", hoặc "(Expanded)" trong khi bỏ qua các thành phần hệ thống của Windows như Thanh tác vụ và Đồng hồ.
- **Nhắc nhở thiết lập cài đặt**: Thêm một thông báo sau khi cài đặt để hướng dẫn người dùng đến menu cài đặt nhằm cấu hình khóa API và các tùy chọn cá nhân của họ.

## Những thay đổi trong phiên bản 5.5 (Bản cập nhật Tự động hóa)

- **AI Operator (Điều khiển tự động - Shift+A):** Đây là tính năng sáng giá nhất của v5.5. Vision Assistant Pro đã nâng cấp từ một trợ lý thụ động thành **AI Operator** cá nhân của bạn. Nó không chỉ mô tả màn hình mà còn thực sự nắm quyền điều khiển.
- **Trình thám hiểm giao diện (UI Explorer - E):** Bạn mệt mỏi vì phải điều hướng qua các "nút không nhãn"? Nhấn **E** để kích hoạt UI Explorer. AI sẽ quét toàn bộ cửa sổ và tạo danh sách mọi thành phần có thể click mà nó thấy—bao gồm cả icon, đồ họa và menu. Chỉ cần chọn một mục từ danh sách và AI Operator sẽ click giúp bạn. Nó giống như việc thêm một "lớp tiếp cận" lên trên bất kỳ ứng dụng nào.
- **Hành động tệp thông minh theo ngữ cảnh (F):** Phím "F" đã được đại tu hoàn toàn. Nó không còn mặc định là bạn chỉ muốn OCR nữa. Khi bạn chọn một hình ảnh, nó sẽ hỏi ý định của bạn: bạn có thể chọn **Mô tả hình ảnh chi tiết** để hiểu bối cảnh hoặc **Trích xuất văn bản có cấu trúc (OCR)** để đọc. Menu sẽ thay đổi linh hoạt dựa trên loại tệp và công cụ AI bạn đang dùng.

## Những thay đổi cho phiên bản 5.5 (Bản cập nhật tự động hóa)

- **Người vận hành AI (Điều khiển tự động - Shift+A):** Đây là viên ngọc quý của v5.5. Vision Assistant Pro đã chuyển từ vai trò trợ lý thụ động sang vai trò **Người vận hành AI** cá nhân của bạn. Nó không chỉ mô tả màn hình—nó còn ra lệnh.
  - _Cách thức hoạt động:_ Bây giờ bạn có thể đưa ra hướng dẫn bằng lời nói để vận hành PC của mình. Ví dụ: trong một ứng dụng hoàn toàn không thể truy cập được, trong đó trình đọc màn hình của bạn ở chế độ im lặng, bạn có thể nhấn **Shift+A** và nhập: _"Nhấp vào nút Cài đặt"_ hoặc _"Tìm trường tìm kiếm, nhập 'Tin tức mới nhất' và nhấn enter."_ AI xác định các phần tử một cách trực quan, di chuyển chuột và thực hiện tác vụ cho bạn.
  - _Ghi chú về hiệu suất:_ Tính năng này được tối ưu hóa cho **Gemini 3.0 Flash (Bản xem trước)**, mang lại phản hồi cực kỳ nhanh và thông minh, có thể xử lý ngay cả những bố cục giao diện người dùng phức tạp nhất.
  - **⚠️ Cảnh báo sử dụng API:** Vì Người vận hành AI cần "xem" chính xác những gì đang diễn ra để đảm bảo chính xác nên nó sẽ gửi ảnh chụp màn hình có độ phân giải cao theo từng bước. Xin lưu ý rằng việc sử dụng thường xuyên sẽ tiêu tốn hạn ngạch API của bạn nhanh hơn nhiều so với các tác vụ dựa trên văn bản tiêu chuẩn.
- **Visual UI Explorer (E):** Bạn cảm thấy mệt mỏi khi điều hướng qua "các nút không được gắn nhãn"? Nhấn **E** để kích hoạt UI Explorer. AI sẽ quét toàn bộ cửa sổ và tạo danh sách mọi thành phần có thể nhấp vào mà nó nhìn thấy—bao gồm các biểu tượng, đồ họa và menu. Chỉ cần chọn một mục từ danh sách và Người vận hành AI sẽ nhấp vào mục đó cho bạn. Nó giống như có một "lớp có thể truy cập" trên bất kỳ ứng dụng nào.
- **Hành động tệp thông minh nhận biết ngữ cảnh (F):** Phím "F" đã được đại tu hoàn toàn. Nó không còn cho rằng bạn chỉ muốn OCR nữa. Khi bạn chọn một hình ảnh, giờ đây nó sẽ hỏi ý định của bạn một cách thông minh: bạn có thể chọn **Mô tả hình ảnh chi tiết** để hiểu cảnh hoặc **Trích xuất văn bản có cấu trúc (OCR)** để đọc. Menu điều chỉnh linh hoạt dựa trên loại tệp và công cụ AI đang hoạt động của bạn.
- **Tối ưu hóa cốt lõi:** Chúng tôi đã thực hiện dọn dẹp sâu logic bên trong của tiện ích bổ sung, loại bỏ các hàm cũ không được sử dụng và mã dư thừa. Điều này mang lại trải nghiệm gọn gàng hơn, nhanh hơn và đáng tin cậy hơn cho tất cả người dùng.

## Những thay đổi trong phiên bản 5.0

- **Kiến trúc đa nhà cung cấp**: Bổ sung hỗ trợ đầy đủ cho **OpenAI**, **Groq**, và **Mistral** bên cạnh Google Gemini. Người dùng hiện có thể chọn backend AI ưa thích của mình.
- **Định tuyến mô hình nâng cao**: Người dùng các nhà cung cấp gốc (Gemini, OpenAI, v.v.) hiện có thể chọn các mô hình cụ thể từ danh sách thả xuống cho các tác vụ khác nhau (OCR, STT, TTS). giờ đây có thể chọn các kiểu máy cụ thể từ danh sách thả xuống cho các tác vụ khác nhau (OCR, STT, TTS).
- **Cấu hình Endpoint nâng cao**: Người dùng nhà cung cấp tùy chỉnh có thể nhập thủ công các URL và tên mô hình cụ thể để kiểm soát chi tiết các máy chủ cục bộ hoặc bên thứ ba.
- **Hiển thị tính năng thông minh**: Menu cài đặt và giao diện Trình đọc tài liệu giờ đây tự động ẩn các tính năng không được hỗ trợ (như TTS) dựa trên nhà cung cấp đã chọn.
- **Tìm nạp mô hình động**: Add-on hiện tìm nạp danh sách mô hình có sẵn trực tiếp từ API của nhà cung cấp, đảm bảo khả năng tương thích với các mô hình mới ngay khi chúng được phát hành.
- **Kết hợp OCR & Dịch thuật**: Tối ưu hóa logic để sử dụng Google Dịch nhằm tăng tốc độ khi dùng Chrome OCR, và dịch thuật bằng AI khi dùng các công cụ Gemini/Groq/OpenAI.
- **"Quét lại bằng AI" toàn cầu**: Tính năng quét lại của Trình đọc tài liệu không còn bị giới hạn ở Gemini. Giờ đây, tính năng này sử dụng bất kỳ nhà cung cấp AI nào đang hoạt động để xử lý lại các trang.

## Những thay đổi trong phiên bản 4.6

- **Gọi lại kết quả tương tác:** Đã thêm phím **Space** vào lớp lệnh, cho phép người dùng mở lại ngay lập tức phản hồi cuối cùng của AI trong cửa sổ trò chuyện để đặt câu hỏi tiếp theo, ngay cả khi chế độ "Đầu ra trực tiếp" đang hoạt động.
- **Cộng đồng Telegram:** Đã thêm liên kết "Kênh Telegram chính thức" vào menu Công cụ của NVDA, cung cấp một cách nhanh chóng để cập nhật những tin tức, tính năng và bản phát hành mới nhất.
- **Tăng cường độ ổn định của phản hồi:** Tối ưu hóa logic cốt lõi cho các tính năng Dịch thuật, OCR và Thị giác để đảm bảo hiệu suất đáng tin cậy hơn và trải nghiệm mượt mà hơn khi sử dụng đầu ra giọng nói trực tiếp.
- **Cải thiện hướng dẫn giao diện:** Đã cập nhật các mô tả cài đặt và tài liệu hướng dẫn để giải thích rõ hơn về hệ thống gọi lại mới và cách thức hoạt động của nó cùng với các cài đặt đầu ra trực tiếp.

## Những thay đổi trong phiên bản 4.5

- **Trình quản lý Prompt nâng cao:** Giới thiệu một hộp thoại quản lý chuyên dụng trong cài đặt để tùy chỉnh các prompt hệ thống mặc định và quản lý các prompt do người dùng xác định với hỗ trợ đầy đủ cho việc thêm, sửa, sắp xếp lại và xem trước.
- **Hỗ trợ Proxy toàn diện:** Đã giải quyết các sự cố kết nối mạng bằng cách đảm bảo rằng các cài đặt proxy do người dùng định cấu hình được áp dụng nghiêm ngặt cho tất cả các yêu cầu API, bao gồm dịch thuật, OCR và tạo giọng nói.
- **Di chuyển dữ liệu tự động:** Tích hợp hệ thống di chuyển thông minh để tự động nâng cấp các cấu hình prompt cũ sang định dạng v2 JSON mạnh mẽ trong lần chạy đầu tiên mà không làm mất dữ liệu.
- **Cập nhật khả năng tương thích (2025.1):** Đặt phiên bản NVDA yêu cầu tối thiểu thành 2025.1 do sự phụ thuộc thư viện trong các tính năng nâng cao như Trình đọc tài liệu để đảm bảo hiệu suất ổn định.
- **Tối ưu hóa giao diện cài đặt:** Sắp xếp hợp lý giao diện cài đặt bằng cách tổ chức lại việc quản lý prompt thành một hộp thoại riêng biệt, mang lại trải nghiệm người dùng rõ ràng và dễ tiếp cận hơn.
- **Hướng dẫn về biến Prompt:** Đã thêm hướng dẫn tích hợp trong các hộp thoại prompt để giúp người dùng dễ dàng xác định và sử dụng các biến động như `[selection]`, `[clipboard]`, và `[screen_obj]`.

## Những thay đổi trong phiên bản 4.0.3

- **Tăng cường độ ổn định mạng:** Đã thêm cơ chế thử lại tự động để xử lý tốt hơn các kết nối internet không ổn định và lỗi máy chủ tạm thời, đảm bảo phản hồi AI đáng tin cậy hơn.
- **Hộp thoại dịch trực quan:** Giới thiệu một cửa sổ dành riêng cho kết quả dịch. Người dùng giờ đây có thể dễ dàng điều hướng và đọc các bản dịch dài theo từng dòng, tương tự như kết quả OCR.
- **Chế độ xem định dạng tổng hợp:** Tính năng "View Formatted" trong Trình đọc tài liệu hiện hiển thị tất cả các trang đã xử lý trong một cửa sổ duy nhất, được tổ chức với các tiêu đề trang rõ ràng.
- **Tối ưu hóa quy trình OCR:** Tự động bỏ qua việc chọn phạm vi trang đối với các tài liệu chỉ có một trang, giúp quá trình nhận dạng diễn ra nhanh chóng và liền mạch hơn.
- **Cải thiện độ ổn định API:** Chuyển sang phương thức xác thực dựa trên header mạnh mẽ hơn, giải quyết các lỗi "All API Keys failed" tiềm ẩn do xung đột khi luân phiên khóa.
- **Sửa lỗi:** Đã giải quyết một số sự cố treo có thể xảy ra, bao gồm sự cố trong quá trình tắt add-on và lỗi tiêu điểm trong hộp thoại trò chuyện.

## Những thay đổi trong phiên bản 4.0.1

- **Trình đọc tài liệu nâng cao:** Một trình xem mới, mạnh mẽ dành cho PDF và hình ảnh với khả năng chọn phạm vi trang, xử lý nền và điều hướng liền mạch bằng `Ctrl+PageUp/Down`.
- **Menu con Tools mới:** Đã thêm một menu con "Vision Assistant" chuyên dụng bên dưới menu Tools của NVDA để truy cập nhanh hơn vào các tính năng cốt lõi, cài đặt và tài liệu hướng dẫn.
- **Tùy chỉnh linh hoạt:** Giờ đây, bạn có thể chọn công cụ OCR và giọng nói TTS ưa thích trực tiếp từ bảng cài đặt.
- **Hỗ trợ nhiều khóa API:** Đã thêm hỗ trợ cho nhiều khóa API Gemini. Bạn có thể nhập một khóa trên mỗi dòng hoặc phân tách chúng bằng dấu phẩy trong cài đặt.
- **Công cụ OCR thay thế:** Giới thiệu một công cụ OCR mới để đảm bảo nhận dạng văn bản đáng tin cậy ngay cả khi đạt đến giới hạn hạn ngạch của Gemini API.
- **Luân phiên Khóa API thông minh:** Tự động chuyển sang và ghi nhớ khóa API hoạt động nhanh nhất để vượt qua giới hạn hạn ngạch.
- **Tài liệu sang MP3/WAV:** Tích hợp khả năng tạo và lưu các tệp âm thanh chất lượng cao ở cả định dạng MP3 (128kbps) và WAV trực tiếp trong trình đọc.
- **Hỗ trợ Instagram Stories:** Đã thêm khả năng mô tả và phân tích Instagram Stories bằng URL của chúng.
- **Hỗ trợ TikTok:** Giới thiệu hỗ trợ cho các video TikTok, cho phép mô tả hình ảnh đầy đủ và chuyển biên âm thanh của các đoạn clip.
- **Hộp thoại cập nhật được thiết kế lại:** Cung cấp một giao diện mới, dễ tiếp cận với hộp văn bản có thể cuộn để đọc rõ các thay đổi của phiên bản trước khi cài đặt.
- **Trạng thái & UX thống nhất:** Chuẩn hóa các hộp thoại tệp trên toàn bộ add-on và cải tiến lệnh 'L' để báo cáo tiến trình theo thời gian thực.

## Những thay đổi trong phiên bản 3.6.0

- **Hệ thống trợ giúp:** Đã thêm lệnh trợ giúp (`H`) trong Lớp lệnh để cung cấp một danh sách dễ truy cập gồm tất cả các phím tắt và chức năng của chúng.
- **Phân tích Video trực tuyến:** Mở rộng hỗ trợ để bao gồm các video trên **Twitter (X)**. Đồng thời cải thiện khả năng phát hiện URL và độ ổn định để có trải nghiệm đáng tin cậy hơn.
- **Đóng góp cho dự án:** Đã thêm hộp thoại quyên góp tùy chọn cho những người dùng muốn ủng hộ các bản cập nhật trong tương lai và sự phát triển liên tục của dự án.

## Những thay đổi trong phiên bản 3.5.0

\* \*\*Lớp Lệnh:\*\* Giới thiệu hệ thống Lớp Lệnh (mặc định: `NVDA+Shift+V`) để nhóm các phím tắt dưới một phím chính duy nhất. Ví dụ, thay vì nhấn `NVDA+Control+Shift+T` để dịch, bây giờ bạn nhấn `NVDA+Shift+V` rồi nhấn `T`.
\* \*\*Phân tích video trực tuyến:\*\* Đã thêm tính năng mới để phân tích trực tiếp video trên YouTube và Instagram bằng cách cung cấp URL.

## Những thay đổi trong phiên bản 3.1.0

- **Chế độ Đầu ra trực tiếp:** Đã thêm tùy chọn để bỏ qua hộp thoại trò chuyện và nghe thẳng các phản hồi của AI qua giọng nói để có trải nghiệm nhanh chóng và liền mạch hơn.
- **Tích hợp Clipboard:** Đã thêm một cài đặt mới để tự động sao chép các phản hồi của AI vào clipboard.

## Những thay đổi trong phiên bản 3.0

- **Ngôn ngữ mới:** Đã thêm bản dịch tiếng **Ba Tư** và tiếng **Việt**.
- **Mở rộng mô hình AI:** Tổ chức lại danh sách chọn mô hình với các tiền tố rõ ràng (`[Free]`, `[Pro]`, `[Auto]`) để giúp người dùng phân biệt giữa các mô hình miễn phí và giới hạn tốc độ (trả phí). Đã thêm hỗ trợ cho **Gemini 3.0 Pro** và **Gemini 2.0 Flash Lite**.
- **Độ ổn định khi Đọc chính tả:** Cải thiện đáng kể độ ổn định của tính năng Đọc chính tả thông minh. Đã thêm kiểm tra an toàn để bỏ qua các đoạn âm thanh ngắn hơn 1 giây, ngăn chặn hiện tượng AI "ảo giác" và các lỗi trống.
- **Xử lý tệp:** Đã sửa lỗi tải lên các tệp có tên không phải tiếng Anh bị thất bại.
- **Tối ưu hóa Prompt:** Cải thiện logic Dịch thuật và cấu trúc lại kết quả của Thị giác.

## Những thay đổi trong phiên bản 2.9

- **Đã thêm bản dịch tiếng Pháp và tiếng Thổ Nhĩ Kỳ.**
- **Chế độ xem định dạng:** Đã thêm nút "View Formatted" trong các hộp thoại trò chuyện để xem cuộc hội thoại với định dạng chuẩn (Tiêu đề, In đậm, Code) trong một cửa sổ có thể duyệt qua tiêu chuẩn.
- **Cài đặt Markdown:** Đã thêm tùy chọn mới "Clean Markdown in Chat" trong phần Cài đặt. Bỏ chọn tùy chọn này cho phép người dùng xem cú pháp Markdown gốc (ví dụ: `**`, `#`) trong cửa sổ trò chuyện.
- **Quản lý hộp thoại:** Đã sửa sự cố trong đó cửa sổ "Refine Text" hoặc cửa sổ trò chuyện sẽ mở nhiều lần hoặc không lấy được tiêu điểm chính xác.
- **Cải tiến UX:** Chuẩn hóa các tiêu đề hộp thoại tệp thành "Open" và loại bỏ các thông báo giọng nói dư thừa (ví dụ: "Opening menu...") để có trải nghiệm mượt mà hơn. để có trải nghiệm mượt mà hơn.

## Những thay đổi trong phiên bản 2.8

- Đã thêm bản dịch tiếng Ý.
- **Thông báo trạng thái:** Đã thêm một lệnh mới (NVDA+Control+Shift+I) để thông báo trạng thái hiện tại của add-on (ví dụ: "Uploading...", "Analyzing...").
- **Xuất HTML:** Nút "Save Content" trong các hộp thoại kết quả hiện lưu đầu ra dưới dạng tệp HTML được định dạng, giữ nguyên các kiểu như tiêu đề và chữ in đậm.
- **Giao diện Cài đặt:** Cải thiện bố cục bảng Cài đặt với các nhóm dễ tiếp cận hơn.
- **Các mô hình mới:** Đã thêm hỗ trợ cho gemini-flash-latest và gemini-flash-lite-latest.
- **Ngôn ngữ:** Đã thêm tiếng Nepal vào các ngôn ngữ được hỗ trợ.
- **Logic menu Refine:** Đã sửa một lỗi nghiêm trọng khiến các lệnh "Refine Text" bị lỗi nếu ngôn ngữ giao diện NVDA không phải là tiếng Anh.
- **Đọc chính tả:** Cải thiện tính năng phát hiện khoảng lặng để ngăn chặn đầu ra văn bản không chính xác khi không có giọng nói được nhập vào.
- **Cài đặt cập nhật:** Tính năng "Check for updates on startup" hiện bị tắt theo mặc định để tuân thủ các chính sách của Add-on Store.
- Dọn dẹp mã nguồn.

## Những thay đổi trong phiên bản 2.7

- Chuyển đổi cấu trúc dự án sang Mẫu Add-on chính thức của NV Access để tuân thủ các tiêu chuẩn tốt hơn.
- Đã triển khai logic thử lại tự động cho các lỗi HTTP 429 (Rate Limit) để đảm bảo độ tin cậy trong thời gian lưu lượng truy cập cao.
- Tối ưu hóa các prompt dịch thuật để có độ chính xác cao hơn và xử lý logic "Smart Swap" tốt hơn.
- Đã cập nhật bản dịch tiếng Nga.

## Những thay đổi trong phiên bản 2.6

- Đã thêm hỗ trợ bản dịch tiếng Nga (Cảm ơn nvda-ru).
- Cập nhật các thông báo lỗi để cung cấp phản hồi mang tính mô tả cao hơn về vấn đề kết nối.
- Thay đổi ngôn ngữ đích mặc định thành tiếng Anh.

## Những thay đổi trong phiên bản 2.5

- Đã thêm lệnh Native File OCR (NVDA+Control+Shift+F).
- Đã thêm nút "Save Chat" vào các hộp thoại kết quả.
- Đã triển khai hỗ trợ bản địa hóa đầy đủ (i18n).
- Đã chuyển các phản hồi âm thanh sang mô-đun tones gốc của NVDA.
- Chuyển sang sử dụng Gemini File API để xử lý tốt hơn các tệp PDF và âm thanh.
- Đã sửa lỗi treo khi dịch văn bản có chứa dấu ngoặc nhọn.

## Những thay đổi trong phiên bản 2.1

- Chuẩn hóa tất cả các phím tắt để sử dụng NVDA+Control+Shift nhằm loại bỏ xung đột với bố cục Bàn phím Laptop của NVDA và các phím nóng hệ thống.

## Những thay đổi cho phiên bản 2.1

- Chuẩn hóa tất cả các phím tắt để sử dụng NVDA+Control+Shift nhằm loại bỏ xung đột với bố cục Laptop của NVDA và các phím nóng hệ thống.

## Những thay đổi trong phiên bản 2.0

- Đã triển khai hệ thống Tự động cập nhật tích hợp sẵn.
- Đã thêm Bộ nhớ đệm Dịch thông minh để truy xuất tức thì các văn bản đã dịch trước đó.
- Đã thêm Bộ nhớ hội thoại để tinh chỉnh kết quả theo ngữ cảnh trong các hộp thoại trò chuyện.
- Đã thêm Lệnh dịch Clipboard chuyên dụng (NVDA+Control+Shift+Y).
- Tối ưu hóa các prompt AI để thực thi nghiêm ngặt đầu ra ngôn ngữ đích.
- Đã sửa lỗi treo do các ký tự đặc biệt trong văn bản đầu vào.

## Những thay đổi trong phiên bản 1.5

- Đã thêm hỗ trợ cho hơn 20 ngôn ngữ mới.
- Đã triển khai Hộp thoại Tinh chỉnh Tương tác cho các câu hỏi tiếp theo.
- Đã thêm tính năng Đọc chính tả thông minh gốc.
- Đã thêm danh mục "Vision Assistant" vào hộp thoại Input Gestures của NVDA.
- Đã sửa các lỗi treo COMError trong một số ứng dụng cụ thể như Firefox và Word.
- Đã thêm cơ chế tự động thử lại đối với các lỗi máy chủ.

## Những thay đổi trong phiên bản 1.0

- Phát hành lần đầu.
