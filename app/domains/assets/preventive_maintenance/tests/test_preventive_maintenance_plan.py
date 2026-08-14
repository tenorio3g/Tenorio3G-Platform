from datetime import datetime

import pytest

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)


def create_plan(
    next_due_at=None,
):
    return PreventiveMaintenancePlan(
        code="PM-001",
        asset_code="S2-480-ES09-T269",
        title="Inspección trimestral",
        frequency_days=90,
        responsible_person_code="55464",
        next_due_at=(
            next_due_at
            or datetime(
                2026,
                9,
                1,
                8,
                0,
            )
        ),
        description=(
            "Inspección preventiva general."
        ),
    )


def test_should_create_preventive_plan():

    plan = create_plan()

    assert plan.code == "PM-001"
    assert (
        plan.asset_code
        == "S2-480-ES09-T269"
    )
    assert (
        plan.title
        == "Inspección trimestral"
    )
    assert plan.frequency_days == 90
    assert (
        plan.responsible_person_code
        == "55464"
    )
    assert plan.is_active is True


def test_should_normalize_codes():

    plan = PreventiveMaintenancePlan(
        code=" pm-001 ",
        asset_code=" asset-001 ",
        title="Inspección",
        frequency_days=30,
        responsible_person_code=" tech-001 ",
        next_due_at=datetime(
            2026,
            9,
            1,
        ),
    )

    assert plan.code == "PM-001"
    assert plan.asset_code == "ASSET-001"
    assert (
        plan.responsible_person_code
        == "TECH-001"
    )


def test_should_reject_invalid_frequency():

    with pytest.raises(
        ValueError,
        match=(
            "frequency_days must be "
            "greater than zero"
        ),
    ):
        PreventiveMaintenancePlan(
            code="PM-001",
            asset_code="ASSET-001",
            title="Inspección",
            frequency_days=0,
            responsible_person_code="TECH-001",
            next_due_at=datetime(
                2026,
                9,
                1,
            ),
        )


def test_should_require_datetime():

    with pytest.raises(
        ValueError,
        match=(
            "next_due_at must be a datetime"
        ),
    ):
        PreventiveMaintenancePlan(
            code="PM-001",
            asset_code="ASSET-001",
            title="Inspección",
            frequency_days=30,
            responsible_person_code="TECH-001",
            next_due_at="2026-09-01",
        )


def test_should_be_due():

    plan = create_plan(
        next_due_at=datetime(
            2026,
            8,
            1,
        )
    )

    assert plan.is_due(
        datetime(
            2026,
            8,
            13,
        )
    ) is True


def test_should_not_be_due():

    plan = create_plan(
        next_due_at=datetime(
            2026,
            9,
            1,
        )
    )

    assert plan.is_due(
        datetime(
            2026,
            8,
            13,
        )
    ) is False


def test_inactive_plan_should_not_be_due():

    plan = create_plan(
        next_due_at=datetime(
            2026,
            8,
            1,
        )
    )

    plan.deactivate()

    assert plan.is_due(
        datetime(
            2026,
            8,
            13,
        )
    ) is False


def test_should_activate_and_deactivate():

    plan = create_plan()

    plan.deactivate()

    assert plan.is_active is False

    plan.activate()

    assert plan.is_active is True