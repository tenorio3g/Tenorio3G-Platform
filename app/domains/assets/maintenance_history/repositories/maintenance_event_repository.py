from abc import ABC, abstractmethod

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)


class MaintenanceEventRepository(ABC):

    @abstractmethod
    def save(
        self,
        event: MaintenanceEvent,
    ) -> MaintenanceEvent:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> MaintenanceEvent | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[MaintenanceEvent]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        code: str,
    ) -> bool:
        raise NotImplementedError