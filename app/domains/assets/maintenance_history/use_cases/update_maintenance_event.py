from dataclasses import dataclass
from datetime import datetime

from app.domains.assets.maintenance_history.repositories import (
    MaintenanceEventRepository,
)


@dataclass
class UpdateMaintenanceEventCommand:
    code: str
    event_type: str
    title: str
    description: str
    performed_by: str
    started_at: datetime
    completed_at: datetime | None = None
    observations: str = ""


@dataclass
class UpdateMaintenanceEventResult:
    success: bool
    error: str | None = None


class UpdateMaintenanceEvent:

    def __init__(
        self,
        repository: MaintenanceEventRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: UpdateMaintenanceEventCommand,
    ) -> UpdateMaintenanceEventResult:

        event = self._repository.get_by_code(
            command.code
        )

        if event is None:
            return UpdateMaintenanceEventResult(
                success=False,
                error="Maintenance event not found.",
            )

        if (
            command.completed_at is not None
            and command.completed_at
            < command.started_at
        ):
            return UpdateMaintenanceEventResult(
                success=False,
                error=(
                    "Completion time cannot be "
                    "before start time."
                ),
            )

        if not command.event_type.strip():
            return UpdateMaintenanceEventResult(
                success=False,
                error=(
                    "Maintenance event type is required."
                ),
            )

        if not command.title.strip():
            return UpdateMaintenanceEventResult(
                success=False,
                error=(
                    "Maintenance event title is required."
                ),
            )

        if not command.performed_by.strip():
            return UpdateMaintenanceEventResult(
                success=False,
                error="Performed by is required.",
            )

        event.event_type = command.event_type
        event.title = command.title
        event.description = command.description
        event.performed_by = command.performed_by
        event.started_at = command.started_at
        event.completed_at = command.completed_at
        event.observations = command.observations

        self._repository.save(event)

        return UpdateMaintenanceEventResult(
            success=True,
        )