from dataclasses import dataclass

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class GetWorkOrderQuery:
    code: str


@dataclass(frozen=True)
class GetWorkOrderResult:
    work_order: WorkOrder


class GetWorkOrder:

    def __init__(
        self,
        repository: WorkOrderRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: GetWorkOrderQuery,
    ) -> GetWorkOrderResult:

        work_order = self._repository.get_by_code(
            query.code
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        return GetWorkOrderResult(
            work_order=work_order
        )