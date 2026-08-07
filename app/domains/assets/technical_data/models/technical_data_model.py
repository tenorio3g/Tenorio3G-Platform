from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.foundation.database import Base


class TechnicalDataModel(Base):
    """
    Modelo ORM para la información técnica de un activo.

    Este modelo pertenece a la infraestructura de persistencia.
    No contiene lógica de negocio.
    """

    __tablename__ = "asset_technical_data"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    asset_code: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        nullable=False,
        index=True,
    )

    equipment_type: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    manufacturer: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    serial_number: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    voltage: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    phases: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    frequency: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    motor_power: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    observations: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    def __repr__(self) -> str:
        return (
            "TechnicalDataModel("
            f"asset_code='{self.asset_code}', "
            f"equipment_type='{self.equipment_type}', "
            f"model='{self.model}'"
            ")"
        )