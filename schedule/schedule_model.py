from pydantic import BaseModel, Field
from typing import Optional, List

class BudgetRatio(BaseModel):
    total_budget: int = Field(0, example=1000000, description="nTotalBudget")
    lod_budget: int = Field(0, example=300000, description="nLodgingRatio")
    food_budget: int = Field(0, example=200000, description="nFoodRatio")
    transport_budget: int = Field(0, example=200000, description="nTransportRatio")
    budget_ratio: int = Field(25, example=75, description="nAlarmRatio")

class ScheduleRequest(BaseModel):
    iUserFK: int = Field(..., example=1, description="사용자 ID")
    strWhere: str = Field(..., example="제주도", description="여행지 (location)")
    dtDate1: str = Field(..., example="2026-03-04", description="출발일 (depart_date)")
    dtDate2: str = Field(..., example="2026-03-08", description="종료일 (return_date)")
    strWithWho: str = Field(..., example="혼자", description="동행자 (companion)")
    strTransport: str = Field(..., example="대중교통", description="교통수단 (transport)")
    nTotalPeople: int = Field(1, example=1, description="인원수")
    budget: Optional[BudgetRatio] = None

class ScheduleActivity(BaseModel):
    dtSchedule: str = Field(..., example="2026-03-04 10:00:00", description="일정 시간 (YYYY-MM-DD HH:MM:SS)")
    strLocationName: str = Field(..., example="제주국제공항", description="방문 장소 명칭 (location 테이블 조회용)")
    strMemo: str = Field("", example="공항 도착 및 렌터카 픽업", description="짧은 활동 요약 (필요 없으면 빈 값)")

class ScheduleDay(BaseModel):
    day: str = Field(..., example="Day1", description="Day1, Day2...")
    activities: List[ScheduleActivity]

class ScheduleResponse(BaseModel):
    day_schedules: List[ScheduleDay]

class SaveScheduleRequest(BaseModel):
    # 부모 테이블용 데이터
    iUserFK: int = Field(..., example=1)
    strWhere: str = Field(..., example="제주도")
    dtDate1: str = Field(..., example="2026-03-04")
    dtDate2: str = Field(..., example="2026-03-08")
    strWithWho: str = Field(..., example="가족과")
    strTransport: str = Field(..., example="렌터카")
    nTotalPeople: int = Field(..., example=3)
    budget: Optional[BudgetRatio] = None
    
    # 자식 테이블용 데이터 (AI가 생성한 리스트를 그대로 전달)
    day_schedules: List[ScheduleDay]