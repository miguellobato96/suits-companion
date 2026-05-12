from fastapi import APIRouter, HTTPException, Query, status

from app.character_repository import (
    create_new_character,
    delete_existing_character,
    get_all_characters,
    get_character_by_id,
    update_existing_character,
)
from app.character_schemas import Character, CharacterCreate

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.get("/", response_model=list[Character])
def get_characters(
    search: str | None = Query(default=None, min_length=1, max_length=100),
) -> list[Character]:
    return get_all_characters(search)


@router.get("/{character_id}", response_model=Character)
def get_character(character_id: int) -> Character:
    character = get_character_by_id(character_id)

    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")

    return character


@router.post("/", response_model=Character, status_code=status.HTTP_201_CREATED)
def create_character(character_data: CharacterCreate) -> Character:
    return create_new_character(character_data)


@router.put("/{character_id}", response_model=Character)
def update_character(character_id: int, character_data: CharacterCreate) -> Character:
    character = update_existing_character(character_id, character_data)

    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")

    return character


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(character_id: int) -> None:
    deleted = delete_existing_character(character_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Character not found")

    return None