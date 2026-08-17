from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from .work_order_technician_assignment_repository import (
    WorkOrderTechnicianAssignmentRepository,
)


class InMemoryWorkOrderTechnicianAssignmentRepository(
    WorkOrderTechnicianAssignmentRepository,
):

    def __init__(
        self,
    ):
        self._assignments: dict[
            tuple[str, str],
            WorkOrderTechnicianAssignment,
        ] = {}

    def save(
        self,
        assignment: WorkOrderTechnicianAssignment,
    ) -> None:

        key = (
            assignment.work_order_code,
            assignment.person_code,
        )

        if key in self._assignments:
            raise ValueError(
                "technician already assigned to work order"
            )

        self._assignments[
            key
        ] = assignment

    def exists(
        self,
        work_order_code: str,
        person_code: str,
    ) -> bool:

        key = (
            str(
                work_order_code
            ).strip().upper(),
            str(
                person_code
            ).strip(),
        )

        return key in self._assignments

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderTechnicianAssignment]:

        normalized_code = str(
            work_order_code
        ).strip().upper()

        return [
            assignment
            for assignment
            in self._assignments.values()
            if assignment.work_order_code
            == normalized_code
        ]

    def delete(
        self,
        work_order_code: str,
        person_code: str,
    ) -> None:

        key = (
            str(
                work_order_code
            ).strip().upper(),
            str(
                person_code
            ).strip(),
        )

        self._assignments.pop(
            key,
            None,
        )