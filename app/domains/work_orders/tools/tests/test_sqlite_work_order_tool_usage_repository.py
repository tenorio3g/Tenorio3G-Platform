from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)

from app.domains.work_orders.tools.repositories import (
    SQLiteWorkOrderToolUsageRepository,
)

from app.domains.work_orders.tools.value_objects import (
    ToolUsageStatus,
)


def create_repository():

    engine = create_engine(
        "sqlite:///:memory:"
    )

    Base.metadata.create_all(
        engine
    )

    session_factory = sessionmaker(
        bind=engine
    )

    return SQLiteWorkOrderToolUsageRepository(
        session_factory
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
        observations="Uso eléctrico.",
    )


def test_should_save_and_list_usage():

    repository = create_repository()

    repository.save(
        create_usage()
    )

    result = repository.list_by_work_order(
        "WO-001"
    )

    assert len(result) == 1

    usage = result[0]

    assert usage.usage_id == "TU-001"
    assert usage.tool_code == "TL-001"
    assert usage.tool_name == "Multímetro"
    assert usage.quantity == 1

    assert (
        usage.status
        == ToolUsageStatus.ISSUED
    )


def test_should_update_returned_usage():

    repository = create_repository()

    usage = create_usage()

    repository.save(
        usage
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

    result = repository.list_by_work_order(
        "WO-001"
    )

    persisted = result[0]

    assert (
        persisted.status
        == ToolUsageStatus.RETURNED
    )

    assert (
        persisted.returned_at
        == datetime(
            2026,
            8,
            17,
            12,
            0,
        )
    )


def test_should_filter_by_work_order():

    repository = create_repository()

    repository.save(
        create_usage()
    )

    repository.save(
        WorkOrderToolUsage(
            usage_id="TU-002",
            work_order_code="WO-002",
            tool_code="TL-002",
            tool_name="Pinza amperimétrica",
            quantity=1,
            issued_at=datetime(
                2026,
                8,
                17,
                11,
                0,
            ),
        )
    )

    result = repository.list_by_work_order(
        " wo-001 "
    )

    assert len(result) == 1
    assert result[0].usage_id == "TU-001"


def test_should_return_empty_list():

    repository = create_repository()

    result = repository.list_by_work_order(
        "WO-NOT-FOUND"
    )

    assert result == []
def test_should_get_usage_by_id():

    repository = create_repository()

    repository.save(
        create_usage()
    )

    result = repository.get_by_id(
        " tu-001 "
    )

    assert result is not None
    assert result.usage_id == "TU-001"
