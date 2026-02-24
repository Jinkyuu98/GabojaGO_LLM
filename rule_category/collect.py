import requests
import os
import json
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")
URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

def search_kakao(keyword):
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": keyword, "size": 15}
    response = requests.get(URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("documents", [])
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

def collect_data():
    # 카테고리별 검색 키워드 (각 25% 비율을 위해 조정)
    categories = {
        "F": ["맛집", "카페", "식당"],
        "T": ["주차장", "지하철역", "기차역", "터미널"],
        "L": ["호텔", "펜션", "게스트하우스", "리조트"],
        "E": ["관광명소", "공원", "박물관", "영화관", "쇼핑몰"]
    }
    
    collected_results = []
    
    for cat_label, keywords in categories.items():
        print(f"Collecting data for category: {cat_label}")
        cat_data = []
        for kw in keywords:
            docs = search_kakao(kw)
            for doc in docs:
                item = {
                    "assigned_cat": cat_label,
                    "place_name": doc.get("place_name"),
                    "category_name": doc.get("category_name"),
                    "category_group_name": doc.get("category_group_name")
                }
                cat_data.append(item)
            if len(cat_data) >= 30: # 각 카테고리당 충분한 샘플 확보
                break
        collected_results.extend(cat_data)

    # 결과 저장
    output_path = os.path.join("Test", "collected_categories.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(collected_results, f, ensure_ascii=False, indent=4)
    
    print(f"Total collected: {len(collected_results)}")
    
    # 통계 출력
    stats = {}
    for item in collected_results:
        cat = item["assigned_cat"]
        stats[cat] = stats.get(cat, 0) + 1
    
    print("\nData Distribution:")
    total = len(collected_results)
    for cat, count in stats.items():
        percentage = (count / total) * 100
        print(f"Category {cat}: {count} items ({percentage:.2f}%)")

if __name__ == "__main__":
    if not KAKAO_API_KEY:
        print("Error: KAKAO_API_KEY not found in .env")
    else:
        collect_data()
