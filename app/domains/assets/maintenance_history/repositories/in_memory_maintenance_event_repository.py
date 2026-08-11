from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from .maintenance_event_repository import (
    MaintenanceEventRepository,
)


class InMemoryMaintenanceEventRepository(
    MaintenanceEventRepository
):

    def __init__(self) -> None:
        self._events: dict[
            str,
            MaintenanceEvent,
        ] = {}

    def save(
        self,
        event: MaintenanceEvent,
    ) -> MaintenanceEvent:

        self._events[event.code] = event

        return event

    def get_by_code(
        self,
        code: str,
    ) -> MaintenanceEvent | None:

        return self._events.get(code)

    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[MaintenanceEvent]:

        return [
            event
            for event in self._events.values()
            if event.asset_code == asset_code
        ]

    def delete(
        self,
        code: str,
    ) -> bool:

        if code not in self._events:
            return False

        del self._events[code]

        return True