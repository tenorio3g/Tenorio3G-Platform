from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
)

from app.domains.assets.preventive_maintenance.repositories import (
    SQLitePreventiveMaintenanceExecutionRepository,
)


def build_repository(
    tmp_path,
):

    database_path = (
        tmp_path
        / "preventive_maintenance_execution.db"
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
        SQLitePreventiveMaintenanceExecutionRepository(
            SessionLocal
        )
    )

    return repository, engine


def create_execution(
    code="PME-001",
    plan_code="PM-001",
    asset_code="ASSET-001",
):

    return PreventiveMaintenanceExecution(
        code=code,
        plan_code=plan_code,
        asset_code=asset_code,
        performed_by="Fortunato Tenorio",
        scheduled_at=datetime(
            2026,
            9,
            1,
            8,
            0,
        ),
        completed_at=datetime(
            2026,
            9,
            1,
            10,
            0,
        ),
        observations="Sin anomalías.",
    )


def test_should_save_and_get_execution(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    repository.save(
        create_execution()
    )

    persisted = repository.get_by_code(
        "PME-001"
    )

    assert persisted is not None
    assert persisted.code == "PME-001"
    assert persisted.plan_code == "PM-001"

    engine.dispose()


def test_should_list_by_plan(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    repository.save(
        create_execution(
            code="PME-001",
            plan_code="PM-001",
        )
    )

    repository.save(
        create_execution(
            code="PME-002",
            plan_code="PM-001",
        )
    )

    repository.save(
        create_execution(
            code="PME-003",
            plan_code="PM-002",
        )
    )

    executions = repository.list_by_plan(
        " pm-001 "
    )

    assert len(executions) == 2

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
        create_execution(
            code="PME-001",
            asset_code="ASSET-001",
        )
    )

    repository.save(
        create_execution(
            code="PME-002",
            asset_code="ASSET-001",
        )
    )

    repository.save(
        create_execution(
            code="PME-003",
            asset_code="ASSET-002",
        )
    )

    executions = repository.list_by_asset(
        " asset-001 "
    )

    assert len(executions) == 2

    engine.dispose()


def test_unknown_execution_should_return_none(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    result = repository.get_by_code(
        "PME-NOT-FOUND"
    )

    assert result is None

    engine.dispose()