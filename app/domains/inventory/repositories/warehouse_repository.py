from abc import ABC, abstractmethod

from app.domains.inventory.entities import Warehouse


class WarehouseRepository(ABC):

    @abstractmethod
    def save(
        self,
        warehouse: Warehouse,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> Warehouse | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[Warehouse]:
        raise NotImplementedError
