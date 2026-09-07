import pandas as pd
import re
from collections import Counter
import unicodedata

def clean_text(text):
    text = unicodedata.normalize('NFD', str(text).lower().strip())
    text = re.sub(r'[\u0300-\u036f]', '', text)
    text = text.replace('đ', 'd').replace('Đ', 'd')
    text = re.sub(r'[^\w\s]', ' ', text)
    return text

def get_ngrams(text, n):
    words = text.split()
    return [' '.join(words[i:i+n]) for i in range(len(words)-n+1)]

print("[+] Đang đọc file dữ liệu lớn...")
df = pd.read_csv('/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Data Processed/bill_output_processed - brand.csv')
texts = df['Item Name'].dropna().tolist()

print("[+] Đang phân tích và trích xuất N-grams (1-từ, 2-từ, 3-từ)...")
unigrams = Counter()
bigrams = Counter()
trigrams = Counter()

for text in texts:
    cleaned = clean_text(text)
    unigrams.update(get_ngrams(cleaned, 1))
    bigrams.update(get_ngrams(cleaned, 2))
    trigrams.update(get_ngrams(cleaned, 3))

print("[+] Đang lưu kết quả ra file...")
# Kết hợp lại thành 1 list
results = []
for k, v in unigrams.most_common(2000):
    results.append({'Keyword': k, 'Type': '1-từ', 'Frequency': v})
for k, v in bigrams.most_common(2000):
    results.append({'Keyword': k, 'Type': '2-từ', 'Frequency': v})
for k, v in trigrams.most_common(2000):
    results.append({'Keyword': k, 'Type': '3-từ', 'Frequency': v})

out_df = pd.DataFrame(results)
out_path = '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Potential_Keys_For_Classification.xlsx'
out_df.to_excel(out_path, index=False)
print(f"[+] Hoàn tất! File đã được lưu tại: {out_path}")
