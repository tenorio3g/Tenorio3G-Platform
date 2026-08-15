from datetime import datetime

import pytest

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    InMemoryPreventiveMaintenanceExecutionRepository,
    InMemoryPreventiveMaintenanceRepository,
)

from app.domains.assets.preventive_maintenance.use_cases import (
    CompletePreventiveMaintenancePlan,
    CompletePreventiveMaintenancePlanCommand,
)


def build_use_case():

    plan_repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    execution_repository = (
        InMemoryPreventiveMaintenanceExecutionRepository()
    )

    use_case = CompletePreventiveMaintenancePlan(
        plan_repository,
        execution_repository,
    )

    return (
        plan_repository,
        execution_repository,
        use_case,
    )




def test_should_preserve_original_scheduled_date():

    (
        plan_repository,
        execution_repository,
        use_case,
    ) = build_use_case()

    plan_repository.save(
        create_plan()
    )

    use_case.execute(
        CompletePreventiveMaintenancePlanCommand(
            execution_code="PME-SCHEDULED-001",
            plan_code="PM-001",
            performed_by="Fortunato Tenorio",
            completed_at=datetime(
                2026,
                9,
                1,
                10,
                0,
            ),
        )
    )

    execution = (
        execution_repository.get_by_code(
            "PME-SCHEDULED-001"
        )
    )

    assert execution is not None

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


def test_should_schedule_from_original_due_date_when_completed_early():

    (
        plan_repository,
        _,
        use_case,
    ) = build_use_case()

    plan_repository.save(
        create_plan()
    )

    result = use_case.execute(
        CompletePreventiveMaintenancePlanCommand(
            execution_code="PME-EARLY-001",
            plan_code="PM-001",
            performed_by="Fortunato Tenorio",
            completed_at=datetime(
                2026,
                8,
                30,
                10,
                0,
            ),
        )
    )

    assert (
        result.plan.next_due_at
        == datetime(
            2026,
            11,
            30,
            8,
            0,
        )
    )


def test_should_schedule_from_original_due_date_when_completed_exactly():

    (
        plan_repository,
        _,
        use_case,
    ) = build_use_case()

    plan_repository.save(
        create_plan()
    )

    result = use_case.execute(
        CompletePreventiveMaintenancePlanCommand(
            execution_code="PME-EXACT-001",
            plan_code="PM-001",
            performed_by="Fortunato Tenorio",
            completed_at=datetime(
                2026,
                9,
                1,
                8,
                0,
            ),
        )
    )

    assert (
        result.plan.next_due_at
        == datetime(
            2026,
            11,
            30,
            8,
            0,
        )
    )







def create_plan(
    is_active=True,
):

    return PreventiveMaintenancePlan(
        code="PM-001",
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
        is_active=is_active,
    )


def test_should_complete_plan_and_schedule_next_due_date():

    (
        plan_repository,
        execution_repository,
        use_case,
    ) = build_use_case()

    plan_repository.save(
        create_plan()
    )

    result = use_case.execute(
        CompletePreventiveMaintenancePlanCommand(
            execution_code="PME-001",
            plan_code="PM-001",
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

    execution = (
        execution_repository.get_by_code(
            "PME-001"
        )
    )

    assert execution is not None
    assert execution.plan_code == "PM-001"

    persisted_plan = (
        plan_repository.get_by_code(
            "PM-001"
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


def test_should_reject_unknown_plan():

    _, _, use_case = build_use_case()

    with pytest.raises(
        ValueError,
        match=(
            "preventive maintenance plan not found"
        ),
    ):
        use_case.execute(
            CompletePreventiveMaintenancePlanCommand(
                execution_code="PME-001",
                plan_code="PM-NOT-FOUND",
                performed_by="Fortunato",
                completed_at=datetime(
                    2026,
                    9,
                    1,
                ),
            )
        )


def test_should_reject_inactive_plan():

    plan_repository, _, use_case = (
        build_use_case()
    )

    plan_repository.save(
        create_plan(
            is_active=False
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "preventive maintenance plan is inactive"
        ),
    ):
        use_case.execute(
            CompletePreventiveMaintenancePlanCommand(
                execution_code="PME-001",
                plan_code="PM-001",
                performed_by="Fortunato",
                completed_at=datetime(
                    2026,
                    9,
                    1,
                ),
            )
        )


def test_should_reject_duplicate_execution():

    (
        plan_repository,
        execution_repository,
        use_case,
    ) = build_use_case()

    plan_repository.save(
        create_plan()
    )

    command = (
        CompletePreventiveMaintenancePlanCommand(
            execution_code="PME-001",
            plan_code="PM-001",
            performed_by="Fortunato",
            completed_at=datetime(
                2026,
                9,
                1,
            ),
        )
    )

    use_case.execute(
        command
    )

    with pytest.raises(
        ValueError,
        match=(
            "preventive maintenance execution already exists"
        ),
    ):
        use_case.execute(
            command
        )

    