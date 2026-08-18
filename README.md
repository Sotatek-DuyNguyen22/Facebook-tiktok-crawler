# Facebook & TikTok Audio Crawler

## I./ Các công cụ sử dụng

Đây là một số công cụ chung dùng để tìm kiếm keywords và download các audio:

- [Thư viện yt-dlp](https://github.com/yt-dlp/yt-dlp): dùng để download audio
  từ các nguồn khác nhau.
- [FFmpeg](https://ffmpeg.org/): dùng cho việc xử lý audio, ví dụ chuyển các
  audio về cùng một định dạng và sample rate. Đầu ra yêu cầu có định dạng WAV,
  sample rate 16 kHz (16.000 Hz) và một channel (mono).
- [ffprobe](https://ffmpeg.org/ffprobe.html): dùng để kiểm tra và xác nhận file
  audio có đúng định dạng yêu cầu hay không.

## II./ Các bước cần thiết

1. Set up công cụ dùng để tìm kiếm keywords.
2. Tìm kiếm các video/audio liên quan.
3. Download audio bằng `yt-dlp`.
4. Chuyển audio về định dạng yêu cầu bằng FFmpeg và xác nhận lại audio bằng
   ffprobe.
5. Export data theo đúng định dạng file JSON được yêu cầu trong phần Format
   data.

## III./ Các vấn đề cần giải quyết

Code baseline chỉ cung cấp các chức năng cơ bản. Các bạn cần giải quyết những
vấn đề sau:

### 1./ Loại bỏ audio trùng lặp

Đối với các audio có ID bị lặp, cần phải lọc và loại bỏ audio trùng. Đặc biệt
cần xử lý vấn đề này khi sử dụng nhiều keywords.

### 2./ Tiếp tục download khi chương trình bị dừng

Nếu quá trình bị dừng giữa chừng, cần có cơ chế fallback để tiếp tục download
từ audio đang xử lý, thay vì phải làm lại từ đầu.

Có thể thiết lập cơ chế lưu trữ riêng các audio bị lỗi, sau đó thử download lại
các audio đó trong lần chạy tiếp theo.

### 3./ Bảo đảm định dạng audio đầu ra

Cần bảo đảm tất cả audio đầu ra có:

```text
Format:      WAV
Sample rate: 16 kHz (16.000 Hz)
Channels:    1 (mono)
```

### 4./ Xử lý audio có music

Cần xử lý các audio bị lẫn music hoặc chỉ có music, để bảo đảm dữ liệu cuối
cùng phù hợp với yêu cầu sử dụng.

### 5./ Download song song có kiểm soát

Download tuần tự có thể chậm khi số lượng video lớn. Tuy nhiên, gửi quá nhiều
request đồng thời có thể gây rate limit hoặc checkpoint tài khoản.

- Mỗi worker phải xử lý lỗi độc lập.
- Một video lỗi không được làm dừng toàn bộ chương trình.
- Việc ghi metadata và trạng thái phải an toàn khi nhiều worker cùng hoạt động.

### 6./ Export dữ liệu đúng format

Đầu ra của các audio sau khi xử lý cần phải tuân theo đúng định dạng được mô tả
trong phần Format data.

### 7./ Xử lý giới hạn truy cập

Cần xử lý các vấn đề về cookies, IP và các giới hạn truy cập khác để tránh bị
Facebook hoặc TikTok restrict access trong quá trình download audio.

Việc xử lý phải tuân thủ điều khoản sử dụng của nền tảng và chính sách mạng của
đơn vị.

### 8./ Viết tài liệu báo cáo

Ngoài data và báo cáo được yêu cầu, cần có một document mô tả:

- Cách nhóm xử lý từng vấn đề được liệt kê bên trên.
- Các bước post-processing được sử dụng để xử lý audio.
- Các bước lọc audio để bảo đảm audio sạch.
- Lý do lựa chọn từng bước lọc và post-processing.
