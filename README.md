# Bot Clicker Google Search Automation

Một ứng dụng sử dụng PyQt5 kết hợp với xử lý ảnh và điều khiển chuột/bàn phím để tự động hóa thao tác tìm kiếm trên Google.

## 🧠 Chức năng chính

1. **Tự động tìm và double click vào icon Google trên desktop.**
2. **Click vào thanh tìm kiếm của Google.**
3. **Nhập từ khóa tìm kiếm và nhấn Enter.**
4. **Tìm kết quả theo từ khóa cụ thể và click vào.**
5. **Hỗ trợ cuộn trang và chuyển sang trang tiếp theo nếu không tìm thấy kết quả.**
6. **Giao diện PyQt5 thân thiện, dễ sử dụng.**

---

## 📷 Giao diện người dùng

- **SEARCH_QUERY**: Nhập từ khóa bạn muốn tìm trên Google.
- **Keywords**: Nhập từ khóa bạn muốn chương trình tìm và click trong trang kết quả.
- **Run**: Bắt đầu chu trình tự động.
- **Stop**: Dừng chu trình sau khi hoàn thành chu kỳ hiện tại.
- **Số chu trình đã chạy**: Theo dõi số lần chương trình đã hoàn thành chu kỳ tìm kiếm.

---

## 🛠️ Cài đặt môi trường (Anaconda)

### 1. Tạo môi trường từ file `environment.yml`:

```bash
conda env create -f environment.yml
```

### 2. Kích hoạt môi trường:

```bash
conda activate bot-clicker
```

### 3. Cài thêm thư viện `docTR` (Document Text Recognition):

```bash
pip install "doctr[torch]"
```

> **Lưu ý**: Bạn cần Python ≥ 3.7 và có thể sẽ cần cài thêm PyTorch nếu chưa có. Nếu bạn dùng GPU, hãy cài PyTorch phù hợp tại: https://pytorch.org/get-started/locally/

---

## 🚀 Chạy chương trình

```bash
python main.py
```

---

## 📁 Cấu trúc thư mục

```
project/
│
├── assets/                    # Chứa các template như icon Google
├── src/
│   ├── program.py             # Chứa lớp Programn với logic tự động
│   ├── template_matcher.py    # Phát hiện template bằng OpenCV
│   ├── search_key_ocr.py      # Nhận dạng từ khóa bằng OCR (tùy chọn docTR)
│   ├── keyboard_controller.py # Gõ từ khóa, nhấn phím
│   ├── mouse_controller.py    # Điều khiển chuột
│
├── main.py                    # Giao diện người dùng (PyQt5)
├── environment.yml            # File thiết lập môi trường Conda
└── README.md                  # Tài liệu này
```

---

## 🔧 Yêu cầu hệ thống

- **OS**: Windows
- **Python**: >=3.7
- **Anaconda**: Khuyên dùng
- **Màn hình**: Phải có màn hình chính (primary screen)

---

## ⚠️ Lưu ý

- Kiểm tra và đảm bảo template ảnh (`google_icon.JPG`) đúng với màn hình của bạn.
- Một số hàm yêu cầu chạy trong môi trường có giao diện (GUI).
- Không dùng trên nhiều màn hình nếu chưa xử lý `region` phù hợp.

---

## 📬 Liên hệ

Nếu bạn cần hỗ trợ hoặc muốn đóng góp:

- Email: quanglvhust@gmail.com
- GitHub: [github.com/quanglv1996](https://github.com/quanglv1996)

---

Chúc bạn sử dụng vui vẻ!