from datetime import datetime

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from app.domains.work_orders.use_cases.list_work_order_summaries import (
    ListWorkOrderSummariesResult,
    WorkOrderSummaryItem,
)

from app.domains.work_orders.presentation import (
    WorkOrderSummaryPresenter,
)


def create_summary(
    status=WorkOrderStatus.IN_PROGRESS,
):

    work_order = WorkOrder(
        code="WO-001",
        title="Mantenimiento tablero",
        description="Prueba",
        work_type="CORRECTIVE",
        priority="HIGH",
        asset_code="ASSET-001",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            8,
            21,
            10,
            30,
        ),
        status=status,
    )

    return WorkOrderSummaryItem(
        work_order=work_order,
        asset=None,
        requester=None,
        supervisor=None,
        active_technicians=[],
        participant_technicians=[],
    )


def test_should_present_in_progress_work_order():

    result = ListWorkOrderSummariesResult(
        items=[
            create_summary(
                WorkOrderStatus.IN_PROGRESS
            )
        ]
    )

    view_model = (
        WorkOrderSummaryPresenter.present(
            result
        )
    )

    item = view_model.items[0]

    assert item.code == "WO-001"
    assert item.status == "IN_PROGRESS"
    assert item.status_label == "En proceso"
    assert item.technician_label == "Realizando"
    assert item.created_at == "21/08/2026 10:30"


def test_should_present_closed_work_order():

    result = ListWorkOrderSummariesResult(
        items=[
            create_summary(
                WorkOrderStatus.CLOSED
            )
        ]
    )

    view_model = (
        WorkOrderSummaryPresenter.present(
            result
        )
    )

    item = view_model.items[0]

    assert item.status == "CLOSED"
    assert item.status_label == "Cerrada"
    assert item.technician_label == "Participaron"


def test_should_present_missing_related_data():

    result = ListWorkOrderSummariesResult(
        items=[
            create_summary()
        ]
    )

    view_model = (
        WorkOrderSummaryPresenter.present(
            result
        )
    )

    item = view_model.items[0]

    assert (
        item.asset_name
        == "Activo no disponible"
    )

    assert (
        item.requester_name
        == "Solicitante no disponible"
    )

    assert (
        item.supervisor_name
        == "Supervisor no disponible"
    )

    assert item.technician_names == []


def test_should_present_summary_totals():

    result = ListWorkOrderSummariesResult(
        items=[
            create_summary(),
            create_summary(
                WorkOrderStatus.CLOSED
            ),
        ]
    )

    view_model = (
        WorkOrderSummaryPresenter.present(
            result
        )
    )

    assert view_model.total == 2
    assert view_model.has_items is True

def test_should_classify_in_progress_as_active():

    result = ListWorkOrderSummariesResult(
        items=[
            create_summary(
                WorkOrderStatus.IN_PROGRESS
            )
        ]
    )

    view_model = (
        WorkOrderSummaryPresenter.present(
            result
        )
    )

    item = view_model.items[0]

    assert (
        item.operational_state
        == "ACTIVE"
    )

    assert (
        item.operational_state_label
        == "Activa"
    )


def test_should_classify_closed_as_finished():

    result = ListWorkOrderSummariesResult(
        items=[
            create_summary(
                WorkOrderStatus.CLOSED
            )
        ]
    )

    view_model = (
        WorkOrderSummaryPresenter.present(
            result
        )
    )

    item = view_model.items[0]

    assert (
        item.operational_state
        == "FINISHED"
    )

    assert (
        item.operational_state_label
        == "Finalizada"
    )


def test_should_calculate_summary_counters():

    result = ListWorkOrderSummariesResult(
        items=[
            create_summary(
                WorkOrderStatus.IN_PROGRESS
            ),
            create_summary(
                WorkOrderStatus.ON_HOLD
            ),
            create_summary(
                WorkOrderStatus.CLOSED
            ),
            create_summary(
                WorkOrderStatus.CANCELLED
            ),
        ]
    )

    view_model = (
        WorkOrderSummaryPresenter.present(
            result
        )
    )

    assert view_model.total == 4
    assert view_model.total_active == 2
    assert view_model.total_finished == 1
    assert view_model.total_cancelled == 1

    assert (
        view_model.total_by_status(
            "IN_PROGRESS"
        )
        == 1
    )
