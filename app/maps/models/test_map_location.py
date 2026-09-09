from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base
from app.maps.models.map_location import MapLocation


def test_should_persist_map_location() -> None:
    test_engine = create_engine(
        "sqlite:///:memory:",
        future=True,
    )

    TestSession = sessionmaker(
        bind=test_engine,
        future=True,
    )

    Base.metadata.create_all(
        test_engine,
        tables=[MapLocation.__table__],
    )

    location = MapLocation(
        asset_code="S2-480-ES09-T269",
        name="TABLERO GENERAL ES09",
        category="tableros",
        x=52.4,
        y=38.7,
    )

    with TestSession() as session:
        session.add(location)
        session.commit()

        persisted = session.scalar(
            select(MapLocation).where(
                MapLocation.asset_code
                == "S2-480-ES09-T269"
            )
        )

        assert persisted is not None
        assert persisted.asset_code == (
            "S2-480-ES09-T269"
        )
        assert persisted.layer_code == "electrical"
        assert persisted.name == (
            "TABLERO GENERAL ES09"
        )
        assert persisted.category == "tableros"
        assert persisted.x == 52.4
        assert persisted.y == 38.7

    test_engine.dispose()


def test_should_default_to_electrical_layer():
    location = MapLocation(
        asset_code="T269",
        name="Tablero General ES09",
        category="panel",
        x=50.0,
        y=40.0,
    )

    assert location.layer_code == "electrical"


def test_should_accept_explicit_layer_code():
    location = MapLocation(
        asset_code="CH-001",
        name="Chiller 1",
        category="chiller",
        x=25.0,
        y=30.0,
        layer_code="hvac",
    )

    assert location.layer_code == "hvac"


def test_should_normalize_layer_code():
    location = MapLocation(
        asset_code="CH-001",
        name="Chiller 1",
        category="chiller",
        x=25.0,
        y=30.0,
        layer_code="  HVAC  ",
    )

    assert location.layer_code == "hvac"


def test_should_reject_empty_layer_code():
    try:
        MapLocation(
            asset_code="CH-001",
            name="Chiller 1",
            category="chiller",
            x=25.0,
            y=30.0,
            layer_code="   ",
        )
    except ValueError as exc:
        assert str(exc) == (
            "El codigo de la capa es obligatorio."
        )
    else:
        raise AssertionError(
            "Se esperaba ValueError."
        )
def test_should_use_ground_floor_as_default_plan() -> None:
    location = MapLocation(
        asset_code="ASSET-PLAN-001",
        name="Activo con plano por defecto",
        category="default",
        x=10.0,
        y=20.0,
    )

    assert location.plan_code == "ground_floor"


def test_should_accept_explicit_plan_code() -> None:
    location = MapLocation(
        asset_code="ASSET-PLAN-002",
        name="Activo en techo",
        category="default",
        x=30.0,
        y=40.0,
        plan_code="roof",
    )

    assert location.plan_code == "roof"


def test_should_normalize_plan_code() -> None:
    location = MapLocation(
        asset_code="ASSET-PLAN-003",
        name="Activo en planta alta",
        category="default",
        x=50.0,
        y=60.0,
        plan_code="  UPPER_FLOOR  ",
    )

    assert location.plan_code == "upper_floor"


def test_should_reject_empty_plan_code() -> None:
    try:
        MapLocation(
            asset_code="ASSET-PLAN-004",
            name="Activo sin plano",
            category="default",
            x=70.0,
            y=80.0,
            plan_code="   ",
        )
    except ValueError as error:
        assert str(error) == (
            "El codigo del plano es obligatorio."
        )
    else:
        raise AssertionError(
            "Se esperaba ValueError para plan_code vacio."
        )
