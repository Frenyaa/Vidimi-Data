import json

keywords_path = '../config/keywords.json'

with open(keywords_path, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

if 'FOOD_COMBO' in keywords:
    combo_items = keywords.pop('FOOD_COMBO')
    if 'COMBO/SET' not in keywords:
        keywords['COMBO/SET'] = combo_items
    else:
        keywords['COMBO/SET'].extend(combo_items)
        
    with open(keywords_path, 'w', encoding='utf-8') as f:
        json.dump(keywords, f, ensure_ascii=False, indent=2)
    print("Đã đổi tên nhãn FOOD_COMBO thành COMBO/SET thành công!")
else:
    print("Không tìm thấy nhãn FOOD_COMBO.")
