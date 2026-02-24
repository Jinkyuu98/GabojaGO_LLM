import requests
import os
import json
import time
import random
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")
SEARCH_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

def call_api(url, params):
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Quota Limit Reached or Throttled. Waiting 1s...")
            time.sleep(1)
            return call_api(url, params)
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return {}
    except Exception as e:
        print(f"Request failed: {e}")
        return {}

def collect_exploratory():
    regions = [
        "서울 강남구", "서울 서초구", "서울 동작구", "서울 관악구", "서울 송파구", "서울 강동구", "서울 성동구", "서울 광진구",
        "서울 동대문구", "서울 중랑구", "서울 성북구", "서울 강북구", "서울 도봉구", "서울 노원구", "서울 은평구", "서울 서대문구",
        "서울 마포구", "서울 양천구", "서울 강서구", "서울 구로구", "서울 금천구", "서울 영등포구", "서울 용산구",
        "서울 종로구", "서울 중구", "부산 해운대구", "부산 부산진구", "부산 동래구", "부산 사하구", "부산 금정구", "부산 수영구",
        "인천 중구", "인천 연수구", "인천 남동구", "인천 부평구", "대구 중구", "대구 수성구", "대구 달서구", "광주 북구", "광주 서구",
        "대전 유성구", "대전 서구", "울산 남구", "세종시", "경기 수원시", "경기 성남시", "경기 안양시", "경기 부천시", "경기 광명시",
        "경기 평택시", "경기 안산시", "경기 고양시", "경기 과천시", "경기 구리시", "경기 남양주시", "경기 오산시", "경기 시흥시",
        "경기 군포시", "경기 의왕시", "경기 하남시", "경기 용인시", "경기 파주시", "경기 이천시", "경기 안성시", "경기 김포시",
        "경기 화성시", "경기 광주시", "경기 양주시", "경기 포천시", "경기 여주시", "충북 청주시", "충북 충주시", "충북 제천시",
        "충남 천안시", "충남 공주시", "충남 보령시", "충남 아산시", "충남 서산시", "충남 논산시", "충남 당진시", "전북 전주시",
        "전북 군산시", "전북 익산시", "전남 목포시", "전남 여수시", "전남 순천시", "전남 나주시", "전남 광양시", "경북 포항시",
        "경북 경주시", "경북 김천시", "경북 안동시", "경북 구미시", "경북 영주시", "경북 상주시", "경북 문경시", "경북 경산시",
        "경남 창원시", "경남 진주시", "경남 통영시", "경남 사천시", "경남 김해시", "경남 밀양시", "경남 거제시", "경남 양산시",
        "제주 제주시", "제주 서귀포시"
    ]
    
    category_codes = [
        "MT1", "CS2", "PS3", "SC4", "PK6", "OL7", "SW8", "BK9", "CT1", "AG2", "PO3", "AT4", "AD5", "FD6", "CE7", "HP8", "PM9"
    ]
    
    exploratory_keywords = [
        "명소", "가볼만한곳", "핫플레이스", "관광", "시설", "빌딩", "센터", "상가", "공원", "복합문화공간"
    ]
    
    # 순서를 섞어서 새로운 데이터가 더 잘 나오게 함
    random.shuffle(regions)
    random.shuffle(category_codes)
    random.shuffle(exploratory_keywords)
    
    seen_ids = set()
    collected_results = []
    total_target = 80000 
    output_path = os.path.join("Test", "collected_large.json")
    
    if os.path.exists(output_path):
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                collected_results = json.load(f)
                seen_ids = {item["id"] for item in collected_results if "id" in item}
                print(f"Resuming counts: {len(collected_results)} items...")
        except: pass

    last_save_count = len(collected_results)

    try:
        print("--- Mode: Category Group Codes ---")
        for code in category_codes:
            if len(collected_results) >= total_target: break
            for region in regions:
                if len(collected_results) >= total_target: break
                
                print(f"Searching Code: {code}, Region: {region} (Total: {len(collected_results)})")
                for page in range(1, 4):
                    params = {"query": region, "category_group_code": code, "size": 15, "page": page}
                    res_json = call_api(SEARCH_URL, params)
                    docs = res_json.get("documents", [])
                    if not docs: break
                    
                    added = 0
                    for doc in docs:
                        pid = doc.get("id")
                        if pid not in seen_ids:
                            collected_results.append({
                                "id": pid,
                                "place_name": doc.get("place_name"),
                                "category_name": doc.get("category_name"),
                                "category_group_name": doc.get("category_group_name"),
                                "source": f"code_{code}"
                            })
                            seen_ids.add(pid)
                            added += 1
                    
                    if added == 0: break
                    if len(collected_results) - last_save_count >= 500:
                        with open(output_path, "w", encoding="utf-8") as f:
                            json.dump(collected_results, f, ensure_ascii=False, indent=2)
                        last_save_count = len(collected_results)
                        print(f"Progress saved: {last_save_count} items")
                
                time.sleep(0.05)

        if len(collected_results) < total_target:
            print("--- Mode: Exploratory Keywords ---")
            for kw in exploratory_keywords:
                if len(collected_results) >= total_target: break
                for region in regions:
                    if len(collected_results) >= total_target: break
                    
                    print(f"Searching Keyword: {kw}, Region: {region} (Total: {len(collected_results)})")
                    for page in range(1, 4):
                        params = {"query": f"{region} {kw}", "size": 15, "page": page}
                        res_json = call_api(SEARCH_URL, params)
                        docs = res_json.get("documents", [])
                        if not docs: break
                        
                        added = 0
                        for doc in docs:
                            pid = doc.get("id")
                            if pid not in seen_ids:
                                collected_results.append({
                                    "id": pid,
                                    "place_name": doc.get("place_name"),
                                    "category_name": doc.get("category_name"),
                                    "category_group_name": doc.get("category_group_name"),
                                    "source": f"kw_{kw}"
                                })
                                seen_ids.add(pid)
                                added += 1
                        
                        if added == 0: break
                        if len(collected_results) - last_save_count >= 500:
                            with open(output_path, "w", encoding="utf-8") as f:
                                json.dump(collected_results, f, ensure_ascii=False, indent=2)
                            last_save_count = len(collected_results)
                            print(f"Progress saved: {last_save_count} items")
                    
                    time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nInterrupted. Saving...")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(collected_results, f, ensure_ascii=False, indent=2)
    
    print(f"\nFinal Collected: {len(collected_results)}")
    
if __name__ == "__main__":
    if not KAKAO_API_KEY:
        print("No KAKAO_API_KEY")
    else:
        collect_exploratory()
