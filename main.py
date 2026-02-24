import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
import logging
load_dotenv()
log_level = os.getenv("LOG_LEVEL").upper()
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.info(f"Log Level: {log_level}")

from vision_llm.expense import router as expense_router
from schedule.schedule_routes import router as schedule_router

app = FastAPI(title="GabojaGO Vision LLM Local Test Server")

# 라우터 등록
app.include_router(
    expense_router,
    prefix="/expense",
    tags=["Expense"]
)
app.include_router(
    schedule_router,
    prefix="/schedule",
    tags=["Schedule"]
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
