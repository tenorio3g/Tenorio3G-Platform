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


def test_should_persist_explicit_layer_code(
    tmp_path,
) -> None:
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        MapLocation(
            asset_code="CH-001",
            name="Chiller 1",
            category="chiller",
            x=25.0,
            y=30.0,
            layer_code="hvac",
        )
    )

    saved = repository.find_by_asset_code(
        "CH-001"
    )

    assert saved is not None
    assert saved.layer_code == "hvac"

    engine.dispose()


def test_should_update_existing_layer_code(
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
            layer_code="electrical",
        )
    )

    repository.save(
        MapLocation(
            asset_code="ASSET-001",
            name="Activo 1",
            category="default",
            x=15.0,
            y=25.0,
            layer_code="hvac",
        )
    )

    saved = repository.find_by_asset_code(
        "ASSET-001"
    )

    assert saved is not None
    assert saved.layer_code == "hvac"
    assert saved.x == 15.0
    assert saved.y == 25.0

    engine.dispose()
def test_should_persist_explicit_plan_code(
    tmp_path,
) -> None:
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        MapLocation(
            asset_code="CH-ROOF-001",
            name="Chiller en techo",
            category="chiller",
            x=25.0,
            y=30.0,
            layer_code="hvac",
            plan_code="roof",
        )
    )

    saved = repository.find_by_asset_code(
        "CH-ROOF-001"
    )

    assert saved is not None
    assert saved.plan_code == "roof"
    assert saved.layer_code == "hvac"

    engine.dispose()


def test_should_update_existing_plan_code(
    tmp_path,
) -> None:
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        MapLocation(
            asset_code="ASSET-PLAN-001",
            name="Activo 1",
            category="default",
            x=10.0,
            y=20.0,
            layer_code="electrical",
            plan_code="ground_floor",
        )
    )

    repository.save(
        MapLocation(
            asset_code="ASSET-PLAN-001",
            name="Activo 1",
            category="default",
            x=15.0,
            y=25.0,
            layer_code="electrical",
            plan_code="upper_floor",
        )
    )

    saved = repository.find_by_asset_code(
        "ASSET-PLAN-001"
    )

    assert saved is not None
    assert saved.plan_code == "upper_floor"
    assert saved.layer_code == "electrical"
    assert saved.x == 15.0
    assert saved.y == 25.0

    engine.dispose()
