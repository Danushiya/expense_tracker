from tests.conftest import client


def test_create_category():

    response = client.post(
        "/categories",
        json={
            "name": "Health",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Health"


def test_get_categories():

    response = client.get("/categories")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_category():

    create = client.post(
        "/categories",
        json={
            "name": "Books",
        },
    )

    category_id = create.json()["id"]

    response = client.get(
        f"/categories/{category_id}"
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Books"


def test_duplicate_category():

    client.post(
        "/categories",
        json={
            "name": "Travel",
        },
    )

    response = client.post(
        "/categories",
        json={
            "name": "Travel",
        },
    )

    assert response.status_code == 409


def test_category_not_found():

    response = client.get("/categories/999")

    assert response.status_code == 404