from fastapi import APIRouter, HTTPException
# from library.DB import DB
from .schedule_llm import ScheduleGPT
from .schedule_model import ScheduleRequest, ScheduleResponse, SaveScheduleRequest
# from .schedule_table import ScheduleTable, ScheduleModel
# from .schedule_table_location import ScheduleLocationTable, ScheduleLocationModel
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
        # LLM으로 일정만 생성해서 반환
        ai_res: ScheduleResponse = schedule_ai.chain.invoke(req.model_dump())
        end_time = time.perf_counter()
        duration = end_time - start_time
        logger.info(f"일정 생성 시간: {duration:.2f}초")
        return ai_res # 프론트엔드로 생성된 결과 전송
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"생성 실패: {str(e)}")

# --- 2단계: 일정 확정 및 저장 (버튼 클릭 시 호출) ---
@router.post("/save", response_model=SaveScheduleRequest)
async def save_schedule(save_data: SaveScheduleRequest):
    return {"message": "DB 저장 성공!"}
    # try:
    #     with DB.CONNECT() as conn:
    #         with conn.cursor() as cursor:
    #             # 1. 부모 테이블 (schedule) 저장
    #             sm = ScheduleModel(
    #                 iUserFK=save_data.iUserFK,
    #                 dtDate1=save_data.dtDate1,
    #                 dtDate2=save_data.dtDate2,
    #                 strWhere=save_data.strWhere,
    #                 strWithWho=save_data.strWithWho,
    #                 strTransport=save_data.strTransport,
    #                 nTotalPeople=save_data.nTotalPeople,
    #                 nTotalBudget=save_data.nTotalBudget,
    #                 nAlarmRatio=save_data.nAlarmRatio,
    #                 nTransportRatio=save_data.nTransportRatio,
    #                 nLodgingRatio=save_data.nLodgingRatio,
    #                 nFoodRatio=save_data.nFoodRatio,
    #                 chStatus=save_data.chStatus or 'P'
    #             )
    #             DB.EXECUTE(cursor, ScheduleTable.TO_INSERT_QUERY(sm))
    #             schedule_id = cursor.lastrowid

    #             # 2. 상세 일정 (schedule_location) 저장
    #             for day in save_data.day_schedules:
    #                 for act in day.activities:
    #                     # 장소 ID 조회 (strLocationName으로 찾기)
    #                     cursor.execute(f"SELECT iPK FROM location WHERE strName = '{act.strLocationName}' LIMIT 1")
    #                     row = cursor.fetchone()
                        
    #                     # 장소가 없으면 1번(기본값) 또는 새로 등록 로직
    #                     loc_id = row[0] if row else 1

    #                     slm = ScheduleLocationModel(
    #                         iScheduleFK=schedule_id,
    #                         iLocationFK=loc_id,
    #                         dtSchedule=act.dtSchedule,
    #                         strMemo=act.strMemo or ""
    #                     )
    #                     DB.EXECUTE(cursor, ScheduleLocationTable.TO_INSERT_QUERY(slm))
            
    #         conn.commit()
            
    #     return {"status": "success", "schedule_id": schedule_id}

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"저장 실패: {str(e)}")