from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    InMemoryPreventiveMaintenanceRepository,
)

from app.domains.assets.preventive_maintenance.use_cases import (
    ListPreventiveMaintenancePlansByAsset,
    ListPreventiveMaintenancePlansByAssetQuery,
)


def create_plan(
    code: str,
    asset_code: str,
):
    return PreventiveMaintenancePlan(
        code=code,
        asset_code=asset_code,
        title="Inspección preventiva",
        frequency_days=30,
        responsible_person_code="55464",
        next_due_at=datetime(
            2026,
            9,
            1,
        ),
    )


def test_should_list_plans_by_asset():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    repository.save(
        create_plan(
            "PM-001",
            "ASSET-001",
        )
    )

    repository.save(
        create_plan(
            "PM-002",
            "ASSET-001",
        )
    )

    repository.save(
        create_plan(
            "PM-003",
            "ASSET-002",
        )
    )

    use_case = (
        ListPreventiveMaintenancePlansByAsset(
            repository
        )
    )

    result = use_case.execute(
        ListPreventiveMaintenancePlansByAssetQuery(
            asset_code="ASSET-001"
        )
    )

    assert len(result.plans) == 2

    assert {
        plan.code
        for plan in result.plans
    } == {
        "PM-001",
        "PM-002",
    }


def test_should_return_empty_list():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    use_case = (
        ListPreventiveMaintenancePlansByAsset(
            repository
        )
    )

    result = use_case.execute(
        ListPreventiveMaintenancePlansByAssetQuery(
            asset_code="ASSET-NOT-FOUND"
        )
    )

    assert result.plans == []