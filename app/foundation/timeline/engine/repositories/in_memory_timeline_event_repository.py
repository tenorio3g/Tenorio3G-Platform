from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)

from .timeline_event_repository import (
    TimelineEventRepository,
)


class InMemoryTimelineEventRepository(
    TimelineEventRepository,
):

    def __init__(
        self,
    ):
        self._events: dict[
            str,
            TimelineEvent,
        ] = {}

    def save(
        self,
        event: TimelineEvent,
    ) -> None:

        self._events[
            event.event_id
        ] = event

    def get_by_id(
        self,
        event_id: str,
    ) -> TimelineEvent | None:

        normalized_id = str(
            event_id
        ).strip().upper()

        return self._events.get(
            normalized_id
        )

    def list_by_entity(
        self,
        entity_type: str,
        entity_code: str,
    ) -> list[TimelineEvent]:

        normalized_type = str(
            entity_type
        ).strip().upper()

        normalized_code = str(
            entity_code
        ).strip().upper()

        events = [
            event
            for event in self._events.values()
            if (
                event.entity_type == normalized_type
                and
                event.entity_code == normalized_code
            )
        ]

        return sorted(
            events,
            key=lambda event: event.occurred_at,
            reverse=True,
        )