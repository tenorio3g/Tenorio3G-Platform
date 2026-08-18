from datetime import datetime

import pytest

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.tools.repositories import (
    InMemoryWorkOrderToolUsageRepository,
)

from app.domains.work_orders.tools.use_cases import (
    IssueToolToWorkOrder,
    IssueToolToWorkOrderCommand,
)

from app.domains.work_orders.tools.value_objects import (
    ToolUsageStatus,
)


def create_work_order():

    return WorkOrder(
        code="WO-001",
        title="Revisión eléctrica",
        description="Inspección de tablero",
        work_type="CORRECTIVE",
        priority="HIGH",
        asset_code="ASSET-001",
        requester_person_code="P-001",
        supervisor_person_code="P-002",
        created_at=datetime(
            2026,
            8,
            17,
            8,
            0,
        ),
    )


def test_should_issue_tool_to_existing_work_order():

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    tool_repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    work_order_repository.save(
        create_work_order()
    )

    use_case = IssueToolToWorkOrder(
        tool_repository,
        work_order_repository,
    )

    result = use_case.execute(
        IssueToolToWorkOrderCommand(
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
            observations="Medición de voltaje.",
        )
    )

    assert result.usage.usage_id == "TU-001"

    assert (
        result.usage.status
        == ToolUsageStatus.ISSUED
    )

    usages = (
        tool_repository
        .list_by_work_order(
            "WO-001"
        )
    )

    assert len(usages) == 1

    assert (
        usages[0].tool_code
        == "TL-001"
    )


def test_should_reject_unknown_work_order():

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    tool_repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    use_case = IssueToolToWorkOrder(
        tool_repository,
        work_order_repository,
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            IssueToolToWorkOrderCommand(
                usage_id="TU-001",
                work_order_code="WO-NOT-FOUND",
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
        )