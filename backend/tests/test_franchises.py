from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_franchises():
    response = client.get("/franchises/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_franchises_are_sorted_by_name():
    response = client.get("/franchises/")

    assert response.status_code == 200

    data = response.json()

    names = [franchise["name"] for franchise in data]

    assert names == sorted(names)
