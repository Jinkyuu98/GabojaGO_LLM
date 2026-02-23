# pip install openai langchain langchain-openai pydantic

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
import logging
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
# LLM.py에서 Test해보기 위해 추가#
from dotenv import load_dotenv
load_dotenv()
#################################
logger = logging.getLogger(__name__)

class CategoryModel(BaseModel):
    category: Literal["F", "T", "L", "E"] = Field(..., description="예산에 사용된 카테고리 4가지(F:식비, T:교통비, L:숙박비, E:기타)중 하나")

class ScheduleModel(BaseModel):
    pass

class ExpenseEvidence(BaseModel):
    store_name_evidence: Optional[str] = Field(None, description="store_name 근거 원문 1줄(그대로)")
    date_evidence: Optional[str] = Field(None, description="date 근거 원문 1줄(그대로)")
    total_evidence: Optional[str] = Field(None, description="total(실지불) 근거 원문 1줄(그대로)")
    original_total_evidence: Optional[str] = Field(None, description="original_total(합계/정가) 근거 원문 1줄(그대로)")
    discount_amount_evidence: Optional[str] = Field(None, description="discount_amount(할인) 근거 원문 1줄(그대로)")

class ExpenseModel(BaseModel):
    store_name: Optional[str] = Field(None, description="매장명")
    date: Optional[str] = Field(None, description="날짜/시간(YYYY-MM-DD HH:MM:SS 또는 YYYY-MM-DD)")
    total: Optional[int] = Field(None, description="실제 지불한 금액(가계부/여행 지출액)")
    original_total: Optional[int] = Field(None, description="할인/쿠폰 적용 전 합계(정가/합계)")
    discount_amount: Optional[int] = Field(None, description="할인/쿠폰/포인트로 감면된 금액")
    evidence: Optional[ExpenseEvidence] = None
# category: Optional[Literal["F", "T", "L", "E"]] = Field(None, description="카테고리(F:식비, T:교통비, L:숙박비, E:기타)")
    # LLM이 분류한 category의 근거가 된 영수증의 텍스트(debug용, 추후 이부분은 삭제할지 가져갈지는 정해야함)
class TripGPT:
    def __init__(self, model_name: str):
        self._llm = ChatOpenAI(
            model = model_name,
            temperature = 0
        )

# class TripGIMINI:
#     def __init__(self, model_name: str):
#         self._llm = ChatGoogleGenerativeAI(
#             model = model_name,
#             temperate=0
#         )

class CategoryGPT(TripGPT):
    def __init__(self):
        LLM_MODEL_CATEGORY = os.getenv("LLM_MODEL_CATEGORY")
        super().__init__(LLM_MODEL_CATEGORY)
        output_parser = PydanticOutputParser(pydantic_object=CategoryModel)
        prompt = ChatPromptTemplate.from_messages([
            ("system",
             "너는 카카오 지도 API에서 받은 장소 정보를 기반으로 예산 카테고리를 분류하는 AI다. "
             "반드시 다음 4가지 중 하나만 선택하라: "
             "F:식비, T:교통비, L:숙박비, E:기타. "
             "기타는 숙박비, 식비, 교통비를 제외한 나머지 분류이다. "
             "다른 설명은 하지 말고 JSON 형식으로만 답하라. "
             ),
            ("system", "{format_instructions}"),
            ("human", 
             "다음은 카카오 지도 API에서 받은 장소 정보이다.\n\n"
             "place_name: {place_name}\n"
             "category_group_name: {category_group_name}\n"
             "category_name: {category_name}\n\n"
             "이 장소를 예산 카테고리로 분류하라."
             )
        ]).partial(format_instructions=output_parser.get_format_instructions())
        self.chain = prompt | self._llm | output_parser

class ScheduleGPT(TripGPT):
    def __init__(self):
        LLM_MODEL_SCHEDULE = os.getenv("LLM_MODEL_SCHEDULE")
        super().__init__(LLM_MODEL_SCHEDULE)
        output_parser = PydanticOutputParser(pydantic_object=ScheduleModel)
        prompt = ChatPromptTemplate.from_messages([
            
        ])
        self.chain = prompt | self._llm | output_parser
    pass
# import base64
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

# 실제 테스트를 위한 함수 및 코드.
if __name__ == "__main__":
    from pathlib import Path
    import random
    import base64
    from image_validation import validate_image, image_uri_prefix
    
    ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

    def guess_content_type(path: Path) -> str:
        ext = path.suffix.lower()
        if ext in [".jpg", ".jpeg"]:
            return "image/jpeg"
        if ext == ".png":
            return "image/png"
        if ext == ".webp":
            return "image/webp"
        raise ValueError(f"지원하지 않는 확장자: {ext}")

    def build_data_uri(img_path: Path) -> str:
        image_bytes = img_path.read_bytes()
        content_type = guess_content_type(img_path)
        validate_image(content_type, len(image_bytes))
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        return image_uri_prefix(content_type) + b64

    def iter_files(receipts_dir: Path):
        files = sorted(
            [p for p in receipts_dir.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED_EXT],
            key=lambda p: p.name.lower()
        )
        if not files:
            raise FileNotFoundError(f"{receipts_dir} 폴더에 이미지가 없음(jpg/jpeg/png/webp)")
        return files
        
    BASE_DIR = Path(__file__).parent
    receipts_dir = BASE_DIR / "receipt"   # test/receipt 폴더

    files = iter_files(receipts_dir)

    MODE = os.getenv("TEST_MODE", "random")  # "random" or "seq"
    TEST_COUNT = int(os.getenv("TEST_COUNT", "5"))

    llm = ExpenseGPT()

    if MODE == "seq":
        selected = files[:min(TEST_COUNT, len(files))]
    else:
        # random (no duplicates)
        selected = random.sample(files, k=min(TEST_COUNT, len(files)))

    for idx, img_path in enumerate(selected, start=1):
        print(f"\n[TEST {idx}] {img_path.name}")
        try:
            data_uri = build_data_uri(img_path)
            result = llm.chain.invoke({"image_data": data_uri})

            if hasattr(result, "model_dump"):
                print(result.model_dump())
            else:
                print(result)

        except OutputParserException as e:
            print(f"[PARSER FAIL] {img_path.name}")
            # 모델 원문 출력(디버깅용)
            try:
                print("----- RAW LLM OUTPUT START -----")
                print(e.llm_output)
                print("----- RAW LLM OUTPUT END -----")
            except Exception:
                pass
        except Exception as e:
            print(f"[ERROR] {img_path.name}: {e}")