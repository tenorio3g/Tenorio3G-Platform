from __future__ import annotations

from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.maps.models.map_layer import MapLayer

from .map_layer_repository import MapLayerRepository


class SQLiteMapLayerRepository(
    MapLayerRepository,
):
    """
    Implementacion SQLite del repositorio de capas del mapa.
    """

    def __init__(
        self,
        session_factory: Callable[[], Session],
    ) -> None:
        self._session_factory = session_factory

    def save(
        self,
        layer: MapLayer,
    ) -> None:
        with self._session_factory() as session:
            existing = session.scalar(
                select(MapLayer).where(
                    MapLayer.code == layer.code
                )
            )

            if existing is None:
                session.add(layer)

            else:
                existing.name = layer.name
                existing.order = layer.order
                existing.is_active = layer.is_active

            session.commit()

    def find_by_code(
        self,
        code: str,
    ) -> MapLayer | None:
        clean_code = str(code).strip().lower()

        with self._session_factory() as session:
            statement = select(
                MapLayer
            ).where(
                MapLayer.code == clean_code
            )

            return session.scalar(statement)

    def find_all(
        self,
    ) -> list[MapLayer]:
        with self._session_factory() as session:
            statement = (
                select(MapLayer)
                .order_by(
                    MapLayer.order,
                    MapLayer.name,
                )
            )

            return list(
                session.scalars(statement).all()
            )

    def find_active(
        self,
    ) -> list[MapLayer]:
        with self._session_factory() as session:
            statement = (
                select(MapLayer)
                .where(
                    MapLayer.is_active.is_(True)
                )
                .order_by(
                    MapLayer.order,
                    MapLayer.name,
                )
            )

            return list(
                session.scalars(statement).all()
            )
