from datetime import datetime

import pytest

from app.operations.operational_activities.entities.operational_activity import (
    OperationalActivity,
    OperationalActivitySource,
    OperationalActivityStatus,
)


def test_should_create_completed_manual_operational_activity_without_work_order():
    started_at = datetime(
        2026,
        9,
        15,
        7,
        0,
    )

    ended_at = datetime(
        2026,
        9,
        15,
        8,
        30,
    )

    created_at = datetime(
        2026,
        9,
        15,
        8,
        35,
    )

    activity = OperationalActivity(
        code="OP-ACT-001",
        description=(
            "Instalaci?n de m?dem y antenas "
            "en gabinete del ?rea de inversores"
        ),
        started_at=started_at,
        ended_at=ended_at,
        result_notes="",
        area="Subestaci?n 1",
        location_description="?rea de inversores",
        asset_code=None,
        work_order_code=None,
        source=OperationalActivitySource.MANUAL,
        created_at=created_at,
        created_by_person_code="SUP-001",
    )

    assert activity.code == "OP-ACT-001"
    assert activity.description == (
        "Instalaci?n de m?dem y antenas "
        "en gabinete del ?rea de inversores"
    )

    assert activity.started_at == started_at
    assert activity.ended_at == ended_at

    assert activity.status == (
        OperationalActivityStatus.COMPLETED
    )

    assert activity.result_notes == ""
    assert activity.area == "Subestaci?n 1"
    assert (
        activity.location_description
        == "?rea de inversores"
    )

    assert activity.asset_code is None
    assert activity.work_order_code is None

    assert (
        activity.source
        == OperationalActivitySource.MANUAL
    )

    assert activity.created_at == created_at
    assert (
        activity.created_by_person_code
        == "SUP-001"
    )

    assert activity.work_date == started_at.date()

def test_should_create_operational_activity_in_progress():
    started_at = datetime(
        2026,
        9,
        17,
        7,
        0,
    )

    activity = OperationalActivity(
        code="OP-ACT-002",
        description=(
            "Revisi?n de alumbrado exterior"
        ),
        started_at=started_at,
        area="Exterior",
        created_by_person_code="SUP-001",
    )

    assert activity.code == "OP-ACT-002"
    assert activity.started_at == started_at
    assert activity.ended_at is None

    assert activity.status == (
        OperationalActivityStatus.IN_PROGRESS
    )

    assert activity.work_date == started_at.date()

    assert activity.result_notes == ""
    assert activity.asset_code is None
    assert activity.work_order_code is None

    assert (
        activity.source
        == OperationalActivitySource.MANUAL
    )

def test_should_reject_end_before_start():
    started_at = datetime(
        2026,
        9,
        17,
        10,
        0,
    )

    ended_at = datetime(
        2026,
        9,
        17,
        9,
        0,
    )

    with pytest.raises(
        ValueError,
        match="ended_at cannot be before started_at",
    ):
        OperationalActivity(
            code="OP-ACT-003",
            description="Revisi?n de tablero",
            started_at=started_at,
            ended_at=ended_at,
            created_by_person_code="SUP-001",
        )

def test_should_complete_operational_activity_in_progress():
    started_at = datetime(
        2026,
        9,
        17,
        7,
        0,
    )

    ended_at = datetime(
        2026,
        9,
        17,
        9,
        0,
    )

    activity = OperationalActivity(
        code="OP-ACT-004",
        description="Revisi?n de alumbrado exterior",
        started_at=started_at,
        area="Exterior",
        created_by_person_code="SUP-001",
    )

    assert activity.status == (
        OperationalActivityStatus.IN_PROGRESS
    )

    activity.complete(
        ended_at=ended_at,
        result_notes=(
            "Se realiz? recorrido y revisi?n "
            "del alumbrado exterior."
        ),
    )

    assert activity.ended_at == ended_at

    assert activity.status == (
        OperationalActivityStatus.COMPLETED
    )

    assert activity.result_notes == (
        "Se realiz? recorrido y revisi?n "
        "del alumbrado exterior."
    )

def test_should_reject_completing_activity_twice():
    started_at = datetime(
        2026,
        9,
        17,
        7,
        0,
    )

    first_ended_at = datetime(
        2026,
        9,
        17,
        9,
        0,
    )

    second_ended_at = datetime(
        2026,
        9,
        17,
        10,
        0,
    )

    activity = OperationalActivity(
        code="OP-ACT-005",
        description="Revisi?n de alumbrado exterior",
        started_at=started_at,
        created_by_person_code="SUP-001",
    )

    activity.complete(
        ended_at=first_ended_at,
        result_notes="Revisi?n terminada.",
    )

    with pytest.raises(
        ValueError,
        match="activity is already completed",
    ):
        activity.complete(
            ended_at=second_ended_at,
            result_notes="Resultado modificado.",
        )

    assert activity.ended_at == first_ended_at
    assert (
        activity.result_notes
        == "Revisi?n terminada."
    )

def test_should_reject_completing_before_start():
    started_at = datetime(
        2026,
        9,
        17,
        10,
        0,
    )

    invalid_ended_at = datetime(
        2026,
        9,
        17,
        9,
        0,
    )

    activity = OperationalActivity(
        code="OP-ACT-006",
        description="Revisi?n de tablero",
        started_at=started_at,
        created_by_person_code="SUP-001",
    )

    with pytest.raises(
        ValueError,
        match="ended_at cannot be before started_at",
    ):
        activity.complete(
            ended_at=invalid_ended_at,
            result_notes="Revisi?n terminada.",
        )

    assert activity.ended_at is None

    assert activity.status == (
        OperationalActivityStatus.IN_PROGRESS
    )

    assert activity.result_notes == ""

def test_new_activity_should_have_empty_completion_audit():
    activity = OperationalActivity(
        code="OP-ACT-020",
        description="Revisi?n de equipo",
        started_at=datetime(
            2026,
            9,
            17,
            14,
            0,
        ),
        area="Producci?n",
        created_by_person_code="TECH-001",
    )

    assert activity.completed_at is None

    assert (
        activity.completed_by_person_code
        == ""
    )

    assert activity.status == (
        OperationalActivityStatus.IN_PROGRESS
    )

def test_should_reject_completed_at_before_ended_at():
    activity = OperationalActivity(
        code="OP-ACT-024",
        description="Revisi?n de tablero el?ctrico",
        started_at=datetime(
            2026,
            9,
            17,
            14,
            0,
        ),
        area="Producci?n",
        created_by_person_code="SUP-001",
    )

    with pytest.raises(
        ValueError,
        match="^completed_at cannot be before ended_at$",
    ):
        activity.complete(
            ended_at=datetime(
                2026,
                9,
                17,
                15,
                0,
            ),
            result_notes="Revisi?n terminada",
            completed_at=datetime(
                2026,
                9,
                17,
                14,
                59,
            ),
            completed_by_person_code="TECH-001",
        )

    assert activity.ended_at is None
    assert activity.result_notes == ""
    assert activity.completed_at is None

    assert (
        activity.completed_by_person_code
        == ""
    )

    assert activity.status == (
        OperationalActivityStatus.IN_PROGRESS
    )

