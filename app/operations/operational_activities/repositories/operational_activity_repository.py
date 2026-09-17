from abc import ABC, abstractmethod
from datetime import date

from app.operations.operational_activities.entities.operational_activity import (
    OperationalActivity,
)


class OperationalActivityRepository(ABC):
    @abstractmethod
    def save(
        self,
        activity: OperationalActivity,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> OperationalActivity | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[OperationalActivity]:
        raise NotImplementedError

    @abstractmethod
    def list_by_date(
        self,
        report_date: date,
    ) -> list[OperationalActivity]:
        raise NotImplementedError
