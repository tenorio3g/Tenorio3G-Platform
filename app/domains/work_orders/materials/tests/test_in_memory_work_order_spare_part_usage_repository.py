from datetime import datetime

from app.domains.work_orders.materials.entities import (
    WorkOrderSparePartUsage,
)

from app.domains.work_orders.materials.repositories import (
    InMemoryWorkOrderSparePartUsageRepository,
)


def create_usage(
    work_order_code="WO-001",
    spare_part_code="SP-001",
    quantity=1,
):

    return WorkOrderSparePartUsage(
        work_order_code=work_order_code,
        spare_part_code=spare_part_code,
        quantity=quantity,
        unit_cost=10,
        used_at=datetime(
            2026,
            8,
            17,
            16,
            0,
        ),
    )


def test_should_save_usage():

    repository = (
        InMemoryWorkOrderSparePartUsageRepository()
    )

    repository.save(
        create_usage()
    )

    result = repository.list_by_work_order(
        "WO-001"
    )

    assert len(result) == 1

    assert (
        result[0].spare_part_code
        == "SP-001"
    )


def test_should_normalize_work_order_code():

    repository = (
        InMemoryWorkOrderSparePartUsageRepository()
    )

    repository.save(
        create_usage()
    )

    result = repository.list_by_work_order(
        " wo-001 "
    )

    assert len(result) == 1


def test_should_list_only_requested_work_order():

    repository = (
        InMemoryWorkOrderSparePartUsageRepository()
    )

    repository.save(
        create_usage(
            work_order_code="WO-001",
            spare_part_code="SP-001",
        )
    )

    repository.save(
        create_usage(
            work_order_code="WO-002",
            spare_part_code="SP-002",
        )
    )

    result = repository.list_by_work_order(
        "WO-001"
    )

    assert len(result) == 1

    assert (
        result[0].spare_part_code
        == "SP-001"
    )


def test_should_allow_same_spare_part_multiple_times():

    repository = (
        InMemoryWorkOrderSparePartUsageRepository()
    )

    repository.save(
        create_usage(
            quantity=2
        )
    )

    repository.save(
        create_usage(
            quantity=1
        )
    )

    result = repository.list_by_work_order(
        "WO-001"
    )

    assert len(result) == 2

    assert sum(
        usage.quantity
        for usage in result
    ) == 3