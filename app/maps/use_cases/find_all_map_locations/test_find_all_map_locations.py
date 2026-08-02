from __future__ import annotations

from app.foundation.database import Base, engine
from app.maps.models.map_location import MapLocation
from app.maps.repositories.sqlite_map_location_repository import (
    SQLiteMapLocationRepository,
)
from app.maps.use_cases.find_all_map_locations.find_all_map_locations import (
    FindAllMapLocations,
)


def test_should_find_all_map_locations() -> None:
    Base.metadata.create_all(engine)

    repository = SQLiteMapLocationRepository()

    repository.save(
        MapLocation(
            asset_code="TEST-USECASE-001",
            name="Ubicación del caso de uso",
            category="tableros",
            x=33.5,
            y=44.2,
        )
    )

    use_case = FindAllMapLocations(repository)

    result = use_case.execute()

    assert result.success is True
    assert result.message == (
        "Ubicaciones obtenidas correctamente."
    )
    assert any(
        location.asset_code == "TEST-USECASE-001"
        for location in result.locations
    )

    repository.delete("TEST-USECASE-001")