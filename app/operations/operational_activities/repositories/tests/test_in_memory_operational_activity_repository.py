from datetime import date, datetime

from app.operations.operational_activities.entities.operational_activity import (
    OperationalActivity,
)
from app.operations.operational_activities.repositories.in_memory_operational_activity_repository import (
    InMemoryOperationalActivityRepository,
)


def create_activity(
    code: str = "OP-ACT-001",
) -> OperationalActivity:
    return OperationalActivity(
        code=code,
        description="Revisi?n de alumbrado exterior",
        started_at=datetime(
            2026,
            9,
            17,
            7,
            0,
        ),
        area="Exterior",
        created_by_person_code="SUP-001",
    )


def test_should_save_and_get_operational_activity_by_code():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = create_activity()

    repository.save(activity)

    saved_activity = repository.get_by_code(
        "OP-ACT-001"
    )

    assert saved_activity is activity
    assert saved_activity.code == "OP-ACT-001"

def test_should_list_all_operational_activities():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    first_activity = create_activity(
        code="OP-ACT-001",
    )

    second_activity = create_activity(
        code="OP-ACT-002",
    )

    repository.save(first_activity)
    repository.save(second_activity)

    activities = repository.list_all()

    assert len(activities) == 2
    assert activities == [
        first_activity,
        second_activity,
    ]

def test_should_list_activity_inside_requested_date():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-003",
        description="Mantenimiento a UPS",
        started_at=datetime(
            2026,
            9,
            17,
            14,
            30,
        ),
        ended_at=datetime(
            2026,
            9,
            17,
            16,
            30,
        ),
        area="Pintura",
        work_order_code="71416",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    activities = repository.list_by_date(
        date(2026, 9, 17)
    )

    assert activities == [activity]

def test_should_list_activity_on_both_dates_when_crossing_midnight():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-004",
        description="Soporte en Subestaci?n 1",
        started_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
        ended_at=datetime(
            2026,
            9,
            17,
            1,
            30,
        ),
        area="Subestaci?n 1",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    activities_day_16 = repository.list_by_date(
        date(2026, 9, 16)
    )

    activities_day_17 = repository.list_by_date(
        date(2026, 9, 17)
    )

    assert activities_day_16 == [activity]
    assert activities_day_17 == [activity]

def test_should_list_open_activity_carried_over_from_previous_date():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-005",
        description="Soporte en Subestaci?n 1",
        started_at=datetime(
            2026,
            9,
            16,
            23,
            30,
        ),
        ended_at=None,
        area="Subestaci?n 1",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    activities_day_16 = repository.list_by_date(
        date(2026, 9, 16)
    )

    activities_day_17 = repository.list_by_date(
        date(2026, 9, 17)
    )

    assert activities_day_16 == [activity]
    assert activities_day_17 == [activity]

def test_should_exclude_activity_unrelated_to_requested_date():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-006",
        description="Revisi?n de alumbrado",
        started_at=datetime(
            2026,
            9,
            16,
            7,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            16,
            9,
            0,
        ),
        area="MD2",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    activities = repository.list_by_date(
        date(2026, 9, 17)
    )

    assert activities == []

