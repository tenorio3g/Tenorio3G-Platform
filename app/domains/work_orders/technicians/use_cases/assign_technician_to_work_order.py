from dataclasses import dataclass
from datetime import datetime

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from app.domains.work_orders.technicians.repositories import (
    WorkOrderTechnicianAssignmentRepository,
)


@dataclass(frozen=True)
class AssignTechnicianToWorkOrderCommand:
    work_order_code: str
    person_code: str
    assigned_at: datetime


@dataclass(frozen=True)
class AssignTechnicianToWorkOrderResult:
    assignment: WorkOrderTechnicianAssignment


class AssignTechnicianToWorkOrder:

    def __init__(
        self,
        work_order_repository: WorkOrderRepository,
        person_repository: PersonRepository,
        assignment_repository: WorkOrderTechnicianAssignmentRepository,
    ):
        self._work_order_repository = (
            work_order_repository
        )

        self._person_repository = (
            person_repository
        )

        self._assignment_repository = (
            assignment_repository
        )

    def execute(
        self,
        command: AssignTechnicianToWorkOrderCommand,
    ) -> AssignTechnicianToWorkOrderResult:

        work_order = (
            self._work_order_repository.get_by_code(
                command.work_order_code
            )
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        person = (
            self._person_repository.get_by_code(
                command.person_code
            )
        )

        if person is None:
            raise ValueError(
                "technician not found"
            )

        if not person.is_active:
            raise ValueError(
                "technician is inactive"
            )

        if self._assignment_repository.exists(
            work_order.code,
            person.code,
        ):
            raise ValueError(
                "technician already assigned to work order"
            )

        assignment = WorkOrderTechnicianAssignment(
            work_order_code=work_order.code,
            person_code=person.code,
            assigned_at=command.assigned_at,
        )

        self._assignment_repository.save(
            assignment
        )

        return AssignTechnicianToWorkOrderResult(
            assignment=assignment
        )