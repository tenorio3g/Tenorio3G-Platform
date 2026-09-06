from app.domains.locations.repositories.in_memory_physical_location_repository import (
    InMemoryPhysicalLocationRepository,
)
from app.domains.locations.use_cases.register_physical_location.command import (
    RegisterPhysicalLocationCommand,
)
from app.domains.locations.use_cases.register_physical_location.register_physical_location import (
    RegisterPhysicalLocation,
)


def create_use_case():
    repository = (
        InMemoryPhysicalLocationRepository()
    )

    use_case = RegisterPhysicalLocation(
        repository
    )

    return repository, use_case


def test_register_physical_location() -> None:

    repository, use_case = create_use_case()

    command = RegisterPhysicalLocationCommand(
        code="MD1-PINTURA",
        name="Pintura MD1",
        area="MD1",
    )

    result = use_case.execute(
        command
    )

    assert result.success is True
    assert result.location is not None

    saved_location = repository.find_by_code(
        "MD1-PINTURA"
    )

    assert saved_location is not None
    assert saved_location.name == "Pintura MD1"
    assert saved_location.area == "MD1"


def test_register_physical_location_rejects_duplicate_code() -> None:

    repository, use_case = create_use_case()

    command = RegisterPhysicalLocationCommand(
        code="MD1-PINTURA",
        name="Pintura MD1",
        area="MD1",
    )

    first_result = use_case.execute(
        command
    )

    second_result = use_case.execute(
        command
    )

    assert first_result.success is True
    assert second_result.success is False
    assert second_result.location is None

    locations = repository.find_all()

    assert len(locations) == 1


def test_register_physical_location_trims_values() -> None:

    repository, use_case = create_use_case()

    command = RegisterPhysicalLocationCommand(
        code="  MD1-PINTURA  ",
        name="  Pintura MD1  ",
        area="  MD1  ",
    )

    result = use_case.execute(
        command
    )

    assert result.success is True

    saved_location = repository.find_by_code(
        "MD1-PINTURA"
    )

    assert saved_location is not None
    assert saved_location.code == "MD1-PINTURA"
    assert saved_location.name == "Pintura MD1"
    assert saved_location.area == "MD1"
