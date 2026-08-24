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


class WorkOrderModel(Base):

    __tablename__ = "work_orders"

    code: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
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

    work_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    priority: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    asset_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    requester_person_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    requester_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    requester_phone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    requester_area: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    supervisor_person_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )

    location_description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )