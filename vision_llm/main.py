# main.py 에 추가되어야 할 내용
from routes import expense

app = FastAPI()

app.include_router(
    expense.router,
    prefix="/expense",
    tags=["Expense"]
)