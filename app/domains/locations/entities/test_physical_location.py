import pytest

from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)


def test_create_physical_location() -> None:

    location = PhysicalLocation(
        code="MD1-PINTURA",
        name="Pintura MD1",
        area="MD1",
    )

    assert location.code == "MD1-PINTURA"
    assert location.name == "Pintura MD1"
    assert location.area == "MD1"
    assert location.is_active is True


def test_physical_location_values_are_trimmed() -> None:

    location = PhysicalLocation(
        code="  MD1-PINTURA  ",
        name="  Pintura MD1  ",
        area="  MD1  ",
    )

    assert location.code == "MD1-PINTURA"
    assert location.name == "Pintura MD1"
    assert location.area == "MD1"


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("code", "   "),
        ("name", "   "),
        ("area", "   "),
    ],
)
def test_physical_location_requires_values(
    field_name: str,
    value: str,
) -> None:

    values = {
        "code": "MD1-PINTURA",
        "name": "Pintura MD1",
        "area": "MD1",
    }

    values[field_name] = value

    with pytest.raises(ValueError):
        PhysicalLocation(
            **values,
        )
