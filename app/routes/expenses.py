from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from calendar import monthrange
from app.database import get_db
from app.models import Expense, Category
from app.schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    MonthlySummaryResponse,
    CategorySummary,
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
    "/summary",
    response_model=MonthlySummaryResponse,
)
def get_summary(
    month: str,
    db: Session = Depends(get_db),
):
    try:
        target_month = datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Month must be in YYYY-MM format.",
        )

    from calendar import monthrange
    from datetime import date

    year = target_month.year
    month_number = target_month.month

    last_day = monthrange(year, month_number)[1]

    start_date = date(year, month_number, 1)
    end_date = date(year, month_number, last_day)

    total = (
        db.query(func.sum(Expense.amount))
        .filter(
            Expense.spent_on >= start_date,
            Expense.spent_on <= end_date,
        )
        .scalar()
        or 0
    )

    results = (
        db.query(
            Category.name,
            func.sum(Expense.amount),
        )
        .join(Expense)
        .filter(
            Expense.spent_on >= start_date,
            Expense.spent_on <= end_date,
        )
        .group_by(Category.name)
        .all()
    )

    category_summary = []

    for name, category_total in results:

        percentage = 0

        if total > 0:
            percentage = round(
                (category_total / total) * 100,
                2,
            )

        category_summary.append(
            CategorySummary(
                category=name,
                total=category_total,
                percentage=percentage,
            )
        )

    return MonthlySummaryResponse(
        month=month,
        total_spend=total,
        categories=category_summary,
    )

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
