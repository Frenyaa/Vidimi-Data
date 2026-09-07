import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
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

def train_system_pipeline(csv_path, model_dir):
    print(f"Reading data from {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Giả định cột text là 'Item Name' và nhãn là 'Category'
    text_col = 'Item Name' if 'Item Name' in df.columns else df.columns[0]
    label_col = 'Category' if 'Category' in df.columns else df.columns[1]
    
    df = df.dropna(subset=[text_col, label_col])
    
    print("Preprocessing text...")
    preprocessor = TextPreprocessor()
    df['clean_text'] = df[text_col].apply(preprocessor.preprocess)
    
    print("Label Encoding...")
    le = LabelEncoder()
    y = le.fit_transform(df[label_col])
    
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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    xgb_model = xgb.XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=6, use_label_encoder=False, eval_metric='mlogloss', n_jobs=1)
    xgb_model.fit(X_train, y_train)
    
    print("Evaluating...")
    y_pred = xgb_model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    
    joblib.dump(xgb_model, f"{model_dir}/xgb_pipeline.pkl")
    print(f"Saved models to {model_dir}")

if __name__ == "__main__":
    train_system_pipeline('../data/labeled/sample_labels.csv', '../data/model')
