import os
import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import xgboost as xgb
from modAL.models import ActiveLearner
from modAL.uncertainty import uncertainty_sampling
from classify import TextPreprocessor
import json

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

def train_active_learning(csv_path, keywords_path, model_dir):
    print(f"Reading training data for Active Learning from {csv_path}")
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=['Item Name', 'Item price clean'])
    
    print("Đang tiến hành dọn dẹp văn bản (NLP Preprocessing)...")
    from tqdm import tqdm
    tqdm.pandas(desc="Dọn dẹp văn bản")
    preprocessor = TextPreprocessor()
    df['clean_text'] = df['Item Name'].progress_apply(preprocessor.preprocess)
    
    with open(keywords_path, 'r', encoding='utf-8') as f:
        keywords = json.load(f)
        
    import re
    compiled_rules = {}
    for cat, kws in keywords.items():
        if not kws: continue
        kws_escaped = [re.escape(kw.lower()) for kw in kws]
        pattern = r'(?:\b|^|\s)(' + '|'.join(kws_escaped) + r')(?:\b|$|\s)'
        compiled_rules[cat] = re.compile(pattern)

    def rule_based_label(row):
        text = str(row['Item Name']).lower()
        clean = str(row['clean_text'])
        for cat, compiled_regex in compiled_rules.items():
            if compiled_regex.search(text) or compiled_regex.search(clean):
                return cat
        return "UNKNOWN"
        
    df['Mapped_Label'] = df.apply(rule_based_label, axis=1)
    train_df = df[df['Mapped_Label'] != "UNKNOWN"].copy()
    pool_df = df[df['Mapped_Label'] == "UNKNOWN"].copy() # Dữ liệu chưa biết để AI chủ động hỏi (Query Pool)
    
    train_df['Price'] = pd.to_numeric(train_df['Item price clean'], errors='coerce').fillna(0.0)
    pool_df['Price'] = pd.to_numeric(pool_df['Item price clean'], errors='coerce').fillna(0.0)
    
    le = LabelEncoder()
    y_train = le.fit_transform(train_df['Mapped_Label'])
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(le, f"{model_dir}/label_encoder.pkl")
    
    print("Extracting TF-IDF 2000-dim...")
    tfidf = TfidfVectorizer(max_features=2000, ngram_range=(1, 2))
    tfidf_features_train = tfidf.fit_transform(train_df['clean_text']).toarray()
    joblib.dump(tfidf, f"{model_dir}/tfidf_vectorizer.pkl")
    
    print("Khởi chạy PhoBERT (Mở tốc độ cao MPS / GPU nếu có)...")
    import torch
    device = 'mps' if torch.backends.mps.is_available() else 'cpu'
    encoder = SentenceTransformer('keepitreal/vietnamese-sbert', device=device)
    
    print("Extracting PhoBERT 768-dim cho tập huấn luyện...")
    semantic_train = encoder.encode(train_df['clean_text'].tolist(), show_progress_bar=True, batch_size=256)
    
    price_train = train_df['Price'].values.reshape(-1, 1)
    X_train = np.hstack((tfidf_features_train, semantic_train, price_train))
    
    print("Khởi tạo ActiveLearner (modAL) với XGBoost...")
    estimator = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=6, use_label_encoder=False, eval_metric='mlogloss', n_jobs=1)
    
    learner = ActiveLearner(
        estimator=estimator,
        query_strategy=uncertainty_sampling,
        X_training=X_train, y_training=y_train
    )
    
    print("Mô hình đã học ban đầu. Lưu ActiveLearner...")
    joblib.dump(learner.estimator, f"{model_dir}/xgb_pipeline.pkl")
    
    if len(pool_df) > 0:
        print(f"Tiến hành Active Learning: Lọc ra các câu hỏi khó nhất từ {len(pool_df)} dữ liệu UNKNOWN...")
        tfidf_pool = tfidf.transform(pool_df['clean_text']).toarray()
        semantic_pool = encoder.encode(pool_df['clean_text'].tolist(), show_progress_bar=True, batch_size=256)
        price_pool = pool_df['Price'].values.reshape(-1, 1)
        X_pool = np.hstack((tfidf_pool, semantic_pool, price_pool))
        
        # modAL tự động chọn ra N mẫu mà nó bối rối nhất
        n_queries = 20
        query_idx, query_inst = learner.query(X_pool, n_instances=n_queries)
        
        uncertain_samples = pool_df.iloc[query_idx][['Bill ID', 'Item Name', 'Item price clean']]
        uncertain_samples['Human_Label'] = "" # Để trống cho con người điền trên Google Sheets
        
        review_path = '../data/to_review/active_learning_queries.csv'
        os.makedirs('../data/to_review', exist_ok=True)
        uncertain_samples.to_csv(review_path, index=False)
        print(f"Đã xuất {n_queries} mẫu khó nhất ra {review_path} để Review bằng Google Sheets!")
    
if __name__ == "__main__":
    train_active_learning(
        '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Data Processed/bill_output_processed - brand.csv',
        '../config/keywords.json',
        '../data/model'
    )
