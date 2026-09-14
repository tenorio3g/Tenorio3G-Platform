from dataclasses import dataclass

from app.domains.identity.people.entities import (
    Person,
)

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
class WorkSessionSummaryItem:
    work_session: WorkSession
    person: Person


@dataclass(frozen=True)
class GetWorkSessionSummaryQuery:
    work_order_code: str


@dataclass(frozen=True)
class GetWorkSessionSummaryResult:
    items: list[WorkSessionSummaryItem]


class GetWorkSessionSummary:

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
        query: GetWorkSessionSummaryQuery,
    ) -> GetWorkSessionSummaryResult:

        sessions = (
            self._work_session_repository
            .list_by_work_order(
                query.work_order_code
            )
        )

        items = []

        for work_session in sessions:

            person = (
                self._person_repository
                .get_by_code(
                    work_session.person_code
                )
            )

            if person is None:
                continue

            items.append(
                WorkSessionSummaryItem(
                    work_session=work_session,
                    person=person,
                )
            )

        return GetWorkSessionSummaryResult(
            items=items
        )