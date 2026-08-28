from datetime import datetime

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.presentation import (
    WorkOrderPresenter,
    WorkOrderViewModel,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


def create_work_order():

    return WorkOrder(
        code="WO-001",
        title="Inspección general",
        description="Revisión del tablero.",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code="S2-480-ES09-T269",
        requester_person_code="55464",
        supervisor_person_code="12",
        created_at=datetime(
            2026,
            8,
            16,
            8,
            30,
        ),
    )


def test_should_present_work_order():

    work_order = create_work_order()

    view_model = (
        WorkOrderPresenter.present(
            work_order
        )
    )

    assert isinstance(
        view_model,
        WorkOrderViewModel,
    )

    assert view_model.code == "WO-001"
    assert view_model.title == "Inspección general"

    assert (
        view_model.asset_code
        == "S2-480-ES09-T269"
    )

    assert (
        view_model.requester_person_code
        == "55464"
    )

    assert (
        view_model.supervisor_person_code
        == "12"
    )

    assert (
        view_model.status
        == WorkOrderStatus.CREATED.value
    )

    assert (
        view_model.created_at
        == "16/08/2026 08:30"
    )


def test_should_present_current_status():

    work_order = create_work_order()

    work_order.approve()
    work_order.assign()
    work_order.start()

    view_model = (
        WorkOrderPresenter.present(
            work_order
        )
    )

    assert (
        view_model.status
        == WorkOrderStatus.IN_PROGRESS.value
    )
