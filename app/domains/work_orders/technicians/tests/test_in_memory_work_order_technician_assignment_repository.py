from datetime import datetime

import pytest

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from app.domains.work_orders.technicians.repositories import (
    InMemoryWorkOrderTechnicianAssignmentRepository,
)


def create_assignment(
    work_order_code="WO-001",
    person_code="55464",
):

    return WorkOrderTechnicianAssignment(
        work_order_code=work_order_code,
        person_code=person_code,
        assigned_at=datetime(
            2026,
            8,
            15,
            23,
            0,
        ),
    )


def test_should_save_assignment():

    repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    repository.save(
        create_assignment()
    )

    assert repository.exists(
        "WO-001",
        "55464",
    ) is True


def test_exists_should_normalize_values():

    repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    repository.save(
        create_assignment()
    )

    assert repository.exists(
        " wo-001 ",
        " 55464 ",
    ) is True


def test_should_reject_duplicate_assignment():

    repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    assignment = create_assignment()

    repository.save(
        assignment
    )

    with pytest.raises(
        ValueError,
        match=(
            "technician already assigned to work order"
        ),
    ):
        repository.save(
            assignment
        )


def test_should_list_assignments_by_work_order():

    repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    repository.save(
        create_assignment(
            work_order_code="WO-001",
            person_code="55464",
        )
    )

    repository.save(
        create_assignment(
            work_order_code="WO-001",
            person_code="12",
        )
    )

    repository.save(
        create_assignment(
            work_order_code="WO-002",
            person_code="999",
        )
    )

    result = repository.list_by_work_order(
        " wo-001 "
    )

    assert len(result) == 2

    assert {
        item.person_code
        for item in result
    } == {
        "55464",
        "12",
    }


def test_should_delete_assignment():

    repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    repository.save(
        create_assignment()
    )

    repository.delete(
        " wo-001 ",
        " 55464 ",
    )

    assert repository.exists(
        "WO-001",
        "55464",
    ) is False