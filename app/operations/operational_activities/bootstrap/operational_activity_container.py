from app.foundation.database import (
    SessionLocal,
)

from app.operations.operational_activities.repositories import (
    SQLiteOperationalActivityRepository,
)

from app.operations.operational_activities.use_cases import (
    CompleteOperationalActivity,
    CreateOperationalActivity,
)


# ============================================================
# REPOSITORIES
# ============================================================

operational_activity_repository = (
    SQLiteOperationalActivityRepository(
        SessionLocal
    )
)

# ============================================================
# USE CASES
# ============================================================

create_operational_activity = (
    CreateOperationalActivity(
        operational_activity_repository
    )
)

complete_operational_activity = (
    CompleteOperationalActivity(
        operational_activity_repository
    )
)
