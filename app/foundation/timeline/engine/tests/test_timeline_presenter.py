from datetime import datetime

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)

from app.foundation.timeline.engine.presentation import (
    TimelinePresenter,
)

from app.foundation.timeline.engine.use_cases import (
    ListTimelineEventsResult,
)


def test_should_present_timeline_events():

    result = ListTimelineEventsResult(
        items=[
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
                    14,
                    30,
                ),
                description=(
                    "Orden registrada."
                ),
                reference_type=(
                    "WORK_ORDER"
                ),
                reference_code=(
                    "WO-001"
                ),
            )
        ]
    )

    view_model = TimelinePresenter.present(
        result
    )

    assert view_model.has_items is True
    assert view_model.total == 1

    item = view_model.items[0]

    assert item.event_id == "EVT-001"
    assert item.event_type == "CREATED"
    assert item.title == "Orden creada"

    assert (
        item.occurred_at
        == "19/08/2026 14:30"
    )

    assert (
        item.reference_code
        == "WO-001"
    )


def test_should_present_empty_timeline():

    result = ListTimelineEventsResult(
        items=[]
    )

    view_model = TimelinePresenter.present(
        result
    )

    assert view_model.has_items is False
    assert view_model.total == 0
    assert view_model.items == []