import pandas as pd
import json

excel_path = '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/VN_FnB_Master_Expansion_v22_EnergyDrinks_2026.xlsx'
keywords_path = '../config/keywords.json'

print("Reading v22 Master Expansion file...")
df = pd.read_excel(excel_path)

with open(keywords_path, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

# Initialize categories if they don't exist
def add_to_dict(cat, word):
    if not isinstance(word, str) or word.strip() == "": return
    word = word.strip()
    if cat not in keywords:
        keywords[cat] = []
    # Check lowercase to avoid duplicates
    if word.lower() not in [k.lower() for k in keywords[cat]]:
        keywords[cat].append(word)

def map_category(eng_cat):
    eng_cat = str(eng_cat).lower()
    if any(x in eng_cat for x in ['milk tea', 'fruit tea', 'tea latte', 'brewed tea', 'pure tea', 'tea', 'matcha', 'oolong', 'deerioca', 'okinawa']):
        return 'BEV_TRA_SUA' 
    if any(x in eng_cat for x in ['coffee', 'espresso', 'cà phê', 'latte', 'macchiato', 'cafe', 'frappuccino', 'freeze']):
        return 'BEV_CAFE'
    if any(x in eng_cat for x in ['instant', 'noodle', 'mì', 'pho', 'bún', 'convenience food', 'dry processed food']):
        return 'FOOD_AN_SAN'
    if any(x in eng_cat for x in ['snack', 'candy', 'gum', 'dessert', 'ice cream', 'biscuit', 'cake', 'bakery', 'buns', 'toasts', 'bread', 'confectionery', 'cookie', 'cracker', 'crisp', 'bánh trung thu', 'wafer', 'chocolate', "lay's"]):
        return 'FOOD_SNACK' 
    if any(x in eng_cat for x in ['yogurt']):
        return 'BEV_SUA_CHUA'
    if any(x in eng_cat for x in ['milk']):
        return 'BEV_SUA_TUOI'
    if any(x in eng_cat for x in ['juice', 'ice blended', 'smoothie']):
        return 'BEV_NUOC_EP'
    if any(x in eng_cat for x in ['water']):
        return 'BEV_NUOC_KHOANG'
    if any(x in eng_cat for x in ['soft drink', 'beverage', 'drink', 'energy drink']):
        return 'BEV_NUOC_NGOT'
    if any(x in eng_cat for x in ['sauce', 'seasoning', 'topping', 'starter', 'powder']):
        return 'FOOD_OTHER'
    if any(x in eng_cat for x in ['sausage', 'giò', 'meat', 'canned food', 'frozen food', 'chicken', 'pork', 'beef', 'fish', 'fried & roasted']):
        return 'FOOD_THIT_CA'
    if any(x in eng_cat for x in ['salad', 'fruit', 'vegetable']):
        return 'FOOD_RAU_CU_QUA'
    if any(x in eng_cat for x in ['combo', 'set menu']):
        return 'COMBO/SET'
    if any(x in eng_cat for x in ['pizza', 'pasta', 'burger', 'melts']):
        return 'FOOD_LPN' 
    return None

added_count = 0
for idx, row in df.iterrows():
    eng_cat = row.get('category', '')
    target_cat = map_category(eng_cat)
    
    if target_cat:
        # Extract all text variations to maximize rule-based coverage
        product_name = row.get('canonical_name', '')
        official_name = row.get('official_system_name', '')
        normalized_name = row.get('normalized_name', '')
        brand_product_key = row.get('brand_product_key', '')
        
        if pd.notna(product_name): add_to_dict(target_cat, str(product_name))
        if pd.notna(official_name): add_to_dict(target_cat, str(official_name))
        if pd.notna(normalized_name): add_to_dict(target_cat, str(normalized_name))
        
        if pd.notna(brand_product_key):
            clean_key = str(brand_product_key).replace("::", " ").replace("_", " ")
            add_to_dict(target_cat, clean_key)
            added_count += 1 

with open(keywords_path, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

print(f"Successfully added {added_count} new brand product keys and their variations from Master Expansion v22!")
