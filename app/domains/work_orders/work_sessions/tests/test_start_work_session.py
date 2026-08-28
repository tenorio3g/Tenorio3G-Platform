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

from app.domains.work_orders.work_sessions.use_cases import (
    StartWorkSession,
    StartWorkSessionCommand,
)


NOW = datetime(
    2026,
    8,
    26,
    7,
    0,
)


def create_work_order(
    *,
    code: str = "WO-001",
    status: WorkOrderStatus = WorkOrderStatus.ASSIGNED,
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
        created_at=NOW,
        status=status,
    )


def create_activity(
    *,
    code: str = "ACT-001",
    work_order_code: str = "WO-001",
    status: ActivityStatus = ActivityStatus.PENDING,
) -> WorkOrderActivity:

    started_at = None
    completed_at = None

    if status == ActivityStatus.IN_PROGRESS:
        started_at = datetime(
            2026,
            8,
            26,
            6,
            30,
        )

    if status == ActivityStatus.COMPLETED:
        started_at = datetime(
            2026,
            8,
            26,
            6,
            30,
        )

        completed_at = datetime(
            2026,
            8,
            26,
            6,
            50,
        )

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


def create_active_session(
    *,
    code: str = "WS-ACTIVE",
    person_code: str = "TECH-001",
) -> WorkSession:

    return WorkSession(
        code=code,
        work_order_code="WO-OTHER",
        activity_code="ACT-OTHER",
        person_code=person_code,
        started_at=NOW,
        source=WorkSessionSource.AUTOMATIC,
        created_at=NOW,
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

    use_case = StartWorkSession(
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
    code: str = "WS-001",
    work_order_code: str = "WO-001",
    activity_code: str = "ACT-001",
    person_code: str = "TECH-001",
) -> StartWorkSessionCommand:

    return StartWorkSessionCommand(
        code=code,
        work_order_code=work_order_code,
        activity_code=activity_code,
        person_code=person_code,
        started_at=NOW,
        created_at=NOW,
        created_by_person_code="TECH-001",
    )


def prepare_valid_context(
    *,
    work_order_status: WorkOrderStatus = (
        WorkOrderStatus.ASSIGNED
    ),
    activity_status: ActivityStatus = (
        ActivityStatus.PENDING
    ),
):

    (
        use_case,
        work_order_repository,
        activity_repository,
        person_repository,
        work_session_repository,
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


def test_should_start_work_session_from_assigned_work_order():

    (
        use_case,
        work_order_repository,
        activity_repository,
        _,
        work_session_repository,
    ) = prepare_valid_context()

    result = use_case.execute(
        create_command()
    )

    session = result.work_session

    assert session.code == "WS-001"
    assert session.work_order_code == "WO-001"
    assert session.activity_code == "ACT-001"
    assert session.person_code == "TECH-001"

    assert (
        session.source
        == WorkSessionSource.AUTOMATIC
    )

    assert session.is_active is True

    work_order = work_order_repository.get_by_code(
        "WO-001"
    )

    assert work_order is not None

    assert (
        work_order.status
        == WorkOrderStatus.IN_PROGRESS
    )

    activity = activity_repository.get_by_code(
        "ACT-001"
    )

    assert activity is not None

    assert (
        activity.status
        == ActivityStatus.IN_PROGRESS
    )

    assert activity.started_at == NOW

    stored_session = (
        work_session_repository.get_by_code(
            "WS-001"
        )
    )

    assert stored_session is not None


def test_should_start_session_when_work_order_already_in_progress():

    (
        use_case,
        work_order_repository,
        _,
        _,
        _,
    ) = prepare_valid_context(
        work_order_status=(
            WorkOrderStatus.IN_PROGRESS
        ),
        activity_status=(
            ActivityStatus.PENDING
        ),
    )

    result = use_case.execute(
        create_command()
    )

    assert result.work_session.is_active is True

    work_order = work_order_repository.get_by_code(
        "WO-001"
    )

    assert work_order is not None

    assert (
        work_order.status
        == WorkOrderStatus.IN_PROGRESS
    )


def test_should_start_session_for_activity_already_in_progress():

    (
        use_case,
        _,
        activity_repository,
        _,
        _,
    ) = prepare_valid_context(
        work_order_status=(
            WorkOrderStatus.IN_PROGRESS
        ),
        activity_status=(
            ActivityStatus.IN_PROGRESS
        ),
    )

    original_started_at = (
        activity_repository
        .get_by_code(
            "ACT-001"
        )
        .started_at
    )

    result = use_case.execute(
        create_command()
    )

    assert result.work_session.is_active is True

    activity = activity_repository.get_by_code(
        "ACT-001"
    )

    assert activity is not None

    assert (
        activity.started_at
        == original_started_at
    )


def test_should_allow_person_not_assigned_to_work_order():

    (
        use_case,
        _,
        _,
        person_repository,
        _,
    ) = prepare_valid_context()

    person_repository.save(
        create_person(
            code="TECH-002",
        )
    )

    result = use_case.execute(
        create_command(
            person_code="TECH-002",
        )
    )

    assert (
        result.work_session.person_code
        == "TECH-002"
    )


def test_should_reject_missing_work_order():

    (
        use_case,
        _,
        activity_repository,
        person_repository,
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


def test_should_reject_work_order_not_ready_for_execution():

    (
        use_case,
        _,
        _,
        _,
        _,
    ) = prepare_valid_context(
        work_order_status=(
            WorkOrderStatus.APPROVED
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "work order cannot start "
            "session from current status"
        ),
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


def test_should_reject_person_with_active_session():

    (
        use_case,
        _,
        _,
        _,
        work_session_repository,
    ) = prepare_valid_context()

    work_session_repository.save(
        create_active_session()
    )

    with pytest.raises(
        ValueError,
        match=(
            "person already has an "
            "active work session"
        ),
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_completed_activity():

    (
        use_case,
        _,
        _,
        _,
        _,
    ) = prepare_valid_context(
        work_order_status=(
            WorkOrderStatus.IN_PROGRESS
        ),
        activity_status=(
            ActivityStatus.COMPLETED
        ),
    )

    with pytest.raises(
        ValueError,
        match=(
            "cannot start work session "
            "for completed activity"
        ),
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
        work_session_repository,
    ) = prepare_valid_context()

    work_session_repository.save(
        WorkSession(
            code="WS-001",
            work_order_code="WO-OLD",
            activity_code="ACT-OLD",
            person_code="TECH-OTHER",
            started_at=datetime(
                2026,
                8,
                25,
                7,
                0,
            ),
            ended_at=datetime(
                2026,
                8,
                25,
                8,
                0,
            ),
            source=(
                WorkSessionSource.AUTOMATIC
            ),
            created_at=datetime(
                2026,
                8,
                25,
                7,
                0,
            ),
            created_by_person_code=(
                "TECH-OTHER"
            ),
        )
    )

    with pytest.raises(
        ValueError,
        match="work session code already exists",
    ):
        use_case.execute(
            create_command(
                code="WS-001",
            )
        )
