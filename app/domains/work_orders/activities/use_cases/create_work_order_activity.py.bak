from dataclasses import dataclass

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.repositories import (
    WorkOrderActivityRepository,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class CreateWorkOrderActivityCommand:
    code: str
    work_order_code: str
    title: str
    responsible_person_code: str
    description: str = ""
    estimated_minutes: int | None = None


@dataclass(frozen=True)
class CreateWorkOrderActivityResult:
    activity: WorkOrderActivity


class CreateWorkOrderActivity:

    def __init__(
        self,
        activity_repository: WorkOrderActivityRepository,
        work_order_repository: WorkOrderRepository,
        person_repository: PersonRepository,
    ):
        self._activity_repository = (
            activity_repository
        )

        self._work_order_repository = (
            work_order_repository
        )

        self._person_repository = (
            person_repository
        )

    def execute(
        self,
        command: CreateWorkOrderActivityCommand,
    ) -> CreateWorkOrderActivityResult:

        work_order = (
            self._work_order_repository.get_by_code(
                command.work_order_code
            )
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        person = (
            self._person_repository.get_by_code(
                command.responsible_person_code
            )
        )

        if person is None:
            raise ValueError(
                "responsible person not found"
            )

        if not person.is_active:
            raise ValueError(
                "responsible person is inactive"
            )

        existing = (
            self._activity_repository.get_by_code(
                command.code
            )
        )

        if existing is not None:
            raise ValueError(
                "activity code already exists"
            )

        activity = WorkOrderActivity(
            code=command.code,
            work_order_code=(
                work_order.code
            ),
            title=command.title,
            responsible_person_code=(
                person.code
            ),
            description=command.description,
            estimated_minutes=(
                command.estimated_minutes
            ),
        )

        self._activity_repository.save(
            activity
        )

        return CreateWorkOrderActivityResult(
            activity=activity
        )