from datetime import datetime

import pytest

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.use_cases import (
    CancelWorkOrder,
    CancelWorkOrderCommand,
    CloseWorkOrder,
    CloseWorkOrderCommand,
    CompleteWorkOrder,
    CompleteWorkOrderCommand,
    HoldWorkOrder,
    HoldWorkOrderCommand,
    ResumeWorkOrder,
    ResumeWorkOrderCommand,
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


def lifecycle_command(
    command_class,
    code="WO-001",
):

    return command_class(
        code=code,
        actor_person_code="55464",
        occurred_at=datetime(
            2026,
            8,
            20,
            14,
            0,
        ),
    )


def test_should_hold_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    work_order = create_work_order()

    work_order.assign()
    work_order.start()

    repository.save(
        work_order
    )

    use_case = HoldWorkOrder(
        repository
    )

    result = use_case.execute(
        lifecycle_command(
            HoldWorkOrderCommand
        )
    )

    assert (
        result.work_order.status
        == WorkOrderStatus.ON_HOLD
    )


def test_should_resume_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    work_order = create_work_order()

    work_order.assign()
    work_order.start()
    work_order.hold()

    repository.save(
        work_order
    )

    use_case = ResumeWorkOrder(
        repository
    )

    result = use_case.execute(
        lifecycle_command(
            ResumeWorkOrderCommand
        )
    )

    assert (
        result.work_order.status
        == WorkOrderStatus.IN_PROGRESS
    )


def test_should_complete_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    work_order = create_work_order()

    work_order.assign()
    work_order.start()

    repository.save(
        work_order
    )

    use_case = CompleteWorkOrder(
        repository
    )

    result = use_case.execute(
        lifecycle_command(
            CompleteWorkOrderCommand
        )
    )

    assert (
        result.work_order.status
        == WorkOrderStatus.COMPLETED
    )


def test_should_close_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    work_order = create_work_order()

    work_order.assign()
    work_order.start()
    work_order.complete()

    repository.save(
        work_order
    )

    use_case = CloseWorkOrder(
        repository
    )

    result = use_case.execute(
        lifecycle_command(
            CloseWorkOrderCommand
        )
    )

    assert (
        result.work_order.status
        == WorkOrderStatus.CLOSED
    )


def test_should_cancel_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order()
    )

    use_case = CancelWorkOrder(
        repository
    )

    result = use_case.execute(
        lifecycle_command(
            CancelWorkOrderCommand
        )
    )

    assert (
        result.work_order.status
        == WorkOrderStatus.CANCELLED
    )


@pytest.mark.parametrize(
    "use_case_class, command_class",
    [
        (
            HoldWorkOrder,
            HoldWorkOrderCommand,
        ),
        (
            ResumeWorkOrder,
            ResumeWorkOrderCommand,
        ),
        (
            CompleteWorkOrder,
            CompleteWorkOrderCommand,
        ),
        (
            CloseWorkOrder,
            CloseWorkOrderCommand,
        ),
        (
            CancelWorkOrder,
            CancelWorkOrderCommand,
        ),
    ],
)
def test_should_reject_unknown_work_order(
    use_case_class,
    command_class,
):

    repository = (
        InMemoryWorkOrderRepository()
    )

    use_case = use_case_class(
        repository
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            lifecycle_command(
                command_class,
                code="WO-404",
            )
        )