# Triển khai lên Render.com (Streamlit)

## Chuẩn bị
1. Tạo repository trên GitHub, ví dụ: `thpt-phan-tich-diem-thi`.
2. Đưa toàn bộ mã nguồn dự án này lên repository.

## Tạo dịch vụ Web Service trên Render
1. Đăng nhập https://render.com và liên kết với GitHub.
2. Chọn **New +** → **Web Service** → chọn repository vừa tạo.
3. **Environment**: `Python`
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `streamlit run app.py --server.port $PORT --server.headless true`
6. Nhấn **Create Web Service** và chờ Render dựng ứng dụng.

Sau khi xong, Render sẽ cấp một URL công khai để truy cập.

## Lưu ý
- Gói miễn phí có thể ngủ sau một thời gian không truy cập.
- Nếu cần chạy ổn định, cân nhắc gói trả phí hoặc các nền tảng khác (Hugging Face Spaces, Deta Space).
