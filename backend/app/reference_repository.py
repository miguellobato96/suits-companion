from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql.elements import ColumnElement

from app.character_models import CharacterModel
from app.reference_models import ReferenceModel
from app.reference_schemas import (
    Reference,
    ReferenceCreate,
    ReferencePatch,
    ReferenceUpdate,
)


def build_reference_search_filter(search: str) -> ColumnElement[bool]:
    search_pattern = f"%{search}%"

    return or_(
        ReferenceModel.title.ilike(search_pattern),
        ReferenceModel.context.ilike(search_pattern),
    )


def to_reference(reference_model: ReferenceModel) -> Reference:
    return Reference.model_validate(reference_model)


def character_exists(db: Session, character_id: int) -> bool:
    return db.get(CharacterModel, character_id) is not None


def get_all_references(
    db: Session,
    search: str | None = None,
    reference_type: str | None = None,
    character_id: int | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[Reference]:
    statement = select(ReferenceModel).options(
        joinedload(ReferenceModel.spoken_by_character)
    )

    if search is not None:
        statement = statement.where(build_reference_search_filter(search))

    if reference_type is not None:
        statement = statement.where(ReferenceModel.reference_type == reference_type)

    if character_id is not None:
        statement = statement.where(ReferenceModel.spoken_by_character_id == character_id)

    statement = statement.order_by(ReferenceModel.id).offset(offset).limit(limit)

    reference_models = db.scalars(statement).all()

    return [to_reference(reference_model) for reference_model in reference_models]


def count_references(
    db: Session,
    search: str | None = None,
    reference_type: str | None = None,
    character_id: int | None = None,
) -> int:
    statement = select(func.count()).select_from(ReferenceModel)

    if search is not None:
        statement = statement.where(build_reference_search_filter(search))

    if reference_type is not None:
        statement = statement.where(ReferenceModel.reference_type == reference_type)

    if character_id is not None:
        statement = statement.where(ReferenceModel.spoken_by_character_id == character_id)

    return db.scalar(statement) or 0


def get_reference_by_id(db: Session, reference_id: int) -> Reference | None:
    statement = (
        select(ReferenceModel)
        .options(joinedload(ReferenceModel.spoken_by_character))
        .where(ReferenceModel.id == reference_id)
    )

    reference_model = db.scalar(statement)

    if reference_model is None:
        return None

    return to_reference(reference_model)


def create_new_reference(
    db: Session,
    reference_data: ReferenceCreate,
) -> Reference:
    reference_model = ReferenceModel(
        title=reference_data.title,
        reference_type=reference_data.reference_type,
        season=reference_data.season,
        episode=reference_data.episode,
        context=reference_data.context,
        external_url=reference_data.external_url,
        spoken_by_character_id=reference_data.spoken_by_character_id,
    )

    db.add(reference_model)
    db.commit()
    db.refresh(reference_model)

    statement = (
        select(ReferenceModel)
        .options(joinedload(ReferenceModel.spoken_by_character))
        .where(ReferenceModel.id == reference_model.id)
    )

    created_reference = db.scalar(statement)

    if created_reference is None:
        raise RuntimeError("Created reference could not be loaded")

    return to_reference(created_reference)


def update_existing_reference(
    db: Session,
    reference_id: int,
    reference_data: ReferenceUpdate,
) -> Reference | None:
    reference_model = db.get(ReferenceModel, reference_id)

    if reference_model is None:
        return None

    reference_model.title = reference_data.title
    reference_model.reference_type = reference_data.reference_type
    reference_model.season = reference_data.season
    reference_model.episode = reference_data.episode
    reference_model.context = reference_data.context
    reference_model.external_url = reference_data.external_url
    reference_model.spoken_by_character_id = reference_data.spoken_by_character_id

    db.commit()

    return get_reference_by_id(db, reference_id)


def patch_existing_reference(
    db: Session,
    reference_id: int,
    reference_data: ReferencePatch,
) -> Reference | None:
    reference_model = db.get(ReferenceModel, reference_id)

    if reference_model is None:
        return None

    patch_data = reference_data.model_dump(exclude_unset=True)

    for field_name, field_value in patch_data.items():
        setattr(reference_model, field_name, field_value)

    db.commit()

    return get_reference_by_id(db, reference_id)


def delete_existing_reference(db: Session, reference_id: int) -> bool:
    reference_model = db.get(ReferenceModel, reference_id)

    if reference_model is None:
        return False

    db.delete(reference_model)
    db.commit()

    return True