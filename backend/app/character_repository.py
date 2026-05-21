from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from app.character_models import CharacterModel
from app.character_schemas import Character, CharacterCreate, CharacterUpdate


def build_search_filter(search: str) -> ColumnElement[bool]:
    search_pattern = f"%{search}%"

    return or_(
        CharacterModel.name.ilike(search_pattern),
        CharacterModel.role.ilike(search_pattern),
        CharacterModel.actor.ilike(search_pattern),
    )


def to_character(character_model: CharacterModel) -> Character:
    return Character.model_validate(character_model)


def get_all_characters(
    db: Session,
    search: str | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[Character]:
    statement = select(CharacterModel)

    if search is not None:
        statement = statement.where(build_search_filter(search))

    statement = statement.order_by(CharacterModel.id).offset(offset).limit(limit)

    character_models = db.scalars(statement).all()

    return [to_character(character_model) for character_model in character_models]


def count_characters(db: Session, search: str | None = None) -> int:
    statement = select(func.count()).select_from(CharacterModel)

    if search is not None:
        statement = statement.where(build_search_filter(search))

    return db.scalar(statement) or 0


def get_character_by_id(db: Session, character_id: int) -> Character | None:
    character_model = db.get(CharacterModel, character_id)

    if character_model is None:
        return None

    return to_character(character_model)


def create_new_character(db: Session, character_data: CharacterCreate) -> Character:
    character_model = CharacterModel(
        name=character_data.name,
        role=character_data.role,
        actor=character_data.actor,
    )

    db.add(character_model)
    db.commit()
    db.refresh(character_model)

    return to_character(character_model)


def update_existing_character(
    db: Session,
    character_id: int,
    character_data: CharacterUpdate,
) -> Character | None:
    character_model = db.get(CharacterModel, character_id)

    if character_model is None:
        return None

    character_model.name = character_data.name
    character_model.role = character_data.role
    character_model.actor = character_data.actor

    db.commit()
    db.refresh(character_model)

    return to_character(character_model)


def delete_existing_character(db: Session, character_id: int) -> bool:
    character_model = db.get(CharacterModel, character_id)

    if character_model is None:
        return False

    db.delete(character_model)
    db.commit()

    return True