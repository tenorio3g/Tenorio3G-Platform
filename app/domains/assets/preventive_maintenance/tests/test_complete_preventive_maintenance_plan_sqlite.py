from datetime import datetime

from app.domains.assets.preventive_maintenance.bootstrap import (
    complete_preventive_maintenance_plan,
)

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.use_cases import (
    CompletePreventiveMaintenancePlanCommand,
)


def test_should_complete_plan_using_sqlite_repositories(
    preventive_maintenance_execution_test_db,
):

    (
        plan_repository,
        execution_repository,
    ) = preventive_maintenance_execution_test_db

    plan_repository.save(
        PreventiveMaintenancePlan(
            code="PM-SQL-001",
            asset_code="ASSET-001",
            title="Inspección trimestral",
            frequency_days=90,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
            description="Plan preventivo.",
        )
    )

    result = (
        complete_preventive_maintenance_plan.execute(
            CompletePreventiveMaintenancePlanCommand(
                execution_code="PME-SQL-001",
                plan_code="PM-SQL-001",
                performed_by="Fortunato Tenorio",
                completed_at=datetime(
                    2026,
                    9,
                    1,
                    10,
                    0,
                ),
                observations="Sin anomalías.",
            )
        )
    )

    execution = (
        execution_repository.get_by_code(
            "PME-SQL-001"
        )
    )

    assert execution is not None
    assert execution.plan_code == "PM-SQL-001"

    persisted_plan = (
        plan_repository.get_by_code(
            "PM-SQL-001"
        )
    )

    assert persisted_plan is not None

    assert (
        persisted_plan.next_due_at
        == datetime(
            2026,
            11,
            30,
            10,
            0,
        )
    )

    assert (
        result.plan.next_due_at
        == persisted_plan.next_due_at
    )