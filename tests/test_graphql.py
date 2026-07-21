import uuid
from datetime import date

from tests.conftest import client

from app.database import SessionLocal
from app.models import Category, Expense


def create_category():

    db = SessionLocal()

    category = Category(
        name=f"GraphQL-{uuid.uuid4()}"
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    category_id = category.id

    db.close()

    return category_id


def create_expense(category_id):

    db = SessionLocal()

    expense = Expense(
        amount=500,
        description="Lunch",
        spent_on=date(2026, 3, 10),
        category_id=category_id,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    expense_id = expense.id

    db.close()

    return expense_id


def test_graphql_query_expenses():

    category_id = create_category()
    create_expense(category_id)

    query = """
    {
      expenses {
        id
        amount
        description
      }
    }
    """

    response = client.post(
        "/graphql",
        json={"query": query},
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert data["data"]["expenses"] is not None


def test_graphql_query_categories():

    create_category()

    query = """
    {
      categories {
        id
        name
      }
    }
    """

    response = client.post(
        "/graphql",
        json={"query": query},
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data
    assert data["data"]["categories"] is not None


def test_graphql_add_expense():

    category_id = create_category()

    mutation = f"""
    mutation {{
      addExpense(
        input: {{
          amount: 800
          description: "GraphQL Expense"
          spentOn: "2026-03-15"
          categoryId: {category_id}
        }}
      ) {{
        id
        amount
        description
      }}
    }}
    """

    response = client.post(
        "/graphql",
        json={"query": mutation},
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data

    assert (
        data["data"]["addExpense"]["description"]
        == "GraphQL Expense"
    )

    assert (
        data["data"]["addExpense"]["amount"]
        == 800
    )


def test_graphql_delete_expense():

    category_id = create_category()

    expense_id = create_expense(category_id)

    mutation = f"""
    mutation {{
      deleteExpense(id: {expense_id})
    }}
    """

    response = client.post(
        "/graphql",
        json={"query": mutation},
    )

    assert response.status_code == 200

    data = response.json()

    assert "data" in data

    assert (
        data["data"]["deleteExpense"]
        is True
    )