from __future__ import annotations

from app.foundation.database import Base, engine
from app.maps.models.map_location import MapLocation
from app.maps.repositories.sqlite_map_location_repository import (
    SQLiteMapLocationRepository,
)


def test_should_find_all_map_locations() -> None:
    Base.metadata.create_all(engine)

    repository = SQLiteMapLocationRepository()

    repository.save(
        MapLocation(
            asset_code="TEST-MAP-001",
            name="Ubicación de prueba",
            category="tableros",
            x=25.5,
            y=40.2,
        )
    )

    locations = repository.find_all()

    assert isinstance(locations, list)
    assert any(
        location.asset_code == "TEST-MAP-001"
        for location in locations
    )

    repository.delete("TEST-MAP-001")