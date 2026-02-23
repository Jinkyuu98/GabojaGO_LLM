# Test Folder - GabojaGO Backend

이 폴더는 GabojaGO 백엔드 프로젝트의 주요 모듈(OCR, 카테고리 분류, 데이터 수집 등)을 로컬 환경에서 독립적으로 테스트하고 검증하기 위한 공간입니다.

## 📂 폴더 구조 및 주요 파일

### 1. Vision LLM (OCR 및 지출 내역 추출)
- **`vision_llm/`**: 영수증 이미지 분석 및 지출 내역 추출 로직이 포함된 모듈입니다.
  - `LLM.py`: LangChain 기반 OCR LLM 엔진.
  - `expense.py`: FastAPI 엔드포인트 라우터.
  - `expense_model.py`: Pydantic 데이터 모델.
  - `image_validation.py`: 이미지 검증 유틸리티.
- **`main.py`**: 로컬에서 Vision LLM 기능을 테스트하기 위한 FastAPI 서버 실행 파일입니다. (`python Test/main.py`)
- **`receipt/`**: 테스트용 영수증 이미지들이 저장된 폴더입니다.

### 2. Category Classification (카테고리 분류 엔진)
- **`category_rules.py`**: 카카오 맵 카테고리 데이터를 기반으로 한 분류 규칙 정의 파일입니다.
- **`analyze_data.py`**: 수집된 장소 데이터를 분석하여 규칙을 도출하는 스크립트입니다.
- **`test_rules.py`**: 작성된 분류 규칙이 정상적으로 작동하는지 확인하는 테스트 스크립트입니다.
- **`verify_refined_rules.py`**: 개선된 규칙의 정확도를 검증합니다.

### 3. Data Collection (데이터 수집 유틸리티)
- **`collect.py` / `collect_large.py`**: 카카오 맵 API 등을 사용하여 장소 데이터를 수집하는 스크립트입니다.
- **`collected_categories.json` / `collected_large.json`**: 수집된 장소 데이터 결과물입니다.

### 4. 기타 테스트 및 리포트
- **`LLM.py`**: (레거시/통합) LLM 테스트 스크립트.
- **`analysis_report.txt`**: 자동화된 데이터 분석 결과 리포트.
- **`test_expense.py`**: 지출 내역 추출 기능의 단위 테스트.

---

## 🚀 로컬 실행 방법

### Vision LLM API 서버 실행
```bash
python Test/main.py
```
실행 후 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)에서 Swagger UI를 통해 API 테스트가 가능합니다.

### 분류 규칙 유효성 검사
```bash
python Test/test_rules.py
```

## ⚠️ 주의사항
- API 키 등 민감한 설정은 루트 폴더나 Test 폴더 내의 `.env` 파일에 기록되어 있어야 합니다.
- `pip install -r requirements.txt` (또는 필요한 패키지: `fastapi`, `uvicorn`, `langchain-openai` 등)가 설치되어 있는지 확인하세요.
