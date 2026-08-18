from dataclasses import dataclass

from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)

from app.domains.work_orders.tools.repositories import (
    WorkOrderToolUsageRepository,
)


@dataclass(frozen=True)
class ListWorkOrderToolsQuery:
    work_order_code: str


@dataclass(frozen=True)
class ListWorkOrderToolsResult:
    items: list[WorkOrderToolUsage]


class ListWorkOrderTools:

    def __init__(
        self,
        repository: WorkOrderToolUsageRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: ListWorkOrderToolsQuery,
    ) -> ListWorkOrderToolsResult:

        work_order_code = str(
            query.work_order_code
        ).strip().upper()

        items = (
            self._repository
            .list_by_work_order(
                work_order_code
            )
        )

        return ListWorkOrderToolsResult(
            items=items
        )