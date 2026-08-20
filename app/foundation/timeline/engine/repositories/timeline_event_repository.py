from abc import ABC, abstractmethod

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)


class TimelineEventRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        event: TimelineEvent,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        event_id: str,
    ) -> TimelineEvent | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_entity(
        self,
        entity_type: str,
        entity_code: str,
    ) -> list[TimelineEvent]:
        raise NotImplementedError