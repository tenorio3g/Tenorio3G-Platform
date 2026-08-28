from datetime import datetime

import pytest

from app.foundation.timeline.engine.repositories import (
    InMemoryTimelineEventRepository,
)

from app.foundation.timeline.engine.use_cases import (
    RecordTimelineEvent,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.timeline import (
    WorkOrderTimelineRecorder,
)

from app.domains.work_orders.use_cases import (
    CloseWorkOrder,
    CloseWorkOrderCommand,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


def create_completed_work_order():

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

    work_order.approve()
    work_order.assign()
    work_order.start()
    work_order.complete()

    return work_order


def create_close_command(
    code="WO-001",
):

    return CloseWorkOrderCommand(
        code=code,
        actor_person_code="55464",
        occurred_at=datetime(
            2026,
            8,
            20,
            12,
            0,
        ),
    )


def test_should_close_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_completed_work_order()
    )

    use_case = CloseWorkOrder(
        repository
    )

    result = use_case.execute(
        create_close_command()
    )

    assert (
        result.work_order.status
        == WorkOrderStatus.CLOSED
    )

    persisted = repository.get_by_code(
        "WO-001"
    )

    assert (
        persisted.status
        == WorkOrderStatus.CLOSED
    )


def test_should_reject_unknown_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    use_case = CloseWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            create_close_command(
                code="WO-404"
            )
        )


def test_should_preserve_domain_transition_rules():

    repository = (
        InMemoryWorkOrderRepository()
    )

    work_order = (
        create_completed_work_order()
    )

    work_order.close()

    repository.save(
        work_order
    )

    use_case = CloseWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
    ):
        use_case.execute(
            create_close_command()
        )


def test_should_record_closed_event():

    repository = (
        InMemoryWorkOrderRepository()
    )

    timeline_repository = (
        InMemoryTimelineEventRepository()
    )

    record_timeline_event = (
        RecordTimelineEvent(
            timeline_repository
        )
    )

    timeline_recorder = (
        WorkOrderTimelineRecorder(
            record_timeline_event
        )
    )

    repository.save(
        create_completed_work_order()
    )

    use_case = CloseWorkOrder(
        repository,
        timeline_recorder,
    )

    occurred_at = datetime(
        2026,
        8,
        20,
        12,
        30,
    )

    result = use_case.execute(
        CloseWorkOrderCommand(
            code="WO-001",
            actor_person_code="55464",
            occurred_at=occurred_at,
        )
    )

    events = (
        timeline_repository
        .list_by_entity(
            "WORK_ORDER",
            result.work_order.code,
        )
    )

    assert len(events) == 1

    event = events[0]

    assert (
        event.event_type
        == "WORK_ORDER_CLOSED"
    )

    assert (
        event.entity_type
        == "WORK_ORDER"
    )

    assert (
        event.entity_code
        == "WO-001"
    )

    assert (
        event.actor_person_code
        == "55464"
    )

    assert (
        event.occurred_at
        == occurred_at
    )

    assert (
        event.reference_type
        == "WORK_ORDER"
    )

    assert (
        event.reference_code
        == "WO-001"
    )
