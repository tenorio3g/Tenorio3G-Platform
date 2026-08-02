from __future__ import annotations

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.foundation.database import Base


class MapLocation(Base):
    """
    Modelo persistente que representa la posición de un activo
    dentro del mapa industrial.
    """

    __tablename__ = "map_locations"

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

    name: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="default",
    )

    x: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    y: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            "MapLocation("
            f"asset_code='{self.asset_code}', "
            f"name='{self.name}', "
            f"x={self.x}, "
            f"y={self.y})"
        )