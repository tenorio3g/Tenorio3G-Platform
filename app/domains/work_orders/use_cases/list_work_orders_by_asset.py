from dataclasses import dataclass

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class ListWorkOrdersByAssetQuery:
    asset_code: str


@dataclass(frozen=True)
class ListWorkOrdersByAssetResult:
    work_orders: list[WorkOrder]


class ListWorkOrdersByAsset:

    def __init__(
        self,
        repository: WorkOrderRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: ListWorkOrdersByAssetQuery,
    ) -> ListWorkOrdersByAssetResult:

        work_orders = (
            self._repository.list_by_asset(
                query.asset_code
            )
        )

        return ListWorkOrdersByAssetResult(
            work_orders=work_orders
        )