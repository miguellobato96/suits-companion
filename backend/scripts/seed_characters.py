from sqlalchemy import select
from sqlalchemy.orm import Session

from app.character_models import CharacterModel
from app.database import SessionLocal


INITIAL_CHARACTERS = [
    {
        "name": "Harvey Specter",
        "role": "Senior Partner",
        "actor": "Gabriel Macht",
    },
    {
        "name": "Mike Ross",
        "role": "Associate",
        "actor": "Patrick J. Adams",
    },
    {
        "name": "Donna Paulsen",
        "role": "Legal Secretary / COO",
        "actor": "Sarah Rafferty",
    },
]


def character_exists(db: Session, name: str) -> bool:
    statement = select(CharacterModel).where(CharacterModel.name == name)
    return db.scalar(statement) is not None


def main() -> None:
    db = SessionLocal()

    try:
        created_count = 0

        for character_data in INITIAL_CHARACTERS:
            if character_exists(db, character_data["name"]):
                continue

            db.add(CharacterModel(**character_data))
            created_count += 1

        db.commit()

        print(f"Seed completed. Created {created_count} characters.")
    finally:
        db.close()


if __name__ == "__main__":
    main()