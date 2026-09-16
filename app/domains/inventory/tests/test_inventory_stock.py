import pytest

from app.domains.inventory.entities.inventory_stock import (
    InventoryStock,
)


def create_stock(
    quantity=10,
    minimum_stock=4,
    maximum_stock=20,
    reorder_point=8,
):

    return InventoryStock(
        spare_part_code="BRG-6206",
        location_code="LOC-001",
        quantity=quantity,
        minimum_stock=minimum_stock,
        maximum_stock=maximum_stock,
        reorder_point=reorder_point,
    )


def test_should_create_inventory_stock():

    stock = create_stock()

    assert stock.spare_part_code == "BRG-6206"
    assert stock.location_code == "LOC-001"
    assert stock.quantity == 10
    assert stock.minimum_stock == 4
    assert stock.maximum_stock == 20
    assert stock.reorder_point == 8


def test_should_normalize_codes():

    stock = InventoryStock(
        spare_part_code=" brg-6206 ",
        location_code=" loc-001 ",
        quantity=10,
    )

    assert stock.spare_part_code == "BRG-6206"
    assert stock.location_code == "LOC-001"


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("spare_part_code", ""),
        ("spare_part_code", "   "),
        ("location_code", ""),
        ("location_code", "   "),
    ],
)
def test_should_reject_empty_required_codes(
    field_name,
    value,
):

    data = {
        "spare_part_code": "BRG-6206",
        "location_code": "LOC-001",
        "quantity": 10,
    }

    data[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} is required",
    ):
        InventoryStock(**data)


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("quantity", -1),
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
        "location_code": "LOC-001",
        "quantity": 10,
        "minimum_stock": 4,
        "maximum_stock": 20,
        "reorder_point": 8,
    }

    data[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} cannot be negative",
    ):
        InventoryStock(**data)


def test_should_reject_maximum_below_minimum():

    with pytest.raises(
        ValueError,
        match="maximum_stock cannot be below minimum_stock",
    ):
        create_stock(
            minimum_stock=10,
            maximum_stock=5,
        )


def test_should_allow_zero_stock():

    stock = create_stock(
        quantity=0,
    )

    assert stock.quantity == 0
    assert stock.is_out_of_stock is True


def test_should_detect_below_minimum():

    stock = create_stock(
        quantity=3,
    )

    assert stock.is_below_minimum is True
    assert stock.needs_reorder is True


def test_should_detect_reorder_point():

    stock = create_stock(
        quantity=8,
    )

    assert stock.needs_reorder is True
    assert stock.is_below_minimum is False


def test_should_not_require_reorder_above_point():

    stock = create_stock(
        quantity=9,
    )

    assert stock.needs_reorder is False


def test_should_not_be_out_of_stock_when_quantity_exists():

    stock = create_stock(
        quantity=1,
    )

    assert stock.is_out_of_stock is False


def test_should_allow_minimum_without_maximum_configured():

    stock = InventoryStock(
        spare_part_code="BRG-6206",
        location_code="LOC-001",
        quantity=10,
        minimum_stock=4,
        maximum_stock=0,
    )

    assert stock.minimum_stock == 4
    assert stock.maximum_stock == 0


def test_should_allow_maximum_equal_to_minimum():

    stock = create_stock(
        minimum_stock=10,
        maximum_stock=10,
    )

    assert stock.minimum_stock == 10
    assert stock.maximum_stock == 10


def test_should_not_be_below_minimum_at_exact_minimum():

    stock = create_stock(
        quantity=4,
    )

    assert stock.is_below_minimum is False


def test_should_require_reorder_at_exact_reorder_point():

    stock = create_stock(
        quantity=8,
    )

    assert stock.needs_reorder is True


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("quantity", float("nan")),
        ("quantity", float("inf")),
        ("quantity", float("-inf")),
        ("minimum_stock", float("nan")),
        ("maximum_stock", float("inf")),
        ("reorder_point", float("-inf")),
    ],
)
def test_should_reject_non_finite_values(
    field_name,
    value,
):

    data = {
        "spare_part_code": "BRG-6206",
        "location_code": "LOC-001",
        "quantity": 10,
        "minimum_stock": 4,
        "maximum_stock": 20,
        "reorder_point": 8,
    }

    data[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} must be finite",
    ):
        InventoryStock(**data)
