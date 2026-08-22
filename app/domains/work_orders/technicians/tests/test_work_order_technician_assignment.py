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
def test_should_be_active_by_default():

    assignment = WorkOrderTechnicianAssignment(
        work_order_code="WO-001",
        person_code="55464",
        assigned_at=datetime(
            2026,
            8,
            20,
            8,
            0,
        ),
    )

    assert assignment.is_active is True
    assert assignment.unassigned_at is None


def test_should_unassign_assignment():

    assignment = WorkOrderTechnicianAssignment(
        work_order_code="WO-001",
        person_code="55464",
        assigned_at=datetime(
            2026,
            8,
            20,
            8,
            0,
        ),
    )

    unassigned_at = datetime(
        2026,
        8,
        20,
        12,
        30,
    )

    assignment.unassign(
        unassigned_at
    )

    assert assignment.is_active is False

    assert (
        assignment.unassigned_at
        == unassigned_at
    )


def test_should_reject_unassign_before_assignment():

    assignment = WorkOrderTechnicianAssignment(
        work_order_code="WO-001",
        person_code="55464",
        assigned_at=datetime(
            2026,
            8,
            20,
            8,
            0,
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "unassigned_at cannot be before assigned_at"
        ),
    ):
        assignment.unassign(
            datetime(
                2026,
                8,
                20,
                7,
                59,
            )
        )


def test_should_reject_second_unassign():

    assignment = WorkOrderTechnicianAssignment(
        work_order_code="WO-001",
        person_code="55464",
        assigned_at=datetime(
            2026,
            8,
            20,
            8,
            0,
        ),
    )

    assignment.unassign(
        datetime(
            2026,
            8,
            20,
            12,
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "technician assignment is already inactive"
        ),
    ):
        assignment.unassign(
            datetime(
                2026,
                8,
                20,
                13,
                0,
            )
        )


def test_should_validate_unassigned_at_type():

    with pytest.raises(
        ValueError,
        match=(
            "unassigned_at must be a datetime or None"
        ),
    ):
        WorkOrderTechnicianAssignment(
            work_order_code="WO-001",
            person_code="55464",
            assigned_at=datetime(
                2026,
                8,
                20,
                8,
                0,
            ),
            unassigned_at="2026-08-20",
        )