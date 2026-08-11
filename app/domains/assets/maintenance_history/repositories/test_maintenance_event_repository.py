from datetime import datetime

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.repositories import (
    InMemoryMaintenanceEventRepository,
)


def create_event(
    code: str = "ME-ES09-001",
    asset_code: str = "S2-480-ES09-T269",
) -> MaintenanceEvent:

    return MaintenanceEvent(
        code=code,
        asset_code=asset_code,
        event_type="corrective",
        title="Reparación",
        description="Evento de prueba.",
        performed_by="Fortunato Tenorio",
        started_at=datetime(
            2026,
            8,
            9,
            14,
            0,
        ),
    )


def test_should_save_and_get_event() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    event = create_event()

    repository.save(event)

    persisted = repository.get_by_code(
        "ME-ES09-001"
    )

    assert persisted is not None
    assert persisted.code == "ME-ES09-001"
    assert (
        persisted.asset_code
        == "S2-480-ES09-T269"
    )


def test_should_return_none_when_event_does_not_exist() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    result = repository.get_by_code(
        "DOES-NOT-EXIST"
    )

    assert result is None


def test_should_list_events_by_asset() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
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


def test_should_delete_event() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    repository.save(
        create_event()
    )

    result = repository.delete(
        "ME-ES09-001"
    )

    assert result is True

    assert repository.get_by_code(
        "ME-ES09-001"
    ) is None


def test_delete_should_return_false_when_event_does_not_exist() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    result = repository.delete(
        "DOES-NOT-EXIST"
    )

    assert result is False