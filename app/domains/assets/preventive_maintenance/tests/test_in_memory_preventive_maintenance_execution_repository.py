from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
)

from app.domains.assets.preventive_maintenance.repositories import (
    InMemoryPreventiveMaintenanceExecutionRepository,
)


def create_execution(
    code="PME-001",
    plan_code="PM-001",
    asset_code="ASSET-001",
):
    return PreventiveMaintenanceExecution(
        code=code,
        plan_code=plan_code,
        asset_code=asset_code,
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
        observations="Sin anomalías.",
    )


def test_should_save_and_get_execution():

    repository = (
        InMemoryPreventiveMaintenanceExecutionRepository()
    )

    repository.save(
        create_execution()
    )

    execution = repository.get_by_code(
        "PME-001"
    )

    assert execution is not None
    assert execution.code == "PME-001"


def test_get_by_code_should_normalize_code():

    repository = (
        InMemoryPreventiveMaintenanceExecutionRepository()
    )

    repository.save(
        create_execution()
    )

    execution = repository.get_by_code(
        " pme-001 "
    )

    assert execution is not None
    assert execution.code == "PME-001"


def test_should_list_executions_by_plan():

    repository = (
        InMemoryPreventiveMaintenanceExecutionRepository()
    )

    repository.save(
        create_execution(
            code="PME-001",
            plan_code="PM-001",
        )
    )

    repository.save(
        create_execution(
            code="PME-002",
            plan_code="PM-001",
        )
    )

    repository.save(
        create_execution(
            code="PME-003",
            plan_code="PM-002",
        )
    )

    executions = repository.list_by_plan(
        " pm-001 "
    )

    assert len(executions) == 2

    assert {
        execution.code
        for execution in executions
    } == {
        "PME-001",
        "PME-002",
    }


def test_should_list_executions_by_asset():

    repository = (
        InMemoryPreventiveMaintenanceExecutionRepository()
    )

    repository.save(
        create_execution(
            code="PME-001",
            asset_code="ASSET-001",
        )
    )

    repository.save(
        create_execution(
            code="PME-002",
            asset_code="ASSET-001",
        )
    )

    repository.save(
        create_execution(
            code="PME-003",
            asset_code="ASSET-002",
        )
    )

    executions = repository.list_by_asset(
        " asset-001 "
    )

    assert len(executions) == 2