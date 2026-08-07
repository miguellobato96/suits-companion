from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from app.database import Base


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