from datetime import datetime

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.holds.entities import (
    ActivityHold,
)

from app.domains.work_orders.activities.holds.value_objects import (
    ActivityHoldReason,
)

from app.domains.work_orders.activities.presentation import (
    WorkOrderActivitiesPresenter,
)

from app.domains.work_orders.activities.use_cases import (
    ListWorkOrderActivitiesResult,
    WorkOrderActivityItem,
)

from app.domains.work_orders.activities.use_cases.list_work_order_activities import (
    ActivityHoldHistoryItem,
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

    assert item.hold_reason is None
    assert item.hold_reason_label is None
    assert item.hold_observations is None
    assert item.held_at is None
    assert item.held_by_person_code is None


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
        ),
        completion_notes=(
            "Se realizó la inspección y "
            "se corrigieron las conexiones."
        ),
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
    assert presented.completion_notes == (
        "Se realizó la inspección y "
        "se corrigieron las conexiones."
    )


def test_should_present_activity_on_hold():

    item = create_item()

    item.activity.start(
        datetime(
            2026,
            9,
            14,
            10,
            0,
        )
    )

    item.activity.hold()

    hold = ActivityHold(
        code="AH-001",
        activity_code="ACT-001",
        reason=ActivityHoldReason.PENDING_MATERIAL,
        observations="Esperando llegada de material.",
        held_at=datetime(
            2026,
            9,
            14,
            10,
            30,
        ),
        held_by_person_code="55464",
    )

    item = WorkOrderActivityItem(
        activity=item.activity,
        responsible_person=(
            item.responsible_person
        ),
        active_hold=hold,
        held_by_person=(
            item.responsible_person
        ),
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

    assert presented.status == "ON_HOLD"
    assert presented.status_label == "En espera"

    assert (
        presented.hold_reason
        == "PENDING_MATERIAL"
    )

    assert (
        presented.hold_reason_label
        == "Material pendiente"
    )

    assert (
        presented.hold_observations
        == "Esperando llegada de material."
    )

    assert (
        presented.held_at
        == "14/09/2026 10:30"
    )

    assert (
        presented.held_by_person_code
        == "55464"
    )

    
    assert (
        presented.held_by_person_name
        == "Fortunato"
    )


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


def test_should_present_activity_hold_history():

    item = create_item()

    held_by_person = Person(
        code="TECH-001",
        name="Técnico Uno",
    )

    resumed_by_person = Person(
        code="TECH-002",
        name="Técnico Dos",
    )

    first_hold = ActivityHold(
        code="AH-001",
        activity_code="ACT-001",
        reason=(
            ActivityHoldReason.PENDING_MATERIAL
        ),
        observations="Esperando material",
        held_at=datetime(
            2026,
            9,
            14,
            10,
            0,
        ),
        held_by_person_code="TECH-001",
        resumed_at=datetime(
            2026,
            9,
            14,
            10,
            30,
        ),
        resumed_by_person_code="TECH-002",
    )

    second_hold = ActivityHold(
        code="AH-002",
        activity_code="ACT-001",
        reason=(
            ActivityHoldReason.EQUIPMENT_IN_USE
        ),
        observations="Área sin liberar",
        held_at=datetime(
            2026,
            9,
            14,
            11,
            0,
        ),
        held_by_person_code="TECH-001",
    )

    item = WorkOrderActivityItem(
        activity=item.activity,
        responsible_person=(
            item.responsible_person
        ),
        hold_history=[
            ActivityHoldHistoryItem(
                hold=first_hold,
                held_by_person=held_by_person,
                resumed_by_person=(
                    resumed_by_person
                ),
            ),
            ActivityHoldHistoryItem(
                hold=second_hold,
                held_by_person=held_by_person,
                resumed_by_person=None,
            ),
        ],
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

    assert len(presented.hold_history) == 2

    first = presented.hold_history[0]

    assert first.code == "AH-001"
    assert first.reason == "PENDING_MATERIAL"
    assert (
        first.reason_label
        == "Material pendiente"
    )
    assert (
        first.observations
        == "Esperando material"
    )
    assert (
        first.held_at
        == "14/09/2026 10:00"
    )
    assert (
        first.held_by_person_name
        == "Técnico Uno"
    )
    assert (
        first.resumed_at
        == "14/09/2026 10:30"
    )
    assert (
        first.resumed_by_person_name
        == "Técnico Dos"
    )
    assert first.duration_minutes == 30
    assert first.is_active is False

    second = presented.hold_history[1]

    assert second.code == "AH-002"
    assert (
        second.reason_label
        == "Equipo en uso"
    )
    assert second.resumed_at is None
    assert second.resumed_by_person_name is None
    assert second.duration_minutes is None
    assert second.is_active is True
