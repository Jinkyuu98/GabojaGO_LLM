# 경로: GabojaGO_backend/library/
# pip install langchain langchain-openai openai pydantic
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from .expense_model import ExpenseModel
# from .models import ExpenseModel
# models 폴더안에 있는 __init__.py안에 정의가 되어있어야함
# from .expense_model import ExpenseModel
# from .category_model import CategoryModel 과 같이.
# 이렇게 구성한다면 from .models import ExpenseModel, CategoryModel 과 같이 다양한 모듈을
# 한번에 불러 올 수 있음

class TripGPT:
    def __init__(self, model_name: str):
        self._llm = ChatOpenAI(model=model_name, temperature=0)

class ExpenseGPT(TripGPT):
    def __init__(self):
        LLM_MODEL_EXPENSE = os.getenv("LLM_MODEL_EXPENSE")
        super().__init__(LLM_MODEL_EXPENSE)
        output_parser = PydanticOutputParser(pydantic_object=ExpenseModel)
        system_prompt = (
            """
            너는 영수증 이미지에서 정보를 추출해 JSON으로 구조화하는 AI다. 반드시 JSON만 출력하고 다른 설명은 하지 마라.
            
            [추출 필드 정의 및 생성 규칙]
            - category: 영수증의 내용을 분석하여 결제 종류를 추측해라. 반드시 다음 4개 중 하나를 반환해라 (F: 식비, T: 교통비, L: 숙박비, E: 기타).
            - date: 영수증에 보이는 결제 날짜/시간을 읽고, 반드시 'YYYY-MM-DD HH:MM:SS' 형식의 문자열로 반환해라 (시간이 없으면 00:00:00 처리).
            - total: 사용자가 실제로 지불한 최종 결제 금액 (숫자만 반환).
            - strMemo: 영수증 분석 내용을 바탕으로 다음 형식에 맞춰 하나의 문자열로 요약해라.
              형식: "상호명: [상호명], 내용: [구매품목이나 영수증 내용 요약 (evidence 포함)]"
              예시: "상호명: 스타벅스 제주성산점, 내용: 아메리카노 외 1건 (합계 10000)"
            
            [중요 규칙]
            1) total은 '합계'가 아니라 '실제로 결제한 금액'이다.
            2) strMemo를 작성할 때 카드번호/승인번호/전화번호 등 민감정보는 절대 포함시키지 말고 '[REDACTED]'로 마스킹하라.
            3) 확실하지 않은 정보(예: 할인금액이 없는 경우)는 0으로 처리하거나 메모 작성 시 생략해라.
            """
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("system", "{format_instructions}"),
            ("human", [
                {"type": "text", "text": "이 영수증에서 category(분류), date(결제일시), total(실결제금액), strMemo(상호명/카테고리 근거)를 추출해 JSON으로 응답해라."},
                {"type": "image_url", "image_url": "{image_data}"}
            ]),
        ]).partial(format_instructions=output_parser.get_format_instructions())

        self.chain = prompt | self._llm | output_parser