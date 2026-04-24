# HƯỚNG DẪN SỬ DỤNG MB BANK BALANCE ALERT

## 📁 Cấu trúc thư mục (Trong `dist/MB_Bank_Alert`)
*   `MB_Bank_Alert.exe`: File chạy chính.
*   `.env`: File chứa thông tin cấu hình (Bạn cần tạo từ file mẫu).
*   `.env.example`:  **[File mẫu tham khảo trên GitHub](https://github.com/hoafd/Loa_MBB/blob/main/.env.example)**.
*   `_internal/`: Thư mục chứa thư viện hệ thống và dữ liệu mã hóa (Không được xóa).

---

## 🚀 Các bước cài đặt và sử dụng

### Bước 1: Triển khai
1. Copy toàn bộ thư mục `MB_Bank_Alert` sang máy tính hoặc VPS bạn muốn chạy.

### Bước 2: Cấu hình thông tin
1. Tạo file `.env` (Nếu chưa có, hãy copy từ `.env.example` và đổi tên).
2. Mở file `.env` bằng Notepad và điền thông số theo **một trong hai cách**:
   *   **Cách 1 (Nhanh nhất)**: Dán thẳng link Feed vào biến `ADAFRUIT_URL`.
       *   Ví dụ: `ADAFRUIT_URL=https://io.adafruit.com/api/v2/your_user/feeds/your-feed-name`
   *   **Cách 2 (Thủ công)**: Điền `ADAFRUIT_IO_USERNAME` và `FEED_NAME` riêng biệt.
3. **Bắt buộc**: Điền `ADAFRUIT_IO_KEY` (Lấy từ biểu tượng chìa khóa trên Adafruit IO).
4. Lưu file lại.

### Bước 3: Khởi chạy và "Đóng gói" (Bake)
1. Click đúp vào file `MB_Bank_Alert.exe` để chạy.
2. **Trong lần chạy đầu tiên**:
   *   Chương trình sẽ đọc file `.env`, tự động truy vấn mã phần cứng (UUID) của máy.
   *   Mã hóa toàn bộ thông tin và lưu vào hệ thống.
   *   **Tự động xóa file .env** và thay thế bằng file mẫu trắng để bảo mật.

---

## 📱 Cấu hình Máy gửi (Android)
Hệ thống hiện tại đã được tối ưu cực kỳ đơn giản. Bạn chỉ cần gửi duy nhất **Số tiền** lên Cloud.

### Bước 1: Chuẩn bị trên điện thoại
1. **Bật thông báo MB Bank**: Mở App MB Bank -> Tiện ích -> Cài đặt thông báo -> Bật biến động số dư qua App.
2. **Cấp quyền cho MacroDroid**: Vào Cài đặt điện thoại -> Truy cập thông báo -> Cho phép MacroDroid.

### Bước 2: Thiết lập MacroDroid
1. Tải ứng dụng **MacroDroid** trên Play Store.

2. Chọn 1 trong 2 phương án sau (cả 2 đều là như nhau):
   * **Phương án a**: Tải file **[Loa_MBB.macro](https://github.com/hoafd/Loa_MBB/releases/download/Loa_MBB/Loa_MBB.macro)** về điện thoại.
     Mở MacroDroid -> **Trang chủ** -> **Xuất/Nhập** -> **Nhập Bộ nhớ** -> Chọn file vừa tải.

   * **Phương án b**: Tìm mẫu `Loa_MBB` trong kho MacroDroid.

3. Nhấp vào mục **Biến cục bộ** (dưới cùng của màn hình chính), sau đó nhấp vào các giá trị của 3 biến có biểu tượng **ổ khóa** 🔒 để thay đổi chúng.
   *   `api`: Link API Feed của Adafruit IO. ( Lấy link ở mục Feed trong Adafruit IO)
   *   `X-AIO-Key`: Active Key của bạn. ( lấy key ở mục chìa khóa trong Adafruit IO)
   *   `stk-MB`: 3 số cuối của số tài khoản MB Bank cần theo dõi.

---

## 📝 Cấu trúc Log & Giọng đọc
*   **Trên màn hình**: Sẽ tự động hiện `[2024/04/24 12:54:22] + 1.000.000 VND`
*   **Ra loa**: Sẽ đọc *"Bạn vừa nhận Một triệu đồng"*

---

## 🛠 Thay đổi cấu hình
Nếu bạn muốn thay đổi tài khoản hoặc Key:
1. Tạo lại file `.env` cạnh file EXE.
2. Điền thông tin mới vào và chạy lại EXE. Nó sẽ tự động cập nhật bản mã hóa mới.

## 🔒 Lưu ý bảo mật
*   Nếu bạn mang thư mục này sang máy tính khác, chương trình **sẽ không chạy được** vì dữ liệu đã bị khóa vào phần cứng máy tính.
*   Tuyệt đối không xóa thư mục `_internal` vì đó là nơi chứa dữ liệu đã mã hóa của bạn.
