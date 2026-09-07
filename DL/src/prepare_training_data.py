import pandas as pd
import json
import os
from classify import TextPreprocessor

def prepare_data(raw_csv_path, output_labeled_path, keywords_path):
    print(f"Reading raw data from {raw_csv_path}")
    # Đọc data (giả lập)
    if not os.path.exists(raw_csv_path):
        print("Raw data not found, creating dummy data...")
        os.makedirs(os.path.dirname(raw_csv_path), exist_ok=True)
        dummy = pd.DataFrame({
            "Item Name": ["Trà sữa chân châu", "Bia tiger", "Cơm chiên", "Gà rán KFC", "Panna cotta", "Yogurt trái cây", "Cookies cream"] * 20
        })
        dummy.to_csv(raw_csv_path, index=False)
        
    df = pd.read_csv(raw_csv_path)
    
    # Tiền xử lý
    preprocessor = TextPreprocessor()
    df['clean_text'] = df['Item Name'].apply(preprocessor.preprocess)
    
    # Gán nhãn Rule-based
    with open(keywords_path, 'r', encoding='utf-8') as f:
        keywords = json.load(f)
        
    import re
    compiled_patterns = {}
    for cat, kws in keywords.items():
        escaped_kws = [re.escape(kw.lower()) for kw in kws]
        pattern_str = r'(?:\b|^|\s)(' + '|'.join(escaped_kws) + r')(?:\b|$|\s)'
        compiled_patterns[cat] = re.compile(pattern_str)

    def rule_based_label(row):
        text = str(row['Item Name']).lower()
        clean = str(row['clean_text'])
        for cat, pattern in compiled_patterns.items():
            if pattern.search(text) or pattern.search(clean):
                return cat
        return "UNKNOWN_NEEDS_REVIEW"
        
    df['auto_label'] = df.apply(rule_based_label, axis=1)
    
    # Lưu kết quả auto_labeled
    os.makedirs(os.path.dirname(output_labeled_path), exist_ok=True)
    df.to_csv(output_labeled_path, index=False)
    print(f"Auto-labeled data saved to {output_labeled_path}")
    
    # Lọc ra các item cần review
    review_df = df[df['auto_label'] == 'UNKNOWN_NEEDS_REVIEW']
    review_path = '../data/to_review/needs_review.csv'
    os.makedirs(os.path.dirname(review_path), exist_ok=True)
    review_df.to_csv(review_path, index=False)
    print(f"Items needing manual review saved to {review_path}")

if __name__ == "__main__":
    prepare_data('../data/raw/raw_bills.csv', '../data/labeled/auto_labeled_bills.csv', '../config/keywords.json')
