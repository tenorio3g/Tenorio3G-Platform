from dataclasses import dataclass

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class AssignWorkOrderCommand:
    code: str


@dataclass(frozen=True)
class AssignWorkOrderResult:
    work_order: WorkOrder


class AssignWorkOrder:

    def __init__(
        self,
        repository: WorkOrderRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: AssignWorkOrderCommand,
    ) -> AssignWorkOrderResult:

        work_order = self._repository.get_by_code(
            command.code
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        work_order.assign()

        self._repository.save(
            work_order
        )

        return AssignWorkOrderResult(
            work_order=work_order
        )