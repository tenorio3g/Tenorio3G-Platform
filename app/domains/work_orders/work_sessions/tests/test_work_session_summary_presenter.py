from datetime import datetime

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from app.domains.work_orders.work_sessions.presentation.work_session_summary_presenter import (
    WorkSessionSummaryPresenter,
)

from app.domains.work_orders.work_sessions.use_cases.get_work_session_summary import (
    GetWorkSessionSummaryResult,
    WorkSessionSummaryItem,
)

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)


def create_item(
    code: str,
    person_code: str,
    person_name: str,
    started_at: datetime,
    ended_at: datetime | None,
):
    return WorkSessionSummaryItem(
        work_session=WorkSession(
            code=code,
            work_order_code="WO-001",
            activity_code="WO-001-ACT-001",
            person_code=person_code,
            started_at=started_at,
            ended_at=ended_at,
            source=WorkSessionSource.AUTOMATIC,
            created_at=started_at,
            created_by_person_code=person_code,
        ),
        person=Person(
            code=person_code,
            name=person_name,
        ),
    )


def test_should_present_closed_sessions_and_total_time():

    result = GetWorkSessionSummaryResult(
        items=[
            create_item(
                code="WO-001-WS-001",
                person_code="TECH-001",
                person_name="Técnico Uno",
                started_at=datetime(
                    2026, 9, 12, 8, 0
                ),
                ended_at=datetime(
                    2026, 9, 12, 8, 45
                ),
            ),
            create_item(
                code="WO-001-WS-002",
                person_code="TECH-001",
                person_name="Técnico Uno",
                started_at=datetime(
                    2026, 9, 12, 9, 0
                ),
                ended_at=datetime(
                    2026, 9, 12, 9, 50
                ),
            ),
        ]
    )

    view_model = (
        WorkSessionSummaryPresenter.present(
            result
        )
    )

    activity = view_model.by_activity[
        "WO-001-ACT-001"
    ]

    assert activity.total_minutes == 95
    assert (
        activity.total_duration_label
        == "1 h 35 min"
    )
    assert activity.closed_session_count == 2
    assert activity.has_active_session is False

    assert len(activity.sessions) == 2

    assert (
        activity.sessions[0].duration_label
        == "45 min"
    )

    assert (
        activity.sessions[1].duration_label
        == "50 min"
    )


def test_should_show_active_session_without_adding_to_total():

    result = GetWorkSessionSummaryResult(
        items=[
            create_item(
                code="WO-001-WS-001",
                person_code="TECH-001",
                person_name="Técnico Uno",
                started_at=datetime(
                    2026, 9, 12, 8, 0
                ),
                ended_at=datetime(
                    2026, 9, 12, 8, 30
                ),
            ),
            create_item(
                code="WO-001-WS-002",
                person_code="TECH-001",
                person_name="Técnico Uno",
                started_at=datetime(
                    2026, 9, 12, 9, 0
                ),
                ended_at=None,
            ),
        ]
    )

    view_model = (
        WorkSessionSummaryPresenter.present(
            result
        )
    )

    activity = view_model.by_activity[
        "WO-001-ACT-001"
    ]

    assert activity.total_minutes == 30
    assert activity.total_duration_label == (
        "30 min"
    )

    assert activity.closed_session_count == 1
    assert activity.has_active_session is True

    active_session = activity.sessions[1]

    assert active_session.is_active is True
    assert active_session.duration_minutes is None
    assert active_session.duration_label == (
        "En curso"
    )


def test_should_calculate_time_per_technician():

    result = GetWorkSessionSummaryResult(
        items=[
            create_item(
                code="WO-001-WS-001",
                person_code="TECH-001",
                person_name="Técnico Uno",
                started_at=datetime(
                    2026, 9, 12, 8, 0
                ),
                ended_at=datetime(
                    2026, 9, 12, 9, 0
                ),
            ),
            create_item(
                code="WO-001-WS-002",
                person_code="TECH-002",
                person_name="Técnico Dos",
                started_at=datetime(
                    2026, 9, 12, 9, 0
                ),
                ended_at=datetime(
                    2026, 9, 12, 9, 35
                ),
            ),
        ]
    )

    view_model = (
        WorkSessionSummaryPresenter.present(
            result
        )
    )

    activity = view_model.by_activity[
        "WO-001-ACT-001"
    ]

    assert activity.total_minutes == 95

    technicians = {
        item.person_code: item
        for item in activity.technicians
    }

    assert technicians[
        "TECH-001"
    ].total_minutes == 60

    assert technicians[
        "TECH-001"
    ].total_duration_label == "1 h"

    assert technicians[
        "TECH-002"
    ].total_minutes == 35

    assert technicians[
        "TECH-002"
    ].total_duration_label == "35 min"