from dataclasses import dataclass

from app.domains.assets.entities import (
    Asset,
)

from app.domains.assets.repositories import (
    AssetRepository,
)

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)

from app.domains.work_orders.technicians.repositories import (
    WorkOrderTechnicianAssignmentRepository,
)


@dataclass(frozen=True)
class WorkOrderSummaryItem:
    work_order: WorkOrder
    asset: Asset | None
    requester: Person | None
    supervisor: Person | None
    active_technicians: list[Person]
    participant_technicians: list[Person]


@dataclass(frozen=True)
class ListWorkOrderSummariesResult:
    items: list[WorkOrderSummaryItem]


class ListWorkOrderSummaries:

    def __init__(
        self,
        work_order_repository: WorkOrderRepository,
        asset_repository: AssetRepository,
        person_repository: PersonRepository,
        technician_assignment_repository: (
            WorkOrderTechnicianAssignmentRepository
        ),
    ):
        self._work_order_repository = (
            work_order_repository
        )

        self._asset_repository = (
            asset_repository
        )

        self._person_repository = (
            person_repository
        )

        self._technician_assignment_repository = (
            technician_assignment_repository
        )

    def execute(
        self,
    ) -> ListWorkOrderSummariesResult:

        work_orders = (
            self._work_order_repository.list_all()
        )

        items = []

        for work_order in work_orders:

            asset = (
                self._asset_repository.find_by_code(
                    work_order.asset_code
                )
            )

            requester = (
                self._person_repository.get_by_code(
                    work_order.requester_person_code
                )
            )

            supervisor = (
                self._person_repository.get_by_code(
                    work_order.supervisor_person_code
                )
            )

            assignments = (
                self._technician_assignment_repository
                .list_by_work_order(
                    work_order.code
                )
            )

            active_technicians = []
            participant_technicians = []

            participant_codes = set()

            for assignment in assignments:

                person = (
                    self._person_repository.get_by_code(
                        assignment.person_code
                    )
                )

                if person is None:
                    continue

                if (
                    person.code
                    not in participant_codes
                ):
                    participant_technicians.append(
                        person
                    )

                    participant_codes.add(
                        person.code
                    )

                if assignment.is_active:
                    active_technicians.append(
                        person
                    )

            items.append(
                WorkOrderSummaryItem(
                    work_order=work_order,
                    asset=asset,
                    requester=requester,
                    supervisor=supervisor,
                    active_technicians=(
                        active_technicians
                    ),
                    participant_technicians=(
                        participant_technicians
                    ),
                )
            )

        items.sort(
            key=lambda item: (
                item.work_order.created_at
            ),
            reverse=True,
        )

        return ListWorkOrderSummariesResult(
            items=items
        )