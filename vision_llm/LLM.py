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
            "너는 영수증 이미지에서 정보를 추출해 JSON으로 구조화하는 AI다. 반드시 JSON만 출력하고 다른 설명은 하지 마라.\n"
            "\n"
            "[추출 필드 정의]\n"
            "- store_name: 영수증 상호명\n"
            "- date: 영수증에 보이는 날짜/시간을 읽고, 가능하면 YYYY-MM-DD HH:MM:SS 또는 YYYY-MM-DD로 반환\n"
            "- total: 사용자가 실제로 지불한 금액(실지불/실결제/받은금액/결제금액/카드승인금액/현금지불에 해당)\n"
            "- original_total: 할인/쿠폰 적용 전 합계(합계/정가/총액)\n"
            "- discount_amount: 할인/쿠폰/제휴할인/포인트 차감으로 줄어든 금액(할인금액)\n"
            "\n"
            "[중요 규칙]\n"
            "1) total은 '합계'가 아니라 '실제로 지불한 금액'이다.\n"
            "2) 할인/쿠폰이 있으면 가능하면 original_total - discount_amount = total 관계가 성립하도록 해석하라.\n"
            "3) 확실하지 않으면 해당 값은 null로 둬라.\n"
            "\n"
            "[evidence 규칙]\n"
            "evidence에는 각 필드를 확인할 수 있는 영수증 원문 라인을 가능한 한 그대로 넣어라(요약/추측 금지).\n"
            "단, 카드번호/승인번호/전화번호/주소 등 민감정보는 절대 그대로 출력하지 말고 '[REDACTED]'로 마스킹하라.\n"
            "민감정보가 섞인 줄은 가능한 다른 줄(예: '합계 4,600', '할인금액 4,600', '받은금액 500')을 evidence로 선택하라.\n"
        )
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("system", "{format_instructions}"),
            ("human", [
                {"type": "text", "text": "이 영수증에서 store_name, date, total(실지불), original_total(합계), discount_amount(할인), evidence를 추출해라."},
                {"type": "image_url", "image_url": "{image_data}"}
            ]),
        ]).partial(format_instructions=output_parser.get_format_instructions())

        self.chain = prompt | self._llm | output_parser