from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routes.categories import router as category_router
from app.routes.expenses import router as expense_router
from app.graphql.schema import schema

from strawberry.fastapi import GraphQLRouter

app = FastAPI(title="Expense Tracker API")

Base.metadata.create_all(bind=engine)

graphql_app = GraphQLRouter(schema)

app.include_router(category_router)
app.include_router(expense_router)
app.include_router(graphql_app, prefix="/graphql")

app.mount(
    "/",
    StaticFiles(directory="app/static", html=True),
    name="static",
)
