from datetime import datetime

import pytest

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.work_orders.work_sessions.audit.repositories import (
    InMemoryWorkSessionAuditRepository,
)

from app.domains.work_orders.work_sessions.audit.value_objects import (
    WorkSessionAuditEventType,
)

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from app.domains.work_orders.work_sessions.repositories import (
    InMemoryWorkSessionRepository,
)

from app.domains.work_orders.work_sessions.use_cases import (
    CorrectManualWorkSession,
    CorrectManualWorkSessionCommand,
)

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
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


def create_manual_session(
    *,
    code: str = "WS-001",
    person_code: str = "TECH-001",
    started_at: datetime | None = None,
    ended_at: datetime | None = None,
) -> WorkSession:

    return WorkSession(
        code=code,
        work_order_code="WO-001",
        activity_code="ACT-001",
        person_code=person_code,
        started_at=started_at or dt(7),
        ended_at=ended_at or dt(8),
        source=WorkSessionSource.MANUAL,
        created_at=dt(8),
        created_by_person_code="SUP-001",
    )


def create_automatic_session(
    *,
    code: str = "WS-001",
    person_code: str = "TECH-001",
) -> WorkSession:

    return WorkSession(
        code=code,
        work_order_code="WO-001",
        activity_code="ACT-001",
        person_code=person_code,
        started_at=dt(7),
        ended_at=dt(8),
        source=WorkSessionSource.AUTOMATIC,
        created_at=dt(7),
        created_by_person_code="TECH-001",
    )


def create_use_case(
    *,
    session: WorkSession | None = None,
    actor: Person | None = None,
):

    work_session_repository = (
        InMemoryWorkSessionRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    audit_repository = (
        InMemoryWorkSessionAuditRepository()
    )

    if session is not None:
        work_session_repository.save(
            session
        )

    if actor is not None:
        person_repository.save(
            actor
        )

    use_case = CorrectManualWorkSession(
        work_session_repository=(
            work_session_repository
        ),
        person_repository=(
            person_repository
        ),
        audit_repository=(
            audit_repository
        ),
    )

    return (
        use_case,
        work_session_repository,
        person_repository,
        audit_repository,
    )


def valid_command(
    *,
    code: str = "WS-001",
    started_at: datetime | None = None,
    ended_at: datetime | None = None,
    corrected_at: datetime | None = None,
    corrected_by_person_code: str = "SUP-001",
    reason: str = "Correction of captured time",
) -> CorrectManualWorkSessionCommand:

    return CorrectManualWorkSessionCommand(
        code=code,
        started_at=started_at or dt(7, 30),
        ended_at=ended_at or dt(9),
        corrected_at=corrected_at or dt(12),
        corrected_by_person_code=(
            corrected_by_person_code
        ),
        reason=reason,
    )


def test_should_correct_manual_work_session():

    actor = Person(
        code="SUP-001",
        name="Supervisor One",
    )

    use_case, _, _, _ = create_use_case(
        session=create_manual_session(),
        actor=actor,
    )

    result = use_case.execute(
        valid_command()
    )

    session = result.work_session

    assert session.started_at == dt(7, 30)
    assert session.ended_at == dt(9)
    assert session.duration_minutes == 90


def test_should_persist_corrected_manual_work_session():

    actor = Person(
        code="SUP-001",
        name="Supervisor One",
    )

    (
        use_case,
        work_session_repository,
        _,
        _,
    ) = create_use_case(
        session=create_manual_session(),
        actor=actor,
    )

    use_case.execute(
        valid_command()
    )

    stored_session = (
        work_session_repository.get_by_code(
            "WS-001"
        )
    )

    assert stored_session is not None
    assert stored_session.started_at == dt(7, 30)
    assert stored_session.ended_at == dt(9)


def test_should_reject_missing_work_session():

    actor = Person(
        code="SUP-001",
        name="Supervisor One",
    )

    use_case, _, _, _ = create_use_case(
        actor=actor,
    )

    with pytest.raises(
        ValueError,
        match="work session not found",
    ):
        use_case.execute(
            valid_command(
                code="WS-404",
            )
        )


def test_should_reject_automatic_work_session():

    actor = Person(
        code="SUP-001",
        name="Supervisor One",
    )

    use_case, _, _, _ = create_use_case(
        session=create_automatic_session(),
        actor=actor,
    )

    with pytest.raises(
        ValueError,
        match=(
            "only manual work sessions "
            "can be corrected"
        ),
    ):
        use_case.execute(
            valid_command()
        )


def test_should_reject_missing_correction_actor():

    use_case, _, _, _ = create_use_case(
        session=create_manual_session(),
    )

    with pytest.raises(
        ValueError,
        match="correction actor not found",
    ):
        use_case.execute(
            valid_command(
                corrected_by_person_code=(
                    "SUP-404"
                ),
            )
        )


def test_should_reject_inactive_correction_actor():

    actor = Person(
        code="SUP-001",
        name="Supervisor One",
        is_active=False,
    )

    use_case, _, _, _ = create_use_case(
        session=create_manual_session(),
        actor=actor,
    )

    with pytest.raises(
        ValueError,
        match="correction actor is inactive",
    ):
        use_case.execute(
            valid_command()
        )


def test_should_reject_empty_correction_reason():

    actor = Person(
        code="SUP-001",
        name="Supervisor One",
    )

    use_case, _, _, _ = create_use_case(
        session=create_manual_session(),
        actor=actor,
    )

    with pytest.raises(
        ValueError,
        match="reason is required",
    ):
        use_case.execute(
            valid_command(
                reason="   ",
            )
        )


def test_should_ignore_same_session_when_checking_overlap():

    actor = Person(
        code="SUP-001",
        name="Supervisor One",
    )

    use_case, _, _, _ = create_use_case(
        session=create_manual_session(
            started_at=dt(7),
            ended_at=dt(8),
        ),
        actor=actor,
    )

    result = use_case.execute(
        valid_command(
            started_at=dt(7, 30),
            ended_at=dt(8, 30),
        )
    )

    assert result.work_session.started_at == dt(
        7,
        30,
    )

    assert result.work_session.ended_at == dt(
        8,
        30,
    )


def test_should_reject_overlap_with_other_work_session():

    actor = Person(
        code="SUP-001",
        name="Supervisor One",
    )

    (
        use_case,
        work_session_repository,
        _,
        _,
    ) = create_use_case(
        session=create_manual_session(
            code="WS-001",
            started_at=dt(7),
            ended_at=dt(8),
        ),
        actor=actor,
    )

    work_session_repository.save(
        create_manual_session(
            code="WS-002",
            started_at=dt(9),
            ended_at=dt(10),
        )
    )

    with pytest.raises(
        ValueError,
        match="work session overlaps existing session",
    ):
        use_case.execute(
            valid_command(
                started_at=dt(8, 30),
                ended_at=dt(9, 30),
            )
        )


def test_should_create_corrected_audit_entry():

    actor = Person(
        code="SUP-001",
        name="Supervisor One",
    )

    (
        use_case,
        _,
        _,
        audit_repository,
    ) = create_use_case(
        session=create_manual_session(
            started_at=dt(7),
            ended_at=dt(8),
        ),
        actor=actor,
    )

    use_case.execute(
        valid_command(
            started_at=dt(7, 30),
            ended_at=dt(9),
            corrected_at=dt(12),
            reason="  Wrong captured time  ",
        )
    )

    entries = (
        audit_repository.list_by_work_session(
            "WS-001"
        )
    )

    assert len(entries) == 1

    entry = entries[0]

    assert (
        entry.event_type
        == WorkSessionAuditEventType.CORRECTED
    )

    assert entry.work_session_code == "WS-001"

    assert entry.actor_person_code == "SUP-001"

    assert entry.occurred_at == dt(12)

    assert entry.reason == "Wrong captured time"

    assert entry.previous_started_at == dt(7)
    assert entry.previous_ended_at == dt(8)

    assert entry.new_started_at == dt(7, 30)
    assert entry.new_ended_at == dt(9)
