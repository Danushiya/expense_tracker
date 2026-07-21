from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.database import get_db
from app.models import Category
from app.schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get(
    "",
    response_model=list[CategoryResponse],
)
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.get(Category, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category

@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(Category)
        .filter(Category.name == category_data.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Category already exists",
        )

    category = Category(name=category_data.name)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category

@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = db.get(Category, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    duplicate = (
        db.query(Category)
        .filter(
            Category.name == category_data.name,
            Category.id != category_id,
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Category already exists",
        )

    category.name = category_data.name

    db.commit()
    db.refresh(category)

    return category

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = db.get(Category, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    if category.expenses:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a category that has expenses.",
        )

    db.delete(category)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
