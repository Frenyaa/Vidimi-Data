import json

keywords_path = '../config/keywords.json'

with open(keywords_path, 'r', encoding='utf-8') as f:
    keywords = json.load(f)

nuoc_ngot = keywords.get("BEV_NUOC_NGOT", [])
new_nuoc_ngot = []

moved_to_tra_sua = 0
moved_to_tra = 0

for kw in nuoc_ngot:
    kw_lower = kw.lower()
    
    # Katinat tra sua, phuc long tra sua, tocotoco tra sua, milk tea
    if "tra sua" in kw_lower or "milk tea" in kw_lower:
        if kw not in keywords["BEV_TRA_SUA"]:
            keywords["BEV_TRA_SUA"].append(kw)
        moved_to_tra_sua += 1
    # tra, tea
    elif "tra " in kw_lower or " tra" in kw_lower or "trà" in kw_lower or "tea" in kw_lower or kw_lower.startswith("tra"):
        if kw not in keywords["BEV_TRA"]:
            keywords["BEV_TRA"].append(kw)
        moved_to_tra += 1
    else:
        new_nuoc_ngot.append(kw)

keywords["BEV_NUOC_NGOT"] = new_nuoc_ngot

with open(keywords_path, 'w', encoding='utf-8') as f:
    json.dump(keywords, f, ensure_ascii=False, indent=2)

print(f"Đã dọn dẹp {moved_to_tra_sua} món sang BEV_TRA_SUA và {moved_to_tra} món sang BEV_TRA từ mục BEV_NUOC_NGOT.")
