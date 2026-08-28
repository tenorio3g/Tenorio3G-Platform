from abc import ABC, abstractmethod

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)


class WorkSessionRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        work_session: WorkSession,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> WorkSession | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_activity(
        self,
        activity_code: str,
    ) -> list[WorkSession]:
        raise NotImplementedError

    @abstractmethod
    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkSession]:
        raise NotImplementedError

    @abstractmethod
    def list_by_person(
        self,
        person_code: str,
    ) -> list[WorkSession]:
        raise NotImplementedError
    @abstractmethod
    def has_overlap(
        self,
        person_code: str,
        started_at,
        ended_at,
        exclude_work_session_code: str | None = None,
    ) -> bool:
        raise NotImplementedError
    @abstractmethod
    def get_active_by_person(
        self,
        person_code: str,
    ) -> WorkSession | None:
        raise NotImplementedError
