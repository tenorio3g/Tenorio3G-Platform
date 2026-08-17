from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.repositories import (
    SQLiteWorkOrderActivityRepository,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
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

    return SQLiteWorkOrderActivityRepository(
        session_factory
    )


def create_activity(
    code="ACT-001",
    work_order_code="WO-001",
):

    return WorkOrderActivity(
        code=code,
        work_order_code=work_order_code,
        title="Inspección general",
        description="Revisar conexiones.",
        responsible_person_code="55464",
        estimated_minutes=30,
    )


def test_should_save_and_get_activity():

    repository = create_repository()

    repository.save(
        create_activity()
    )

    persisted = repository.get_by_code(
        "ACT-001"
    )

    assert persisted is not None
    assert persisted.code == "ACT-001"
    assert persisted.work_order_code == "WO-001"
    assert persisted.title == "Inspección general"

    assert (
        persisted.responsible_person_code
        == "55464"
    )

    assert (
        persisted.status
        == ActivityStatus.PENDING
    )

    assert persisted.estimated_minutes == 30


def test_should_list_activities_by_work_order():

    repository = create_repository()

    repository.save(
        create_activity(
            "ACT-001",
            "WO-001",
        )
    )

    repository.save(
        create_activity(
            "ACT-002",
            "WO-001",
        )
    )

    repository.save(
        create_activity(
            "ACT-003",
            "WO-002",
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


def test_should_persist_lifecycle_changes():

    repository = create_repository()

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

    assert (
        persisted.status
        == ActivityStatus.IN_PROGRESS
    )

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

    activity = persisted

    activity.complete(
        datetime(
            2026,
            8,
            16,
            10,
            45,
        )
    )

    repository.save(
        activity
    )

    persisted = repository.get_by_code(
        "ACT-001"
    )

    assert (
        persisted.status
        == ActivityStatus.COMPLETED
    )

    assert persisted.actual_minutes == 45


def test_should_update_existing_activity():

    repository = create_repository()

    activity = create_activity()

    repository.save(
        activity
    )

    activity.title = (
        "Inspección eléctrica completa"
    )

    activity.description = (
        "Revisar conexiones y torque."
    )

    activity.estimated_minutes = 60

    repository.save(
        activity
    )

    persisted = repository.get_by_code(
        "ACT-001"
    )

    assert (
        persisted.title
        == "Inspección eléctrica completa"
    )

    assert (
        persisted.description
        == "Revisar conexiones y torque."
    )

    assert persisted.estimated_minutes == 60


def test_should_delete_activity():

    repository = create_repository()

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