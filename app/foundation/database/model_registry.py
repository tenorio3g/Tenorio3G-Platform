"""
Registro central de modelos ORM de Tenorio3G.

La finalidad de este m?dulo es asegurar que todos los modelos
SQLAlchemy est?n importados y registrados en Base.metadata antes
de inicializar el esquema de base de datos.
"""

# ==========================================================
# Assets
# ==========================================================

from app.domains.assets.models import (
    AssetModelRecord,
    AssetRecordModel,
)

from app.domains.assets.documents.models.document_model import (
    DocumentModel,
)

from app.domains.assets.maintenance_history.models.maintenance_event_model import (
    MaintenanceEventModel,
)

from app.domains.assets.photos.models.photo_model import (
    PhotoModel,
)

from app.domains.assets.preventive_maintenance.models.preventive_maintenance_execution_model import (
    PreventiveMaintenanceExecutionModel,
)

from app.domains.assets.preventive_maintenance.models.preventive_maintenance_plan_model import (
    PreventiveMaintenancePlanModel,
)

from app.domains.assets.spare_parts.models.asset_spare_part_model import (
    AssetSparePartModel,
)

from app.domains.assets.spare_parts.models.spare_part_model import (
    SparePartModel,
)

from app.domains.assets.technical_data.models.technical_data_model import (
    TechnicalDataModel,
)

# ==========================================================
# Identity
# ==========================================================

from app.domains.identity.people.models.person_model import (
    PersonModel,
)

from app.domains.identity.roles.models.role_model import (
    RoleModel,
)

from app.domains.identity.users.models.user_model import (
    UserModel,
)

# ==========================================================
# Work Orders
# ==========================================================

from app.domains.work_orders.models.work_order_model import (
    WorkOrderModel,
)

from app.domains.work_orders.activities.models.work_order_activity_model import (
    WorkOrderActivityModel,
)

from app.domains.work_orders.evidence.models.work_order_evidence_model import (
    WorkOrderEvidenceModel,
)

from app.domains.work_orders.materials.models.work_order_spare_part_usage_model import (
    WorkOrderSparePartUsageModel,
)

from app.domains.work_orders.technicians.models.work_order_technician_assignment_model import (
    WorkOrderTechnicianAssignmentModel,
)

from app.domains.work_orders.tools.models.work_order_tool_usage_model import (
    WorkOrderToolUsageModel,
)

from app.domains.work_orders.work_sessions.models.work_session_audit_entry_model import (
    WorkSessionAuditEntryModel,
)

from app.domains.work_orders.work_sessions.models.work_session_model import (
    WorkSessionModel,
)

# ==========================================================
# Foundation Timeline
# ==========================================================

from app.foundation.timeline.engine.models.timeline_event_model import (
    TimelineEventModel,
)

# ==========================================================
# Physical Locations
# ==========================================================

from app.domains.locations.models import (
    PhysicalLocationModel,
)


# ==========================================================
# Maps
# ==========================================================

from app.maps.models.map_location import (
    MapLocation,
)


__all__ = [
    "AssetModelRecord",
    "AssetRecordModel",
    "DocumentModel",
    "MaintenanceEventModel",
    "PhotoModel",
    "PreventiveMaintenanceExecutionModel",
    "PreventiveMaintenancePlanModel",
    "AssetSparePartModel",
    "SparePartModel",
    "TechnicalDataModel",
    "PersonModel",
    "RoleModel",
    "UserModel",
    "WorkOrderModel",
    "WorkOrderActivityModel",
    "WorkOrderEvidenceModel",
    "WorkOrderSparePartUsageModel",
    "WorkOrderTechnicianAssignmentModel",
    "WorkOrderToolUsageModel",
    "WorkSessionAuditEntryModel",
    "WorkSessionModel",
    "TimelineEventModel",
    "PhysicalLocationModel",
    "MapLocation",
]
