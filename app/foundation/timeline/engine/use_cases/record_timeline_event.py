from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)

from app.foundation.timeline.engine.repositories import (
    TimelineEventRepository,
)


@dataclass(frozen=True)
class RecordTimelineEventCommand:
    entity_type: str
    entity_code: str
    event_type: str
    title: str
    actor_person_code: str | None
    occurred_at: datetime
    description: str = ""
    reference_type: str | None = None
    reference_code: str | None = None
    event_id: str | None = None
    actor_name: str | None = None


@dataclass(frozen=True)
class RecordTimelineEventResult:
    event: TimelineEvent


class RecordTimelineEvent:

    def __init__(
        self,
        repository: TimelineEventRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: RecordTimelineEventCommand,
    ) -> RecordTimelineEventResult:

        event_id = (
            str(command.event_id)
            .strip()
            .upper()
            if command.event_id
            else f"EVT-{uuid4().hex.upper()}"
        )

        existing = (
            self._repository
            .get_by_id(
                event_id
            )
        )

        if existing is not None:
            raise ValueError(
                "timeline event already exists"
            )

        event = TimelineEvent(
            event_id=event_id,
            entity_type=command.entity_type,
            entity_code=command.entity_code,
            event_type=command.event_type,
            title=command.title,
            actor_person_code=(
                command.actor_person_code
            ),
            actor_name=(
                command.actor_name
            ),
            occurred_at=command.occurred_at,
            description=command.description,
            reference_type=(
                command.reference_type
            ),
            reference_code=(
                command.reference_code
            ),
        )

        self._repository.save(
            event
        )

        return RecordTimelineEventResult(
            event=event
        )
