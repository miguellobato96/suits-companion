from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_references_returns_paginated_response() -> None:
    response = client.get("/references/")

    assert response.status_code == 200

    body = response.json()

    assert "items" in body
    assert "total" in body
    assert "offset" in body
    assert "limit" in body
    assert isinstance(body["items"], list)
    assert body["offset"] == 0
    assert body["limit"] == 20


def test_get_references_with_invalid_limit_returns_422() -> None:
    response = client.get("/references/?limit=0")

    assert response.status_code == 422


def test_create_reference_with_invalid_character_returns_400() -> None:
    response = client.post(
        "/references/",
        json={
            "title": "Invalid Character Test",
            "reference_type": "movie",
            "season": 1,
            "episode": 1,
            "context": "Temporary test payload for invalid character handling.",
            "external_url": None,
            "spoken_by_character_id": 999,
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Character does not exist"}


def test_patch_missing_reference_returns_404() -> None:
    response = client.patch(
        "/references/999",
        json={
            "context": "This reference does not exist.",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Reference not found"}


def test_get_missing_character_references_returns_404() -> None:
    response = client.get("/characters/999/references")

    assert response.status_code == 404
    assert response.json() == {"detail": "Character not found"}


def test_references_reject_invalid_franchise_id():
    response = client.get("/references/?franchise_id=0")

    assert response.status_code == 422


def test_references_unknown_franchise_returns_empty_page():
    response = client.get("/references/?franchise_id=999999")

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["offset"] == 0
    assert data["limit"] == 20