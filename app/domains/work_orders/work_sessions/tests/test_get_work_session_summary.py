from datetime import datetime

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

from app.domains.work_orders.work_sessions.use_cases.get_work_session_summary import (
    GetWorkSessionSummary,
    GetWorkSessionSummaryQuery,
)

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)


def create_work_session(
    code: str,
    work_order_code: str,
    activity_code: str,
    person_code: str,
    started_at: datetime,
    ended_at: datetime | None = None,
) -> WorkSession:

    return WorkSession(
        code=code,
        work_order_code=work_order_code,
        activity_code=activity_code,
        person_code=person_code,
        started_at=started_at,
        ended_at=ended_at,
        source=WorkSessionSource.AUTOMATIC,
        created_at=started_at,
        created_by_person_code=person_code,
    )


def test_should_list_work_sessions_with_person():

    work_session_repository = (
        InMemoryWorkSessionRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    person_repository.save(
        Person(
            code="TECH-001",
            name="Técnico Uno",
        )
    )

    work_session_repository.save(
        create_work_session(
            code="WO-001-WS-001",
            work_order_code="WO-001",
            activity_code="WO-001-ACT-001",
            person_code="TECH-001",
            started_at=datetime(
                2026,
                9,
                12,
                8,
                0,
            ),
            ended_at=datetime(
                2026,
                9,
                12,
                8,
                45,
            ),
        )
    )

    use_case = GetWorkSessionSummary(
        work_session_repository,
        person_repository,
    )

    result = use_case.execute(
        GetWorkSessionSummaryQuery(
            work_order_code="WO-001",
        )
    )

    assert len(result.items) == 1

    item = result.items[0]

    assert item.work_session.code == (
        "WO-001-WS-001"
    )

    assert item.person.code == "TECH-001"
    assert item.person.name == "Técnico Uno"


def test_should_only_return_sessions_from_requested_work_order():

    work_session_repository = (
        InMemoryWorkSessionRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    person_repository.save(
        Person(
            code="TECH-001",
            name="Técnico Uno",
        )
    )

    work_session_repository.save(
        create_work_session(
            code="WO-001-WS-001",
            work_order_code="WO-001",
            activity_code="WO-001-ACT-001",
            person_code="TECH-001",
            started_at=datetime(
                2026,
                9,
                12,
                8,
                0,
            ),
        )
    )

    work_session_repository.save(
        create_work_session(
            code="WO-002-WS-001",
            work_order_code="WO-002",
            activity_code="WO-002-ACT-001",
            person_code="TECH-001",
            started_at=datetime(
                2026,
                9,
                12,
                9,
                0,
            ),
        )
    )

    use_case = GetWorkSessionSummary(
        work_session_repository,
        person_repository,
    )

    result = use_case.execute(
        GetWorkSessionSummaryQuery(
            work_order_code="WO-001",
        )
    )

    assert len(result.items) == 1

    assert (
        result.items[0]
        .work_session
        .work_order_code
        == "WO-001"
    )


def test_should_skip_session_when_person_does_not_exist():

    work_session_repository = (
        InMemoryWorkSessionRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    work_session_repository.save(
        create_work_session(
            code="WO-001-WS-001",
            work_order_code="WO-001",
            activity_code="WO-001-ACT-001",
            person_code="TECH-404",
            started_at=datetime(
                2026,
                9,
                12,
                8,
                0,
            ),
        )
    )

    use_case = GetWorkSessionSummary(
        work_session_repository,
        person_repository,
    )

    result = use_case.execute(
        GetWorkSessionSummaryQuery(
            work_order_code="WO-001",
        )
    )

    assert result.items == []