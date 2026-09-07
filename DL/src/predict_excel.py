import pandas as pd
import re
from classify import FoodClassifierPipeline

# 1. Khởi tạo Pipeline
print("Đang tải mô hình...")
pipeline = FoodClassifierPipeline('../config/keywords.json', '../data/model')

# 2. Đọc file Excel
file_path = '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Du-Lieu-Check-In.1788433372.xls'
print(f"Đang đọc dữ liệu từ file {file_path}...")
df = pd.read_excel(file_path)

# 3. Trích xuất tên món ăn từ cột 'Items'
print("Đang xử lý tách món ăn từ các Bill...")
extracted_items = []

# Duyệt qua từng dòng Bill
for idx, row in df.iterrows():
    items_raw = str(row.get('Items', ''))
    if items_raw == 'nan' or not items_raw:
        continue
        
    # Tách các món bằng dấu \n
    item_lines = items_raw.split('\n')
    for line in item_lines:
        # Tách lấy 'name: [tên món], slg: ..., price: [giá]'
        match = re.search(r'name:\s*(.*?),\s*slg:\s*.*?,\s*price:\s*(\d+)', line, re.IGNORECASE)
        if match:
            item_name = match.group(1).strip()
            item_price = float(match.group(2))
            extracted_items.append({
                'Bill ID': row.get('Bill ID', ''),
                'Original Item Name': item_name,
                'Price': item_price
            })

items_df = pd.DataFrame(extracted_items)
print(f"Đã trích xuất thành công {len(items_df)} món ăn từ {len(df)} hóa đơn.")

test_df = items_df

print("\nĐang tiến hành phân loại bằng AI (Xử lý batch, sẽ nhanh hơn hàng chục lần)...")
results = []
from tqdm import tqdm

batch_size = 512
for i in tqdm(range(0, len(test_df), batch_size), desc="Phân loại (Batch)"):
    batch_df = test_df.iloc[i:i+batch_size]
    names = batch_df['Original Item Name'].tolist()
    prices = batch_df['Price'].tolist()
    
    batch_results = pipeline.predict_batch(names, prices)
    for (name, price, (cat, method, clean)) in zip(names, prices, batch_results):
        results.append({
            'Original Text': name,
            'Price': price,
            'Cleaned Text': clean,
            'Predicted Category': cat,
            'Method': method
        })

results_df = pd.DataFrame(results)

# 4. Hiển thị kết quả
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
print("\n" + "="*80)
print("KẾT QUẢ PHÂN LOẠI MẪU")
print("="*80)
print(results_df.to_string())

# Xuất ra file Excel mới để bạn xem
output_path = '../data/output/Predicted_Check_In.xlsx'
results_df.to_excel(output_path, index=False)
print(f"\nĐã xuất kết quả ra file: {output_path}")
