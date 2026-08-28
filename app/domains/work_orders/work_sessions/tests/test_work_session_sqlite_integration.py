from datetime import datetime

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    SQLitePersonRepository,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    SQLiteWorkOrderRepository,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.repositories import (
    SQLiteWorkOrderActivityRepository,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)

from app.domains.work_orders.work_sessions.audit.repositories import (
    SQLiteWorkSessionAuditRepository,
)

from app.domains.work_orders.work_sessions.audit.value_objects import (
    WorkSessionAuditEventType,
)

from app.domains.work_orders.work_sessions.repositories import (
    SQLiteWorkSessionRepository,
)

from app.domains.work_orders.work_sessions.use_cases import (
    AddManualWorkSession,
    AddManualWorkSessionCommand,
    CorrectManualWorkSession,
    CorrectManualWorkSessionCommand,
    EndWorkSession,
    EndWorkSessionCommand,
    StartWorkSession,
    StartWorkSessionCommand,
)

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)


@pytest.fixture
def repositories(tmp_path):

    database_path = (
        tmp_path
        / "work_sessions_integration_test.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}",
        future=True,
    )

    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(
        engine
    )

    person_repository = (
        SQLitePersonRepository(
            session_factory
        )
    )

    work_order_repository = (
        SQLiteWorkOrderRepository(
            session_factory
        )
    )

    activity_repository = (
        SQLiteWorkOrderActivityRepository(
            session_factory
        )
    )

    work_session_repository = (
        SQLiteWorkSessionRepository(
            session_factory
        )
    )

    audit_repository = (
        SQLiteWorkSessionAuditRepository(
            session_factory
        )
    )

    yield {
        "person": person_repository,
        "work_order": work_order_repository,
        "activity": activity_repository,
        "work_session": work_session_repository,
        "audit": audit_repository,
    }

    Base.metadata.drop_all(
        engine
    )

    engine.dispose()


def create_person() -> Person:

    return Person(
        code="TECH-001",
        name="Angel",
        position="Technician",
    )


def create_assigned_work_order() -> WorkOrder:

    work_order = WorkOrder(
        code="WO-001",
        title="Inspeccion general",
        description="Inspeccion de equipo.",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code="ASSET-001",
        requester_person_code="TECH-001",
        supervisor_person_code="TECH-001",
        created_at=datetime(
            2026,
            8,
            26,
            6,
            30,
        ),
    )

    work_order.approve()
    work_order.assign()

    return work_order


def create_activity() -> WorkOrderActivity:

    return WorkOrderActivity(
        code="ACT-001",
        work_order_code="WO-001",
        title="Revision electrica",
        description="Revisar conexiones.",
        responsible_person_code="TECH-001",
        estimated_minutes=120,
    )


def prepare_base_data(
    repositories,
):

    repositories["person"].save(
        create_person()
    )

    repositories["work_order"].save(
        create_assigned_work_order()
    )

    repositories["activity"].save(
        create_activity()
    )


def test_should_execute_complete_automatic_work_session_flow(
    repositories,
):

    prepare_base_data(
        repositories
    )

    start_work_session = (
        StartWorkSession(
            repositories["work_order"],
            repositories["activity"],
            repositories["person"],
            repositories["work_session"],
        )
    )

    end_work_session = (
        EndWorkSession(
            repositories["work_session"],
            repositories["person"],
        )
    )

    started_at = datetime(
        2026,
        8,
        26,
        7,
        0,
    )

    start_result = (
        start_work_session.execute(
            StartWorkSessionCommand(
                code="WS-AUTO-001",
                work_order_code="WO-001",
                activity_code="ACT-001",
                person_code="TECH-001",
                started_at=started_at,
                created_at=started_at,
                created_by_person_code=(
                    "TECH-001"
                ),
            )
        )
    )

    started_session = (
        start_result.work_session
    )

    assert (
        started_session.source
        == WorkSessionSource.AUTOMATIC
    )

    assert started_session.is_active is True

    persisted_work_order = (
        repositories["work_order"]
        .get_by_code(
            "WO-001"
        )
    )

    assert persisted_work_order is not None

    assert (
        persisted_work_order.status
        == WorkOrderStatus.IN_PROGRESS
    )

    persisted_activity = (
        repositories["activity"]
        .get_by_code(
            "ACT-001"
        )
    )

    assert persisted_activity is not None

    assert (
        persisted_activity.status
        == ActivityStatus.IN_PROGRESS
    )

    persisted_started_session = (
        repositories["work_session"]
        .get_by_code(
            "WS-AUTO-001"
        )
    )

    assert (
        persisted_started_session
        is not None
    )

    assert (
        persisted_started_session.is_active
        is True
    )

    ended_at = datetime(
        2026,
        8,
        26,
        9,
        30,
    )

    end_work_session.execute(
        EndWorkSessionCommand(
            code="WS-AUTO-001",
            ended_at=ended_at,
            actor_person_code="TECH-001",
        )
    )

    persisted_ended_session = (
        repositories["work_session"]
        .get_by_code(
            "WS-AUTO-001"
        )
    )

    assert persisted_ended_session is not None

    assert (
        persisted_ended_session.is_active
        is False
    )

    assert (
        persisted_ended_session.ended_at
        == ended_at
    )

    assert (
        persisted_ended_session.duration_minutes
        == 150
    )

    assert (
        repositories["work_session"]
        .get_active_by_person(
            "TECH-001"
        )
        is None
    )


def test_should_execute_complete_manual_work_session_audit_flow(
    repositories,
):

    prepare_base_data(
        repositories
    )

    add_manual_work_session = (
        AddManualWorkSession(
            repositories["work_order"],
            repositories["activity"],
            repositories["person"],
            repositories["work_session"],
            repositories["audit"],
        )
    )

    correct_manual_work_session = (
        CorrectManualWorkSession(
            repositories["work_session"],
            repositories["person"],
            repositories["audit"],
        )
    )

    original_started_at = datetime(
        2026,
        8,
        26,
        10,
        0,
    )

    original_ended_at = datetime(
        2026,
        8,
        26,
        11,
        0,
    )

    created_at = datetime(
        2026,
        8,
        26,
        12,
        0,
    )

    add_result = (
        add_manual_work_session.execute(
            AddManualWorkSessionCommand(
                code="WS-MAN-001",
                work_order_code="WO-001",
                activity_code="ACT-001",
                person_code="TECH-001",
                started_at=original_started_at,
                ended_at=original_ended_at,
                created_at=created_at,
                created_by_person_code=(
                    "TECH-001"
                ),
                reason=(
                    "Registro manual de trabajo."
                ),
            )
        )
    )

    manual_session = (
        add_result.work_session
    )

    assert (
        manual_session.source
        == WorkSessionSource.MANUAL
    )

    assert manual_session.is_active is False

    persisted_manual_session = (
        repositories["work_session"]
        .get_by_code(
            "WS-MAN-001"
        )
    )

    assert persisted_manual_session is not None

    assert (
        persisted_manual_session.started_at
        == original_started_at
    )

    assert (
        persisted_manual_session.ended_at
        == original_ended_at
    )

    audit_entries = (
        repositories["audit"]
        .list_by_work_session(
            "WS-MAN-001"
        )
    )

    assert len(audit_entries) == 1

    assert (
        audit_entries[0].event_type
        == WorkSessionAuditEventType.MANUAL_CREATED
    )

    corrected_started_at = datetime(
        2026,
        8,
        26,
        9,
        45,
    )

    corrected_ended_at = datetime(
        2026,
        8,
        26,
        11,
        15,
    )

    corrected_at = datetime(
        2026,
        8,
        26,
        13,
        0,
    )

    correction_result = (
        correct_manual_work_session.execute(
            CorrectManualWorkSessionCommand(
                code="WS-MAN-001",
                started_at=corrected_started_at,
                ended_at=corrected_ended_at,
                corrected_at=corrected_at,
                corrected_by_person_code=(
                    "TECH-001"
                ),
                reason=(
                    "Correccion de horario."
                ),
            )
        )
    )

    corrected_session = (
        correction_result.work_session
    )

    assert (
        corrected_session.started_at
        == corrected_started_at
    )

    assert (
        corrected_session.ended_at
        == corrected_ended_at
    )

    persisted_corrected_session = (
        repositories["work_session"]
        .get_by_code(
            "WS-MAN-001"
        )
    )

    assert (
        persisted_corrected_session
        is not None
    )

    assert (
        persisted_corrected_session.started_at
        == corrected_started_at
    )

    assert (
        persisted_corrected_session.ended_at
        == corrected_ended_at
    )

    assert (
        persisted_corrected_session.duration_minutes
        == 90
    )

    audit_entries = (
        repositories["audit"]
        .list_by_work_session(
            "WS-MAN-001"
        )
    )

    assert len(audit_entries) == 2

    assert [
        entry.event_type
        for entry in audit_entries
    ] == [
        WorkSessionAuditEventType.MANUAL_CREATED,
        WorkSessionAuditEventType.CORRECTED,
    ]

    correction_audit = audit_entries[1]

    assert (
        correction_audit.previous_started_at
        == original_started_at
    )

    assert (
        correction_audit.previous_ended_at
        == original_ended_at
    )

    assert (
        correction_audit.new_started_at
        == corrected_started_at
    )

    assert (
        correction_audit.new_ended_at
        == corrected_ended_at
    )

    assert (
        correction_audit.actor_person_code
        == "TECH-001"
    )

    assert (
        correction_audit.reason
        == "Correccion de horario."
    )
