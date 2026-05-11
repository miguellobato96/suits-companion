from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/characters", tags=["Characters"])


class CharacterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)
    actor: str = Field(min_length=1, max_length=100)


class Character(BaseModel):
    id: int
    name: str
    role: str
    actor: str


characters = [
    Character(
        id=1,
        name="Harvey Specter",
        role="Senior Partner",
        actor="Gabriel Macht",
    ),
    Character(
        id=2,
        name="Mike Ross",
        role="Associate",
        actor="Patrick J. Adams",
    ),
    Character(
        id=3,
        name="Donna Paulsen",
        role="Legal Secretary / COO",
        actor="Sarah Rafferty",
    ),
]


def get_next_character_id() -> int:
    if not characters:
        return 1

    return max(character.id for character in characters) + 1


@router.get("/", response_model=list[Character])
def get_characters() -> list[Character]:
    return characters


@router.get("/{character_id}", response_model=Character)
def get_character(character_id: int) -> Character:
    for character in characters:
        if character.id == character_id:
            return character

    raise HTTPException(status_code=404, detail="Character not found")


@router.post("/", response_model=Character, status_code=status.HTTP_201_CREATED)
def create_character(character_data: CharacterCreate) -> Character:
    character = Character(
        id=get_next_character_id(),
        name=character_data.name,
        role=character_data.role,
        actor=character_data.actor,
    )

    characters.append(character)

    return character


@router.put("/{character_id}", response_model=Character)
def update_character(character_id: int, character_data: CharacterCreate) -> Character:
    for index, character in enumerate(characters):
        if character.id == character_id:
            updated_character = Character(
                id=character.id,
                name=character_data.name,
                role=character_data.role,
                actor=character_data.actor,
            )

            characters[index] = updated_character

            return updated_character

    raise HTTPException(status_code=404, detail="Character not found")


@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(character_id: int) -> None:
    for index, character in enumerate(characters):
        if character.id == character_id:
            characters.pop(index)
            return None

    raise HTTPException(status_code=404, detail="Character not found")