from app.foundation.database import (
    SessionLocal,
)

from app.foundation.timeline.engine.repositories import (
    SQLiteTimelineEventRepository,
)

from app.foundation.timeline.engine.use_cases import (
    ListTimelineEvents,
    RecordTimelineEvent,
)


timeline_event_repository = (
    SQLiteTimelineEventRepository(
        SessionLocal
    )
)


record_timeline_event = (
    RecordTimelineEvent(
        timeline_event_repository
    )
)


list_timeline_events = (
    ListTimelineEvents(
        timeline_event_repository
    )
)