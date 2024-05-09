## IricsDo

# Bài tập lớn môn Xử Lý Ngôn Ngữ Tự Nhiên

***Giáo viên: Phan Thị Tươi***

***Học kỳ: 2***

***Năm học: 2023 - 2024***

### Thông tin cá nhân

***Họ tên học viên: Đỗ Duy***

***Mã số học viên: 2270512***

### Chú thích bài nộp

Chú thích dựa theo tệp hướng dẫn làm BTL của giáo viên hướng dẫn.

## Thư viện cần cài đặt
1. os (built-in library)
2. [re](https://pypi.org/project/regex/)
3. copy (built-in library)
4. [pandas](https://pypi.org/project/pandas/)

## Chứa 3 thư mục

input: Gồm 2 file

- **query.txt** : Chứa 21 câu hỏi, được đánh số từ 1 đến 21 theo thứ tự trong phần hướng dẫn BTL.

- **data.xlsx** : Chứa dữ liệu các môn học, gồm có 5 cột và 20 hàng.

output: Gồm 5 thư mục con

- **Thư mục parsing_dependency_grammar** : tương ứng chứa phần trả lời cho câu hỏi *2.2.a* trong phần hướng dẫn BTL. Bao gồm 21 tệp định dạng xlsx được đánh số từ 1 đến 21 tương ứng với 21 câu hỏi trong tệp query.txt

- **Thư mục grammatical_relations** : tương ứng chứa phần trả lời cho câu hỏi *2.2.b* và *2.2.c*. Cũng bao gồm 21 tệp định dạng xlsx được đánh số từ 1 đến 21 tương ứng với 21 câu hỏi trong tệp query.txt

- **Thư mục logical_form** : tương ứng chứa phần trả lời cho câu hỏi *2.2.d*. Cũng bao gồm 21 tệp định dạng txt được đánh số từ 1 đến 21 tương ứng với 21 câu hỏi trong tệp query.txt

- **Thư mục procedural_semantics** : tương ứng chứa phần trả lời cho câu hỏi *2.2.e*. Cũng bao gồm 21 tệp định dạng txt được đánh số từ 1 đến 21 tương ứng với 21 câu hỏi trong tệp query.txt

- **Thư mục answer_question** : tương ứng chứa phần trả lời cho câu hỏi *2.2.f*. Cũng bao gồm 21 tệp định dạng txt được đánh số từ 1 đến 21 tương ứng với 21 câu hỏi trong tệp query.txt

modles: Gồm 3 tệp mã

- **action_parsing_dependcy_grammar.py** : Chứa các hàm dùng cho việc trả lời câu hỏi *2.2.a*

- **make_folder.py**: Chứa hàm tạo ra các thư mục con lưu kết quả trả lời ở thư mục output

- **npl.py** : Chứa toàn bộ lớp, hàm và các đoạn mã liên quan phục vụ cho việc trả lời tất cả các câu hỏi trong BTL. Đây cũng là tệp chính của toàn bộ phần mã.
Các hàm trong tệp action_parsing_dependcy_grammar.py
sẽ được gọi ở lớp này.

## Chứa 2 tệp

- **main.py** : Tệp chính để chạy chương trình. Tệp này gồm 2 phần chính:

    - Một là tạo thư mục lưu kết quả (gọi đến hàm tạo thư mục trong tệp make_folder.py). 
    
    - Hai là khởi tạo lớp chứa trong file nlp.py. 

    Chi tiết

    - Đầu tiên hàm đọc tệp query.txt sẽ được gọi để đọc tất cả câu hỏi và lưu vào danh sách. 

    - Sau đó dùng một vòng lặp duyệt hết tất cả phần tử trong danh sách này để trả lời cho từng câu hỏi.

    - Từng câu hỏi sẽ được tiền xử lý trước (loại bỏ những từ, dấu không cần thiết). Rồi thực hiện trả lời cho từng câu hỏi ở mục 2.2 trong phần hướng dẫn BTL. 

    - Khi đoạn mã đến cuối vòng lặp, tức là các câu hỏi đã được xử lý xong và lưu vào các thư mục con tương ứng ở output. Sau đó, đoạn mã tiếp tục duyệt đến câu hỏi tiếp theo, cứ như vậy cho hết danh sách các câu hỏi.

- **README.md** : Chính là tệp này, dùng để chú thích các thành phần trong phần bài làm

### ***Ghi chú: Bài nộp này em sẽ xóa hết tất cả tệp ở thư mục output, chỉ để thư mục rỗng. Sau khi thực thi đoạn mã ở tệp main.py. Các thư mục con và câu trả lời tương ứng với từng câu hỏi sẽ xuất hiện.***