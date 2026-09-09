import os
import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import xgboost as xgb
import json
from classify import TextPreprocessor

os.environ["TOKENIZERS_PARALLELISM"] = "false"

def train_with_price(csv_path, keywords_path, model_dir):
    print(f"Reading training data from {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Lấy tên món và giá
    df = df.dropna(subset=['Item Name', 'Item price clean'])
    
    # 1. Tự động gán nhãn bằng Bộ Luật Khổng Lồ (Rule-based) để tạo tập Train
    print("Auto-labeling data using Keywords (Rule-based)...")
    preprocessor = TextPreprocessor()
    df['clean_text'] = df['Item Name'].apply(preprocessor.preprocess)
    
    with open(keywords_path, 'r', encoding='utf-8') as f:
        keywords = json.load(f)
        
    import re
    all_keywords = []
    for cat, kws in keywords.items():
        for kw in kws:
            kw_lower = kw.lower()
            pattern = re.compile(r'(?:\b|^|\s)' + re.escape(kw_lower) + r'(?:\b|$|\s)')
            all_keywords.append((kw_lower, pattern, cat))
    
    # Sort by length descending
    all_keywords.sort(key=lambda x: len(x[0]), reverse=True)

    def rule_based_label(row):
        text = str(row['Item Name']).lower()
        clean = str(row['clean_text'])
        for kw_lower, pattern, cat in all_keywords:
            if pattern.search(text) or pattern.search(clean):
                return cat
        return "UNKNOWN"
        
    df['Mapped_Label'] = df.apply(rule_based_label, axis=1)
    
    # Chỉ giữ lại những món chắc chắn đúng để dạy cho AI
    train_df = df[df['Mapped_Label'] != "UNKNOWN"].copy()
    print(f"Sử dụng {len(train_df)} mẫu chuẩn xác để huấn luyện XGBoost...")
    
    # Xử lý giá tiền (Price)
    train_df['Price'] = pd.to_numeric(train_df['Item price clean'], errors='coerce').fillna(0.0)
    
    print("Label Encoding...")
    le = LabelEncoder()
    y = le.fit_transform(train_df['Mapped_Label'])
    
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(le, f"{model_dir}/label_encoder.pkl")
    
    print("Extracting features (TF-IDF Character N-Grams + Semantic Vectors)...")
    tfidf = TfidfVectorizer(max_features=2000, analyzer='char_wb', ngram_range=(2, 4))
    tfidf_features = tfidf.fit_transform(train_df['clean_text']).toarray()
    joblib.dump(tfidf, f"{model_dir}/tfidf_vectorizer.pkl")
    
    encoder = SentenceTransformer('keepitreal/vietnamese-sbert')
    semantic_features = encoder.encode(train_df['clean_text'].tolist(), show_progress_bar=True)
    
    # Hợp nhất: TF-IDF (2000) + Semantic (768)
    X = np.hstack((tfidf_features, semantic_features))
    
    print("Training Hybrid XGBoost WITHOUT PRICE feature...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)
    
    # [OPTIMIZATION] n_jobs=-1 uses all CPU cores. tree_method='hist' is 10x faster for large datasets.
    xgb_model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=4, eval_metric='mlogloss', n_jobs=-1, tree_method='hist')
    xgb_model.fit(X_train, y_train)
    
    print("Evaluating...")
    y_pred = xgb_model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    
    joblib.dump(xgb_model, f"{model_dir}/xgb_pipeline.pkl")
    print(f"Saved models to {model_dir}")

if __name__ == "__main__":
    train_with_price(
        '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Data Processed/bill_output_processed - brand.csv',
        '../config/keywords.json',
        '../data/model'
    )
