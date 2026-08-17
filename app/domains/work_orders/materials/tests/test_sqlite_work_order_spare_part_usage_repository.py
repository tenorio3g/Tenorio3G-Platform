from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.work_orders.materials.entities import (
    WorkOrderSparePartUsage,
)

from app.domains.work_orders.materials.repositories import (
    SQLiteWorkOrderSparePartUsageRepository,
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

    return (
        SQLiteWorkOrderSparePartUsageRepository(
            session_factory
        )
    )


def create_usage(
    quantity=2,
    used_at=None,
):

    return WorkOrderSparePartUsage(
        work_order_code="WO-001",
        spare_part_code="SP-001",
        quantity=quantity,
        unit_cost=12.5,
        used_at=(
            used_at
            or datetime(
                2026,
                8,
                17,
                10,
                30,
            )
        ),
        observations="Cambio de refacción.",
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

    assert usage.work_order_code == "WO-001"
    assert usage.spare_part_code == "SP-001"
    assert usage.quantity == 2
    assert usage.unit_cost == 12.5
    assert usage.total_cost == 25
    assert usage.observations == "Cambio de refacción."


def test_should_normalize_work_order_code():

    repository = create_repository()

    repository.save(
        create_usage()
    )

    result = repository.list_by_work_order(
        " wo-001 "
    )

    assert len(result) == 1


def test_should_allow_same_spare_part_multiple_times():

    repository = create_repository()

    repository.save(
        create_usage(
            quantity=2,
            used_at=datetime(
                2026,
                8,
                17,
                10,
                0,
            ),
        )
    )

    repository.save(
        create_usage(
            quantity=1,
            used_at=datetime(
                2026,
                8,
                17,
                14,
                0,
            ),
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


def test_should_return_empty_list_when_no_usages():

    repository = create_repository()

    result = repository.list_by_work_order(
        "WO-NOT-FOUND"
    )

    assert result == []