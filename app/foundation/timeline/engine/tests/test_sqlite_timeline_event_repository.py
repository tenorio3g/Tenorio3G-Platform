from datetime import datetime

from sqlalchemy import (
    create_engine,
)

from sqlalchemy.orm import (
    sessionmaker,
)

from app.foundation.database import (
    Base,
)

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)

from app.foundation.timeline.engine.repositories import (
    SQLiteTimelineEventRepository,
)


def create_repository():

    engine = create_engine(
        "sqlite:///:memory:"
    )

    Base.metadata.create_all(
        engine
    )

    session_factory = sessionmaker(
        bind=engine,
    )

    return SQLiteTimelineEventRepository(
        session_factory
    )


def create_event(
    event_id="EVT-001",
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
        description="Prueba SQLite",
        reference_type="WORK_ORDER",
        reference_code=entity_code,
    )


def test_should_save_and_get_event():

    repository = create_repository()

    event = create_event()

    repository.save(
        event
    )

    persisted = repository.get_by_id(
        "evt-001"
    )

    assert persisted is not None

    assert (
        persisted.event_id
        == "EVT-001"
    )

    assert (
        persisted.entity_code
        == "WO-001"
    )

    assert (
        persisted.description
        == "Prueba SQLite"
    )


def test_should_update_existing_event():

    repository = create_repository()

    event = create_event()

    repository.save(
        event
    )

    updated = TimelineEvent(
        event_id="EVT-001",
        entity_type="WORK_ORDER",
        entity_code="WO-001",
        event_type="UPDATED",
        title="Evento actualizado",
        actor_person_code="55464",
        occurred_at=datetime(
            2026,
            8,
            19,
            13,
            0,
        ),
        description="Actualizado",
    )

    repository.save(
        updated
    )

    persisted = repository.get_by_id(
        "EVT-001"
    )

    assert (
        persisted.event_type
        == "UPDATED"
    )

    assert (
        persisted.title
        == "Evento actualizado"
    )


def test_should_list_by_entity():

    repository = create_repository()

    repository.save(
        create_event(
            event_id="EVT-001",
            entity_code="WO-001",
        )
    )

    repository.save(
        create_event(
            event_id="EVT-002",
            entity_code="WO-002",
        )
    )

    repository.save(
        create_event(
            event_id="EVT-003",
            entity_code="WO-001",
        )
    )

    events = repository.list_by_entity(
        "work_order",
        "wo-001",
    )

    assert len(events) == 2


def test_should_order_events_descending():

    repository = create_repository()

    repository.save(
        create_event(
            event_id="EVT-OLD",
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
            event_id="EVT-NEW",
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

    assert (
        events[0].event_id
        == "EVT-NEW"
    )

    assert (
        events[1].event_id
        == "EVT-OLD"
    )