from datetime import datetime

from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)

from app.domains.work_orders.tools.presentation import (
    WorkOrderToolsPresenter,
)

from app.domains.work_orders.tools.repositories import (
    InMemoryWorkOrderToolUsageRepository,
)

from app.domains.work_orders.tools.use_cases import (
    ListWorkOrderTools,
    ListWorkOrderToolsQuery,
)


def test_should_list_and_present_tools():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    repository.save(
        WorkOrderToolUsage(
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
            observations="Medición.",
        )
    )

    use_case = ListWorkOrderTools(
        repository
    )

    result = use_case.execute(
        ListWorkOrderToolsQuery(
            work_order_code=" wo-001 "
        )
    )

    view_model = (
        WorkOrderToolsPresenter.present(
            result
        )
    )

    assert view_model.has_items is True
    assert view_model.total == 1
    assert view_model.issued == 1
    assert view_model.returned == 0

    item = view_model.items[0]

    assert item.usage_id == "TU-001"
    assert item.tool_code == "TL-001"
    assert item.tool_name == "Multímetro"
    assert item.quantity == 1
    assert item.status == "ISSUED"
    assert item.status_label == "Prestada"

    assert (
        item.issued_at
        == "17/08/2026 10:00"
    )

    assert item.returned_at is None


def test_should_present_returned_tool():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    usage = WorkOrderToolUsage(
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

    use_case = ListWorkOrderTools(
        repository
    )

    result = use_case.execute(
        ListWorkOrderToolsQuery(
            work_order_code="WO-001"
        )
    )

    view_model = (
        WorkOrderToolsPresenter.present(
            result
        )
    )

    assert view_model.issued == 0
    assert view_model.returned == 1

    item = view_model.items[0]

    assert item.status == "RETURNED"
    assert item.status_label == "Devuelta"

    assert (
        item.returned_at
        == "17/08/2026 12:00"
    )


def test_should_present_empty_tools():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    use_case = ListWorkOrderTools(
        repository
    )

    result = use_case.execute(
        ListWorkOrderToolsQuery(
            work_order_code="WO-001"
        )
    )

    view_model = (
        WorkOrderToolsPresenter.present(
            result
        )
    )

    assert view_model.has_items is False
    assert view_model.total == 0
    assert view_model.issued == 0
    assert view_model.returned == 0