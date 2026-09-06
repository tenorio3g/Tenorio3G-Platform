import pytest

from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)
from app.domains.locations.repositories.in_memory_physical_location_repository import (
    InMemoryPhysicalLocationRepository,
)


def create_location(
    code: str = "MD1-PINTURA",
    name: str = "Pintura MD1",
    area: str = "MD1",
) -> PhysicalLocation:

    return PhysicalLocation(
        code=code,
        name=name,
        area=area,
    )


def test_save_and_find_location_by_code() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    location = create_location()

    repository.save(location)

    saved_location = repository.find_by_code(
        "MD1-PINTURA"
    )

    assert saved_location is location


def test_find_by_code_returns_none_when_not_found() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    assert (
        repository.find_by_code(
            "UNKNOWN"
        )
        is None
    )


def test_find_all_returns_locations_ordered_by_code() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    repository.save(
        create_location(
            code="SUBESTACION-NORTE",
            name="Subestacion Norte",
            area="SERVICIOS",
        )
    )

    repository.save(
        create_location(
            code="MD1-PINTURA",
            name="Pintura MD1",
            area="MD1",
        )
    )

    locations = repository.find_all()

    assert [
        location.code
        for location in locations
    ] == [
        "MD1-PINTURA",
        "SUBESTACION-NORTE",
    ]


def test_save_updates_existing_location() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    repository.save(
        create_location()
    )

    repository.save(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura Principal MD1",
            area="MD1",
        )
    )

    locations = repository.find_all()

    assert len(locations) == 1

    saved_location = repository.find_by_code(
        "MD1-PINTURA"
    )

    assert saved_location is not None
    assert (
        saved_location.name
        == "Pintura Principal MD1"
    )


def test_update_existing_location() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    repository.save(
        create_location()
    )

    updated_location = PhysicalLocation(
        code="MD1-PINTURA",
        name="Pintura Actualizada",
        area="MD1",
        is_active=False,
    )

    repository.update(
        updated_location
    )

    saved_location = repository.find_by_code(
        "MD1-PINTURA"
    )

    assert saved_location is not None
    assert (
        saved_location.name
        == "Pintura Actualizada"
    )
    assert saved_location.is_active is False


def test_update_requires_existing_location() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    with pytest.raises(KeyError):
        repository.update(
            create_location()
        )
