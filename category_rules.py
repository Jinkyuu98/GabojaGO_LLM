import logging

logger = logging.getLogger(__name__)

def classify_category(place_name: str, category_name: str, category_group_name: str) -> str:
    """
    장소 정보를 기반으로 예산 카테고리(F, T, L, E)를 분류합니다.
    분석 데이터(7.7만건) 기반 룰 세팅.
    
    - F: 식비 (음식점, 카페, 제과, 술집 등)
    - T: 교통비 (주차장, 주유소, 지하철, 터미널 등)
    - L: 숙박비 (호텔, 펜션, 캠핑, 게스트하우스 등)
    - E: 기타 (공공기관, 병원, 은행, 마트, 편의점 등 그 외 모든 항목)
    """
    
    cat_full = category_name or ""
    grp_name = category_group_name or ""
    
    # 1. 숙박비 (L) - 가장 명확한 숙박 그룹 및 키워드 우선
    l_keywords = ["숙박", "호텔", "모텔", "펜션", "게스트하우스", "민박", "콘도", "리조트", "캠핑", "글램핑", "호스텔", "스테이", "유스호스텔"]
    if grp_name == "숙박" or any(kw in cat_full for kw in l_keywords):
        return "L"
        
    # 2. 교통비 (T) - 주차, 주유, 대중교통 관련
    t_groups = ["주차장", "주유소,충전소", "지하철역"]
    t_keywords = ["주차", "주유", "충전", "지하철", "전철", "기차", "철도", "공항", "터미널", "버스정류장", "정류소", "정류장", "톨게이트", "대리운전", "렌터카"]
    if grp_name in t_groups or any(kw in cat_full for kw in t_keywords):
        # 단, '주차장'이 포함된 업종 중 '음식점' 성격이 강한 경우 예외 처리가 필요할 수도 있으나, 
        # 카카오 API는 보통 주차장 그룹을 명확히 분리하므로 그대로 적용.
        return "T"
        
    # 3. 식비 (F) - 음식점, 카페, 간식, 술 등
    f_groups = ["음식점", "카페"]
    f_keywords = ["음식점", "카페", "커피", "베이커리", "제과", "디저트", "술집", "호프", "치킨", "피자", "분식", "뷔페", "패밀리레스토랑", "패스트푸드", "간식"]
    if grp_name in f_groups or any(kw in cat_full for kw in f_keywords):
        return "F"
        
    # 4. 기타 (E) - 나머지 모든 항목
    return "E"
