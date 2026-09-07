import pandas as pd
from classify import FoodClassifierPipeline

print("Loading Hybrid Classifier...")
clf = FoodClassifierPipeline(config_path="../config/keywords.json", model_dir="../models")

df = pd.read_excel('/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/test.xlsx')

results = []
for idx, row in df.iterrows():
    product_name = str(row.get('Product Name', ''))
    if product_name == 'nan' or not product_name:
        continue
    
    price = 0.0 # dummy
    pred_label, method, score = clf.predict_single(product_name, price)
    
    results.append({
        'Product Name': product_name,
        'Original Category': row.get('Product Category', ''),
        'Predicted Label': pred_label,
        'Method': method
    })

res_df = pd.DataFrame(results)
res_df.to_excel('../data/output/test_predicted.xlsx', index=False)
print("Saved predictions to ../data/output/test_predicted.xlsx")
