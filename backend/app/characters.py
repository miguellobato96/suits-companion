from fastapi import APIRouter
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