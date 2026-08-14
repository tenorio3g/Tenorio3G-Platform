from datetime import datetime

import pytest

from app.domains.assets.preventive_maintenance.repositories import (
    InMemoryPreventiveMaintenanceRepository,
)

from app.domains.assets.preventive_maintenance.use_cases import (
    CreatePreventiveMaintenancePlan,
    CreatePreventiveMaintenancePlanCommand,
)


def build_use_case():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    use_case = CreatePreventiveMaintenancePlan(
        repository
    )

    return repository, use_case


def create_command():

    return CreatePreventiveMaintenancePlanCommand(
        code="PM-001",
        asset_code="S2-480-ES09-T269",
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
        description=(
            "Inspección preventiva general."
        ),
    )


def test_should_create_plan():

    repository, use_case = build_use_case()

    result = use_case.execute(
        create_command()
    )

    assert result.plan.code == "PM-001"

    persisted = repository.get_by_code(
        "PM-001"
    )

    assert persisted is not None
    assert (
        persisted.title
        == "Inspección trimestral"
    )


def test_should_reject_duplicate_plan():

    _, use_case = build_use_case()

    command = create_command()

    use_case.execute(
        command
    )

    with pytest.raises(
        ValueError,
        match=(
            "preventive maintenance plan "
            "already exists"
        ),
    ):
        use_case.execute(
            command
        )