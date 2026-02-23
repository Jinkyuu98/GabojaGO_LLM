import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

# .env 파일 로드 (OpenAI API Key 등)
load_dotenv()

# vision_llm 모듈 임포트
from vision_llm.expense import router as expense_router

app = FastAPI(title="GabojaGO Vision LLM Local Test Server")

# 라우터 등록
app.include_router(
    expense_router,
    prefix="/expense",
    tags=["Expense"]
)

@app.get("/")
async def root():
    return {"message": "GabojaGO Vision LLM Test Server is running!"}

if __name__ == "__main__":
    # 로컬 테스트를 위해 uvicorn으로 서버 실행
    # 실행 방법: python Test/main.py
    print("\n--- GabojaGO Vision LLM Local Test Server ---")
    print("API Documentation: http://127.0.0.1:8000/docs\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
