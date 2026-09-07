import pandas as pd
import re
from collections import Counter
import unicodedata
import sys
import os

# Import RuleBasedClassifier từ file rule_based_classifier.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from rule_based_classifier import RuleBasedClassifier

classifier = RuleBasedClassifier()

def clean_text(text):
    text = unicodedata.normalize('NFD', str(text).lower().strip())
    text = re.sub(r'[\u0300-\u036f]', '', text)
    text = text.replace('đ', 'd').replace('Đ', 'd')
    text = re.sub(r'[^\w\s]', ' ', text)
    return ' ' + ' '.join(text.split()) + ' '

def get_ngrams(text, n):
    words = text.split()
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

print("[+] Đang đọc file dữ liệu lớn...")
df = pd.read_csv('/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Data Processed/bill_output_processed - brand.csv')
texts = df['Item Name'].dropna().tolist()

print("[+] Đang trích xuất N-grams...")
unigrams = Counter()
bigrams = Counter()
trigrams = Counter()

for text in texts:
    cleaned = clean_text(text).strip()
    unigrams.update(get_ngrams(cleaned, 1))
    bigrams.update(get_ngrams(cleaned, 2))
    trigrams.update(get_ngrams(cleaned, 3))

print("[+] Đang phân loại các N-grams theo Dictionary BEV_/FOOD_ ...")
results = []
def process_counter(counter_obj, type_name):
    for k, v in counter_obj.most_common(5000):
        # Dùng bộ phân loại bạn đã tạo để gán nhãn cho từng từ khóa
        label, match_kw = classifier.classify(k)
        
        results.append({
            'Keyword': k,
            'Type': type_name,
            'Frequency': v,
            'Mapped_Label': label,
            'Matched_Rule': match_kw
        })

process_counter(unigrams, '1-từ')
process_counter(bigrams, '2-từ')
process_counter(trigrams, '3-từ')

out_df = pd.DataFrame(results)
# Sort để các từ được phân loại (khác UNKNOWN) lên đầu
out_df = out_df.sort_values(by=['Mapped_Label', 'Frequency'], ascending=[True, False])
out_path = '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Potential_Keys_Mapped_BEV_FOOD.xlsx'
out_df.to_excel(out_path, index=False)
print(f"[+] Hoàn tất! File đã được lưu tại: {out_path}")
