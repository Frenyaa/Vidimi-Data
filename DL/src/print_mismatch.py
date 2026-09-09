import pandas as pd

df = pd.read_excel('/Users/buidoanhaiyen/Documents/Vidimi/Code/DL/data/output/test_random_50_predicted.xlsx')
df_valid = df.dropna(subset=['Mapped Ground Truth'])

print("Mismatched Items:")
mismatches = df_valid[df_valid['Mapped Ground Truth'] != df_valid['Predicted Label']]
for idx, row in mismatches.iterrows():
    print(f"- {row['Product Name']}\n  GT: {row['Mapped Ground Truth']} | Pred: {row['Predicted Label']} | Method: {row['Method']}")
    
print("\nUnmapped Ground Truths:")
unmapped = df[df['Mapped Ground Truth'].isna()]
for cat in unmapped['Original Category'].unique():
    print(f"- {cat}")
