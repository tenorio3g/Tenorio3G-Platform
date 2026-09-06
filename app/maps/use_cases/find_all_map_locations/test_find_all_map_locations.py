from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base
from app.maps.models.map_location import (
    MapLocation,
)
from app.maps.repositories.sqlite_map_location_repository import (
    SQLiteMapLocationRepository,
)
from app.maps.use_cases.find_all_map_locations.find_all_map_locations import (
    FindAllMapLocations,
)


def test_should_find_all_map_locations(
    tmp_path,
) -> None:
    database_path = (
        tmp_path
        / "maps_find_all.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    TestSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(
        bind=engine
    )

    repository = (
        SQLiteMapLocationRepository(
            TestSessionLocal
        )
    )

    repository.save(
        MapLocation(
            asset_code="ASSET-001",
            name="Activo 1",
            category="default",
            x=10.0,
            y=20.0,
        )
    )

    repository.save(
        MapLocation(
            asset_code="ASSET-002",
            name="Activo 2",
            category="default",
            x=30.0,
            y=40.0,
        )
    )

    use_case = FindAllMapLocations(
        repository
    )

    result = use_case.execute()

    assert result.success is True
    assert len(result.locations) == 2

    assert result.locations[0].asset_code == (
        "ASSET-001"
    )

    assert result.locations[1].asset_code == (
        "ASSET-002"
    )

    engine.dispose()
