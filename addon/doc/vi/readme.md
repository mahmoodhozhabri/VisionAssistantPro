Tài liệu hướng dẫn Vision Assistant Pro

# Vision Assistant Pro

**Vision Assistant Pro** là trợ lý AI đa phương thức tiên tiến dành cho NVDA. Nó tận dụng các mô hình Gemini của Google để cung cấp khả năng đọc, dịch, đọc chính tả bằng giọng nói và phân tích tài liệu thông minh trên màn hình.

_Tiện ích bổ sung này được phát hành ra cộng đồng để vinh danh Ngày Quốc tế Người khuyết tật._

## 1. Cài đặt & Cấu hình

đi đến **NVDA Menu > Preferences > Settings > Vision Assistant Pro**.

- **API Key:** Yêu cầu. Nhận khóa miễn phí từ [Google AI Studio](https://aistudio.google.com/).
- **Mô hình:** Chọn `gemini-2.5-flash-lite` (Nhanh nhất) hoặc các mẫu Flash tiêu chuẩn.
- **Ngôn ngữ:** Đặt ngôn ngữ Nguồn, đích và Phản hồi AI.
- **Chuyển đổi thông minh:** Tự động hoán đổi ngôn ngữ nếu văn bản nguồn khớp với ngôn ngữ đích.

## 2. Phím tắt chung

Để đảm bảo khả năng tương thích tối đa với bố cục máy tính xách tay, tất cả các phím tắt đều sử dụng **NVDA + Control + Shift**.

| phím tắt                    | chức năng             | mô tả                                                                 |
|-----------------------------|----------------------|-----------------------------------------------------------------------------|
| NVDA+Ctrl+Shift+T           | trình dịch thông minh     | Dịch văn bản dưới con trỏ điều hướng. Ưu tiên lựa chọn.      |
| NVDA+Ctrl+Shift+Y           | Dịch từ bộ nhớ | dịch nội dng trong bộ nhớ. **khuyên dùng cho trình duyệt web**.            |
| NVDA+Ctrl+Shift+S           | Đọc chính tả thông minh       | Chuyển đổi lời nói thành văn bản. Nhấn một lần để bắt đầu, một lần nữa để dừng và gõ.       |
| NVDA+Ctrl+Shift+R           | Tinh chỉnh văn bản         | Tóm tắt, sửa lỗi ngữ pháp, giải thích hoặc chạy **Prompts Tùy chỉnh**.                 |
| NVDA+Ctrl+Shift+C           | Giải CAPTCHA        | Tự động chụp và giải CAPTCHA.                                 |
| NVDA+Ctrl+Shift+V           | nhìn đối tượng        | Mô tả đối tượng điều hướng với cuộc trò chuyện tiếp theo.                         |
| NVDA+Ctrl+Shift+O           | nhìn toàn màn hình    | Phân tích toàn bộ bố cục và nội dung màn hình.                                  |
| NVDA+Ctrl+Shift+D           | Hỏi đáp tài liệu     | Trò chuyện với PDF/TXT/MD/PY files.                                              |
| NVDA+Ctrl+Shift+F           | File OCR             | OCR trực tiếp từ image/PDF file.                                             |
| NVDA+Ctrl+Shift+A           |Phiên âm âm thanh    | phiên âm MP3/WAV/OGG files.                                               |
| NVDA+Ctrl+Shift+L           | bản dịch cuối cùng     | đọc-lại bản dịch cuối cùng không có API.                                      |
| NVDA+Ctrl+Shift+U           | kiểm tra cập nhật         | Kiểm tra GitHub cho phiên bản mới nhất.                                            |
| NVDA+Ctrl+Shift+I           | Đọc trạng thái     | Thông báo tình trạng hiện tại (e.g., "Đang tải lên...", "Idle").                |

## 3. tùy chỉnh Prompts & biến

tạo lệnh trong cài đặt: `Name:Prompt Text` (tách biệt với `|` hoặc dòng mới).

### Biến có sẵn

| biến         | Mô tả                                      | Nhập đầu vào       |
|------------------|--------------------------------------------------|------------------|
| `[selection]`    | Currently selected text                          | Text             |
| `[clipboard]`    | Clipboard content                                | Text             |
| `[screen_obj]`   | Screenshot of navigator object                   | Image            |
| `[screen_full]`  | Full screen screenshot                           | Image            |
| `[file_ocr]`     | Select image/PDF/TIFF (defaults to "Extract text")| Image, PDF, TIFF |
| `[file_read]`    | Select text document                             | TXT, Code, PDF   |
| `[file_audio]`   | Select audio file                                | MP3, WAV, OGG    |

### Ví dụ Prompts tùy chỉnh

- **Quick OCR:** `My OCR:[file_ocr]`
- **Translate Image:** `Translate Img:Extract text from this image and translate to Persian. [file_ocr]`
- **Analyze Audio:** `Summarize Audio:Listen to this recording and summarize the main points. [file_audio]`
- **Code Debugger:** `Debug:Find bugs in this code and explain them: [selection]`

**Lưu ý:** File tải lên giới hạn đến 15MB. yêu cầu internet. Nhiều-trang TIFFs hỗ trợ.

## Thay đổi cho phiên bản 2.9

*   **Đã thêm bản dịch tiếng Pháp và tiếng Thổ Nhĩ Kỳ.**
*   **Chế độ xem định dạng:** Đã thêm nút "Xem định dạng" trong hộp thoại trò chuyện để xem cuộc trò chuyện có định dạng phù hợp (tiêu đề, định dạng, mã) trong cửa sổ có thể duyệt tiêu chuẩn.
*   **Cài đặt Markdown:** Đã thêm tùy chọn mới "Làm sạch makdownr trong trò chuyện" trong Cài đặt. Việc bỏ chọn tùy chọn này sẽ cho phép người dùng xem cú pháp Markdown thô (ví dụ: `**`, `#`) trong cửa sổ trò chuyện.
*   **Quản lý hộp thoại:** Đã khắc phục sự cố trong đó "Tinh chỉnh văn bản" hoặc cửa sổ trò chuyện mở nhiều lần hoặc không lấy nét chính xác.
*   **Cải tiến UX:** Tiêu đề hộp thoại tệp được tiêu chuẩn hóa thành "Mở" và loại bỏ các thông báo bằng giọng nói dư thừa (ví dụ: "Mở menu...") để có trải nghiệm mượt mà hơn.

## Thay đổi cho 2.8

* Đã thêm bản dịch tiếng Ý.
*   **Báo cáo trạng thái:** Đã thêm lệnh mới (NVDA+Control+Shift+I) để thông báo trạng thái hiện tại của tiện ích bổ sung (ví dụ: "Đang tải lên...", "Phân tích...").
*   **Xuất HTML:** Nút "Lưu nội dung" trong hộp thoại kết quả hiện lưu kết quả đầu ra dưới dạng tệp HTML được định dạng, giữ nguyên các kiểu như tiêu đề và văn bản in đậm.
*   **Giao diện người dùng cài đặt:** Cải thiện bố cục bảng Cài đặt với khả năng phân nhóm có thể truy cập được.
*   **Mẫu mới:** Đã thêm hỗ trợ cho gemini-flash-mới nhất và gemini-flash-lite-mới nhất.
*   **Ngôn ngữ:** Đã thêm tiếng Nepal vào các ngôn ngữ được hỗ trợ.
*   **Tinh chỉnh logic menu:** Đã sửa lỗi nghiêm trọng khiến lệnh "Tinh chỉnh văn bản" không thành công nếu ngôn ngữ giao diện NVDA không phải là tiếng Anh.
*   **Đọc chính tả:** Cải thiện tính năng phát hiện khoảng lặng để ngăn văn bản xuất ra không chính xác khi không có giọng nói nào được nhập vào.
*   **Cài đặt cập nhật:** "Kiểm tra các bản cập nhật khi khởi động" hiện bị tắt theo mặc định để tuân thủ các chính sách của Cửa hàng tiện ích bổ sung.
* Dọn dẹp mã.

## Thay đổi cho 2.7

* Đã di chuyển cấu trúc dự án sang Mẫu tiện ích bổ sung NV Access chính thức để tuân thủ các tiêu chuẩn tốt hơn.
* Triển khai logic thử lại tự động đối với các lỗi HTTP 429 (Giới hạn tốc độ) để đảm bảo độ tin cậy khi lưu lượng truy cập cao.
* Lời nhắc dịch được tối ưu hóa để có độ chính xác cao hơn và xử lý logic "Hoán đổi thông minh" tốt hơn.
* Cập nhật bản dịch tiếng Nga.

## Thay đổi cho 2.6

* Đã thêm hỗ trợ dịch tiếng Nga (Cảm ơn nvda-ru).
* Đã cập nhật thông báo lỗi để cung cấp phản hồi mang tính mô tả hơn về khả năng kết nối.
* Đã thay đổi ngôn ngữ mục tiêu mặc định sang tiếng Anh.

## Thay đổi cho 2.5

* Đã thêm Lệnh OCR tệp gốc (NVDA+Control+Shift+F).
* Đã thêm nút "Lưu trò chuyện" vào hộp thoại kết quả.
* Đã triển khai hỗ trợ bản địa hóa đầy đủ (i18n).
* Chuyển phản hồi âm thanh sang mô-đun âm gốc của NVDA.
* Đã chuyển sang API tệp Gemini để xử lý tốt hơn các tệp PDF và âm thanh.
* Đã sửa lỗi sự cố khi dịch văn bản có dấu ngoặc nhọn.

## Thay đổi cho 2.1.1

* Đã khắc phục sự cố trong đó biến [file ocr] không hoạt động chính xác trong Lời nhắc Tùy chỉnh.

## Thay đổi cho 2.1

* Chuẩn hóa tất cả các phím tắt để sử dụng NVDA+Control+Shift nhằm loại bỏ xung đột với bố cục Laptop của NVDA và các phím nóng hệ thống.

## Thay đổi cho 2.0

* Triển khai hệ thống Tự động cập nhật tích hợp.
* Đã thêm Bộ đệm dịch thuật thông minh để truy xuất ngay văn bản đã dịch trước đó.
* Đã thêm Bộ nhớ hội thoại để tinh chỉnh kết quả theo ngữ cảnh trong hộp thoại trò chuyện.
* Thêm lệnh dịch từ Clipboard (NVDA+Control+Shift+Y).
* Lời nhắc AI được tối ưu hóa để thực thi nghiêm ngặt đầu ra ngôn ngữ đích.
* Đã sửa lỗi sự cố do các ký tự đặc biệt trong văn bản đầu vào.

## Thay đổi cho 1.5

* Đã thêm hỗ trợ cho hơn 20 ngôn ngữ mới.
* Đã triển khai Hộp thoại Tinh chỉnh Tương tác cho các câu hỏi tiếp theo.
* Đã thêm tính năng Đọc chính tả thông minh gốc.
* Đã thêm danh mục "Trợ lý thị giác" vào hộp thoại Cử chỉ nhập liệu của NVDA.
* Đã sửa lỗi COMError gặp sự cố trong các ứng dụng cụ thể như Firefox và Word.
* Đã thêm cơ chế thử lại tự động cho các lỗi máy chủ.

## Thay đổi cho 1.0

* Phát hành lần đầu.
