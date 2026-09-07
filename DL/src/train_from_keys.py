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
from classify import TextPreprocessor

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"

def train_from_keys(excel_path, model_dir):
    print(f"Reading training data from {excel_path}")
    df = pd.read_excel(excel_path)
    
    df = df.dropna(subset=['Keyword', 'Mapped_Label'])
    
    print("Preprocessing text...")
    preprocessor = TextPreprocessor()
    df['clean_text'] = df['Keyword'].apply(preprocessor.preprocess)
    
    print("Label Encoding...")
    le = LabelEncoder()
    y = le.fit_transform(df['Mapped_Label'])
    
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(le, f"{model_dir}/label_encoder.pkl")
    
    print("Extracting features (TF-IDF + Semantic Vectors 768-dim)...")
    tfidf = TfidfVectorizer(max_features=2000, ngram_range=(1, 2))
    tfidf_features = tfidf.fit_transform(df['clean_text']).toarray()
    joblib.dump(tfidf, f"{model_dir}/tfidf_vectorizer.pkl")
    
    encoder = SentenceTransformer('keepitreal/vietnamese-sbert')
    semantic_features = encoder.encode(df['clean_text'].tolist(), show_progress_bar=True)
    
    X = np.hstack((tfidf_features, semantic_features))
    
    print("Training Hybrid XGBoost...")
    # Tắt train_test_split chia phức tạp vì đây là tập học, ta học toàn bộ
    xgb_model = xgb.XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=6, use_label_encoder=False, eval_metric='mlogloss', n_jobs=1)
    xgb_model.fit(X, y)
    
    print("Evaluating on Train set...")
    y_pred = xgb_model.predict(X)
    print(f"Accuracy: {accuracy_score(y, y_pred):.4f}")
    
    joblib.dump(xgb_model, f"{model_dir}/xgb_pipeline.pkl")
    print(f"Saved models to {model_dir}")

if __name__ == "__main__":
    train_from_keys(
        '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Potential_Keys_Mapped_BEV_FOOD.xlsx', 
        '../data/model'
    )
