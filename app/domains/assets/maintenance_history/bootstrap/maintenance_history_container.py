from app.domains.assets.maintenance_history.repositories import (
    SQLiteMaintenanceEventRepository,
)

from app.domains.assets.maintenance_history.use_cases import (
    CreateMaintenanceEvent,
    DeleteMaintenanceEvent,
    GetMaintenanceEvent,
    ListMaintenanceEventsByAsset,
    UpdateMaintenanceEvent,
)


maintenance_event_repository = (
    SQLiteMaintenanceEventRepository()
)


create_maintenance_event = CreateMaintenanceEvent(
    maintenance_event_repository
)

get_maintenance_event = GetMaintenanceEvent(
    maintenance_event_repository
)

list_maintenance_events_by_asset = (
    ListMaintenanceEventsByAsset(
        maintenance_event_repository
    )
)

update_maintenance_event = UpdateMaintenanceEvent(
    maintenance_event_repository
)

delete_maintenance_event = DeleteMaintenanceEvent(
    maintenance_event_repository
)