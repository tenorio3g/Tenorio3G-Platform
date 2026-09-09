from __future__ import annotations

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.foundation.database import Base


class MapLocation(Base):
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

    layer_code: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        default="electrical",
    )

    plan_code: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        default="ground_floor",
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

    def __init__(
        self,
        asset_code: str,
        name: str,
        x: float,
        y: float,
        category: str = "default",
        layer_code: str = "electrical",
        plan_code: str = "ground_floor",
    ) -> None:
        clean_layer_code = str(
            layer_code
        ).strip().lower()

        clean_plan_code = str(
            plan_code
        ).strip().lower()

        if not clean_layer_code:
            raise ValueError(
                "El codigo de la capa es obligatorio."
            )

        if not clean_plan_code:
            raise ValueError(
                "El codigo del plano es obligatorio."
            )

        self.asset_code = asset_code
        self.layer_code = clean_layer_code
        self.plan_code = clean_plan_code
        self.name = name
        self.category = category
        self.x = x
        self.y = y

    def move_to(
        self,
        x: float,
        y: float,
    ) -> None:
        if not self._coordinates_are_valid(
            x,
            y,
        ):
            raise ValueError(
                "Las coordenadas deben estar entre 0 y 100."
            )

        self.x = x
        self.y = y

    @staticmethod
    def _coordinates_are_valid(
        x: float,
        y: float,
    ) -> bool:
        return (
            0.0 <= x <= 100.0
            and 0.0 <= y <= 100.0
        )

    def __repr__(
        self,
    ) -> str:
        return (
            "MapLocation("
            f"asset_code='{self.asset_code}', "
            f"layer_code='{self.layer_code}', "
            f"plan_code='{self.plan_code}', "
            f"name='{self.name}', "
            f"x={self.x}, "
            f"y={self.y})"
        )
