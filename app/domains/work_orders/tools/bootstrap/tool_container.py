from app.foundation.database import (
    SessionLocal,
)

from app.domains.work_orders.bootstrap import (
    work_order_repository,
)

from app.domains.work_orders.tools.repositories import (
    SQLiteWorkOrderToolUsageRepository,
)

from app.domains.work_orders.tools.use_cases import (
    IssueToolToWorkOrder,
    ListWorkOrderTools,
    ReturnToolFromWorkOrder,
)


# ============================================================
# REPOSITORY
# ============================================================

work_order_tool_usage_repository = (
    SQLiteWorkOrderToolUsageRepository(
        SessionLocal
    )
)


# ============================================================
# USE CASES
# ============================================================

issue_tool_to_work_order = (
    IssueToolToWorkOrder(
        work_order_tool_usage_repository,
        work_order_repository,
    )
)

return_tool_from_work_order = (
    ReturnToolFromWorkOrder(
        work_order_tool_usage_repository
    )
)

list_work_order_tools = (
    ListWorkOrderTools(
        work_order_tool_usage_repository
    )
)