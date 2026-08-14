from abc import ABC, abstractmethod

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)


class PreventiveMaintenanceRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        plan: PreventiveMaintenancePlan,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> PreventiveMaintenancePlan | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_asset(
        self,
        asset_code: str,
    ) -> list[PreventiveMaintenancePlan]:
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[PreventiveMaintenancePlan]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        code: str,
    ) -> None:
        raise NotImplementedError