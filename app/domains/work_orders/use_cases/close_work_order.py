from dataclasses import dataclass

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class CloseWorkOrderCommand:
    code: str


@dataclass(frozen=True)
class CloseWorkOrderResult:
    work_order: WorkOrder


class CloseWorkOrder:

    def __init__(
        self,
        repository: WorkOrderRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: CloseWorkOrderCommand,
    ) -> CloseWorkOrderResult:

        work_order = self._repository.get_by_code(
            command.code
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        work_order.close()

        self._repository.save(
            work_order
        )

        return CloseWorkOrderResult(
            work_order=work_order
        )
