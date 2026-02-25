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
        "3. 'strLocationName'은 나중에 위치 검색이 가능하도록 건물명이나 장소의 공식 명칭을 정확히 작성해라.\n"
        "4. 'strMemo'는 해당 장소에서 수행할 구체적인 활동이나 추천 메뉴 등을 15자 내외로 핵심만 요약해라.\n"
        "5. 모든 출력은 반드시 한국어로 작성해라."
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("system", "{format_instructions}"),
            ("human", "위치: {strWhere}, 기간: {dtDate1}~{dtDate2}, 동행: {strWithWho}, 교통: {strTransport}, 총예산: {nTotalBudget}원(교통:{nTransportRatio}, 숙박:{nLodgingRatio}, 식비:{nFoodRatio})"),
        ]).partial(format_instructions=output_parser.get_format_instructions())
        
        self.chain = prompt | self._llm | output_parser