from dataclasses import dataclass

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.repositories import (
    MaintenanceEventRepository,
)


@dataclass
class GetMaintenanceEventQuery:
    code: str


@dataclass
class GetMaintenanceEventResult:
    success: bool
    event: MaintenanceEvent | None = None
    error: str | None = None


class GetMaintenanceEvent:

    def __init__(
        self,
        repository: MaintenanceEventRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: GetMaintenanceEventQuery,
    ) -> GetMaintenanceEventResult:

        event = self._repository.get_by_code(
            query.code
        )

        if event is None:
            return GetMaintenanceEventResult(
                success=False,
                error="Maintenance event not found.",
            )

        return GetMaintenanceEventResult(
            success=True,
            event=event,
        )