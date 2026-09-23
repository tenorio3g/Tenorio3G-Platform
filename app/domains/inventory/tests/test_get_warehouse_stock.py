import pytest

from app.domains.inventory.entities import (
    InventoryLocation,
    InventoryStock,
)

from app.domains.inventory.repositories import (
    InMemoryInventoryLocationRepository,
    InMemoryInventoryStockRepository,
)

from app.domains.inventory.queries import (
    GetWarehouseStock,
)


def create_location(
    code,
    warehouse_code,
):
    return InventoryLocation(
        code=code,
        warehouse_code=warehouse_code,
        name=code,
    )


def create_stock(
    spare_part_code,
    location_code,
    quantity,
):
    return InventoryStock(
        spare_part_code=spare_part_code,
        location_code=location_code,
        quantity=quantity,
    )


def create_query():
    location_repository = (
        InMemoryInventoryLocationRepository()
    )

    stock_repository = (
        InMemoryInventoryStockRepository()
    )

    query = GetWarehouseStock(
        location_repository=location_repository,
        stock_repository=stock_repository,
    )

    return (
        query,
        location_repository,
        stock_repository,
    )


def test_should_calculate_total_stock_in_warehouse():

    (
        query,
        location_repository,
        stock_repository,
    ) = create_query()

    location_repository.save(
        create_location(
            "LOC-001",
            "WH-001",
        )
    )

    location_repository.save(
        create_location(
            "LOC-002",
            "WH-001",
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-6206",
            "LOC-001",
            3,
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-6206",
            "LOC-002",
            5,
        )
    )

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.spare_part_code == "BRG-6206"
    assert result.warehouse_code == "WH-001"
    assert result.total_quantity == 8


def test_should_return_stock_breakdown_by_location():

    (
        query,
        location_repository,
        stock_repository,
    ) = create_query()

    location_repository.save(
        create_location(
            "LOC-001",
            "WH-001",
        )
    )

    location_repository.save(
        create_location(
            "LOC-002",
            "WH-001",
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-6206",
            "LOC-001",
            3,
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-6206",
            "LOC-002",
            5,
        )
    )

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert len(result.locations) == 2

    quantities = {
        item.location_code: item.quantity
        for item in result.locations
    }

    assert quantities == {
        "LOC-001": 3,
        "LOC-002": 5,
    }


def test_should_not_include_stock_from_other_warehouse():

    (
        query,
        location_repository,
        stock_repository,
    ) = create_query()

    location_repository.save(
        create_location(
            "LOC-001",
            "WH-001",
        )
    )

    location_repository.save(
        create_location(
            "LOC-002",
            "WH-001",
        )
    )

    location_repository.save(
        create_location(
            "LOC-003",
            "WH-002",
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-6206",
            "LOC-001",
            3,
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-6206",
            "LOC-002",
            5,
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-6206",
            "LOC-003",
            100,
        )
    )

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.total_quantity == 8

    assert {
        item.location_code
        for item in result.locations
    } == {
        "LOC-001",
        "LOC-002",
    }


def test_should_not_include_other_spare_parts():

    (
        query,
        location_repository,
        stock_repository,
    ) = create_query()

    location_repository.save(
        create_location(
            "LOC-001",
            "WH-001",
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-6206",
            "LOC-001",
            3,
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-9999",
            "LOC-001",
            100,
        )
    )

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.total_quantity == 3

    assert len(result.locations) == 1


def test_should_omit_locations_without_stock_record():

    (
        query,
        location_repository,
        stock_repository,
    ) = create_query()

    location_repository.save(
        create_location(
            "LOC-001",
            "WH-001",
        )
    )

    location_repository.save(
        create_location(
            "LOC-002",
            "WH-001",
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-6206",
            "LOC-001",
            3,
        )
    )

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.total_quantity == 3

    assert len(result.locations) == 1
    assert (
        result.locations[0].location_code
        == "LOC-001"
    )


def test_should_return_zero_when_spare_part_has_no_stock():

    (
        query,
        location_repository,
        stock_repository,
    ) = create_query()

    location_repository.save(
        create_location(
            "LOC-001",
            "WH-001",
        )
    )

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.total_quantity == 0
    assert result.locations == []


def test_should_normalize_query_codes():

    (
        query,
        location_repository,
        stock_repository,
    ) = create_query()

    location_repository.save(
        create_location(
            "LOC-001",
            "WH-001",
        )
    )

    stock_repository.save(
        create_stock(
            "BRG-6206",
            "LOC-001",
            7,
        )
    )

    result = query.execute(
        spare_part_code=" brg-6206 ",
        warehouse_code=" wh-001 ",
    )

    assert result.spare_part_code == "BRG-6206"
    assert result.warehouse_code == "WH-001"
    assert result.total_quantity == 7



@pytest.mark.parametrize(
    "spare_part_code",
    [
        "",
        "   ",
    ],
)
def test_should_reject_empty_spare_part_code(
    spare_part_code,
):

    (
        query,
        _,
        _,
    ) = create_query()

    with pytest.raises(
        ValueError,
        match="spare_part_code is required",
    ):
        query.execute(
            spare_part_code=spare_part_code,
            warehouse_code="WH-001",
        )


@pytest.mark.parametrize(
    "warehouse_code",
    [
        "",
        "   ",
    ],
)
def test_should_reject_empty_warehouse_code(
    warehouse_code,
):

    (
        query,
        _,
        _,
    ) = create_query()

    with pytest.raises(
        ValueError,
        match="warehouse_code is required",
    ):
        query.execute(
            spare_part_code="BRG-6206",
            warehouse_code=warehouse_code,
        )
