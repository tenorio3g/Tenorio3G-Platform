from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)

from .work_order_tool_usage_repository import (
    WorkOrderToolUsageRepository,
)


class InMemoryWorkOrderToolUsageRepository(
    WorkOrderToolUsageRepository,
):

    def __init__(
        self,
    ):
        self._usages: list[
            WorkOrderToolUsage
        ] = []

    def save(
        self,
        usage: WorkOrderToolUsage,
    ) -> None:

        if usage not in self._usages:
            self._usages.append(
                usage
            )

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderToolUsage]:

        normalized_code = str(
            work_order_code
        ).strip().upper()

        return [
            usage
            for usage in self._usages
            if usage.work_order_code
            == normalized_code
        ]


    def get_by_id(
        self,
        usage_id: str,
    ) -> WorkOrderToolUsage | None:

        normalized_id = str(
            usage_id
        ).strip().upper()

        return next(
            (
                usage
                for usage in self._usages
                if usage.usage_id == normalized_id
            ),
            None,
        )