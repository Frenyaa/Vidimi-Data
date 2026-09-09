import json

with open('/Users/buidoanhaiyen/Documents/Vidimi/Code/DL/config/keywords.json', 'r', encoding='utf-8') as f:
    kw = json.load(f)

print("FOOD_THIT_CA count:", len(kw.get('FOOD_THIT_CA', [])))
print("FOOD_TINH_BOT count:", len(kw.get('FOOD_TINH_BOT', [])))

# Let's check a few items
for item in ['bún thịt xào', 'bún thịt nướng', 'cơm chiên hải sản', 'bún thịt bò']:
    found = False
    for cat, words in kw.items():
        if item in words:
            print(f"'{item}' is in {cat}")
            found = True
    if not found:
        print(f"'{item}' not found in any category")
