from datetime import datetime

from app.domains.work_orders.activities.holds.entities import (
    ActivityHold,
)

from app.domains.work_orders.activities.holds.repositories import (
    InMemoryActivityHoldRepository,
)

from app.domains.work_orders.activities.holds.value_objects import (
    ActivityHoldReason,
)


def create_hold(
    code="HOLD-001",
    activity_code="ACT-001",
):

    return ActivityHold(
        code=code,
        activity_code=activity_code,
        reason=ActivityHoldReason.PENDING_MATERIAL,
        observations="Pendiente de material.",
        held_at=datetime(
            2026,
            9,
            14,
            10,
            0,
        ),
        held_by_person_code="TECH-001",
    )


def test_should_save_and_get_hold():

    repository = (
        InMemoryActivityHoldRepository()
    )

    hold = create_hold()

    repository.save(
        hold
    )

    result = repository.get_by_code(
        "HOLD-001"
    )

    assert result is hold


def test_should_return_none_for_unknown_hold():

    repository = (
        InMemoryActivityHoldRepository()
    )

    result = repository.get_by_code(
        "HOLD-NOT-FOUND"
    )

    assert result is None


def test_should_list_holds_by_activity():

    repository = (
        InMemoryActivityHoldRepository()
    )

    first_hold = create_hold(
        code="HOLD-001",
        activity_code="ACT-001",
    )

    first_hold.resume(
        resumed_at=datetime(
            2026,
            9,
            14,
            11,
            0,
        ),
        resumed_by_person_code="TECH-002",
    )

    repository.save(
        first_hold
    )

    repository.save(
        create_hold(
            code="HOLD-002",
            activity_code="ACT-001",
        )
    )

    repository.save(
        create_hold(
            code="HOLD-003",
            activity_code="ACT-002",
        )
    )

    result = repository.list_by_activity(
        "ACT-001"
    )

    assert len(result) == 2

    assert {
        hold.code
        for hold in result
    } == {
        "HOLD-001",
        "HOLD-002",
    }

def test_should_get_active_hold_by_activity():

    repository = (
        InMemoryActivityHoldRepository()
    )

    closed_hold = create_hold(
        code="HOLD-001",
        activity_code="ACT-001",
    )

    closed_hold.resume(
        resumed_at=datetime(
            2026,
            9,
            14,
            11,
            0,
        ),
        resumed_by_person_code="TECH-002",
    )

    repository.save(
        closed_hold
    )

    active_hold = create_hold(
        code="HOLD-002",
        activity_code="ACT-001",
    )

    repository.save(
        active_hold
    )

    result = repository.get_active_by_activity(
        "ACT-001"
    )

    assert result is active_hold


def test_should_return_none_when_activity_has_no_active_hold():

    repository = (
        InMemoryActivityHoldRepository()
    )

    hold = create_hold()

    hold.resume(
        resumed_at=datetime(
            2026,
            9,
            14,
            11,
            0,
        ),
        resumed_by_person_code="TECH-002",
    )

    repository.save(
        hold
    )

    result = repository.get_active_by_activity(
        "ACT-001"
    )

    assert result is None


def test_should_not_allow_two_active_holds_for_same_activity():

    repository = (
        InMemoryActivityHoldRepository()
    )

    first_hold = create_hold(
        code="HOLD-001",
        activity_code="ACT-001",
    )

    second_hold = create_hold(
        code="HOLD-002",
        activity_code="ACT-001",
    )

    repository.save(
        first_hold
    )

    try:
        repository.save(
            second_hold
        )

        assert False, (
            "repository should reject "
            "multiple active holds "
            "for same activity"
        )

    except ValueError as error:

        assert str(error) == (
            "activity already has active hold"
        )
