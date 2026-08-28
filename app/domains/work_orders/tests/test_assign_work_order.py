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
from app.foundation.timeline.engine.repositories import (
    InMemoryTimelineEventRepository,
)

from app.foundation.timeline.engine.use_cases import (
    RecordTimelineEvent,
)

from app.domains.work_orders.timeline import (
    WorkOrderTimelineRecorder,
)
def create_work_order(
    approved=False,
):

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

    if approved:
        work_order.approve()

    return work_order


def test_should_assign_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order(
            approved=True
        )
    )

    use_case = AssignWorkOrder(
        repository
    )

    result = use_case.execute(
        AssignWorkOrderCommand(
            code="WO-001",
            actor_person_code="55464",
            occurred_at=datetime(
                2026,
                8,
                19,
                18,
                0,
            ),
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
                code="WO-404",
                actor_person_code="55464",
                occurred_at=datetime(
                    2026,
                    8,
                    19,
                    18,
                    0,
                ),
            )
        )


def test_should_preserve_domain_transition_rules():

    repository = (
        InMemoryWorkOrderRepository()
    )

    work_order = create_work_order(
        approved=True
    )

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
                code="WO-001",
                actor_person_code="55464",
                occurred_at=datetime(
                    2026,
                    8,
                    19,
                    18,
                    0,
                ),
            )
        )

def test_should_record_assigned_event():

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
        create_work_order(
            approved=True
        )
    )

    use_case = AssignWorkOrder(
        repository,
        timeline_recorder,
    )

    occurred_at = datetime(
        2026,
        8,
        19,
        18,
        30,
    )

    result = use_case.execute(
        AssignWorkOrderCommand(
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
        == "WORK_ORDER_ASSIGNED"
    )

    assert (
        event.actor_person_code
        == "55464"
    )

    assert (
        event.occurred_at
        == occurred_at
    )


def test_should_reject_assignment_before_approval():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order()
    )

    use_case = AssignWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
        match=(
            "work order cannot be assigned "
            "from current status"
        ),
    ):
        use_case.execute(
            AssignWorkOrderCommand(
                code="WO-001",
                actor_person_code="55464",
                occurred_at=datetime(
                    2026,
                    8,
                    19,
                    18,
                    0,
                ),
            )
        )
