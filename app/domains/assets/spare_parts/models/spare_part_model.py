from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.foundation.database import Base


class SparePartModel(Base):
    """
    Modelo ORM para una refacción.
    """

    __tablename__ = "spare_parts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    code: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )

    manufacturer: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        default="",
    )

    part_number: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        default="",
    )

    unit: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="pieza",
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )