from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.franchise_models import FranchiseModel

if TYPE_CHECKING:
    from app.reference_models import ReferenceModel


media_franchises = Table(
    "media_franchises",
    Base.metadata,
    Column(
        "media_id",
        ForeignKey("media.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "franchise_id",
        ForeignKey("franchises.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


reference_media = Table(
    "reference_media",
    Base.metadata,
    Column(
        "reference_id",
        ForeignKey("cultural_references.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "media_id",
        ForeignKey("media.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


reference_franchises = Table(
    "reference_franchises",
    Base.metadata,
    Column(
        "reference_id",
        ForeignKey("cultural_references.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "franchise_id",
        ForeignKey("franchises.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class MediaModel(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    media_type: Mapped[str] = mapped_column(String(50), nullable=False)
    release_year: Mapped[int | None] = mapped_column(nullable=True)

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

    franchises: Mapped[list[FranchiseModel]] = relationship(
        secondary=media_franchises,
        back_populates="media",
    )

    references: Mapped[list["ReferenceModel"]] = relationship(
        secondary=reference_media,
        back_populates="media",
    )
