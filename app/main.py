from fastapi import FastAPI

from app.database import Base, engine

app = FastAPI(title="Expense Tracker API")

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running!"}