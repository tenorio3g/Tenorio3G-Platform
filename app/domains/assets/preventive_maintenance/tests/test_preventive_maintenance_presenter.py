from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.presentation import (
    PreventiveMaintenancePresenter,
)


def create_plan(
    code: str,
    next_due_at: datetime,
    is_active: bool = True,
):

    return PreventiveMaintenancePlan(
        code=code,
        asset_code="ASSET-001",
        title=f"Plan {code}",
        frequency_days=30,
        responsible_person_code="55464",
        next_due_at=next_due_at,
        is_active=is_active,
    )


def test_should_present_programmed_plan():

    reference_at = datetime(
        2026,
        8,
        13,
        10,
        0,
    )

    plan = create_plan(
        "PM-001",
        datetime(
            2026,
            9,
            1,
            8,
            0,
        ),
    )

    result = (
        PreventiveMaintenancePresenter.present(
            [plan],
            reference_at,
        )
    )

    assert result.total == 1
    assert result.has_items is True
    assert result.items[0].status == "PROGRAMADO"


def test_should_present_due_today():

    reference_at = datetime(
        2026,
        8,
        13,
        10,
        0,
    )

    plan = create_plan(
        "PM-001",
        datetime(
            2026,
            8,
            13,
            8,
            0,
        ),
    )

    result = (
        PreventiveMaintenancePresenter.present(
            [plan],
            reference_at,
        )
    )

    assert result.items[0].status == "HOY"


def test_should_present_overdue_plan():

    reference_at = datetime(
        2026,
        8,
        13,
        10,
        0,
    )

    plan = create_plan(
        "PM-001",
        datetime(
            2026,
            8,
            1,
            8,
            0,
        ),
    )

    result = (
        PreventiveMaintenancePresenter.present(
            [plan],
            reference_at,
        )
    )

    assert result.items[0].status == "VENCIDO"


def test_should_present_inactive_plan():

    reference_at = datetime(
        2026,
        8,
        13,
    )

    plan = create_plan(
        "PM-001",
        datetime(
            2026,
            8,
            1,
        ),
        is_active=False,
    )

    result = (
        PreventiveMaintenancePresenter.present(
            [plan],
            reference_at,
        )
    )

    assert result.items[0].status == "INACTIVO"


def test_should_order_by_next_due_date():

    reference_at = datetime(
        2026,
        8,
        13,
    )

    plans = [
        create_plan(
            "PM-003",
            datetime(2026, 10, 1),
        ),
        create_plan(
            "PM-001",
            datetime(2026, 8, 20),
        ),
        create_plan(
            "PM-002",
            datetime(2026, 9, 1),
        ),
    ]

    result = (
        PreventiveMaintenancePresenter.present(
            plans,
            reference_at,
        )
    )

    assert [
        item.code
        for item in result.items
    ] == [
        "PM-001",
        "PM-002",
        "PM-003",
    ]


def test_should_present_empty_list():

    result = (
        PreventiveMaintenancePresenter.present(
            [],
            datetime(
                2026,
                8,
                13,
            ),
        )
    )

    assert result.items == []
    assert result.has_items is False
    assert result.total == 0