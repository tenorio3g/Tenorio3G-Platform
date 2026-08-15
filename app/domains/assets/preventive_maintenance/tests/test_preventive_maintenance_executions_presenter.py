from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
)

from app.domains.assets.preventive_maintenance.presentation import (
    PreventiveMaintenanceExecutionsPresenter,
)


def create_execution(
    code: str,
    completed_at: datetime,
    observations="Sin anomalías.",
):

    return PreventiveMaintenanceExecution(
        code=code,
        plan_code="PM-001",
        asset_code="ASSET-001",
        performed_by="Fortunato Tenorio",
        scheduled_at=datetime(
            2026,
            8,
            31,
            8,
            0,
        ),
        completed_at=completed_at,
        observations=observations,
    )


def test_should_present_execution():

    execution = create_execution(
        "PME-001",
        datetime(
            2026,
            9,
            1,
            10,
            30,
        ),
    )

    result = (
        PreventiveMaintenanceExecutionsPresenter.present(
            [execution]
        )
    )

    assert result.total == 1
    assert result.has_items is True

    item = result.items[0]

    assert item.code == "PME-001"
    assert item.plan_code == "PM-001"

    assert (
        item.performed_by
        == "Fortunato Tenorio"
    )

    assert (
        item.completed_at
        == "01/09/2026 10:30"
    )
    assert (
        item.scheduled_at
        == "31/08/2026 08:00"
    )

    assert item.status == "ATRASADO"


def test_should_order_newest_execution_first():

    executions = [
        create_execution(
            "PME-001",
            datetime(
                2026,
                6,
                1,
            ),
        ),
        create_execution(
            "PME-003",
            datetime(
                2026,
                9,
                1,
            ),
        ),
        create_execution(
            "PME-002",
            datetime(
                2026,
                8,
                1,
            ),
        ),
    ]

    result = (
        PreventiveMaintenanceExecutionsPresenter.present(
            executions
        )
    )

    assert [
        item.code
        for item in result.items
    ] == [
        "PME-003",
        "PME-002",
        "PME-001",
    ]


def test_should_use_default_observations():

    execution = create_execution(
        "PME-001",
        datetime(
            2026,
            9,
            1,
        ),
        observations="",
    )

    result = (
        PreventiveMaintenanceExecutionsPresenter.present(
            [execution]
        )
    )

    assert (
        result.items[0].observations
        == "Sin observaciones."
    )


def test_should_present_empty_list():

    result = (
        PreventiveMaintenanceExecutionsPresenter.present(
            []
        )
    )

    assert result.items == []
    assert result.has_items is False
    assert result.total == 0

def test_should_present_on_time_status():

    execution = PreventiveMaintenanceExecution(
        code="PME-ONTIME-001",
        plan_code="PM-001",
        asset_code="ASSET-001",
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
            8,
            31,
            10,
            0,
        ),
    )

    result = (
        PreventiveMaintenanceExecutionsPresenter.present(
            [execution]
        )
    )

    assert (
        result.items[0].status
        == "A TIEMPO"
    )