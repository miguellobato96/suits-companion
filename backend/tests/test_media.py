from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_media():
    response = client.get("/media/")

    assert response.status_code == 200

    data = response.json()

    assert set(data.keys()) == {
        "items",
        "total",
        "offset",
        "limit",
    }

    assert isinstance(data["items"], list)
    assert isinstance(data["total"], int)
    assert data["offset"] == 0
    assert data["limit"] == 20


def test_media_rejects_invalid_limit():
    response = client.get("/media/?limit=0")

    assert response.status_code == 422


def test_missing_media_returns_not_found():
    response = client.get("/media/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Media not found"
