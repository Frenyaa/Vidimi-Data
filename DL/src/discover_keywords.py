import os
import pandas as pd
import json
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from classify import FoodClassifierPipeline, TextPreprocessor

def discover_new_keywords(excel_path, config_path, model_dir, output_path):
    print("1. Khởi tạo AI Pipeline để dự đoán dữ liệu...")
    pipeline = FoodClassifierPipeline(config_path, model_dir)
    preprocessor = TextPreprocessor()
    
    with open(config_path, 'r', encoding='utf-8') as f:
        existing_keywords = json.load(f)
        
    print(f"2. Đọc file {excel_path}...")
    xls = pd.ExcelFile(excel_path)
    all_products = set()
    
    # Đọc các sheet có khả năng chứa sản phẩm
    for sheet_name in xls.sheet_names:
        if sheet_name in ['Location', 'Bill Trùng', 'Nghi ngờ ']:
            continue
        try:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            # Tìm cột chứa tên sản phẩm
            col_name = None
            if 'Tên SP' in df.columns:
                col_name = 'Tên SP'
            elif 'Product Name' in df.columns:
                col_name = 'Product Name'
            elif 'Product' in df.columns:
                col_name = 'Product'
                
            if col_name:
                items = df[col_name].dropna().astype(str).tolist()
                all_products.update(items)
        except Exception as e:
            pass
            
    items_list = list(all_products)
    print(f"Đã trích xuất {len(items_list)} tên sản phẩm duy nhất từ các sheet.")
    
    print("3. Chạy AI phân loại toàn bộ sản phẩm...")
    # Vì không có price trong script đơn giản này, ta mặc định price = 0
    prices = [0.0] * len(items_list)
    batch_size = 512
    predictions = []
    
    from tqdm import tqdm
    for i in tqdm(range(0, len(items_list), batch_size), desc="Đang phân loại"):
        batch_texts = items_list[i:i+batch_size]
        batch_prices = prices[i:i+batch_size]
        batch_results = pipeline.predict_batch(batch_texts, batch_prices)
        for text, (cat, method, clean) in zip(batch_texts, batch_results):
            predictions.append({'text': text, 'clean': clean, 'cat': cat})
            
    df_preds = pd.DataFrame(predictions)
    
    print("4. Đang phân tích N-grams để tìm từ khóa mới...")
    new_keywords_suggestions = []
    
    for cat in df_preds['cat'].unique():
        if cat == "UNKNOWN_OTHER": continue
        
        # Lấy các món được dự đoán thuộc nhóm cat
        cat_texts = df_preds[df_preds['cat'] == cat]['clean'].tolist()
        if not cat_texts: continue
        
        # Dùng CountVectorizer để đếm cụm 1-3 từ phổ biến nhất
        vectorizer = CountVectorizer(ngram_range=(1, 3), min_df=2)
        try:
            X = vectorizer.fit_transform(cat_texts)
            word_counts = zip(vectorizer.get_feature_names_out(), X.sum(axis=0).tolist()[0])
            sorted_words = sorted(word_counts, key=lambda x: x[1], reverse=True)
            
            # Lấy tập keyword cũ của nhóm này
            old_kws = [k.lower() for k in existing_keywords.get(cat, [])]
            
            # Lọc ra các từ khóa MỚI (chưa có trong list cũ)
            count_added = 0
            for word, freq in sorted_words:
                # Bỏ qua các cụm từ quá ngắn hoặc chứa số/ký tự đặc biệt
                if len(word) < 3 or any(char.isdigit() for char in word):
                    continue
                # Bỏ qua nếu từ đã tồn tại trong luật cũ (chính xác hoặc nằm trong)
                if any(word in old_kw or old_kw in word for old_kw in old_kws):
                    continue
                
                new_keywords_suggestions.append({
                    'Category': cat,
                    'Suggested_Keyword': word,
                    'Frequency': freq,
                    'Example_Item': next(t for t in cat_texts if word in t)
                })
                count_added += 1
                if count_added >= 30: # Lấy Top 30 từ khóa mới mỗi nhóm
                    break
        except:
            pass

    suggest_df = pd.DataFrame(new_keywords_suggestions)
    suggest_df.to_excel(output_path, index=False)
    print(f"\nHOÀN TẤT! Đã phát hiện {len(suggest_df)} từ khóa tiềm năng mới.")
    print(f"File đề xuất từ khóa đã được lưu tại: {output_path}")

if __name__ == "__main__":
    discover_new_keywords(
        '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Data Clean.xlsx',
        '../config/keywords.json',
        '../data/model',
        '../data/output/Suggested_New_Keywords.xlsx'
    )
