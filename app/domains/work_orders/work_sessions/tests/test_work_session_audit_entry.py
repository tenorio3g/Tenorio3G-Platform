from datetime import datetime

import pytest

from app.domains.work_orders.work_sessions.audit.entities import (
    WorkSessionAuditEntry,
)

from app.domains.work_orders.work_sessions.audit.value_objects import (
    WorkSessionAuditEventType,
)


def dt(
    hour: int,
    minute: int = 0,
) -> datetime:

    return datetime(
        2026,
        8,
        26,
        hour,
        minute,
    )


def test_should_create_manual_created_audit_entry():

    entry = WorkSessionAuditEntry(
        work_session_code="WS-001",
        event_type=(
            WorkSessionAuditEventType.MANUAL_CREATED
        ),
        reason=(
            "Trabajo no registrado "
            "durante la intervención"
        ),
        actor_person_code="SUP-001",
        occurred_at=dt(14),
    )

    assert entry.work_session_code == "WS-001"

    assert (
        entry.event_type
        == WorkSessionAuditEventType.MANUAL_CREATED
    )

    assert (
        entry.reason
        == "Trabajo no registrado durante la intervención"
    )

    assert entry.actor_person_code == "SUP-001"
    assert entry.occurred_at == dt(14)

    assert entry.previous_started_at is None
    assert entry.previous_ended_at is None
    assert entry.new_started_at is None
    assert entry.new_ended_at is None


def test_should_create_corrected_audit_entry():

    entry = WorkSessionAuditEntry(
        work_session_code="WS-001",
        event_type=(
            WorkSessionAuditEventType.CORRECTED
        ),
        reason="Corrección de tiempo",
        actor_person_code="SUP-001",
        occurred_at=dt(14),
        previous_started_at=dt(9),
        previous_ended_at=dt(10, 15),
        new_started_at=dt(9),
        new_ended_at=dt(10),
    )

    assert entry.previous_started_at == dt(9)
    assert entry.previous_ended_at == dt(10, 15)
    assert entry.new_started_at == dt(9)
    assert entry.new_ended_at == dt(10)


def test_should_normalize_codes():

    entry = WorkSessionAuditEntry(
        work_session_code="  ws-001  ",
        event_type=(
            WorkSessionAuditEventType.MANUAL_CREATED
        ),
        reason="Registro manual",
        actor_person_code="  sup-001  ",
        occurred_at=dt(14),
    )

    assert entry.work_session_code == "WS-001"
    assert entry.actor_person_code == "SUP-001"


def test_should_trim_reason():

    entry = WorkSessionAuditEntry(
        work_session_code="WS-001",
        event_type=(
            WorkSessionAuditEventType.MANUAL_CREATED
        ),
        reason="   Registro manual   ",
        actor_person_code="SUP-001",
        occurred_at=dt(14),
    )

    assert entry.reason == "Registro manual"


def test_should_reject_empty_work_session_code():

    with pytest.raises(
        ValueError,
        match="work_session_code is required",
    ):
        WorkSessionAuditEntry(
            work_session_code="   ",
            event_type=(
                WorkSessionAuditEventType.MANUAL_CREATED
            ),
            reason="Registro manual",
            actor_person_code="SUP-001",
            occurred_at=dt(14),
        )


def test_should_reject_empty_actor_person_code():

    with pytest.raises(
        ValueError,
        match="actor_person_code is required",
    ):
        WorkSessionAuditEntry(
            work_session_code="WS-001",
            event_type=(
                WorkSessionAuditEventType.MANUAL_CREATED
            ),
            reason="Registro manual",
            actor_person_code="   ",
            occurred_at=dt(14),
        )


def test_should_reject_empty_reason():

    with pytest.raises(
        ValueError,
        match="reason is required",
    ):
        WorkSessionAuditEntry(
            work_session_code="WS-001",
            event_type=(
                WorkSessionAuditEventType.MANUAL_CREATED
            ),
            reason="   ",
            actor_person_code="SUP-001",
            occurred_at=dt(14),
        )


def test_should_reject_invalid_event_type():

    with pytest.raises(
        ValueError,
        match="invalid audit event type",
    ):
        WorkSessionAuditEntry(
            work_session_code="WS-001",
            event_type="MANUAL_CREATED",
            reason="Registro manual",
            actor_person_code="SUP-001",
            occurred_at=dt(14),
        )


def test_should_reject_invalid_occurred_at():

    with pytest.raises(
        ValueError,
        match="occurred_at must be datetime",
    ):
        WorkSessionAuditEntry(
            work_session_code="WS-001",
            event_type=(
                WorkSessionAuditEventType.MANUAL_CREATED
            ),
            reason="Registro manual",
            actor_person_code="SUP-001",
            occurred_at="2026-08-26 14:00",
        )


def test_should_require_correction_time_values():

    with pytest.raises(
        ValueError,
        match="correction time values are required",
    ):
        WorkSessionAuditEntry(
            work_session_code="WS-001",
            event_type=(
                WorkSessionAuditEventType.CORRECTED
            ),
            reason="Corrección",
            actor_person_code="SUP-001",
            occurred_at=dt(14),
        )


def test_should_reject_invalid_corrected_time_range():

    with pytest.raises(
        ValueError,
        match="new end cannot be before new start",
    ):
        WorkSessionAuditEntry(
            work_session_code="WS-001",
            event_type=(
                WorkSessionAuditEventType.CORRECTED
            ),
            reason="Corrección",
            actor_person_code="SUP-001",
            occurred_at=dt(14),
            previous_started_at=dt(9),
            previous_ended_at=dt(10),
            new_started_at=dt(11),
            new_ended_at=dt(10),
        )
