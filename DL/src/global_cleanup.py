import json
import os

# Đường dẫn file
file_path = '../config/keywords.json'

with open(file_path, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

categories_to_check = list(keywords.keys())

moved_count = 0
items_to_move = []

for cat in categories_to_check:
    original_items = keywords[cat].copy()
    for item in original_items:
        text = item.lower()
        new_cat = None
        
        # 1. Nhóm RAU CỦ QUẢ
        if "salad" in text or "xa lach" in text or "xà lách" in text:
            new_cat = "FOOD_RAU_CU_QUA"
        # 2. Nhóm SỮA CHUA
        elif "sua chua" in text or "sữa chua" in text or "yogurt" in text:
            new_cat = "BEV_SUA_CHUA"
        # 3. Nhóm PHÔ MAI / BƠ SỮA
        elif "pho mai" in text or "phô mai" in text or "cheese" in text or "mascarpone" in text or "raclette" in text or "camembert" in text or "ricotta" in text or "mozzarella" in text:
            new_cat = "FOOD_SUA_AN"
        # 4. Nhóm TINH BỘT / PIZZA
        elif "pizza" in text or "spaghetti" in text or "spag" in text or "mì ý" in text or "mi y" in text or "udon" in text or "ramen" in text or "toast" in text or "bap nuong" in text or "bắp nướng" in text:
            new_cat = "FOOD_TINH_BOT"
        # 5. Nhóm SÚP
        elif "xup" in text or "súp" in text or "sup " in text:
            new_cat = "FOOD_OTHER"
        # 6. Nhóm THỊT / CÁ
        elif "ca ngu" in text or "cá ngừ" in text or "ca hoi" in text or "cá hồi" in text or "thit xong khoi" in text or "thịt xông khói" in text:
            new_cat = "FOOD_THIT_CA"
        # 7. Nhóm TRÁNG MIỆNG / KEM
        elif "kem" in text or "pudding" in text or "panna cotta" in text or "tiramisu" in text or "terrine" in text or "croissant" in text:
            new_cat = "FOOD_SNACK"
            
        if new_cat and new_cat != cat:
            items_to_move.append((item, cat, new_cat))

for item, old_cat, new_cat in items_to_move:
    if item in keywords[old_cat]:
        keywords[old_cat].remove(item)
    if new_cat not in keywords:
        keywords[new_cat] = []
    if item not in keywords[new_cat]:
        keywords[new_cat].append(item)
    moved_count += 1

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

print(f"Đã di dời thành công {moved_count} từ khóa về đúng danh mục!")
