import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from .schedule_model import ScheduleResponse
from vision_llm.LLM import TripGPT 

class ScheduleGPT(TripGPT):
    def __init__(self):
        super().__init__(model_name=os.getenv("LLM_MODEL_SCHEDULE"))
        output_parser = PydanticOutputParser(pydantic_object=ScheduleResponse)
        
        system_prompt = (
                    "너는 사용자의 여행 조건을 분석하여 최적화된 동선의 일정을 만들어주는 '상세 여행 스케줄러 AI'다.\n"
                    "반드시 JSON 형태로만 응답하며, 모든 필드는 제공된 스키마 규칙을 엄격히 따른다.\n\n"

                    "[입력 정보 활용 규칙]\n"
                    "1. 위치(strWhere): 해당 지역의 실제 유명 장소와 맛집을 기반으로 일정을 구성해라.\n"
                    "2. 기간(dtDate1 ~ dtDate2): 시작일의 오전부터 종료일의 오후까지 전체 기간을 빠짐없이 채워라.\n"
                    "3. 동행자(strWithWho) & 인원(nTotalPeople): 동행자의 성격(가족, 연인, 혼자 등)에 적합한 장소를 추천해라.\n"
                    "4. 이동수단(strTransport): 설정된 이동수단으로 이동 가능한 현실적인 동선을 고려해라.\n"
                    "5. 테마 및 예산: 사용자가 입력한 예산(nTotalBudget, nTransportRatio, nLodgingRatio, nFoodRatio)을 반영하여 장소의 등급과 활동을 결정해라.\n\n"

                    "[출력 형식 규칙]\n"
                    "1. day_schedules 리스트 내에 날짜별로 'Day1', 'Day2' 순서대로 객체를 생성해라.\n"
                    "2. 'dtSchedule'은 반드시 해당 일자의 시간 정보를 포함한 'YYYY-MM-DD HH:MM:SS' 형식이어야 한다.\n"
                    "3. 'place_name'은 지도 API 검색이 가능하도록 '공식 명칭'을 정확히 작성해라.\n"
                    "   - 예: '애월 카페' (X) -> '몽상드애월' (O)\n"
                    "   - 예: '공항 근처 고기국수' (X) -> '자매국수' (O)\n"
                    "4. 'category_group_code'에는 장소의 성격에 맞는 카카오지도 API 카테고리 그룹 코드를 작성해라.\n"
                    "   - 매핑 코드: MT1(대형마트), CS2(편의점), PS3(어린이집/유치원), SC4(학교), AC5(학원), PK6(주차장), OL7(주유소/충전소), SW8(지하철역), BK9(은행), CT1(문화시설), AG2(중개업소), PO3(공공기관), AT4(관광명소), AD5(숙박), FD6(음식점), CE7(카페), HP8(병원), PM9(약국)\n"
                    "   - 주의: 해당되는 코드가 없다면 값을 비워도 좋다.\n"
                    "5. 'strMemo'는 해당 장소에서 수행할 구체적인 활동이나 추천 메뉴 등을 15자 내외로 핵심만 요약해라.\n"
                    "6. 모든 출력은 반드시 한국어로 작성해라."
                    )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("system", "{format_instructions}"),
            ("human", "위치: {strWhere}, 기간: {dtDate1}~{dtDate2}, 동행: {strWithWho}, 교통: {strTransport}, 총예산: {nTotalBudget}원(교통:{nTransportRatio}, 숙박:{nLodgingRatio}, 식비:{nFoodRatio})"),
        ]).partial(format_instructions=output_parser.get_format_instructions())
        
        self.chain = prompt | self._llm | output_parser