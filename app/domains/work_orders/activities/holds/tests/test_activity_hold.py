from datetime import datetime

import pytest

from app.domains.work_orders.activities.holds.entities import (
    ActivityHold,
)

from app.domains.work_orders.activities.holds.value_objects import (
    ActivityHoldReason,
)


def create_hold():

    return ActivityHold(
        code="HOLD-001",
        activity_code="ACT-001",
        reason=ActivityHoldReason.PENDING_MATERIAL,
        observations="Pendiente llegada de material.",
        held_at=datetime(
            2026,
            9,
            14,
            10,
            0,
        ),
        held_by_person_code="TECH-001",
    )


def test_should_create_activity_hold():

    hold = create_hold()

    assert hold.code == "HOLD-001"
    assert hold.activity_code == "ACT-001"

    assert (
        hold.reason
        == ActivityHoldReason.PENDING_MATERIAL
    )

    assert (
        hold.observations
        == "Pendiente llegada de material."
    )

    assert hold.held_at == datetime(
        2026,
        9,
        14,
        10,
        0,
    )

    assert (
        hold.held_by_person_code
        == "TECH-001"
    )

    assert hold.resumed_at is None

    assert (
        hold.resumed_by_person_code
        is None
    )

    assert hold.is_active is True


def test_should_normalize_codes():

    hold = ActivityHold(
        code=" hold-001 ",
        activity_code=" act-001 ",
        reason=ActivityHoldReason.PENDING_MATERIAL,
        observations="",
        held_at=datetime(
            2026,
            9,
            14,
            10,
            0,
        ),
        held_by_person_code=" tech-001 ",
    )

    assert hold.code == "HOLD-001"
    assert hold.activity_code == "ACT-001"

    assert (
        hold.held_by_person_code
        == "TECH-001"
    )


def test_should_require_code():

    with pytest.raises(
        ValueError,
        match="code is required",
    ):
        ActivityHold(
            code="",
            activity_code="ACT-001",
            reason=ActivityHoldReason.PENDING_MATERIAL,
            observations="",
            held_at=datetime(
                2026,
                9,
                14,
                10,
                0,
            ),
            held_by_person_code="TECH-001",
        )


def test_should_require_activity_code():

    with pytest.raises(
        ValueError,
        match="activity_code is required",
    ):
        ActivityHold(
            code="HOLD-001",
            activity_code="",
            reason=ActivityHoldReason.PENDING_MATERIAL,
            observations="",
            held_at=datetime(
                2026,
                9,
                14,
                10,
                0,
            ),
            held_by_person_code="TECH-001",
        )


def test_should_require_valid_reason():

    with pytest.raises(
        ValueError,
        match="reason must be ActivityHoldReason",
    ):
        ActivityHold(
            code="HOLD-001",
            activity_code="ACT-001",
            reason="INVALID",
            observations="",
            held_at=datetime(
                2026,
                9,
                14,
                10,
                0,
            ),
            held_by_person_code="TECH-001",
        )


def test_should_require_held_at_datetime():

    with pytest.raises(
        ValueError,
        match="held_at must be datetime",
    ):
        ActivityHold(
            code="HOLD-001",
            activity_code="ACT-001",
            reason=ActivityHoldReason.PENDING_MATERIAL,
            observations="",
            held_at="2026-09-14",
            held_by_person_code="TECH-001",
        )


def test_should_require_held_by_person_code():

    with pytest.raises(
        ValueError,
        match="held_by_person_code is required",
    ):
        ActivityHold(
            code="HOLD-001",
            activity_code="ACT-001",
            reason=ActivityHoldReason.PENDING_MATERIAL,
            observations="",
            held_at=datetime(
                2026,
                9,
                14,
                10,
                0,
            ),
            held_by_person_code="",
        )


def test_should_resume_activity_hold():

    hold = create_hold()

    resumed_at = datetime(
        2026,
        9,
        14,
        12,
        30,
    )

    hold.resume(
        resumed_at=resumed_at,
        resumed_by_person_code="TECH-002",
    )

    assert hold.resumed_at == resumed_at

    assert (
        hold.resumed_by_person_code
        == "TECH-002"
    )

    assert hold.is_active is False


def test_should_not_resume_twice():

    hold = create_hold()

    hold.resume(
        resumed_at=datetime(
            2026,
            9,
            14,
            12,
            30,
        ),
        resumed_by_person_code="TECH-002",
    )

    with pytest.raises(
        ValueError,
        match="activity hold is already resumed",
    ):
        hold.resume(
            resumed_at=datetime(
                2026,
                9,
                14,
                13,
                0,
            ),
            resumed_by_person_code="TECH-003",
        )


def test_should_not_resume_before_hold():

    hold = create_hold()

    with pytest.raises(
        ValueError,
        match="resumed_at cannot be before held_at",
    ):
        hold.resume(
            resumed_at=datetime(
                2026,
                9,
                14,
                9,
                59,
            ),
            resumed_by_person_code="TECH-002",
        )


def test_should_require_resumed_by_person_code():

    hold = create_hold()

    with pytest.raises(
        ValueError,
        match="resumed_by_person_code is required",
    ):
        hold.resume(
            resumed_at=datetime(
                2026,
                9,
                14,
                12,
                30,
            ),
            resumed_by_person_code="",
        )


def test_should_require_resumed_at_datetime():

    hold = create_hold()

    with pytest.raises(
        ValueError,
        match="resumed_at must be datetime",
    ):
        hold.resume(
            resumed_at="2026-09-14",
            resumed_by_person_code="TECH-002",
        )
