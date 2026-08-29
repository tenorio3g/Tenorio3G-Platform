from datetime import datetime

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from app.domains.operational_intelligence.queries import (
    GetWorkOrderStatusSummary,
)


def create_work_order(
    code: str,
    status: WorkOrderStatus,
) -> WorkOrder:

    return WorkOrder(
        code=code,
        title=f"Orden {code}",
        description="Prueba",
        work_type="CORRECTIVE",
        priority="MEDIUM",
        asset_code="ASSET-001",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            8,
            29,
            10,
            0,
        ),
        status=status,
    )


def test_should_calculate_work_order_status_summary():

    repository = (
        InMemoryWorkOrderRepository()
    )

    statuses = [
        WorkOrderStatus.CREATED,
        WorkOrderStatus.APPROVED,
        WorkOrderStatus.APPROVED,
        WorkOrderStatus.ASSIGNED,
        WorkOrderStatus.IN_PROGRESS,
        WorkOrderStatus.IN_PROGRESS,
        WorkOrderStatus.IN_PROGRESS,
        WorkOrderStatus.ON_HOLD,
        WorkOrderStatus.COMPLETED,
        WorkOrderStatus.COMPLETED,
        WorkOrderStatus.CLOSED,
        WorkOrderStatus.CANCELLED,
    ]

    for index, status in enumerate(
        statuses,
        start=1,
    ):
        repository.save(
            create_work_order(
                code=f"WO-{index:03d}",
                status=status,
            )
        )

    query = GetWorkOrderStatusSummary(
        work_order_repository=repository,
    )

    result = query.execute()

    assert result.created == 1
    assert result.approved == 2
    assert result.assigned == 1
    assert result.in_progress == 3
    assert result.on_hold == 1

    assert result.completed == 2
    assert result.closed == 1
    assert result.cancelled == 1

    assert result.open_total == 8
    assert result.terminal_total == 4
    assert result.total == 12


def test_should_return_zero_summary_when_no_work_orders():

    repository = (
        InMemoryWorkOrderRepository()
    )

    query = GetWorkOrderStatusSummary(
        work_order_repository=repository,
    )

    result = query.execute()

    assert result.created == 0
    assert result.approved == 0
    assert result.assigned == 0
    assert result.in_progress == 0
    assert result.on_hold == 0

    assert result.completed == 0
    assert result.closed == 0
    assert result.cancelled == 0

    assert result.open_total == 0
    assert result.terminal_total == 0
    assert result.total == 0
