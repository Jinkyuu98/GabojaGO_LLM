import json
import os
import sys
from collections import Counter

# 프로젝트 루트 경로 추가 (library 모듈 임포트 가능하도록)
sys.path.append(os.getcwd())
from library.category_rules import classify_category

def verify_rules():
    input_path = os.path.join("Test", "collected_large.json")
    if not os.path.exists(input_path):
        print("Data file not found.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Verifying rules against {len(data)} samples...")

    results = []
    for item in data:
        p_name = item.get("place_name", "")
        c_name = item.get("category_name", "")
        g_name = item.get("category_group_name", "")
        
        predicted = classify_category(p_name, c_name, g_name)
        results.append(predicted)

    # 분포 확인
    counts = Counter(results)
    print("\n--- Categorization Distribution ---")
    total = len(results)
    for cat in ["F", "T", "L", "E"]:
        count = counts.get(cat, 0)
        percentage = (count / total) * 100
        print(f"{cat}: {count} ({percentage:.2f}%)")

    # 각 카테고리별 샘플 5개씩 출력
    print("\n--- Samples per Category ---")
    for cat in ["F", "T", "L", "E"]:
        print(f"\n[{cat}]")
        found = 0
        for item in data:
            p_name = item.get("place_name", "")
            c_name = item.get("category_name", "")
            g_name = item.get("category_group_name", "")
            predicted = classify_category(p_name, c_name, g_name)
            
            if predicted == cat:
                print(f"  - {p_name} | {c_name} | {g_name}")
                found += 1
            if found >= 5:
                break

if __name__ == "__main__":
    verify_rules()
