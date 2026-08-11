from dataclasses import dataclass
from datetime import datetime

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.repositories import (
    MaintenanceEventRepository,
)


@dataclass
class CreateMaintenanceEventCommand:
    code: str
    asset_code: str
    event_type: str
    title: str
    description: str
    performed_by: str
    started_at: datetime
    completed_at: datetime | None = None
    observations: str = ""


@dataclass
class CreateMaintenanceEventResult:
    success: bool
    event: MaintenanceEvent | None = None
    error: str | None = None


class CreateMaintenanceEvent:

    def __init__(
        self,
        repository: MaintenanceEventRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: CreateMaintenanceEventCommand,
    ) -> CreateMaintenanceEventResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is not None:
            return CreateMaintenanceEventResult(
                success=False,
                error=(
                    "Maintenance event already exists."
                ),
            )

        try:
            event = MaintenanceEvent(
                code=command.code,
                asset_code=command.asset_code,
                event_type=command.event_type,
                title=command.title,
                description=command.description,
                performed_by=command.performed_by,
                started_at=command.started_at,
                completed_at=command.completed_at,
                observations=command.observations,
            )
        except ValueError as exc:
            return CreateMaintenanceEventResult(
                success=False,
                error=str(exc),
            )

        self._repository.save(event)

        return CreateMaintenanceEventResult(
            success=True,
            event=event,
        )