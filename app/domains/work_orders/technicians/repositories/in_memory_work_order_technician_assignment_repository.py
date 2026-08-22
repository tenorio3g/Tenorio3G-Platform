from datetime import datetime

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
        self._assignments: list[
            WorkOrderTechnicianAssignment
        ] = []

    def save(
        self,
        assignment: WorkOrderTechnicianAssignment,
    ) -> None:

        if self.exists(
            assignment.work_order_code,
            assignment.person_code,
        ):
            raise ValueError(
                "technician already assigned to work order"
            )

        self._assignments.append(
            assignment
        )

    def exists(
        self,
        work_order_code: str,
        person_code: str,
    ) -> bool:

        normalized_work_order_code = str(
            work_order_code
        ).strip().upper()

        normalized_person_code = str(
            person_code
        ).strip()

        return any(
            assignment.work_order_code
            == normalized_work_order_code
            and assignment.person_code
            == normalized_person_code
            and assignment.is_active
            for assignment in self._assignments
        )

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderTechnicianAssignment]:

        normalized_work_order_code = str(
            work_order_code
        ).strip().upper()

        assignments = [
            assignment
            for assignment in self._assignments
            if assignment.work_order_code
            == normalized_work_order_code
        ]

        return sorted(
            assignments,
            key=lambda assignment: (
                assignment.assigned_at
            ),
        )

    def unassign(
        self,
        work_order_code: str,
        person_code: str,
        unassigned_at: datetime,
    ) -> None:

        normalized_work_order_code = str(
            work_order_code
        ).strip().upper()

        normalized_person_code = str(
            person_code
        ).strip()

        for assignment in reversed(
            self._assignments
        ):

            if (
                assignment.work_order_code
                == normalized_work_order_code
                and assignment.person_code
                == normalized_person_code
                and assignment.is_active
            ):
                assignment.unassign(
                    unassigned_at
                )

                return

        raise ValueError(
            "technician is not assigned to work order"
        )


    def reactivate(
        self,
        work_order_code: str,
        person_code: str,
        assigned_at: datetime,
    ) -> WorkOrderTechnicianAssignment:

        normalized_work_order_code = str(
            work_order_code
        ).strip().upper()

        normalized_person_code = str(
            person_code
        ).strip()

        if not isinstance(
            assigned_at,
            datetime,
        ):
            raise ValueError(
                "assigned_at must be a datetime"
            )

        for assignment in reversed(
            self._assignments
        ):

            if (
                assignment.work_order_code
                == normalized_work_order_code
                and assignment.person_code
                == normalized_person_code
                and not assignment.is_active
            ):

                assignment.assigned_at = (
                    assigned_at
                )

                assignment.unassigned_at = (
                    None
                )

                return assignment

        raise ValueError(
            "technician assignment history not found"
        )



    def delete(
        self,
        work_order_code: str,
        person_code: str,
    ) -> None:
        """
        Eliminación física temporal para mantener
        compatibilidad con el contrato anterior.

        Será retirada cuando UnassignTechnicianFromWorkOrder
        utilice unassign().
        """

        normalized_work_order_code = str(
            work_order_code
        ).strip().upper()

        normalized_person_code = str(
            person_code
        ).strip()

        self._assignments = [
            assignment
            for assignment in self._assignments
            if not (
                assignment.work_order_code
                == normalized_work_order_code
                and assignment.person_code
                == normalized_person_code
            )
        ]