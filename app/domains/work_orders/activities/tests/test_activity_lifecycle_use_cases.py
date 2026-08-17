from datetime import datetime

import pytest

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.repositories import (
    InMemoryWorkOrderActivityRepository,
)

from app.domains.work_orders.activities.use_cases import (
    CompleteWorkOrderActivity,
    CompleteWorkOrderActivityCommand,
    StartWorkOrderActivity,
    StartWorkOrderActivityCommand,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)


def create_activity():

    return WorkOrderActivity(
        code="ACT-001",
        work_order_code="WO-001",
        title="Inspección visual",
        responsible_person_code="55464",
        estimated_minutes=30,
    )


def test_should_start_activity():

    repository = (
        InMemoryWorkOrderActivityRepository()
    )

    repository.save(
        create_activity()
    )

    use_case = StartWorkOrderActivity(
        repository
    )

    started_at = datetime(
        2026,
        8,
        16,
        18,
        30,
    )

    result = use_case.execute(
        StartWorkOrderActivityCommand(
            code="ACT-001",
            started_at=started_at,
        )
    )

    assert (
        result.activity.status
        == ActivityStatus.IN_PROGRESS
    )

    persisted = repository.get_by_code(
        "ACT-001"
    )

    assert persisted.started_at == started_at


def test_should_reject_start_unknown_activity():

    repository = (
        InMemoryWorkOrderActivityRepository()
    )

    use_case = StartWorkOrderActivity(
        repository
    )

    with pytest.raises(
        ValueError,
        match="activity not found",
    ):
        use_case.execute(
            StartWorkOrderActivityCommand(
                code="ACT-NOT-FOUND",
                started_at=datetime(
                    2026,
                    8,
                    16,
                    18,
                    30,
                ),
            )
        )


def test_should_complete_activity():

    repository = (
        InMemoryWorkOrderActivityRepository()
    )

    activity = create_activity()

    activity.start(
        datetime(
            2026,
            8,
            16,
            18,
            30,
        )
    )

    repository.save(
        activity
    )

    use_case = CompleteWorkOrderActivity(
        repository
    )

    completed_at = datetime(
        2026,
        8,
        16,
        19,
        15,
    )

    result = use_case.execute(
        CompleteWorkOrderActivityCommand(
            code="ACT-001",
            completed_at=completed_at,
        )
    )

    assert (
        result.activity.status
        == ActivityStatus.COMPLETED
    )

    assert (
        result.activity.actual_minutes
        == 45
    )

    persisted = repository.get_by_code(
        "ACT-001"
    )

    assert (
        persisted.completed_at
        == completed_at
    )


def test_should_reject_complete_unknown_activity():

    repository = (
        InMemoryWorkOrderActivityRepository()
    )

    use_case = CompleteWorkOrderActivity(
        repository
    )

    with pytest.raises(
        ValueError,
        match="activity not found",
    ):
        use_case.execute(
            CompleteWorkOrderActivityCommand(
                code="ACT-NOT-FOUND",
                completed_at=datetime(
                    2026,
                    8,
                    16,
                    19,
                    0,
                ),
            )
        )