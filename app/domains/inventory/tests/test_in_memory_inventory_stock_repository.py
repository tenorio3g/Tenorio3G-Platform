from app.domains.inventory.entities import (
    InventoryStock,
)
from app.domains.inventory.repositories import (
    InMemoryInventoryStockRepository,
)


def create_stock(
    spare_part_code="BRG-6206",
    location_code="LOC-001",
    quantity=10,
):
    return InventoryStock(
        spare_part_code=spare_part_code,
        location_code=location_code,
        quantity=quantity,
    )


def test_should_save_and_get_stock():

    repository = InMemoryInventoryStockRepository()

    stock = create_stock()

    repository.save(stock)

    stored = repository.get(
        "BRG-6206",
        "LOC-001",
    )

    assert stored is stock


def test_get_should_normalize_codes():

    repository = InMemoryInventoryStockRepository()

    repository.save(
        create_stock()
    )

    stored = repository.get(
        " brg-6206 ",
        " loc-001 ",
    )

    assert stored is not None
    assert stored.spare_part_code == "BRG-6206"
    assert stored.location_code == "LOC-001"


def test_get_unknown_stock_should_return_none():

    repository = InMemoryInventoryStockRepository()

    stored = repository.get(
        "BRG-9999",
        "LOC-999",
    )

    assert stored is None


def test_same_spare_part_can_exist_in_multiple_locations():

    repository = InMemoryInventoryStockRepository()

    repository.save(
        create_stock(
            location_code="LOC-001",
            quantity=10,
        )
    )

    repository.save(
        create_stock(
            location_code="LOC-002",
            quantity=4,
        )
    )

    stock_1 = repository.get(
        "BRG-6206",
        "LOC-001",
    )

    stock_2 = repository.get(
        "BRG-6206",
        "LOC-002",
    )

    assert stock_1 is not None
    assert stock_2 is not None

    assert stock_1.quantity == 10
    assert stock_2.quantity == 4


def test_different_spare_parts_can_exist_in_same_location():

    repository = InMemoryInventoryStockRepository()

    repository.save(
        create_stock(
            spare_part_code="BRG-6206",
        )
    )

    repository.save(
        create_stock(
            spare_part_code="FUSE-001",
        )
    )

    stock_1 = repository.get(
        "BRG-6206",
        "LOC-001",
    )

    stock_2 = repository.get(
        "FUSE-001",
        "LOC-001",
    )

    assert stock_1 is not None
    assert stock_2 is not None


def test_save_should_replace_same_composite_key():

    repository = InMemoryInventoryStockRepository()

    repository.save(
        create_stock(
            quantity=10,
        )
    )

    repository.save(
        create_stock(
            quantity=7,
        )
    )

    stored = repository.get(
        "BRG-6206",
        "LOC-001",
    )

    assert stored is not None
    assert stored.quantity == 7


def test_list_by_spare_part_should_filter_stock():

    repository = InMemoryInventoryStockRepository()

    repository.save(
        create_stock(
            spare_part_code="BRG-6206",
            location_code="LOC-001",
        )
    )

    repository.save(
        create_stock(
            spare_part_code="BRG-6206",
            location_code="LOC-002",
        )
    )

    repository.save(
        create_stock(
            spare_part_code="FUSE-001",
            location_code="LOC-001",
        )
    )

    stocks = repository.list_by_spare_part(
        " brg-6206 "
    )

    assert len(stocks) == 2

    assert {
        stock.location_code
        for stock in stocks
    } == {
        "LOC-001",
        "LOC-002",
    }


def test_list_by_location_should_filter_stock():

    repository = InMemoryInventoryStockRepository()

    repository.save(
        create_stock(
            spare_part_code="BRG-6206",
            location_code="LOC-001",
        )
    )

    repository.save(
        create_stock(
            spare_part_code="FUSE-001",
            location_code="LOC-001",
        )
    )

    repository.save(
        create_stock(
            spare_part_code="BELT-A42",
            location_code="LOC-002",
        )
    )

    stocks = repository.list_by_location(
        " loc-001 "
    )

    assert len(stocks) == 2

    assert {
        stock.spare_part_code
        for stock in stocks
    } == {
        "BRG-6206",
        "FUSE-001",
    }
