from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.media_models import reference_media


class ReferenceModel(Base):
    __tablename__ = "cultural_references"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    reference_type: Mapped[str] = mapped_column(String(50), nullable=False)

    season: Mapped[int | None] = mapped_column(Integer, nullable=True)
    episode: Mapped[int | None] = mapped_column(Integer, nullable=True)

    quote: Mapped[str | None] = mapped_column(Text, nullable=True)
    context: Mapped[str] = mapped_column(Text, nullable=False)

    spoken_by_character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    spoken_by_character = relationship("CharacterModel")

    media: Mapped[list["MediaModel"]] = relationship(
        secondary=reference_media,
        back_populates="references",
    )