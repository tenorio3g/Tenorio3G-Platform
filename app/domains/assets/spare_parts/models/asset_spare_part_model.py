from __future__ import annotations

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.foundation.database import Base


class AssetSparePartModel(Base):
    """
    Relación persistente entre un activo y una refacción.
    """

    __tablename__ = "asset_spare_parts"

    __table_args__ = (
        UniqueConstraint(
            "asset_code",
            "spare_part_code",
            name="uq_asset_spare_part",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    asset_code: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        index=True,
    )

    spare_part_code: Mapped[str] = mapped_column(
        ForeignKey("spare_parts.code"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1,
    )

    position: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
        default="",
    )

    observations: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    is_critical: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )