from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_characters_returns_paginated_response() -> None:
    response = client.get("/characters/")

    assert response.status_code == 200

    body = response.json()

    assert "items" in body
    assert "total" in body
    assert "offset" in body
    assert "limit" in body
    assert isinstance(body["items"], list)
    assert body["offset"] == 0
    assert body["limit"] == 20


def test_get_characters_with_invalid_limit_returns_422() -> None:
    response = client.get("/characters/?limit=0")

    assert response.status_code == 422
