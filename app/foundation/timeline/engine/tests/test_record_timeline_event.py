from datetime import datetime

import pytest

from app.foundation.timeline.engine.repositories import (
    InMemoryTimelineEventRepository,
)

from app.foundation.timeline.engine.use_cases import (
    RecordTimelineEvent,
    RecordTimelineEventCommand,
)


def test_should_record_timeline_event():

    repository = (
        InMemoryTimelineEventRepository()
    )

    use_case = RecordTimelineEvent(
        repository
    )

    result = use_case.execute(
        RecordTimelineEventCommand(
            event_id="EVT-001",
            entity_type="WORK_ORDER",
            entity_code="WO-001",
            event_type="CREATED",
            title="Orden creada",
            actor_person_code="55464",
            occurred_at=datetime(
                2026,
                8,
                19,
                12,
                0,
            ),
            description="Orden registrada.",
        )
    )

    assert (
        result.event.event_id
        == "EVT-001"
    )

    persisted = repository.get_by_id(
        "EVT-001"
    )

    assert persisted is result.event


def test_should_generate_event_id_when_missing():

    repository = (
        InMemoryTimelineEventRepository()
    )

    use_case = RecordTimelineEvent(
        repository
    )

    result = use_case.execute(
        RecordTimelineEventCommand(
            entity_type="WORK_ORDER",
            entity_code="WO-001",
            event_type="CREATED",
            title="Orden creada",
            actor_person_code="55464",
            occurred_at=datetime(
                2026,
                8,
                19,
            ),
        )
    )

    assert (
        result.event.event_id
        .startswith("EVT-")
    )


def test_should_reject_duplicate_event_id():

    repository = (
        InMemoryTimelineEventRepository()
    )

    use_case = RecordTimelineEvent(
        repository
    )

    command = RecordTimelineEventCommand(
        event_id="EVT-001",
        entity_type="WORK_ORDER",
        entity_code="WO-001",
        event_type="CREATED",
        title="Orden creada",
        actor_person_code="55464",
        occurred_at=datetime(
            2026,
            8,
            19,
        ),
    )

    use_case.execute(
        command
    )

    with pytest.raises(
        ValueError,
        match="timeline event already exists",
    ):
        use_case.execute(
            command
        )