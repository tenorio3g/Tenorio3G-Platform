from abc import ABC, abstractmethod

from app.domains.work_orders.activities.holds.entities import (
    ActivityHold,
)


class ActivityHoldRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        hold: ActivityHold,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> ActivityHold | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_activity(
        self,
        activity_code: str,
    ) -> list[ActivityHold]:
        raise NotImplementedError

    @abstractmethod
    def get_active_by_activity(
        self,
        activity_code: str,
    ) -> ActivityHold | None:
        raise NotImplementedError
