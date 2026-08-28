from dataclasses import dataclass
from datetime import datetime

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from app.domains.work_orders.activities.repositories import (
    WorkOrderActivityRepository,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from app.domains.work_orders.work_sessions.repositories import (
    WorkSessionRepository,
)

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)


@dataclass(frozen=True)
class StartWorkSessionCommand:
    code: str
    work_order_code: str
    activity_code: str
    person_code: str
    started_at: datetime
    created_at: datetime
    created_by_person_code: str


@dataclass(frozen=True)
class StartWorkSessionResult:
    work_session: WorkSession


class StartWorkSession:

    def __init__(
        self,
        work_order_repository: WorkOrderRepository,
        activity_repository: WorkOrderActivityRepository,
        person_repository: PersonRepository,
        work_session_repository: WorkSessionRepository,
    ):
        self._work_order_repository = (
            work_order_repository
        )

        self._activity_repository = (
            activity_repository
        )

        self._person_repository = (
            person_repository
        )

        self._work_session_repository = (
            work_session_repository
        )

    def execute(
        self,
        command: StartWorkSessionCommand,
    ) -> StartWorkSessionResult:

        work_order = (
            self._work_order_repository.get_by_code(
                command.work_order_code
            )
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        if work_order.status not in (
            WorkOrderStatus.ASSIGNED,
            WorkOrderStatus.IN_PROGRESS,
        ):
            raise ValueError(
                "work order cannot start "
                "session from current status"
            )

        activity = (
            self._activity_repository.get_by_code(
                command.activity_code
            )
        )

        if activity is None:
            raise ValueError(
                "activity not found"
            )

        if (
            activity.work_order_code
            != work_order.code
        ):
            raise ValueError(
                "activity does not belong "
                "to work order"
            )

        if (
            activity.status
            == ActivityStatus.COMPLETED
        ):
            raise ValueError(
                "cannot start work session "
                "for completed activity"
            )

        person = (
            self._person_repository.get_by_code(
                command.person_code
            )
        )

        if person is None:
            raise ValueError(
                "person not found"
            )

        if not person.is_active:
            raise ValueError(
                "person is not active"
            )

        existing_session = (
            self._work_session_repository.get_by_code(
                command.code
            )
        )

        if existing_session is not None:
            raise ValueError(
                "work session code already exists"
            )

        active_session = (
            self._work_session_repository
            .get_active_by_person(
                person.code
            )
        )

        if active_session is not None:
            raise ValueError(
                "person already has an "
                "active work session"
            )

        if (
            work_order.status
            == WorkOrderStatus.ASSIGNED
        ):
            work_order.start()

            self._work_order_repository.save(
                work_order
            )

        if (
            activity.status
            == ActivityStatus.PENDING
        ):
            activity.start(
                command.started_at
            )

            self._activity_repository.save(
                activity
            )

        work_session = WorkSession(
            code=command.code,
            work_order_code=work_order.code,
            activity_code=activity.code,
            person_code=person.code,
            started_at=command.started_at,
            source=(
                WorkSessionSource.AUTOMATIC
            ),
            created_at=command.created_at,
            created_by_person_code=(
                command.created_by_person_code
            ),
        )

        self._work_session_repository.save(
            work_session
        )

        return StartWorkSessionResult(
            work_session=work_session
        )
