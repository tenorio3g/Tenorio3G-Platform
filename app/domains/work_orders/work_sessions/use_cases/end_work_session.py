from dataclasses import dataclass
from datetime import datetime

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from app.domains.work_orders.work_sessions.repositories import (
    WorkSessionRepository,
)


@dataclass(frozen=True)
class EndWorkSessionCommand:
    code: str
    ended_at: datetime
    actor_person_code: str


@dataclass(frozen=True)
class EndWorkSessionResult:
    work_session: WorkSession


class EndWorkSession:

    def __init__(
        self,
        work_session_repository: WorkSessionRepository,
        person_repository: PersonRepository,
    ):
        self._work_session_repository = (
            work_session_repository
        )

        self._person_repository = (
            person_repository
        )

    def execute(
        self,
        command: EndWorkSessionCommand,
    ) -> EndWorkSessionResult:

        work_session = (
            self._work_session_repository.get_by_code(
                command.code
            )
        )

        if work_session is None:
            raise ValueError(
                "work session not found"
            )

        actor_code = str(
            command.actor_person_code
        ).strip()

        actor = (
            self._person_repository.get_by_code(
                actor_code
            )
        )

        if actor is None:
            raise ValueError(
                "actor person not found"
            )

        if not actor.is_active:
            raise ValueError(
                "actor person is inactive"
            )

        if (
            actor.code
            != work_session.person_code
        ):
            raise ValueError(
                "actor does not own work session"
            )

        work_session.end(
            command.ended_at
        )

        self._work_session_repository.save(
            work_session
        )

        return EndWorkSessionResult(
            work_session=work_session
        )
