from dataclasses import dataclass

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.repositories import (
    MaintenanceEventRepository,
)


@dataclass
class ListMaintenanceEventsByAssetQuery:
    asset_code: str


@dataclass
class ListMaintenanceEventsByAssetResult:
    success: bool
    events: list[MaintenanceEvent]
    error: str | None = None


class ListMaintenanceEventsByAsset:

    def __init__(
        self,
        repository: MaintenanceEventRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: ListMaintenanceEventsByAssetQuery,
    ) -> ListMaintenanceEventsByAssetResult:

        if not query.asset_code.strip():
            return ListMaintenanceEventsByAssetResult(
                success=False,
                events=[],
                error="Asset code is required.",
            )

        events = self._repository.get_by_asset_code(
            query.asset_code
        )

        return ListMaintenanceEventsByAssetResult(
            success=True,
            events=events,
        )