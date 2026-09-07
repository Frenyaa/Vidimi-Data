import pandas as pd
import json

file_paths = [
    '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Potential_Keys_Mapped_BEV_FOOD.xlsx'
]

keywords_dict = {}

for file_path in file_paths:
    print(f"Reading keys from {file_path}...")
    df = pd.read_excel(file_path)
    
    # Drop rows with missing Label or Keyword
    df = df.dropna(subset=['Keyword', 'Mapped_Label'])
    
    # Gom nhóm Keyword theo Mapped_Label
    for idx, row in df.iterrows():
        label = str(row['Mapped_Label']).strip()
        keyword = str(row['Keyword']).strip().lower()
        
        # Bỏ qua các nhãn lỗi
        if label == "UNKNOWN_NEED_ML_MODEL":
            continue
            
        if label not in keywords_dict:
            keywords_dict[label] = []
            
        if keyword not in keywords_dict[label]:
            keywords_dict[label].append(keyword)

# Lưu vào config/keywords.json
out_path = '../config/keywords.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(keywords_dict, f, ensure_ascii=False, indent=2)

print(f"Đã cập nhật {len(keywords_dict)} Category với hàng ngàn Keyword vào file {out_path}!")
