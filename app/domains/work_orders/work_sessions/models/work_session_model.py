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


class WorkSessionModel(Base):

    __tablename__ = "work_sessions"

    code: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    work_order_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    activity_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    person_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
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
