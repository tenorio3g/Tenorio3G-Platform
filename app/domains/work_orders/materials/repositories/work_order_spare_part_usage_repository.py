from abc import ABC, abstractmethod

from app.domains.work_orders.materials.entities import (
    WorkOrderSparePartUsage,
)


class WorkOrderSparePartUsageRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        usage: WorkOrderSparePartUsage,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderSparePartUsage]:
        raise NotImplementedError