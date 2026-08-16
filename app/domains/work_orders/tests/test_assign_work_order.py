from datetime import datetime

import pytest

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.use_cases import (
    AssignWorkOrder,
    AssignWorkOrderCommand,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


def create_work_order():

    return WorkOrder(
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


def test_should_assign_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order()
    )

    use_case = AssignWorkOrder(
        repository
    )

    result = use_case.execute(
        AssignWorkOrderCommand(
            code="WO-001"
        )
    )

    assert (
        result.work_order.status
        == WorkOrderStatus.ASSIGNED
    )

    persisted = repository.get_by_code(
        "WO-001"
    )

    assert (
        persisted.status
        == WorkOrderStatus.ASSIGNED
    )


def test_should_reject_unknown_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    use_case = AssignWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            AssignWorkOrderCommand(
                code="WO-404"
            )
        )


def test_should_preserve_domain_transition_rules():

    repository = (
        InMemoryWorkOrderRepository()
    )

    work_order = create_work_order()

    work_order.assign()

    repository.save(
        work_order
    )

    use_case = AssignWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
    ):
        use_case.execute(
            AssignWorkOrderCommand(
                code="WO-001"
            )
        )