# 경로: GabojaGO_backend/models/
# 기존에 LLM.py에 정의되어있던 스키마 분리
# Expense 관련 Pydantic 모델을 별도 파일로 분리하여 관리한다.
#
# 분리 이유:
# 1. LLM에서 PydanticOutputParser를 사용하기 위해 결과 스키마 정의가 필요함
# 2. 해당 스키마는 LLM 내부 전용이 아니라, FastAPI 응답(JSON), 서비스 로직, 추후 DB 매핑 등
#    여러 계층에서 공통으로 사용되는 데이터 계약이기 때문
# 3. LLM 로직(prompt/chain)과 데이터 구조(schema)를 분리하여 의존성을 낮추기 위함
#
# 사용 위치:
# - llm/ExpenseGPT → OutputParser 결과 파싱
# - FastAPI → response 모델(JSON 반환)
# - service layer → 지출 데이터 가공/저장 로직
#
# 즉, 본 파일은 "LLM 전용 모델"이 아니라 프로젝트 전반에서 재사용되는 도메인 스키마 역할을 한다.

# pip install pydantic
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExpenseEvidence(BaseModel):
    store_name: str = Field(..., example="스타벅스 제주성산점", description="영수증에 적힌 상호명")
    category_evidence: Optional[str] = Field(None, example="아메리카노")


class ExpenseModel(BaseModel):
    # TODO(Front-end Refactoring): 
    # 추후 프론트엔드에서 Javascript로 리팩토링할 예정이며, 프론트에서 실제 user_id와 schedule_id 값을 보내줄 수 있습니다.
    # 현재는 FastAPI에서 자체적인 LLM 기능 테스트를 위해 임시로 Optional 및 기본값(0)을 부여합니다.
    iUserFK: Optional[int] = Field(0, example=1, description="사용자 ID (추후 프론트엔드 연동 전까지 기본값 0)")
    iScheduleFK: Optional[int] = Field(0, example=1, description="일정 ID (추후 프론트엔드 연동 전까지 기본값 0)")
    category: str = Field(..., example="E", description="지출 카테고리(F: 식비, T: 교통비, L: 숙박비, E: 기타)")
    date: str = Field(..., example="2026-03-04 10:00:00", description="YYYY-MM-DD HH:MM:SS 형식의 영수증 날짜/시간")
    total: int = Field(..., example=10000, description="실제 지불된 결제 금액")
    strMemo: Optional[str] = Field(None, example="상호명: 스타벅스 제주성산점, 정가: 10000, 할인금액: 2000, 내용: 아메리카노(합계 10000)", description="상호명, 원가, 할인, 근거 등이 합성된 통합 메모")

###################################################################################################################
"""
category는 LLM을 통해서 추측하는 형태로 다시 변경, 지출 카테고리인 F, T, L, E를 반환
store_name은 strMemo 필드를 만든 후에 strMemo에 들어갈 수 있도록 변경
strMemo에는 evidence와 original_total, discount_amount 등의 정보들을 모두 넣어서 반환
date는 DATETIME 형식으로 수정 -- 현재는 Optional[str]로 되어있음 -> YYYY-MM-DD HH:MM:SS 형식으로 변경
해당 내용 프롬프트에도 적용

Front로 리팩토링 할 예정이므로 ScheduleID와 UserID도 가지고 있으므로 함께 보내주어야 함
최종적으로 DB있는 SERVER에 Request할 때는 ScheduleID, UserID, category,date,total,strMemo만 보내주면 됨

back에서는 해당 내용을 바탕으로 DB에 PK값을 할당해 반환
"""