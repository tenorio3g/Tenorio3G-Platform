from app.foundation.database import (
    SessionLocal,
)

from app.domains.identity.people.bootstrap import (
    person_repository,
)

from app.domains.work_orders.bootstrap import (
    work_order_repository,
)

from app.domains.work_orders.activities.repositories import (
    SQLiteWorkOrderActivityRepository,
)

from app.domains.work_orders.activities.use_cases import (
    CompleteWorkOrderActivity,
    CreateWorkOrderActivity,
    ListWorkOrderActivities,
    StartWorkOrderActivity,
)


# ============================================================
# REPOSITORY
# ============================================================

work_order_activity_repository = (
    SQLiteWorkOrderActivityRepository(
        SessionLocal
    )
)


# ============================================================
# USE CASES
# ============================================================

create_work_order_activity = (
    CreateWorkOrderActivity(
        work_order_activity_repository,
        work_order_repository,
        person_repository,
    )
)

list_work_order_activities = (
    ListWorkOrderActivities(
        work_order_activity_repository,
        person_repository,
    )
)


start_work_order_activity = (
    StartWorkOrderActivity(
        work_order_activity_repository
    )
)

complete_work_order_activity = (
    CompleteWorkOrderActivity(
        work_order_activity_repository
    )
)