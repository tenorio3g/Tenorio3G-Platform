from dataclasses import dataclass

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class ListWorkOrdersResult:
    work_orders: list[WorkOrder]


class ListWorkOrders:

    def __init__(
        self,
        repository: WorkOrderRepository,
    ):
        self._repository = repository

    def execute(
        self,
    ) -> ListWorkOrdersResult:

        work_orders = (
            self._repository.list_all()
        )

        return ListWorkOrdersResult(
            work_orders=work_orders
        )