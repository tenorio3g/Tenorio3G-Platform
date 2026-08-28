from datetime import datetime

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from app.domains.work_orders.work_sessions.repositories import (
    InMemoryWorkSessionRepository,
)

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)


def create_session(
    *,
    code="WS-001",
    work_order_code="WO-001",
    activity_code="ACT-001",
    person_code="TECH-001",
    started_at=None,
    ended_at=None,
):

    return WorkSession(
        code=code,
        work_order_code=work_order_code,
        activity_code=activity_code,
        person_code=person_code,
        started_at=(
            started_at
            or datetime(
                2026,
                8,
                26,
                7,
                0,
            )
        ),
        ended_at=ended_at,
        source=WorkSessionSource.AUTOMATIC,
        created_at=datetime(
            2026,
            8,
            26,
            7,
            0,
        ),
        created_by_person_code=person_code,
    )


def test_should_save_and_get_work_session():

    repository = (
        InMemoryWorkSessionRepository()
    )

    session = create_session()

    repository.save(
        session
    )

    result = repository.get_by_code(
        "ws-001"
    )

    assert result is session


def test_should_list_sessions_by_activity():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_session(
            code="WS-001",
            activity_code="ACT-001",
        )
    )

    repository.save(
        create_session(
            code="WS-002",
            activity_code="ACT-002",
        )
    )

    result = repository.list_by_activity(
        "act-001"
    )

    assert len(result) == 1
    assert result[0].code == "WS-001"


def test_should_list_sessions_by_work_order():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_session(
            code="WS-001",
            work_order_code="WO-001",
        )
    )

    repository.save(
        create_session(
            code="WS-002",
            work_order_code="WO-002",
        )
    )

    result = repository.list_by_work_order(
        "wo-001"
    )

    assert len(result) == 1
    assert result[0].code == "WS-001"


def test_should_list_sessions_by_person():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_session(
            code="WS-001",
            person_code="TECH-001",
        )
    )

    repository.save(
        create_session(
            code="WS-002",
            person_code="TECH-002",
        )
    )

    result = repository.list_by_person(
        "tech-001"
    )

    assert len(result) == 1
    assert result[0].code == "WS-001"


def test_should_get_active_session_by_person():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_session(
            code="WS-001",
            person_code="TECH-001",
            started_at=datetime(
                2026,
                8,
                26,
                7,
                0,
            ),
            ended_at=datetime(
                2026,
                8,
                26,
                8,
                0,
            ),
        )
    )

    repository.save(
        create_session(
            code="WS-002",
            person_code="TECH-001",
            started_at=datetime(
                2026,
                8,
                26,
                9,
                0,
            ),
        )
    )

    result = repository.get_active_by_person(
        "TECH-001"
    )

    assert result is not None
    assert result.code == "WS-002"


def test_should_return_none_when_person_has_no_active_session():

    repository = (
        InMemoryWorkSessionRepository()
    )

    repository.save(
        create_session(
            code="WS-001",
            ended_at=datetime(
                2026,
                8,
                26,
                8,
                0,
            ),
        )
    )

    result = repository.get_active_by_person(
        "TECH-001"
    )

    assert result is None


def test_should_update_existing_session():

    repository = (
        InMemoryWorkSessionRepository()
    )

    session = create_session()

    repository.save(
        session
    )

    session.end(
        datetime(
            2026,
            8,
            26,
            8,
            0,
        )
    )

    repository.save(
        session
    )

    result = repository.get_by_code(
        "WS-001"
    )

    assert result is not None
    assert result.is_active is False
    assert result.duration_minutes == 60