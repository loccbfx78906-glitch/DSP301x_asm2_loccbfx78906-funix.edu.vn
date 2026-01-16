# Grade The Exams (Hệ Thống Chấm Điểm Thi Trắc Nghiệm)

Một chương trình Python mạnh mẽ giúp tự động hóa quy trình chấm điểm thi trắc nghiệm từ các tệp dữ liệu lớp học, thực hiện thống kê điểm số và phân tích độ khó của từng câu hỏi.

## Tính năng chính

- **Xử lý File:**
  - Tìm kiếm và mở file dữ liệu lớp học (`.txt`) theo tên nhập vào.
  - Sử dụng Regex để kiểm tra tính hợp lệ của tên lớp và dữ liệu bên trong.

- **Làm sạch dữ liệu:**
  - Tự động lọc các dòng dữ liệu lỗi (sai định dạng Mã số sinh viên `Nxxxxxxxx` hoặc thừa/thiếu câu trả lời).
  - Báo cáo chi tiết từng dòng lỗi để giáo viên kiểm tra.

- **Chấm điểm tự động:**
  - Hệ thống chấm điểm theo quy chế:
    - **Đúng:** +4 điểm
    - **Sai:** -1 điểm
    - **Bỏ trống:** 0 điểm

- **Thống kê & Phân tích:**
  - Tính điểm cao nhất, thấp nhất, trung bình, trung vị của cả lớp.
  - Đếm số lượng học sinh đạt điểm giỏi (>80).
  - **Phân tích câu hỏi:** Tự động phát hiện các câu hỏi "khó" (có số lượng người làm sai nhiều nhất) và các câu hỏi bị bỏ qua nhiều nhất.
  - Sử dụng thư viện **Pandas** & **NumPy** để tối ưu hóa tốc độ xử lý.

## Yêu cầu hệ thống

Để chạy được chương trình, máy tính cần cài đặt Python và các thư viện sau:

- Python 3.9
- Pandas
- NumPy

## Tác giả
**[Cao Bá Lộc]**

* **GitHub:** https://github.com/loccbfx78906-glitch
* **Email:** loccbfx78906@funix.edu.vn