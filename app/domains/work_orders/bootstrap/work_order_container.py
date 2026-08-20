from app.foundation.database import (
    SessionLocal,
)

from app.domains.assets.bootstrap.assets_container import (
    repository as asset_repository,
)

from app.domains.identity.people.bootstrap import (
    person_repository,
)

from app.domains.work_orders.repositories import (
    SQLiteWorkOrderRepository,
)

from app.domains.work_orders.use_cases import (
    AssignWorkOrder,
    CancelWorkOrder,
    CloseWorkOrder,
    CompleteWorkOrder,
    CreateWorkOrder,
    GetWorkOrder,
    GetWorkOrderDetail,
    HoldWorkOrder,
    ListWorkOrders,
    ListWorkOrdersByAsset,
    ResumeWorkOrder,
    StartWorkOrder,
)
from app.foundation.timeline.engine.bootstrap import (
    record_timeline_event,
    
)


from app.domains.work_orders.timeline import (
    WorkOrderTimelineRecorder,
)

# ============================================================
# REPOSITORY
# ============================================================

work_order_repository = (
    SQLiteWorkOrderRepository(
        SessionLocal
    )
)


# ============================================================
# USE CASES
# ============================================================

create_work_order = CreateWorkOrder(
    work_order_repository,
    asset_repository,
    person_repository,
    record_timeline_event,
)

# ============================================================
# QUERIES
# ============================================================

get_work_order = GetWorkOrder(
    work_order_repository
)

list_work_orders = ListWorkOrders(
    work_order_repository
)

list_work_orders_by_asset = (
    ListWorkOrdersByAsset(
        work_order_repository
    )
)
get_work_order_detail = GetWorkOrderDetail(
    work_order_repository,
    asset_repository,
    person_repository,
)
# ============================================================
# COMMANDS - WORK ORDER LIFECYCLE
# ============================================================
work_order_timeline_recorder = (
    WorkOrderTimelineRecorder(
        record_timeline_event
    )
)

assign_work_order = AssignWorkOrder(
    work_order_repository,
    work_order_timeline_recorder,
)

start_work_order = StartWorkOrder(
    work_order_repository,
    work_order_timeline_recorder,
)

hold_work_order = HoldWorkOrder(
    work_order_repository,
    work_order_timeline_recorder,
)

resume_work_order = ResumeWorkOrder(
    work_order_repository,
    work_order_timeline_recorder,
)

complete_work_order = CompleteWorkOrder(
    work_order_repository,
    work_order_timeline_recorder,
)

close_work_order = CloseWorkOrder(
    work_order_repository,
    work_order_timeline_recorder,
)

cancel_work_order = CancelWorkOrder(
    work_order_repository,
    work_order_timeline_recorder,
)

