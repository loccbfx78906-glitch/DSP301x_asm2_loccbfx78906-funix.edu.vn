from pathlib import Path
import re
import numpy as np
import pandas as pd

# Trang trí cho đẹp
icon_right = "👍"
icon_wrong = "🤦"
icon_exit = "🔌"
icon_analyzing = "💻"

folder = Path(__file__).parent

while True: 
    try:
        class_name = input(f"Nhập tên lớp cần tra cứu điểm(nếu muốn thoát hãy nhập 'thoát'):").lower().strip()
        pattern = r"^[a-z0-9]*$" # chỉ nhận chứ và số, không viết cách, không có khoảng trắng
        if class_name == "thoát":
            print(f"{icon_exit} Đã thoát chương trình")
            break
        elif class_name == "":
            print(f"{icon_wrong} Không được bỏ trống dòng này, vui lòng nhập tên lớp")
            continue
        elif not re.match(pattern, class_name):
            print(f"{icon_wrong} Tên lớp chứa ký tự không hợp lệ, không viết cách, chỉ được chứa chữ và số")
            print("Vui lòng nhập lại tên lớp")
            continue
        else:
            file_name = folder/f"{class_name}.txt"
            if file_name.exists():
                print(f"{icon_right} Đã mở file đáp án của lớp {class_name} thành công")
                with open(file_name, "r+", encoding="utf-8") as f:
                    total_exam = f.readlines()
                    #print(total_exam) # list chứa các phần tử là string
                    print(f"{icon_analyzing} Đã phân tích dữ liệu {icon_analyzing}\n")
                    total_invalid_exam = []
                    total_valid_exam = []
                    for line in total_exam:
                        exam = line.strip().split(",") # tách string thành list bỏ \n cuối dòng
                        pattern_check_N = r"^N\d{8}$"
                        if len(exam) != 26:
                            if not re.match(pattern_check_N, exam[0]): 
                                print(f"""Bài làm dư/thiếu so với 26 đáp án và sai mã số:\n{exam}
                                 """)
                            else: 
                                print(f"""Bài làm dư/thiếu so với 26 đáp án:\n{exam}
                                 """)
                            total_invalid_exam.append(exam)
                        else:
                            if not re.match(pattern_check_N, exam[0]): 
                                print(f"""Bài làm sai mã số:\n{exam}
                                 """)
                                total_invalid_exam.append(exam)
                            else: 
                                total_valid_exam.append(exam)
                    print(f"1.Tổng số bài làm là {len(total_exam)} bài")
                    print(f"2.Tổng số bài làm hợp lệ là {len(total_valid_exam)} bài")
                    print(f"3.Tổng số bài không hợp lệ là {len(total_invalid_exam)} bài")
                    #print(total_valid_exam) # list trong list
                        
                    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
                    list_answer_key = answer_key.strip().split(",")
                    # print(f"Điểm từng học sinh trong lớp:")
                    top_score = []
                    all_score = []
                    save_file_name = folder/f"{class_name}_grade.txt"
                    with open(save_file_name, "w", encoding="utf-8") as sf:
                        for valid_exam in total_valid_exam:
                            right_answer = sum(1 for a, b in zip(valid_exam[1:], list_answer_key) if a == b)
                            wrong_answer = sum(1 for a, b in zip(valid_exam[1:], list_answer_key) if a != "" and a != b)
                            # print(right_answer, wrong_answer)
                            score = right_answer*4 - wrong_answer*1
                            all_score.append(score)
                            # print(f"Mã số {valid_exam[0]}: {score}")
                            if score > 80: top_score.append(score)
                            dong = f"{valid_exam[0]}, {score}"
                            sf.write(dong + "\n")
                    # print(top_score)
                        
                    array_top_score = np.array(top_score)
                    array_all_score = np.array(all_score)
                    print(f"4.Số học sinh có điểm cao: {len(array_top_score)}")
                    print(f"5.Điểm trung bình cả lớp: {round((array_all_score.mean()),2)}") # tính trung bình
                    print(f"6.Điểm số cao nhất lớp: {array_all_score.max()}")
                    print(f"7.Điểm số thấp nhất lớp: {array_all_score.min()}")
                    print(f"8.Miền giá trị của điểm: {np.ptp(array_all_score)}") # điểm lớn nhất - điểm nhỏ nhất
                    print(f"9.Giá trị trung vị của điểm: {round(np.median(array_all_score))}") # tính trung vị
                    
                    col_id = ["Mã số"]
                    col_question = [f"Q{i}" for i in range(1, 26)]
                    cols = col_id + col_question
                    df = pd.DataFrame(total_valid_exam, columns=cols)
                    df_answers = df.replace(r"^\s*$", np.nan, regex=True) # buộc phải có regex=True để cho pandas biết đang làm việc với regex
                    total_student = df_answers.shape[0]
                    # print(df)

                    missing_answers = df_answers.iloc[:, 1:].isnull().sum() # lấy toàn bộ các ô bị trống theo cột
                    count_most_missing_answer = missing_answers.max() # tìm số lượng bị bỏ trống nhiều nhất trong 1 cột
                    most_missing_answer = missing_answers[missing_answers == count_most_missing_answer] # boolean indexing
                    list_missing_answer = []
                    for answer, count in most_missing_answer.items():
                        ratio = round((count / total_student),2) 
                        formatted_string = f"{answer} - {count} - {ratio}"
                        list_missing_answer.append(formatted_string)
                    final_string_missing_answer = ", ".join(list_missing_answer)
                    print(f"10.Câu hỏi bị bỏ trống câu trả lời nhiều nhất: {final_string_missing_answer}")

                    df_question = df.iloc[:, 1:] # lấy dữ liệu các cột trả lời(trừ mã số)
                    mask_wrong_answer = (df_question != list_answer_key) & (df_question != "")
                    total_wrong_answer = mask_wrong_answer.sum()
                    max_wrong_answer = total_wrong_answer.max()
                    most_wrong_answer = total_wrong_answer[total_wrong_answer == max_wrong_answer]
                    list_wrong_answer = []
                    for q , times in most_wrong_answer.items():
                        percent = round((times/total_student),2)
                        list_wrong_answer.append(f"{q} - {times} - {percent}")
                    final_string_wrong_answer = ", ".join(list_wrong_answer)
                    print(f"11.Câu hỏi bị trả lời sai nhiều nhất: {final_string_wrong_answer}")

                    
                    
            else: print(f"{icon_wrong} Không tìm thấy file đáp án của lớp {class_name}")    
    except Exception as e: 
        print(f"{icon_wrong}Lỗi không xác định xảy ra: {e}")
        print(f"Bạn có thể nhập lại tên lớp!")




