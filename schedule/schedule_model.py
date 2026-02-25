from pydantic import BaseModel, Field
from typing import Optional, List

class ScheduleRequest(BaseModel):
    iPK: Optional[int] = Field(default=None, description="PK")
    iUserFK: int = Field(..., example=1, description="사용자 ID")
    dtDate1: str = Field(..., example="2026-03-04", description="출발일 (depart_date)")
    dtDate2: str = Field(..., example="2026-03-08", description="종료일 (return_date)")
    strWhere: str = Field(..., example="제주도", description="여행지 (location)")
    strWithWho: str = Field(..., example="혼자", description="동행자 (companion)")
    strTransport: str = Field(..., example="대중교통", description="교통수단 (transport)")
    nTotalPeople: int = Field(1, example=1, description="인원수")
    nTotalBudget: int = Field(0, example=1000000, description="총 예산")
    nAlarmRatio: int = Field(25, example=75, description="알림 비율")
    nTransportRatio: int = Field(0, example=200000, description="교통 예산")
    nLodgingRatio: int = Field(0, example=300000, description="숙박 예산")
    nFoodRatio: int = Field(0, example=200000, description="식비 예산")
    chStatus: Optional[str] = Field(default=None, example="A", description="상태")
    dtCreate: Optional[str] = Field(default=None, description="생성일시")

class ScheduleActivity(BaseModel):
    dtSchedule: str = Field(..., example="2026-03-04 10:00:00", description="일정 시간 (YYYY-MM-DD HH:MM:SS)")
    place_name: str = Field(..., example="몽상드애월", description="방문 장소 명칭 (지도 API 검색이 가능한 공식 명칭)")
    category_group_code: Optional[str] = Field(None, example="CE7", description="장소 성격에 맞는 카카오 카테고리 그룹 코드 (예: CT1, AT4, FD6, CE7 등)")
    strMemo: str = Field("", example="공항 도착 및 렌터카 픽업", description="짧은 활동 요약 (필요 없으면 빈 값)")

class LocationRequestItemModel(BaseModel):
    place_name: str = Field(..., example="성산일출봉", description="장소 명칭")
    category_group_code: Optional[str] = Field(None, example="AT4", description="카카오톡 지도API에 해당하는 카테고리 그룹 코드")

class LocationRequestListModel(BaseModel):
    place_name_list: List[LocationRequestItemModel] = Field(..., example=[{"place_name": "제주국제공항 상주직원주차장", "category_group_code": "PK6"}, {"place_name": "스타벅스 성산일출봉점", "category_group_code": "CE7"}, {"place_name": "더베스트 제주 성산 호텔", "category_group_code": "AD5"}], description="AI가 생성한 방문 장소 명칭 리스트")

class ScheduleDay(BaseModel):
    day: str = Field(..., example="Day1", description="Day1, Day2...")
    activities: List[ScheduleActivity]

class ScheduleResponse(BaseModel):
    day_schedules: List[ScheduleDay]