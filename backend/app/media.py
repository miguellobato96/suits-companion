from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.media_models import MediaModel
from app.media_repository import count_media, get_media, get_media_by_id
from app.media_schemas import Media, MediaListResponse


router = APIRouter(
    prefix="/media",
    tags=["media"],
)


@router.get(
    "/",
    response_model=MediaListResponse,
)
def list_media(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> MediaListResponse:
    items = get_media(
        db=db,
        offset=offset,
        limit=limit,
    )

    total = count_media(db)

    return MediaListResponse(
        items=items,
        total=total,
        offset=offset,
        limit=limit,
    )


@router.get(
    "/{media_id}",
    response_model=Media,
)
def read_media(
    media_id: int,
    db: Session = Depends(get_db),
) -> MediaModel:
    media = get_media_by_id(db, media_id)

    if media is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found",
        )

    return media