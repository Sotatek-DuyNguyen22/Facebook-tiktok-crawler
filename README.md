# Facebook & TikTok Audio Crawler

## Mục tiêu

Mục tiêu của project là xây dựng và hoàn thiện một pipeline thu thập dữ liệu
speech tiếng Việt từ Facebook và TikTok theo các keywords được assign.

Sau khi hoàn thành project, mỗi thành viên cần đạt được các mục tiêu sau:

1. Tìm kiếm và thu thập video/reel có nội dung tiếng Việt liên quan đến
   keywords được giao.
2. Download và chuyển đổi audio về cùng một định dạng chuẩn:

   ```text
   Format:      WAV
   Sample rate: 16 kHz (16.000 Hz)
   Channels:    1 (mono)
   ```

3. Bảo đảm dữ liệu có speech rõ ràng, tự nhiên, ít noise và không có music hoặc
   nhạc nền.
4. Loại bỏ video/audio trùng lặp, kể cả khi một nội dung được tìm thấy từ nhiều
   keywords khác nhau.
5. Lưu metadata và mapping để mỗi file audio có thể truy ngược về keyword và
   link video/reel/audio gốc.
6. Xây dựng cơ chế xử lý lỗi và tiếp tục crawl khi chương trình bị gián đoạn,
   thay vì phải chạy lại từ đầu.
7. Hỗ trợ download song song có kiểm soát mà không làm hỏng metadata hoặc trạng
   thái của pipeline.
8. Hoàn thành tối thiểu **500 giờ dữ liệu hợp lệ/người trong 7 tuần**.
9. Viết tài liệu mô tả giải pháp, các bước post-processing và lý do lựa chọn
   từng phương pháp làm sạch audio.

Kết quả cuối cùng không chỉ là các file audio đã download, mà phải là một bộ dữ
liệu speech tiếng Việt sạch, đúng format, không trùng lặp và có đầy đủ thông tin
nguồn gốc.

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

## III./ Yêu cầu về sản lượng và chất lượng dữ liệu

### 1./ Mục tiêu và tiến độ

| Yêu cầu | Chỉ tiêu |
|---|---:|
| Tổng số lượng dữ liệu cần crawl | **500 giờ/người** |
| Thời gian hoàn thành | **7 tuần** |
| Trung bình mỗi tuần | Khoảng **72 giờ/tuần** |
| Trung bình mỗi ngày | Khoảng **15 giờ/ngày** nếu làm việc 5 ngày/tuần |

500 giờ trong 7 tuần tương đương khoảng 71,4 giờ mỗi tuần. Vì vậy, mục tiêu
thực tế được làm tròn thành 72 giờ/tuần, tương đương khoảng 14,4–15 giờ/ngày
nếu tính theo 5 ngày làm việc mỗi tuần.

### 2./ Yêu cầu về nội dung

- Nội dung audio phải là **tiếng Việt**.
- Ưu tiên speech rõ ràng, tự nhiên và dễ nghe.
- Không lấy video chỉ có music hoặc speech bị lẫn nhạc nền.
- Hạn chế audio có quá nhiều noise, speech bị rè, nhỏ hoặc không rõ.
- Audio sau khi xử lý phải phù hợp để sử dụng làm speech dataset.

### 3./ Yêu cầu về tính duy nhất và nguồn dữ liệu

- Không crawl trùng video hoặc trùng audio.
- Mỗi audio phải có mapping tới link nguồn ban đầu.
- Link nguồn có thể là video, reel hoặc audio gốc.
- Thông tin mapping phải đủ để truy ngược từ file audio về nội dung nguồn.

### 4./ Yêu cầu về keyword

- Phải crawl đúng theo keywords được assign.
- Nếu sử dụng keyword khác, vẫn phải ưu tiên audio có speech tiếng Việt rõ
  ràng, tự nhiên và không có nhạc nền.
- Cần lưu lại keyword đã dùng để tìm thấy từng audio.

### 5./ Checklist kiểm tra dữ liệu

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
