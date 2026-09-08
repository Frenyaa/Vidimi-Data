import json

keywords_path = '../config/keywords.json'

with open(keywords_path, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

def add_kw(cat, word):
    if cat not in keywords:
        keywords[cat] = []
    if word.lower() not in [k.lower() for k in keywords[cat]]:
        keywords[cat].append(word)

# 1. Combo
add_kw('FOOD_COMBO', 'combo')
add_kw('FOOD_COMBO', 'set menu')
add_kw('FOOD_COMBO', 'combo 165k')

# 2. Fish burger
add_kw('FOOD_TINH_BOT', 'fish burger')
add_kw('FOOD_TINH_BOT', 'burger ca')

# 3. Fries
add_kw('FOOD_SNACK', 'fries')
add_kw('FOOD_SNACK', 'french fries')
add_kw('FOOD_SNACK', 'khoai tay chien')

# 4. Chocolate sữa dừa
add_kw('BEV_SINH_TO', 'chocolate sua dua')
add_kw('BEV_SINH_TO', 'chocolate sữa dừa')

# 5. Croissant dính chữ
add_kw('FOOD_TINH_BOT', 'croissantnhan')
add_kw('FOOD_TINH_BOT', 'croissant')

# 6. Rau câu
add_kw('FOOD_SNACK', 'rau cau')
add_kw('FOOD_SNACK', 'rau câu')
add_kw('FOOD_SNACK', 'thach')
add_kw('FOOD_SNACK', 'jelly')
add_kw('FOOD_SNACK', 'alpen jelly')

with open(keywords_path, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

print("Đã thêm thành công các từ khóa sửa lỗi (Edge Cases) vào keywords.json!")
