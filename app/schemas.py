from pydantic import BaseModel, ConfigDict, Field
from datetime import date


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class ExpenseBase(BaseModel):
    amount: float = Field(gt=0)
    description: str
    spent_on: date
    category_id: int

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(ExpenseBase):
    pass

class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: str
    spent_on: date
    category_id: int
    category_name: str

    model_config = ConfigDict(from_attributes=True)

