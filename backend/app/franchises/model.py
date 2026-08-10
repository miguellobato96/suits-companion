from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from app.core.database import Base

if TYPE_CHECKING:
    from app.media.model import MediaModel
    from app.references.model import ReferenceModel


class FranchiseModel(Base):
    __tablename__ = "franchises"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
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

    media: Mapped[list["MediaModel"]] = relationship(
        secondary="media_franchises",
        back_populates="franchises",
    )

    references: Mapped[list["ReferenceModel"]] = relationship(
        secondary="reference_franchises",
        back_populates="franchises",
    )
