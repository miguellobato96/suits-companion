from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.character_repository import (
    count_characters,
    create_new_character,
    delete_existing_character,
    get_all_characters,
    get_character_by_id,
    update_existing_character,
)
from app.character_schemas import (
    Character,
    CharacterCreate,
    CharacterListResponse,
    CharacterUpdate,
)
from app.database import get_db

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.get("/", response_model=CharacterListResponse)
def get_characters(
    search: str | None = Query(default=None, min_length=1, max_length=100),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> CharacterListResponse:
    characters = get_all_characters(db, search, offset, limit)
    total = count_characters(db, search)

    return CharacterListResponse(
        items=characters,
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get("/{character_id}", response_model=Character)
def get_character(
    character_id: int,
    db: Session = Depends(get_db),
) -> Character:
    character = get_character_by_id(db, character_id)

    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")

    return character


@router.post("/", response_model=Character, status_code=status.HTTP_201_CREATED)
def create_character(
    character_data: CharacterCreate,
    db: Session = Depends(get_db),
) -> Character:
    return create_new_character(db, character_data)


@router.put("/{character_id}", response_model=Character)
def update_character(
    character_id: int,
    character_data: CharacterUpdate,
    db: Session = Depends(get_db),
) -> Character:
    character = update_existing_character(db, character_id, character_data)

    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")

    return character


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
) -> None:
    deleted = delete_existing_character(db, character_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Character not found")

    return None