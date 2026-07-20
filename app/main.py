from fastapi import FastAPI

from app.database import Base, engine
from app.routes.categories import router as category_router
from app.routes.expenses import router as expense_router

app = FastAPI(title="Expense Tracker API")

Base.metadata.create_all(bind=engine)

app.include_router(category_router)
app.include_router(expense_router)

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running!"}