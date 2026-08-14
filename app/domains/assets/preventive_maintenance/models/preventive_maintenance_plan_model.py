from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.foundation.database import Base


class PreventiveMaintenancePlanModel(Base):

    __tablename__ = (
        "asset_preventive_maintenance_plans"
    )

    code: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    asset_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    frequency_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    responsible_person_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    next_due_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
        default="",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )