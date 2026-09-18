from datetime import date, datetime

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.operations.operational_activities.entities import (
    OperationalActivity,
    OperationalActivitySource,
    OperationalActivityStatus,
)

from app.operations.operational_activities.models import (
    OperationalActivityModel,
)

from app.operations.operational_activities.repositories import (
    SQLiteOperationalActivityRepository,
)


@pytest.fixture
def repository(tmp_path):

    database_path = (
        tmp_path
        / "operational_activities.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    Base.metadata.create_all(
        engine
    )

    session_factory = sessionmaker(
        bind=engine
    )

    repository = (
        SQLiteOperationalActivityRepository(
            session_factory
        )
    )

    yield repository

    engine.dispose()


def test_should_save_and_get_completed_activity(
    repository,
):

    activity = OperationalActivity(
        code="OP-ACT-001",
        description=(
            "Instalaci?n de modem y antenas "
            "en gabinete de inversor"
        ),
        started_at=datetime(
            2026,
            9,
            15,
            7,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            15,
            8,
            30,
        ),
        result_notes=(
            "Instalaci?n terminada"
        ),
        area="Subestaci?n 1",
        location_description=(
            "Gabinete de inversor"
        ),
        asset_code=None,
        work_order_code=None,
        source=(
            OperationalActivitySource.MANUAL
        ),
        created_at=datetime(
            2026,
            9,
            15,
            8,
            35,
        ),
        created_by_person_code="TECH-001",
        completed_at=datetime(
            2026,
            9,
            15,
            8,
            35,
        ),
        completed_by_person_code="TECH-001",
    )

    repository.save(
        activity
    )

    restored = repository.get_by_code(
        "OP-ACT-001"
    )

    assert restored is not None

    assert restored.code == "OP-ACT-001"

    assert restored.description == (
        "Instalaci?n de modem y antenas "
        "en gabinete de inversor"
    )

    assert restored.started_at == datetime(
        2026,
        9,
        15,
        7,
        0,
    )

    assert restored.ended_at == datetime(
        2026,
        9,
        15,
        8,
        30,
    )

    assert restored.result_notes == (
        "Instalaci?n terminada"
    )

    assert restored.area == "Subestaci?n 1"

    assert restored.location_description == (
        "Gabinete de inversor"
    )

    assert restored.asset_code is None
    assert restored.work_order_code is None

    assert restored.source == (
        OperationalActivitySource.MANUAL
    )

    assert restored.created_at == datetime(
        2026,
        9,
        15,
        8,
        35,
    )

    assert (
        restored.created_by_person_code
        == "TECH-001"
    )

    assert restored.completed_at == datetime(
        2026,
        9,
        15,
        8,
        35,
    )

    assert (
        restored.completed_by_person_code
        == "TECH-001"
    )



def test_should_update_open_activity_when_completed(
    repository,
):

    activity = OperationalActivity(
        code="OP-ACT-002",
        description=(
            "Revisi?n de alumbrado"
        ),
        started_at=datetime(
            2026,
            9,
            17,
            10,
            0,
        ),
        area="Recibos 1",
        source=(
            OperationalActivitySource.MANUAL
        ),
        created_at=datetime(
            2026,
            9,
            17,
            10,
            0,
        ),
        created_by_person_code="TECH-001",
    )

    repository.save(
        activity
    )

    activity.complete(
        ended_at=datetime(
            2026,
            9,
            17,
            11,
            30,
        ),
        result_notes=(
            "Revisi?n terminada sin anomal?as"
        ),
        completed_at=datetime(
            2026,
            9,
            17,
            11,
            35,
        ),
        completed_by_person_code="TECH-002",
    )

    repository.save(
        activity
    )

    restored = repository.get_by_code(
        "OP-ACT-002"
    )

    assert restored is not None

    assert restored.ended_at == datetime(
        2026,
        9,
        17,
        11,
        30,
    )

    assert restored.result_notes == (
        "Revisi?n terminada sin anomal?as"
    )

    assert restored.completed_at == datetime(
        2026,
        9,
        17,
        11,
        35,
    )

    assert (
        restored.completed_by_person_code
        == "TECH-002"
    )

    assert (
        restored.status
        == OperationalActivityStatus.COMPLETED
    )



def test_should_list_activity_contained_in_date(
    repository,
):

    activity = OperationalActivity(
        code="OP-ACT-003",
        description="Actividad dentro del d?a",
        started_at=datetime(
            2026, 9, 17, 8, 0
        ),
        ended_at=datetime(
            2026, 9, 17, 10, 0
        ),
        source=OperationalActivitySource.MANUAL,
        created_at=datetime(
            2026, 9, 17, 8, 0
        ),
        created_by_person_code="TECH-001",
    )

    repository.save(activity)

    activities = repository.list_by_date(
        date(2026, 9, 17)
    )

    assert [
        item.code
        for item in activities
    ] == ["OP-ACT-003"]


def test_should_list_cross_midnight_activity_on_both_dates(
    repository,
):

    activity = OperationalActivity(
        code="OP-ACT-004",
        description="Actividad que cruza medianoche",
        started_at=datetime(
            2026, 9, 16, 23, 30
        ),
        ended_at=datetime(
            2026, 9, 17, 0, 30
        ),
        source=OperationalActivitySource.MANUAL,
        created_at=datetime(
            2026, 9, 16, 23, 30
        ),
        created_by_person_code="TECH-001",
    )

    repository.save(activity)

    september_16 = repository.list_by_date(
        date(2026, 9, 16)
    )

    september_17 = repository.list_by_date(
        date(2026, 9, 17)
    )

    assert [
        item.code
        for item in september_16
    ] == ["OP-ACT-004"]

    assert [
        item.code
        for item in september_17
    ] == ["OP-ACT-004"]


def test_should_list_carried_open_activity_on_later_date(
    repository,
):

    activity = OperationalActivity(
        code="OP-ACT-005",
        description="Actividad abierta",
        started_at=datetime(
            2026, 9, 16, 22, 0
        ),
        source=OperationalActivitySource.MANUAL,
        created_at=datetime(
            2026, 9, 16, 22, 0
        ),
        created_by_person_code="TECH-001",
    )

    repository.save(activity)

    activities = repository.list_by_date(
        date(2026, 9, 17)
    )

    assert [
        item.code
        for item in activities
    ] == ["OP-ACT-005"]


def test_should_exclude_activity_outside_requested_date(
    repository,
):

    activity = OperationalActivity(
        code="OP-ACT-006",
        description="Actividad de otro d?a",
        started_at=datetime(
            2026, 9, 15, 8, 0
        ),
        ended_at=datetime(
            2026, 9, 15, 9, 0
        ),
        source=OperationalActivitySource.MANUAL,
        created_at=datetime(
            2026, 9, 15, 8, 0
        ),
        created_by_person_code="TECH-001",
    )

    repository.save(activity)

    activities = repository.list_by_date(
        date(2026, 9, 17)
    )

    assert activities == []



def test_should_exclude_activity_ending_exactly_at_day_start(
    repository,
):

    activity = OperationalActivity(
        code="OP-ACT-007",
        description=(
            "Actividad terminada exactamente "
            "a medianoche"
        ),
        started_at=datetime(
            2026, 9, 16, 23, 0
        ),
        ended_at=datetime(
            2026, 9, 17, 0, 0
        ),
        source=OperationalActivitySource.MANUAL,
        created_at=datetime(
            2026, 9, 16, 23, 0
        ),
        created_by_person_code="TECH-001",
    )

    repository.save(activity)

    september_16 = repository.list_by_date(
        date(2026, 9, 16)
    )

    september_17 = repository.list_by_date(
        date(2026, 9, 17)
    )

    assert [
        item.code
        for item in september_16
    ] == ["OP-ACT-007"]

    assert september_17 == []


def test_should_exclude_activity_starting_exactly_at_next_day(
    repository,
):

    activity = OperationalActivity(
        code="OP-ACT-008",
        description=(
            "Actividad iniciada exactamente "
            "al comenzar el d?a siguiente"
        ),
        started_at=datetime(
            2026, 9, 18, 0, 0
        ),
        ended_at=datetime(
            2026, 9, 18, 1, 0
        ),
        source=OperationalActivitySource.MANUAL,
        created_at=datetime(
            2026, 9, 18, 0, 0
        ),
        created_by_person_code="TECH-001",
    )

    repository.save(activity)

    september_17 = repository.list_by_date(
        date(2026, 9, 17)
    )

    september_18 = repository.list_by_date(
        date(2026, 9, 18)
    )

    assert september_17 == []

    assert [
        item.code
        for item in september_18
    ] == ["OP-ACT-008"]
