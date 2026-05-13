from pydantic import BaseModel, ConfigDict, Field


class CharacterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=100)
    actor: str = Field(min_length=1, max_length=100)


class Character(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    role: str
    actor: str