from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)
from app.domains.locations.repositories.in_memory_physical_location_repository import (
    InMemoryPhysicalLocationRepository,
)
from app.domains.locations.use_cases.find_physical_location_by_code.query import (
    FindPhysicalLocationByCodeQuery,
)
from app.domains.locations.use_cases.find_physical_location_by_code.find_physical_location_by_code import (
    FindPhysicalLocationByCode,
)


def test_find_physical_location_by_code() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    repository.save(
        PhysicalLocation(
            code="MD1-PINTURA",
            name="Pintura MD1",
            area="MD1",
        )
    )

    use_case = FindPhysicalLocationByCode(
        repository
    )

    result = use_case.execute(
        FindPhysicalLocationByCodeQuery(
            code="MD1-PINTURA",
        )
    )

    assert result.success is True
    assert result.location is not None
    assert result.location.code == "MD1-PINTURA"
    assert result.location.name == "Pintura MD1"


def test_find_physical_location_by_code_returns_failure_when_missing() -> None:

    repository = (
        InMemoryPhysicalLocationRepository()
    )

    use_case = FindPhysicalLocationByCode(
        repository
    )

    result = use_case.execute(
        FindPhysicalLocationByCodeQuery(
            code="UNKNOWN",
        )
    )

    assert result.success is False
    assert result.location is None


def test_find_physical_location_by_code_trims_code() -> None:

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

    use_case = FindPhysicalLocationByCode(
        repository
    )

    result = use_case.execute(
        FindPhysicalLocationByCodeQuery(
            code="  SUBESTACION-NORTE  ",
        )
    )

    assert result.success is True
    assert result.location is not None
    assert result.location.code == "SUBESTACION-NORTE"
