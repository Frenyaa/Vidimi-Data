import pandas as pd
from classify import FoodClassifierPipeline

input_file = '../data/output/test_rule_results_new_predicted.xlsx'
output_file = '../data/output/test_rule_results_new_predicted.xlsx'

print(f"Reading {input_file}...")
df = pd.read_excel(input_file)

# Khởi tạo pipeline
print("Loading model pipeline...")
pipeline = FoodClassifierPipeline(
    model_dir="../data/model",
    config_path="../config/keywords.json"
)

# Chạy dự đoán
print("Predicting batch...")
texts = df['Product Name'].tolist()
prices = [0.0] * len(texts)

results = pipeline.predict_batch(texts, prices)

# results is a list of tuples: (cat, method, clean_text)
df['Predicted Label'] = [res[0] for res in results]
df['Method'] = [res[1] for res in results]
df['Clean Text'] = [res[2] for res in results]

print(f"Saving to {output_file}...")
df.to_excel(output_file, index=False)
print("Done!")
