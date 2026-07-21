from datetime import date

import strawberry
from graphql import GraphQLError

from app.database import SessionLocal
from app.models import Category, Expense


@strawberry.type
class CategoryType:
    id: int
    name: str


@strawberry.type
class ExpenseType:
    id: int
    amount: float
    description: str
    spent_on: date
    category: CategoryType

@strawberry.input
class ExpenseInput:
    amount: float
    description: str
    spent_on: date
    category_id: int


@strawberry.type
class Query:

    @strawberry.field
    def categories(self) -> list[CategoryType]:
        db = SessionLocal()

        try:
            categories = db.query(Category).all()

            return [
                CategoryType(
                    id=category.id,
                    name=category.name,
                )
                for category in categories
            ]

        finally:
            db.close()

    @strawberry.field
    def expenses(
        self,
        category_id: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[ExpenseType]:

        db = SessionLocal()

        try:
            query = db.query(Expense)

            if category_id is not None:
                query = query.filter(
                    Expense.category_id == category_id
                )

            if from_date is not None:
                query = query.filter(
                    Expense.spent_on >= from_date
                )

            if to_date is not None:
                query = query.filter(
                    Expense.spent_on <= to_date
                )

            expenses = query.all()

            return [
                ExpenseType(
                    id=expense.id,
                    amount=expense.amount,
                    description=expense.description,
                    spent_on=expense.spent_on,
                    category=CategoryType(
                        id=expense.category.id,
                        name=expense.category.name,
                    ),
                )
                for expense in expenses
            ]

        finally:
            db.close()

@strawberry.type
class CategoryType:
    id: int
    name: str

    @strawberry.field
    def expenses(self) -> list["ExpenseType"]:

        db = SessionLocal()

        try:
            expenses = (
                db.query(Expense)
                .filter(Expense.category_id == self.id)
                .all()
            )

            return [
                ExpenseType(
                    id=expense.id,
                    amount=expense.amount,
                    description=expense.description,
                    spent_on=expense.spent_on,
                    category=CategoryType(
                        id=expense.category.id,
                        name=expense.category.name,
                    ),
                )
                for expense in expenses
            ]

        finally:
            db.close()

@strawberry.type
class Mutation:

    @strawberry.mutation
    def add_expense(
        self,
        input: ExpenseInput,
    ) -> ExpenseType:

        db = SessionLocal()

        try:
            category = db.get(
                Category,
                input.category_id,
            )

            if not category:
                raise GraphQLError(
                    "Category not found"
                )

            expense = Expense(
                amount=input.amount,
                description=input.description,
                spent_on=input.spent_on,
                category_id=input.category_id,
            )

            db.add(expense)
            db.commit()
            db.refresh(expense)

            return ExpenseType(
                id=expense.id,
                amount=expense.amount,
                description=expense.description,
                spent_on=expense.spent_on,
                category=CategoryType(
                    id=category.id,
                    name=category.name,
                ),
            )

        finally:
            db.close()


    @strawberry.mutation
    def delete_expense(
        self,
        id: int,
    ) -> bool:

        db = SessionLocal()

        try:
            expense = db.get(
                Expense,
                id,
            )

            if not expense:
                raise GraphQLError(
                    "Expense not found"
                )

            db.delete(expense)
            db.commit()

            return True

        finally:
            db.close()


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)