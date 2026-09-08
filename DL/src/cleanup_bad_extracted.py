import json

keywords_path = '../config/keywords.json'

with open(keywords_path, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

def remove_kw(cat, word):
    if cat in keywords:
        keywords[cat] = [kw for kw in keywords[cat] if kw.lower() != word.lower()]

# Loại bỏ các chuỗi dài bị bắt nhầm vào nhóm sai do lấy từ test.xlsx
remove_kw('FOOD_RAU_CU_QUA', 'FRIES')
remove_kw('FOOD_RAU_CU_QUA', 'FRENCH FRIES')
remove_kw('FOOD_RAU_CU_QUA', 'Rau câu dừa T.N.LAN 160g')
remove_kw('FOOD_RAU_CU_QUA', 'Rau câu dừa T.N.LAN 360g')
remove_kw('FOOD_RAU_CU_QUA', 'Rau câu cafe T.N.LAN 160g')

remove_kw('FOOD_OTHER', 'Combo Group 2B')
remove_kw('UNKNOWN_OTHER', 'Combo 2 Thực phẩm bảo vệ sức khỏe Enterogermina')
remove_kw('UNKNOWN_OTHER', 'Combo 2 Thực phẩm bảo vệ sức khỏe Enterogermina xoài keo')

with open(keywords_path, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

print("Đã dọn dẹp các từ khóa bị hút nhầm từ test.xlsx!")
