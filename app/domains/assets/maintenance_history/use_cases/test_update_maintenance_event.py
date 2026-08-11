from datetime import datetime

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.repositories import (
    InMemoryMaintenanceEventRepository,
)

from app.domains.assets.maintenance_history.use_cases import (
    UpdateMaintenanceEvent,
    UpdateMaintenanceEventCommand,
)


def create_event() -> MaintenanceEvent:

    return MaintenanceEvent(
        code="ME-001",
        asset_code="ASSET-A",
        event_type="inspection",
        title="Inspección inicial",
        description="Revisión.",
        performed_by="Fortunato Tenorio",
        started_at=datetime(
            2026,
            8,
            10,
            8,
            0,
        ),
    )


def test_should_update_maintenance_event() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    repository.save(create_event())

    use_case = UpdateMaintenanceEvent(
        repository
    )

    result = use_case.execute(
        UpdateMaintenanceEventCommand(
            code="ME-001",
            event_type="corrective",
            title="Reparación terminada",
            description="Se reemplazó componente.",
            performed_by="Fortunato Tenorio",
            started_at=datetime(
                2026,
                8,
                10,
                8,
                0,
            ),
            completed_at=datetime(
                2026,
                8,
                10,
                10,
                30,
            ),
            observations="Equipo liberado.",
        )
    )

    assert result.success is True
    assert result.error is None

    updated = repository.get_by_code(
        "ME-001"
    )

    assert updated is not None
    assert updated.event_type == "corrective"
    assert updated.title == "Reparación terminada"
    assert updated.is_completed is True

    # Identidad y relación no cambian.
    assert updated.code == "ME-001"
    assert updated.asset_code == "ASSET-A"


def test_should_return_not_found_when_updating() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    use_case = UpdateMaintenanceEvent(
        repository
    )

    result = use_case.execute(
        UpdateMaintenanceEventCommand(
            code="DOES-NOT-EXIST",
            event_type="inspection",
            title="Inspección",
            description="Revisión.",
            performed_by="Fortunato Tenorio",
            started_at=datetime(
                2026,
                8,
                10,
                8,
                0,
            ),
        )
    )

    assert result.success is False
    assert (
        result.error
        == "Maintenance event not found."
    )


def test_should_reject_invalid_completion_time() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    repository.save(create_event())

    use_case = UpdateMaintenanceEvent(
        repository
    )

    result = use_case.execute(
        UpdateMaintenanceEventCommand(
            code="ME-001",
            event_type="corrective",
            title="Reparación",
            description="Prueba.",
            performed_by="Fortunato Tenorio",
            started_at=datetime(
                2026,
                8,
                10,
                10,
                0,
            ),
            completed_at=datetime(
                2026,
                8,
                10,
                9,
                0,
            ),
        )
    )

    assert result.success is False

    assert (
        result.error
        == (
            "Completion time cannot be "
            "before start time."
        )
    )