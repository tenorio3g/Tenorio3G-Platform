from app.domains.work_orders.work_sessions.audit.entities import (
    WorkSessionAuditEntry,
)

from .work_session_audit_repository import (
    WorkSessionAuditRepository,
)


class InMemoryWorkSessionAuditRepository(
    WorkSessionAuditRepository,
):

    def __init__(
        self,
    ):
        self._entries: list[
            WorkSessionAuditEntry
        ] = []

    def save(
        self,
        entry: WorkSessionAuditEntry,
    ) -> None:

        self._entries.append(
            entry
        )

    def list_by_work_session(
        self,
        work_session_code: str,
    ) -> list[WorkSessionAuditEntry]:

        normalized_code = (
            self._normalize_code(
                work_session_code
            )
        )

        return [
            entry
            for entry in self._entries
            if (
                entry.work_session_code
                == normalized_code
            )
        ]

    @staticmethod
    def _normalize_code(
        value: str,
    ) -> str:

        return str(
            value
        ).strip().upper()
