from datetime import datetime

import pytest

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    InMemoryPreventiveMaintenanceRepository,
)

from app.domains.assets.preventive_maintenance.use_cases import (
    UpdatePreventiveMaintenancePlan,
    UpdatePreventiveMaintenancePlanCommand,
)


def build_repository():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    repository.save(
        PreventiveMaintenancePlan(
            code="PM-001",
            asset_code="ASSET-001",
            title="Inspección inicial",
            frequency_days=30,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                9,
                1,
            ),
        )
    )

    return repository


def test_should_update_plan():

    repository = build_repository()

    use_case = UpdatePreventiveMaintenancePlan(
        repository
    )

    result = use_case.execute(
        UpdatePreventiveMaintenancePlanCommand(
            code="PM-001",
            asset_code="ASSET-001",
            title="Inspección actualizada",
            frequency_days=90,
            responsible_person_code="55464",
            next_due_at=datetime(
                2026,
                12,
                1,
            ),
            description="Plan actualizado.",
            is_active=True,
        )
    )

    assert (
        result.plan.title
        == "Inspección actualizada"
    )

    assert result.plan.frequency_days == 90

    persisted = repository.get_by_code(
        "PM-001"
    )

    assert persisted is not None

    assert (
        persisted.title
        == "Inspección actualizada"
    )

    assert persisted.frequency_days == 90


def test_should_reject_unknown_plan():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    use_case = UpdatePreventiveMaintenancePlan(
        repository
    )

    with pytest.raises(
        ValueError,
        match=(
            "preventive maintenance plan "
            "not found"
        ),
    ):
        use_case.execute(
            UpdatePreventiveMaintenancePlanCommand(
                code="PM-NOT-FOUND",
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