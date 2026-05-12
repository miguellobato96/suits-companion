from app.character_schemas import Character, CharacterCreate


characters = [
    Character(
        id=1,
        name="Harvey Specter",
        role="Senior Partner",
        actor="Gabriel Macht",
    ),
    Character(
        id=2,
        name="Mike Ross",
        role="Associate",
        actor="Patrick J. Adams",
    ),
    Character(
        id=3,
        name="Donna Paulsen",
        role="Legal Secretary / COO",
        actor="Sarah Rafferty",
    ),
]


def get_all_characters(search: str | None = None) -> list[Character]:
    if search is None:
        return characters

    normalized_search = search.lower()

    return [
        character
        for character in characters
        if normalized_search in character.name.lower()
        or normalized_search in character.role.lower()
        or normalized_search in character.actor.lower()
    ]


def get_character_by_id(character_id: int) -> Character | None:
    for character in characters:
        if character.id == character_id:
            return character

    return None


def create_new_character(character_data: CharacterCreate) -> Character:
    character = Character(
        id=get_next_character_id(),
        name=character_data.name,
        role=character_data.role,
        actor=character_data.actor,
    )

    characters.append(character)

    return character


def update_existing_character(
    character_id: int,
    character_data: CharacterCreate,
) -> Character | None:
    for index, character in enumerate(characters):
        if character.id == character_id:
            updated_character = Character(
                id=character.id,
                name=character_data.name,
                role=character_data.role,
                actor=character_data.actor,
            )

            characters[index] = updated_character

            return updated_character

    return None


def delete_existing_character(character_id: int) -> bool:
    for index, character in enumerate(characters):
        if character.id == character_id:
            characters.pop(index)
            return True

    return False


def get_next_character_id() -> int:
    if not characters:
        return 1

    return max(character.id for character in characters) + 1