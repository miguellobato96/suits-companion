from sqlalchemy import select

from app.character_models import CharacterModel
from app.database import SessionLocal
from app.franchise_models import FranchiseModel
from app.media_models import MediaModel
from app.reference_models import ReferenceModel


FRANCHISES = [
    "Batman",
    "Dirty Harry",
    "Indiana Jones",
    "James Bond",
    "Rocky",
    "Star Trek",
    "Star Wars",
    "Superman",
    "Terminator",
    "The Godfather",
]


MEDIA = [
    {
        "title": "One Flew Over the Cuckoo's Nest",
        "media_type": "movie",
        "release_year": 1975,
        "franchises": [],
    },
    {
        "title": "Serpico",
        "media_type": "movie",
        "release_year": 1973,
        "franchises": [],
    },
    {
        "title": "The Godfather",
        "media_type": "movie",
        "release_year": 1972,
        "franchises": ["The Godfather"],
    },
    {
        "title": "Batman",
        "media_type": "movie",
        "release_year": 1989,
        "franchises": ["Batman"],
    },
    {
        "title": "Batman Returns",
        "media_type": "movie",
        "release_year": 1992,
        "franchises": ["Batman"],
    },
    {
        "title": "Batman Forever",
        "media_type": "movie",
        "release_year": 1995,
        "franchises": ["Batman"],
    },
    {
        "title": "Batman & Robin",
        "media_type": "movie",
        "release_year": 1997,
        "franchises": ["Batman"],
    },
    {
        "title": "Animal House",
        "media_type": "movie",
        "release_year": 1978,
        "franchises": [],
    },
    {
        "title": "Raiders of the Lost Ark",
        "media_type": "movie",
        "release_year": 1981,
        "franchises": ["Indiana Jones"],
    },
    {
        "title": "Fast Times at Ridgemont High",
        "media_type": "movie",
        "release_year": 1982,
        "franchises": [],
    },
    {
        "title": "Wall Street",
        "media_type": "movie",
        "release_year": 1987,
        "franchises": [],
    },
    {
        "title": "To Kill a Mockingbird",
        "media_type": "movie",
        "release_year": 1962,
        "franchises": [],
    },
    {
        "title": "Ally McBeal",
        "media_type": "series",
        "release_year": 1997,
        "franchises": [],
    },
    {
        "title": "Old School",
        "media_type": "movie",
        "release_year": 2003,
        "franchises": [],
    },
    {
        "title": "Rocky",
        "media_type": "movie",
        "release_year": 1976,
        "franchises": ["Rocky"],
    },
    {
        "title": "Rocky III",
        "media_type": "movie",
        "release_year": 1982,
        "franchises": ["Rocky"],
    },
    {
        "title": "Top Gun",
        "media_type": "movie",
        "release_year": 1986,
        "franchises": [],
    },
    {
        "title": "Good Will Hunting",
        "media_type": "movie",
        "release_year": 1997,
        "franchises": [],
    },
    {
        "title": "Star Trek II: The Wrath of Khan",
        "media_type": "movie",
        "release_year": 1982,
        "franchises": ["Star Trek"],
    },
    {
        "title": "The Girl with the Dragon Tattoo",
        "media_type": "movie",
        "release_year": 2011,
        "franchises": [],
    },
    {
        "title": "Dirty Harry",
        "media_type": "movie",
        "release_year": 1971,
        "franchises": ["Dirty Harry"],
    },
    {
        "title": "The Terminator",
        "media_type": "movie",
        "release_year": 1984,
        "franchises": ["Terminator"],
    },
    {
        "title": "Goldfinger",
        "media_type": "movie",
        "release_year": 1964,
        "franchises": ["James Bond"],
    },
    {
        "title": "Octopussy",
        "media_type": "movie",
        "release_year": 1983,
        "franchises": ["James Bond"],
    },
    {
        "title": "Lord of the Flies",
        "media_type": "book",
        "release_year": 1954,
        "franchises": [],
    },
    {
        "title": "Frasier",
        "media_type": "series",
        "release_year": 1993,
        "franchises": [],
    },
    {
        "title": "Spies Like Us",
        "media_type": "movie",
        "release_year": 1985,
        "franchises": [],
    },
    {
        "title": "Philadelphia",
        "media_type": "movie",
        "release_year": 1993,
        "franchises": [],
    },
    {
        "title": "Mississippi Burning",
        "media_type": "movie",
        "release_year": 1988,
        "franchises": [],
    },
    {
        "title": "Casablanca",
        "media_type": "movie",
        "release_year": 1942,
        "franchises": [],
    },
    {
        "title": "Gone with the Wind",
        "media_type": "movie",
        "release_year": 1939,
        "franchises": [],
    },
    {
        "title": "Citizen Kane",
        "media_type": "movie",
        "release_year": 1941,
        "franchises": [],
    },
    {
        "title": "Dirty Dancing",
        "media_type": "movie",
        "release_year": 1987,
        "franchises": [],
    },
]


def get_or_create_franchise(
    db,
    name: str,
) -> tuple[FranchiseModel, bool]:
    franchise = db.scalar(
        select(FranchiseModel).where(
            FranchiseModel.name == name
        )
    )

    if franchise is not None:
        return franchise, False

    franchise = FranchiseModel(name=name)

    db.add(franchise)
    db.flush()

    return franchise, True


def get_media(
    db,
    title: str,
    media_type: str,
    release_year: int | None,
) -> MediaModel | None:
    return db.scalar(
        select(MediaModel).where(
            MediaModel.title == title,
            MediaModel.media_type == media_type,
            MediaModel.release_year == release_year,
        )
    )


def seed_media() -> None:
    with SessionLocal() as db:
        franchise_map: dict[str, FranchiseModel] = {}

        inserted_franchises = 0
        inserted_media = 0

        for franchise_name in FRANCHISES:
            franchise, created = get_or_create_franchise(
                db,
                franchise_name,
            )

            franchise_map[franchise_name] = franchise

            if created:
                inserted_franchises += 1

        for media_data in MEDIA:
            media = get_media(
                db=db,
                title=media_data["title"],
                media_type=media_data["media_type"],
                release_year=media_data["release_year"],
            )

            if media is None:
                media = MediaModel(
                    title=media_data["title"],
                    media_type=media_data["media_type"],
                    release_year=media_data["release_year"],
                )

                db.add(media)
                inserted_media += 1

            expected_franchises = [
                franchise_map[name]
                for name in media_data["franchises"]
            ]

            existing_franchise_ids = {
                franchise.id
                for franchise in media.franchises
            }

            for franchise in expected_franchises:
                if franchise.id not in existing_franchise_ids:
                    media.franchises.append(franchise)

        db.commit()

        print(f"Inserted {inserted_franchises} franchises.")
        print(f"Inserted {inserted_media} media records.")


if __name__ == "__main__":
    seed_media()