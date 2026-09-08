import pandas as pd
import json

excel_path = '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/VN_FnB_Master_Expansion_v11_KOI_BreadTalk_2026.xlsx'
keywords_path = '../config/keywords.json'

print(f"Reading {excel_path}...")
df = pd.read_excel(excel_path)

# Dictionary map category
cat_map = {
    'Burger': 'FOOD_TINH_BOT', 'Pizza': 'FOOD_TINH_BOT', 'Pasta': 'FOOD_TINH_BOT', 'Pasta/Main': 'FOOD_TINH_BOT', 'Bakery': 'FOOD_TINH_BOT',
    'Sandwich': 'FOOD_TINH_BOT', 'Buns': 'FOOD_TINH_BOT', 'Toasts': 'FOOD_TINH_BOT', 'Euro Bread': 'FOOD_TINH_BOT', 'Rice - Burger - Pasta': 'FOOD_TINH_BOT',
    
    'Milk Tea': 'BEV_TRA_SUA', 'Okinawa': 'BEV_TRA_SUA', 'Brown Sugar Deerioca': 'BEV_TRA_SUA', 'Fresh Milk Tea': 'BEV_TRA_SUA', 'Snow Cap Milk Tea': 'BEV_TRA_SUA', 'Brown Sugar Cream Cheese': 'BEV_TRA_SUA', 'Signature Macchiato': 'BEV_TRA_SUA',
    
    'Fruit Tea': 'BEV_TRA', 'Pure Tea': 'BEV_TRA', 'Tea': 'BEV_TRA', 'Brewed Tea': 'BEV_TRA', 'Fresh Tea': 'BEV_TRA', 'Oolong': 'BEV_TRA', 'Jasmine Tea': 'BEV_TRA', 'Trà': 'BEV_TRA', 'Tea Latte': 'BEV_TRA', '2025 Tea Latte': 'BEV_TRA', 'Flavored Tea': 'BEV_TRA', 'Fruit/Oolong': 'BEV_TRA', 'Chewy Tea': 'BEV_TRA', 'Packaged Tea': 'BEV_TRA', 'Teaspresso Latte': 'BEV_TRA',
    
    'Cafe': 'BEV_CAFE', 'Coffee': 'BEV_CAFE', 'Latte': 'BEV_CAFE', 'Americano': 'BEV_CAFE', 'Latte & Frappe': 'BEV_CAFE', 'Cà Phê': 'BEV_CAFE', 'Cà Phê / Espresso': 'BEV_CAFE', 'Cà Phê / Cold Brew': 'BEV_CAFE', 'Espresso Beverage': 'BEV_CAFE', 'Coffee Beverage': 'BEV_CAFE', 'Cold Brew': 'BEV_CAFE', 'Cà Phê Việt Nam': 'BEV_CAFE', 'PhinĐI': 'BEV_CAFE', 'Packaged Coffee': 'BEV_CAFE',
    
    'Ice Blended': 'BEV_SINH_TO', 'Matcha': 'BEV_SINH_TO', 'Freeze': 'BEV_SINH_TO', 'Coffee Frappuccino': 'BEV_SINH_TO', 'Cream Frappuccino': 'BEV_SINH_TO', 'Teaspresso Frappe': 'BEV_SINH_TO', 'Blended': 'BEV_SINH_TO', 'Yogurt': 'BEV_SINH_TO', 'MatchaĐI': 'BEV_SINH_TO',
    
    'Ice Cream': 'FOOD_SNACK', 'Dessert': 'FOOD_SNACK', 'Appetizer/Salad': 'FOOD_SNACK', 'Salad': 'FOOD_SNACK', 'Soup': 'FOOD_SNACK', 'Starter': 'FOOD_SNACK', 'Snacks / Side': 'FOOD_SNACK', 'Side': 'FOOD_SNACK', 'Bánh Trung Thu 2026': 'FOOD_SNACK', 'Cake': 'FOOD_SNACK', 'Cakes': 'FOOD_SNACK', 'Slices Cake': 'FOOD_SNACK', 'Dry Cakes': 'FOOD_SNACK', 'Cookie': 'FOOD_SNACK', 'Snack': 'FOOD_SNACK',
    
    'Chicken': 'FOOD_THIT_CA', 'Fried & Roasted': 'FOOD_THIT_CA',
    'Rice': 'FOOD_AN_SAN',
    
    'Beverage': 'BEV_NUOC_NGOT', 'Signature': 'BEV_NUOC_NGOT', '2026 Seasonal Beverage': 'BEV_NUOC_NGOT', 'RTD Beverage': 'BEV_NUOC_NGOT', 'Packaged Beverage': 'BEV_NUOC_NGOT', 'Drinks': 'BEV_NUOC_NGOT', 'Special drink': 'BEV_NUOC_NGOT', '2026 New Beverage': 'BEV_NUOC_NGOT', '2025 Seasonal Beverage': 'BEV_NUOC_NGOT', 'Chocolate Beverage': 'BEV_NUOC_NGOT',
    
    'Juice': 'BEV_NUOC_EP'
}

with open(keywords_path, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

added_count = 0
for idx, row in df.iterrows():
    raw_cat = str(row['category']).strip()
    brand = str(row['brand']).strip().lower()
    norm_name = str(row['normalized_name']).strip()
    
    if pd.isna(row['normalized_name']) or not norm_name:
        continue
        
    mapped_label = cat_map.get(raw_cat)
    
    if not mapped_label:
        continue # Bỏ qua các loại không nằm trong map (combo, seasonal food, v.v)
        
    if mapped_label not in keywords:
        keywords[mapped_label] = []
        
    existing_kws_lower = [k.lower() for k in keywords[mapped_label]]
    
    if norm_name.lower() not in existing_kws_lower:
        keywords[mapped_label].append(norm_name)
        existing_kws_lower.append(norm_name.lower())
        added_count += 1
        
    brand_specific_name = f"{brand} {norm_name}"
    if brand_specific_name.lower() not in existing_kws_lower:
        keywords[mapped_label].append(brand_specific_name)
        existing_kws_lower.append(brand_specific_name.lower())
        added_count += 1

with open(keywords_path, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

print(f"Thành công! Đã bơm thêm {added_count} từ khóa từ file KOI & BreadTalk vào keywords.json!")
