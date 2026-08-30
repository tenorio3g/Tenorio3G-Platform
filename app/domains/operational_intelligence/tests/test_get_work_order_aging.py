from datetime import (
    datetime,
    timedelta,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)

from app.foundation.timeline.engine.repositories import (
    InMemoryTimelineEventRepository,
)

from app.foundation.timeline.engine.use_cases import (
    ListTimelineEvents,
)

from app.domains.operational_intelligence.queries import (
    GetWorkOrderAging,
)


def create_work_order(
    code: str,
    status: WorkOrderStatus,
    created_at: datetime,
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
        created_at=created_at,
        status=status,
    )


def create_timeline_event(
    event_id: str,
    work_order_code: str,
    event_type: str,
    occurred_at: datetime,
) -> TimelineEvent:

    return TimelineEvent(
        event_id=event_id,
        entity_type="WORK_ORDER",
        entity_code=work_order_code,
        event_type=event_type,
        title=event_type,
        actor_person_code="SUP-001",
        occurred_at=occurred_at,
    )


def create_query(
    work_orders,
    timeline_events=(),
):

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    for work_order in work_orders:
        work_order_repository.save(
            work_order
        )

    timeline_repository = (
        InMemoryTimelineEventRepository()
    )

    for event in timeline_events:
        timeline_repository.save(
            event
        )

    return GetWorkOrderAging(
        work_order_repository=(
            work_order_repository
        ),
        list_timeline_events=(
            ListTimelineEvents(
                timeline_repository
            )
        ),
    )


def test_should_calculate_created_work_order_aging():

    created_at = datetime(
        2026,
        8,
        20,
        8,
        0,
    )

    now = datetime(
        2026,
        8,
        29,
        8,
        0,
    )

    query = create_query(
        [
            create_work_order(
                code="WO-001",
                status=WorkOrderStatus.CREATED,
                created_at=created_at,
            )
        ]
    )

    result = query.execute(
        now=now
    )

    assert len(result) == 1

    item = result[0]

    assert item.work_order_code == "WO-001"
    assert item.status == WorkOrderStatus.CREATED

    assert item.created_at == created_at
    assert item.status_since == created_at

    assert item.age == timedelta(
        days=9
    )

    assert (
        item.time_in_current_status
        == timedelta(days=9)
    )


def test_should_use_approved_timeline_event_as_status_since():

    created_at = datetime(
        2026,
        8,
        20,
        8,
        0,
    )

    approved_at = datetime(
        2026,
        8,
        22,
        10,
        0,
    )

    now = datetime(
        2026,
        8,
        29,
        10,
        0,
    )

    query = create_query(
        [
            create_work_order(
                code="WO-002",
                status=WorkOrderStatus.APPROVED,
                created_at=created_at,
            )
        ],
        [
            create_timeline_event(
                event_id="EVT-001",
                work_order_code="WO-002",
                event_type="WORK_ORDER_APPROVED",
                occurred_at=approved_at,
            )
        ],
    )

    result = query.execute(
        now=now
    )

    item = result[0]

    assert item.status_since == approved_at

    assert (
        item.time_in_current_status
        == timedelta(days=7)
    )

    assert item.age == timedelta(
        days=9,
        hours=2,
    )


def test_should_use_latest_start_or_resume_for_in_progress():

    created_at = datetime(
        2026,
        8,
        20,
        8,
        0,
    )

    started_at = datetime(
        2026,
        8,
        22,
        8,
        0,
    )

    held_at = datetime(
        2026,
        8,
        23,
        8,
        0,
    )

    resumed_at = datetime(
        2026,
        8,
        24,
        8,
        0,
    )

    now = datetime(
        2026,
        8,
        29,
        8,
        0,
    )

    query = create_query(
        [
            create_work_order(
                code="WO-003",
                status=WorkOrderStatus.IN_PROGRESS,
                created_at=created_at,
            )
        ],
        [
            create_timeline_event(
                event_id="EVT-001",
                work_order_code="WO-003",
                event_type="WORK_ORDER_STARTED",
                occurred_at=started_at,
            ),
            create_timeline_event(
                event_id="EVT-002",
                work_order_code="WO-003",
                event_type="WORK_ORDER_HELD",
                occurred_at=held_at,
            ),
            create_timeline_event(
                event_id="EVT-003",
                work_order_code="WO-003",
                event_type="WORK_ORDER_RESUMED",
                occurred_at=resumed_at,
            ),
        ],
    )

    result = query.execute(
        now=now
    )

    item = result[0]

    assert item.status_since == resumed_at

    assert (
        item.time_in_current_status
        == timedelta(days=5)
    )


def test_should_not_invent_status_since_when_event_is_missing():

    created_at = datetime(
        2026,
        8,
        20,
        8,
        0,
    )

    now = datetime(
        2026,
        8,
        29,
        8,
        0,
    )

    query = create_query(
        [
            create_work_order(
                code="WO-004",
                status=WorkOrderStatus.ASSIGNED,
                created_at=created_at,
            )
        ]
    )

    result = query.execute(
        now=now
    )

    item = result[0]

    assert item.age == timedelta(
        days=9
    )

    assert item.status_since is None
    assert item.time_in_current_status is None


def test_should_exclude_terminal_work_orders():

    created_at = datetime(
        2026,
        8,
        20,
        8,
        0,
    )

    now = datetime(
        2026,
        8,
        29,
        8,
        0,
    )

    query = create_query(
        [
            create_work_order(
                code="WO-005",
                status=WorkOrderStatus.COMPLETED,
                created_at=created_at,
            ),
            create_work_order(
                code="WO-006",
                status=WorkOrderStatus.CLOSED,
                created_at=created_at,
            ),
            create_work_order(
                code="WO-007",
                status=WorkOrderStatus.CANCELLED,
                created_at=created_at,
            ),
        ]
    )

    result = query.execute(
        now=now
    )

    assert result == []
