from app.foundation.database import (
    SessionLocal,
)

from app.domains.identity.people.bootstrap import (
    person_repository,
)

from app.domains.work_orders.bootstrap.work_order_container import (
    work_order_repository,
)

from app.domains.work_orders.technicians.repositories import (
    SQLiteWorkOrderTechnicianAssignmentRepository,
)

from app.domains.work_orders.technicians.use_cases import (
    AssignTechnicianToWorkOrder,
    ListWorkOrderTechnicians,
    UnassignTechnicianFromWorkOrder,
)


# ============================================================
# REPOSITORY
# ============================================================

technician_assignment_repository = (
    SQLiteWorkOrderTechnicianAssignmentRepository(
        SessionLocal
    )
)


# ============================================================
# USE CASES
# ============================================================

assign_technician_to_work_order = (
    AssignTechnicianToWorkOrder(
        work_order_repository,
        person_repository,
        technician_assignment_repository,
    )
)

list_work_order_technicians = (
    ListWorkOrderTechnicians(
        technician_assignment_repository,
        person_repository,
    )
)

unassign_technician_from_work_order = (
    UnassignTechnicianFromWorkOrder(
        work_order_repository,
        technician_assignment_repository,
    )
)