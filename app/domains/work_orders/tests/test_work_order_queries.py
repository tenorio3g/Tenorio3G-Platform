from datetime import datetime

import pytest

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.use_cases import (
    GetWorkOrder,
    GetWorkOrderQuery,
    ListWorkOrders,
    ListWorkOrdersByAsset,
    ListWorkOrdersByAssetQuery,
)


def create_work_order(
    code="WO-001",
    asset_code="ASSET-001",
):

    return WorkOrder(
        code=code,
        title="Inspección general",
        description="Prueba.",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code=asset_code,
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


def test_should_get_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order()
    )

    use_case = GetWorkOrder(
        repository
    )

    result = use_case.execute(
        GetWorkOrderQuery(
            code=" wo-001 "
        )
    )

    assert (
        result.work_order.code
        == "WO-001"
    )


def test_should_reject_unknown_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    use_case = GetWorkOrder(
        repository
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            GetWorkOrderQuery(
                code="WO-404"
            )
        )


def test_should_list_all_work_orders():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order(
            code="WO-001"
        )
    )

    repository.save(
        create_work_order(
            code="WO-002"
        )
    )

    use_case = ListWorkOrders(
        repository
    )

    result = use_case.execute()

    assert len(
        result.work_orders
    ) == 2


def test_should_list_work_orders_by_asset():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order(
            code="WO-001",
            asset_code="ASSET-001",
        )
    )

    repository.save(
        create_work_order(
            code="WO-002",
            asset_code="ASSET-001",
        )
    )

    repository.save(
        create_work_order(
            code="WO-003",
            asset_code="ASSET-002",
        )
    )

    use_case = ListWorkOrdersByAsset(
        repository
    )

    result = use_case.execute(
        ListWorkOrdersByAssetQuery(
            asset_code=" asset-001 "
        )
    )

    assert len(
        result.work_orders
    ) == 2

    assert {
        work_order.code
        for work_order
        in result.work_orders
    } == {
        "WO-001",
        "WO-002",
    }