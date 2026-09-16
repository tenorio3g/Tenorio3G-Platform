from abc import ABC, abstractmethod

from app.domains.inventory.entities import (
    InventoryLocation,
)


class InventoryLocationRepository(ABC):

    @abstractmethod
    def save(
        self,
        location: InventoryLocation,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> InventoryLocation | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_warehouse(
        self,
        warehouse_code: str,
    ) -> list[InventoryLocation]:
        raise NotImplementedError
