from datetime import datetime

import pytest

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)

from app.foundation.timeline.engine.repositories import (
    InMemoryTimelineEventRepository,
)

from app.foundation.timeline.engine.use_cases import (
    RecordTimelineEvent,
    RecordTimelineEventCommand,
)


def test_should_allow_registered_actor():

    event = TimelineEvent(
        event_id="EVT-REGISTERED",
        entity_type="WORK_ORDER",
        entity_code="WO-001",
        event_type="CREATED",
        title="Orden creada",
        actor_person_code="req-001",
        occurred_at=datetime(
            2026,
            8,
            22,
            20,
            0,
        ),
        actor_name="Fortunato Tenorio",
    )

    assert (
        event.actor_person_code
        == "REQ-001"
    )

    assert (
        event.actor_name
        == "Fortunato Tenorio"
    )


def test_should_allow_manual_actor():

    event = TimelineEvent(
        event_id="EVT-MANUAL",
        entity_type="WORK_ORDER",
        entity_code="WO-001",
        event_type="CREATED",
        title="Orden creada",
        actor_person_code=None,
        actor_name="Juan Perez",
        occurred_at=datetime(
            2026,
            8,
            22,
            20,
            0,
        ),
    )

    assert event.actor_person_code is None

    assert (
        event.actor_name
        == "Juan Perez"
    )


def test_should_require_actor_identity():

    with pytest.raises(
        ValueError,
        match=(
            "actor_person_code or "
            "actor_name is required"
        ),
    ):

        TimelineEvent(
            event_id="EVT-NO-ACTOR",
            entity_type="WORK_ORDER",
            entity_code="WO-001",
            event_type="CREATED",
            title="Orden creada",
            actor_person_code=None,
            actor_name=None,
            occurred_at=datetime(
                2026,
                8,
                22,
                20,
                0,
            ),
        )


def test_should_record_manual_actor():

    repository = (
        InMemoryTimelineEventRepository()
    )

    use_case = RecordTimelineEvent(
        repository
    )

    result = use_case.execute(
        RecordTimelineEventCommand(
            event_id="EVT-MANUAL",
            entity_type="WORK_ORDER",
            entity_code="WO-001",
            event_type="WORK_ORDER_CREATED",
            title="Orden de trabajo creada",
            actor_person_code=None,
            actor_name="Juan Perez",
            occurred_at=datetime(
                2026,
                8,
                22,
                20,
                0,
            ),
        )
    )

    assert (
        result.event.actor_person_code
        is None
    )

    assert (
        result.event.actor_name
        == "Juan Perez"
    )
