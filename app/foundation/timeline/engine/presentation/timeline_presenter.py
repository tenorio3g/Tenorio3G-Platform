from app.foundation.timeline.engine.use_cases import (
    ListTimelineEventsResult,
)

from .timeline_view_model import (
    TimelineEventItemViewModel,
    TimelineViewModel,
)


class TimelinePresenter:

    EVENT_TYPE_LABELS = {
        "WORK_ORDER_CREATED": "Creación",
        "WORK_ORDER_ASSIGNED": "Asignación",
        "WORK_ORDER_STARTED": "Inicio",
        "WORK_ORDER_ON_HOLD": "Pausa",
        "WORK_ORDER_RESUMED": "Reanudación",
        "WORK_ORDER_COMPLETED": "Finalización",
        "WORK_ORDER_CLOSED": "Cierre",
        "WORK_ORDER_CANCELLED": "Cancelación",
    }

    @classmethod
    def present(
        cls,
        result: ListTimelineEventsResult,
    ) -> TimelineViewModel:

        items = [
            TimelineEventItemViewModel(
                event_id=item.event_id,
                event_type=item.event_type,
                event_type_label=(
                    cls._get_event_type_label(
                        item.event_type
                    )
                ),
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

    @classmethod
    def _get_event_type_label(
        cls,
        event_type: str,
    ) -> str:

        return cls.EVENT_TYPE_LABELS.get(
            event_type,
            event_type
            .replace("_", " ")
            .title(),
        )