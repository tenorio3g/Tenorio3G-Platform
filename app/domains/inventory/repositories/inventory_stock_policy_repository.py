from abc import ABC, abstractmethod

from app.domains.inventory.entities import (
    InventoryStockPolicy,
)


class InventoryStockPolicyRepository(ABC):

    @abstractmethod
    def save(
        self,
        policy: InventoryStockPolicy,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        spare_part_code: str,
        warehouse_code: str,
    ) -> InventoryStockPolicy | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_spare_part(
        self,
        spare_part_code: str,
    ) -> list[InventoryStockPolicy]:
        raise NotImplementedError

    @abstractmethod
    def list_by_warehouse(
        self,
        warehouse_code: str,
    ) -> list[InventoryStockPolicy]:
        raise NotImplementedError
