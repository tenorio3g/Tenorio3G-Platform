from __future__ import annotations

from sqlalchemy import select

from app.foundation.database import SessionLocal
from app.maps.models.map_location import MapLocation

from .map_location_repository import MapLocationRepository


class SQLiteMapLocationRepository(
    MapLocationRepository,
):
    """
    Implementación SQLite del repositorio de ubicaciones.
    """

    def find_all(self) -> list[MapLocation]:
        with SessionLocal() as session:
            statement = (
                select(MapLocation)
                .order_by(MapLocation.name)
            )

            return list(
                session.scalars(statement).all()
            )

    def find_by_asset_code(
        self,
        asset_code: str,
    ) -> MapLocation | None:
        clean_code = asset_code.strip()

        with SessionLocal() as session:
            statement = select(MapLocation).where(
                MapLocation.asset_code == clean_code
            )

            return session.scalar(statement)

    def save(
        self,
        location: MapLocation,
    ) -> None:
        with SessionLocal() as session:
            existing = session.scalar(
                select(MapLocation).where(
                    MapLocation.asset_code
                    == location.asset_code
                )
            )

            if existing is None:
                session.add(location)
            else:
                existing.name = location.name
                existing.category = location.category
                existing.x = location.x
                existing.y = location.y

            session.commit()

    def delete(
        self,
        asset_code: str,
    ) -> None:
        clean_code = asset_code.strip()

        with SessionLocal() as session:
            location = session.scalar(
                select(MapLocation).where(
                    MapLocation.asset_code == clean_code
                )
            )

            if location is None:
                return

            session.delete(location)
            session.commit()