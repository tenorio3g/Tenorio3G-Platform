from datetime import datetime

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)
from app.domains.work_orders.activities.bootstrap import (
    work_order_activity_repository,
)

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from app.domains.work_orders.bootstrap.work_order_container import (
    work_order_summary_technician_repository,
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

    work_order = create_web_work_order(
        code="WO-WEB-001"
    )

    work_order.approve()

    work_orders_test_db.save(
        work_order
    )

    work_order_summary_technician_repository.save(
        WorkOrderTechnicianAssignment(
            work_order_code="WO-WEB-001",
            person_code="TECH-001",
            assigned_at=datetime(
                2026,
                8,
                25,
                18,
                0,
            ),
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

    assert persisted is not None

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
    work_order.approve()
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
    work_order.approve()
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
    work_order.approve()
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
    work_order.approve()
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
    work_order.approve()
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

def test_should_unassign_technician_from_web(
    authenticated_client,
    work_orders_test_db,
):

    from datetime import datetime

    from app.domains.work_orders.technicians.bootstrap import (
        technician_assignment_repository,
    )

    from app.domains.work_orders.technicians.entities import (
        WorkOrderTechnicianAssignment,
    )

    work_order = create_web_work_order(
        code="WO-WEB-UNASSIGN"
    )

    work_orders_test_db.save(
        work_order
    )
    technician_assignment_repository.delete(
        "WO-WEB-UNASSIGN",
        "55464",
    )
    technician_assignment_repository.save(
        WorkOrderTechnicianAssignment(
            work_order_code="WO-WEB-UNASSIGN",
            person_code="55464",
            assigned_at=datetime(
                2026,
                8,
                16,
                14,
                30,
            ),
        )
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-UNASSIGN/"
        "tecnicos/55464/quitar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert technician_assignment_repository.exists(
        "WO-WEB-UNASSIGN",
        "55464",
    ) is False

def test_should_render_create_activity_form_with_assigned_technician(
    authenticated_client,
    work_orders_test_db,
):

    from app.domains.work_orders.technicians.bootstrap import (
        technician_assignment_repository,
    )

    work_order_code = "WO-ACTFORM-001"

    work_orders_test_db.save(
        create_web_work_order(
            work_order_code
        )
    )

    technician_assignment_repository.save(
        WorkOrderTechnicianAssignment(
            work_order_code=work_order_code,
            person_code="55464",
            assigned_at=datetime(
                2026,
                9,
                12,
                16,
                0,
            ),
        )
    )

    response = authenticated_client.get(
        f"/ordenes/{work_order_code}/actividades/nueva"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert (
        'name="responsible_person_code"'
        in html
    )

    assert "<select" in html

    assert 'value="55464"' in html

    assert "Crear actividad" in html

    assert (
        'name="code"'
        not in html
    )


def test_should_render_create_activity_form_without_assigned_technicians(
    authenticated_client,
    work_orders_test_db,
):

    work_order_code = "WO-ACTFORM-002"

    work_orders_test_db.save(
        create_web_work_order(
            work_order_code
        )
    )

    response = authenticated_client.get(
        f"/ordenes/{work_order_code}/actividades/nueva"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert (
        "Esta orden no tiene técnicos asignados."
        in html
    )

    assert (
        'name="responsible_person_code"'
        not in html
    )

    assert (
        ">Crear actividad<"
        not in html
    )


def test_should_preserve_activity_responsible_when_post_validation_fails(
    authenticated_client,
    work_orders_test_db,
    work_order_activities_test_db,
):

    from app.domains.work_orders.technicians.bootstrap import (
        technician_assignment_repository,
    )

    work_order_code = "WO-ACTFORM-003"

    work_orders_test_db.save(
        create_web_work_order(
            work_order_code
        )
    )

    technician_assignment_repository.save(
        WorkOrderTechnicianAssignment(
            work_order_code=work_order_code,
            person_code="55464",
            assigned_at=datetime(
                2026,
                9,
                12,
                16,
                0,
            ),
        )
    )

    response = authenticated_client.post(
        f"/ordenes/{work_order_code}/actividades/nueva",
        data={
            "title": "",
            "responsible_person_code": "55464",
            "description": "Prueba de validación",
            "estimated_minutes": "30",
        },
        follow_redirects=False,
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert (
        'value="55464"'
        in html
    )

    assert "selected" in html

    assert (
        'name="code"'
        not in html
    )


def test_should_create_activity_from_web_with_automatic_code(
    authenticated_client,
    work_orders_test_db,
    work_order_activities_test_db,
):

    from app.domains.work_orders.technicians.bootstrap import (
        technician_assignment_repository,
    )

    work_order_code = "WO-ACTWEB-001"

    work_orders_test_db.save(
        create_web_work_order(
            work_order_code
        )
    )

    technician_assignment_repository.save(
        WorkOrderTechnicianAssignment(
            work_order_code=work_order_code,
            person_code="55464",
            assigned_at=datetime(
                2026,
                9,
                12,
                16,
                0,
            ),
        )
    )

    response = authenticated_client.post(
        f"/ordenes/{work_order_code}/actividades/nueva",
        data={
            "title": "Inspección visual",
            "responsible_person_code": "55464",
            "description": (
                "Actividad creada desde interfaz web."
            ),
            "estimated_minutes": "30",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    expected_code = (
        f"{work_order_code}-ACT-001"
    )

    persisted = (
        work_order_activities_test_db.get_by_code(
            expected_code
        )
    )

    assert persisted is not None

    assert (
        persisted.code
        == expected_code
    )

    assert (
        persisted.work_order_code
        == work_order_code
    )

    assert (
        persisted.responsible_person_code
        == "55464"
    )

    assert (
        persisted.title
        == "Inspección visual"
    )

def test_should_start_activity_from_web(
    authenticated_client,
    work_order_activities_test_db,
):

    activity = WorkOrderActivity(
        code="ACT-WEB-START",
        work_order_code="WO-REAL-001",
        title="Actividad web",
        responsible_person_code="55464",
        estimated_minutes=30,
    )

    work_order_activities_test_db.save(
        activity
    )
    

    response = authenticated_client.post(
        "/ordenes/WO-REAL-001/"
        "actividades/ACT-WEB-START/iniciar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = (
        work_order_activities_test_db.get_by_code(
            "ACT-WEB-START"
        )
    )

    assert (
        persisted.status
        == ActivityStatus.IN_PROGRESS
    )

    assert persisted.started_at is not None


def test_should_complete_activity_from_web(
    authenticated_client,
    work_order_activities_test_db,
):

    activity = WorkOrderActivity(
        code="ACT-WEB-COMPLETE",
        work_order_code="WO-REAL-001",
        title="Actividad web",
        responsible_person_code="55464",
        estimated_minutes=30,
    )

    activity.start(
        datetime.now()
    )

    work_order_activities_test_db.save(
        activity
    )

    response = authenticated_client.post(
        "/ordenes/WO-REAL-001/"
        "actividades/ACT-WEB-COMPLETE/finalizar",
        follow_redirects=False,
    )

    assert response.status_code == 302

    persisted = (
        work_order_activities_test_db.get_by_code(
            "ACT-WEB-COMPLETE"
        )
    )

    assert (
        persisted.status
        == ActivityStatus.COMPLETED
    )

    assert (
        persisted.completed_at
        is not None
    )

    assert (
        persisted.actual_minutes
        is not None
    )

def test_should_render_add_spare_part_form(
    authenticated_client,
):

    response = authenticated_client.get(
        "/ordenes/WO-REAL-001/refacciones/nueva"
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "Registrar refacción utilizada" in html
    assert "Código de refacción" in html
    assert "Cantidad" in html


def test_should_add_spare_part_from_web(
    authenticated_client,
    work_orders_test_db,
    work_order_materials_test_db,
    monkeypatch,
):

    from app.domains.assets.spare_parts.entities import (
        SparePart,
    )

    from app.domains.assets.spare_parts.repositories import (
        InMemorySparePartRepository,
    )

    from app.domains.work_orders.materials.bootstrap import (
        add_spare_part_to_work_order,
    )

    work_order = create_web_work_order(
        code="WO-WEB-SPARE"
    )
    work_order.approve()

    work_orders_test_db.save(
        work_order
    )

    spare_part_repository = (
        InMemorySparePartRepository()
    )

    spare_part_repository.save_spare_part(
        SparePart(
            code="SP-WEB-001",
            name="Balero web",
            manufacturer="SKF",
            part_number="6206",
            unit="pieza",
        )
    )

    monkeypatch.setattr(
        add_spare_part_to_work_order,
        "_spare_part_repository",
        spare_part_repository,
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-SPARE/refacciones/nueva",
        data={
            "spare_part_code": "SP-WEB-001",
            "quantity": "2",
            "unit_cost": "15.50",
            "observations": "Prueba web.",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    usages = (
        work_order_materials_test_db
        .list_by_work_order(
            "WO-WEB-SPARE"
        )
    )

    assert len(usages) == 1

    usage = usages[0]

    assert usage.spare_part_code == "SP-WEB-001"
    assert usage.quantity == 2
    assert usage.unit_cost == 15.5
    assert usage.total_cost == 31.0

    assert (
        usage.observations
        == "Prueba web."
    )


def test_should_reject_unknown_spare_part_from_web(
    authenticated_client,
    work_orders_test_db,
    work_order_materials_test_db,
    monkeypatch,
):

    from app.domains.assets.spare_parts.repositories import (
        InMemorySparePartRepository,
    )

    from app.domains.work_orders.materials.bootstrap import (
        add_spare_part_to_work_order,
    )

    work_order = create_web_work_order(
        code="WO-WEB-SPARE-MISSING"
    )

    work_orders_test_db.save(
        work_order
    )

    monkeypatch.setattr(
        add_spare_part_to_work_order,
        "_spare_part_repository",
        InMemorySparePartRepository(),
    )

    response = authenticated_client.post(
        "/ordenes/WO-WEB-SPARE-MISSING/refacciones/nueva",
        data={
            "spare_part_code": "SP-NOT-FOUND",
            "quantity": "1",
            "unit_cost": "10",
            "observations": "",
        },
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "spare part not found" in html

    assert (
        work_order_materials_test_db
        .list_by_work_order(
            "WO-WEB-SPARE-MISSING"
        )
        == []
    )


def test_should_reject_invalid_spare_part_quantity_from_web(
    authenticated_client,
):

    response = authenticated_client.post(
        "/ordenes/WO-REAL-001/refacciones/nueva",
        data={
            "spare_part_code": "TEST-BRG-6206",
            "quantity": "abc",
            "unit_cost": "10",
            "observations": "",
        },
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "abc" in html


def test_should_reject_invalid_spare_part_unit_cost_from_web(
    authenticated_client,
):

    response = authenticated_client.post(
        "/ordenes/WO-REAL-001/refacciones/nueva",
        data={
            "spare_part_code": "TEST-BRG-6206",
            "quantity": "1",
            "unit_cost": "abc",
            "observations": "",
        },
    )

    assert response.status_code == 200

    html = response.get_data(
        as_text=True
    )

    assert "abc" in html


# ============================================================
# WORK-ORDER-EXECUTION-002B
# Web integration: iniciar trabajo
# ============================================================


def test_should_redirect_unauthenticated_start_work_session_to_login(
    client,
):
    response = client.post(
        (
            "/ordenes/WO-WSWEB-001/"
            "actividades/WO-WSWEB-001-ACT-001/"
            "trabajo/iniciar"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert "/login" in response.headers["Location"]


def test_should_start_work_session_from_web(
    authenticated_client,
    work_orders_test_db,
    work_order_activities_test_db,
    people_test_db,
):
    from app.domains.identity.people.entities import Person

    from app.domains.work_orders.work_sessions.bootstrap import (
        work_session_repository,
    )

    work_order_code = "WO-WSWEB-001"
    activity_code = "WO-WSWEB-001-ACT-001"

    people_test_db.save(
        Person(
            code="TEST-001",
            name="Técnico de prueba",
        )
    )

    work_order = create_web_work_order(
        code=work_order_code,
    )

    work_order.approve()
    work_order.assign()

    work_orders_test_db.save(
        work_order
    )

    activity = WorkOrderActivity(
        code=activity_code,
        work_order_code=work_order_code,
        title="Inspección desde web",
        responsible_person_code="TEST-001",
        estimated_minutes=30,
    )

    work_order_activities_test_db.save(
        activity
    )

    response = authenticated_client.post(
        (
            f"/ordenes/{work_order_code}/"
            f"actividades/{activity_code}/"
            "trabajo/iniciar"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 302

    sessions = (
        work_session_repository.list_by_work_order(
            work_order_code
        )
    )

    assert len(sessions) == 1

    session = sessions[0]

    assert session.code == "WO-WSWEB-001-WS-001"

    assert session.work_order_code == work_order_code

    assert session.activity_code == activity_code

    assert session.person_code == "TEST-001"

    assert session.created_by_person_code == "TEST-001"

    assert session.ended_at is None

    persisted_activity = (
        work_order_activities_test_db.get_by_code(
            activity_code
        )
    )

    assert (
        persisted_activity.status
        == ActivityStatus.IN_PROGRESS
    )

    assert persisted_activity.started_at is not None

    persisted_order = (
        work_orders_test_db.get_by_code(
            work_order_code
        )
    )

    assert (
        persisted_order.status
        == WorkOrderStatus.IN_PROGRESS
    )


def test_should_reject_start_work_session_for_non_responsible_person(
    authenticated_client,
    work_orders_test_db,
    work_order_activities_test_db,
    people_test_db,
):
    from app.domains.identity.people.entities import Person

    from app.domains.work_orders.work_sessions.bootstrap import (
        work_session_repository,
    )

    work_order_code = "WO-WSWEB-002"
    activity_code = "WO-WSWEB-002-ACT-001"

    people_test_db.save(
        Person(
            code="TEST-001",
            name="Técnico autenticado",
        )
    )

    work_order = create_web_work_order(
        code=work_order_code,
    )

    work_order.approve()
    work_order.assign()

    work_orders_test_db.save(
        work_order
    )

    activity = WorkOrderActivity(
        code=activity_code,
        work_order_code=work_order_code,
        title="Actividad de otro técnico",
        responsible_person_code="TECH-OTHER",
        estimated_minutes=30,
    )

    work_order_activities_test_db.save(
        activity
    )

    response = authenticated_client.post(
        (
            f"/ordenes/{work_order_code}/"
            f"actividades/{activity_code}/"
            "trabajo/iniciar"
        ),
        follow_redirects=False,
    )

    assert response.status_code == 400

    assert (
        b"person is not responsible for activity"
        in response.data
    )

    sessions = (
        work_session_repository.list_by_work_order(
            work_order_code
        )
    )

    assert sessions == []

    persisted_activity = (
        work_order_activities_test_db.get_by_code(
            activity_code
        )
    )

    assert (
        persisted_activity.status
        == ActivityStatus.PENDING
    )
