from datetime import datetime

import pytest

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)


def test_should_create_activity():

    activity = WorkOrderActivity(
        code="act-001",
        work_order_code="wo-001",
        title=" Inspección visual ",
        responsible_person_code="55464",
        description=" Revisar conexiones. ",
        estimated_minutes=30,
    )

    assert activity.code == "ACT-001"

    assert (
        activity.work_order_code
        == "WO-001"
    )

    assert (
        activity.title
        == "Inspección visual"
    )

    assert (
        activity.description
        == "Revisar conexiones."
    )

    assert (
        activity.responsible_person_code
        == "55464"
    )

    assert (
        activity.estimated_minutes
        == 30
    )

    assert (
        activity.status
        == ActivityStatus.PENDING
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "code",
        "work_order_code",
        "title",
        "responsible_person_code",
    ],
)
def test_should_require_fields(
    field_name,
):

    data = {
        "code": "ACT-001",
        "work_order_code": "WO-001",
        "title": "Inspección",
        "responsible_person_code": "55464",
    }

    data[field_name] = ""

    with pytest.raises(
        ValueError,
        match=f"{field_name} is required",
    ):
        WorkOrderActivity(
            **data
        )


def test_should_require_positive_estimated_minutes():

    with pytest.raises(
        ValueError,
        match=(
            "estimated_minutes must be greater than zero"
        ),
    ):
        WorkOrderActivity(
            code="ACT-001",
            work_order_code="WO-001",
            title="Inspección",
            responsible_person_code="55464",
            estimated_minutes=0,
        )


def test_should_require_valid_status():

    with pytest.raises(
        ValueError,
        match="status must be an ActivityStatus",
    ):
        WorkOrderActivity(
            code="ACT-001",
            work_order_code="WO-001",
            title="Inspección",
            responsible_person_code="55464",
            status="PENDING",
        )


def test_should_require_started_at_datetime():

    with pytest.raises(
        ValueError,
        match="started_at must be a datetime",
    ):
        WorkOrderActivity(
            code="ACT-001",
            work_order_code="WO-001",
            title="Inspección",
            responsible_person_code="55464",
            started_at="2026-08-16",
        )


def test_should_require_completed_at_datetime():

    with pytest.raises(
        ValueError,
        match="completed_at must be a datetime",
    ):
        WorkOrderActivity(
            code="ACT-001",
            work_order_code="WO-001",
            title="Inspección",
            responsible_person_code="55464",
            completed_at="2026-08-16",
        )

def create_activity():

    return WorkOrderActivity(
        code="ACT-001",
        work_order_code="WO-001",
        title="Inspección",
        responsible_person_code="55464",
        estimated_minutes=30,
    )


def test_should_start_activity():

    activity = create_activity()

    started_at = datetime(
        2026,
        8,
        16,
        10,
        0,
    )

    activity.start(
        started_at
    )

    assert (
        activity.status
        == ActivityStatus.IN_PROGRESS
    )

    assert (
        activity.started_at
        == started_at
    )


def test_should_not_start_activity_twice():

    activity = create_activity()

    activity.start(
        datetime(
            2026,
            8,
            16,
            10,
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "activity cannot be started "
            "from current status"
        ),
    ):
        activity.start(
            datetime(
                2026,
                8,
                16,
                10,
                5,
            )
        )


def test_should_not_complete_pending_activity():

    activity = create_activity()

    with pytest.raises(
        ValueError,
        match=(
            "activity cannot be completed "
            "from current status"
        ),
    ):
        activity.complete(
            datetime(
                2026,
                8,
                16,
                11,
                0,
            )
        )


def test_should_complete_activity():

    activity = create_activity()

    activity.start(
        datetime(
            2026,
            8,
            16,
            10,
            0,
        )
    )

    completed_at = datetime(
        2026,
        8,
        16,
        10,
        45,
    )

    activity.complete(
        completed_at
    )

    assert (
        activity.status
        == ActivityStatus.COMPLETED
    )

    assert (
        activity.completed_at
        == completed_at
    )

    assert (
        activity.actual_minutes
        == 45
    )


def test_should_not_complete_before_start():

    activity = create_activity()

    activity.start(
        datetime(
            2026,
            8,
            16,
            10,
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "completed_at cannot be "
            "before started_at"
        ),
    ):
        activity.complete(
            datetime(
                2026,
                8,
                16,
                9,
                59,
            )
        )


def test_actual_minutes_should_be_none_until_completed():

    activity = create_activity()

    assert (
        activity.actual_minutes
        is None
    )

    activity.start(
        datetime(
            2026,
            8,
            16,
            10,
            0,
        )
    )

    assert (
        activity.actual_minutes
        is None
    )