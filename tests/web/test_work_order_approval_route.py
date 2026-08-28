from datetime import datetime

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from app.domains.work_orders.bootstrap import (
    work_order_repository,
)

from app.foundation.timeline.engine.bootstrap import (
    timeline_event_repository,
)


def create_pending_work_order():

    return WorkOrder(
        code="WO-WEB-APPROVE-001",
        title="Solicitud pendiente de aprobación",
        description="Prueba web de aprobación.",
        work_type="PROJECT",
        priority="MEDIUM",
        asset_code=None,
        requester_person_code=None,
        requester_name="Juan Perez",
        requester_phone="8991234567",
        requester_area="Produccion",
        supervisor_person_code=None,
        location_description="Linea 4",
        created_at=datetime(
            2026,
            8,
            24,
            10,
            0,
        ),
    )


def test_should_approve_work_order_from_web(
    authenticated_client,
    work_orders_test_db,
):

    work_order_repository.save(
        create_pending_work_order()
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-APPROVE-001/aprobar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = work_order_repository.get_by_code(
        "WO-WEB-APPROVE-001"
    )

    assert persisted is not None

    assert (
        persisted.status
        == WorkOrderStatus.APPROVED
    )

    events = timeline_event_repository.list_by_entity(
        "WORK_ORDER",
        "WO-WEB-APPROVE-001",
    )

    assert len(events) == 1

    event = events[0]

    assert (
        event.event_type
        == "WORK_ORDER_APPROVED"
    )

    assert (
        event.actor_person_code
        == "TEST-001"
    )


def test_should_reject_approval_without_authenticated_person(
    client,
    work_orders_test_db,
):

    work_order_repository.save(
        create_pending_work_order()
    )

    response = client.post(
        "/ordenes/WO-WEB-APPROVE-001/aprobar",
        follow_redirects=False,
    )

    assert response.status_code == 401


def test_should_reject_second_approval(
    authenticated_client,
    work_orders_test_db,
):

    work_order = create_pending_work_order()

    work_order.approve()

    work_order_repository.save(
        work_order
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-APPROVE-001/aprobar",
        follow_redirects=False,
    )

    assert response.status_code == 400
