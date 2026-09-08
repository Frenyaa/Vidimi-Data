import json

keywords_path = '../config/keywords.json'

with open(keywords_path, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

def add_kw(cat, word):
    if cat not in keywords:
        keywords[cat] = []
    if word.lower() not in [k.lower() for k in keywords[cat]]:
        keywords[cat].append(word)

# F&B Missing
add_kw('FOOD_TINH_BOT', 'spag')
add_kw('FOOD_THIT_CA', 'cjoy')
add_kw('BEV_SUA_CHUA', 'yomost')
add_kw('FOOD_OTHER', 'ajinomoto')

# Non-F&B Missing (Supermarket items that confuse XGBoost)
add_kw('UNKNOWN_OTHER', 'omo')
add_kw('UNKNOWN_OTHER', 'tresemme')
add_kw('UNKNOWN_OTHER', 'thuốc 555')
add_kw('UNKNOWN_OTHER', 'bvs')
add_kw('UNKNOWN_OTHER', 'băng keo')
add_kw('UNKNOWN_OTHER', 'povidine')
add_kw('UNKNOWN_OTHER', 'dulux')
add_kw('UNKNOWN_OTHER', 'vé xe buýt')
add_kw('UNKNOWN_OTHER', 'usdt')
add_kw('UNKNOWN_OTHER', 'coupon')

with open(keywords_path, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

print("Đã bổ sung thêm các từ khóa ngoại lai (Supermarket/Non-F&B) vào keywords.json!")
