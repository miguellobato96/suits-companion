from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.media_models import MediaModel
from app.reference_models import ReferenceModel  # noqa: F401


def get_media(
    db: Session,
    offset: int = 0,
    limit: int = 20,
) -> list[MediaModel]:
    statement = (
        select(MediaModel)
        .options(joinedload(MediaModel.franchises))
        .order_by(MediaModel.title, MediaModel.release_year)
        .offset(offset)
        .limit(limit)
    )

    return list(db.scalars(statement).unique().all())


def count_media(db: Session) -> int:
    statement = select(func.count()).select_from(MediaModel)

    return db.scalar(statement) or 0


def get_media_by_id(
    db: Session,
    media_id: int,
) -> MediaModel | None:
    statement = (
        select(MediaModel)
        .options(joinedload(MediaModel.franchises))
        .where(MediaModel.id == media_id)
    )

    return db.scalars(statement).unique().one_or_none()
