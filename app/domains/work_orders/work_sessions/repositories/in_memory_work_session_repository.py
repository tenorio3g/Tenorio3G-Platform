from datetime import datetime

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from .work_session_repository import (
    WorkSessionRepository,
)


class InMemoryWorkSessionRepository(
    WorkSessionRepository,
):

    def __init__(
        self,
    ):
        self._sessions: dict[
            str,
            WorkSession,
        ] = {}

    def save(
        self,
        work_session: WorkSession,
    ) -> None:

        self._sessions[
            work_session.code
        ] = work_session

    def get_by_code(
        self,
        code: str,
    ) -> WorkSession | None:

        normalized_code = self._normalize_code(
            code
        )

        return self._sessions.get(
            normalized_code
        )

    def list_by_activity(
        self,
        activity_code: str,
    ) -> list[WorkSession]:

        normalized_code = self._normalize_code(
            activity_code
        )

        return [
            session
            for session in self._sessions.values()
            if (
                session.activity_code
                == normalized_code
            )
        ]

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkSession]:

        normalized_code = self._normalize_code(
            work_order_code
        )

        return [
            session
            for session in self._sessions.values()
            if (
                session.work_order_code
                == normalized_code
            )
        ]

    def list_by_person(
        self,
        person_code: str,
    ) -> list[WorkSession]:

        normalized_code = self._normalize_code(
            person_code
        )

        return [
            session
            for session in self._sessions.values()
            if (
                session.person_code
                == normalized_code
            )
        ]

    def get_active_by_person(
        self,
        person_code: str,
    ) -> WorkSession | None:

        normalized_code = self._normalize_code(
            person_code
        )

        active_sessions = [
            session
            for session in self._sessions.values()
            if (
                session.person_code
                == normalized_code
                and session.is_active
            )
        ]

        if not active_sessions:
            return None

        return max(
            active_sessions,
            key=lambda session: (
                session.started_at
            ),
        )

    def has_overlap(
        self,
        person_code: str,
        started_at: datetime,
        ended_at: datetime,
        exclude_work_session_code: str | None = None,
    ) -> bool:

        normalized_person_code = (
            self._normalize_code(
                person_code
            )
        )

        normalized_excluded_code = None

        if exclude_work_session_code is not None:
            normalized_excluded_code = (
                self._normalize_code(
                    exclude_work_session_code
                )
            )

        for session in self._sessions.values():

            if (
                normalized_excluded_code is not None
                and session.code
                == normalized_excluded_code
            ):
                continue

            if (
                session.person_code
                != normalized_person_code
            ):
                continue

            existing_start = (
                session.started_at
            )

            existing_end = (
                session.ended_at
            )

            starts_before_new_ends = (
                existing_start
                < ended_at
            )

            existing_extends_past_new_start = (
                existing_end is None
                or existing_end > started_at
            )

            if (
                starts_before_new_ends
                and existing_extends_past_new_start
            ):
                return True

        return False
    @staticmethod
    def _normalize_code(
        value: str,
    ) -> str:

        return str(
            value
        ).strip().upper()
