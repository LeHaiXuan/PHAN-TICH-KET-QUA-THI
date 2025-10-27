# Ứng dụng Phân tích Điểm thi THPT

Một ứng dụng **Streamlit** giúp phân tích kết quả thi của học sinh theo **kỳ thi**, **môn học**, **lớp** và **tổ chuyên môn**; hỗ trợ **so sánh giữa các kỳ thi** và **xuất báo cáo PDF**.

## Tính năng
- 📊 Tổng quan điểm theo bộ lọc (kỳ thi, lớp, môn, tổ chuyên môn)
- 🔁 So sánh giữa hai kỳ thi: chênh lệch trung bình theo môn/lớp/tổ
- 🧩 Thống kê theo tổ chuyên môn: trung bình, trung vị, phân phối điểm
- 🖨️ Xuất báo cáo PDF (nhiều trang) gồm bảng số liệu và biểu đồ
- 🗂️ Dùng **file mẫu** hoặc **tải lên dữ liệu của trường** (CSV/Excel)

## Cấu trúc dữ liệu
File dữ liệu cần các cột:
```
StudentID, HoTen, Lop, Mon, ToChuyenMon, KyThi, Diem
```
> Xem file mẫu: `data/samples/sample_scores.csv`

## Chạy trên máy tính (Windows/macOS/Linux)
1. Cài **Python 3.10+** từ https://www.python.org/downloads/
2. Mở Terminal/Command Prompt tại thư mục dự án.
3. (Khuyến nghị) Tạo môi trường ảo:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate   # Windows
   ```
4. Cài thư viện:
   ```bash
   pip install -r requirements.txt
   ```
5. Chạy ứng dụng:
   ```bash
   streamlit run app.py
   ```
6. Trình duyệt sẽ mở tại `http://localhost:8501`

## Triển khai trực tuyến (đề xuất Render/Hugging Face Spaces)
- **Render.com** (dịch vụ web miễn phí ở mức cơ bản): đọc `scripts/deploy_render.md`
- **Hugging Face Spaces**: chọn template **Streamlit**, kéo thả mã nguồn.
- **GitHub Codespaces**: chạy trực tiếp trong trình duyệt (để demo nội bộ).

## Thay dữ liệu bằng dữ liệu thật của trường
- Chuẩn hóa cột như phần *Cấu trúc dữ liệu*.
- Xuất dữ liệu Excel từ phần mềm hiện có, dùng **Power Query**/**pandas** để đổi tên cột nếu cần.
- Sau đó vào ứng dụng và **Upload** file.

## Giấy phép
MIT License – tự do sử dụng, chỉnh sửa, triển khai.

--
*Được chuẩn bị cho THPT Lê Quý Đôn - Long Bình Tân.*
