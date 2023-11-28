# Dữ liệu khóa học Udemy:

#### Người thực hiện:
- Trần Lý Bửu - HUET - <a href="https://github.com/tranlybuu"/>GITHUB</a>
- Lê Văn Tân - HUET - <a href="https://github.com/levantanfc11"/>GITHUB</a>

## Yêu cầu

- Python phiên bản 3.11 trở xuống (<=3.11)
- Cài đặt Cơ sở dữ liệu MongoDB để lưu trữ dữ liệu

## Cách cài đặt môi trường:

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
- `TIMEOUT`: Nhập bao nhiêu thì bot sẽ crawl chậm hơn bấy nhiêu lần nếu mạng lag. Mặc định là 4
- `MONGODB_DATABASE_URI`: URI của server mongodb
- `MONGODB_DATABASE_NAME`: Tên của Database bạn muốn lưu trữ trong mongo
- `NUMBER_OF_CRAWL_MACHINE`: Số thứ tự máy đang crawl bắt đầu từ 1 (Ví dụ bạn có 3 máy thì giá trị này ở 3 máy sẽ lần lượt là 1, 2, 3). Mặc định là 1

## Cách sử dụng Crawl Bot:

#### Nếu trong database của bạn CHƯA có dữ liệu các đường dẫn khóa học của Udemy hoặc database của bạn chưa có dữ liệu nào:

- Mở Terminal ở thư mục hiện tại (CMD/Powershell với Windows và Terminal với MacOS/Linux => `cd <đường_dẫn_thư_mục_hiện_tại>`) 
- Chạy `Python run_crawl_url.py` để thu thập các đường dẫn khóa học (Nếu bạn có nhiều máy tính thì có thể chia đều Object trong biến `crawl_category_url` để crawl nhanh hơn)
- Bước này sẽ mất khoảng 30 tiếng nếu bạn sử dụng 1 máy để chạy
- Sau khi hoàn thành thu thập đường dẫn khóa học, bạn có thể tiếp tục thu thập dữ liệu chi tiết các khóa học ở bước tiếp theo

#### Nếu trong cơ sở dữ liệu của bạn ĐÃ có dữ liệu các đường dẫn khóa học của Udemy:
- Mở Terminal ở thư mục hiện tại (CMD/Powershell với Windows và Terminal với MacOS/Linux => `cd <đường_dẫn_thư_mục_hiện_tại>`) 
- Chạy `Python main.py` để thu thập các đường dẫn khóa học (Nếu bạn có nhiều máy tính thì có thể sử dụng biến `NUMBER_OF_CRAWL_MACHINE` trong `.env` để crawl nhanh hơn)
- Bước này sẽ mất khá nhiều thời gian nếu bạn sử dụng chỉ 1 máy để chạy. Trung bình 1 khóa học sẽ tốn khoảng 8 giây để thu thập tất cả dữ liệu

## Cơ sở dữ liệu:

- Title: Tên khóa học
- best_seller: 
- price: giá khóa học
- category: Lĩnh vực khóa học
- skill: Kỹ năng
- gain_exp_list: Kết quả học được
- describe: Mô tả khóa học
- students_enrolled: Số lượng người đã đăng ký khóa học
- study_time: Thời gian học
- language: Ngôn ngữ khóa học
- average_rating: Xếp hạng khóa học
- review_count: Số lượng đánh giá
- url_id: ID của đường dẫn khóa học
- organi: Danh sách giáo viên
- organi > teacher_name: Tên giáo viên
- organi > teacher_job: nghề nghiệp giáo viên
- organi > teacher_image: Đường dẫn ảnh giáo viên
- organi > teacher_count_student: tổng số học sinh của giáo viên
- organi > teacher_count_course: tổng số khóa học của giáo viên
