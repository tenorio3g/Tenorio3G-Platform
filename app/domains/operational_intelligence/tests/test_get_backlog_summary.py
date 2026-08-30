from datetime import (
    datetime,
    timedelta,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from app.domains.operational_intelligence.queries import (
    GetBacklogSummary,
    WorkOrderAgingItem,
)


BASE_DATE = datetime(
    2026,
    8,
    29,
    8,
    0,
)


def create_aging_item(
    code: str,
    status: WorkOrderStatus,
    age: timedelta,
) -> WorkOrderAgingItem:

    created_at = BASE_DATE - age

    return WorkOrderAgingItem(
        work_order_code=code,
        status=status,
        created_at=created_at,
        status_since=created_at,
        age=age,
        time_in_current_status=age,
    )


def test_should_return_empty_backlog_summary():

    query = GetBacklogSummary()

    result = query.execute(
        items=[]
    )

    assert result.total_open == 0

    assert result.created == 0
    assert result.approved == 0
    assert result.assigned == 0
    assert result.in_progress == 0
    assert result.on_hold == 0

    assert result.average_age is None
    assert result.oldest_age is None


def test_should_count_backlog_by_status():

    items = [
        create_aging_item(
            "WO-001",
            WorkOrderStatus.CREATED,
            timedelta(days=1),
        ),
        create_aging_item(
            "WO-002",
            WorkOrderStatus.APPROVED,
            timedelta(days=2),
        ),
        create_aging_item(
            "WO-003",
            WorkOrderStatus.APPROVED,
            timedelta(days=3),
        ),
        create_aging_item(
            "WO-004",
            WorkOrderStatus.ASSIGNED,
            timedelta(days=4),
        ),
        create_aging_item(
            "WO-005",
            WorkOrderStatus.IN_PROGRESS,
            timedelta(days=5),
        ),
        create_aging_item(
            "WO-006",
            WorkOrderStatus.IN_PROGRESS,
            timedelta(days=6),
        ),
        create_aging_item(
            "WO-007",
            WorkOrderStatus.ON_HOLD,
            timedelta(days=7),
        ),
    ]

    query = GetBacklogSummary()

    result = query.execute(
        items=items
    )

    assert result.total_open == 7

    assert result.created == 1
    assert result.approved == 2
    assert result.assigned == 1
    assert result.in_progress == 2
    assert result.on_hold == 1


def test_should_calculate_average_backlog_age():

    items = [
        create_aging_item(
            "WO-001",
            WorkOrderStatus.CREATED,
            timedelta(days=1),
        ),
        create_aging_item(
            "WO-002",
            WorkOrderStatus.ASSIGNED,
            timedelta(days=3),
        ),
        create_aging_item(
            "WO-003",
            WorkOrderStatus.IN_PROGRESS,
            timedelta(days=5),
        ),
    ]

    query = GetBacklogSummary()

    result = query.execute(
        items=items
    )

    assert result.average_age == timedelta(
        days=3
    )


def test_should_return_oldest_backlog_age():

    items = [
        create_aging_item(
            "WO-001",
            WorkOrderStatus.CREATED,
            timedelta(hours=12),
        ),
        create_aging_item(
            "WO-002",
            WorkOrderStatus.APPROVED,
            timedelta(days=8),
        ),
        create_aging_item(
            "WO-003",
            WorkOrderStatus.ON_HOLD,
            timedelta(days=3),
        ),
    ]

    query = GetBacklogSummary()

    result = query.execute(
        items=items
    )

    assert result.oldest_age == timedelta(
        days=8
    )
