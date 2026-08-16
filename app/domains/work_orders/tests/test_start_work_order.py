from datetime import datetime

import pytest

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.use_cases import (
    StartWorkOrder,
    StartWorkOrderCommand,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


def create_assigned_work_order():

    work_order = WorkOrder(
        code="WO-001",
        title="Inspección general",
        description="Prueba.",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code="ASSET-001",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            8,
            15,
            8,
            0,
        ),
    )

    work_order.assign()

    return work_order


def test_should_start_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_assigned_work_order()
    )

    use_case = StartWorkOrder(
        repository
    )

    result = use_case.execute(
        StartWorkOrderCommand(
            code="WO-001"
        )
    )

    assert (
        result.work_order.status
        == WorkOrderStatus.IN_PROGRESS
    )


def test_should_reject_unknown_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    use_case = StartWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            StartWorkOrderCommand(
                code="WO-404"
            )
        )


def test_should_preserve_domain_transition_rules():

    repository = (
        InMemoryWorkOrderRepository()
    )

    work_order = create_assigned_work_order()

    work_order.start()

    repository.save(
        work_order
    )

    use_case = StartWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
    ):
        use_case.execute(
            StartWorkOrderCommand(
                code="WO-001"
            )
        )