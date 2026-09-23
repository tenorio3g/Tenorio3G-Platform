import pytest

from app.domains.inventory.entities.inventory_stock import (
    InventoryStock,
)


def create_stock(
    quantity=10,
):

    return InventoryStock(
        spare_part_code="BRG-6206",
        location_code="LOC-001",
        quantity=quantity,
    )


def test_should_create_inventory_stock():

    stock = create_stock()

    assert stock.spare_part_code == "BRG-6206"
    assert stock.location_code == "LOC-001"
    assert stock.quantity == 10


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


def test_should_reject_negative_quantity():

    with pytest.raises(
        ValueError,
        match="quantity cannot be negative",
    ):
        create_stock(
            quantity=-1,
        )


def test_should_allow_zero_stock():

    stock = create_stock(
        quantity=0,
    )

    assert stock.quantity == 0
    assert stock.is_out_of_stock is True


def test_should_not_be_out_of_stock_when_quantity_exists():

    stock = create_stock(
        quantity=1,
    )

    assert stock.is_out_of_stock is False


@pytest.mark.parametrize(
    "value",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_should_reject_non_finite_quantity(
    value,
):

    with pytest.raises(
        ValueError,
        match="quantity must be finite",
    ):
        create_stock(
            quantity=value,
        )
