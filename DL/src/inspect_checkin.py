import pandas as pd
file_path = '/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Du-Lieu-Check-In.1788433372.xls'
try:
    df = pd.read_excel(file_path, nrows=5)
    print("Columns:")
    print(df.columns.tolist())
    print("\nFirst 3 rows:")
    for i, row in df.head(3).iterrows():
        print(f"Row {i}:")
        for k, v in row.items():
            if pd.notna(v) and str(v) != 'nan':
                print(f"  {k}: {v}")
except Exception as e:
    print(f"Error: {e}")
