from dataclasses import dataclass

from app.domains.assets.maintenance_history.repositories import (
    MaintenanceEventRepository,
)


@dataclass
class DeleteMaintenanceEventCommand:
    code: str


@dataclass
class DeleteMaintenanceEventResult:
    success: bool
    error: str | None = None


class DeleteMaintenanceEvent:

    def __init__(
        self,
        repository: MaintenanceEventRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: DeleteMaintenanceEventCommand,
    ) -> DeleteMaintenanceEventResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is None:
            return DeleteMaintenanceEventResult(
                success=False,
                error="Maintenance event not found.",
            )

        deleted = self._repository.delete(
            command.code
        )

        if not deleted:
            return DeleteMaintenanceEventResult(
                success=False,
                error=(
                    "Maintenance event could not be deleted."
                ),
            )

        return DeleteMaintenanceEventResult(
            success=True,
        )