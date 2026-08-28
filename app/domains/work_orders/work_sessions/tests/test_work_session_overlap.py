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


def create_session(
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
        ended_at=ended_at,
        source=WorkSessionSource.AUTOMATIC,
        created_at=dt(7),
        created_by_person_code=person_code,
    )


def test_should_detect_overlap_inside_existing_session():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            started_at=dt(7),
            ended_at=dt(9),
        )
    )

    assert repository.has_overlap(
        "TECH-001",
        dt(8),
        dt(8, 30),
    ) is True


def test_should_detect_overlap_starting_inside_existing_session():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            started_at=dt(7),
            ended_at=dt(9),
        )
    )

    assert repository.has_overlap(
        "TECH-001",
        dt(8, 30),
        dt(10),
    ) is True


def test_should_detect_overlap_ending_inside_existing_session():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            started_at=dt(8),
            ended_at=dt(10),
        )
    )

    assert repository.has_overlap(
        "TECH-001",
        dt(7),
        dt(9),
    ) is True


def test_should_detect_new_session_covering_existing_session():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            started_at=dt(8),
            ended_at=dt(9),
        )
    )

    assert repository.has_overlap(
        "TECH-001",
        dt(7),
        dt(10),
    ) is True


def test_should_allow_session_ending_when_existing_starts():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            started_at=dt(9),
            ended_at=dt(10),
        )
    )

    assert repository.has_overlap(
        "TECH-001",
        dt(8),
        dt(9),
    ) is False


def test_should_allow_session_starting_when_existing_ends():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            started_at=dt(7),
            ended_at=dt(9),
        )
    )

    assert repository.has_overlap(
        "TECH-001",
        dt(9),
        dt(10),
    ) is False


def test_should_ignore_sessions_from_other_person():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            person_code="TECH-002",
            started_at=dt(7),
            ended_at=dt(10),
        )
    )

    assert repository.has_overlap(
        "TECH-001",
        dt(8),
        dt(9),
    ) is False


def test_should_detect_overlap_with_active_session():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            started_at=dt(8),
            ended_at=None,
        )
    )

    assert repository.has_overlap(
        "TECH-001",
        dt(9),
        dt(10),
    ) is True


def test_should_allow_historical_session_before_active_session():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            started_at=dt(13),
            ended_at=None,
        )
    )

    assert repository.has_overlap(
        "TECH-001",
        dt(9),
        dt(10),
    ) is False

def test_should_ignore_excluded_work_session_when_checking_overlap():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            code="WS-001",
            person_code="TECH-001",
            started_at=dt(8),
            ended_at=dt(10),
        )
    )

    assert repository.has_overlap(
        person_code="TECH-001",
        started_at=dt(8),
        ended_at=dt(10, 30),
        exclude_work_session_code="WS-001",
    ) is False


def test_should_still_detect_other_overlap_when_one_session_is_excluded():

    repository = InMemoryWorkSessionRepository()

    repository.save(
        create_session(
            code="WS-001",
            person_code="TECH-001",
            started_at=dt(7),
            ended_at=dt(8),
        )
    )

    repository.save(
        create_session(
            code="WS-002",
            person_code="TECH-001",
            started_at=dt(9),
            ended_at=dt(11),
        )
    )

    assert repository.has_overlap(
        person_code="TECH-001",
        started_at=dt(7, 30),
        ended_at=dt(10),
        exclude_work_session_code="WS-001",
    ) is True
