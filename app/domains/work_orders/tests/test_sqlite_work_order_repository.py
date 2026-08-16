from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    SQLiteWorkOrderRepository,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


def build_repository(
    tmp_path,
):

    database_path = (
        tmp_path
        / "work_orders_test.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}",
        future=True,
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(
        engine
    )

    repository = (
        SQLiteWorkOrderRepository(
            SessionLocal
        )
    )

    return repository, engine


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


def test_should_save_and_get_work_order(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    repository.save(
        create_work_order()
    )

    persisted = repository.get_by_code(
        "WO-001"
    )

    assert persisted is not None
    assert persisted.code == "WO-001"
    assert persisted.status == WorkOrderStatus.CREATED

    engine.dispose()


def test_should_persist_status_changes(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    work_order = create_work_order()

    repository.save(
        work_order
    )

    work_order.assign()
    work_order.start()

    repository.save(
        work_order
    )

    persisted = repository.get_by_code(
        "WO-001"
    )

    assert persisted is not None

    assert (
        persisted.status
        == WorkOrderStatus.IN_PROGRESS
    )

    engine.dispose()


def test_should_list_by_asset(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
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

    engine.dispose()


def test_should_delete_work_order(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    repository.save(
        create_work_order()
    )

    repository.delete(
        "WO-001"
    )

    assert (
        repository.get_by_code(
            "WO-001"
        )
        is None
    )

    engine.dispose()