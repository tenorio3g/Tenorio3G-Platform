from dataclasses import dataclass

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)

from app.foundation.timeline.engine.repositories import (
    TimelineEventRepository,
)


@dataclass(frozen=True)
class ListTimelineEventsQuery:
    entity_type: str
    entity_code: str


@dataclass(frozen=True)
class ListTimelineEventsResult:
    items: list[TimelineEvent]


class ListTimelineEvents:

    def __init__(
        self,
        repository: TimelineEventRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: ListTimelineEventsQuery,
    ) -> ListTimelineEventsResult:

        items = (
            self._repository
            .list_by_entity(
                query.entity_type,
                query.entity_code,
            )
        )

        return ListTimelineEventsResult(
            items=items
        )