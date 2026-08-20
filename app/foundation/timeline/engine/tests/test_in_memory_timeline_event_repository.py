from datetime import datetime

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)

from app.foundation.timeline.engine.repositories import (
    InMemoryTimelineEventRepository,
)


def create_event(
    event_id,
    entity_type="WORK_ORDER",
    entity_code="WO-001",
    occurred_at=None,
):

    return TimelineEvent(
        event_id=event_id,
        entity_type=entity_type,
        entity_code=entity_code,
        event_type="CREATED",
        title="Evento",
        actor_person_code="55464",
        occurred_at=(
            occurred_at
            or datetime(
                2026,
                8,
                19,
                12,
                0,
            )
        ),
    )


def test_should_save_and_get_event():

    repository = (
        InMemoryTimelineEventRepository()
    )

    event = create_event(
        "EVT-001"
    )

    repository.save(
        event
    )

    persisted = repository.get_by_id(
        "evt-001"
    )

    assert persisted is event


def test_should_return_none_when_event_does_not_exist():

    repository = (
        InMemoryTimelineEventRepository()
    )

    assert repository.get_by_id(
        "EVT-X"
    ) is None


def test_should_list_events_by_entity():

    repository = (
        InMemoryTimelineEventRepository()
    )

    repository.save(
        create_event(
            "EVT-001",
            entity_code="WO-001",
        )
    )

    repository.save(
        create_event(
            "EVT-002",
            entity_code="WO-002",
        )
    )

    repository.save(
        create_event(
            "EVT-003",
            entity_code="WO-001",
        )
    )

    events = repository.list_by_entity(
        "work_order",
        "wo-001",
    )

    assert len(events) == 2

    assert {
        event.event_id
        for event in events
    } == {
        "EVT-001",
        "EVT-003",
    }


def test_should_order_events_descending():

    repository = (
        InMemoryTimelineEventRepository()
    )

    repository.save(
        create_event(
            "EVT-OLD",
            occurred_at=datetime(
                2026,
                8,
                19,
                8,
                0,
            ),
        )
    )

    repository.save(
        create_event(
            "EVT-NEW",
            occurred_at=datetime(
                2026,
                8,
                19,
                18,
                0,
            ),
        )
    )

    events = repository.list_by_entity(
        "WORK_ORDER",
        "WO-001",
    )

    assert events[0].event_id == "EVT-NEW"
    assert events[1].event_id == "EVT-OLD"


def test_should_separate_entity_types():

    repository = (
        InMemoryTimelineEventRepository()
    )

    repository.save(
        create_event(
            "EVT-WO",
            entity_type="WORK_ORDER",
            entity_code="WO-001",
        )
    )

    repository.save(
        create_event(
            "EVT-ASSET",
            entity_type="ASSET",
            entity_code="WO-001",
        )
    )

    events = repository.list_by_entity(
        "WORK_ORDER",
        "WO-001",
    )

    assert len(events) == 1
    assert events[0].event_id == "EVT-WO"