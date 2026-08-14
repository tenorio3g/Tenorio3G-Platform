from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    InMemoryPreventiveMaintenanceRepository,
)

from app.domains.assets.preventive_maintenance.use_cases import (
    DeletePreventiveMaintenancePlan,
    DeletePreventiveMaintenancePlanCommand,
)


def test_should_delete_existing_plan():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    repository.save(
        PreventiveMaintenancePlan(
            code="PM-001",
            asset_code="ASSET-001",
            title="Inspección",
            frequency_days=30,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
            ),
        )
    )

    use_case = DeletePreventiveMaintenancePlan(
        repository
    )

    result = use_case.execute(
        DeletePreventiveMaintenancePlanCommand(
            code="PM-001"
        )
    )

    assert result.deleted is True

    assert repository.get_by_code(
        "PM-001"
    ) is None


def test_delete_unknown_plan_should_return_false():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    use_case = DeletePreventiveMaintenancePlan(
        repository
    )

    result = use_case.execute(
        DeletePreventiveMaintenancePlanCommand(
            code="PM-NOT-FOUND"
        )
    )

    assert result.deleted is False