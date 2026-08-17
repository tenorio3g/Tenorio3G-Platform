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

from app.domains.work_orders.technicians.repositories import (
    InMemoryWorkOrderTechnicianAssignmentRepository,
)

from app.domains.work_orders.technicians.use_cases import (
    AssignTechnicianToWorkOrder,
    AssignTechnicianToWorkOrderCommand,
)


def build_use_case():

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    assignment_repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    use_case = AssignTechnicianToWorkOrder(
        work_order_repository,
        person_repository,
        assignment_repository,
    )

    return (
        work_order_repository,
        person_repository,
        assignment_repository,
        use_case,
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
            15,
            23,
            0,
        ),
    )


def test_should_assign_technician():

    (
        work_order_repository,
        person_repository,
        assignment_repository,
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

    result = use_case.execute(
        AssignTechnicianToWorkOrderCommand(
            work_order_code="WO-001",
            person_code="55464",
            assigned_at=datetime(
                2026,
                8,
                15,
                23,
                30,
            ),
        )
    )

    assert (
        result.assignment.work_order_code
        == "WO-001"
    )

    assert (
        result.assignment.person_code
        == "55464"
    )

    assert assignment_repository.exists(
        "WO-001",
        "55464",
    ) is True


def test_should_reject_unknown_work_order():

    _, person_repository, _, use_case = (
        build_use_case()
    )

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
            AssignTechnicianToWorkOrderCommand(
                work_order_code="WO-404",
                person_code="55464",
                assigned_at=datetime(
                    2026,
                    8,
                    15,
                ),
            )
        )


def test_should_reject_unknown_technician():

    (
        work_order_repository,
        _,
        _,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    with pytest.raises(
        ValueError,
        match="technician not found",
    ):
        use_case.execute(
            AssignTechnicianToWorkOrderCommand(
                work_order_code="WO-001",
                person_code="999",
                assigned_at=datetime(
                    2026,
                    8,
                    15,
                ),
            )
        )


def test_should_reject_inactive_technician():

    (
        work_order_repository,
        person_repository,
        _,
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
        match="technician is inactive",
    ):
        use_case.execute(
            AssignTechnicianToWorkOrderCommand(
                work_order_code="WO-001",
                person_code="55464",
                assigned_at=datetime(
                    2026,
                    8,
                    15,
                ),
            )
        )


def test_should_reject_duplicate_assignment():

    (
        work_order_repository,
        person_repository,
        _,
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

    command = AssignTechnicianToWorkOrderCommand(
        work_order_code="WO-001",
        person_code="55464",
        assigned_at=datetime(
            2026,
            8,
            15,
            23,
            30,
        ),
    )

    use_case.execute(
        command
    )

    with pytest.raises(
        ValueError,
        match=(
            "technician already assigned to work order"
        ),
    ):
        use_case.execute(
            command
        )