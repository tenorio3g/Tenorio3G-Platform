from abc import ABC, abstractmethod

from app.domains.work_orders.entities import (
    WorkOrder,
)


class WorkOrderRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        work_order: WorkOrder,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> WorkOrder | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[WorkOrder]:
        raise NotImplementedError

    @abstractmethod
    def list_by_asset(
        self,
        asset_code: str,
    ) -> list[WorkOrder]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        code: str,
    ) -> None:
        raise NotImplementedError