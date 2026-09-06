from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base
from app.maps.models.map_location import (
    MapLocation,
)
from app.maps.repositories.sqlite_map_location_repository import (
    SQLiteMapLocationRepository,
)


def create_repository(tmp_path):
    database_path = (
        tmp_path
        / "maps_repository.db"
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

    return repository, engine


def test_should_find_all_map_locations(
    tmp_path,
) -> None:
    repository, engine = create_repository(
        tmp_path
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

    locations = repository.find_all()

    assert len(locations) == 2

    assert locations[0].asset_code == (
        "ASSET-001"
    )

    assert locations[1].asset_code == (
        "ASSET-002"
    )

    engine.dispose()


def test_repository_should_use_injected_session_factory(
    tmp_path,
) -> None:
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        MapLocation(
            asset_code="MAP-TEST-001",
            name="Activo de prueba",
            category="default",
            x=25.0,
            y=40.0,
        )
    )

    saved = repository.find_by_asset_code(
        "MAP-TEST-001"
    )

    assert saved is not None
    assert saved.asset_code == "MAP-TEST-001"
    assert saved.x == 25.0
    assert saved.y == 40.0

    engine.dispose()
