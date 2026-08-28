from datetime import datetime

from app.domains.work_orders.work_sessions.audit.entities import (
    WorkSessionAuditEntry,
)

from app.domains.work_orders.work_sessions.audit.value_objects import (
    WorkSessionAuditEventType,
)

from app.domains.work_orders.work_sessions.audit.repositories import (
    InMemoryWorkSessionAuditRepository,
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


def create_entry(
    *,
    work_session_code: str = "WS-001",
    reason: str = "Registro manual",
    occurred_at: datetime | None = None,
) -> WorkSessionAuditEntry:

    return WorkSessionAuditEntry(
        work_session_code=work_session_code,
        event_type=(
            WorkSessionAuditEventType.MANUAL_CREATED
        ),
        reason=reason,
        actor_person_code="SUP-001",
        occurred_at=occurred_at or dt(14),
    )


def test_should_save_audit_entry():

    repository = (
        InMemoryWorkSessionAuditRepository()
    )

    entry = create_entry()

    repository.save(
        entry
    )

    entries = repository.list_by_work_session(
        "WS-001"
    )

    assert len(entries) == 1
    assert entries[0] is entry


def test_should_list_all_entries_for_work_session():

    repository = (
        InMemoryWorkSessionAuditRepository()
    )

    first = create_entry(
        reason="Registro inicial",
        occurred_at=dt(14),
    )

    second = WorkSessionAuditEntry(
        work_session_code="WS-001",
        event_type=(
            WorkSessionAuditEventType.CORRECTED
        ),
        reason="Corrección posterior",
        actor_person_code="SUP-001",
        occurred_at=dt(15),
        previous_started_at=dt(9),
        previous_ended_at=dt(10),
        new_started_at=dt(9),
        new_ended_at=dt(9, 45),
    )

    repository.save(first)
    repository.save(second)

    entries = repository.list_by_work_session(
        "WS-001"
    )

    assert len(entries) == 2

    assert entries[0] is first
    assert entries[1] is second


def test_should_not_return_entries_from_other_work_session():

    repository = (
        InMemoryWorkSessionAuditRepository()
    )

    repository.save(
        create_entry(
            work_session_code="WS-001"
        )
    )

    repository.save(
        create_entry(
            work_session_code="WS-002"
        )
    )

    entries = repository.list_by_work_session(
        "WS-001"
    )

    assert len(entries) == 1

    assert (
        entries[0].work_session_code
        == "WS-001"
    )


def test_should_normalize_work_session_code():

    repository = (
        InMemoryWorkSessionAuditRepository()
    )

    repository.save(
        create_entry(
            work_session_code="WS-001"
        )
    )

    entries = repository.list_by_work_session(
        "  ws-001  "
    )

    assert len(entries) == 1


def test_should_return_empty_list_when_no_entries_exist():

    repository = (
        InMemoryWorkSessionAuditRepository()
    )

    entries = repository.list_by_work_session(
        "WS-404"
    )

    assert entries == []


def test_should_preserve_multiple_audit_entries():

    repository = (
        InMemoryWorkSessionAuditRepository()
    )

    for minute in range(3):

        repository.save(
            create_entry(
                reason=f"Registro {minute}",
                occurred_at=datetime(
                    2026,
                    8,
                    26,
                    14,
                    minute,
                ),
            )
        )

    entries = repository.list_by_work_session(
        "WS-001"
    )

    assert len(entries) == 3

    assert [
        entry.reason
        for entry in entries
    ] == [
        "Registro 0",
        "Registro 1",
        "Registro 2",
    ]
