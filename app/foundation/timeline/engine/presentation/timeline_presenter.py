from app.foundation.timeline.engine.use_cases import (
    ListTimelineEventsResult,
)

from .timeline_view_model import (
    TimelineEventItemViewModel,
    TimelineViewModel,
)


class TimelinePresenter:

    @staticmethod
    def present(
        result: ListTimelineEventsResult,
    ) -> TimelineViewModel:

        items = [
            TimelineEventItemViewModel(
                event_id=item.event_id,
                event_type=item.event_type,
                title=item.title,
                description=item.description,
                actor_person_code=(
                    item.actor_person_code
                ),
                occurred_at=(
                    item.occurred_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                ),
                reference_type=(
                    item.reference_type
                ),
                reference_code=(
                    item.reference_code
                ),
            )
            for item in result.items
        ]

        return TimelineViewModel(
            items=items
        )