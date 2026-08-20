from datetime import datetime

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)

from app.foundation.timeline.engine.repositories import (
    InMemoryTimelineEventRepository,
)

from app.foundation.timeline.engine.use_cases import (
    ListTimelineEvents,
    ListTimelineEventsQuery,
)


def test_should_list_timeline_events():

    repository = (
        InMemoryTimelineEventRepository()
    )

    repository.save(
        TimelineEvent(
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
                10,
                0,
            ),
        )
    )

    repository.save(
        TimelineEvent(
            event_id="EVT-002",
            entity_type="WORK_ORDER",
            entity_code="WO-001",
            event_type="STARTED",
            title="Orden iniciada",
            actor_person_code="55464",
            occurred_at=datetime(
                2026,
                8,
                19,
                12,
                0,
            ),
        )
    )

    use_case = ListTimelineEvents(
        repository
    )

    result = use_case.execute(
        ListTimelineEventsQuery(
            entity_type="work_order",
            entity_code="wo-001",
        )
    )

    assert len(
        result.items
    ) == 2

    assert (
        result.items[0].event_id
        == "EVT-002"
    )

    assert (
        result.items[1].event_id
        == "EVT-001"
    )


def test_should_return_empty_list():

    repository = (
        InMemoryTimelineEventRepository()
    )

    use_case = ListTimelineEvents(
        repository
    )

    result = use_case.execute(
        ListTimelineEventsQuery(
            entity_type="WORK_ORDER",
            entity_code="WO-X",
        )
    )

    assert result.items == []