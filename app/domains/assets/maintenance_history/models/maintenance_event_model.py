from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.foundation.database import Base


class MaintenanceEventModel(Base):
    __tablename__ = "asset_maintenance_events"

    code: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    asset_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
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

    performed_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    observations: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
        default="",
    )