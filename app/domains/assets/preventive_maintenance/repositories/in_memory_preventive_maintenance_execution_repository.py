from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
)

from .preventive_maintenance_execution_repository import (
    PreventiveMaintenanceExecutionRepository,
)


class InMemoryPreventiveMaintenanceExecutionRepository(
    PreventiveMaintenanceExecutionRepository,
):

    def __init__(
        self,
    ):
        self._executions: dict[
            str,
            PreventiveMaintenanceExecution,
        ] = {}

    def save(
        self,
        execution: PreventiveMaintenanceExecution,
    ) -> None:

        self._executions[
            execution.code
        ] = execution

    def get_by_code(
        self,
        code: str,
    ) -> PreventiveMaintenanceExecution | None:

        normalized_code = str(
            code
        ).strip().upper()

        return self._executions.get(
            normalized_code
        )

    def list_by_plan(
        self,
        plan_code: str,
    ) -> list[PreventiveMaintenanceExecution]:

        normalized_plan_code = str(
            plan_code
        ).strip().upper()

        return [
            execution
            for execution
            in self._executions.values()
            if execution.plan_code
            == normalized_plan_code
        ]

    def list_by_asset(
        self,
        asset_code: str,
    ) -> list[PreventiveMaintenanceExecution]:

        normalized_asset_code = str(
            asset_code
        ).strip().upper()

        return [
            execution
            for execution
            in self._executions.values()
            if execution.asset_code
            == normalized_asset_code
        ]