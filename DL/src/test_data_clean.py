import pandas as pd
from classify import FoodClassifierPipeline

print("Loading Hybrid Classifier...")
clf = FoodClassifierPipeline(config_path="../config/keywords.json", model_dir="../data/model")

print("Loading data from Data Clean.xlsx (Sheet: T72026)...")
df = pd.read_excel('/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Data Clean.xlsx', sheet_name='T72026')

# Check column names to find the product name column
col_name = None
for col in ['Item Name', 'Product Name', 'Product', 'Name', 'Item']:
    if col in df.columns:
        col_name = col
        break

if not col_name:
    # If standard names not found, just use the first text-like column or print columns
    print("Columns available:", df.columns.tolist())
    # Assuming 'Product Name' or similar might be there under a different case
    for col in df.columns:
        if 'name' in str(col).lower() or 'item' in str(col).lower() or 'sản phẩm' in str(col).lower():
            col_name = col
            break

if not col_name:
    print("Could not identify the product name column!")
    exit(1)

print(f"Using column '{col_name}' for prediction...")

results = []
for idx, row in df.iterrows():
    product_name = str(row.get(col_name, ''))
    if product_name == 'nan' or not product_name.strip():
        continue
    
    price = 0.0 # Not used by our current XGBoost pipeline but required by predict_single signature
    pred_label, method, score = clf.predict_single(product_name, price)
    
    results.append({
        col_name: product_name,
        'Predicted Fine Label': pred_label,
        'Method': method,
        'Confidence Score': score
    })

res_df = pd.DataFrame(results)
out_path = '../data/output/Data_Clean_T72026_predicted.xlsx'
res_df.to_excel(out_path, index=False)
print(f"Predicted {len(res_df)} items. Saved results to {out_path}")
