from app.domains.inventory.entities import (
    InventoryLocation,
)
from app.domains.inventory.repositories import (
    InMemoryInventoryLocationRepository,
)


def create_location(
    code="LOC-001",
    warehouse_code="WH-001",
    name="Rack principal",
):
    return InventoryLocation(
        code=code,
        warehouse_code=warehouse_code,
        name=name,
        aisle="A",
        rack="R01",
        level="N01",
        bin="B01",
    )


def test_should_save_and_get_location():

    repository = (
        InMemoryInventoryLocationRepository()
    )

    location = create_location()

    repository.save(location)

    stored = repository.get_by_code("LOC-001")

    assert stored is location


def test_get_by_code_should_normalize_code():

    repository = (
        InMemoryInventoryLocationRepository()
    )

    repository.save(create_location())

    stored = repository.get_by_code(
        " loc-001 "
    )

    assert stored is not None
    assert stored.code == "LOC-001"


def test_get_unknown_location_should_return_none():

    repository = (
        InMemoryInventoryLocationRepository()
    )

    assert (
        repository.get_by_code("LOC-999")
        is None
    )


def test_save_should_replace_existing_location():

    repository = (
        InMemoryInventoryLocationRepository()
    )

    repository.save(
        create_location(
            name="Ubicación anterior",
        )
    )

    repository.save(
        create_location(
            name="Ubicación actualizada",
        )
    )

    stored = repository.get_by_code("LOC-001")

    assert stored is not None
    assert stored.name == "Ubicación actualizada"


def test_list_by_warehouse_should_filter_locations():

    repository = (
        InMemoryInventoryLocationRepository()
    )

    repository.save(
        create_location(
            code="LOC-001",
            warehouse_code="WH-001",
        )
    )

    repository.save(
        create_location(
            code="LOC-002",
            warehouse_code="WH-001",
        )
    )

    repository.save(
        create_location(
            code="LOC-003",
            warehouse_code="WH-002",
        )
    )

    locations = repository.list_by_warehouse(
        "WH-001"
    )

    assert len(locations) == 2

    assert {
        location.code
        for location in locations
    } == {
        "LOC-001",
        "LOC-002",
    }


def test_list_by_warehouse_should_normalize_code():

    repository = (
        InMemoryInventoryLocationRepository()
    )

    repository.save(
        create_location(
            warehouse_code="WH-001",
        )
    )

    locations = repository.list_by_warehouse(
        " wh-001 "
    )

    assert len(locations) == 1
    assert locations[0].code == "LOC-001"
