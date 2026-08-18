from datetime import datetime

import pytest

from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)

from app.domains.work_orders.tools.value_objects import (
    ToolUsageStatus,
)


def create_usage():

    return WorkOrderToolUsage(
        usage_id="TU-001",
        work_order_code="WO-001",
        tool_code="TL-001",
        tool_name="Multímetro",
        quantity=1,
        issued_at=datetime(
            2026,
            8,
            17,
            10,
            0,
        ),
        observations="Uso eléctrico.",
    )


def test_should_create_tool_usage():

    usage = create_usage()

    assert usage.work_order_code == "WO-001"
    assert usage.tool_code == "TL-001"
    assert usage.tool_name == "Multímetro"
    assert usage.quantity == 1

    assert (
        usage.status
        == ToolUsageStatus.ISSUED
    )

    assert usage.returned_at is None


@pytest.mark.parametrize(
    "field_name",
    [
        "work_order_code",
        "tool_code",
        "tool_name",
    ],
)
def test_should_require_fields(
    field_name,
):

    data = {
        "usage_id": "TU-001",   
        "work_order_code": "WO-001",
        "tool_code": "TL-001",
        "tool_name": "Multímetro",
        "quantity": 1,
        "issued_at": datetime(
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
        WorkOrderToolUsage(
            **data
        )


def test_should_require_positive_quantity():

    with pytest.raises(
        ValueError,
        match="quantity must be greater than zero",
    ):
        WorkOrderToolUsage(
            usage_id="TU-001",
            work_order_code="WO-001",
            tool_code="TL-001",
            tool_name="Multímetro",
            quantity=0,
            issued_at=datetime(
                2026,
                8,
                17,
            ),
        )


def test_should_return_tool():

    usage = create_usage()

    returned_at = datetime(
        2026,
        8,
        17,
        12,
        0,
    )

    usage.return_tool(
        returned_at
    )

    assert (
        usage.status
        == ToolUsageStatus.RETURNED
    )

    assert (
        usage.returned_at
        == returned_at
    )


def test_should_not_return_tool_twice():

    usage = create_usage()

    usage.return_tool(
        datetime(
            2026,
            8,
            17,
            12,
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "tool usage cannot be returned "
            "from current status"
        ),
    ):
        usage.return_tool(
            datetime(
                2026,
                8,
                17,
                13,
                0,
            )
        )


def test_should_not_return_before_issue():

    usage = create_usage()

    with pytest.raises(
        ValueError,
        match=(
            "returned_at cannot be before issued_at"
        ),
    ):
        usage.return_tool(
            datetime(
                2026,
                8,
                17,
                9,
                59,
            )
        )

def test_should_require_usage_id():

    with pytest.raises(
        ValueError,
        match="usage_id is required",
    ):
        WorkOrderToolUsage(
            usage_id="",
            work_order_code="WO-001",
            tool_code="TL-001",
            tool_name="Multímetro",
            quantity=1,
            issued_at=datetime(
                2026,
                8,
                17,
            ),
        )