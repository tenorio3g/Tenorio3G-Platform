from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    SQLitePreventiveMaintenanceRepository,
)


def build_repository(
    tmp_path,
):

    database_path = (
        tmp_path
        / "preventive_maintenance.db"
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
        SQLitePreventiveMaintenanceRepository(
            SessionLocal
        )
    )

    return repository, engine


def create_plan(
    code="PM-001",
    asset_code="ASSET-001",
):

    return PreventiveMaintenancePlan(
        code=code,
        asset_code=asset_code,
        title="Inspección preventiva",
        frequency_days=30,
        responsible_person_code="55464",
        next_due_at=datetime(
            2026,
            9,
            1,
            8,
            0,
        ),
        description="Plan preventivo.",
    )


def test_should_save_and_get_plan(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    repository.save(
        create_plan()
    )

    persisted = repository.get_by_code(
        "PM-001"
    )

    assert persisted is not None
    assert persisted.code == "PM-001"
    assert (
        persisted.asset_code
        == "ASSET-001"
    )

    engine.dispose()


def test_should_update_existing_plan(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    repository.save(
        create_plan()
    )

    updated = PreventiveMaintenancePlan(
        code="PM-001",
        asset_code="ASSET-001",
        title="Inspección actualizada",
        frequency_days=90,
        responsible_person_code="55464",
        next_due_at=datetime(
            2026,
            12,
            1,
        ),
        description="Actualizado.",
        is_active=False,
    )

    repository.save(
        updated
    )

    persisted = repository.get_by_code(
        "PM-001"
    )

    assert persisted is not None

    assert (
        persisted.title
        == "Inspección actualizada"
    )

    assert persisted.frequency_days == 90
    assert persisted.is_active is False

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
        create_plan(
            "PM-001",
            "ASSET-001",
        )
    )

    repository.save(
        create_plan(
            "PM-002",
            "ASSET-001",
        )
    )

    repository.save(
        create_plan(
            "PM-003",
            "ASSET-002",
        )
    )

    plans = repository.list_by_asset(
        " asset-001 "
    )

    assert len(plans) == 2

    engine.dispose()


def test_should_list_all(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    repository.save(
        create_plan(
            "PM-001"
        )
    )

    repository.save(
        create_plan(
            "PM-002"
        )
    )

    plans = repository.list_all()

    assert len(plans) == 2

    engine.dispose()


def test_should_delete_plan(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    repository.save(
        create_plan()
    )

    repository.delete(
        " pm-001 "
    )

    assert repository.get_by_code(
        "PM-001"
    ) is None

    engine.dispose()


def test_unknown_plan_should_return_none(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    result = repository.get_by_code(
        "PM-NOT-FOUND"
    )

    assert result is None

    engine.dispose()