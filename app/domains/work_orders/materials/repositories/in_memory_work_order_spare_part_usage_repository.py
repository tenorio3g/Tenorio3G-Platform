from app.domains.work_orders.materials.entities import (
    WorkOrderSparePartUsage,
)

from .work_order_spare_part_usage_repository import (
    WorkOrderSparePartUsageRepository,
)


class InMemoryWorkOrderSparePartUsageRepository(
    WorkOrderSparePartUsageRepository,
):

    def __init__(
        self,
    ):
        self._usages: list[
            WorkOrderSparePartUsage
        ] = []

    def save(
        self,
        usage: WorkOrderSparePartUsage,
    ) -> None:

        self._usages.append(
            usage
        )

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderSparePartUsage]:

        normalized_code = str(
            work_order_code
        ).strip().upper()

        return [
            usage
            for usage in self._usages
            if usage.work_order_code
            == normalized_code
        ]