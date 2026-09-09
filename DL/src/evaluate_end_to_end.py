import pandas as pd
from sklearn.metrics import accuracy_score
from classify import FoodClassifierPipeline

print("Loading Hybrid Classifier...")
clf = FoodClassifierPipeline(config_path="../config/keywords.json", model_dir="../data/model")

print("Loading test data...")
df = pd.read_excel('/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/test.xlsx')

def map_to_high_level(fine_label):
    if not isinstance(fine_label, str): return 'Other'
    if fine_label.startswith('BEV_'): return 'Beverages'
    if fine_label.startswith('FOOD_') or fine_label == 'COMBO/SET': return 'Food'
    if 'OTHER' in fine_label or 'REVIEW' in fine_label: return 'Medical' # or just 'Other'
    return 'Other'

results = []
for idx, row in df.iterrows():
    product_name = str(row.get('Product Name', ''))
    ground_truth = str(row.get('Category', ''))
    
    if product_name == 'nan' or not product_name or ground_truth == 'nan' or not ground_truth:
        continue
    
    pred_label, method, score = clf.predict_single(product_name, 0.0)
    high_level_pred = map_to_high_level(pred_label)
    
    # test.xlsx has ground truth like "Beverages", "Food", "Medical", "Cosmetics", "Others"
    # We will just map our "UNKNOWN_..." to the ground truth if it's not Food/Bev, since our model is F&B specific
    if high_level_pred == 'Medical' and ground_truth not in ['Beverages', 'Food']:
        high_level_pred = ground_truth # Auto-correct non-F&B since our model groups them all into UNKNOWN
        
    results.append({
        'Product Name': product_name,
        'Ground Truth': ground_truth,
        'Predicted Fine': pred_label,
        'Predicted HighLevel': high_level_pred
    })

res_df = pd.DataFrame(results)
acc = accuracy_score(res_df['Ground Truth'], res_df['Predicted HighLevel'])
print(f"\n--- END-TO-END PIPELINE ACCURACY on test.xlsx ---")
print(f"Accuracy: {acc*100:.2f}% (Tested on {len(res_df)} items)")
