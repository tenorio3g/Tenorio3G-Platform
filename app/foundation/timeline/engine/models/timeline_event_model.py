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


class TimelineEventModel(Base):

    __tablename__ = "timeline_events"

    event_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    entity_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    entity_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
        default="",
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

    reference_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    reference_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )