from datetime import datetime

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.work_orders.activities.holds.entities import (
    ActivityHold,
)

from app.domains.work_orders.activities.holds.repositories import (
    SQLiteActivityHoldRepository,
)

from app.domains.work_orders.activities.holds.value_objects import (
    ActivityHoldReason,
)


def create_repository():

    engine = create_engine(
        "sqlite:///:memory:"
    )

    Base.metadata.create_all(
        engine
    )

    session_factory = sessionmaker(
        bind=engine
    )

    return SQLiteActivityHoldRepository(
        session_factory
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

    repository = create_repository()

    repository.save(
        create_hold()
    )

    persisted = repository.get_by_code(
        "HOLD-001"
    )

    assert persisted is not None
    assert persisted.code == "HOLD-001"
    assert persisted.activity_code == "ACT-001"

    assert (
        persisted.reason
        == ActivityHoldReason.PENDING_MATERIAL
    )

    assert (
        persisted.observations
        == "Pendiente de material."
    )

    assert persisted.is_active is True


def test_should_list_holds_by_activity():

    repository = create_repository()

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
        " act-001 "
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

    repository = create_repository()

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

    assert result is not None
    assert result.code == "HOLD-002"
    assert result.is_active is True


def test_should_persist_resume_changes():

    repository = create_repository()

    hold = create_hold()

    repository.save(
        hold
    )

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

    repository.save(
        hold
    )

    persisted = repository.get_by_code(
        "HOLD-001"
    )

    assert persisted is not None

    assert (
        persisted.resumed_at
        == datetime(
            2026,
            9,
            14,
            12,
            30,
        )
    )

    assert (
        persisted.resumed_by_person_code
        == "TECH-002"
    )

    assert persisted.is_active is False


def test_should_not_allow_two_active_holds_for_same_activity():

    repository = create_repository()

    repository.save(
        create_hold(
            code="HOLD-001",
            activity_code="ACT-001",
        )
    )

    with pytest.raises(
        ValueError,
        match="activity already has active hold",
    ):
        repository.save(
            create_hold(
                code="HOLD-002",
                activity_code="ACT-001",
            )
        )
