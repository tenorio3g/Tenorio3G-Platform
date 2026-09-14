from app.foundation.database import (
    SessionLocal,
)

from app.domains.identity.people.bootstrap import (
    person_repository,
)

from app.domains.work_orders.bootstrap import (
    work_order_repository,
)

from app.domains.work_orders.technicians.bootstrap import (
    technician_assignment_repository,
)

from app.domains.work_orders.activities.holds.repositories import (
    SQLiteActivityHoldRepository,
)

from app.domains.work_orders.activities.repositories import (
    SQLiteWorkOrderActivityRepository,
)

from app.domains.work_orders.activities.use_cases import (
    CompleteWorkOrderActivity,
    CreateWorkOrderActivity,
    HoldWorkOrderActivity,
    ListWorkOrderActivities,
    ResumeWorkOrderActivity,
    StartWorkOrderActivity,
)


# ============================================================
# REPOSITORIES
# ============================================================

work_order_activity_repository = (
    SQLiteWorkOrderActivityRepository(
        SessionLocal
    )
)

activity_hold_repository = (
    SQLiteActivityHoldRepository(
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
        technician_assignment_repository,
    )
)

list_work_order_activities = (
    ListWorkOrderActivities(
        work_order_activity_repository,
        person_repository,
        activity_hold_repository,
    )
)

start_work_order_activity = (
    StartWorkOrderActivity(
        work_order_activity_repository
    )
)

hold_work_order_activity = (
    HoldWorkOrderActivity(
        work_order_activity_repository,
        activity_hold_repository,
    )
)

resume_work_order_activity = (
    ResumeWorkOrderActivity(
        work_order_activity_repository,
        activity_hold_repository,
    )
)

complete_work_order_activity = (
    CompleteWorkOrderActivity(
        work_order_activity_repository
    )
)
