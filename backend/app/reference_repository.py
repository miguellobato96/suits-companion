from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.character_models import CharacterModel
from app.franchise_models import FranchiseModel
from app.media_models import MediaModel
from app.reference_models import ReferenceModel
from app.reference_schemas import ReferenceCreate, ReferenceUpdate


def _reference_load_options():
    return (
        joinedload(ReferenceModel.spoken_by_character),
        joinedload(ReferenceModel.media).joinedload(MediaModel.franchises),
        joinedload(ReferenceModel.franchises),
    )


def get_references(
    db: Session,
    search: str | None = None,
    reference_type: str | None = None,
    character_id: int | None = None,
    franchise_id: int | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[ReferenceModel]:
    statement = (
        select(ReferenceModel)
        .options(*_reference_load_options())
        .order_by(ReferenceModel.id)
    )

    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(
                ReferenceModel.title.ilike(pattern),
                ReferenceModel.quote.ilike(pattern),
                ReferenceModel.context.ilike(pattern),
            )
        )

    if reference_type:
        statement = statement.where(
            ReferenceModel.reference_type == reference_type
        )

    if character_id is not None:
        statement = statement.where(
            ReferenceModel.spoken_by_character_id == character_id
        )

    if franchise_id is not None:
        statement = statement.where(
            ReferenceModel.franchises.any(
                FranchiseModel.id == franchise_id
            )
        )

    statement = statement.offset(offset).limit(limit)

    return list(
        db.scalars(statement)
        .unique()
        .all()
    )


def count_references(
    db: Session,
    search: str | None = None,
    reference_type: str | None = None,
    character_id: int | None = None,
    franchise_id: int | None = None,
) -> int:
    statement = select(func.count()).select_from(ReferenceModel)

    if search:
        pattern = f"%{search}%"
        statement = statement.where(
            or_(
                ReferenceModel.title.ilike(pattern),
                ReferenceModel.quote.ilike(pattern),
                ReferenceModel.context.ilike(pattern),
            )
        )

    if reference_type:
        statement = statement.where(
            ReferenceModel.reference_type == reference_type
        )

    if character_id is not None:
        statement = statement.where(
            ReferenceModel.spoken_by_character_id == character_id
        )

    if franchise_id is not None:
        statement = statement.where(
            ReferenceModel.franchises.any(
                FranchiseModel.id == franchise_id
            )
        )

    return db.scalar(statement) or 0


def get_reference(
    db: Session,
    reference_id: int,
) -> ReferenceModel | None:
    statement = (
        select(ReferenceModel)
        .options(*_reference_load_options())
        .where(ReferenceModel.id == reference_id)
    )

    return db.scalars(statement).unique().one_or_none()


def character_exists(
    db: Session,
    character_id: int,
) -> bool:
    return db.get(CharacterModel, character_id) is not None


def get_media_by_ids(
    db: Session,
    media_ids: list[int],
) -> list[MediaModel]:
    unique_ids = list(dict.fromkeys(media_ids))

    if not unique_ids:
        return []

    statement = (
        select(MediaModel)
        .options(joinedload(MediaModel.franchises))
        .where(MediaModel.id.in_(unique_ids))
    )

    return list(
        db.scalars(statement)
        .unique()
        .all()
    )


def get_franchises_by_ids(
    db: Session,
    franchise_ids: list[int],
) -> list[FranchiseModel]:
    unique_ids = list(dict.fromkeys(franchise_ids))

    if not unique_ids:
        return []

    statement = select(FranchiseModel).where(
        FranchiseModel.id.in_(unique_ids)
    )

    return list(db.scalars(statement).all())


def create_reference(
    db: Session,
    data: ReferenceCreate,
    media: list[MediaModel],
    franchises: list[FranchiseModel],
) -> ReferenceModel:
    values = data.model_dump(
        exclude={"media_ids", "franchise_ids"}
    )

    reference = ReferenceModel(**values)
    reference.media = media
    reference.franchises = franchises

    db.add(reference)
    db.commit()

    created_reference = get_reference(db, reference.id)

    if created_reference is None:
        raise RuntimeError("Created reference could not be retrieved")

    return created_reference


def update_reference(
    db: Session,
    reference: ReferenceModel,
    data: ReferenceUpdate,
    media: list[MediaModel],
    franchises: list[FranchiseModel],
) -> ReferenceModel:
    values = data.model_dump(
        exclude={"media_ids", "franchise_ids"}
    )

    for field, value in values.items():
        setattr(reference, field, value)

    reference.media = media
    reference.franchises = franchises

    db.commit()

    updated_reference = get_reference(db, reference.id)

    if updated_reference is None:
        raise RuntimeError("Updated reference could not be retrieved")

    return updated_reference


def patch_reference(
    db: Session,
    reference: ReferenceModel,
    updates: dict,
    media: list[MediaModel] | None = None,
    franchises: list[FranchiseModel] | None = None,
    update_media: bool = False,
    update_franchises: bool = False,
) -> ReferenceModel:
    for field, value in updates.items():
        setattr(reference, field, value)

    if update_media:
        reference.media = media or []

    if update_franchises:
        reference.franchises = franchises or []

    db.commit()

    updated_reference = get_reference(db, reference.id)

    if updated_reference is None:
        raise RuntimeError("Updated reference could not be retrieved")

    return updated_reference


def delete_reference(
    db: Session,
    reference: ReferenceModel,
) -> None:
    db.delete(reference)
    db.commit()


def get_references_by_character(
    db: Session,
    character_id: int,
    offset: int = 0,
    limit: int = 20,
) -> list[ReferenceModel]:
    return get_references(
        db=db,
        character_id=character_id,
        offset=offset,
        limit=limit,
    )


def count_references_by_character(
    db: Session,
    character_id: int,
) -> int:
    return count_references(
        db=db,
        character_id=character_id,
    )