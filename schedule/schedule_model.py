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
    chStatus: Optional[str] = Field(default=None, example="P", description="상태")
    dtCreate: Optional[str] = Field(default=None, description="생성일시")

class ScheduleActivity(BaseModel):
    dtSchedule: str = Field(..., example="2026-03-04 10:00:00", description="일정 시간 (YYYY-MM-DD HH:MM:SS)")
    strLocationName: str = Field(..., example="제주국제공항", description="방문 장소 명칭 (location 테이블 조회용)")
    strMemo: str = Field("", example="공항 도착 및 렌터카 픽업", description="짧은 활동 요약 (필요 없으면 빈 값)")

# class SchedulePlacesRequestModel(BaseModel):
#     place_name_list: list[str] = Field(..., example="제주국제공항", description="방문 장소 명칭 (location 테이블 조회용)")

# class SchedulePlacesResponseModel(BaseModel):
#     location_list: list[LocationModel] = Field(..., example="제주국제공항", description="방문 장소 명칭 (location 테이블 조회용)")

class ScheduleDay(BaseModel):
    day: str = Field(..., example="Day1", description="Day1, Day2...")
    activities: List[ScheduleActivity]

class ScheduleResponse(BaseModel):
    day_schedules: List[ScheduleDay]

class SaveScheduleRequest(BaseModel):
    # 부모 테이블용 데이터
    iPK: Optional[int] = Field(default=None, description="PK")
    iUserFK: int = Field(..., example=1)
    dtDate1: str = Field(..., example="2026-03-04")
    dtDate2: str = Field(..., example="2026-03-08")
    strWhere: str = Field(..., example="제주도")
    strWithWho: str = Field(..., example="가족과")
    strTransport: str = Field(..., example="렌터카")
    nTotalPeople: int = Field(..., example=3)
    nTotalBudget: int = Field(0, example=1000000)
    nAlarmRatio: int = Field(25, example=75)
    nTransportRatio: int = Field(0, example=200000)
    nLodgingRatio: int = Field(0, example=300000)
    nFoodRatio: int = Field(0, example=200000)
    chStatus: Optional[str] = Field(default=None, example="P")
    dtCreate: Optional[str] = Field(default=None)
    
    # 자식 테이블용 데이터 (AI가 생성한 리스트를 그대로 전달)
    day_schedules: List[ScheduleDay]