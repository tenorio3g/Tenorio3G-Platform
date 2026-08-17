from datetime import datetime

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.presentation import (
    WorkOrderActivitiesPresenter,
)

from app.domains.work_orders.activities.use_cases import (
    ListWorkOrderActivitiesResult,
    WorkOrderActivityItem,
)


def create_item(
    code="ACT-001",
    name="Fortunato",
):

    activity = WorkOrderActivity(
        code=code,
        work_order_code="WO-001",
        title="Inspección visual",
        responsible_person_code="55464",
        description="Revisar conexiones.",
        estimated_minutes=30,
    )

    person = Person(
        code="55464",
        name=name,
        position="Supervisor",
    )

    return WorkOrderActivityItem(
        activity=activity,
        responsible_person=person,
    )


def test_should_present_activity():

    result = ListWorkOrderActivitiesResult(
        items=[
            create_item()
        ]
    )

    view_model = (
        WorkOrderActivitiesPresenter.present(
            result
        )
    )

    assert view_model.total == 1
    assert view_model.has_items is True

    item = view_model.items[0]

    assert item.code == "ACT-001"

    assert (
        item.title
        == "Inspección visual"
    )

    assert (
        item.responsible_person_name
        == "Fortunato"
    )

    assert item.status == "PENDING"
    assert item.status_label == "Pendiente"

    assert item.estimated_minutes == 30
    assert item.actual_minutes is None


def test_should_present_activity_lifecycle():

    item = create_item()

    item.activity.start(
        datetime(
            2026,
            8,
            16,
            10,
            0,
        )
    )

    item.activity.complete(
        datetime(
            2026,
            8,
            16,
            10,
            45,
        )
    )

    result = ListWorkOrderActivitiesResult(
        items=[item]
    )

    view_model = (
        WorkOrderActivitiesPresenter.present(
            result
        )
    )

    presented = view_model.items[0]

    assert presented.status == "COMPLETED"
    assert presented.status_label == "Finalizada"

    assert (
        presented.started_at
        == "16/08/2026 10:00"
    )

    assert (
        presented.completed_at
        == "16/08/2026 10:45"
    )

    assert presented.actual_minutes == 45


def test_should_calculate_progress():

    first = create_item(
        code="ACT-001"
    )

    second = create_item(
        code="ACT-002"
    )

    first.activity.start(
        datetime(
            2026,
            8,
            16,
            10,
            0,
        )
    )

    first.activity.complete(
        datetime(
            2026,
            8,
            16,
            10,
            30,
        )
    )

    result = ListWorkOrderActivitiesResult(
        items=[
            first,
            second,
        ]
    )

    view_model = (
        WorkOrderActivitiesPresenter.present(
            result
        )
    )

    assert view_model.total == 2
    assert view_model.completed == 1
    assert view_model.progress_percent == 50


def test_empty_activities_should_have_zero_progress():

    result = ListWorkOrderActivitiesResult(
        items=[]
    )

    view_model = (
        WorkOrderActivitiesPresenter.present(
            result
        )
    )

    assert view_model.has_items is False
    assert view_model.total == 0
    assert view_model.completed == 0
    assert view_model.progress_percent == 0