from __future__ import annotations

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.foundation.database import Base


class MapLayer(Base):
    """
    Modelo persistente que representa una capa logica
    disponible dentro del mapa industrial.
    """

    __tablename__ = "map_layers"

    code: Mapped[str] = mapped_column(
        String(80),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    def __init__(
        self,
        code: str,
        name: str,
        order: int = 0,
        is_active: bool = True,
    ) -> None:
        clean_code = str(code).strip().lower()
        clean_name = str(name).strip()

        if not clean_code:
            raise ValueError(
                "El codigo de la capa es obligatorio."
            )

        if not clean_name:
            raise ValueError(
                "El nombre de la capa es obligatorio."
            )

        if not isinstance(order, int):
            raise ValueError(
                "El orden de la capa debe ser entero."
            )

        if order < 0:
            raise ValueError(
                "El orden de la capa no puede ser negativo."
            )

        if type(is_active) is not bool:
            raise ValueError(
                "El estado activo de la capa debe ser booleano."
            )

        self.code = clean_code
        self.name = clean_name
        self.order = order
        self.is_active = is_active

    def __repr__(self) -> str:
        return (
            "MapLayer("
            f"code='{self.code}', "
            f"name='{self.name}', "
            f"order={self.order}, "
            f"is_active={self.is_active})"
        )
