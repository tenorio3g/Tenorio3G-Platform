from abc import ABC, abstractmethod

from app.domains.work_orders.work_sessions.audit.entities import (
    WorkSessionAuditEntry,
)


class WorkSessionAuditRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        entry: WorkSessionAuditEntry,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_by_work_session(
        self,
        work_session_code: str,
    ) -> list[WorkSessionAuditEntry]:
        raise NotImplementedError
