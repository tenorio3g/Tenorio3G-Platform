from datetime import datetime

import pytest

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)


def test_should_create_timeline_event():

    event = TimelineEvent(
        event_id="evt-001",
        entity_type="work_order",
        entity_code="wo-001",
        event_type="activity_completed",
        title="Actividad finalizada",
        actor_person_code="55464",
        occurred_at=datetime(
            2026,
            8,
            19,
            18,
            0,
        ),
        description="Inspección terminada.",
        reference_type="work_order_activity",
        reference_code="act-001",
    )

    assert event.event_id == "EVT-001"
    assert event.entity_type == "WORK_ORDER"
    assert event.entity_code == "WO-001"

    assert (
        event.event_type
        == "ACTIVITY_COMPLETED"
    )

    assert (
        event.reference_type
        == "WORK_ORDER_ACTIVITY"
    )

    assert (
        event.reference_code
        == "ACT-001"
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "event_id",
        "entity_type",
        "entity_code",
        "event_type",
        "title",
        "actor_person_code",
    ],
)
def test_should_require_fields(
    field_name,
):

    data = {
        "event_id": "EVT-001",
        "entity_type": "WORK_ORDER",
        "entity_code": "WO-001",
        "event_type": "CREATED",
        "title": "Orden creada",
        "actor_person_code": "55464",
        "occurred_at": datetime(
            2026,
            8,
            19,
        ),
    }

    data[field_name] = ""

    with pytest.raises(
        ValueError,
        match=f"{field_name} is required",
    ):
        TimelineEvent(
            **data
        )


def test_should_require_datetime():

    with pytest.raises(
        ValueError,
        match="occurred_at must be a datetime",
    ):
        TimelineEvent(
            event_id="EVT-001",
            entity_type="WORK_ORDER",
            entity_code="WO-001",
            event_type="CREATED",
            title="Orden creada",
            actor_person_code="55464",
            occurred_at="2026-08-19",
        )


def test_should_allow_empty_optional_references():

    event = TimelineEvent(
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
        reference_type="",
        reference_code="",
    )

    assert event.reference_type is None
    assert event.reference_code is None