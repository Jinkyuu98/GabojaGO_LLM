import json
import os
import sys

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from library.category_rules import classify_category

def test_rules():
    data_path = os.path.join("Test", "collected_categories.json")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    correct = 0
    total = len(data)
    results = []

    for item in data:
        assigned = item["assigned_cat"]
        predicted = classify_category(
            item["place_name"], 
            item["category_name"], 
            item.get("category_group_name", "")
        )
        
        is_correct = (assigned == predicted)
        if is_correct:
            correct += 1
        else:
            results.append({
                "place_name": item["place_name"],
                "category_name": item["category_name"],
                "assigned": assigned,
                "predicted": predicted
            })

    accuracy = (correct / total) * 100
    print(f"Total: {total}, Correct: {correct}, Accuracy: {accuracy:.2f}%")

    if results:
        print("\nMisclassified Examples (Top 10):")
        for res in results[:10]:
            print(f"Place: {res['place_name']}, Category: {res['category_name']}, Assigned: {res['assigned']}, Predicted: {res['predicted']}")

if __name__ == "__main__":
    test_rules()
