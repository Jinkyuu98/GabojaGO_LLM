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

class ExpenseEvidence(BaseModel):
    store_name_evidence: Optional[str] = Field(None)
    date_evidence: Optional[str] = Field(None)
    total_evidence: Optional[str] = Field(None)
    original_total_evidence: Optional[str] = Field(None)
    discount_amount_evidence: Optional[str] = Field(None)

class ExpenseModel(BaseModel):
    store_name: Optional[str] = Field(None)
    date: Optional[str] = Field(None)
    total: Optional[int] = Field(None)
    original_total: Optional[int] = Field(None)
    discount_amount: Optional[int] = Field(None)
    evidence: Optional[ExpenseEvidence] = None