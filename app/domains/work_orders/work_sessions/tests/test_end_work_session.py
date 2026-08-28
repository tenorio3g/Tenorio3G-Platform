from datetime import datetime

import pytest

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from app.domains.work_orders.work_sessions.repositories import (
    InMemoryWorkSessionRepository,
)

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)

from app.domains.work_orders.work_sessions.use_cases import (
    EndWorkSession,
    EndWorkSessionCommand,
)


STARTED_AT = datetime(
    2026,
    8,
    26,
    7,
    0,
)


def create_active_session(
    *,
    code: str = "WS-001",
) -> WorkSession:

    return WorkSession(
        code=code,
        work_order_code="WO-001",
        activity_code="ACT-001",
        person_code="TECH-001",
        started_at=STARTED_AT,
        source=WorkSessionSource.AUTOMATIC,
        created_at=STARTED_AT,
        created_by_person_code="TECH-001",
    )


def create_ended_session(
    *,
    code: str = "WS-001",
) -> WorkSession:

    return WorkSession(
        code=code,
        work_order_code="WO-001",
        activity_code="ACT-001",
        person_code="TECH-001",
        started_at=STARTED_AT,
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            0,
        ),
        source=WorkSessionSource.AUTOMATIC,
        created_at=STARTED_AT,
        created_by_person_code="TECH-001",
    )


def create_person_repository():

    repository = (
        InMemoryPersonRepository()
    )

    repository.save(
        Person(
            code="TECH-001",
            name="Technician",
        )
    )

    return repository


def test_should_end_active_work_session():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_active_session()
    )

    person_repository = (
        create_person_repository()
    )

    use_case = EndWorkSession(
        repository,
        person_repository,
    )

    command = EndWorkSessionCommand(
        code="WS-001",
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            30,
        ),
        actor_person_code="TECH-001",
    )

    result = use_case.execute(
        command
    )

    session = result.work_session

    assert session.is_active is False

    assert session.ended_at == datetime(
        2026,
        8,
        26,
        8,
        30,
    )

    assert session.duration_minutes == 90


def test_should_persist_ended_work_session():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_active_session()
    )

    person_repository = (
        create_person_repository()
    )

    use_case = EndWorkSession(
        repository,
        person_repository,
    )

    use_case.execute(
        EndWorkSessionCommand(
            code="WS-001",
            ended_at=datetime(
                2026,
                8,
                26,
                9,
                0,
            ),
            actor_person_code="TECH-001",
        )
    )

    stored_session = repository.get_by_code(
        "WS-001"
    )

    assert stored_session is not None
    assert stored_session.is_active is False
    assert stored_session.duration_minutes == 120


def test_should_normalize_work_session_code():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_active_session()
    )

    person_repository = (
        create_person_repository()
    )

    use_case = EndWorkSession(
        repository,
        person_repository,
    )

    result = use_case.execute(
        EndWorkSessionCommand(
            code="  ws-001  ",
            ended_at=datetime(
                2026,
                8,
                26,
                8,
                0,
            ),
            actor_person_code="TECH-001",
        )
    )

    assert result.work_session.code == "WS-001"


def test_should_reject_missing_work_session():

    repository = (
        InMemoryWorkSessionRepository()
    )

    person_repository = (
        create_person_repository()
    )

    use_case = EndWorkSession(
        repository,
        person_repository,
    )

    with pytest.raises(
        ValueError,
        match="work session not found",
    ):
        use_case.execute(
            EndWorkSessionCommand(
                code="WS-404",
                ended_at=datetime(
                    2026,
                    8,
                    26,
                    8,
                    0,
                ),
                actor_person_code="TECH-001",
            )
        )


def test_should_reject_already_ended_work_session():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_ended_session()
    )

    person_repository = (
        create_person_repository()
    )

    use_case = EndWorkSession(
        repository,
        person_repository,
    )

    with pytest.raises(
        ValueError,
        match="work session already ended",
    ):
        use_case.execute(
            EndWorkSessionCommand(
                code="WS-001",
                ended_at=datetime(
                    2026,
                    8,
                    26,
                    9,
                    0,
                ),
                actor_person_code="TECH-001",
            )
        )


def test_should_reject_end_before_start():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_active_session()
    )

    person_repository = (
        create_person_repository()
    )

    use_case = EndWorkSession(
        repository,
        person_repository,
    )

    with pytest.raises(
        ValueError,
        match="end cannot be before start",
    ):
        use_case.execute(
            EndWorkSessionCommand(
                code="WS-001",
                ended_at=datetime(
                    2026,
                    8,
                    26,
                    6,
                    59,
                ),
                actor_person_code="TECH-001",
            )
        )


def test_should_allow_zero_duration():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_active_session()
    )

    person_repository = (
        create_person_repository()
    )

    use_case = EndWorkSession(
        repository,
        person_repository,
    )

    result = use_case.execute(
        EndWorkSessionCommand(
            code="WS-001",
            ended_at=STARTED_AT,
            actor_person_code="TECH-001",
        )
    )

    assert result.work_session.is_active is False
    assert result.work_session.duration_minutes == 0


def test_should_reject_missing_actor():

    work_session_repository = (
        InMemoryWorkSessionRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    work_session_repository.save(
        create_active_session()
    )

    use_case = EndWorkSession(
        work_session_repository,
        person_repository,
    )

    with pytest.raises(
        ValueError,
        match="actor person not found",
    ):
        use_case.execute(
            EndWorkSessionCommand(
                code="WS-001",
                ended_at=datetime(
                    2026,
                    8,
                    26,
                    8,
                    30,
                ),
                actor_person_code="TECH-404",
            )
        )


def test_should_reject_inactive_actor():

    work_session_repository = (
        InMemoryWorkSessionRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    work_session_repository.save(
        create_active_session()
    )

    person_repository.save(
        Person(
            code="TECH-001",
            name="Technician",
            is_active=False,
        )
    )

    use_case = EndWorkSession(
        work_session_repository,
        person_repository,
    )

    with pytest.raises(
        ValueError,
        match="actor person is inactive",
    ):
        use_case.execute(
            EndWorkSessionCommand(
                code="WS-001",
                ended_at=datetime(
                    2026,
                    8,
                    26,
                    8,
                    30,
                ),
                actor_person_code="TECH-001",
            )
        )


def test_should_reject_actor_that_does_not_own_session():

    work_session_repository = (
        InMemoryWorkSessionRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    work_session_repository.save(
        create_active_session()
    )

    person_repository.save(
        Person(
            code="TECH-002",
            name="Other technician",
        )
    )

    use_case = EndWorkSession(
        work_session_repository,
        person_repository,
    )

    with pytest.raises(
        ValueError,
        match="actor does not own work session",
    ):
        use_case.execute(
            EndWorkSessionCommand(
                code="WS-001",
                ended_at=datetime(
                    2026,
                    8,
                    26,
                    8,
                    30,
                ),
                actor_person_code="TECH-002",
            )
        )



