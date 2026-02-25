from fastapi import APIRouter, HTTPException
from .schedule_model import ScheduleRequest, ScheduleResponse, LocationRequestListModel, LocationRequestItemModel
from .schedule_llm import ScheduleGPT
import time
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
schedule_ai = ScheduleGPT()

# --- 1단계: 일정 생성 (DB 저장 안 함) ---
@router.post("/generate", response_model=ScheduleResponse)
async def generate_schedule(req: ScheduleRequest):
    start_time = time.perf_counter()
    logger.info(f"일정 생성 시작: {req.model_dump()}")
    try:
        ai_res: ScheduleResponse = schedule_ai.chain.invoke(req.model_dump())
        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"일정 생성 시간: {duration:.2f}초")
        return ai_res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"생성 실패: {str(e)}")

# --- 2단계: 생성된 일정에서 DB 서버 전송용 장소 목록 추출 ---
@router.post("/location/request", response_model=LocationRequestListModel)
async def request_location(schedule_data: ScheduleResponse):
    """
    생성된 전체 일정 데이터(ScheduleResponse)를 받아,
    DB/카카오 API 서버가 요구하는 스키마(LocationRequestListModel)로 파싱하여 반환합니다.
    """
    place_items = []
    for day in schedule_data.day_schedules:
        for act in day.activities:
            place_items.append(
                LocationRequestItemModel(
                    place_name=act.place_name,
                    category_group_code=act.category_group_code
                )
            )
            
    return LocationRequestListModel(place_name_list=place_items)
