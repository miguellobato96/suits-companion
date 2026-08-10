from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.characters.schemas import Character
from app.franchises.schemas import Franchise
from app.media.schemas import Media

ReferenceType = Literal[
    "movie",
    "series",
    "character",
    "person",
    "book",
    "music",
    "brand",
    "franchise",
    "other",
]


class ReferenceBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    reference_type: ReferenceType

    season: int | None = Field(default=None, ge=1)
    episode: int | None = Field(default=None, ge=1)

    quote: str | None = None
    context: str = Field(min_length=1)

    spoken_by_character_id: int = Field(ge=1)


class ReferenceCreate(ReferenceBase):
    media_ids: list[int] = Field(default_factory=list)
    franchise_ids: list[int] = Field(default_factory=list)


class ReferenceUpdate(ReferenceBase):
    media_ids: list[int] = Field(default_factory=list)
    franchise_ids: list[int] = Field(default_factory=list)


class ReferencePatch(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    reference_type: ReferenceType | None = None

    season: int | None = Field(default=None, ge=1)
    episode: int | None = Field(default=None, ge=1)

    quote: str | None = None
    context: str | None = Field(default=None, min_length=1)

    spoken_by_character_id: int | None = Field(default=None, ge=1)

    media_ids: list[int] | None = None
    franchise_ids: list[int] | None = None


class Reference(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    reference_type: str

    season: int | None
    episode: int | None

    quote: str | None
    context: str

    spoken_by_character_id: int

    spoken_by_character: Character
    media: list[Media]
    franchises: list[Franchise]

    created_at: datetime
    updated_at: datetime


class ReferenceListResponse(BaseModel):
    items: list[Reference]
    total: int
    offset: int
    limit: int
