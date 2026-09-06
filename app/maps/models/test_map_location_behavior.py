import pytest

from app.maps.models.map_location import (
    MapLocation,
)


def create_location() -> MapLocation:
    return MapLocation(
        asset_code="ASSET-001",
        name="Tablero General",
        category="tableros",
        x=10.0,
        y=20.0,
    )


def test_should_move_map_location() -> None:
    location = create_location()

    location.move_to(
        x=60.0,
        y=70.0,
    )

    assert location.x == 60.0
    assert location.y == 70.0

    assert location.asset_code == (
        "ASSET-001"
    )
    assert location.name == (
        "Tablero General"
    )
    assert location.category == (
        "tableros"
    )


def test_should_allow_map_boundaries() -> None:
    location = create_location()

    location.move_to(
        x=0.0,
        y=100.0,
    )

    assert location.x == 0.0
    assert location.y == 100.0


def test_should_reject_coordinates_outside_map() -> None:
    invalid_coordinates = (
        (-0.1, 50.0),
        (100.1, 50.0),
        (50.0, -0.1),
        (50.0, 100.1),
    )

    for x, y in invalid_coordinates:
        location = create_location()

        with pytest.raises(
            ValueError,
            match="coordenadas",
        ):
            location.move_to(
                x=x,
                y=y,
            )

        assert location.x == 10.0
        assert location.y == 20.0
