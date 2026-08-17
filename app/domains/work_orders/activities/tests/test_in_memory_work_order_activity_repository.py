from datetime import datetime

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.repositories import (
    InMemoryWorkOrderActivityRepository,
)


def create_activity(
    code="ACT-001",
    work_order_code="WO-001",
):

    return WorkOrderActivity(
        code=code,
        work_order_code=work_order_code,
        title="Inspección general",
        responsible_person_code="55464",
        description="Prueba.",
        estimated_minutes=30,
    )


def test_should_save_and_get_activity():

    repository = (
        InMemoryWorkOrderActivityRepository()
    )

    repository.save(
        create_activity()
    )

    activity = repository.get_by_code(
        "ACT-001"
    )

    assert activity is not None
    assert activity.code == "ACT-001"


def test_get_by_code_should_normalize_code():

    repository = (
        InMemoryWorkOrderActivityRepository()
    )

    repository.save(
        create_activity()
    )

    activity = repository.get_by_code(
        " act-001 "
    )

    assert activity is not None
    assert activity.code == "ACT-001"


def test_should_list_activities_by_work_order():

    repository = (
        InMemoryWorkOrderActivityRepository()
    )

    repository.save(
        create_activity(
            code="ACT-001",
            work_order_code="WO-001",
        )
    )

    repository.save(
        create_activity(
            code="ACT-002",
            work_order_code="WO-001",
        )
    )

    repository.save(
        create_activity(
            code="ACT-003",
            work_order_code="WO-002",
        )
    )

    result = repository.list_by_work_order(
        " wo-001 "
    )

    assert len(result) == 2

    assert {
        activity.code
        for activity in result
    } == {
        "ACT-001",
        "ACT-002",
    }


def test_should_persist_activity_state_changes():

    repository = (
        InMemoryWorkOrderActivityRepository()
    )

    activity = create_activity()

    repository.save(
        activity
    )

    activity.start(
        datetime(
            2026,
            8,
            16,
            10,
            0,
        )
    )

    repository.save(
        activity
    )

    persisted = repository.get_by_code(
        "ACT-001"
    )

    assert persisted is not None

    assert (
        persisted.started_at
        == datetime(
            2026,
            8,
            16,
            10,
            0,
        )
    )


def test_should_delete_activity():

    repository = (
        InMemoryWorkOrderActivityRepository()
    )

    repository.save(
        create_activity()
    )

    repository.delete(
        " act-001 "
    )

    assert (
        repository.get_by_code(
            "ACT-001"
        )
        is None
    )