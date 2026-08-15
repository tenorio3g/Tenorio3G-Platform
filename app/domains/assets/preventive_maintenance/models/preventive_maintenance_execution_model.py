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


class PreventiveMaintenanceExecutionModel(Base):

    __tablename__ = (
        "asset_preventive_maintenance_executions"
    )

    code: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    plan_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    asset_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    performed_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )


    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )


    completed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    observations: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
        default="",
    )