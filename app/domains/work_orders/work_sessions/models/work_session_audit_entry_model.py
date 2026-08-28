from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.foundation.database import Base


class WorkSessionAuditEntryModel(Base):

    __tablename__ = "work_session_audit_entries"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    work_session_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    reason: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
    )

    actor_person_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    previous_started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    previous_ended_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    new_started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    new_ended_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )
