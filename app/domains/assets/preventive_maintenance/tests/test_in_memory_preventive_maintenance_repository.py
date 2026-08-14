from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    InMemoryPreventiveMaintenanceRepository,
)


def create_plan(
    code="PM-001",
    asset_code="ASSET-001",
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
            8,
            0,
        ),
    )


def test_should_save_and_get_plan():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    plan = create_plan()

    repository.save(
        plan
    )

    persisted = repository.get_by_code(
        "PM-001"
    )

    assert persisted is not None
    assert persisted.code == "PM-001"


def test_get_by_code_should_normalize_code():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    repository.save(
        create_plan()
    )

    persisted = repository.get_by_code(
        " pm-001 "
    )

    assert persisted is not None
    assert persisted.code == "PM-001"


def test_should_list_plans_by_asset():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    repository.save(
        create_plan(
            code="PM-001",
            asset_code="ASSET-001",
        )
    )

    repository.save(
        create_plan(
            code="PM-002",
            asset_code="ASSET-001",
        )
    )

    repository.save(
        create_plan(
            code="PM-003",
            asset_code="ASSET-002",
        )
    )

    plans = repository.list_by_asset(
        " asset-001 "
    )

    assert len(plans) == 2

    assert {
        plan.code
        for plan in plans
    } == {
        "PM-001",
        "PM-002",
    }


def test_should_list_all_plans():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    repository.save(
        create_plan(
            code="PM-001"
        )
    )

    repository.save(
        create_plan(
            code="PM-002"
        )
    )

    plans = repository.list_all()

    assert len(plans) == 2


def test_should_replace_existing_plan():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    repository.save(
        create_plan()
    )

    updated = PreventiveMaintenancePlan(
        code="PM-001",
        asset_code="ASSET-001",
        title="Inspección actualizada",
        frequency_days=60,
        responsible_person_code="55464",
        next_due_at=datetime(
            2026,
            10,
            1,
        ),
    )

    repository.save(
        updated
    )

    persisted = repository.get_by_code(
        "PM-001"
    )

    assert persisted is not None
    assert (
        persisted.title
        == "Inspección actualizada"
    )
    assert persisted.frequency_days == 60


def test_should_delete_plan():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    repository.save(
        create_plan()
    )

    repository.delete(
        " pm-001 "
    )

    assert repository.get_by_code(
        "PM-001"
    ) is None


def test_delete_unknown_plan_should_not_fail():

    repository = (
        InMemoryPreventiveMaintenanceRepository()
    )

    repository.delete(
        "PM-NOT-FOUND"
    )

    assert repository.list_all() == []