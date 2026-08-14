from app.foundation.database import (
    SessionLocal,
)

from app.domains.assets.preventive_maintenance.repositories import (
    SQLitePreventiveMaintenanceRepository,
)

from app.domains.assets.preventive_maintenance.use_cases import (
    CreatePreventiveMaintenancePlan,
    DeletePreventiveMaintenancePlan,
    GetPreventiveMaintenancePlan,
    ListPreventiveMaintenancePlansByAsset,
    UpdatePreventiveMaintenancePlan,
)


preventive_maintenance_repository = (
    SQLitePreventiveMaintenanceRepository(
        SessionLocal
    )
)


create_preventive_maintenance_plan = (
    CreatePreventiveMaintenancePlan(
        preventive_maintenance_repository
    )
)

get_preventive_maintenance_plan = (
    GetPreventiveMaintenancePlan(
        preventive_maintenance_repository
    )
)

list_preventive_maintenance_plans_by_asset = (
    ListPreventiveMaintenancePlansByAsset(
        preventive_maintenance_repository
    )
)

update_preventive_maintenance_plan = (
    UpdatePreventiveMaintenancePlan(
        preventive_maintenance_repository
    )
)

delete_preventive_maintenance_plan = (
    DeletePreventiveMaintenancePlan(
        preventive_maintenance_repository
    )
)