from datetime import datetime

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.repositories import (
    InMemoryMaintenanceEventRepository,
)

from app.domains.assets.maintenance_history.use_cases import (
    DeleteMaintenanceEvent,
    DeleteMaintenanceEventCommand,
)


def create_event() -> MaintenanceEvent:

    return MaintenanceEvent(
        code="ME-001",
        asset_code="ASSET-A",
        event_type="inspection",
        title="Inspección",
        description="Revisión general.",
        performed_by="Fortunato Tenorio",
        started_at=datetime(
            2026,
            8,
            10,
            8,
            0,
        ),
    )


def test_should_delete_maintenance_event() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    repository.save(
        create_event()
    )

    use_case = DeleteMaintenanceEvent(
        repository
    )

    result = use_case.execute(
        DeleteMaintenanceEventCommand(
            code="ME-001"
        )
    )

    assert result.success is True
    assert result.error is None

    assert repository.get_by_code(
        "ME-001"
    ) is None


def test_should_return_not_found_when_deleting() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    use_case = DeleteMaintenanceEvent(
        repository
    )

    result = use_case.execute(
        DeleteMaintenanceEventCommand(
            code="DOES-NOT-EXIST"
        )
    )

    assert result.success is False

    assert (
        result.error
        == "Maintenance event not found."
    )