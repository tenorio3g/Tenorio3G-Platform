from datetime import datetime

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from app.domains.work_orders.technicians.repositories import (
    SQLiteWorkOrderTechnicianAssignmentRepository,
)


def build_repository(
    tmp_path,
):

    database_path = (
        tmp_path
        / "technician_assignments_test.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}",
        future=True,
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(
        engine
    )

    repository = (
        SQLiteWorkOrderTechnicianAssignmentRepository(
            SessionLocal
        )
    )

    return repository, engine


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
            16,
            0,
            0,
        ),
    )


def test_should_save_and_find_assignment(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    repository.save(
        create_assignment()
    )

    assert repository.exists(
        "WO-001",
        "55464",
    ) is True

    engine.dispose()


def test_should_reject_duplicate_assignment(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
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

    engine.dispose()


def test_should_list_assignments_by_work_order(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
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

    engine.dispose()


def test_should_delete_assignment(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    repository.save(
        create_assignment()
    )

    repository.delete(
        "WO-001",
        "55464",
    )

    assert repository.exists(
        "WO-001",
        "55464",
    ) is False

    engine.dispose()

def test_should_unassign_without_deleting_history(
    tmp_path,
):

    repository, engine = (
        build_repository(
            tmp_path
        )
    )

    assignment = WorkOrderTechnicianAssignment(
        work_order_code="WO-001",
        person_code="55464",
        assigned_at=datetime(
            2026,
            8,
            20,
            8,
            0,
        ),
    )

    repository.save(
        assignment
    )

    unassigned_at = datetime(
        2026,
        8,
        20,
        12,
        30,
    )

    repository.unassign(
        "WO-001",
        "55464",
        unassigned_at,
    )

    assert repository.exists(
        "WO-001",
        "55464",
    ) is False

    assignments = (
        repository.list_by_work_order(
            "WO-001"
        )
    )

    assert len(assignments) == 1

    persisted = assignments[0]

    assert persisted.is_active is False

    assert (
        persisted.unassigned_at
        == unassigned_at
    )

    engine.dispose()