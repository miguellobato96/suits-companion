from types import SimpleNamespace

from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from sqlalchemy.orm import Session

from app.characters.model import CharacterModel
from app.franchises.model import FranchiseModel
from app.main import app
from app.references import router as references_router

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


def test_references_reject_invalid_franchise_id() -> None:
    response = client.get("/references/?franchise_id=0")

    assert response.status_code == 422


def test_references_unknown_franchise_returns_empty_page() -> None:
    response = client.get("/references/?franchise_id=999999")

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["offset"] == 0
    assert data["limit"] == 20


def test_filter_options_returns_expected_response_shape() -> None:
    response = client.get("/references/filter-options")

    assert response.status_code == 200

    data = response.json()

    assert "characters" in data
    assert "franchises" in data
    assert isinstance(data["characters"], list)
    assert isinstance(data["franchises"], list)


def test_filter_options_reject_invalid_ids() -> None:
    character_response = client.get("/references/filter-options?character_id=0")
    franchise_response = client.get("/references/filter-options?franchise_id=0")

    assert character_response.status_code == 422
    assert franchise_response.status_code == 422


def test_filter_options_apply_cross_filters(
    monkeypatch: MonkeyPatch,
) -> None:
    def fake_character_filter_options(
        _db,
        *,
        search: str | None = None,
        franchise_id: int | None = None,
    ) -> list[dict]:
        assert search == "batman"
        assert franchise_id == 1

        return [
            {
                "id": 1,
                "name": "Harvey Specter",
                "count": 1,
            },
            {
                "id": 2,
                "name": "Mike Ross",
                "count": 2,
            },
        ]

    def fake_franchise_filter_options(
        _db,
        *,
        search: str | None = None,
        character_id: int | None = None,
    ) -> list[dict]:
        assert search == "batman"
        assert character_id == 2

        return [
            {
                "id": 1,
                "name": "Batman",
                "count": 2,
            },
        ]

    monkeypatch.setattr(
        references_router,
        "get_character_filter_options",
        fake_character_filter_options,
    )
    monkeypatch.setattr(
        references_router,
        "get_franchise_filter_options",
        fake_franchise_filter_options,
    )

    response = client.get(
        "/references/filter-options",
        params={
            "search": "batman",
            "character_id": 2,
            "franchise_id": 1,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "characters": [
            {
                "id": 1,
                "name": "Harvey Specter",
                "count": 1,
            },
            {
                "id": 2,
                "name": "Mike Ross",
                "count": 2,
            },
        ],
        "franchises": [
            {
                "id": 1,
                "name": "Batman",
                "count": 2,
            },
        ],
    }


def test_filter_options_preserve_selected_options_with_zero_count(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        references_router,
        "get_character_filter_options",
        lambda *_args, **_kwargs: [],
    )
    monkeypatch.setattr(
        references_router,
        "get_franchise_filter_options",
        lambda *_args, **_kwargs: [],
    )

    def fake_session_get(
        _self,
        entity,
        entity_id: int,
    ):
        if entity is CharacterModel and entity_id == 2:
            return SimpleNamespace(
                id=2,
                name="Mike Ross",
            )

        if entity is FranchiseModel and entity_id == 1:
            return SimpleNamespace(
                id=1,
                name="Batman",
            )

        return None

    monkeypatch.setattr(Session, "get", fake_session_get)

    response = client.get(
        "/references/filter-options",
        params={
            "search": "no-results",
            "character_id": 2,
            "franchise_id": 1,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "characters": [
            {
                "id": 2,
                "name": "Mike Ross",
                "count": 0,
            },
        ],
        "franchises": [
            {
                "id": 1,
                "name": "Batman",
                "count": 0,
            },
        ],
    }
