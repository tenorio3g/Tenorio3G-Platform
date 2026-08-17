from app.foundation.database import (
    SessionLocal,
)

from app.domains.assets.spare_parts.bootstrap.spare_parts_container import (
    spare_part_repository,
)

from app.domains.work_orders.bootstrap import (
    work_order_repository,
)

from app.domains.work_orders.materials.repositories import (
    SQLiteWorkOrderSparePartUsageRepository,
)

from app.domains.work_orders.materials.use_cases import (
    AddSparePartToWorkOrder,
    ListWorkOrderSpareParts,
)


# ============================================================
# REPOSITORY
# ============================================================

work_order_spare_part_usage_repository = (
    SQLiteWorkOrderSparePartUsageRepository(
        SessionLocal
    )
)


# ============================================================
# USE CASES
# ============================================================

add_spare_part_to_work_order = (
    AddSparePartToWorkOrder(
        work_order_repository,
        spare_part_repository,
        work_order_spare_part_usage_repository,
    )
)

list_work_order_spare_parts = (
    ListWorkOrderSpareParts(
        work_order_spare_part_usage_repository,
        spare_part_repository,
    )
)