from datetime import datetime

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.presentation import (
    MaintenanceHistoryPresenter,
)


def create_event(
    code: str,
    started_at: datetime,
    completed_at: datetime | None = None,
) -> MaintenanceEvent:

    return MaintenanceEvent(
        code=code,
        asset_code="ASSET-A",
        event_type="inspection",
        title="Inspección",
        description="Revisión general.",
        performed_by="Fortunato Tenorio",
        started_at=started_at,
        completed_at=completed_at,
        observations="Sin novedad.",
    )


def test_should_present_maintenance_history() -> None:

    events = [
        create_event(
            code="ME-001",
            started_at=datetime(
                2026, 8, 10, 8, 0
            ),
        )
    ]

    view_model = (
        MaintenanceHistoryPresenter.present(
            events
        )
    )

    assert view_model.has_items is True
    assert view_model.total == 1

    item = view_model.items[0]

    assert item.code == "ME-001"
    assert item.title == "Inspección"
    assert item.status == "Abierto"
    assert item.started_at == "10/08/2026 08:00"


def test_should_identify_completed_event() -> None:

    events = [
        create_event(
            code="ME-001",
            started_at=datetime(
                2026, 8, 10, 8, 0
            ),
            completed_at=datetime(
                2026, 8, 10, 9, 30
            ),
        )
    ]

    view_model = (
        MaintenanceHistoryPresenter.present(
            events
        )
    )

    assert (
        view_model.items[0].status
        == "Completado"
    )

    assert (
        view_model.items[0].completed_at
        == "10/08/2026 09:30"
    )


def test_should_order_most_recent_first() -> None:

    events = [
        create_event(
            code="ME-OLD",
            started_at=datetime(
                2026, 8, 1, 8, 0
            ),
        ),
        create_event(
            code="ME-NEW",
            started_at=datetime(
                2026, 8, 10, 8, 0
            ),
        ),
    ]

    view_model = (
        MaintenanceHistoryPresenter.present(
            events
        )
    )

    assert (
        view_model.items[0].code
        == "ME-NEW"
    )

    assert (
        view_model.items[1].code
        == "ME-OLD"
    )


def test_should_present_empty_history() -> None:

    view_model = (
        MaintenanceHistoryPresenter.present(
            []
        )
    )

    assert view_model.has_items is False
    assert view_model.total == 0
    assert view_model.items == []