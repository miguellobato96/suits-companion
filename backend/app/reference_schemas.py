from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.character_schemas import Character


ReferenceType = Literal[
    "movie",
    "series",
    "person",
    "book",
    "music",
    "brand",
    "other",
]


class ReferenceBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    reference_type: ReferenceType
    season: int | None = Field(default=None, ge=1)
    episode: int | None = Field(default=None, ge=1)
    context: str = Field(min_length=1, max_length=1000)
    external_url: str | None = Field(default=None, max_length=500)
    spoken_by_character_id: int = Field(ge=1)


class ReferenceCreate(ReferenceBase):
    pass


class ReferenceUpdate(ReferenceBase):
    pass


class ReferencePatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    reference_type: ReferenceType | None = None
    season: int | None = Field(default=None, ge=1)
    episode: int | None = Field(default=None, ge=1)
    context: str | None = Field(default=None, min_length=1, max_length=1000)
    external_url: str | None = Field(default=None, max_length=500)
    spoken_by_character_id: int | None = Field(default=None, ge=1)


class Reference(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    reference_type: str
    season: int | None
    episode: int | None
    context: str
    external_url: str | None
    spoken_by_character_id: int
    created_at: datetime
    updated_at: datetime
    spoken_by_character: Character


class ReferenceListResponse(BaseModel):
    items: list[Reference]
    total: int
    offset: int
    limit: int