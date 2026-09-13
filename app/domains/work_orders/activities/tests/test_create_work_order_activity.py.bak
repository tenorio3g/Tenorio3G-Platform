from datetime import datetime

import pytest

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.work_orders.activities.repositories import (
    InMemoryWorkOrderActivityRepository,
)

from app.domains.work_orders.activities.use_cases import (
    CreateWorkOrderActivity,
    CreateWorkOrderActivityCommand,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)


def create_work_order():

    return WorkOrder(
        code="WO-001",
        title="Orden de prueba",
        description="Prueba.",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code="ASSET-001",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            8,
            16,
            10,
            0,
        ),
    )


def build_use_case():

    activity_repository = (
        InMemoryWorkOrderActivityRepository()
    )

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    use_case = CreateWorkOrderActivity(
        activity_repository,
        work_order_repository,
        person_repository,
    )

    return (
        activity_repository,
        work_order_repository,
        person_repository,
        use_case,
    )


def create_command():

    return CreateWorkOrderActivityCommand(
        code="ACT-001",
        work_order_code="WO-001",
        title="Inspección visual",
        responsible_person_code="55464",
        description="Revisar conexiones.",
        estimated_minutes=30,
    )


def test_should_create_work_order_activity():

    (
        activity_repository,
        work_order_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
            position="Supervisor",
        )
    )

    result = use_case.execute(
        create_command()
    )

    assert (
        result.activity.code
        == "ACT-001"
    )

    persisted = (
        activity_repository.get_by_code(
            "ACT-001"
        )
    )

    assert persisted is not None

    assert (
        persisted.work_order_code
        == "WO-001"
    )


def test_should_reject_unknown_work_order():

    (
        _,
        _,
        person_repository,
        use_case,
    ) = build_use_case()

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
        )
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_unknown_responsible_person():

    (
        _,
        work_order_repository,
        _,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    with pytest.raises(
        ValueError,
        match="responsible person not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_inactive_responsible_person():

    (
        _,
        work_order_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
            is_active=False,
        )
    )

    with pytest.raises(
        ValueError,
        match="responsible person is inactive",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_duplicate_activity_code():

    (
        _,
        work_order_repository,
        person_repository,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
        )
    )

    use_case.execute(
        create_command()
    )

    with pytest.raises(
        ValueError,
        match="activity code already exists",
    ):
        use_case.execute(
            create_command()
        )