from datetime import datetime

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from app.domains.work_orders.technicians.repositories import (
    InMemoryWorkOrderTechnicianAssignmentRepository,
)

from app.domains.work_orders.technicians.use_cases import (
    ListWorkOrderTechnicians,
    ListWorkOrderTechniciansQuery,
)


def test_should_list_work_order_technicians():

    assignment_repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    assignment_repository.save(
        WorkOrderTechnicianAssignment(
            work_order_code="WO-001",
            person_code="55464",
            assigned_at=datetime(
                2026,
                8,
                16,
                0,
                0,
            ),
        )
    )

    person_repository.save(
        Person(
            code="55464",
            name="Fortunato",
            position="Técnico",
        )
    )

    use_case = ListWorkOrderTechnicians(
        assignment_repository,
        person_repository,
    )

    result = use_case.execute(
        ListWorkOrderTechniciansQuery(
            work_order_code="WO-001"
        )
    )

    assert len(result.items) == 1

    item = result.items[0]

    assert (
        item.assignment.work_order_code
        == "WO-001"
    )

    assert (
        item.assignment.person_code
        == "55464"
    )

    assert item.person.name == "Fortunato"


def test_should_return_empty_list_when_no_assignments():

    assignment_repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    use_case = ListWorkOrderTechnicians(
        assignment_repository,
        person_repository,
    )

    result = use_case.execute(
        ListWorkOrderTechniciansQuery(
            work_order_code="WO-001"
        )
    )

    assert result.items == []


def test_should_ignore_missing_person():

    assignment_repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    assignment_repository.save(
        WorkOrderTechnicianAssignment(
            work_order_code="WO-001",
            person_code="999",
            assigned_at=datetime(
                2026,
                8,
                16,
            ),
        )
    )

    use_case = ListWorkOrderTechnicians(
        assignment_repository,
        person_repository,
    )

    result = use_case.execute(
        ListWorkOrderTechniciansQuery(
            work_order_code="WO-001"
        )
    )

    assert result.items == []