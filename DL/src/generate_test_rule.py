import pandas as pd
import re
import json
from classify import TextPreprocessor

def generate_test_rule_results():
    print("Đang tải dữ liệu từ file Check-In gốc...")
    file_path = '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Du-Lieu-Check-In.1788433372.xls'
    df = pd.read_excel(file_path)
    
    print("Đang tải bộ từ điển (keywords.json)...")
    with open('../config/keywords.json', 'r', encoding='utf-8') as f:
        keywords = json.load(f)
        
    preprocessor = TextPreprocessor()
    extracted_items = []
    
    print("Bóc tách tên món và áp dụng Rule-based (tìm Keyword khớp)...")
    from tqdm import tqdm
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Xử lý Bill"):
        items_raw = str(row.get('Items', ''))
        if items_raw == 'nan' or not items_raw:
            continue
            
        item_lines = items_raw.split('\n')
        for line in item_lines:
            match = re.search(r'name:\s*(.*?),\s*slg', line, re.IGNORECASE)
            if match:
                product_name = match.group(1).strip()
                clean_text = preprocessor.preprocess(product_name)
                original_lower = product_name.lower()
                
                # Tìm rule khớp
                predicted_label = "UNKNOWN"
                matched_kw = ""
                
                # Tối ưu: gom tất cả từ khóa, sắp xếp theo độ dài giảm dần để ưu tiên khớp cụm dài
                all_kws = []
                for cat, kws in keywords.items():
                    for kw in kws:
                        all_kws.append((kw, cat))
                all_kws.sort(key=lambda x: len(x[0]), reverse=True)
                
                matched = False
                for kw, cat in all_kws:
                    kw_lower = kw.lower()
                    pattern = r'(?:\b|^|\s)' + re.escape(kw_lower) + r'(?:\b|$|\s)'
                    if re.search(pattern, original_lower) or re.search(pattern, clean_text):
                        predicted_label = cat
                        matched_kw = kw
                        matched = True
                        break
                
                extracted_items.append({
                    'Bill ID': row.get('Bill ID', ''),
                    'Ngày chụp bill': row.get('Ngày chụp bill', ''),
                    'Ngày trên bill': row.get('Ngày trên bill', ''),
                    'User ID': row.get('User ID', ''),
                    'Gender ID': row.get('Gender ID', ''),
                    'Age ID': row.get('Age ID', ''),
                    'Place ID': row.get('Place ID', ''),
                    'Brand ID': row.get('Brand ID', ''),
                    'Loại địa điểm ID': row.get('Loại địa điểm ID', ''),
                    'Khu vực ID': row.get('Khu vực ID', ''),
                    'Product Name': product_name,
                    'Product Category': '', # Có thể để trống hoặc điền sau
                    'Category': '',         # Có thể để trống hoặc điền sau
                    'Predicted_Rule_Label': predicted_label,
                    'Matched_Keyword': matched_kw
                })

    result_df = pd.DataFrame(extracted_items)
    
    output_path = '../data/output/test_rule_results_new.xlsx'
    result_df.to_excel(output_path, index=False)
    print(f"\nĐã xuất file Test Rule Results ra: {output_path}")

if __name__ == "__main__":
    generate_test_rule_results()
