from datetime import datetime

import pytest

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


def create_work_order():

    return WorkOrder(
        code="WO-APPROVE-001",
        title="Instalar contacto 110 V",
        description="Solicitud de prueba.",
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
            8,
            0,
        ),
    )


def test_should_approve_created_work_order():

    work_order = create_work_order()

    work_order.approve()

    assert (
        work_order.status
        == WorkOrderStatus.APPROVED
    )


def test_should_not_approve_twice():

    work_order = create_work_order()

    work_order.approve()

    with pytest.raises(
        ValueError,
        match=(
            "work order cannot be approved "
            "from current status"
        ),
    ):
        work_order.approve()
