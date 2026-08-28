from datetime import datetime

import pytest

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.timeline import (
    WorkOrderTimelineRecorder,
)

from app.domains.work_orders.use_cases.approve_work_order import (
    ApproveWorkOrder,
    ApproveWorkOrderCommand,
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


def create_command(
    code="WO-APPROVE-001",
):

    return ApproveWorkOrderCommand(
        code=code,
        actor_person_code="55464",
        occurred_at=datetime(
            2026,
            8,
            24,
            9,
            0,
        ),
    )


def test_should_approve_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order()
    )

    use_case = ApproveWorkOrder(
        repository
    )

    result = use_case.execute(
        create_command()
    )

    assert (
        result.work_order.status
        == WorkOrderStatus.APPROVED
    )

    persisted = repository.get_by_code(
        "WO-APPROVE-001"
    )

    assert (
        persisted.status
        == WorkOrderStatus.APPROVED
    )


def test_should_reject_unknown_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    use_case = ApproveWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            create_command(
                code="WO-404"
            )
        )


def test_should_preserve_domain_transition_rules():

    repository = (
        InMemoryWorkOrderRepository()
    )

    work_order = create_work_order()

    work_order.approve()

    repository.save(
        work_order
    )

    use_case = ApproveWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
        match=(
            "work order cannot be approved "
            "from current status"
        ),
    ):
        use_case.execute(
            create_command()
        )


def test_should_record_approved_event():

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
        create_work_order()
    )

    use_case = ApproveWorkOrder(
        repository,
        timeline_recorder,
    )

    occurred_at = datetime(
        2026,
        8,
        24,
        9,
        30,
    )

    result = use_case.execute(
        ApproveWorkOrderCommand(
            code="WO-APPROVE-001",
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
        == "WORK_ORDER_APPROVED"
    )

    assert (
        event.actor_person_code
        == "55464"
    )

    assert (
        event.occurred_at
        == occurred_at
    )
