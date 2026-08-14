from dataclasses import dataclass

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    PreventiveMaintenanceRepository,
)


@dataclass(frozen=True)
class ListPreventiveMaintenancePlansByAssetQuery:
    asset_code: str


@dataclass(frozen=True)
class ListPreventiveMaintenancePlansByAssetResult:
    plans: list[PreventiveMaintenancePlan]


class ListPreventiveMaintenancePlansByAsset:

    def __init__(
        self,
        repository: PreventiveMaintenanceRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: ListPreventiveMaintenancePlansByAssetQuery,
    ) -> ListPreventiveMaintenancePlansByAssetResult:

        plans = self._repository.list_by_asset(
            query.asset_code
        )

        return ListPreventiveMaintenancePlansByAssetResult(
            plans=plans
        )