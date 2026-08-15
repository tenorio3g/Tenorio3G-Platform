from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.presentation import (
    PreventiveMaintenanceMetricsPresenter,
)


def create_plan(
    code,
    next_due_at,
    is_active=True,
):

    return PreventiveMaintenancePlan(
        code=code,
        asset_code="ASSET-001",
        title=f"Plan {code}",
        frequency_days=30,
        responsible_person_code="55464",
        next_due_at=next_due_at,
        is_active=is_active,
    )


def create_execution(
    code,
    scheduled_at,
    completed_at,
):

    return PreventiveMaintenanceExecution(
        code=code,
        plan_code="PM-001",
        asset_code="ASSET-001",
        performed_by="Fortunato Tenorio",
        scheduled_at=scheduled_at,
        completed_at=completed_at,
    )


def test_should_calculate_preventive_metrics():

    reference_at = datetime(
        2026,
        8,
        14,
        12,
        0,
    )

    plans = [
        create_plan(
            "PM-001",
            datetime(2026, 8, 20),
        ),
        create_plan(
            "PM-002",
            datetime(2026, 8, 14),
        ),
        create_plan(
            "PM-003",
            datetime(2026, 8, 10),
        ),
        create_plan(
            "PM-004",
            datetime(2026, 8, 1),
            is_active=False,
        ),
    ]

    executions = [
        create_execution(
            "PME-001",
            datetime(
                2026,
                8,
                14,
                12,
                0,
            ),
            datetime(
                2026,
                8,
                14,
                10,
                0,
            ),
        ),
        create_execution(
            "PME-002",
            datetime(
                2026,
                8,
                14,
                8,
                0,
            ),
            datetime(
                2026,
                8,
                14,
                10,
                0,
            ),
        ),
    ]

    result = (
        PreventiveMaintenanceMetricsPresenter.present(
            plans,
            executions,
            reference_at,
        )
    )

    assert result.total_plans == 4
    assert result.active_plans == 3
    assert result.programmed == 1
    assert result.due_today == 1
    assert result.overdue == 1
    assert result.inactive == 1
    assert result.executions == 2
    assert result.on_time_executions == 1
    assert result.late_executions == 1
    assert result.compliance_percent == 50.0


def test_should_calculate_empty_metrics():

    result = (
        PreventiveMaintenanceMetricsPresenter.present(
            [],
            [],
            datetime(
                2026,
                8,
                14,
            ),
        )
    )

    assert result.total_plans == 0
    assert result.active_plans == 0
    assert result.programmed == 0
    assert result.due_today == 0
    assert result.overdue == 0
    assert result.inactive == 0
    assert result.executions == 0
    assert result.on_time_executions == 0
    assert result.late_executions == 0
    assert result.compliance_percent == 0.0