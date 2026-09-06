from __future__ import annotations

from datetime import date

from sqlalchemy import (
    Date,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.foundation.database import Base


class AssetRecordModel(Base):

    __tablename__ = "assets"

    code: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    asset_model_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    serial_number: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="",
    )

    location_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    installation_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    deactivation_reason: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )
