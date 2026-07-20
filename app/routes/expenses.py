from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Expense, Category
from app.schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
)

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)

@router.get(
    "",
    response_model=list[ExpenseResponse],
)
def get_expenses(
    category_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Expense)

    if category_id:
        query = query.filter(
            Expense.category_id == category_id
        )

    if from_date:
        query = query.filter(
            Expense.spent_on >= from_date
        )

    if to_date:
        query = query.filter(
            Expense.spent_on <= to_date
        )

    expenses = query.all()

    return [
        ExpenseResponse(
            id=e.id,
            amount=e.amount,
            description=e.description,
            spent_on=e.spent_on,
            category_id=e.category_id,
            category_name=e.category.name,
        )
        for e in expenses
    ]

@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    expense = db.get(Expense, expense_id)

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    return ExpenseResponse(
        id=expense.id,
        amount=expense.amount,
        description=expense.description,
        spent_on=expense.spent_on,
        category_id=expense.category_id,
        category_name=expense.category.name,
    )

@router.post(
    "",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
):
    category = db.get(Category, expense_data.category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    expense = Expense(**expense_data.model_dump())

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return ExpenseResponse(
        id=expense.id,
        amount=expense.amount,
        description=expense.description,
        spent_on=expense.spent_on,
        category_id=expense.category_id,
        category_name=expense.category.name,
    )

@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
):
    expense = db.get(Expense, expense_id)

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    category = db.get(Category, expense_data.category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    for key, value in expense_data.model_dump().items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)

    return ExpenseResponse(
        id=expense.id,
        amount=expense.amount,
        description=expense.description,
        spent_on=expense.spent_on,
        category_id=expense.category_id,
        category_name=expense.category.name,
    )

@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    expense = db.get(Expense, expense_id)

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )

    db.delete(expense)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)