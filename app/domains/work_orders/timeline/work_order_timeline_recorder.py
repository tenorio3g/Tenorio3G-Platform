from datetime import datetime

from app.foundation.timeline.engine.use_cases import (
    RecordTimelineEvent,
    RecordTimelineEventCommand,
)


class WorkOrderTimelineRecorder:

    EVENT_TITLES = {
        "WORK_ORDER_APPROVED": (
            "Orden de trabajo aprobada"
        ),
        "WORK_ORDER_ASSIGNED": (
            "Orden de trabajo asignada"
        ),
        "WORK_ORDER_STARTED": (
            "Orden de trabajo iniciada"
        ),
        "WORK_ORDER_HELD": (
            "Orden de trabajo pausada"
        ),
        "WORK_ORDER_RESUMED": (
            "Orden de trabajo reanudada"
        ),
        "WORK_ORDER_COMPLETED": (
            "Orden de trabajo completada"
        ),
        "WORK_ORDER_CLOSED": (
            "Orden de trabajo cerrada"
        ),
        "WORK_ORDER_CANCELLED": (
            "Orden de trabajo cancelada"
        ),
    }

    def __init__(
        self,
        record_timeline_event: RecordTimelineEvent,
    ):
        self._record_timeline_event = (
            record_timeline_event
        )

    def record(
        self,
        work_order_code: str,
        event_type: str,
        actor_person_code: str,
        occurred_at: datetime,
        description: str = "",
    ):

        normalized_event_type = str(
            event_type
        ).strip().upper()

        title = self.EVENT_TITLES.get(
            normalized_event_type
        )

        if title is None:
            raise ValueError(
                "unsupported work order timeline event"
            )

        return self._record_timeline_event.execute(
            RecordTimelineEventCommand(
                entity_type="WORK_ORDER",
                entity_code=work_order_code,
                event_type=normalized_event_type,
                title=title,
                actor_person_code=actor_person_code,
                occurred_at=occurred_at,
                description=description,
                reference_type="WORK_ORDER",
                reference_code=work_order_code,
            )
        )