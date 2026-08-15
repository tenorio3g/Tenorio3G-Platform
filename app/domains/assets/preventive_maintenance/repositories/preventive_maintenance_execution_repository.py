from abc import ABC, abstractmethod

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
)


class PreventiveMaintenanceExecutionRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        execution: PreventiveMaintenanceExecution,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> PreventiveMaintenanceExecution | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_plan(
        self,
        plan_code: str,
    ) -> list[PreventiveMaintenanceExecution]:
        raise NotImplementedError

    @abstractmethod
    def list_by_asset(
        self,
        asset_code: str,
    ) -> list[PreventiveMaintenanceExecution]:
        raise NotImplementedError