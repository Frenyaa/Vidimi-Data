import re

# Từ điển ánh xạ Mã Nhãn Chuẩn (từ hình ảnh cung cấp) với bộ Keywords tương ứng
RULE_BASED_KEYWORDS = {
    # ------------------ NHÓM ĐỒ UỐNG (BEV_) ------------------
    "BEV_CAFE": [
        "cà phê", "ca phe", "cafe", "coffee", "bạc xỉu", "bac xiu", 
        "latte", "espresso", "cold brew", "phin", "americano", "capuchino", "mocha"
    ],
    "BEV_TRA_SUA": [
        "trà sữa", "tra sua", "milk tea", "trân châu", "tran chau", 
        "boba", "thạch đào", "macchiato", "tiger sugar", "bubble tea", "topping"
    ],
    "BEV_TRA": [
        "trà sen vàng", "trà đào", "trà chanh", "trà tắc", "trà lài",
        "trà xanh", "trà sen", "trà hoa", "lục trà", "hồng trà", "trà ổi",
        "tea", "trà", "tra" # Chú ý: Các từ khóa chung nên để cuối hoặc cần xử lý thứ tự ưu tiên
    ],
    "BEV_NUOC_NGOT": [
        "coca", "pepsi", "sprite", "fanta", "7up", "mirinda", "soda",
        "nước ngọt", "nuoc ngot", "có ga", "schweppes"
    ],
    "BEV_TANG_LUC": [
        "red bull", "sting", "number 1", "number one", "warrior", "monster",
        "tăng lực", "tang luc", "bò húc"
    ],
    "BEV_NUOC_KHOANG": [
        "lavie", "aquafina", "dasani", "vĩnh hảo", "thạch bích",
        "nước khoáng", "nuoc khoang", "nước suối", "nuoc suoi", "nước lọc"
    ],
    "BEV_SUA_TUOI": [
        "milo", "vinamilk", "fami", "sữa lúa mạch", "sữa tươi", "sua tuoi",
        "sữa hạt", "sua hat", "ovaltine", "th true", "sữa tiệt trùng", "sữa đậu"
    ],
    "BEV_NUOC_EP": [
        "ép cam", "dừa xiêm", "cocoxim", "nước mía", "chanh đá",
        "nước ép", "nuoc ep", "nước dừa", "juice", "vfresh", "tropicana"
    ],
    "BEV_SINH_TO": [
        "sinh tố", "sinh to", "smoothie"
    ],
    "BEV_DA_XAY": [
        "đá xay", "da xay", "freeze", "frappuccino", "matcha đá xay", "ice blended"
    ],
    "BEV_BIA": [
        "tiger", "heineken", "333", "bia sài gòn", "bia saigon", "budweiser",
        "bia", "beer", "strongbow", "corona", "larue"
    ],
    "BEV_RUOU": [
        "rượu vang", "vodka", "whisky", "chivas", "soju", "sake",
        "rượu", "ruou", "wine"
    ],

    # ------------------ NHÓM ĐỒ ĂN (FOOD_) ------------------
    "FOOD_TINH_BOT": [
        "bánh mì", "banh mi", "cơm tấm", "com tam", "bún", "bun", 
        "phở", "pho", "mì gói", "mi goi", "spaghetti", "khoai tây chiên", 
        "cơm", "com", "mì", "mi", "cháo", "chao", "xôi", "xoi", "nui", "bún thịt nướng", "bún chả"
    ],
    "FOOD_RAU_CU_QUA": [
        "rau muống", "cà chua", "cà rốt", "cải thảo", "khổ qua", "xoài", "dưa hấu",
        "rau", "củ", "trái cây", "salad", "nấm", "kim chi", "rong biển", "khoai tây", "khoai lang", "ớt", "chuối"
    ],
    "FOOD_THIT_CA": [
        "thịt bò", "thịt heo", "thịt gà", "chim cút", "trứng lòng đào", 
        "cá", "tôm", "mực", "cua", "ghẹ", "ốc", "hải sản", "trứng", "thịt", "bò", "gà", "heo", "nạc", "nạc bò", "nạc heo"
    ],
    "FOOD_AN_SAN": [
        "gà rán", "fried chicken", "nuggets", "nugget", "pizza", "cơm trộn", "lẩu gà", "há cảo", "nem nướng", "burger",
        "dimsum", "lẩu", "nướng", "bbq", "kfc", "bánh xèo"
    ],
    "FOOD_SNACK": [
        "oishi", "bim bim", "bánh đậu xanh", "bánh quy", "kẹo dẻo", "hạt điều",
        "snack", "kẹo", "bánh", "hạt", "socola", "lay's", "rau câu", "thạch", "bông lan"
    ],
    "FOOD_SUA_AN": [
        "sữa chua ăn", "sữa chua", "phô mai", "kem que", "kem hộp", "bơ", "kem"
    ],
    "FOOD_KHO_GIA_VI": [
        "xúc xích", "nước mắm", "tương ớt", "dầu ăn", "pate", "kim chi", "hạt nêm",
        "gia vị", "sốt", "tương", "muối", "mì chính", "bột ngọt"
    ],

    # ------------------ NHÓM KHÁC (OTHER) ------------------
    "FOOD_OTHER": [
        "khăn lạnh", "khăn giấy", "hộp mang về", "ly nhựa", "vé", "phí dịch vụ",
        "thuốc lá", "quẹt", "đồ chơi", "túi nilong", "vat", "phụ thu", "ship", "vận chuyển",
        "sữa tắm", "nước hoa", "dầu gội"
    ]
}

class RuleBasedClassifier:
    def __init__(self, keywords_dict=None, standard_file_path=None):
        if keywords_dict is not None:
            self.keywords_dict = keywords_dict
        elif standard_file_path is not None:
            self.keywords_dict = self.load_keywords_from_file(standard_file_path)
        else:
            self.keywords_dict = RULE_BASED_KEYWORDS
            
        # Tự động sinh thêm từ khóa không dấu và viết tắt
        self.augment_keywords()
            
    def load_keywords_from_file(self, file_path):
        """Đọc file tiêu chuẩn (CSV/Excel) để tự động tạo dictionary"""
        import pandas as pd
        print(f"[+] Đang nạp từ điển từ file: {file_path}")
        if str(file_path).endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # Hỗ trợ tên cột linh hoạt (loại bỏ khoảng trắng thừa, viết hoa thường)
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # Tìm cột tương ứng
        label_col = next((c for c in df.columns if 'mã' in c or 'mã nhãn' in c or 'code' in c), None)
        example_col = next((c for c in df.columns if 'ví dụ' in c or 'từ khóa' in c or 'keyword' in c or 'mặt' in c), None)
        
        if not label_col or not example_col:
            raise ValueError(f"Không tìm thấy cột 'Mã nhãn chuẩn' hoặc 'Ví dụ mặt hàng' trong file {file_path}")
            
        generated_dict = {}
        for _, row in df.dropna(subset=[label_col, example_col]).iterrows():
            label = str(row[label_col]).strip()
            # Tách các từ khóa bởi dấu phẩy, chấm phẩy hoặc dấu gạch
            raw_examples = str(row[example_col]).replace(';', ',').split(',')
            
            # Xử lý: loại bỏ khoảng trắng thừa, chuyển thành chữ thường
            keywords = [self.clean_text(kw) for kw in raw_examples if kw.strip()]
            
            if label not in generated_dict:
                generated_dict[label] = []
            generated_dict[label].extend(keywords)
            
        print(f"[+] Đã nạp thành công {len(generated_dict)} danh mục từ file.")
        return generated_dict
        
    def remove_accents(self, text):
        import unicodedata
        text = unicodedata.normalize('NFD', str(text))
        text = re.sub(r'[\\u0300-\\u036f]', '', text)
        text = text.replace('đ', 'd').replace('Đ', 'd')
        return text

    def get_abbreviation(self, text):
        words = text.split()
        if len(words) > 1:
            return ''.join([w[0] for w in words if w])
        return ""

    def augment_keywords(self):
        augmented_dict = {}
        for category, keywords in self.keywords_dict.items():
            new_kws = set()
            for kw in keywords:
                new_kws.add(kw)
                # Thêm bản không dấu
                no_accent = self.remove_accents(kw)
                if len(no_accent) > 1:
                    new_kws.add(no_accent)
                # Đã gỡ bỏ phần tự động sinh viết tắt (abbreviation) vì dễ gây nhầm lẫn (vd: dầu ăn -> da -> nhầm với sữa tắm trắng da)
            augmented_dict[category] = list(new_kws)
        self.keywords_dict = augmented_dict

    def clean_text(self, text):
        # Đưa về chữ thường và loại bỏ khoảng trắng thừa
        return str(text).lower().strip()

    def classify(self, text):
        cleaned_text = self.clean_text(text)
        
        # Lưu kết quả match
        matched_categories = []
        
        for category, keywords in self.keywords_dict.items():
            for kw in keywords:
                # Kiểm tra keyword có nằm trong câu không
                if kw in cleaned_text:
                    # Lưu lại (Category, Keyword, Độ dài keyword)
                    # Độ dài keyword càng dài càng ưu tiên (ví dụ "trà sữa" ưu tiên hơn "trà")
                    matched_categories.append((category, kw, len(kw)))
                    
        if not matched_categories:
            return "UNKNOWN_NEED_ML_MODEL", None
            
        # Sắp xếp các kết quả match theo độ dài keyword giảm dần
        # Keyword nào dài nhất sẽ được chọn làm nhãn cuối cùng
        matched_categories.sort(key=lambda x: x[2], reverse=True)
        best_match = matched_categories[0]
        return best_match[0], best_match[1] # Trả về (Mã nhãn, Keyword ăn khớp)

    def process_file(self, file_path, text_column="Product Name"):
        """Đọc file, phân loại và đề xuất từ khóa mới từ các dòng bị UNKNOWN"""
        import pandas as pd
        from collections import Counter
        
        print(f"\\n[+] Đang đọc file: {file_path}...")
        if str(file_path).endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        if text_column not in df.columns:
            print(f"Lỗi: Không tìm thấy cột '{text_column}' trong file!")
            return None
            
        df = df.dropna(subset=[text_column])
        
        labels = []
        matched_keys = []
        unknown_texts = []
        
        for text in df[text_column]:
            label, key = self.classify(text)
            labels.append(label)
            matched_keys.append(key)
            if label == "UNKNOWN_NEED_ML_MODEL":
                unknown_texts.append(str(text))
                
        df['Predicted_Rule_Label'] = labels
        df['Matched_Keyword'] = matched_keys
        
        # Thống kê tìm keys mới (Từ tần suất cao trong nhóm UNKNOWN)
        print("\\n[+] ĐỀ XUẤT TỪ KHÓA MỚI (TỪ NHÓM UNKNOWN)")
        print(f"Tổng số món không tìm thấy keywords: {len(unknown_texts)}")
        if unknown_texts:
            all_words = []
            for t in unknown_texts:
                # Lọc chữ cơ bản, giữ lại tiếng Việt
                clean_t = re.sub(r'[^\w\s]', ' ', self.clean_text(t))
                words = clean_t.split()
                all_words.extend(words)
                
            word_counts = Counter(all_words)
            # Lấy top 5000 từ phổ biến nhất
            top_new_keys = word_counts.most_common(5000)
            
            # Xuất file csv chứa 5000 keys mới này
            keys_df = pd.DataFrame(top_new_keys, columns=["Keyword", "Frequency"])
            keys_out_path = str(file_path).replace(".csv", "_unknown_keys.csv").replace(".xlsx", "_unknown_keys.csv")
            keys_df.to_csv(keys_out_path, index=False)
            
            print(f"-> Đã trích xuất {len(keys_df)} từ khóa mới và lưu vào file: {keys_out_path}")
            print("Các từ xuất hiện nhiều nhất (Top 10):")
            for word, count in top_new_keys[:10]:
                print(f" - '{word}': {count} lần")
        else:
            print("Tuyệt vời! Không có món nào bị sót (UNKNOWN).")
            
        # Xuất file kết quả
        out_path = str(file_path).replace(".csv", "_rule_results.csv").replace(".xlsx", "_rule_results.xlsx")
        if str(file_path).endswith('.csv'):
            df.to_csv(out_path, index=False)
        else:
            df.to_excel(out_path, index=False)
        print(f"\\n[+] Đã xuất kết quả phân loại ra file: {out_path}")
        return df

# --- Demo chạy thử ---
if __name__ == "__main__":
    classifier = RuleBasedClassifier()
    
    # 1. Chạy thử trên vài ví dụ đơn lẻ
    test_items = [
        "Trà sữa trân châu đường đen",
        "Bạc xỉu đá",
        "Gà rán KFC",
        "Món lạ chưa có trong từ khóa"
    ]
    
    print("="*60)
    print(f"{'TÊN MÓN ĂN THỰC TẾ':<30} | {'MÃ NHÃN'} | {'TỪ KHÓA MATCH'}")
    print("="*60)
    for item in test_items:
        pred_label, match_key = classifier.classify(item)
        print(f"{item:<30} | {pred_label:<20} | {str(match_key)}")
    print("="*60)
    
    # 2. Chạy thử đọc file bill_output_processed - brand.csv để tìm keys
    print("\\n[BẮT ĐẦU QUÉT FILE BILL OUTPUT ĐỂ TÌM TỪ KHÓA MỚI]")
    bill_output_path = "/Users/buidoanhaiyen/Documents/Vidimi/Code/6. Data/Data Processed/bill_output_processed - brand.csv"
    # Gọi hàm process_file với text_column là "Item Name"
    classifier.process_file(bill_output_path, text_column="Item Name")
