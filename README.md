# Facebook & TikTok Audio Crawler

## Đề bài

### Crawl dữ liệu từ Facebook và TikTok

Mỗi bạn sẽ được assign từ **1–2 keywords** để crawl dữ liệu từ **Facebook
Reels** hoặc **TikTok**.

### Yêu cầu

| Hạng mục | Yêu cầu |
|---|---:|
| Tổng số lượng dữ liệu cần crawl | **500 giờ/người** |
| Thời gian hoàn thành | **7 tuần** |
| Trung bình mỗi tuần | Khoảng **72 giờ/tuần** |
| Trung bình mỗi ngày | Khoảng **15 giờ/ngày** |

Yêu cầu đối với dữ liệu:

- Nội dung phải là **tiếng Việt**.
- Ưu tiên nội dung có speech rõ ràng, tự nhiên.
- Không lấy video chỉ có music hoặc speech bị lẫn nhạc nền.
- Hạn chế video có quá nhiều noise hoặc speech không rõ.
- Không crawl trùng video hoặc trùng audio.
- Mỗi audio phải có mapping tới link video, reel hoặc audio gốc.
- Phải crawl đúng theo keywords được assign.
- Nếu sử dụng keyword khác, audio vẫn phải có speech rõ ràng, tự nhiên và không
  có nhạc nền.

## Mục tiêu

Mục tiêu của project là xây dựng và hoàn thiện một pipeline thu thập dữ liệu
speech tiếng Việt từ Facebook và TikTok.

Sau khi hoàn thành project, mỗi thành viên cần:

1. Biết cách tìm kiếm video/reel theo keyword và download audio từ nội dung
   nguồn.
2. Chuẩn hóa toàn bộ audio về WAV, 16 kHz, mono.
3. Xây dựng cơ chế phát hiện dữ liệu trùng, xử lý lỗi và tiếp tục crawl khi
   chương trình bị gián đoạn.
4. Xử lý song song có kiểm soát và bảo đảm metadata được ghi an toàn.
5. Đánh giá và làm sạch audio để loại bỏ music, noise và speech không rõ.
6. Lưu metadata để truy ngược mỗi file audio về keyword và link nguồn gốc.
7. Export dữ liệu đúng Format data được yêu cầu.
8. Viết tài liệu mô tả giải pháp và các bước post-processing audio.

Kết quả cuối cùng phải là một bộ dữ liệu speech tiếng Việt sạch, đúng format,
không trùng lặp và có đầy đủ thông tin nguồn gốc.

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

## III./ Checklist kiểm tra dữ liệu

Trước khi tính một audio vào tổng số giờ hoàn thành, cần kiểm tra:

- [ ] Audio có nội dung tiếng Việt.
- [ ] Speech rõ ràng và tự nhiên.
- [ ] Không có music hoặc nhạc nền.
- [ ] Noise ở mức chấp nhận được.
- [ ] Không trùng video/audio đã thu thập.
- [ ] Có link nguồn gốc.
- [ ] Có mapping với keyword tìm kiếm.
- [ ] File đúng định dạng WAV, 16 kHz, mono.

## IV./ Các vấn đề cần giải quyết

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
