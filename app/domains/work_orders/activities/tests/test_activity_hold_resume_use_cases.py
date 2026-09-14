from datetime import datetime

import pytest

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.holds.repositories import (
    InMemoryActivityHoldRepository,
)

from app.domains.work_orders.activities.holds.value_objects import (
    ActivityHoldReason,
)

from app.domains.work_orders.activities.repositories import (
    InMemoryWorkOrderActivityRepository,
)

from app.domains.work_orders.activities.use_cases import (
    HoldWorkOrderActivity,
    HoldWorkOrderActivityCommand,
    ResumeWorkOrderActivity,
    ResumeWorkOrderActivityCommand,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)


def create_activity():

    activity = WorkOrderActivity(
        code="ACT-001",
        work_order_code="WO-001",
        title="Reemplazar contactor",
        responsible_person_code="TECH-001",
        estimated_minutes=30,
    )

    activity.start(
        datetime(
            2026,
            9,
            14,
            10,
            0,
        )
    )

    return activity


def create_repositories():

    activity_repository = (
        InMemoryWorkOrderActivityRepository()
    )

    hold_repository = (
        InMemoryActivityHoldRepository()
    )

    return (
        activity_repository,
        hold_repository,
    )


def test_should_hold_activity_and_create_hold_record():

    (
        activity_repository,
        hold_repository,
    ) = create_repositories()

    activity_repository.save(
        create_activity()
    )

    use_case = HoldWorkOrderActivity(
        activity_repository,
        hold_repository,
    )

    result = use_case.execute(
        HoldWorkOrderActivityCommand(
            code="ACT-001",
            hold_code="HOLD-001",
            reason=ActivityHoldReason.PENDING_MATERIAL,
            observations="Pendiente llegada de material.",
            held_at=datetime(
                2026,
                9,
                14,
                11,
                0,
            ),
            held_by_person_code="TECH-001",
        )
    )

    assert (
        result.activity.status
        == ActivityStatus.ON_HOLD
    )

    assert result.hold.code == "HOLD-001"

    assert (
        result.hold.reason
        == ActivityHoldReason.PENDING_MATERIAL
    )

    persisted_hold = (
        hold_repository.get_active_by_activity(
            "ACT-001"
        )
    )

    assert persisted_hold is not None
    assert persisted_hold.code == "HOLD-001"
    assert persisted_hold.is_active is True


def test_should_reject_hold_unknown_activity():

    (
        activity_repository,
        hold_repository,
    ) = create_repositories()

    use_case = HoldWorkOrderActivity(
        activity_repository,
        hold_repository,
    )

    with pytest.raises(
        ValueError,
        match="activity not found",
    ):
        use_case.execute(
            HoldWorkOrderActivityCommand(
                code="ACT-NOT-FOUND",
                hold_code="HOLD-001",
                reason=ActivityHoldReason.PENDING_MATERIAL,
                observations="",
                held_at=datetime(
                    2026,
                    9,
                    14,
                    11,
                    0,
                ),
                held_by_person_code="TECH-001",
            )
        )


def test_should_reject_second_active_hold():

    (
        activity_repository,
        hold_repository,
    ) = create_repositories()

    activity = create_activity()

    activity_repository.save(
        activity
    )

    use_case = HoldWorkOrderActivity(
        activity_repository,
        hold_repository,
    )

    use_case.execute(
        HoldWorkOrderActivityCommand(
            code="ACT-001",
            hold_code="HOLD-001",
            reason=ActivityHoldReason.PENDING_MATERIAL,
            observations="Primera espera.",
            held_at=datetime(
                2026,
                9,
                14,
                11,
                0,
            ),
            held_by_person_code="TECH-001",
        )
    )

    with pytest.raises(
        ValueError,
    ):
        use_case.execute(
            HoldWorkOrderActivityCommand(
                code="ACT-001",
                hold_code="HOLD-002",
                reason=ActivityHoldReason.PENDING_PROVIDER,
                observations="Segunda espera.",
                held_at=datetime(
                    2026,
                    9,
                    14,
                    12,
                    0,
                ),
                held_by_person_code="TECH-001",
            )
        )


def test_should_resume_activity_and_close_active_hold():

    (
        activity_repository,
        hold_repository,
    ) = create_repositories()

    activity_repository.save(
        create_activity()
    )

    hold_use_case = HoldWorkOrderActivity(
        activity_repository,
        hold_repository,
    )

    hold_use_case.execute(
        HoldWorkOrderActivityCommand(
            code="ACT-001",
            hold_code="HOLD-001",
            reason=ActivityHoldReason.PENDING_MATERIAL,
            observations="Pendiente llegada de material.",
            held_at=datetime(
                2026,
                9,
                14,
                11,
                0,
            ),
            held_by_person_code="TECH-001",
        )
    )

    resume_use_case = ResumeWorkOrderActivity(
        activity_repository,
        hold_repository,
    )

    result = resume_use_case.execute(
        ResumeWorkOrderActivityCommand(
            code="ACT-001",
            resumed_at=datetime(
                2026,
                9,
                14,
                13,
                30,
            ),
            resumed_by_person_code="TECH-002",
        )
    )

    assert (
        result.activity.status
        == ActivityStatus.IN_PROGRESS
    )

    assert result.hold.is_active is False

    assert (
        result.hold.resumed_at
        == datetime(
            2026,
            9,
            14,
            13,
            30,
        )
    )

    assert (
        result.hold.resumed_by_person_code
        == "TECH-002"
    )

    assert (
        hold_repository.get_active_by_activity(
            "ACT-001"
        )
        is None
    )


def test_should_reject_resume_unknown_activity():

    (
        activity_repository,
        hold_repository,
    ) = create_repositories()

    use_case = ResumeWorkOrderActivity(
        activity_repository,
        hold_repository,
    )

    with pytest.raises(
        ValueError,
        match="activity not found",
    ):
        use_case.execute(
            ResumeWorkOrderActivityCommand(
                code="ACT-NOT-FOUND",
                resumed_at=datetime(
                    2026,
                    9,
                    14,
                    13,
                    30,
                ),
                resumed_by_person_code="TECH-001",
            )
        )


def test_should_reject_resume_without_active_hold():

    (
        activity_repository,
        hold_repository,
    ) = create_repositories()

    activity = create_activity()

    activity.hold()

    activity_repository.save(
        activity
    )

    use_case = ResumeWorkOrderActivity(
        activity_repository,
        hold_repository,
    )

    with pytest.raises(
        ValueError,
        match="active activity hold not found",
    ):
        use_case.execute(
            ResumeWorkOrderActivityCommand(
                code="ACT-001",
                resumed_at=datetime(
                    2026,
                    9,
                    14,
                    13,
                    30,
                ),
                resumed_by_person_code="TECH-001",
            )
        )
