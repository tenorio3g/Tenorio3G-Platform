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


class WorkOrderTechnicianAssignmentModel(Base):

    __tablename__ = (
        "work_order_technician_assignments"
    )

    work_order_code: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    person_code: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    unassigned_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )