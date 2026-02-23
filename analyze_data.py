import json
import os
from collections import Counter

def analyze_data():
    input_path = os.path.join("Test", "collected_large.json")
    output_report = os.path.join("Test", "analysis_report.txt")
    
    if not os.path.exists(input_path):
        print("Data file not found.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(output_report, "w", encoding="utf-8") as report:
        report.write(f"Total Samples: {len(data)}\n")

        # 1. category_group_name 빈도 분석
        group_counts = Counter(item.get("category_group_name", "") for item in data)
        report.write("\n--- Category Group Name Frequencies ---\n")
        for group, count in group_counts.most_common():
            report.write(f"{group or 'None'}: {count}\n")

        # 2. 그룹별 주요 category_name 분석
        report.write("\n--- Top Category Names per Group ---\n")
        groups = group_counts.keys()
        for group in groups:
            group_label = group or "None"
            report.write(f"\n[{group_label}]\n")
            cat_names = Counter(item.get("category_name", "") for item in data if item.get("category_group_name") == group)
            for name, count in cat_names.most_common(10):
                report.write(f"  - {name}: {count}\n")

        # 3. category_name의 마지막 대분류 추출 분석
        report.write("\n--- Top 50 Deep Category Frequencies ---\n")
        deep_cats = Counter(item.get("category_name", "").split(">")[-1].strip() for item in data)
        for cat, count in deep_cats.most_common(50):
            report.write(f"{cat}: {count}\n")

        # 4. 'None' 그룹이면서 category_name에 특정 키워드가 포함된 경우 분석
        report.write("\n--- Deep Dive: 'None' Group Keywords ---\n")
        keywords_to_check = ["식당", "카페", "주차장", "주유소", "역", "호텔", "모텔", "펜션", "게스트하우스", "정류장", "마트", "편의점"]
        for kw in keywords_to_check:
            matches = Counter(item.get("category_name", "") for item in data 
                             if not item.get("category_group_name") and kw in item.get("category_name", ""))
            if matches:
                report.write(f"\nKeyword [{kw}] in 'None' Group:\n")
                for name, count in matches.most_common(5):
                    report.write(f"  - {name}: {count}\n")

    print(f"Analysis complete. Report saved to {output_report}")

if __name__ == "__main__":
    analyze_data()
