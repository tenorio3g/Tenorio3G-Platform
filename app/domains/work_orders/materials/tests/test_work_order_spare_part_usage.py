from datetime import datetime

import pytest

from app.domains.work_orders.materials.entities import (
    WorkOrderSparePartUsage,
)


def test_should_create_spare_part_usage():

    usage = WorkOrderSparePartUsage(
        work_order_code=" wo-001 ",
        spare_part_code=" SP-001 ",
        quantity=2,
        unit_cost=15.5,
        used_at=datetime(
            2026,
            8,
            17,
            16,
            30,
        ),
        observations="Cambio preventivo.",
    )

    assert (
        usage.work_order_code
        == "WO-001"
    )

    assert (
        usage.spare_part_code
        == "SP-001"
    )

    assert usage.quantity == 2
    assert usage.unit_cost == 15.5
    assert usage.total_cost == 31.0

    assert (
        usage.observations
        == "Cambio preventivo."
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "work_order_code",
        "spare_part_code",
    ],
)
def test_should_require_fields(
    field_name,
):

    data = {
        "work_order_code": "WO-001",
        "spare_part_code": "SP-001",
        "quantity": 1,
        "used_at": datetime(
            2026,
            8,
            17,
        ),
    }

    data[field_name] = ""

    with pytest.raises(
        ValueError,
        match=f"{field_name} is required",
    ):
        WorkOrderSparePartUsage(
            **data
        )


def test_should_require_positive_quantity():

    with pytest.raises(
        ValueError,
        match="quantity must be greater than zero",
    ):
        WorkOrderSparePartUsage(
            work_order_code="WO-001",
            spare_part_code="SP-001",
            quantity=0,
            used_at=datetime(
                2026,
                8,
                17,
            ),
        )


def test_should_reject_invalid_quantity():

    with pytest.raises(
        ValueError,
        match="quantity must be a valid number",
    ):
        WorkOrderSparePartUsage(
            work_order_code="WO-001",
            spare_part_code="SP-001",
            quantity="abc",
            used_at=datetime(
                2026,
                8,
                17,
            ),
        )


def test_should_reject_negative_unit_cost():

    with pytest.raises(
        ValueError,
        match="unit_cost cannot be negative",
    ):
        WorkOrderSparePartUsage(
            work_order_code="WO-001",
            spare_part_code="SP-001",
            quantity=1,
            unit_cost=-1,
            used_at=datetime(
                2026,
                8,
                17,
            ),
        )


def test_should_require_used_at_datetime():

    with pytest.raises(
        ValueError,
        match="used_at must be a datetime",
    ):
        WorkOrderSparePartUsage(
            work_order_code="WO-001",
            spare_part_code="SP-001",
            quantity=1,
            used_at="2026-08-17",
        )