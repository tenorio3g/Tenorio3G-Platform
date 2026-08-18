from abc import ABC, abstractmethod

from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)


class WorkOrderToolUsageRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        usage: WorkOrderToolUsage,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderToolUsage]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        usage_id: str,
    ) -> WorkOrderToolUsage | None:
        raise NotImplementedError