from abc import ABC, abstractmethod

from app.domains.inventory.entities import (
    InventoryMovement,
)


class InventoryMovementRepository(ABC):

    @abstractmethod
    def save(
        self,
        movement: InventoryMovement,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> InventoryMovement | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_spare_part(
        self,
        spare_part_code: str,
    ) -> list[InventoryMovement]:
        raise NotImplementedError

    @abstractmethod
    def list_by_location(
        self,
        location_code: str,
    ) -> list[InventoryMovement]:
        raise NotImplementedError

    @abstractmethod
    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[InventoryMovement]:
        raise NotImplementedError

    @abstractmethod
    def list_by_transfer_code(
        self,
        transfer_code: str,
    ) -> list[InventoryMovement]:
        raise NotImplementedError
