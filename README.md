# Dữ liệu khóa học Coursera:

## Cách sử dụng:

Cài đặt thư viện `pip install -r requirements.lib`

Copy file `.env copy` thành file `.env`

Cấu hình crawl bot:

- `RAW_URL_FILE`: Tên thư mục chứa các url của khóa học vừa thu thập nếu cơ sở dữ liệu chưa có url nào
- `MAX_PAGE`: Số lượng trang tối đa ở danh sách muốn thu thập url của khóa học
- `NON_CRAWL_FILE`: Tên thư mục chứa các url của khóa học CHƯA thu thập dữ liệu
- `CRAWLED_FILE`: Tên thư mục chứa các url của khóa học ĐÃ thu thập dữ liệu
- `ERROR_FILE`: Tên thư mục chứa các url của khóa học LỖI khi thu thập dữ liệu
- `MAX_CRAWL_TIME`: Số lượng khóa học tối đa thu thập dữ liệu trong mỗi lần chạy
- `USE_CHROME`: Tùy chọn sử dụng CHROME hoặc FIREFOX (YES/NO)
- `CHROMEDRIVER_PATH`: Đường dẫn Chromedriver nếu sử dụng CHROME và phiên bản khác `118.0.5993.118`. Download tại <a href="https://chromedriver.chromium.org/downloads"/>ĐÂY</a>
- `USER_CHROME_DIR`: Lấy dữ liệu người dùng Chrome tại `chrome://version/` > `Profile path`
- `TIMEOUT`: Nhập bao nhiêu thì bot sẽ crawl chậm hơn bấy nhiêu lần nếu mạng lag
- `MONGODB_DATABASE_URI`: URI của server mongodb
- `MONGODB_DATABASE_NAME`: Tên của Database bạn muốn lưu trữ trong mongo

Chạy file `main.py` và chờ đợi

## Cơ sở dữ liệu:

- Tiêu đề khóa học: title
- Lĩnh vực: category
- Ảnh của đơn vị đào tạo: organi_image
- Tên của đơn vị đào tạo: organi_name
- Xếp hạng khóa học: average_rating
- Số lượng đánh giá: review_count
- Mức độ của khóa học: difficulty
- Số lượng người đã đăng ký khóa học: students_enrolled
- Thời gian học: study_time
- Kỹ năng đạt được: gain_skills
- Ngôn ngữ giảng dạy: language
