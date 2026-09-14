from datetime import datetime

from sqlalchemy import (
    DateTime,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.foundation.database import Base


class ActivityHoldModel(Base):

    __tablename__ = "activity_holds"

    code: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    activity_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    reason: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    observations: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
        default="",
    )

    held_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    held_by_person_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    resumed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    resumed_by_person_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
