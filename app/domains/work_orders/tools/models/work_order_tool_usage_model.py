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


class WorkOrderToolUsageModel(Base):

    __tablename__ = "work_order_tool_usages"

    usage_id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    work_order_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    tool_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    tool_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    issued_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True,
    )

    returned_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    observations: Mapped[str] = mapped_column(
        String(2000),
        nullable=False,
        default="",
    )