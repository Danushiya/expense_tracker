from tests.conftest import client
import uuid

def create_category():
    response = client.post(
        "/categories",
        json={
            "name": f"Food-{uuid.uuid4()}",
        },
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_create_expense():

    category_id = create_category()

    response = client.post(
        "/expenses",
        json={
            "amount": 500,
            "description": "Lunch",
            "spent_on": "2026-03-10",
            "category_id": category_id,
        },
    )

    assert response.status_code == 201
    assert response.json()["amount"] == 500


def test_get_expense():

    category_id = create_category()

    create = client.post(
        "/expenses",
        json={
            "amount": 800,
            "description": "Dinner",
            "spent_on": "2026-03-15",
            "category_id": category_id,
        },
    )

    expense_id = create.json()["id"]

    response = client.get(
        f"/expenses/{expense_id}"
    )

    assert response.status_code == 200
    assert response.json()["description"] == "Dinner"


def test_filter_expenses():

    category_id = create_category()

    client.post(
        "/expenses",
        json={
            "amount": 300,
            "description": "Breakfast",
            "spent_on": "2026-03-01",
            "category_id": category_id,
        },
    )

    response = client.get(
        f"/expenses?category_id={category_id}"
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_negative_amount():

    category_id = create_category()

    response = client.post(
        "/expenses",
        json={
            "amount": -500,
            "description": "Invalid",
            "spent_on": "2026-03-10",
            "category_id": category_id,
        },
    )

    assert response.status_code == 422


def test_expense_not_found():

    response = client.get("/expenses/9999")

    assert response.status_code == 404


def test_summary():

    category_id = create_category()

    client.post(
        "/expenses",
        json={
            "amount": 1000,
            "description": "Shopping",
            "spent_on": "2026-03-20",
            "category_id": category_id,
        },
    )

    response = client.get(
        "/expenses/summary?month=2026-03"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["month"] == "2026-03"
    assert data["total_spend"] > 0