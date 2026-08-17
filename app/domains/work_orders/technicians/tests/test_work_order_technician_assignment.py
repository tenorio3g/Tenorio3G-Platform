from datetime import datetime

import pytest

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)


def test_should_create_assignment():

    assignment = WorkOrderTechnicianAssignment(
        work_order_code=" wo-001 ",
        person_code=" 55464 ",
        assigned_at=datetime(
            2026,
            8,
            15,
            23,
            0,
        ),
    )

    assert (
        assignment.work_order_code
        == "WO-001"
    )

    assert (
        assignment.person_code
        == "55464"
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "work_order_code",
        "person_code",
    ],
)
def test_should_require_fields(
    field_name,
):

    data = {
        "work_order_code": "WO-001",
        "person_code": "55464",
        "assigned_at": datetime(
            2026,
            8,
            15,
        ),
    }

    data[field_name] = ""

    with pytest.raises(
        ValueError,
        match=f"{field_name} is required",
    ):
        WorkOrderTechnicianAssignment(
            **data
        )


def test_should_require_assigned_at_datetime():

    with pytest.raises(
        ValueError,
        match="assigned_at must be a datetime",
    ):
        WorkOrderTechnicianAssignment(
            work_order_code="WO-001",
            person_code="55464",
            assigned_at="2026-08-15",
        )