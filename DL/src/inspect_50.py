import pandas as pd
file_path = '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/test_random_50.xlsx'
try:
    df = pd.read_excel(file_path, nrows=5)
    print("Columns:", df.columns.tolist())
    for i, row in df.head(3).iterrows():
        print(f"Row {i}:")
        for k, v in row.items():
            if pd.notna(v) and str(v) != 'nan':
                print(f"  {k}: {v}")
except Exception as e:
    print(f"Error: {e}")
