# GabojaGO LLM Python / Test Workspace

이 리포지토리는 GabojaGO 백엔드 프로젝트에서 활용되는 생성형 AI 및 모델 구동 기능(OCR 기반 지출 내역 추출, 스마트 일정 생성, 카카오맵 카테고리 분류, 데이터 수집)을 구현하고, 로컬 환경에서 독립적으로 테스트 및 검증하기 위한 통합 공간입니다.

## 📂 폴더 구조 및 주요 파일

### 1. Vision LLM (OCR 및 지출 내역 추출)
- **`vision_llm/`**: 영수증 이미지 분석 및 지출 내역 추출을 수행하는 지능형 모듈입니다.
  - `LLM.py`: LangChain 기반 OCR 파싱 및 정보를 추출하는 Vision 모델 핵심 로직.
  - `expense.py`: 지출 내역 추출 FastAPI 엔드포인트 라우터.
  - `expense_model.py`: 입출력 데이터의 형태를 정의하는 Pydantic 모델.
  - `image_validation.py`: 유효한 영수증 이미지인지 판단하는 검증 유틸리티.
  - `test_expense.py`: 지출 내역 추출 기능 단위 테스트 스크립트.

### 2. Schedule LLM (스마트 일정 매니저)
- **`schedule/`**: 사용자의 여행 제약조건 및 취향을 바탕으로 LLM을 활용해 최적화된 여행 계획을 수립하는 모듈입니다.
  - `schedule_llm.py`: 프롬프트 엔지니어링 기반 여행 일정 생성 엔진.
  - `schedule_routes.py`: 여행 생성 요청을 처리하는 FastAPI 라우터.
  - `schedule_model.py`: 일정 생성 입출력 형식을 정의하는 Pydantic 모델.

### 3. Category & Data Collection (카카오맵 데이터 수집 및 분류)
- **`rule_category/`**: 장소 카테고리를 GabojaGO 서비스 형식에 맞게 분류하는 각종 로직과 관련 툴이 모여있습니다.
  - `category_rules.py`: 카카오맵 카테고리 데이터를 기반으로 한 자체 분류 규칙 모델.
  - `analyze_data.py`: 수집된 장소 데이터를 분석하여 규칙을 도출하는 스크립트.
  - `collect.py` / `collect_large.py`: 장소 데이터를 크롤링하고 수집하는 스크립트.
  - `test_rules.py` / `verify_refined_rules.py`: 작성된 분류 규칙의 정합성 및 정확도를 검증하는 파일.
  - `collected_categories.json` / `collected_large.json`: 데이터 수집 결과물 샘플.

### 4. 기타 테스트 및 리소스 모음
- **`main.py`**: 단독으로 `vision_llm` 등 주요 컴포넌트들을 연결하여 빠르고 독립적으로 테스트하기 위한 로컬 FastAPI 서버 실행 파일입니다.
- **`dataset/`**: 모델 검증용 및 테스트용으로 축적된 대규모 이미지(영수증 등) 저장소입니다.
- **`receipt/`**: 로컬 서버 테스트를 위해 수동으로 주입되는 샘플 영수증 이미지 저장 폴더입니다.
- **`backend/`**: (`LLM.py`) 현재 통합 또는 분리 작업 중인 이전 버전의 LLM 레거시 코드 및 백업 폴더입니다.

---

## 🚀 로컬 실행 방법

### 로컬 FastAPI 테스트 서버 실행 (루트 디렉토리 기준)
루트 폴더(`GabojaGO_LLM/`)에서 아래 명령어를 실행하여 로컬 서버를 구동합니다.
```bash
python main.py
```
*(기존 `main.py` 파일 내의 `python Test/main.py` 등의 표기는 현재 폴더 구조 변경에 맞춰 무시하시고 위 명령어대로 실행하세요)*

실행 후 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)에서 Swagger UI를 통해 각 기능에 대한 API 테스트가 가능합니다.

### 분류 규칙 유효성 테스트 실행방법
분류 규칙의 변동 사항이 정상적으로 작용하는지는 아래와 같이 디렉토리를 맞춰 테스트를 진행합니다.
```bash
python rule_category/test_rules.py
```

## ⚠️ 주의사항
- API 키(OpenAI 등)와 같은 민감한 설정 정보는 루트 폴더의 `.env` 파일에 기록되어 있어야만 정상적으로 동작합니다.
- 시작하기 전에 파이썬 환경(가상환경 등)에 필요한 리스트가 잘 설치되어 있는지 확인하세요 (`fastapi`, `uvicorn`, `langchain-openai`, `python-dotenv` 등).
