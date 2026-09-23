from app.domains.inventory.entities import (
    InventoryLocation,
    InventoryStock,
    InventoryStockPolicy,
)

from app.domains.inventory.queries import (
    GetWarehouseStock,
    GetWarehouseStockStatus,
)

from app.domains.inventory.repositories import (
    InMemoryInventoryLocationRepository,
    InMemoryInventoryStockPolicyRepository,
    InMemoryInventoryStockRepository,
)


def create_context():

    location_repository = (
        InMemoryInventoryLocationRepository()
    )

    stock_repository = (
        InMemoryInventoryStockRepository()
    )

    policy_repository = (
        InMemoryInventoryStockPolicyRepository()
    )

    warehouse_stock_query = GetWarehouseStock(
        location_repository=location_repository,
        stock_repository=stock_repository,
    )

    status_query = GetWarehouseStockStatus(
        warehouse_stock_query=warehouse_stock_query,
        policy_repository=policy_repository,
    )

    return (
        status_query,
        location_repository,
        stock_repository,
        policy_repository,
    )


def save_location(
    repository,
    code="LOC-001",
    warehouse_code="WH-001",
):

    repository.save(
        InventoryLocation(
            code=code,
            warehouse_code=warehouse_code,
            name=code,
        )
    )


def save_stock(
    repository,
    quantity,
    spare_part_code="BRG-6206",
    location_code="LOC-001",
):

    repository.save(
        InventoryStock(
            spare_part_code=spare_part_code,
            location_code=location_code,
            quantity=quantity,
        )
    )


def save_policy(
    repository,
    minimum_stock=4,
    maximum_stock=20,
    reorder_point=8,
    spare_part_code="BRG-6206",
    warehouse_code="WH-001",
):

    repository.save(
        InventoryStockPolicy(
            spare_part_code=spare_part_code,
            warehouse_code=warehouse_code,
            minimum_stock=minimum_stock,
            maximum_stock=maximum_stock,
            reorder_point=reorder_point,
        )
    )


def test_should_evaluate_stock_with_configured_policy():

    (
        query,
        locations,
        stocks,
        policies,
    ) = create_context()

    save_location(locations)
    save_stock(stocks, quantity=10)
    save_policy(policies)

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.spare_part_code == "BRG-6206"
    assert result.warehouse_code == "WH-001"
    assert result.total_quantity == 10

    assert result.policy_configured is True
    assert result.minimum_stock == 4
    assert result.maximum_stock == 20
    assert result.reorder_point == 8

    assert result.is_below_minimum is False
    assert result.needs_reorder is False


def test_should_detect_reorder_point():

    (
        query,
        locations,
        stocks,
        policies,
    ) = create_context()

    save_location(locations)
    save_stock(stocks, quantity=8)
    save_policy(policies)

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.is_below_minimum is False
    assert result.needs_reorder is True


def test_should_detect_below_minimum():

    (
        query,
        locations,
        stocks,
        policies,
    ) = create_context()

    save_location(locations)
    save_stock(stocks, quantity=3)
    save_policy(policies)

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.is_below_minimum is True
    assert result.needs_reorder is True


def test_should_evaluate_zero_stock():

    (
        query,
        locations,
        _,
        policies,
    ) = create_context()

    save_location(locations)
    save_policy(policies)

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.total_quantity == 0
    assert result.is_below_minimum is True
    assert result.needs_reorder is True


def test_should_explicitly_report_missing_policy():

    (
        query,
        locations,
        stocks,
        _,
    ) = create_context()

    save_location(locations)
    save_stock(stocks, quantity=10)

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.total_quantity == 10

    assert result.policy_configured is False
    assert result.minimum_stock is None
    assert result.maximum_stock is None
    assert result.reorder_point is None
    assert result.is_below_minimum is None
    assert result.needs_reorder is None


def test_should_preserve_location_breakdown():

    (
        query,
        locations,
        stocks,
        policies,
    ) = create_context()

    save_location(
        locations,
        code="LOC-001",
    )

    save_location(
        locations,
        code="LOC-002",
    )

    save_stock(
        stocks,
        quantity=3,
        location_code="LOC-001",
    )

    save_stock(
        stocks,
        quantity=5,
        location_code="LOC-002",
    )

    save_policy(policies)

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.total_quantity == 8

    assert {
        item.location_code: item.quantity
        for item in result.locations
    } == {
        "LOC-001": 3,
        "LOC-002": 5,
    }


def test_should_use_policy_from_requested_warehouse():

    (
        query,
        locations,
        stocks,
        policies,
    ) = create_context()

    save_location(
        locations,
        code="LOC-001",
        warehouse_code="WH-001",
    )

    save_stock(
        stocks,
        quantity=10,
        location_code="LOC-001",
    )

    save_policy(
        policies,
        warehouse_code="WH-001",
        reorder_point=8,
    )

    save_policy(
        policies,
        warehouse_code="WH-002",
        reorder_point=50,
    )

    result = query.execute(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    assert result.reorder_point == 8
    assert result.needs_reorder is False


def test_should_normalize_codes():

    (
        query,
        locations,
        stocks,
        policies,
    ) = create_context()

    save_location(locations)
    save_stock(stocks, quantity=10)
    save_policy(policies)

    result = query.execute(
        spare_part_code=" brg-6206 ",
        warehouse_code=" wh-001 ",
    )

    assert result.spare_part_code == "BRG-6206"
    assert result.warehouse_code == "WH-001"
    assert result.policy_configured is True
    assert result.total_quantity == 10
