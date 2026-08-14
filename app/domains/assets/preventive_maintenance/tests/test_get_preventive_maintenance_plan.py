from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    InMemoryPreventiveMaintenanceRepository,
)

from app.domains.assets.preventive_maintenance.use_cases import (
    GetPreventiveMaintenancePlan,
    GetPreventiveMaintenancePlanQuery,
)


def test_should_get_existing_plan():

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

    use_case = GetPreventiveMaintenancePlan(
        repository
    )

    result = use_case.execute(
        GetPreventiveMaintenancePlanQuery(
            code=" pm-001 "
        )
    )

    assert result.plan is not None
    assert result.plan.code == "PM-001"


def test_should_return_none_when_not_found():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    use_case = GetPreventiveMaintenancePlan(
        repository
    )

    result = use_case.execute(
        GetPreventiveMaintenancePlanQuery(
            code="PM-NOT-FOUND"
        )
    )

    assert result.plan is None