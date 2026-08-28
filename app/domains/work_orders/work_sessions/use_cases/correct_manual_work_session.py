from dataclasses import dataclass
from datetime import datetime

from app.domains.identity.people.repositories import (
    PersonRepository,
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
class CorrectManualWorkSessionCommand:
    code: str
    started_at: datetime
    ended_at: datetime
    corrected_at: datetime
    corrected_by_person_code: str
    reason: str


@dataclass(frozen=True)
class CorrectManualWorkSessionResult:
    work_session: WorkSession


class CorrectManualWorkSession:

    def __init__(
        self,
        work_session_repository: WorkSessionRepository,
        person_repository: PersonRepository,
        audit_repository: WorkSessionAuditRepository,
    ):
        self._work_session_repository = (
            work_session_repository
        )

        self._person_repository = (
            person_repository
        )

        self._audit_repository = (
            audit_repository
        )

    def execute(
        self,
        command: CorrectManualWorkSessionCommand,
    ) -> CorrectManualWorkSessionResult:

        work_session = (
            self._work_session_repository.get_by_code(
                command.code
            )
        )

        if work_session is None:
            raise ValueError(
                "work session not found"
            )

        if (
            work_session.source
            != WorkSessionSource.MANUAL
        ):
            raise ValueError(
                "only manual work sessions "
                "can be corrected"
            )

        reason = (
            ""
            if command.reason is None
            else str(command.reason).strip()
        )

        if not reason:
            raise ValueError(
                "reason is required"
            )

        actor_code = str(
            command.corrected_by_person_code
        ).strip()

        actor = (
            self._person_repository.get_by_code(
                actor_code
            )
        )

        if actor is None:
            raise ValueError(
                "correction actor not found"
            )

        if not actor.is_active:
            raise ValueError(
                "correction actor is inactive"
            )

        if not isinstance(
            command.started_at,
            datetime,
        ):
            raise ValueError(
                "started_at must be datetime"
            )

        if not isinstance(
            command.ended_at,
            datetime,
        ):
            raise ValueError(
                "ended_at must be datetime"
            )

        if command.ended_at < command.started_at:
            raise ValueError(
                "end cannot be before start"
            )

        if not isinstance(
            command.corrected_at,
            datetime,
        ):
            raise ValueError(
                "corrected_at must be datetime"
            )

        has_overlap = (
            self._work_session_repository.has_overlap(
                person_code=work_session.person_code,
                started_at=command.started_at,
                ended_at=command.ended_at,
                exclude_work_session_code=(
                    work_session.code
                ),
            )
        )

        if has_overlap:
            raise ValueError(
                "work session overlaps "
                "existing session"
            )

        previous_started_at = (
            work_session.started_at
        )

        previous_ended_at = (
            work_session.ended_at
        )

        work_session.correct(
            started_at=command.started_at,
            ended_at=command.ended_at,
        )

        self._work_session_repository.save(
            work_session
        )

        audit_entry = WorkSessionAuditEntry(
            work_session_code=work_session.code,
            event_type=(
                WorkSessionAuditEventType.CORRECTED
            ),
            reason=reason,
            actor_person_code=actor.code,
            occurred_at=command.corrected_at,
            previous_started_at=(
                previous_started_at
            ),
            previous_ended_at=(
                previous_ended_at
            ),
            new_started_at=(
                work_session.started_at
            ),
            new_ended_at=(
                work_session.ended_at
            ),
        )

        self._audit_repository.save(
            audit_entry
        )

        return CorrectManualWorkSessionResult(
            work_session=work_session
        )
