from datetime import datetime

import pytest

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)


def test_should_create_maintenance_event() -> None:

    event = MaintenanceEvent(
        code="ME-ES09-001",
        asset_code="S2-480-ES09-T269",
        event_type="corrective",
        title="Reemplazo de contactor principal",
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

    assert event.code == "ME-ES09-001"
    assert event.asset_code == "S2-480-ES09-T269"
    assert event.event_type == "corrective"
    assert event.is_completed is True


def test_event_without_completion_should_be_open() -> None:

    event = MaintenanceEvent(
        code="ME-ES09-002",
        asset_code="S2-480-ES09-T269",
        event_type="inspection",
        title="Inspección eléctrica",
        description="Revisión general.",
        performed_by="Fortunato Tenorio",
        started_at=datetime(
            2026,
            8,
            9,
            10,
            0,
        ),
    )

    assert event.completed_at is None
    assert event.is_completed is False


def test_should_reject_empty_event_code() -> None:

    with pytest.raises(
        ValueError,
        match="Maintenance event code is required",
    ):
        MaintenanceEvent(
            code="",
            asset_code="S2-480-ES09-T269",
            event_type="inspection",
            title="Inspección",
            description="Revisión.",
            performed_by="Fortunato Tenorio",
            started_at=datetime.now(),
        )


def test_should_reject_empty_asset_code() -> None:

    with pytest.raises(
        ValueError,
        match="Asset code is required",
    ):
        MaintenanceEvent(
            code="ME-001",
            asset_code="",
            event_type="inspection",
            title="Inspección",
            description="Revisión.",
            performed_by="Fortunato Tenorio",
            started_at=datetime.now(),
        )


def test_should_reject_completion_before_start() -> None:

    with pytest.raises(
        ValueError,
        match=(
            "Completion time cannot be "
            "before start time"
        ),
    ):
        MaintenanceEvent(
            code="ME-001",
            asset_code="S2-480-ES09-T269",
            event_type="corrective",
            title="Reparación",
            description="Prueba.",
            performed_by="Fortunato Tenorio",
            started_at=datetime(
                2026,
                8,
                9,
                15,
                0,
            ),
            completed_at=datetime(
                2026,
                8,
                9,
                14,
                0,
            ),
        )