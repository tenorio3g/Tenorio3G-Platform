from datetime import datetime

from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)

from app.domains.work_orders.tools.repositories import (
    InMemoryWorkOrderToolUsageRepository,
)


def create_usage(
    usage_id="TU-001",
    work_order_code="WO-001",
    tool_code="TL-001",
):

    return WorkOrderToolUsage(
        usage_id=usage_id,
        work_order_code=work_order_code,
        tool_code=tool_code,
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


def test_should_save_and_list_usage():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    usage = create_usage()

    repository.save(
        usage
    )

    result = repository.list_by_work_order(
        "WO-001"
    )

    assert len(result) == 1
    assert result[0] is usage


def test_should_filter_by_work_order():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    repository.save(
        create_usage(
            work_order_code="WO-001",
            tool_code="TL-001",
        )
    )

    repository.save(
        create_usage(
            work_order_code="WO-002",
            tool_code="TL-002",
        )
    )

    result = repository.list_by_work_order(
        "WO-001"
    )

    assert len(result) == 1

    assert (
        result[0].tool_code
        == "TL-001"
    )


def test_should_normalize_work_order_code():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    repository.save(
        create_usage()
    )

    result = repository.list_by_work_order(
        "  wo-001  "
    )

    assert len(result) == 1


def test_should_not_duplicate_same_usage_object():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    usage = create_usage()

    repository.save(
        usage
    )

    repository.save(
        usage
    )

    result = repository.list_by_work_order(
        "WO-001"
    )

    assert len(result) == 1



def test_should_get_usage_by_id():

    repository = (
        InMemoryWorkOrderToolUsageRepository()
    )

    repository.save(
        create_usage(
            usage_id="TU-001"
        )
    )

    result = repository.get_by_id(
        " tu-001 "
    )

    assert result is not None
    assert result.usage_id == "TU-001"