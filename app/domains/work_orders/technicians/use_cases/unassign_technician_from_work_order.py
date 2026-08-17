from dataclasses import dataclass

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)

from app.domains.work_orders.technicians.repositories import (
    WorkOrderTechnicianAssignmentRepository,
)


@dataclass(frozen=True)
class UnassignTechnicianFromWorkOrderCommand:
    work_order_code: str
    person_code: str


class UnassignTechnicianFromWorkOrder:

    def __init__(
        self,
        work_order_repository: WorkOrderRepository,
        assignment_repository: (
            WorkOrderTechnicianAssignmentRepository
        ),
    ):
        self._work_order_repository = (
            work_order_repository
        )

        self._assignment_repository = (
            assignment_repository
        )

    def execute(
        self,
        command: UnassignTechnicianFromWorkOrderCommand,
    ) -> None:

        work_order = (
            self._work_order_repository.get_by_code(
                command.work_order_code
            )
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        if not self._assignment_repository.exists(
            work_order.code,
            command.person_code,
        ):
            raise ValueError(
                "technician is not assigned to work order"
            )

        self._assignment_repository.delete(
            work_order.code,
            command.person_code,
        )