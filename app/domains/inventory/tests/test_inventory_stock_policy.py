import pytest

from app.domains.inventory.entities import (
    InventoryStockPolicy,
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


def test_should_create_inventory_stock_policy():

    policy = create_policy()

    assert policy.spare_part_code == "BRG-6206"
    assert policy.warehouse_code == "WH-001"
    assert policy.minimum_stock == 4
    assert policy.maximum_stock == 20
    assert policy.reorder_point == 8


def test_should_normalize_codes():

    policy = create_policy(
        spare_part_code=" brg-6206 ",
        warehouse_code=" wh-001 ",
    )

    assert policy.spare_part_code == "BRG-6206"
    assert policy.warehouse_code == "WH-001"


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("spare_part_code", ""),
        ("spare_part_code", "   "),
        ("warehouse_code", ""),
        ("warehouse_code", "   "),
    ],
)
def test_should_reject_empty_codes(
    field_name,
    value,
):

    data = {
        "spare_part_code": "BRG-6206",
        "warehouse_code": "WH-001",
    }

    data[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} is required",
    ):
        InventoryStockPolicy(**data)


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("minimum_stock", -1),
        ("maximum_stock", -1),
        ("reorder_point", -1),
    ],
)
def test_should_reject_negative_values(
    field_name,
    value,
):

    data = {
        "spare_part_code": "BRG-6206",
        "warehouse_code": "WH-001",
        "minimum_stock": 4,
        "maximum_stock": 20,
        "reorder_point": 8,
    }

    data[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} cannot be negative",
    ):
        InventoryStockPolicy(**data)


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("minimum_stock", float("nan")),
        ("minimum_stock", float("inf")),
        ("maximum_stock", float("-inf")),
        ("reorder_point", float("nan")),
    ],
)
def test_should_reject_non_finite_values(
    field_name,
    value,
):

    data = {
        "spare_part_code": "BRG-6206",
        "warehouse_code": "WH-001",
        "minimum_stock": 4,
        "maximum_stock": 20,
        "reorder_point": 8,
    }

    data[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} must be finite",
    ):
        InventoryStockPolicy(**data)


def test_should_reject_maximum_below_minimum():

    with pytest.raises(
        ValueError,
        match=(
            "maximum_stock cannot be below "
            "minimum_stock"
        ),
    ):
        create_policy(
            minimum_stock=10,
            maximum_stock=9,
        )


def test_should_allow_maximum_equal_to_minimum():

    policy = create_policy(
        minimum_stock=10,
        maximum_stock=10,
    )

    assert policy.minimum_stock == 10
    assert policy.maximum_stock == 10


def test_should_allow_minimum_without_maximum():

    policy = create_policy(
        minimum_stock=4,
        maximum_stock=0,
    )

    assert policy.minimum_stock == 4
    assert policy.maximum_stock == 0


def test_should_detect_quantity_below_minimum():

    policy = create_policy(
        minimum_stock=4,
    )

    assert policy.is_below_minimum(
        total_quantity=3,
    ) is True


def test_should_not_be_below_exact_minimum():

    policy = create_policy(
        minimum_stock=4,
    )

    assert policy.is_below_minimum(
        total_quantity=4,
    ) is False


def test_should_require_reorder_below_point():

    policy = create_policy(
        reorder_point=8,
    )

    assert policy.needs_reorder(
        total_quantity=7,
    ) is True


def test_should_require_reorder_at_exact_point():

    policy = create_policy(
        reorder_point=8,
    )

    assert policy.needs_reorder(
        total_quantity=8,
    ) is True


def test_should_not_require_reorder_above_point():

    policy = create_policy(
        reorder_point=8,
    )

    assert policy.needs_reorder(
        total_quantity=9,
    ) is False


@pytest.mark.parametrize(
    "value",
    [
        -1,
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_policy_evaluation_should_reject_invalid_quantity(
    value,
):

    policy = create_policy()

    with pytest.raises(ValueError):
        policy.needs_reorder(
            total_quantity=value,
        )

    with pytest.raises(ValueError):
        policy.is_below_minimum(
            total_quantity=value,
        )
