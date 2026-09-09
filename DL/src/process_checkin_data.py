import pandas as pd
from classify import FoodClassifierPipeline
import warnings
warnings.filterwarnings('ignore')

input_file = '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Du-Lieu-Check-In.1788433372.xls'
output_file = '/Users/buidoanhaiyen/Documents/Vidimi/Code/DL/data/output/Du-Lieu-Check-In_predicted.xlsx'

print(f"Reading input file: {input_file}")
df = pd.read_excel(input_file)

def parse_items(text):
    if pd.isna(text):
        return []
    items = []
    # Tách bằng "name: " vì mỗi món đều bắt đầu bằng chuỗi này
    lines = str(text).split('name: ')
    for line in lines:
        if not line.strip(): 
            continue
        # Dòng sẽ có dạng: "LONG TỈNH, slg: 1, price: 55000"
        if ", slg: " in line:
            parts = line.split(", slg: ")
            name = parts[0].strip()
            rest = parts[1]
            if ", price: " in rest:
                slg_part, price_part = rest.split(", price: ")
                slg = slg_part.strip()
                price = price_part.strip()
                items.append({'Item Name': name, 'Quantity': slg, 'Price': price})
    return items

print("Parsing and exploding 'Items' column...")
# Extract list of dicts
df['parsed_items'] = df['Items'].apply(parse_items)

# Explode the list of dicts into separate rows
df_exploded = df.explode('parsed_items').copy()
df_exploded = df_exploded.dropna(subset=['parsed_items'])

# Extract keys from dict into columns
df_exploded['Item Name'] = df_exploded['parsed_items'].apply(lambda x: x.get('Item Name'))
df_exploded['Quantity'] = df_exploded['parsed_items'].apply(lambda x: x.get('Quantity'))
df_exploded['Price'] = df_exploded['parsed_items'].apply(lambda x: x.get('Price'))

# Drop the temporary column and the original 'Items' column
df_exploded = df_exploded.drop(columns=['parsed_items', 'Items'])

print(f"Extracted {len(df_exploded)} individual items. Loading Classifier...")

# Initialize Classifier
clf = FoodClassifierPipeline(config_path="../config/keywords.json", model_dir="../data/model")

print("Classifying items...")
predictions = []
for idx, row in df_exploded.iterrows():
    name = str(row['Item Name'])
    price = 0.0
    try:
        price = float(row['Price'])
    except:
        pass
    
    pred_label, method, score = clf.predict_single(name, price)
    predictions.append({
        'Predicted Fine Label': pred_label,
        'Method': method,
        'Confidence Score': score
    })

# Attach predictions
pred_df = pd.DataFrame(predictions, index=df_exploded.index)
final_df = pd.concat([df_exploded, pred_df], axis=1)

print(f"Saving predicted data to {output_file}...")
final_df.to_excel(output_file, index=False)
print("Done!")
