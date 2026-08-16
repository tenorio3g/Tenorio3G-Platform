from datetime import datetime

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
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


def test_should_save_and_get_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order()
    )

    work_order = repository.get_by_code(
        "WO-001"
    )

    assert work_order is not None
    assert work_order.code == "WO-001"


def test_get_by_code_should_normalize_code():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order()
    )

    work_order = repository.get_by_code(
        " wo-001 "
    )

    assert work_order is not None
    assert work_order.code == "WO-001"


def test_should_list_all_work_orders():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order(
            code="WO-001",
        )
    )

    repository.save(
        create_work_order(
            code="WO-002",
        )
    )

    result = repository.list_all()

    assert len(result) == 2


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

    result = repository.list_by_asset(
        " asset-001 "
    )

    assert len(result) == 2

    assert {
        item.code
        for item in result
    } == {
        "WO-001",
        "WO-002",
    }


def test_should_delete_work_order():

    repository = (
        InMemoryWorkOrderRepository()
    )

    repository.save(
        create_work_order()
    )

    repository.delete(
        " wo-001 "
    )

    assert (
        repository.get_by_code(
            "WO-001"
        )
        is None
    )