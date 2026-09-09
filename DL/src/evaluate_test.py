import pandas as pd
from sklearn.metrics import accuracy_score
from classify import FoodClassifierPipeline
import warnings
warnings.filterwarnings('ignore')

print("Loading Hybrid Classifier...")
clf = FoodClassifierPipeline(config_path="../config/keywords.json", model_dir="../data/model")

print("Loading test data...")
df = pd.read_excel('/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/test.xlsx')

results = []
for idx, row in df.iterrows():
    product_name = str(row.get('Product Name', ''))
    ground_truth = str(row.get('Product Category', ''))
    
    if product_name == 'nan' or not product_name or ground_truth == 'nan' or not ground_truth:
        continue
    
    price = 0.0 # dummy
    pred_label, method, score = clf.predict_single(product_name, price)
    
    results.append({
        'Product Name': product_name,
        'Product Category': row.get('Product Category', ''),
        'Ground Truth': ground_truth,
        'Predicted Label': pred_label,
        'Method': method
    })

res_df = pd.DataFrame(results)

# Calculate Accuracy
valid_idx = res_df['Ground Truth'].notna() & res_df['Predicted Label'].notna() & (res_df['Ground Truth'] != 'nan')
df_valid = res_df[valid_idx]
acc = accuracy_score(df_valid['Ground Truth'].str.strip(), df_valid['Predicted Label'].str.strip())

res_df.to_excel('../data/output/test_predicted.xlsx', index=False)
print("Saved predictions to ../data/output/test_predicted.xlsx")
print(f"Overall Pipeline Accuracy on test.xlsx: {acc:.4f}")
