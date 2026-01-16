from pathlib import Path # thư viện xử lý đường dẫn file, folder lưu trữ
import re # regex xử lý điều kiện mã số, nhập tên file
import numpy as np # xử lý list sang array, tính trung vị
import pandas as pd # xử lý thống kê câu hỏi bị bỏ xót, trả lời sai

# Icon trang trí cho đẹp
icon_right = "👍"
icon_wrong = "🤦"
icon_exit = "🔌"
icon_analyzing = "💻"

# Xác định các folder để lưu file và truy cập dữ liệu
repo_folder = Path(__file__).parent
data_folder = repo_folder / "data_exam" # dữ liệu điểm các lớp
result_folder = repo_folder / "results" # kết quả điểm học sinh sau khi chấm

# tạo vòng lặp xử lý nhập file
while True: 
    # xử lý ngoại lệ trong khối try-except 
    try:
        class_name = input(f"Nhập tên lớp cần tra cứu điểm(nếu muốn thoát hãy nhập 'thoát'):").lower().strip()
        pattern = r"^[a-z0-9]*$" # chỉ nhận chứ và số, không viết cách, không có khoảng trắng
        # tạo lệnh thoát chương trình
        if class_name == "thoát":
            print(f"{icon_exit} Đã thoát chương trình")
            break
        elif class_name == "":
            print(f"{icon_wrong} Không được bỏ trống dòng này, vui lòng nhập tên lớp")
            continue
        # loại trừ ký tự đặc biệt/nguy hiểm/...
        elif not re.match(pattern, class_name):
            print(f"{icon_wrong} Tên lớp chứa ký tự không hợp lệ, không viết cách, chỉ được chứa chữ và số")
            print("Vui lòng nhập lại tên lớp")
            continue
        # mở file khi thỏa điều kiện
        else:
            file_name = data_folder/f"{class_name}.txt"
            # nếu file tồn tại thì mở file
            if file_name.exists():
                print(f"{icon_right} Đã mở file đáp án của lớp {class_name} thành công\n......................")
                # mở file
                with open(file_name, "r+", encoding="utf-8") as f:
                    total_exam = f.readlines() # đọc file thành list chứa các phần tử là chuỗi
                    #print(total_exam) # list chứa các phần tử là string
                    print(f"{icon_analyzing} Đã phân tích dữ liệu {icon_analyzing}\n......................")
                    total_invalid_exam = [] # tạo list bài làm không hợp lệ 
                    total_valid_exam = [] # tạo list bài làm hợp lệ
                    # duyệt từng phần tử string trong list 
                    for line in total_exam:
                        exam = line.strip().split(",") # tách string thành list bỏ \n cuối dòng
                        pattern_check_N = r"^N\d{8}$" # tạo pattern để check mã số học sinh
                        # xét điều kiện các bài làm hợp lệ và không hợp lệ
                        # nếu bài làm không đủ 25 đáp án --> không hợp lệ
                        if len(exam) != 26:
                            # dùng regex match để check mã số
                            if not re.match(pattern_check_N, exam[0]): 
                                print(f"""Bài làm dư/thiếu so với 26 đáp án và sai mã số:\n{exam}
                                 """)
                            else: 
                                print(f"""Bài làm dư/thiếu so với 26 đáp án:\n{exam}
                                 """)
                            total_invalid_exam.append(exam)
                        # nếu bài làm đủ 25 đáp án --> có thể không hợp lệ do sai mã số
                        else:
                            if not re.match(pattern_check_N, exam[0]): 
                                print(f"""Bài làm sai mã số:\n{exam}
                                 """)
                                total_invalid_exam.append(exam)
                            else: 
                                total_valid_exam.append(exam)
                    # in ra thông tin cần thiết
                    print(f"*****BÁO CÁO ĐIỂM*****")            
                    print(f"1.Tổng số bài làm là {len(total_exam)} bài")
                    print(f"2.Tổng số bài làm hợp lệ là {len(total_valid_exam)} bài")
                    print(f"3.Tổng số bài không hợp lệ là {len(total_invalid_exam)} bài")
                    #print(total_valid_exam) # list trong list

                    # key đáp án    
                    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
                    list_answer_key = answer_key.strip().split(",") # chuyển key về list để chấm điểm
                    # print(f"Điểm từng học sinh trong lớp:")
                    top_score = [] # list các điểm > 80
                    all_score = [] # list toàn bộ điểm
                    # tạo folder chứa các file kết quả chấm điểm
                    save_file_name = result_folder/f"{class_name}_grade.txt"
                    with open(save_file_name, "w", encoding="utf-8") as sf:
                        # dùng zip để xét giá trị 2 list, sau đó chia ;àm 2 nhóm đúng và sai
                        for valid_exam in total_valid_exam:
                            right_answer = sum(1 for a, b in zip(valid_exam[1:], list_answer_key) if a == b)
                            wrong_answer = sum(1 for a, b in zip(valid_exam[1:], list_answer_key) if a != "" and a != b)
                            score = right_answer*4 - wrong_answer*1
                            all_score.append(score) # nhập điểm vào list
                            if score > 80: top_score.append(score)
                            # tạo biến cho mã số + điểm học sinh
                            dong = f"{valid_exam[0]}, {score}"
                            sf.write(dong + "\n") # ghi vào file từng dòng điểm của học sinh
                    # print(top_score)
                        
                    array_top_score = np.array(top_score) # chuyển list sang array
                    array_all_score = np.array(all_score) # chuyển list sang array
                    print(f"4.Số học sinh có điểm cao: {len(array_top_score)}") # tính phần tử array
                    print(f"5.Điểm trung bình cả lớp: {round((array_all_score.mean()),2)}") # tính trung bình
                    print(f"6.Điểm số cao nhất lớp: {array_all_score.max()}")
                    print(f"7.Điểm số thấp nhất lớp: {array_all_score.min()}")
                    print(f"8.Miền giá trị của điểm: {np.ptp(array_all_score)}") # điểm lớn nhất - điểm nhỏ nhất
                    print(f"9.Giá trị trung vị của điểm: {round(np.median(array_all_score))}") # tính trung vị
                    
                    # tạo cột mã số và cột 25 cột câu hỏi
                    col_id = ["Mã số"]
                    col_question = [f"Q{i}" for i in range(1, 26)]
                    cols = col_id + col_question # gộp 2 cột lại thành 1 biến
                    df = pd.DataFrame(total_valid_exam, columns=cols) # tạo bảng đáp án của 1 lớp
                    df_answers = df.replace(r"^\s*$", np.nan, regex=True) # buộc phải có regex=True để cho pandas biết đang làm việc với regex
                    total_student = df_answers.shape[0] # tất cả học sinh
                    # print(df)

                    missing_answers = df_answers.iloc[:, 1:].isnull().sum() # lấy toàn bộ các ô bị trống theo cột
                    count_most_missing_answer = missing_answers.max() # tìm số lượng bị bỏ trống nhiều nhất trong 1 cột
                    most_missing_answer = missing_answers[missing_answers == count_most_missing_answer] # boolean indexing
                    list_missing_answer = [] # tạo list chứa các câu hỏi bị xót nhiều nhất
                    # duyệt 
                    for answer, count in most_missing_answer.items(): 
                        ratio = round((count / total_student),2) # tính tỷ lệ bị bỏ trống, làm tròn
                        formatted_string = f"{answer} - {count} - {ratio}" # tạo 1 string có formatted để in ra giống đề bài
                        list_missing_answer.append(formatted_string)
                    final_string_missing_answer = ", ".join(list_missing_answer) # tách thành string
                    print(f"10.Câu hỏi bị bỏ trống câu trả lời nhiều nhất: {final_string_missing_answer}")

                    df_question = df.iloc[:, 1:] # lấy dữ liệu các cột trả lời(trừ mã số)
                    mask_wrong_answer = (df_question != list_answer_key) & (df_question != "") # lấy câu trả lời sai và không phải để trống
                    total_wrong_answer = mask_wrong_answer.sum() # tất cả câu trả lời sai
                    max_wrong_answer = total_wrong_answer.max() # số học sinh trả lời sai cho câu hỏi nhiều nhất
                    most_wrong_answer = total_wrong_answer[total_wrong_answer == max_wrong_answer]
                    list_wrong_answer = [] # tạo list chứa các câu hỏi bị trả lời sai nhiều nhất
                    for q , times in most_wrong_answer.items():
                        percent = round((times/total_student),2)
                        list_wrong_answer.append(f"{q} - {times} - {percent}")
                    final_string_wrong_answer = ", ".join(list_wrong_answer)
                    print(f"11.Câu hỏi bị trả lời sai nhiều nhất: {final_string_wrong_answer}")

                    
            # nếu file không tồn tại thì thông báo cho người dùng        
            else: print(f"{icon_wrong} Không tìm thấy file đáp án của lớp {class_name}")    
    # xử lý ngoại lệ bao gồm các lỗi khác
    except Exception as e: 
        print(f"{icon_wrong}Lỗi không xác định xảy ra: {e}")
        print(f"Bạn có thể nhập lại tên lớp!")




