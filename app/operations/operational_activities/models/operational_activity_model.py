from datetime import datetime

from sqlalchemy import (
    DateTime,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.foundation.database import Base


class OperationalActivityModel(Base):

    __tablename__ = "operational_activities"

    code: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )

    result_notes: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    area: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        default="",
        index=True,
    )

    location_description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        default="",
    )

    asset_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    work_order_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    created_by_person_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    completed_by_person_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="",
        index=True,
    )
