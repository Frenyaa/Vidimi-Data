import pandas as pd
import json

test_path = '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/test.xlsx'
keywords_path = '../config/keywords.json'

print(f"Reading {test_path}...")
df = pd.read_excel(test_path)

# Map category từ file test sang nhãn của hệ thống
cat_map = {
    'Rau củ': 'FOOD_RAU_CU_QUA',
    'Trái cây': 'FOOD_RAU_CU_QUA',
    'Nấm': 'FOOD_RAU_CU_QUA',
    
    'Thịt heo': 'FOOD_THIT_CA',
    'Thịt gà': 'FOOD_THIT_CA',
    'Thịt bò': 'FOOD_THIT_CA',
    'Cá': 'FOOD_THIT_CA',
    'Hải sản': 'FOOD_THIT_CA',
    'Nghêu, sò, ...': 'FOOD_THIT_CA',
    'Nghều, sò, ...': 'FOOD_THIT_CA',
    'Trứng': 'FOOD_THIT_CA',
    
    'Bánh kẹo': 'FOOD_SNACK',
    'Snack': 'FOOD_SNACK',
    
    'Thuốc': 'UNKNOWN_OTHER',
    'Thực phẩm chức năng': 'UNKNOWN_OTHER',
    'Dung dịch vệ sinh /y tế': 'UNKNOWN_OTHER',
    'Dụng cụ y tế hỗ trợ': 'UNKNOWN_OTHER',
    'Khăn ướt': 'UNKNOWN_OTHER',
    'Khăn lạnh': 'UNKNOWN_OTHER',
    'Khăn': 'UNKNOWN_OTHER',
    'Mũ': 'UNKNOWN_OTHER',
    'Tiền điện tử': 'UNKNOWN_OTHER',
    'Games': 'UNKNOWN_OTHER',
    'Dịch vụ vận tải (vé xe buýt, vé máy bay,...)': 'UNKNOWN_OTHER',
    'Giày dép': 'UNKNOWN_OTHER',
    'Túi': 'UNKNOWN_OTHER',
    'Sách giáo dục': 'UNKNOWN_OTHER',
    'Áo': 'UNKNOWN_OTHER',
    'Đầm': 'UNKNOWN_OTHER',
    'Váy': 'UNKNOWN_OTHER',
    'Chân váy': 'UNKNOWN_OTHER',
    'Quần': 'UNKNOWN_OTHER',
    'Bút vở': 'UNKNOWN_OTHER',
    'Dịch vụ phòng': 'UNKNOWN_OTHER',
    'Toner': 'UNKNOWN_OTHER',
    'Vé xem phim': 'UNKNOWN_OTHER',
    'Phấn phủ': 'UNKNOWN_OTHER',
    'Ngân hàng': 'UNKNOWN_OTHER',
    'Dầu gội': 'UNKNOWN_OTHER',
    'Dầu xả': 'UNKNOWN_OTHER',
    'Sữa tắm': 'UNKNOWN_OTHER',
    'Tẩy trang': 'UNKNOWN_OTHER',
    'Nước giặt': 'UNKNOWN_OTHER',
    'Nước rửa chén': 'UNKNOWN_OTHER',
    'Nước hoa': 'UNKNOWN_OTHER',
    'Nước xả': 'UNKNOWN_OTHER',
    'Nước lau sàn': 'UNKNOWN_OTHER',
    'Dao cạo râu': 'UNKNOWN_OTHER',
    'Dầu nhớt': 'UNKNOWN_OTHER',
    'Điện thoại di động': 'UNKNOWN_OTHER',
    'Dụng cụ ăn uống': 'UNKNOWN_OTHER',
    'Hộp': 'UNKNOWN_OTHER',
    'Nồi cơm điện': 'UNKNOWN_OTHER',
    'Chứng khoán': 'UNKNOWN_OTHER',
    'Kem dưỡng ẩm': 'UNKNOWN_OTHER',
    'Bao tay': 'UNKNOWN_OTHER',
    'Phụ kiện điện tử': 'UNKNOWN_OTHER',
    'Cỏ': 'UNKNOWN_OTHER',
    'Spa': 'UNKNOWN_OTHER',
    'Kem đánh răng': 'UNKNOWN_OTHER',
    'Xe đạp': 'UNKNOWN_OTHER',
    'Sữa chống nắng': 'UNKNOWN_OTHER',
    
    'Gia vị': 'FOOD_OTHER',
    'Combo/Set': 'FOOD_OTHER',
    'Combo /Set': 'FOOD_OTHER',
    
    'Mì gói': 'FOOD_AN_SAN',
    'Mì': 'FOOD_AN_SAN',
    'Món sợi': 'FOOD_AN_SAN',
    'Xôi': 'FOOD_AN_SAN',
    'Cơm': 'FOOD_AN_SAN',
    'Gạo': 'FOOD_AN_SAN',
    
    'Sữa tươi': 'BEV_SUA_TUOI'
}

with open(keywords_path, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

added_count = 0
for idx, row in df.iterrows():
    raw_cat = str(row['Product Category']).strip()
    name = str(row['Product Name']).strip()
    
    if pd.isna(row['Product Name']) or not name:
        continue
        
    mapped_label = cat_map.get(raw_cat)
    
    if mapped_label:
        if mapped_label not in keywords:
            keywords[mapped_label] = []
            
        existing_kws_lower = [k.lower() for k in keywords[mapped_label]]
        
        if name.lower() not in existing_kws_lower:
            keywords[mapped_label].append(name)
            added_count += 1

with open(keywords_path, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

print(f"Đã hút thành công {added_count} món Siêu Thị / Tạp Hóa (Non-F&B và Grocery) từ test.xlsx đưa vào keywords.json!")
