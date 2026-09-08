import json

keywords_path = '../config/keywords.json'

with open(keywords_path, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

def add_kw(cat, word):
    if cat not in keywords:
        keywords[cat] = []
    if word.lower() not in [k.lower() for k in keywords[cat]]:
        keywords[cat].append(word)

# Fix La Vie & Nước khoáng
add_kw('BEV_NUOC_KHOANG', 'la vie')
add_kw('BEV_NUOC_KHOANG', 'lavie')
add_kw('BEV_NUOC_KHOANG', 'nước khoảng') # Typo of nước khoáng

# Fix Revive
add_kw('BEV_NUOC_NGOT', 'revive')

# Fix Sua Susu (to avoid matching "socola" and falling into FOOD_SNACK)
add_kw('BEV_SUA_TUOI', 'sua susu')
add_kw('BEV_SUA_TUOI', 'sữa susu')
add_kw('BEV_SUA_TUOI', 'susu')

with open(keywords_path, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

print("Đã vá xong các lỗi từ vựng do user report!")
