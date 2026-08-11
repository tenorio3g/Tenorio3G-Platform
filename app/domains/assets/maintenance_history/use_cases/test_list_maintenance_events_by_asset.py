from datetime import datetime

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.repositories import (
    InMemoryMaintenanceEventRepository,
)

from app.domains.assets.maintenance_history.use_cases import (
    ListMaintenanceEventsByAsset,
    ListMaintenanceEventsByAssetQuery,
)


def create_event(
    code: str,
    asset_code: str,
) -> MaintenanceEvent:

    return MaintenanceEvent(
        code=code,
        asset_code=asset_code,
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


def test_should_list_events_by_asset() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    repository.save(
        create_event(
            "ME-001",
            "ASSET-A",
        )
    )

    repository.save(
        create_event(
            "ME-002",
            "ASSET-A",
        )
    )

    repository.save(
        create_event(
            "ME-003",
            "ASSET-B",
        )
    )

    use_case = ListMaintenanceEventsByAsset(
        repository
    )

    result = use_case.execute(
        ListMaintenanceEventsByAssetQuery(
            asset_code="ASSET-A"
        )
    )

    assert result.success is True
    assert len(result.events) == 2

    assert {
        event.code
        for event in result.events
    } == {
        "ME-001",
        "ME-002",
    }


def test_should_return_empty_list_when_asset_has_no_events() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    use_case = ListMaintenanceEventsByAsset(
        repository
    )

    result = use_case.execute(
        ListMaintenanceEventsByAssetQuery(
            asset_code="ASSET-A"
        )
    )

    assert result.success is True
    assert result.events == []


def test_should_reject_empty_asset_code() -> None:

    repository = (
        InMemoryMaintenanceEventRepository()
    )

    use_case = ListMaintenanceEventsByAsset(
        repository
    )

    result = use_case.execute(
        ListMaintenanceEventsByAssetQuery(
            asset_code=""
        )
    )

    assert result.success is False
    assert result.events == []
    assert result.error == "Asset code is required."