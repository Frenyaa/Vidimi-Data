import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
import json
import re
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import xgboost as xgb
import joblib
from underthesea import word_tokenize
import unicodedata
import os

class TextPreprocessor:
    def __init__(self):
        self.correction_dict = {
            "chan ga": "chân gà", "nem gion": "nem giòn", "xuc xich": "xúc xích",
            "banh bouchee": "bánh bouchee", "com": "cơm", "suon": "sườn",
            "nuoc": "nước", "ep": "ép", "nac neo": "nạc heo",
            "ot chuong": "ớt chuông", "ốt chuông": "ớt chuông"
        }
    def normalize_unicode(self, text):
        return unicodedata.normalize('NFC', str(text))
    def remove_units(self, text):
        pattern = r'\b(\d+)?\s*(kg|g|cái|lon|chai|ml|pack|hộp|túi|gr|l)\b'
        return re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
    def correct_spelling(self, text):
        for wrong, correct in self.correction_dict.items():
            text = text.replace(wrong, correct)
        return text
    def preprocess(self, text):
        text = self.normalize_unicode(text.lower().strip())
        text = self.correct_spelling(text)
        text = self.remove_units(text)
        tokenized_text = word_tokenize(text, format="text")
        return re.sub(r'\s+', ' ', tokenized_text).strip()

class FoodClassifierPipeline:
    def __init__(self, config_path, model_dir):
        self.preprocessor = TextPreprocessor()
        # Compile rule-based dictionary and sort by length (longest match first)
        with open(config_path, 'r', encoding='utf-8') as f:
            self.keywords = json.load(f)
            
        self.all_keywords = []
        for cat, kws in self.keywords.items():
            for kw in kws:
                kw_lower = kw.lower()
                pattern = re.compile(r'(?:\b|^|\s)' + re.escape(kw_lower) + r'(?:\b|$|\s)')
                self.all_keywords.append((kw_lower, pattern, cat))
        
        # Sort by length descending to match "rau câu dừa" before "dừa"
        self.all_keywords.sort(key=lambda x: len(x[0]), reverse=True)
            
        print("Loading Deep Learning Model (PhoBERT 768-dim)...")
        import torch
        device = 'mps' if torch.backends.mps.is_available() else 'cpu'
        self.embedding_model = SentenceTransformer('keepitreal/vietnamese-sbert', device=device)
        self.category_prototypes = self._compute_prototypes()
        
        try:
            self.xgb_model = joblib.load(f"{model_dir}/xgb_pipeline.pkl")
            self.label_encoder = joblib.load(f"{model_dir}/label_encoder.pkl")
            self.tfidf = joblib.load(f"{model_dir}/tfidf_vectorizer.pkl")
            self.has_ml_model = True
        except FileNotFoundError:
            self.has_ml_model = False

    def _compute_prototypes(self):
        prototypes = {}
        for category, kws in self.keywords.items():
            if kws:
                # Giới hạn lấy 100 keyword đại diện để tính prototype cho nhanh
                sample_kws = kws[:100]
                processed_kws = [self.preprocessor.preprocess(kw) for kw in sample_kws]
                embeddings = self.embedding_model.encode(processed_kws, show_progress_bar=False)
                prototypes[category] = np.mean(embeddings, axis=0)
        return prototypes

    def get_rule_based_prediction(self, original_name, clean_name):
        original_lower = original_name.lower()
        # Duyệt qua các pattern đã compile (đã sắp xếp theo độ dài keyword giảm dần)
        for kw_lower, pattern, cat in self.all_keywords:
            if pattern.search(original_lower) or pattern.search(clean_name):
                return cat
        return "UNKNOWN_NEED_ML_MODEL"

    def predict_single(self, text, price=0.0):
        clean_text = self.preprocessor.preprocess(text)
        rule_pred = self.get_rule_based_prediction(text, clean_text)
        if rule_pred != "UNKNOWN_NEED_ML_MODEL":
            return rule_pred, "1. Rule-based (HIGH_CONFIDENCE)", clean_text
                
        text_vector = self.embedding_model.encode([clean_text])[0]
        max_sim, best_category = -1, None
        
        for category, proto_vec in self.category_prototypes.items():
            sim = cosine_similarity([text_vector], [proto_vec])[0][0]
            if sim > max_sim:
                max_sim, best_category = sim, category
                
        if max_sim >= 0.65:
            return best_category, f"2. Semantic Match (Sim: {max_sim:.2f})", clean_text
            
        if self.has_ml_model:
            tfidf_vec = self.tfidf.transform([clean_text]).toarray()
            price_arr = np.array([[float(price)]])
            combined_vec = np.hstack((tfidf_vec, [text_vector], price_arr))
            probs = self.xgb_model.predict_proba(combined_vec)[0]
            pred_idx = np.argmax(probs)
            return self.label_encoder.inverse_transform([pred_idx])[0], f"3. Hybrid XGBoost (Prob: {probs[pred_idx]:.2f})", clean_text
            
        return "UNKNOWN_OTHER", f"LOW_CONFIDENCE (Max Sim: {max_sim:.2f})", clean_text

    def predict_batch(self, texts, prices):
        clean_texts = [self.preprocessor.preprocess(t) for t in texts]
        
        results = [{"cat": None, "method": None, "clean": clean} for clean in clean_texts]
        unresolved_idx = []
        for i, (orig, clean) in enumerate(zip(texts, clean_texts)):
            orig_lower = orig.lower()
            matched = False
            for kw_lower, pattern, cat in self.all_keywords:
                if pattern.search(orig_lower) or pattern.search(clean):
                    results[i]["cat"] = cat
                    results[i]["method"] = "1. Rule-based (HIGH_CONFIDENCE)"
                    matched = True
                    break
            if not matched:
                unresolved_idx.append(i)
                
        # 3. Batch encode remaining using PhoBERT
        if unresolved_idx:
            unresolved_texts = [clean_texts[i] for i in unresolved_idx]
            embeddings = self.embedding_model.encode(unresolved_texts, show_progress_bar=False)
            
            # 4. Semantic and XGBoost for unresolved
            if self.has_ml_model:
                tfidf_vecs = self.tfidf.transform(unresolved_texts).toarray()
                prices_arr = np.array([[float(prices[i])] for i in unresolved_idx])
                combined_vecs = np.hstack((tfidf_vecs, embeddings, prices_arr))
                probs_batch = self.xgb_model.predict_proba(combined_vecs)
                preds = np.argmax(probs_batch, axis=1)
                labels = self.label_encoder.inverse_transform(preds)
            
            for local_i, global_i in enumerate(unresolved_idx):
                max_sim, best_category = -1, None
                text_vector = embeddings[local_i]
                for category, proto_vec in self.category_prototypes.items():
                    sim = cosine_similarity([text_vector], [proto_vec])[0][0]
                    if sim > max_sim:
                        max_sim, best_category = sim, category
                
                if max_sim >= 0.65:
                    results[global_i]["cat"] = best_category
                    results[global_i]["method"] = f"2. Semantic Match (Sim: {max_sim:.2f})"
                elif self.has_ml_model:
                    prob = probs_batch[local_i][preds[local_i]]
                    results[global_i]["cat"] = labels[local_i]
                    results[global_i]["method"] = f"3. Hybrid XGBoost (Prob: {prob:.2f})"
                else:
                    results[global_i]["cat"] = "UNKNOWN_OTHER"
                    results[global_i]["method"] = f"LOW_CONFIDENCE (Max Sim: {max_sim:.2f})"
                    
        return [(r["cat"], r["method"], r["clean"]) for r in results]

if __name__ == "__main__":
    pipeline = FoodClassifierPipeline('../config/keywords.json', '../data/model')
    test_items = ["xoài uc 1kg", "chan ga OGARI 500g", "pepsi lon 330ml", "thịt bò kobe nhập khẩu"]
    for text in test_items:
        cat, method, clean = pipeline.predict_single(text)
        print(f"{text} -> {clean} -> {cat} ({method})")
