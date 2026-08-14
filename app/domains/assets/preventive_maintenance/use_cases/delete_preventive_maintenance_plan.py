from dataclasses import dataclass

from app.domains.assets.preventive_maintenance.repositories import (
    PreventiveMaintenanceRepository,
)


@dataclass(frozen=True)
class DeletePreventiveMaintenancePlanCommand:
    code: str


@dataclass(frozen=True)
class DeletePreventiveMaintenancePlanResult:
    deleted: bool


class DeletePreventiveMaintenancePlan:

    def __init__(
        self,
        repository: PreventiveMaintenanceRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: DeletePreventiveMaintenancePlanCommand,
    ) -> DeletePreventiveMaintenancePlanResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is None:
            return DeletePreventiveMaintenancePlanResult(
                deleted=False
            )

        self._repository.delete(
            existing.code
        )

        return DeletePreventiveMaintenancePlanResult(
            deleted=True
        )