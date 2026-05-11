from pydantic import BaseModel, Field


class CharacterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)
    actor: str = Field(min_length=1, max_length=100)


class Character(BaseModel):
    id: int
    name: str
    role: str
    actor: str