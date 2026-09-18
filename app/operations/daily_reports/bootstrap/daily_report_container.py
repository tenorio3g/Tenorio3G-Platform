from app.domains.work_orders.bootstrap import (
    work_order_repository,
)

from app.domains.work_orders.activities.bootstrap import (
    work_order_activity_repository,
)

from app.domains.work_orders.work_sessions.bootstrap import (
    work_session_repository,
)

from app.operations.operational_activities.bootstrap import (
    operational_activity_repository,
)

from app.operations.daily_reports.queries import (
    GetDailyOperationalReport,
)


# ============================================================
# QUERIES
# ============================================================

get_daily_operational_report = (
    GetDailyOperationalReport(
        work_order_repository=work_order_repository,
        activity_repository=work_order_activity_repository,
        work_session_repository=work_session_repository,
        operational_activity_repository=(
            operational_activity_repository
        ),
    )
)
