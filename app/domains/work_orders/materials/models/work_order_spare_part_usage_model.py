from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.foundation.database import Base


class WorkOrderSparePartUsageModel(Base):

    __tablename__ = "work_order_spare_part_usages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    work_order_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    spare_part_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    quantity: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    unit_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0,
    )

    used_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    observations: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
        default="",
    )