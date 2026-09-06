from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)
from app.domains.locations.repositories.in_memory_physical_location_repository import (
    InMemoryPhysicalLocationRepository,
)
from app.domains.locations.use_cases.find_all_physical_locations.query import (
    FindAllPhysicalLocationsQuery,
)
from app.domains.locations.use_cases.find_all_physical_locations.find_all_physical_locations import (
    FindAllPhysicalLocations,
)


def test_find_all_physical_locations() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    repository.save(
        PhysicalLocation(
            code="SUBESTACION-NORTE",
            name="Subestacion Norte",
            area="SERVICIOS",
        )
    )

    repository.save(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura MD1",
            area="MD1",
        )
    )

    use_case = FindAllPhysicalLocations(
        repository
    )

    result = use_case.execute(
        FindAllPhysicalLocationsQuery()
    )

    assert result.success is True

    assert [
        location.code
        for location in result.locations
    ] == [
        "MD1-PINTURA",
        "SUBESTACION-NORTE",
    ]


def test_find_all_physical_locations_returns_empty_list() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    use_case = FindAllPhysicalLocations(
        repository
    )

    result = use_case.execute(
        FindAllPhysicalLocationsQuery()
    )

    assert result.success is True
    assert result.locations == []


def test_find_all_physical_locations_includes_inactive_locations() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    repository.save(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura MD1",
            area="MD1",
            is_active=False,
        )
    )

    use_case = FindAllPhysicalLocations(
        repository
    )

    result = use_case.execute(
        FindAllPhysicalLocationsQuery()
    )

    assert len(result.locations) == 1
    assert result.locations[0].is_active is False
