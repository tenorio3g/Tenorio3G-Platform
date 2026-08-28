from dataclasses import dataclass
from datetime import datetime

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)

from app.domains.work_orders.activities.repositories import (
    WorkOrderActivityRepository,
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

from app.domains.work_orders.work_sessions.audit.entities import (
    WorkSessionAuditEntry,
)

from app.domains.work_orders.work_sessions.audit.repositories import (
    WorkSessionAuditRepository,
)

from app.domains.work_orders.work_sessions.audit.value_objects import (
    WorkSessionAuditEventType,
)


@dataclass(frozen=True)
class AddManualWorkSessionCommand:
    code: str
    work_order_code: str
    activity_code: str
    person_code: str
    started_at: datetime
    ended_at: datetime
    created_at: datetime
    created_by_person_code: str
    reason: str


@dataclass(frozen=True)
class AddManualWorkSessionResult:
    work_session: WorkSession


class AddManualWorkSession:

    def __init__(
        self,
        work_order_repository: WorkOrderRepository,
        activity_repository: WorkOrderActivityRepository,
        person_repository: PersonRepository,
        work_session_repository: WorkSessionRepository,
        audit_repository: WorkSessionAuditRepository,
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

        self._audit_repository = (
            audit_repository
        )

    def execute(
        self,
        command: AddManualWorkSessionCommand,
    ) -> AddManualWorkSessionResult:

        reason = str(
            command.reason
        ).strip()

        if not reason:
            raise ValueError(
                "reason is required"
            )

        work_order = (
            self._work_order_repository.get_by_code(
                command.work_order_code
            )
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
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

        if (
            self._work_session_repository.has_overlap(
                person_code=person.code,
                started_at=command.started_at,
                ended_at=command.ended_at,
            )
        ):
            raise ValueError(
                "work session overlaps existing session"
            )

        work_session = WorkSession(
            code=command.code,
            work_order_code=work_order.code,
            activity_code=activity.code,
            person_code=person.code,
            started_at=command.started_at,
            ended_at=command.ended_at,
            source=WorkSessionSource.MANUAL,
            created_at=command.created_at,
            created_by_person_code=(
                command.created_by_person_code
            ),
        )

        self._work_session_repository.save(
            work_session
        )

        audit_entry = WorkSessionAuditEntry(
            work_session_code=work_session.code,
            event_type=(
                WorkSessionAuditEventType.MANUAL_CREATED
            ),
            reason=reason,
            actor_person_code=(
                command.created_by_person_code
            ),
            occurred_at=command.created_at,
        )

        self._audit_repository.save(
            audit_entry
        )

        return AddManualWorkSessionResult(
            work_session=work_session
        )
