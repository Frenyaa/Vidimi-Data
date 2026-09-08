import pandas as pd
import json

# Đọc file reviewed
df = pd.read_csv('../data/to_review/active_learning_queries.csv')
df = df.dropna(subset=['Human_Label', 'Item Name'])

# Đọc keywords hiện tại
with open('../config/keywords.json', 'r', encoding='utf-8') as f:
    keywords = json.load(f)

# Bổ sung các từ khóa mới
added_count = 0
for _, row in df.iterrows():
    label = str(row['Human_Label']).strip()
    item_name = str(row['Item Name']).strip()
    
    if label not in keywords:
        keywords[label] = []
        
    # Kiểm tra xem từ khoá (item name) đã có trong danh sách chưa (không phân biệt hoa thường)
    existing_kws_lower = [k.lower() for k in keywords[label]]
    if item_name.lower() not in existing_kws_lower:
        keywords[label].append(item_name)
        added_count += 1

# Lưu lại
with open('../config/keywords.json', 'w', encoding='utf-8') as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

print(f"Đã bổ sung thành công {added_count} món ăn/đồ uống từ Active Learning vào bộ từ khóa Rule-based!")
