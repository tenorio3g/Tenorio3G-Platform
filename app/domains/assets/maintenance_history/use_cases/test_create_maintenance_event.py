from datetime import datetime

from app.domains.assets.maintenance_history.repositories import (
    InMemoryMaintenanceEventRepository,
)

from app.domains.assets.maintenance_history.use_cases import (
    CreateMaintenanceEvent,
    CreateMaintenanceEventCommand,
)


def create_command(
    code: str = "ME-ES09-001",
) -> CreateMaintenanceEventCommand:

    return CreateMaintenanceEventCommand(
        code=code,
        asset_code="S2-480-ES09-T269",
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


def test_should_create_maintenance_event() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    use_case = CreateMaintenanceEvent(
        repository
    )

    result = use_case.execute(
        create_command()
    )

    assert result.success is True
    assert result.event is not None
    assert result.error is None

    persisted = repository.get_by_code(
        "ME-ES09-001"
    )

    assert persisted is not None
    assert (
        persisted.title
        == "Reemplazo de contactor"
    )


def test_should_reject_duplicate_event() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    use_case = CreateMaintenanceEvent(
        repository
    )

    first = use_case.execute(
        create_command()
    )

    second = use_case.execute(
        create_command()
    )

    assert first.success is True
    assert second.success is False
    assert second.event is None
    assert second.error is not None


def test_should_return_domain_validation_error() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    use_case = CreateMaintenanceEvent(
        repository
    )

    command = create_command(
        code="",
    )

    result = use_case.execute(command)

    assert result.success is False
    assert result.event is None
    assert (
        result.error
        == "Maintenance event code is required."
    )