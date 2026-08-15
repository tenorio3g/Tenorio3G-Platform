from datetime import datetime

import pytest

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
)


def test_should_create_execution():

    execution = PreventiveMaintenanceExecution(
        code="PME-001",
        plan_code="PM-001",
        asset_code="S2-480-ES09-T269",
        performed_by="Fortunato Tenorio",
        scheduled_at=datetime(
            2026,
            9,
            1,
            8,
            0,
        ),
        completed_at=datetime(
            2026,
            9,
            1,
            10,
            30,
        ),
        observations="Sin anomalías.",
    )

    assert execution.code == "PME-001"
    assert execution.plan_code == "PM-001"

    assert (
        execution.asset_code
        == "S2-480-ES09-T269"
    )

    assert (
        execution.performed_by
        == "Fortunato Tenorio"
    )

    assert (
        execution.scheduled_at
        == datetime(
            2026,
            9,
            1,
            8,
            0,
        )
    )

    assert (
        execution.completed_at
        == datetime(
            2026,
            9,
            1,
            10,
            30,
        )
    )

    assert (
        execution.observations
        == "Sin anomalías."
    )


def test_should_normalize_codes():

    execution = PreventiveMaintenanceExecution(
        code=" pme-001 ",
        plan_code=" pm-001 ",
        asset_code=" asset-001 ",
        performed_by=" Técnico ",
        scheduled_at=datetime(
            2026,
            9,
            1,
            8,
            0,
        ),
        completed_at=datetime(
            2026,
            9,
            1,
            10,
            0,
        ),
    )

    assert execution.code == "PME-001"
    assert execution.plan_code == "PM-001"
    assert execution.asset_code == "ASSET-001"

    assert (
        execution.performed_by
        == "Técnico"
    )


def test_should_require_code():

    with pytest.raises(
        ValueError,
        match="code is required",
    ):
        PreventiveMaintenanceExecution(
            code="",
            plan_code="PM-001",
            asset_code="ASSET-001",
            performed_by="Técnico",
            scheduled_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
            completed_at=datetime(
                2026,
                9,
                1,
                10,
                0,
            ),
        )


def test_should_require_plan_code():

    with pytest.raises(
        ValueError,
        match="plan_code is required",
    ):
        PreventiveMaintenanceExecution(
            code="PME-001",
            plan_code="",
            asset_code="ASSET-001",
            performed_by="Técnico",
            scheduled_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
            completed_at=datetime(
                2026,
                9,
                1,
                10,
                0,
            ),
        )


def test_should_require_asset_code():

    with pytest.raises(
        ValueError,
        match="asset_code is required",
    ):
        PreventiveMaintenanceExecution(
            code="PME-001",
            plan_code="PM-001",
            asset_code="",
            performed_by="Técnico",
            scheduled_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
            completed_at=datetime(
                2026,
                9,
                1,
                10,
                0,
            ),
        )


def test_should_require_performed_by():

    with pytest.raises(
        ValueError,
        match="performed_by is required",
    ):
        PreventiveMaintenanceExecution(
            code="PME-001",
            plan_code="PM-001",
            asset_code="ASSET-001",
            performed_by="",
            scheduled_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
            completed_at=datetime(
                2026,
                9,
                1,
                10,
                0,
            ),
        )


def test_should_require_scheduled_at_datetime():

    with pytest.raises(
        ValueError,
        match=(
            "scheduled_at must be a datetime"
        ),
    ):
        PreventiveMaintenanceExecution(
            code="PME-001",
            plan_code="PM-001",
            asset_code="ASSET-001",
            performed_by="Técnico",
            scheduled_at="2026-09-01",
            completed_at=datetime(
                2026,
                9,
                1,
                10,
                0,
            ),
        )


def test_should_require_completed_at_datetime():

    with pytest.raises(
        ValueError,
        match=(
            "completed_at must be a datetime"
        ),
    ):
        PreventiveMaintenanceExecution(
            code="PME-001",
            plan_code="PM-001",
            asset_code="ASSET-001",
            performed_by="Técnico",
            scheduled_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
            completed_at="2026-09-01",
        )


def test_execution_should_be_on_time_when_completed_early():

    execution = PreventiveMaintenanceExecution(
        code="PME-EARLY-001",
        plan_code="PM-001",
        asset_code="ASSET-001",
        performed_by="Fortunato Tenorio",
        scheduled_at=datetime(
            2026,
            9,
            1,
            8,
            0,
        ),
        completed_at=datetime(
            2026,
            8,
            31,
            10,
            0,
        ),
    )

    assert execution.is_on_time() is True
    assert execution.is_late() is False


def test_execution_should_be_on_time_when_completed_exactly():

    execution = PreventiveMaintenanceExecution(
        code="PME-EXACT-001",
        plan_code="PM-001",
        asset_code="ASSET-001",
        performed_by="Fortunato Tenorio",
        scheduled_at=datetime(
            2026,
            9,
            1,
            8,
            0,
        ),
        completed_at=datetime(
            2026,
            9,
            1,
            8,
            0,
        ),
    )

    assert execution.is_on_time() is True
    assert execution.is_late() is False


def test_execution_should_be_late_when_completed_after_due_date():

    execution = PreventiveMaintenanceExecution(
        code="PME-LATE-001",
        plan_code="PM-001",
        asset_code="ASSET-001",
        performed_by="Fortunato Tenorio",
        scheduled_at=datetime(
            2026,
            9,
            1,
            8,
            0,
        ),
        completed_at=datetime(
            2026,
            9,
            1,
            10,
            0,
        ),
    )

    assert execution.is_on_time() is False
    assert execution.is_late() is True