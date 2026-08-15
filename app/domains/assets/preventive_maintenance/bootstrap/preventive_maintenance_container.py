from app.foundation.database import (
    SessionLocal,
)

from app.domains.assets.preventive_maintenance.repositories import (
    SQLitePreventiveMaintenanceExecutionRepository,
    SQLitePreventiveMaintenanceRepository,
)

from app.domains.assets.preventive_maintenance.use_cases import (
    CompletePreventiveMaintenancePlan,
    CreatePreventiveMaintenancePlan,
    DeletePreventiveMaintenancePlan,
    GetPreventiveMaintenancePlan,
    ListPreventiveMaintenanceExecutionsByAsset,
    ListPreventiveMaintenancePlansByAsset,
    UpdatePreventiveMaintenancePlan,
    
)


# ============================================================
# REPOSITORIES
# ============================================================

preventive_maintenance_repository = (
    SQLitePreventiveMaintenanceRepository(
        SessionLocal
    )
)

preventive_maintenance_execution_repository = (
    SQLitePreventiveMaintenanceExecutionRepository(
        SessionLocal
    )
)


# ============================================================
# CREATE
# ============================================================

create_preventive_maintenance_plan = (
    CreatePreventiveMaintenancePlan(
        preventive_maintenance_repository
    )
)


# ============================================================
# GET
# ============================================================

get_preventive_maintenance_plan = (
    GetPreventiveMaintenancePlan(
        preventive_maintenance_repository
    )
)


# ============================================================
# LIST BY ASSET
# ============================================================

list_preventive_maintenance_plans_by_asset = (
    ListPreventiveMaintenancePlansByAsset(
        preventive_maintenance_repository
    )
)

list_preventive_maintenance_executions_by_asset = (
    ListPreventiveMaintenanceExecutionsByAsset(
        preventive_maintenance_execution_repository
    )
)


# ============================================================
# UPDATE
# ============================================================

update_preventive_maintenance_plan = (
    UpdatePreventiveMaintenancePlan(
        preventive_maintenance_repository
    )
)


# ============================================================
# DELETE
# ============================================================

delete_preventive_maintenance_plan = (
    DeletePreventiveMaintenancePlan(
        preventive_maintenance_repository
    )
)


# ============================================================
# COMPLETE / EXECUTE PREVENTIVE MAINTENANCE
# ============================================================

complete_preventive_maintenance_plan = (
    CompletePreventiveMaintenancePlan(
        preventive_maintenance_repository,
        preventive_maintenance_execution_repository,
    )
)