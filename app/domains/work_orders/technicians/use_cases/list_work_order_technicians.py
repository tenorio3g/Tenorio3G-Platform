from dataclasses import dataclass

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from app.domains.work_orders.technicians.repositories import (
    WorkOrderTechnicianAssignmentRepository,
)


@dataclass(frozen=True)
class WorkOrderTechnicianItem:
    assignment: WorkOrderTechnicianAssignment
    person: Person


@dataclass(frozen=True)
class ListWorkOrderTechniciansQuery:
    work_order_code: str


@dataclass(frozen=True)
class ListWorkOrderTechniciansResult:
    items: list[WorkOrderTechnicianItem]


class ListWorkOrderTechnicians:

    def __init__(
        self,
        assignment_repository: (
            WorkOrderTechnicianAssignmentRepository
        ),
        person_repository: PersonRepository,
    ):
        self._assignment_repository = (
            assignment_repository
        )

        self._person_repository = (
            person_repository
        )

    def execute(
        self,
        query: ListWorkOrderTechniciansQuery,
    ) -> ListWorkOrderTechniciansResult:

        assignments = (
            self._assignment_repository
            .list_by_work_order(
                query.work_order_code
            )
        )

        items = []

        for assignment in assignments:

            person = (
                self._person_repository
                .get_by_code(
                    assignment.person_code
                )
            )

            if person is None:
                continue

            items.append(
                WorkOrderTechnicianItem(
                    assignment=assignment,
                    person=person,
                )
            )

        return ListWorkOrderTechniciansResult(
            items=items
        )