from abc import ABC, abstractmethod

from app.domains.inventory.entities import InventoryStock


class InventoryStockRepository(ABC):

    @abstractmethod
    def save(
        self,
        stock: InventoryStock,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        spare_part_code: str,
        location_code: str,
    ) -> InventoryStock | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_spare_part(
        self,
        spare_part_code: str,
    ) -> list[InventoryStock]:
        raise NotImplementedError

    @abstractmethod
    def list_by_location(
        self,
        location_code: str,
    ) -> list[InventoryStock]:
        raise NotImplementedError
