from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReferenceModel(Base):
    __tablename__ = "cultural_references"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    reference_type: Mapped[str] = mapped_column(String(50), nullable=False)
    season: Mapped[int | None] = mapped_column(nullable=True)
    episode: Mapped[int | None] = mapped_column(nullable=True)
    context: Mapped[str] = mapped_column(Text, nullable=False)
    external_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    spoken_by_character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"),
        nullable=False,
        index=True,
    )

    spoken_by_character = relationship("CharacterModel")