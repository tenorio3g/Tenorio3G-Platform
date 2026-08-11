from datetime import datetime

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.repositories import (
    InMemoryMaintenanceEventRepository,
)

from app.domains.assets.maintenance_history.use_cases import (
    GetMaintenanceEvent,
    GetMaintenanceEventQuery,
)


def test_should_get_maintenance_event() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    repository.save(
        MaintenanceEvent(
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
    )

    use_case = GetMaintenanceEvent(
        repository
    )

    result = use_case.execute(
        GetMaintenanceEventQuery(
            code="ME-001"
        )
    )

    assert result.success is True
    assert result.event is not None
    assert result.event.code == "ME-001"
    assert result.error is None


def test_should_return_not_found() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    use_case = GetMaintenanceEvent(
        repository
    )

    result = use_case.execute(
        GetMaintenanceEventQuery(
            code="DOES-NOT-EXIST"
        )
    )

    assert result.success is False
    assert result.event is None
    assert (
        result.error
        == "Maintenance event not found."
    )