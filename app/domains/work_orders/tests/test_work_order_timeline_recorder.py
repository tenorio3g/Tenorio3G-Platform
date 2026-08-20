from datetime import datetime

import pytest

from app.foundation.timeline.engine.repositories import (
    InMemoryTimelineEventRepository,
)

from app.foundation.timeline.engine.use_cases import (
    RecordTimelineEvent,
)

from app.domains.work_orders.timeline import (
    WorkOrderTimelineRecorder,
)


def build_recorder():

    repository = (
        InMemoryTimelineEventRepository()
    )

    record_timeline_event = (
        RecordTimelineEvent(
            repository
        )
    )

    recorder = WorkOrderTimelineRecorder(
        record_timeline_event
    )

    return repository, recorder


def test_should_record_work_order_lifecycle_event():

    repository, recorder = build_recorder()

    occurred_at = datetime(
        2026,
        8,
        19,
        18,
        30,
    )

    recorder.record(
        work_order_code="wo-001",
        event_type="work_order_started",
        actor_person_code="55464",
        occurred_at=occurred_at,
    )

    events = repository.list_by_entity(
        "WORK_ORDER",
        "WO-001",
    )

    assert len(events) == 1

    event = events[0]

    assert (
        event.event_type
        == "WORK_ORDER_STARTED"
    )

    assert (
        event.title
        == "Orden de trabajo iniciada"
    )

    assert (
        event.actor_person_code
        == "55464"
    )

    assert (
        event.occurred_at
        == occurred_at
    )


@pytest.mark.parametrize(
    "event_type",
    [
        "WORK_ORDER_ASSIGNED",
        "WORK_ORDER_STARTED",
        "WORK_ORDER_HELD",
        "WORK_ORDER_RESUMED",
        "WORK_ORDER_COMPLETED",
        "WORK_ORDER_CLOSED",
        "WORK_ORDER_CANCELLED",
    ],
)
def test_should_support_lifecycle_events(
    event_type,
):

    repository, recorder = build_recorder()

    recorder.record(
        work_order_code="WO-001",
        event_type=event_type,
        actor_person_code="55464",
        occurred_at=datetime(
            2026,
            8,
            19,
        ),
    )

    events = repository.list_by_entity(
        "WORK_ORDER",
        "WO-001",
    )

    assert len(events) == 1
    assert events[0].event_type == event_type


def test_should_reject_unsupported_event():

    _, recorder = build_recorder()

    with pytest.raises(
        ValueError,
        match=(
            "unsupported work order timeline event"
        ),
    ):
        recorder.record(
            work_order_code="WO-001",
            event_type="INVALID_EVENT",
            actor_person_code="55464",
            occurred_at=datetime(
                2026,
                8,
                19,
            ),
        )