from datetime import datetime

import pytest

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from app.domains.work_orders.technicians.repositories import (
    InMemoryWorkOrderTechnicianAssignmentRepository,
)

from app.domains.work_orders.technicians.use_cases import (
    UnassignTechnicianFromWorkOrder,
    UnassignTechnicianFromWorkOrderCommand,
)


def create_work_order():

    return WorkOrder(
        code="WO-001",
        title="Orden de prueba",
        description="Prueba.",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code="ASSET-001",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            8,
            16,
            14,
            0,
        ),
    )


def build_use_case():

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    assignment_repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    use_case = UnassignTechnicianFromWorkOrder(
        work_order_repository,
        assignment_repository,
    )

    return (
        work_order_repository,
        assignment_repository,
        use_case,
    )


def test_should_unassign_technician():

    (
        work_order_repository,
        assignment_repository,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    assignment_repository.save(
        WorkOrderTechnicianAssignment(
            work_order_code="WO-001",
            person_code="55464",
            assigned_at=datetime(
                2026,
                8,
                16,
                14,
                15,
            ),
        )
    )

    use_case.execute(
        UnassignTechnicianFromWorkOrderCommand(
            work_order_code="WO-001",
            person_code="55464",
        )
    )

    assert assignment_repository.exists(
        "WO-001",
        "55464",
    ) is False


def test_should_reject_unknown_work_order():

    _, _, use_case = build_use_case()

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            UnassignTechnicianFromWorkOrderCommand(
                work_order_code="WO-404",
                person_code="55464",
            )
        )


def test_should_reject_unassigned_technician():

    (
        work_order_repository,
        _,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    with pytest.raises(
        ValueError,
        match=(
            "technician is not assigned to work order"
        ),
    ):
        use_case.execute(
            UnassignTechnicianFromWorkOrderCommand(
                work_order_code="WO-001",
                person_code="55464",
            )
        )