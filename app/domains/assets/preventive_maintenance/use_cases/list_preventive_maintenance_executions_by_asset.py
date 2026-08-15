from dataclasses import dataclass

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
)

from app.domains.assets.preventive_maintenance.repositories import (
    PreventiveMaintenanceExecutionRepository,
)


@dataclass(frozen=True)
class ListPreventiveMaintenanceExecutionsByAssetQuery:
    asset_code: str


@dataclass(frozen=True)
class ListPreventiveMaintenanceExecutionsByAssetResult:
    executions: list[PreventiveMaintenanceExecution]


class ListPreventiveMaintenanceExecutionsByAsset:

    def __init__(
        self,
        repository: PreventiveMaintenanceExecutionRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: ListPreventiveMaintenanceExecutionsByAssetQuery,
    ) -> ListPreventiveMaintenanceExecutionsByAssetResult:

        executions = self._repository.list_by_asset(
            query.asset_code
        )

        return (
            ListPreventiveMaintenanceExecutionsByAssetResult(
                executions=executions
            )
        )