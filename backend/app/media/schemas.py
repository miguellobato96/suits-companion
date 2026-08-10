from pydantic import BaseModel, ConfigDict

from app.franchises.schemas import Franchise


class Media(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    media_type: str
    release_year: int | None
    franchises: list[Franchise]


class MediaListResponse(BaseModel):
    items: list[Media]
    total: int
    offset: int
    limit: int
