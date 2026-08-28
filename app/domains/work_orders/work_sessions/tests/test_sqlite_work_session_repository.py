from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from app.domains.work_orders.work_sessions.repositories import (
    SQLiteWorkSessionRepository,
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

    return SQLiteWorkSessionRepository(
        session_factory
    )


def create_session(
    code="WS-001",
    work_order_code="WO-001",
    activity_code="ACT-001",
    person_code="TECH-001",
    started_at=None,
    ended_at=None,
    source=WorkSessionSource.MANUAL,
):

    if started_at is None:
        started_at = dt(7)

    if ended_at is None:
        ended_at = dt(8)

    return WorkSession(
        code=code,
        work_order_code=work_order_code,
        activity_code=activity_code,
        person_code=person_code,
        started_at=started_at,
        ended_at=ended_at,
        source=source,
        created_at=dt(8),
        created_by_person_code="SUP-001",
    )


def test_should_save_and_get_work_session():

    repository = create_repository()

    repository.save(
        create_session()
    )

    persisted = repository.get_by_code(
        "WS-001"
    )

    assert persisted is not None

    assert persisted.code == "WS-001"
    assert persisted.work_order_code == "WO-001"
    assert persisted.activity_code == "ACT-001"
    assert persisted.person_code == "TECH-001"

    assert persisted.started_at == dt(7)
    assert persisted.ended_at == dt(8)

    assert (
        persisted.source
        == WorkSessionSource.MANUAL
    )

    assert persisted.created_at == dt(8)

    assert (
        persisted.created_by_person_code
        == "SUP-001"
    )


def test_should_get_work_session_using_normalized_code():

    repository = create_repository()

    repository.save(
        create_session()
    )

    persisted = repository.get_by_code(
        " ws-001 "
    )

    assert persisted is not None
    assert persisted.code == "WS-001"


def test_should_update_existing_work_session():

    repository = create_repository()

    work_session = create_session()

    repository.save(
        work_session
    )

    work_session.correct(
        started_at=dt(7, 30),
        ended_at=dt(9),
    )

    repository.save(
        work_session
    )

    persisted = repository.get_by_code(
        "WS-001"
    )

    assert persisted is not None

    assert (
        persisted.started_at
        == dt(7, 30)
    )

    assert (
        persisted.ended_at
        == dt(9)
    )


def test_should_list_work_sessions_by_activity():

    repository = create_repository()

    repository.save(
        create_session(
            code="WS-001",
            activity_code="ACT-001",
        )
    )

    repository.save(
        create_session(
            code="WS-002",
            activity_code="ACT-001",
        )
    )

    repository.save(
        create_session(
            code="WS-003",
            activity_code="ACT-002",
        )
    )

    result = repository.list_by_activity(
        " act-001 "
    )

    assert {
        session.code
        for session in result
    } == {
        "WS-001",
        "WS-002",
    }


def test_should_list_work_sessions_by_work_order():

    repository = create_repository()

    repository.save(
        create_session(
            code="WS-001",
            work_order_code="WO-001",
        )
    )

    repository.save(
        create_session(
            code="WS-002",
            work_order_code="WO-001",
        )
    )

    repository.save(
        create_session(
            code="WS-003",
            work_order_code="WO-002",
        )
    )

    result = repository.list_by_work_order(
        " wo-001 "
    )

    assert {
        session.code
        for session in result
    } == {
        "WS-001",
        "WS-002",
    }


def test_should_list_work_sessions_by_person():

    repository = create_repository()

    repository.save(
        create_session(
            code="WS-001",
            person_code="TECH-001",
        )
    )

    repository.save(
        create_session(
            code="WS-002",
            person_code="TECH-001",
        )
    )

    repository.save(
        create_session(
            code="WS-003",
            person_code="TECH-002",
        )
    )

    result = repository.list_by_person(
        " tech-001 "
    )

    assert {
        session.code
        for session in result
    } == {
        "WS-001",
        "WS-002",
    }


def test_should_get_active_work_session_by_person():

    repository = create_repository()

    active_session = WorkSession(
        code="WS-ACTIVE",
        work_order_code="WO-001",
        activity_code="ACT-001",
        person_code="TECH-001",
        started_at=dt(10),
        ended_at=None,
        source=WorkSessionSource.AUTOMATIC,
        created_at=dt(10),
        created_by_person_code="TECH-001",
    )

    repository.save(
        active_session
    )

    result = repository.get_active_by_person(
        " tech-001 "
    )

    assert result is not None
    assert result.code == "WS-ACTIVE"
    assert result.is_active is True


def test_should_return_none_when_person_has_no_active_session():

    repository = create_repository()

    repository.save(
        create_session()
    )

    result = repository.get_active_by_person(
        "TECH-001"
    )

    assert result is None


def test_should_detect_overlap():

    repository = create_repository()

    repository.save(
        create_session(
            started_at=dt(8),
            ended_at=dt(10),
        )
    )

    assert (
        repository.has_overlap(
            person_code="TECH-001",
            started_at=dt(9),
            ended_at=dt(11),
        )
        is True
    )


def test_should_not_detect_touching_sessions_as_overlap():

    repository = create_repository()

    repository.save(
        create_session(
            started_at=dt(8),
            ended_at=dt(10),
        )
    )

    assert (
        repository.has_overlap(
            person_code="TECH-001",
            started_at=dt(10),
            ended_at=dt(11),
        )
        is False
    )


def test_should_ignore_different_person_when_checking_overlap():

    repository = create_repository()

    repository.save(
        create_session(
            person_code="TECH-001",
            started_at=dt(8),
            ended_at=dt(10),
        )
    )

    assert (
        repository.has_overlap(
            person_code="TECH-002",
            started_at=dt(9),
            ended_at=dt(11),
        )
        is False
    )


def test_should_ignore_excluded_work_session_when_checking_overlap():

    repository = create_repository()

    repository.save(
        create_session(
            code="WS-001",
            started_at=dt(8),
            ended_at=dt(10),
        )
    )

    assert (
        repository.has_overlap(
            person_code="TECH-001",
            started_at=dt(8, 30),
            ended_at=dt(10, 30),
            exclude_work_session_code=" ws-001 ",
        )
        is False
    )


def test_should_still_detect_other_overlap_when_one_session_is_excluded():

    repository = create_repository()

    repository.save(
        create_session(
            code="WS-001",
            started_at=dt(8),
            ended_at=dt(9),
        )
    )

    repository.save(
        create_session(
            code="WS-002",
            started_at=dt(9),
            ended_at=dt(11),
        )
    )

    assert (
        repository.has_overlap(
            person_code="TECH-001",
            started_at=dt(8, 30),
            ended_at=dt(10),
            exclude_work_session_code="WS-001",
        )
        is True
    )


def test_active_work_session_should_overlap_future_end_time():

    repository = create_repository()

    active_session = WorkSession(
        code="WS-ACTIVE",
        work_order_code="WO-001",
        activity_code="ACT-001",
        person_code="TECH-001",
        started_at=dt(8),
        ended_at=None,
        source=WorkSessionSource.AUTOMATIC,
        created_at=dt(8),
        created_by_person_code="TECH-001",
    )

    repository.save(
        active_session
    )

    assert (
        repository.has_overlap(
            person_code="TECH-001",
            started_at=dt(9),
            ended_at=dt(10),
        )
        is True
    )
