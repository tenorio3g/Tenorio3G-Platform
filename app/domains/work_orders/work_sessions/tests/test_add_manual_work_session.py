from datetime import datetime

import pytest

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.repositories import (
    InMemoryWorkOrderActivityRepository,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from app.domains.work_orders.work_sessions.repositories import (
    InMemoryWorkSessionRepository,
)

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)

from app.domains.work_orders.work_sessions.audit.repositories import (
    InMemoryWorkSessionAuditRepository,
)

from app.domains.work_orders.work_sessions.audit.value_objects import (
    WorkSessionAuditEventType,
)

from app.domains.work_orders.work_sessions.use_cases import (
    AddManualWorkSession,
    AddManualWorkSessionCommand,
)


def dt(
    hour: int,
    minute: int = 0,
) -> datetime:

    return datetime(
        2026,
        8,
        26,
        hour,
        minute,
    )


def create_work_order(
    *,
    code: str = "WO-001",
    status: WorkOrderStatus = WorkOrderStatus.IN_PROGRESS,
) -> WorkOrder:

    return WorkOrder(
        code=code,
        title="Orden de prueba",
        description="",
        work_type="CORRECTIVE",
        priority="NORMAL",
        asset_code=None,
        requester_person_code="REQ-001",
        supervisor_person_code=None,
        created_at=dt(7),
        status=status,
    )


def create_activity(
    *,
    code: str = "ACT-001",
    work_order_code: str = "WO-001",
    status: ActivityStatus = ActivityStatus.IN_PROGRESS,
) -> WorkOrderActivity:

    started_at = None
    completed_at = None

    if status == ActivityStatus.IN_PROGRESS:
        started_at = dt(7)

    if status == ActivityStatus.COMPLETED:
        started_at = dt(7)
        completed_at = dt(8)

    return WorkOrderActivity(
        code=code,
        work_order_code=work_order_code,
        title="Actividad de prueba",
        responsible_person_code="TECH-001",
        description="",
        estimated_minutes=60,
        status=status,
        started_at=started_at,
        completed_at=completed_at,
    )


def create_person(
    *,
    code: str = "TECH-001",
    active: bool = True,
) -> Person:

    return Person(
        code=code,
        name="Técnico de prueba",
        position="Técnico",
        is_active=active,
    )


def create_existing_session(
    *,
    code: str = "WS-OLD",
    person_code: str = "TECH-001",
    started_at=None,
    ended_at=None,
) -> WorkSession:

    return WorkSession(
        code=code,
        work_order_code="WO-OTHER",
        activity_code="ACT-OTHER",
        person_code=person_code,
        started_at=started_at or dt(7),
        ended_at=ended_at,
        source=WorkSessionSource.AUTOMATIC,
        created_at=started_at or dt(7),
        created_by_person_code=person_code,
    )


def create_use_case():

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    activity_repository = (
        InMemoryWorkOrderActivityRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    work_session_repository = (
        InMemoryWorkSessionRepository()
    )

    audit_repository = (
        InMemoryWorkSessionAuditRepository()
    )

    use_case = AddManualWorkSession(
        work_order_repository=(
            work_order_repository
        ),
        activity_repository=(
            activity_repository
        ),
        person_repository=(
            person_repository
        ),
        work_session_repository=(
            work_session_repository
        ),
        audit_repository=(
            audit_repository
        ),
    )

    return (
        use_case,
        work_order_repository,
        activity_repository,
        person_repository,
        work_session_repository,
        audit_repository,
    )

def prepare_context(
    *,
    work_order_status=WorkOrderStatus.IN_PROGRESS,
    activity_status=ActivityStatus.IN_PROGRESS,
):

    (
        use_case,
        work_order_repository,
        activity_repository,
        person_repository,
        work_session_repository,
        audit_repository,
    ) = create_use_case()

    work_order_repository.save(
        create_work_order(
            status=work_order_status,
        )
    )

    activity_repository.save(
        create_activity(
            status=activity_status,
        )
    )

    person_repository.save(
        create_person()
    )

    return (
        use_case,
        work_order_repository,
        activity_repository,
        person_repository,
        work_session_repository,
    )


def create_command(
    *,
    code: str = "WS-MAN-001",
    work_order_code: str = "WO-001",
    activity_code: str = "ACT-001",
    person_code: str = "TECH-001",
    started_at=None,
    ended_at=None,
    created_by_person_code: str = "SUP-001",
    reason: str = "Trabajo no registrado durante la intervención",
):

    return AddManualWorkSessionCommand(
        code=code,
        work_order_code=work_order_code,
        activity_code=activity_code,
        person_code=person_code,
        started_at=started_at or dt(9),
        ended_at=ended_at or dt(10),
        created_at=dt(14),
        created_by_person_code=(
            created_by_person_code
        ),
        reason=reason,
    )


def test_should_add_manual_work_session():

    (
        use_case,
        _,
        _,
        _,
        repository,
    ) = prepare_context()

    result = use_case.execute(
        create_command()
    )

    session = result.work_session

    assert session.code == "WS-MAN-001"
    assert session.work_order_code == "WO-001"
    assert session.activity_code == "ACT-001"
    assert session.person_code == "TECH-001"

    assert (
        session.source
        == WorkSessionSource.MANUAL
    )

    assert session.started_at == dt(9)
    assert session.ended_at == dt(10)
    assert session.duration_minutes == 60
    assert session.is_active is False

    stored = repository.get_by_code(
        "WS-MAN-001"
    )

    assert stored is not None


def test_should_allow_manual_session_created_by_another_person():

    (
        use_case,
        _,
        _,
        _,
        _,
    ) = prepare_context()

    result = use_case.execute(
        create_command(
            person_code="TECH-001",
            created_by_person_code="SUP-001",
        )
    )

    assert (
        result.work_session.person_code
        == "TECH-001"
    )

    assert (
        result.work_session.created_by_person_code
        == "SUP-001"
    )


def test_should_allow_manual_session_for_completed_activity():

    (
        use_case,
        _,
        _,
        _,
        _,
    ) = prepare_context(
        activity_status=(
            ActivityStatus.COMPLETED
        )
    )

    result = use_case.execute(
        create_command()
    )

    assert result.work_session.is_active is False


def test_should_allow_manual_session_for_closed_work_order():

    (
        use_case,
        _,
        _,
        _,
        _,
    ) = prepare_context(
        work_order_status=(
            WorkOrderStatus.CLOSED
        ),
        activity_status=(
            ActivityStatus.COMPLETED
        ),
    )

    result = use_case.execute(
        create_command()
    )

    assert result.work_session.is_active is False


def test_should_not_change_work_order_status():

    (
        use_case,
        work_order_repository,
        _,
        _,
        _,
    ) = prepare_context(
        work_order_status=(
            WorkOrderStatus.CLOSED
        ),
        activity_status=(
            ActivityStatus.COMPLETED
        ),
    )

    use_case.execute(
        create_command()
    )

    work_order = work_order_repository.get_by_code(
        "WO-001"
    )

    assert work_order is not None

    assert (
        work_order.status
        == WorkOrderStatus.CLOSED
    )


def test_should_not_change_activity_status_or_dates():

    (
        use_case,
        _,
        activity_repository,
        _,
        _,
    ) = prepare_context(
        activity_status=(
            ActivityStatus.COMPLETED
        )
    )

    before = activity_repository.get_by_code(
        "ACT-001"
    )

    original_status = before.status
    original_started_at = before.started_at
    original_completed_at = before.completed_at

    use_case.execute(
        create_command()
    )

    after = activity_repository.get_by_code(
        "ACT-001"
    )

    assert after.status == original_status
    assert after.started_at == original_started_at
    assert (
        after.completed_at
        == original_completed_at
    )


def test_should_allow_historical_manual_session_before_active_session():

    (
        use_case,
        _,
        _,
        _,
        repository,
    ) = prepare_context()

    repository.save(
        create_existing_session(
            code="WS-ACTIVE",
            started_at=dt(13),
            ended_at=None,
        )
    )

    result = use_case.execute(
        create_command(
            started_at=dt(9),
            ended_at=dt(10),
        )
    )

    assert result.work_session.is_active is False


def test_should_reject_missing_work_order():

    (
        use_case,
        _,
        activity_repository,
        person_repository,
        _,
        _,
    ) = create_use_case()

    activity_repository.save(
        create_activity()
    )

    person_repository.save(
        create_person()
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_missing_activity():

    (
        use_case,
        work_order_repository,
        _,
        person_repository,
        _,
        _,
    ) = create_use_case()

    work_order_repository.save(
        create_work_order()
    )

    person_repository.save(
        create_person()
    )

    with pytest.raises(
        ValueError,
        match="activity not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_activity_from_another_work_order():

    (
        use_case,
        work_order_repository,
        activity_repository,
        person_repository,
        _,
        _,
    ) = create_use_case()

    work_order_repository.save(
        create_work_order(
            code="WO-001",
        )
    )

    activity_repository.save(
        create_activity(
            work_order_code="WO-002",
        )
    )

    person_repository.save(
        create_person()
    )

    with pytest.raises(
        ValueError,
        match=(
            "activity does not belong "
            "to work order"
        ),
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_missing_person():

    (
        use_case,
        work_order_repository,
        activity_repository,
        _,
        _,
        _,
    ) = create_use_case()

    work_order_repository.save(
        create_work_order()
    )

    activity_repository.save(
        create_activity()
    )

    with pytest.raises(
        ValueError,
        match="person not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_inactive_person():

    (
        use_case,
        work_order_repository,
        activity_repository,
        person_repository,
        _,
        _,
    ) = create_use_case()

    work_order_repository.save(
        create_work_order()
    )

    activity_repository.save(
        create_activity()
    )

    person_repository.save(
        create_person(
            active=False,
        )
    )

    with pytest.raises(
        ValueError,
        match="person is not active",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_duplicate_work_session_code():

    (
        use_case,
        _,
        _,
        _,
        repository,
    ) = prepare_context()

    repository.save(
        create_existing_session(
            code="WS-MAN-001",
            started_at=dt(7),
            ended_at=dt(8),
        )
    )

    with pytest.raises(
        ValueError,
        match="work session code already exists",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_overlapping_manual_session():

    (
        use_case,
        _,
        _,
        _,
        repository,
    ) = prepare_context()

    repository.save(
        create_existing_session(
            started_at=dt(8),
            ended_at=dt(9, 30),
        )
    )

    with pytest.raises(
        ValueError,
        match="work session overlaps existing session",
    ):
        use_case.execute(
            create_command(
                started_at=dt(9),
                ended_at=dt(10),
            )
        )


def test_should_allow_touching_time_boundaries():

    (
        use_case,
        _,
        _,
        _,
        repository,
    ) = prepare_context()

    repository.save(
        create_existing_session(
            started_at=dt(7),
            ended_at=dt(9),
        )
    )

    result = use_case.execute(
        create_command(
            started_at=dt(9),
            ended_at=dt(10),
        )
    )

    assert result.work_session.started_at == dt(9)


def test_should_reject_empty_reason():

    (
        use_case,
        _,
        _,
        _,
        _,
    ) = prepare_context()

    with pytest.raises(
        ValueError,
        match="reason is required",
    ):
        use_case.execute(
            create_command(
                reason="   ",
            )
        )






def test_should_create_audit_entry_for_manual_session():

    (
        use_case,
        work_order_repository,
        activity_repository,
        person_repository,
        work_session_repository,
        audit_repository,
    ) = create_use_case()

    work_order_repository.save(
        create_work_order()
    )

    activity_repository.save(
        create_activity()
    )

    person_repository.save(
        create_person()
    )

    command = create_command(
        code="WS-MAN-AUDIT-001",
        created_by_person_code="SUP-001",
        reason="Emergencia capturada posteriormente",
    )

    use_case.execute(command)

    entries = (
        audit_repository.list_by_work_session(
            "WS-MAN-AUDIT-001"
        )
    )

    assert len(entries) == 1

    entry = entries[0]

    assert (
        entry.work_session_code
        == "WS-MAN-AUDIT-001"
    )

    assert (
        entry.event_type
        == WorkSessionAuditEventType.MANUAL_CREATED
    )

    assert (
        entry.reason
        == "Emergencia capturada posteriormente"
    )

    assert (
        entry.actor_person_code
        == "SUP-001"
    )

    assert entry.occurred_at == dt(14)


def test_should_store_trimmed_reason_in_manual_session_audit():

    (
        use_case,
        work_order_repository,
        activity_repository,
        person_repository,
        work_session_repository,
        audit_repository,
    ) = create_use_case()

    work_order_repository.save(
        create_work_order()
    )

    activity_repository.save(
        create_activity()
    )

    person_repository.save(
        create_person()
    )

    command = create_command(
        code="WS-MAN-AUDIT-002",
        reason="   Trabajo capturado manualmente   ",
    )

    use_case.execute(command)

    entries = (
        audit_repository.list_by_work_session(
            "WS-MAN-AUDIT-002"
        )
    )

    assert len(entries) == 1

    assert (
        entries[0].reason
        == "Trabajo capturado manualmente"
    )
