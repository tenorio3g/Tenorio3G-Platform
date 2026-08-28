from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.work_orders.work_sessions.audit.entities import (
    WorkSessionAuditEntry,
)

from app.domains.work_orders.work_sessions.audit.repositories import (
    SQLiteWorkSessionAuditRepository,
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
        27,
        hour,
        minute,
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

    return SQLiteWorkSessionAuditRepository(
        session_factory
    )


def create_manual_created_entry(
    work_session_code="WS-001",
):

    return WorkSessionAuditEntry(
        work_session_code=work_session_code,
        event_type=(
            WorkSessionAuditEventType.MANUAL_CREATED
        ),
        reason="Manual capture",
        actor_person_code="SUP-001",
        occurred_at=dt(10),
    )


def create_corrected_entry(
    work_session_code="WS-001",
    occurred_at=None,
):

    if occurred_at is None:
        occurred_at = dt(12)

    return WorkSessionAuditEntry(
        work_session_code=work_session_code,
        event_type=(
            WorkSessionAuditEventType.CORRECTED
        ),
        reason="Wrong captured time",
        actor_person_code="SUP-001",
        occurred_at=occurred_at,
        previous_started_at=dt(7),
        previous_ended_at=dt(8),
        new_started_at=dt(7, 30),
        new_ended_at=dt(9),
    )


def test_should_save_and_list_manual_created_entry():

    repository = create_repository()

    repository.save(
        create_manual_created_entry()
    )

    result = repository.list_by_work_session(
        "WS-001"
    )

    assert len(result) == 1

    entry = result[0]

    assert entry.work_session_code == "WS-001"

    assert (
        entry.event_type
        == WorkSessionAuditEventType.MANUAL_CREATED
    )

    assert entry.reason == "Manual capture"
    assert entry.actor_person_code == "SUP-001"
    assert entry.occurred_at == dt(10)

    assert entry.previous_started_at is None
    assert entry.previous_ended_at is None
    assert entry.new_started_at is None
    assert entry.new_ended_at is None


def test_should_save_and_list_corrected_entry():

    repository = create_repository()

    repository.save(
        create_corrected_entry()
    )

    result = repository.list_by_work_session(
        "WS-001"
    )

    assert len(result) == 1

    entry = result[0]

    assert (
        entry.event_type
        == WorkSessionAuditEventType.CORRECTED
    )

    assert (
        entry.previous_started_at
        == dt(7)
    )

    assert (
        entry.previous_ended_at
        == dt(8)
    )

    assert (
        entry.new_started_at
        == dt(7, 30)
    )

    assert (
        entry.new_ended_at
        == dt(9)
    )


def test_should_list_only_entries_for_requested_work_session():

    repository = create_repository()

    repository.save(
        create_manual_created_entry(
            "WS-001"
        )
    )

    repository.save(
        create_manual_created_entry(
            "WS-002"
        )
    )

    result = repository.list_by_work_session(
        " ws-001 "
    )

    assert len(result) == 1

    assert (
        result[0].work_session_code
        == "WS-001"
    )


def test_should_preserve_multiple_audit_entries_for_same_session():

    repository = create_repository()

    repository.save(
        create_manual_created_entry()
    )

    repository.save(
        create_corrected_entry()
    )

    result = repository.list_by_work_session(
        "WS-001"
    )

    assert len(result) == 2

    assert [
        entry.event_type
        for entry in result
    ] == [
        WorkSessionAuditEventType.MANUAL_CREATED,
        WorkSessionAuditEventType.CORRECTED,
    ]


def test_should_return_entries_ordered_by_occurred_at():

    repository = create_repository()

    repository.save(
        create_corrected_entry(
            occurred_at=dt(14),
        )
    )

    repository.save(
        create_manual_created_entry()
    )

    repository.save(
        WorkSessionAuditEntry(
            work_session_code="WS-001",
            event_type=(
                WorkSessionAuditEventType.CORRECTED
            ),
            reason="Second correction",
            actor_person_code="SUP-001",
            occurred_at=dt(12),
            previous_started_at=dt(7),
            previous_ended_at=dt(8),
            new_started_at=dt(7, 15),
            new_ended_at=dt(8, 30),
        )
    )

    result = repository.list_by_work_session(
        "WS-001"
    )

    assert [
        entry.occurred_at
        for entry in result
    ] == [
        dt(10),
        dt(12),
        dt(14),
    ]


def test_should_return_empty_list_when_no_audit_entries_exist():

    repository = create_repository()

    result = repository.list_by_work_session(
        "WS-NOT-FOUND"
    )

    assert result == []
