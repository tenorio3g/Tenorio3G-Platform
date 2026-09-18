from app.foundation.database import (
    SessionLocal,
)

from app.operations.operational_activities.repositories import (
    SQLiteOperationalActivityRepository,
)


# ============================================================
# REPOSITORIES
# ============================================================

operational_activity_repository = (
    SQLiteOperationalActivityRepository(
        SessionLocal
    )
)
