from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.database import Base, engine
from app.graphql.schema import schema
from app.routes.categories import router as category_router
from app.routes.expenses import router as expense_router

app = FastAPI(title="Expense Tracker API")

Base.metadata.create_all(bind=engine)

app.include_router(category_router)
app.include_router(expense_router)

graphql_app = GraphQLRouter(schema)

app.include_router(
    graphql_app,
    prefix="/graphql",
)


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running!"}