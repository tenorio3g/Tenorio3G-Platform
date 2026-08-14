from dataclasses import dataclass

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    PreventiveMaintenanceRepository,
)


@dataclass(frozen=True)
class GetPreventiveMaintenancePlanQuery:
    code: str


@dataclass(frozen=True)
class GetPreventiveMaintenancePlanResult:
    plan: PreventiveMaintenancePlan | None


class GetPreventiveMaintenancePlan:

    def __init__(
        self,
        repository: PreventiveMaintenanceRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: GetPreventiveMaintenancePlanQuery,
    ) -> GetPreventiveMaintenancePlanResult:

        plan = self._repository.get_by_code(
            query.code
        )

        return GetPreventiveMaintenancePlanResult(
            plan=plan
        )