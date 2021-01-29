# Code Judge Simulator
A simple offline code judge program written in python

## Cú pháp
```
python test_tool.py [python_file] [test_foler] <time_limit> <-v>
```
- ```python_file```: File python cần test
- ```test_folder```: Đường dẫn tới folder chứa test cases
- ```time_limit```: Thời gian chạy tối đa cho mỗi test
- ```-v```: Thêm tùy chọn này vào cuối dòng lệnh để hiển thị thêm các thông tin sau: 
    - Output gốc (trong test case)
    - Output của user (kết quả in ra màn hình của python_file)
    - Chiều dạng đoạn text output gốc ```len(correct_output)```
    - Chiều dài đoạn text output user ```len(user_output)```
    - Thời gian ```python_file``` chạy trên mỗi test case

*Lưu ý*:
- Thông số trong ngoặc ```[]``` là bắt buộc phải có
- Thông số trong ngoặc ```<>``` là tùy chọn

**Ví dụ**

*Căn bản*

![basic syntax](https://i.imgur.com/fQXWDgw.gif)

*```-v```*

![-v](https://i.imgur.com/MBBKoNH.gif)

*```time_limit```*

![time_limit](https://i.imgur.com/MQy1cq4.gif)

*```time_limit -v```*

![time_limit -v](https://i.imgur.com/LPnF0dl.gif)

## Cách tạo test cases
- Tạo một folder tên là ```inp``` để chứa tất cả input
- Tạo một folder tên là ```out``` để chứa tất cả output
- Mỗi test case trong thư mục ```inp``` và ```out``` được lưu riêng trong từng file khác nhau
- Đặt tên của mỗi test case là số thứ tự của test case đó. Ví dụ file chứ test case 1 sẽ có tên là ```1```
- Thứ tự test case bắt đầu từ 1
