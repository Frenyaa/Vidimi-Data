import pandas as pd
import json
import glob
import os

def merge_reviewed_data(reviewed_dir, auto_labeled_path, output_path, keywords_path):
    print("Merging user reviewed files...")
    reviewed_files = glob.glob(f"{reviewed_dir}/user_reviewed_*.csv")
    
    if not reviewed_files:
        print("No reviewed files found. Using auto_labeled data as sample_labels.")
        pd.read_csv(auto_labeled_path).to_csv(output_path, index=False)
        return
        
    dfs = [pd.read_csv(f) for f in reviewed_files]
    reviewed_df = pd.concat(dfs, ignore_index=True)
    
    auto_df = pd.read_csv(auto_labeled_path)
    
    # Merge logic (ghi đè nhãn auto bằng nhãn đã review)
    # Giả sử file review có cột 'Item Name' và 'final_label'
    if 'final_label' in reviewed_df.columns:
        merged_df = pd.merge(auto_df, reviewed_df[['Item Name', 'final_label']], on='Item Name', how='left')
        merged_df['Category'] = merged_df['final_label'].combine_first(merged_df['auto_label'])
        merged_df = merged_df[merged_df['Category'] != 'UNKNOWN_NEEDS_REVIEW']
        
        merged_df.to_csv(output_path, index=False)
        print(f"Final training dataset saved to {output_path}")
    else:
        print("Invalid reviewed file format (missing 'final_label')")

if __name__ == "__main__":
    merge_reviewed_data('../data/labeled', '../data/labeled/auto_labeled_bills.csv', '../data/labeled/sample_labels.csv', '../config/keywords.json')
