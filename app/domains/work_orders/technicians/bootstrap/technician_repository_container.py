from app.foundation.database import (
    SessionLocal,
)

from app.domains.work_orders.technicians.repositories import (
    SQLiteWorkOrderTechnicianAssignmentRepository,
)


# ============================================================
# REPOSITORY
# ============================================================

technician_assignment_repository = (
    SQLiteWorkOrderTechnicianAssignmentRepository(
        SessionLocal
    )
)


__all__ = [
    "technician_assignment_repository",
]
