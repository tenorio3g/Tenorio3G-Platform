from dataclasses import dataclass

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class ResumeWorkOrderCommand:
    code: str


@dataclass(frozen=True)
class ResumeWorkOrderResult:
    work_order: WorkOrder


class ResumeWorkOrder:

    def __init__(
        self,
        repository: WorkOrderRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: ResumeWorkOrderCommand,
    ) -> ResumeWorkOrderResult:

        work_order = self._repository.get_by_code(
            command.code
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        work_order.resume()

        self._repository.save(
            work_order
        )

        return ResumeWorkOrderResult(
            work_order=work_order
        )
