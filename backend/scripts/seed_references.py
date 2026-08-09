from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.character_models import CharacterModel
from app.database import SessionLocal
from app.franchise_models import FranchiseModel
from app.media_models import MediaModel
from app.reference_models import ReferenceModel

MediaKey = tuple[str, int]


@dataclass(frozen=True)
class ReferenceSeed:
    title: str
    reference_type: str
    season: int
    episode: int
    character: str
    quote: str | None
    context: str
    media: tuple[MediaKey, ...] = ()
    franchises: tuple[str, ...] = ()


REFERENCES = [
    # S01E01 — Pilot
    ReferenceSeed(
        title="Serpico",
        reference_type="movie",
        season=1,
        episode=1,
        character="Harvey Specter",
        quote="I'll make sure Serpico isn't outside waiting for you.",
        context=(
            "Harvey references Serpico while joking about whether someone "
            "might be waiting outside for Mike."
        ),
        media=(("Serpico", 1973),),
    ),
    ReferenceSeed(
        title="Michael Corleone and Clemenza",
        reference_type="character",
        season=1,
        episode=1,
        character="Mike Ross",
        quote="I feel like Michael Corleone.",
        context=(
            "Mike compares himself to Michael Corleone and Harvey to "
            "Clemenza while discussing a scene from The Godfather."
        ),
        media=(("The Godfather", 1972),),
        franchises=("The Godfather",),
    ),
    ReferenceSeed(
        title="Wayne Manor",
        reference_type="franchise",
        season=1,
        episode=1,
        character="Harvey Specter",
        quote="I wouldn't move your things into Wayne Manor just yet.",
        context=(
            "Harvey invokes Bruce Wayne's home while telling Mike not to "
            "assume they are permanently a team."
        ),
        franchises=("Batman",),
    ),
    ReferenceSeed(
        title="Val Kilmer's Batman",
        reference_type="person",
        season=1,
        episode=1,
        character="Mike Ross",
        quote="Kilmer.",
        context=("Mike names Val Kilmer while he and Harvey compare Batman actors."),
        media=(("Batman Forever", 1995),),
        franchises=("Batman",),
    ),
    ReferenceSeed(
        title="George Clooney's Batman",
        reference_type="person",
        season=1,
        episode=1,
        character="Harvey Specter",
        quote="Clooney.",
        context=("Harvey chooses George Clooney during the Batman actor exchange."),
        media=(("Batman & Robin", 1997),),
        franchises=("Batman",),
    ),
    ReferenceSeed(
        title="Michael Keaton's Batman",
        reference_type="person",
        season=1,
        episode=1,
        character="Mike Ross",
        quote="Keaton.",
        context=("Mike chooses Michael Keaton during the Batman actor exchange."),
        media=(
            ("Batman", 1989),
            ("Batman Returns", 1992),
        ),
        franchises=("Batman",),
    ),
    ReferenceSeed(
        title="Dean Wormer",
        reference_type="character",
        season=1,
        episode=1,
        character="Mike Ross",
        quote="I work for Dean Wormer in the admissions office.",
        context=(
            "Mike uses the name Dean Wormer from Animal House while "
            "pretending to work in an admissions office."
        ),
        media=(("Animal House", 1978),),
    ),
    # S01E02 — Errors and Omissions
    ReferenceSeed(
        title="Ark of the Covenant",
        reference_type="movie",
        season=1,
        episode=2,
        character="Mike Ross",
        quote="The Ark of the Covenant is just down the hall.",
        context=(
            "Mike compares the firm's file storage to the government warehouse "
            "associated with Raiders of the Lost Ark."
        ),
        media=(("Raiders of the Lost Ark", 1981),),
        franchises=("Indiana Jones",),
    ),
    ReferenceSeed(
        title="Mr. Hand",
        reference_type="character",
        season=1,
        episode=2,
        character="Mike Ross",
        quote="But isn't this our time, Mr. Hand?",
        context=(
            "Mike quotes the classroom exchange involving Mr. Hand from "
            "Fast Times at Ridgemont High."
        ),
        media=(("Fast Times at Ridgemont High", 1982),),
    ),
    ReferenceSeed(
        title="Stormtroopers",
        reference_type="character",
        season=1,
        episode=2,
        character="Wyatt",
        quote="Wow, they're like Stormtroopers.",
        context=("Wyatt compares a group of investors to Imperial Stormtroopers."),
        franchises=("Star Wars",),
    ),
    # S01E03 — Meet the New Boss
    ReferenceSeed(
        title="Nurse Ratched",
        reference_type="character",
        season=1,
        episode=3,
        character="Harvey Specter",
        quote="Let me guess. Nurse Ratched.",
        context=(
            "Harvey references Nurse Ratched while joking about Mike's "
            "childhood caregiver fantasy."
        ),
        media=(("One Flew Over the Cuckoo's Nest", 1975),),
    ),
    # S01E05 — Bail Out
    ReferenceSeed(
        title="Gordon Gekko",
        reference_type="character",
        season=1,
        episode=5,
        character="Trevor Evans",
        quote="You look like Gordon Gekko's little brother.",
        context=("Trevor compares Mike's appearance to Gordon Gekko from Wall Street."),
        media=(("Wall Street", 1987),),
    ),
    ReferenceSeed(
        title="Atticus Finch",
        reference_type="character",
        season=1,
        episode=5,
        character="Harvey Specter",
        quote="I say Atticus Finch makes a good speech here.",
        context=("Harvey compares Tony's courtroom argument to Atticus Finch."),
        media=(("To Kill a Mockingbird", 1962),),
    ),
    ReferenceSeed(
        title="Ally McBeal",
        reference_type="series",
        season=1,
        episode=5,
        character="Harvey Specter",
        quote="You've seen way too many reruns of Ally McBeal.",
        context=(
            "Harvey jokes that Tony's legal reasoning comes from watching "
            "the legal television series Ally McBeal."
        ),
        media=(("Ally McBeal", 1997),),
    ),
    # S01E06 — Tricks of the Trade
    ReferenceSeed(
        title="Top Gun — Wingman",
        reference_type="movie",
        season=1,
        episode=6,
        character="Harvey Specter",
        quote="I am not leaving my wingman.",
        context=("Harvey deliberately uses a Top Gun reference while defending Louis."),
        media=(("Top Gun", 1986),),
    ),
    ReferenceSeed(
        title="Top Gun — Ego",
        reference_type="movie",
        season=1,
        episode=6,
        character="Jessica Pearson",
        quote="Your ego's writing checks that your body can't cash.",
        context=("Jessica answers Harvey with another Top Gun reference."),
        media=(("Top Gun", 1986),),
    ),
    ReferenceSeed(
        title="Rocky and Clubber Lang",
        reference_type="character",
        season=1,
        episode=6,
        character="Mike Ross",
        quote="It was like he was Mr. T and you were Rocky.",
        context=("Mike compares a confrontation to Rocky fighting Clubber Lang."),
        media=(("Rocky III", 1982),),
        franchises=("Rocky",),
    ),
    ReferenceSeed(
        title="Good Will Hunting",
        reference_type="movie",
        season=1,
        episode=6,
        character="Rachel Zane",
        quote="I can do the math, Good Will Hunting.",
        context=(
            "Rachel sarcastically compares Mike's explanation of basic arithmetic "
            "to the mathematical genius in Good Will Hunting."
        ),
        media=(("Good Will Hunting", 1997),),
    ),
    ReferenceSeed(
        title="Gordon Gekko — Greed is Good",
        reference_type="movie",
        season=1,
        episode=6,
        character="Mike Ross",
        quote="Greed is good!",
        context=(
            "Mike repeats the phrase strongly associated with Gordon Gekko "
            "in Wall Street."
        ),
        media=(("Wall Street", 1987),),
    ),
    ReferenceSeed(
        title="Old School",
        reference_type="movie",
        season=1,
        episode=6,
        character="Mike Ross",
        quote="Make money money, make money!",
        context=("Mike echoes the party sequence and music used in Old School."),
        media=(("Old School", 2003),),
    ),
    # S01E07 — Play the Man
    ReferenceSeed(
        title="Clark Kent",
        reference_type="character",
        season=1,
        episode=7,
        character="Jenny Griffith",
        quote="You're maybe not as cool as Clark Kent.",
        context=("Jenny compares Mike's secret double life to Clark Kent's."),
        franchises=("Superman",),
    ),
    ReferenceSeed(
        title="Kobayashi Maru",
        reference_type="franchise",
        season=1,
        episode=7,
        character="Harvey Specter",
        quote="Kobayashi Maru.",
        context=(
            "Harvey uses Captain Kirk's solution to the no-win Kobayashi Maru "
            "scenario as an example of rewriting the rules."
        ),
        media=(("Star Trek II: The Wrath of Khan", 1982),),
        franchises=("Star Trek",),
    ),
    # S01E08 — Identity Crisis
    ReferenceSeed(
        title="Dirty Harry",
        reference_type="character",
        season=1,
        episode=8,
        character="Harvey Specter",
        quote="Feeling lucky today, punk?",
        context=("Harvey references Dirty Harry after seeing Louis with a .44 Magnum."),
        media=(("Dirty Harry", 1971),),
        franchises=("Dirty Harry",),
    ),
    ReferenceSeed(
        title="Tom Hagen and Fredo Corleone",
        reference_type="character",
        season=1,
        episode=8,
        character="Harvey Specter",
        quote="I'm more like Robert Duvall. Godfather. His consigliere.",
        context=(
            "Harvey compares himself to Tom Hagen and then compares Mike to Fredo "
            "from The Godfather."
        ),
        media=(("The Godfather", 1972),),
        franchises=("The Godfather",),
    ),
    # S01E09 — Undefeated
    ReferenceSeed(
        title="James Bond",
        reference_type="franchise",
        season=1,
        episode=9,
        character="Harvey Specter",
        quote="Then I wouldn't feel like James Bond.",
        context=(
            "Harvey compares the secrecy of paying Vanessa to a James Bond scene."
        ),
        franchises=("James Bond",),
    ),
    ReferenceSeed(
        title="Pussy Galore",
        reference_type="character",
        season=1,
        episode=9,
        character="Harvey Specter",
        quote="Pussy Galore.",
        context=("Harvey compares Vanessa to the Bond character Pussy Galore."),
        media=(("Goldfinger", 1964),),
        franchises=("James Bond",),
    ),
    ReferenceSeed(
        title="Octopussy",
        reference_type="character",
        season=1,
        episode=9,
        character="Harvey Specter",
        quote="Octopussy?",
        context=("Harvey follows his Bond reference by naming Octopussy."),
        media=(("Octopussy", 1983),),
        franchises=("James Bond",),
    ),
    ReferenceSeed(
        title="Darth Vader",
        reference_type="character",
        season=1,
        episode=9,
        character="Mike Ross",
        quote="It's Louis Litt, not Darth Vader.",
        context=("Mike tells Jimmy not to treat Louis as though he were Darth Vader."),
        franchises=("Star Wars",),
    ),
    ReferenceSeed(
        title="Lord of the Flies",
        reference_type="book",
        season=1,
        episode=9,
        character="Mike Ross",
        quote="This is a law office, not Lord of the Flies.",
        context=(
            "Mike invokes Lord of the Flies while trying to stop the associates "
            "from turning on one another."
        ),
        media=(("Lord of the Flies", 1954),),
    ),
    # S01E10 — The Shelf Life
    ReferenceSeed(
        title="Niles Crane",
        reference_type="character",
        season=1,
        episode=10,
        character="Harvey Specter",
        quote="You sound like Frasier's brother.",
        context=("Harvey compares Louis's fussiness about wine to Niles Crane."),
        media=(("Frasier", 1993),),
    ),
    # S01E11 — Rules of the Game
    ReferenceSeed(
        title="Spies Like Us",
        reference_type="movie",
        season=1,
        episode=11,
        character="Mike Ross",
        quote="Doctor. Doctor.",
        context=(
            "Mike and Harvey reproduce the recurring doctor greeting gag "
            "from Spies Like Us."
        ),
        media=(("Spies Like Us", 1985),),
    ),
    ReferenceSeed(
        title="James Bond Actors",
        reference_type="franchise",
        season=1,
        episode=11,
        character="Mike Ross",
        quote="I could be James Bond.",
        context=(
            "Mike compares himself to different James Bond actors, including "
            "Sean Connery, Daniel Craig and George Lazenby."
        ),
        franchises=("James Bond",),
    ),
    # S01E12 — Dog Fight
    ReferenceSeed(
        title="Mississippi Burning",
        reference_type="movie",
        season=1,
        episode=12,
        character="Harvey Specter",
        quote="Looks like the rattlesnakes are starting to commit suicide.",
        context=(
            "Harvey and Mike use tactics and dialogue inspired by "
            "Mississippi Burning during the case."
        ),
        media=(("Mississippi Burning", 1988),),
    ),
    ReferenceSeed(
        title="Casablanca",
        reference_type="movie",
        season=1,
        episode=12,
        character="Mike Ross",
        quote=None,
        context=(
            "Mike brings up Casablanca while discussing classic films with Rachel."
        ),
        media=(("Casablanca", 1942),),
    ),
    ReferenceSeed(
        title="Gone with the Wind",
        reference_type="movie",
        season=1,
        episode=12,
        character="Mike Ross",
        quote="Gone With The Wind?",
        context=("Mike asks Rachel whether she has seen Gone with the Wind."),
        media=(("Gone with the Wind", 1939),),
    ),
    ReferenceSeed(
        title="Citizen Kane",
        reference_type="movie",
        season=1,
        episode=12,
        character="Mike Ross",
        quote="Citizen Kane?",
        context=("Mike asks Rachel whether she has seen Citizen Kane."),
        media=(("Citizen Kane", 1941),),
    ),
    ReferenceSeed(
        title="Dirty Dancing",
        reference_type="movie",
        season=1,
        episode=12,
        character="Rachel Zane",
        quote="Nobody puts Baby in the corner.",
        context=("Rachel recognizes Dirty Dancing by quoting its best-known line."),
        media=(("Dirty Dancing", 1987),),
    ),
]


def load_characters(db: Session) -> dict[str, CharacterModel]:
    characters = db.scalars(select(CharacterModel)).all()

    return {character.name: character for character in characters}


def load_media(db: Session) -> dict[MediaKey, MediaModel]:
    media_items = db.scalars(select(MediaModel)).all()

    return {
        (media.title, media.release_year): media
        for media in media_items
        if media.release_year is not None
    }


def load_franchises(db: Session) -> dict[str, FranchiseModel]:
    franchises = db.scalars(select(FranchiseModel)).all()

    return {franchise.name: franchise for franchise in franchises}


def validate_dependencies(
    characters: dict[str, CharacterModel],
    media: dict[MediaKey, MediaModel],
    franchises: dict[str, FranchiseModel],
) -> None:
    missing_characters = sorted(
        {
            reference.character
            for reference in REFERENCES
            if reference.character not in characters
        }
    )

    missing_media = sorted(
        {
            media_key
            for reference in REFERENCES
            for media_key in reference.media
            if media_key not in media
        }
    )

    missing_franchises = sorted(
        {
            franchise_name
            for reference in REFERENCES
            for franchise_name in reference.franchises
            if franchise_name not in franchises
        }
    )

    errors = []

    if missing_characters:
        errors.append(f"Missing characters: {missing_characters}")

    if missing_media:
        errors.append(f"Missing media: {missing_media}")

    if missing_franchises:
        errors.append(f"Missing franchises: {missing_franchises}")

    if errors:
        raise RuntimeError("\n".join(errors))


def get_existing_reference(
    db: Session,
    reference: ReferenceSeed,
    character_id: int,
) -> ReferenceModel | None:
    statement = select(ReferenceModel).where(
        ReferenceModel.season == reference.season,
        ReferenceModel.episode == reference.episode,
        ReferenceModel.title == reference.title,
        ReferenceModel.spoken_by_character_id == character_id,
    )

    return db.scalar(statement)


def sync_reference(
    existing: ReferenceModel,
    reference: ReferenceSeed,
    media_items: list[MediaModel],
    franchise_items: list[FranchiseModel],
) -> bool:
    changed = False

    scalar_values = {
        "reference_type": reference.reference_type,
        "quote": reference.quote,
        "context": reference.context,
    }

    for field, value in scalar_values.items():
        if getattr(existing, field) != value:
            setattr(existing, field, value)
            changed = True

    current_media_ids = {item.id for item in existing.media}

    expected_media_ids = {item.id for item in media_items}

    if current_media_ids != expected_media_ids:
        existing.media = media_items
        changed = True

    current_franchise_ids = {item.id for item in existing.franchises}

    expected_franchise_ids = {item.id for item in franchise_items}

    if current_franchise_ids != expected_franchise_ids:
        existing.franchises = franchise_items
        changed = True

    return changed


def seed_references() -> None:
    with SessionLocal() as db:
        characters = load_characters(db)
        media = load_media(db)
        franchises = load_franchises(db)

        validate_dependencies(
            characters=characters,
            media=media,
            franchises=franchises,
        )

        inserted = 0
        updated = 0

        for reference in REFERENCES:
            character = characters[reference.character]

            media_items = [media[media_key] for media_key in reference.media]

            franchise_items = [franchises[name] for name in reference.franchises]

            existing = get_existing_reference(
                db=db,
                reference=reference,
                character_id=character.id,
            )

            if existing is None:
                db.add(
                    ReferenceModel(
                        title=reference.title,
                        reference_type=reference.reference_type,
                        season=reference.season,
                        episode=reference.episode,
                        quote=reference.quote,
                        context=reference.context,
                        spoken_by_character_id=character.id,
                        media=media_items,
                        franchises=franchise_items,
                    )
                )

                inserted += 1
                continue

            if sync_reference(
                existing=existing,
                reference=reference,
                media_items=media_items,
                franchise_items=franchise_items,
            ):
                updated += 1

        db.commit()

        print(f"Inserted {inserted} references.")
        print(f"Updated {updated} references.")


if __name__ == "__main__":
    seed_references()
