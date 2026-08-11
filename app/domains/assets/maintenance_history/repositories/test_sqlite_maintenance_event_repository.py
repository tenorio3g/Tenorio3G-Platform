from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.repositories import (
    SQLiteMaintenanceEventRepository,
)


def create_repository(
    tmp_path,
) -> SQLiteMaintenanceEventRepository:

    database_path = (
        tmp_path
        / "maintenance_history_test.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}",
        echo=False,
        future=True,
    )

    Base.metadata.create_all(engine)

    TestSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    return SQLiteMaintenanceEventRepository(
        TestSessionLocal
    )


def create_event(
    code: str = "ME-ES09-001",
    asset_code: str = "S2-480-ES09-T269",
) -> MaintenanceEvent:

    return MaintenanceEvent(
        code=code,
        asset_code=asset_code,
        event_type="corrective",
        title="Reemplazo de contactor",
        description="Contactor con daño térmico.",
        performed_by="Fortunato Tenorio",
        started_at=datetime(
            2026,
            8,
            9,
            14,
            0,
        ),
        completed_at=datetime(
            2026,
            8,
            9,
            15,
            30,
        ),
        observations="Equipo probado.",
    )


def test_should_save_and_get_event(
    tmp_path,
) -> None:

    repository = create_repository(
        tmp_path
    )

    event = create_event()

    repository.save(event)

    persisted = repository.get_by_code(
        event.code
    )

    assert persisted is not None
    assert persisted.code == event.code
    assert persisted.asset_code == event.asset_code
    assert persisted.title == event.title
    assert persisted.event_type == "corrective"
    assert persisted.is_completed is True


def test_should_list_events_by_asset(
    tmp_path,
) -> None:

    repository = create_repository(
        tmp_path
    )

    repository.save(
        create_event(
            code="ME-001",
            asset_code="ASSET-A",
        )
    )

    repository.save(
        create_event(
            code="ME-002",
            asset_code="ASSET-A",
        )
    )

    repository.save(
        create_event(
            code="ME-003",
            asset_code="ASSET-B",
        )
    )

    events = repository.get_by_asset_code(
        "ASSET-A"
    )

    assert len(events) == 2

    assert {
        event.code
        for event in events
    } == {
        "ME-001",
        "ME-002",
    }


def test_should_update_existing_event(
    tmp_path,
) -> None:

    repository = create_repository(
        tmp_path
    )

    event = create_event()

    repository.save(event)

    event.title = "Contactor reemplazado"
    event.event_type = "repair"
    event.observations = (
        "Equipo liberado para producción."
    )

    repository.save(event)

    persisted = repository.get_by_code(
        event.code
    )

    assert persisted is not None

    assert (
        persisted.title
        == "Contactor reemplazado"
    )

    assert persisted.event_type == "repair"

    assert (
        persisted.observations
        == "Equipo liberado para producción."
    )


def test_should_delete_event(
    tmp_path,
) -> None:

    repository = create_repository(
        tmp_path
    )

    event = create_event()

    repository.save(event)

    result = repository.delete(
        event.code
    )

    assert result is True

    assert repository.get_by_code(
        event.code
    ) is None


def test_delete_should_return_false_when_missing(
    tmp_path,
) -> None:

    repository = create_repository(
        tmp_path
    )

    result = repository.delete(
        "DOES-NOT-EXIST"
    )

    assert result is False