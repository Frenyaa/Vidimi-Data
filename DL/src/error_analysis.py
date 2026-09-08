import pandas as pd

df = pd.read_excel('../data/output/test_rule_results_new_predicted.xlsx')

cat_map = {
    'Rau củ': 'FOOD_RAU_CU_QUA', 'Trái cây': 'FOOD_RAU_CU_QUA', 'Nấm': 'FOOD_RAU_CU_QUA',
    'Thịt heo': 'FOOD_THIT_CA', 'Thịt gà': 'FOOD_THIT_CA', 'Thịt bò': 'FOOD_THIT_CA',
    'Cá': 'FOOD_THIT_CA', 'Hải sản': 'FOOD_THIT_CA', 'Nghêu, sò, ...': 'FOOD_THIT_CA',
    'Nghều, sò, ...': 'FOOD_THIT_CA', 'Trứng': 'FOOD_THIT_CA',
    'Bánh kẹo': 'FOOD_SNACK', 'Snack': 'FOOD_SNACK',
    'Thuốc': 'UNKNOWN_OTHER', 'Thực phẩm chức năng': 'UNKNOWN_OTHER',
    'Dung dịch vệ sinh /y tế': 'UNKNOWN_OTHER', 'Dụng cụ y tế hỗ trợ': 'UNKNOWN_OTHER',
    'Khăn ướt': 'UNKNOWN_OTHER', 'Khăn lạnh': 'UNKNOWN_OTHER', 'Khăn': 'UNKNOWN_OTHER',
    'Mũ': 'UNKNOWN_OTHER', 'Tiền điện tử': 'UNKNOWN_OTHER', 'Games': 'UNKNOWN_OTHER',
    'Giày dép': 'UNKNOWN_OTHER', 'Túi': 'UNKNOWN_OTHER', 'Sách giáo dục': 'UNKNOWN_OTHER',
    'Áo': 'UNKNOWN_OTHER', 'Đầm': 'UNKNOWN_OTHER', 'Váy': 'UNKNOWN_OTHER',
    'Quần': 'UNKNOWN_OTHER', 'Bút vở': 'UNKNOWN_OTHER', 'Dịch vụ phòng': 'UNKNOWN_OTHER',
    'Ngân hàng': 'UNKNOWN_OTHER', 'Dầu gội': 'UNKNOWN_OTHER', 'Sữa tắm': 'UNKNOWN_OTHER',
    'Tẩy trang': 'UNKNOWN_OTHER', 'Nước giặt': 'UNKNOWN_OTHER', 'Nước hoa': 'UNKNOWN_OTHER',
    'Dao cạo râu': 'UNKNOWN_OTHER', 'Điện thoại di động': 'UNKNOWN_OTHER',
    'Dụng cụ ăn uống': 'UNKNOWN_OTHER', 'Hộp': 'UNKNOWN_OTHER',
    'Chứng khoán': 'UNKNOWN_OTHER', 'Kem đánh răng': 'UNKNOWN_OTHER',
    'Sữa chống nắng': 'UNKNOWN_OTHER',
    'Gia vị': 'FOOD_OTHER', 'Combo/Set': 'COMBO/SET', 'Combo /Set': 'COMBO/SET',
    'Mì gói': 'FOOD_AN_SAN', 'Mì': 'FOOD_AN_SAN', 'Món sợi': 'FOOD_AN_SAN',
    'Xôi': 'FOOD_AN_SAN', 'Cơm': 'FOOD_AN_SAN', 'Gạo': 'FOOD_AN_SAN',
    'Sữa tươi': 'BEV_SUA_TUOI'
}

df['Expected Label'] = df['Product Category'].map(cat_map)

# Filter where Expected Label is known, but Prediction is different, AND prediction is NOT low confidence
errors = df[(df['Expected Label'].notna()) & 
            (df['Predicted Label'] != df['Expected Label']) & 
            (~df['Predicted Label'].str.contains('UNKNOWN'))]

print(f"Found {len(errors)} potential logical errors where HIGH CONFIDENCE prediction conflicts with expected mapped category.")
print("Top error examples:")
print(errors[['Product Name', 'Product Category', 'Predicted Label', 'Expected Label', 'Method']].head(30).to_string())

# Xem thử những từ khóa nào gây ra lỗi nhiều nhất
print("\nMost common wrong predictions:")
print(errors.groupby(['Expected Label', 'Predicted Label']).size().sort_values(ascending=False).head(20))
