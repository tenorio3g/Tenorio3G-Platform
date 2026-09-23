from app.domains.inventory.entities import (
    InventoryStockPolicy,
)

from app.domains.inventory.repositories import (
    InMemoryInventoryStockPolicyRepository,
)


def create_policy(
    spare_part_code="BRG-6206",
    warehouse_code="WH-001",
    minimum_stock=4,
    maximum_stock=20,
    reorder_point=8,
):
    return InventoryStockPolicy(
        spare_part_code=spare_part_code,
        warehouse_code=warehouse_code,
        minimum_stock=minimum_stock,
        maximum_stock=maximum_stock,
        reorder_point=reorder_point,
    )


def test_should_save_and_get_policy():

    repository = (
        InMemoryInventoryStockPolicyRepository()
    )

    policy = create_policy()

    repository.save(policy)

    result = repository.get(
        "BRG-6206",
        "WH-001",
    )

    assert result is policy


def test_should_normalize_codes_when_getting():

    repository = (
        InMemoryInventoryStockPolicyRepository()
    )

    policy = create_policy()

    repository.save(policy)

    result = repository.get(
        " brg-6206 ",
        " wh-001 ",
    )

    assert result is policy


def test_should_return_none_when_policy_does_not_exist():

    repository = (
        InMemoryInventoryStockPolicyRepository()
    )

    result = repository.get(
        "BRG-6206",
        "WH-001",
    )

    assert result is None


def test_should_replace_same_composite_key():

    repository = (
        InMemoryInventoryStockPolicyRepository()
    )

    first = create_policy(
        minimum_stock=4,
        reorder_point=8,
    )

    second = create_policy(
        minimum_stock=6,
        reorder_point=10,
    )

    repository.save(first)
    repository.save(second)

    result = repository.get(
        "BRG-6206",
        "WH-001",
    )

    assert result is second
    assert result.minimum_stock == 6
    assert result.reorder_point == 10


def test_same_spare_part_can_have_policy_per_warehouse():

    repository = (
        InMemoryInventoryStockPolicyRepository()
    )

    warehouse_one = create_policy(
        warehouse_code="WH-001",
        minimum_stock=4,
    )

    warehouse_two = create_policy(
        warehouse_code="WH-002",
        minimum_stock=10,
    )

    repository.save(warehouse_one)
    repository.save(warehouse_two)

    assert repository.get(
        "BRG-6206",
        "WH-001",
    ) is warehouse_one

    assert repository.get(
        "BRG-6206",
        "WH-002",
    ) is warehouse_two


def test_should_list_policies_by_spare_part():

    repository = (
        InMemoryInventoryStockPolicyRepository()
    )

    first = create_policy(
        warehouse_code="WH-001",
    )

    second = create_policy(
        warehouse_code="WH-002",
    )

    unrelated = create_policy(
        spare_part_code="BRG-6207",
        warehouse_code="WH-001",
    )

    repository.save(first)
    repository.save(second)
    repository.save(unrelated)

    result = repository.list_by_spare_part(
        " brg-6206 ",
    )

    assert len(result) == 2
    assert first in result
    assert second in result
    assert unrelated not in result


def test_should_list_policies_by_warehouse():

    repository = (
        InMemoryInventoryStockPolicyRepository()
    )

    first = create_policy(
        spare_part_code="BRG-6206",
        warehouse_code="WH-001",
    )

    second = create_policy(
        spare_part_code="BRG-6207",
        warehouse_code="WH-001",
    )

    unrelated = create_policy(
        spare_part_code="BRG-6208",
        warehouse_code="WH-002",
    )

    repository.save(first)
    repository.save(second)
    repository.save(unrelated)

    result = repository.list_by_warehouse(
        " wh-001 ",
    )

    assert len(result) == 2
    assert first in result
    assert second in result
    assert unrelated not in result
