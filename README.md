# 🔔 Loa MB Bank — Thông báo số dư ngân hàng bằng giọng nói tiếng Việt

Ứng dụng Windows tự động **đọc to số tiền** khi có giao dịch MB Bank, sử dụng:
- 📡 **Adafruit IO** — Nhận dữ liệu realtime qua MQTT.
- 🎙️ **Microsoft Edge Neural TTS** — Giọng Việt chuẩn, không cần cài thêm.
- 📱 **MacroDroid (Android)** — Tự động bắt thông báo và đẩy lên Cloud.
- 🔐 **Hardware-Binding** — Cơ chế bảo mật khóa cấu hình vào phần cứng máy tính.

---

## 📋 Yêu cầu hệ thống
- **Điện thoại**: Android đã cài sẵn **App MB Bank** (đã bật thông báo biến động số dư).
- **Máy tính**: Windows 10/11 (để chạy ứng dụng Loa thông báo).
- **Tài khoản**: Adafruit IO (Miễn phí).

---

## 🛠 Chuẩn bị (Rất quan trọng)
1. **Bật thông báo MB Bank**:
   - Mở App MB Bank -> **Tiện ích** -> **Cài đặt thông báo** -> **Thông báo biến động số dư**.
   - Hãy chắc chắn mục **Thông báo qua App** đã được bật (Gạt sang màu xanh).
2. **Cấp quyền cho MacroDroid**:
   - Tải app MacroDroid trên CH Play.
   - Vào **Cài đặt** của điện thoại -> Tìm mục **Truy cập thông báo** (Notification Access).
   - Tìm ứng dụng **MacroDroid** trong danh sách và gạt nút **Cho phép**. (Đây là quyền bắt buộc để ứng dụng đọc được **Thông báo biến động số dư**.)

---

## 📋 Luồng hoạt động

`Điện thoại (MacroDroid)` ➡️ `Adafruit IO Cloud` ➡️ `Máy tính (MB_Bank_Alert)` ➡️ `🔊 Loa`

---

## 🚀 Hướng dẫn cài đặt

Dự án chia làm 2 phần chính: **Máy gửi (Điện thoại)** và **Máy nhận (Máy tính)**.

### 1. Cấu hình Máy gửi (Điện thoại Android)

1. Tải ứng dụng **MacroDroid** trên Play Store.

2. Chọn 1 trong 2 phương án sau:
   * **Phương án a**: Tải file **[Loa_MBB.macro](https://github.com/hoafd/Loa_MBB/releases/download/Loa_MBB/Loa_MBB.macro)** về điện thoại.
     Mở MacroDroid -> **Trang chủ** -> **Xuất/Nhập** -> **Nhập Bộ nhớ** -> Chọn file vừa tải.

   * **Phương án b**: Tìm mẫu `Loa_MBB` trong kho MacroDroid.

3. Nhấp vào mục **Biến cục bộ** (dưới cùng của màn hình chính), sau đó nhấp vào các giá trị của 3 biến có biểu tượng **ổ khóa** 🔒 để thay đổi chúng.
   *   `api`: Link API Feed của Adafruit IO. ( Lấy link ở mục Feed trong Adafruit IO)
   *   `X-AIO-Key`: Active Key của bạn. ( lấy key ở mục chìa khóa trong Adafruit IO)
   *   `stk-MB`: 3 số cuối của số tài khoản MB Bank cần theo dõi.

### 2. Cấu hình Máy nhận (Máy tính Windows)

#### Bước 1 — Tải mã nguồn
```bash
git clone https://github.com/hoafd/Loa_MBB.git && cd Loa_MBB
```

#### Bước 2 — Build tự động (Ultimate Build Tool)
Bạn chỉ cần chạy duy nhất file sau:
```bash
build_exe.bat
```
*Script sẽ tự động cài đặt Python 3.12.10 (nếu thiếu), tạo môi trường ảo, cài thư viện và đóng gói thành file Zip.*

#### Bước 3 — Cấu hình và Chạy
- Giải nén file Zip thu được, điền thông tin vào file `.env` cạnh file EXE.
- Chạy `MB_Bank_Alert.exe`. Chương trình sẽ tự động mã hóa thông tin và xóa file `.env` để bảo mật.

---

## 🔐 Cơ chế bảo mật (Security)
Dự án tích hợp cơ chế **Capture & Bake**:
- **Mã hóa phần cứng**: Cấu hình được mã hóa dựa trên UUID duy nhất của máy tính bạn. Nếu bị đánh cắp, dữ liệu cũng không thể giải mã trên máy khác.
- **Tự động dọn dẹp**: Ngay sau khi đọc cấu hình từ `.env`, chương trình sẽ "nướng" nó vào bản mã và xóa file `.env` gốc để tránh lộ mật khẩu.

---

## 📂 Cấu trúc thư mục
- `termux/`: Chứa mã nguồn và hướng dẫn dành cho điện thoại Android.
- `mb_bank_alert.py`: Mã nguồn chính chạy trên Windows.
- `config_utils.py`: Bộ quản lý cấu hình và mã hóa bảo mật.
- `build_exe.bat`: Công cụ đóng gói tự động (Auto-Python, Auto-Zip).
- `.env.example`: File cấu hình mẫu.

---

## 🎙️ Tùy chỉnh giọng đọc
Mở file `.env` (hoặc cấu hình trước khi build) để thay đổi:
- `vi-VN-HoaiMyNeural`: Giọng nữ miền Nam (Mặc định).
- `vi-VN-NamMinhNeural`: Giọng nam miền Bắc.

---

## 📄 Giấy phép
MIT License — Tự do sử dụng và phát triển.
