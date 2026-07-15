# ==============================================================================
# PHẦN 1: PHÂN TÍCH VÀ ĐỀ XUẤT ĐA GIẢI PHÁP CẤU HÌNH
# 
# 6.1. Phân tích truy xuất quan hệ:
#   1. Vai trò và vị trí của Khóa ngoại:
#      - Vai trò: Thiết lập ràng buộc toàn vẹn tham chiếu, liên kết các dòng của 
#        bảng trung gian với hai bảng chính để xác định cặp đối tượng có quan hệ.
#      - Vị trí: Bắt buộc đặt ở bảng trung gian "Enrollment" (student_id và course_id).
#      - Tại sao: CSDL quan hệ không thể lưu trực tiếp quan hệ N-N trên hai bảng gốc,
#        mà phải tách thành hai quan hệ 1-N qua bảng trung gian. Khóa ngoại luôn 
#        nằm ở bảng phía phần tử "Nhiều" (Enrollment).
#   2. Bản chất của tham số back_populates:
#      - Không bắt buộc phải trùng với tên bảng trong CSDL.
#      - Bản chất: Dùng để chỉ định tên của thuộc tính quan hệ (relationship) 
#        được định nghĩa ở Model đối ứng nhằm đồng bộ trạng thái hai chiều trên 
#        các đối tượng Python khi có thay đổi.
#
# 6.2. Đề xuất hai giải pháp cấu hình Model:
#   - Giải pháp 1 (Trực tiếp qua secondary): Cấu hình relationship trực tiếp giữa 
#     Student và Course bằng cách chỉ định bảng trung gian Enrollment qua tham số secondary.
#   - Giải pháp 2 (Gián tiếp qua hai quan hệ 1-N): Không dùng tham số secondary. 
#     Thiết lập quan hệ 1-N độc lập từ Student -> Enrollment và Course -> Enrollment. 
#     Phải dùng vòng lặp qua Enrollment để lọc dữ liệu đối ứng.
#
# ==============================================================================
# PHẦN 2: SO SÁNH VÀ LỰA CHỌN CẤU HÌNH
#
# 6.3. Bảng so sánh:
#   - Tiêu chí 1: Độ ngắn gọn và tinh giản của code
#     + Giải pháp 1: Rất ngắn gọn, cấu hình một lần và sử dụng trực tiếp.
#     + Giai phập 2: Dài dòng hơn, phải viết code xử lý lọc trung gian.
#   - Tiêu chí 2: Cách truy xuất danh sách sinh viên từ đối tượng Course
#     + Giải pháp 1: Gọi trực tiếp qua thuộc tính: course.students.
#     + Giải pháp 2: Phải thông qua bảng trung gian và duyệt vòng lặp để thu thập đối tượng.
#   - Tiêu chí 3: Độ phức tạp khi cần đọc hiểu cấu trúc code đối với người mới
#     + Giải pháp 1: Dễ hiểu ở mức độ sử dụng, che giấu được sự phức tạp của SQL.
#     + Giải pháp 2: Trực quan về mặt vật lý nhưng phức tạp khi viết code lấy dữ liệu.
#
#   * Trả lời câu hỏi phân tích:
#     - Giải pháp giúp viết code ngắn gọn hơn khi truy xuất: Giải pháp 1.
#     - Giải pháp được khuyến khích sử dụng trong slide: Giải pháp 1 (dùng secondary).
#
# 6.4. Lựa chọn giải pháp:
#   - Giải pháp lựa chọn: Giải pháp 1 (Sử dụng tham số secondary).
#   - Lý do kỹ thuật: Tối ưu hóa mã nguồn, cho phép truy cập trực tiếp danh sách 
#     thực thể đối ứng (course.students) trả về một list thực thể mong muốn mà 
#     không cần lập thủ công, giúp code sạch và tận dụng tốt cơ chế tối ưu truy vấn của SQLAlchemy ORM.
#
# ==============================================================================
# PHẦN 3: THIẾT KẾ VÀ TRIỂN KHAI SOURCE CODE MODEL
#
# 6.5. Thiết kế các bước thực hiện:
#   - Bước 1: Import các module và components cần thiết từ sqlalchemy.
#   - Bước 2: Khởi tạo đối tượng Base từ declarative_base().
#   - Bước 3: Định nghĩa Model Enrollment (Bảng trung gian) với các khóa ngoại.
#   - Bước 4: Định nghĩa Model Student, cấu hình relationship với secondary="enrollments".
#   - Bước 5: Định nghĩa Model Course, cấu hình relationship ngược lại với Student.
# ==============================================================================

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Enrollment(Base):
    __tablename__ = 'enrollments'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id', ondelete="CASCADE"), nullable=False)


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    courses = relationship("Course", secondary="enrollments", back_populates="students")


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    students = relationship("Student", secondary="enrollments", back_populates="courses")
