from abc import ABC, abstractmethod

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)


class WorkOrderActivityRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        activity: WorkOrderActivity,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> WorkOrderActivity | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderActivity]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        code: str,
    ) -> None:
        raise NotImplementedError