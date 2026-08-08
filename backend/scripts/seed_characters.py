from sqlalchemy import select

from app.character_models import CharacterModel
from app.database import SessionLocal


CHARACTERS = [
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
        "role": "Legal Secretary",
        "actor": "Sarah Rafferty",
    },
    {
        "name": "Louis Litt",
        "role": "Junior Partner",
        "actor": "Rick Hoffman",
    },
    {
        "name": "Jessica Pearson",
        "role": "Managing Partner",
        "actor": "Gina Torres",
    },
    {
        "name": "Rachel Zane",
        "role": "Paralegal",
        "actor": "Meghan Markle",
    },
    {
        "name": "Jenny Griffith",
        "role": "Friend of Mike Ross",
        "actor": "Vanessa Ray",
    },
    {
        "name": "Trevor Evans",
        "role": "Friend of Mike Ross",
        "actor": "Tom Lipinski",
    },
    {
        "name": "Wyatt",
        "role": "CEO of Suntech Digital",
        "actor": "Eric Ladin",
    },
    {
        "name": "Vanessa",
        "role": "Private Investigator",
        "actor": "Julie Ann Emery",
    },
    {
        "name": "Tony Santana",
        "role": "Taxi Driver",
        "actor": "José Zúñiga",
    },
    {
        "name": "Detective Packel",
        "role": "Police Detective",
        "actor": "Ari Cohen",
    },
]


def seed_characters() -> None:
    with SessionLocal() as db:
        inserted = 0

        for character_data in CHARACTERS:
            existing = db.scalar(
                select(CharacterModel).where(
                    CharacterModel.name == character_data["name"]
                )
            )

            if existing is not None:
                continue

            db.add(CharacterModel(**character_data))
            inserted += 1

        db.commit()

        print(f"Inserted {inserted} characters.")


if __name__ == "__main__":
    seed_characters()