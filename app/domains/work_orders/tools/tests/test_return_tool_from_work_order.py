from datetime import datetime

import pytest

from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)

from app.domains.work_orders.tools.repositories import (
    InMemoryWorkOrderToolUsageRepository,
)

from app.domains.work_orders.tools.use_cases import (
    ReturnToolFromWorkOrder,
    ReturnToolFromWorkOrderCommand,
)

from app.domains.work_orders.tools.value_objects import (
    ToolUsageStatus,
)


def create_usage():

    return WorkOrderToolUsage(
        usage_id="TU-001",
        work_order_code="WO-001",
        tool_code="TL-001",
        tool_name="Multímetro",
        quantity=1,
        issued_at=datetime(
            2026,
            8,
            17,
            10,
            0,
        ),
    )


def test_should_return_tool():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    repository.save(
        create_usage()
    )

    use_case = ReturnToolFromWorkOrder(
        repository
    )

    returned_at = datetime(
        2026,
        8,
        17,
        12,
        0,
    )

    result = use_case.execute(
        ReturnToolFromWorkOrderCommand(
            usage_id="TU-001",
            returned_at=returned_at,
        )
    )

    assert (
        result.usage.status
        == ToolUsageStatus.RETURNED
    )

    assert (
        result.usage.returned_at
        == returned_at
    )

    persisted = repository.get_by_id(
        "TU-001"
    )

    assert (
        persisted.status
        == ToolUsageStatus.RETURNED
    )


def test_should_reject_unknown_usage():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    use_case = ReturnToolFromWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
        match="tool usage not found",
    ):
        use_case.execute(
            ReturnToolFromWorkOrderCommand(
                usage_id="TU-NOT-FOUND",
                returned_at=datetime(
                    2026,
                    8,
                    17,
                    12,
                    0,
                ),
            )
        )


def test_should_reject_return_twice():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    usage = create_usage()

    usage.return_tool(
        datetime(
            2026,
            8,
            17,
            12,
            0,
        )
    )

    repository.save(
        usage
    )

    use_case = ReturnToolFromWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
        match=(
            "tool usage cannot be returned "
            "from current status"
        ),
    ):
        use_case.execute(
            ReturnToolFromWorkOrderCommand(
                usage_id="TU-001",
                returned_at=datetime(
                    2026,
                    8,
                    17,
                    13,
                    0,
                ),
            )
        )