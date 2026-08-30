from datetime import datetime, timedelta

from app.domains.work_orders.entities import WorkOrder
from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)
from app.foundation.timeline.engine.entities import TimelineEvent
from app.foundation.timeline.engine.repositories import (
    InMemoryTimelineEventRepository,
)
from app.foundation.timeline.engine.use_cases import (
    ListTimelineEvents,
)

from app.domains.operational_intelligence.queries import (
    GetApprovalLeadTime,
)


def create_work_order(
    code: str,
    created_at: datetime,
) -> WorkOrder:

    return WorkOrder(
        code=code,
        title=f"Orden {code}",
        description="Prueba",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code="ASSET-001",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=created_at,
    )


def create_approval_event(
    event_id: str,
    work_order_code: str,
    occurred_at: datetime,
) -> TimelineEvent:

    return TimelineEvent(
        event_id=event_id,
        entity_type="WORK_ORDER",
        entity_code=work_order_code,
        event_type="WORK_ORDER_APPROVED",
        title="Orden aprobada",
        actor_person_code="SUP-001",
        occurred_at=occurred_at,
        reference_type="WORK_ORDER",
        reference_code=work_order_code,
    )


def test_should_calculate_approval_lead_time():

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
        21,
        14,
        0,
    )

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    timeline_repository = (
        InMemoryTimelineEventRepository()
    )

    work_order_repository.save(
        create_work_order(
            code="WO-001",
            created_at=created_at,
        )
    )

    timeline_repository.save(
        create_approval_event(
            event_id="EVT-001",
            work_order_code="WO-001",
            occurred_at=approved_at,
        )
    )

    query = GetApprovalLeadTime(
        work_order_repository=
            work_order_repository,
        list_timeline_events=
            ListTimelineEvents(
                repository=
                    timeline_repository,
            ),
    )

    result = query.execute()

    assert len(result) == 1

    item = result[0]

    assert item.work_order_code == "WO-001"
    assert item.created_at == created_at
    assert item.approved_at == approved_at

    assert item.lead_time == timedelta(
        days=1,
        hours=6,
    )


def test_should_exclude_work_order_without_approval_event():

    created_at = datetime(
        2026,
        8,
        20,
        8,
        0,
    )

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    timeline_repository = (
        InMemoryTimelineEventRepository()
    )

    work_order_repository.save(
        create_work_order(
            code="WO-001",
            created_at=created_at,
        )
    )

    query = GetApprovalLeadTime(
        work_order_repository=
            work_order_repository,
        list_timeline_events=
            ListTimelineEvents(
                repository=
                    timeline_repository,
            ),
    )

    result = query.execute()

    assert result == []
