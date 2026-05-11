from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/characters", tags=["Characters"])

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

@router.get("/", response_model=list[Character])
def get_characters() -> list[Character]:
    return characters

@router.get("/{character_id}", response_model=Character)
def get_character(character_id: int) -> Character:
    for character in characters:
        if character.id == character_id:
            return character

    raise HTTPException(status_code=404, detail="Character not found")