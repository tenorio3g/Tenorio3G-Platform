from datetime import datetime

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

def create_web_work_order(
    code,
):

    return WorkOrder(
        code=code,
        title="Orden web",
        description="Prueba.",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code="S2-480-ES09-T269",
        requester_person_code="55464",
        supervisor_person_code="12",
        created_at=datetime(
            2026,
            8,
            15,
            20,
            0,
        ),
    )

def test_should_assign_work_order_from_web(
    authenticated_client,
    work_orders_test_db,
):

    work_orders_test_db.save(
        create_web_work_order(
            code="WO-WEB-001"
        )
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-001/asignar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = work_orders_test_db.get_by_code(
        "WO-WEB-001"
    )

    assert (
        persisted.status
        == WorkOrderStatus.ASSIGNED
    )

def test_should_start_assigned_work_order_from_web(
    authenticated_client,
    work_orders_test_db,
):

    work_order = create_web_work_order(
        code="WO-WEB-002"
    )

    work_order.assign()

    work_orders_test_db.save(
        work_order
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-002/iniciar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = work_orders_test_db.get_by_code(
        "WO-WEB-002"
    )

    assert (
        persisted.status
        == WorkOrderStatus.IN_PROGRESS
    )

def test_should_resume_work_order_from_web(
    authenticated_client,
    work_orders_test_db,
):

    work_order = create_web_work_order(
        code="WO-WEB-RESUME"
    )

    work_order.assign()
    work_order.start()
    work_order.hold()

    work_orders_test_db.save(
        work_order
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-RESUME/reanudar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = work_orders_test_db.get_by_code(
        "WO-WEB-RESUME"
    )

    assert (
        persisted.status
        == WorkOrderStatus.IN_PROGRESS
    )


def test_should_complete_work_order_from_web(
    authenticated_client,
    work_orders_test_db,
):

    work_order = create_web_work_order(
        code="WO-WEB-COMPLETE"
    )

    work_order.assign()
    work_order.start()

    work_orders_test_db.save(
        work_order
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-COMPLETE/completar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = work_orders_test_db.get_by_code(
        "WO-WEB-COMPLETE"
    )

    assert (
        persisted.status
        == WorkOrderStatus.COMPLETED
    )


def test_should_close_work_order_from_web(
    authenticated_client,
    work_orders_test_db,
):

    work_order = create_web_work_order(
        code="WO-WEB-CLOSE"
    )

    work_order.assign()
    work_order.start()
    work_order.complete()

    work_orders_test_db.save(
        work_order
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-CLOSE/cerrar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = work_orders_test_db.get_by_code(
        "WO-WEB-CLOSE"
    )

    assert (
        persisted.status
        == WorkOrderStatus.CLOSED
    )


def test_should_cancel_work_order_from_web(
    authenticated_client,
    work_orders_test_db,
):

    work_orders_test_db.save(
        create_web_work_order(
            code="WO-WEB-CANCEL"
        )
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-CANCEL/cancelar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = work_orders_test_db.get_by_code(
        "WO-WEB-CANCEL"
    )

    assert (
        persisted.status
        == WorkOrderStatus.CANCELLED
    )

def test_should_hold_work_order_from_web(
    authenticated_client,
    work_orders_test_db,
):

    work_order = create_web_work_order(
        code="WO-WEB-HOLD"
    )

    work_order.assign()
    work_order.start()

    work_orders_test_db.save(
        work_order
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-HOLD/pausar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = work_orders_test_db.get_by_code(
        "WO-WEB-HOLD"
    )

    assert (
        persisted.status
        == WorkOrderStatus.ON_HOLD
    )


def test_work_order_detail_should_render_v2(
    authenticated_client,
):

    response = authenticated_client.get(
        "/ordenes/WO-REAL-001"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "WO-REAL-001" in html

    assert (
        "Prueba persistencia Work Orders"
        in html
    )

    assert (
        "TABLERO GENERAL ES09"
        in html
    )

    assert "Fortunato" in html

    assert (
        "pedro picasdsdfds"
        in html
    )


def test_work_order_detail_should_return_404_when_not_found(
    authenticated_client,
):

    response = authenticated_client.get(
        "/ordenes/WO-NOT-FOUND"
    )

    assert response.status_code == 404