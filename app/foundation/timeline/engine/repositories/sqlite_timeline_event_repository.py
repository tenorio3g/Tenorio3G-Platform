from sqlalchemy import (
    select,
)

from app.foundation.timeline.engine.entities import (
    TimelineEvent,
)

from app.foundation.timeline.engine.models import (
    TimelineEventModel,
)

from .timeline_event_repository import (
    TimelineEventRepository,
)


class SQLiteTimelineEventRepository(
    TimelineEventRepository,
):

    def __init__(
        self,
        session_factory,
    ):
        self._session_factory = (
            session_factory
        )

    def save(
        self,
        event: TimelineEvent,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                TimelineEventModel,
                event.event_id,
            )

            if model is None:

                model = TimelineEventModel(
                    event_id=event.event_id,
                    entity_type=event.entity_type,
                    entity_code=event.entity_code,
                    event_type=event.event_type,
                    title=event.title,
                    description=event.description,
                    actor_person_code=(
                        event.actor_person_code
                    ),
                    occurred_at=event.occurred_at,
                    reference_type=(
                        event.reference_type
                    ),
                    reference_code=(
                        event.reference_code
                    ),
                )

                session.add(
                    model
                )

            else:

                model.entity_type = (
                    event.entity_type
                )

                model.entity_code = (
                    event.entity_code
                )

                model.event_type = (
                    event.event_type
                )

                model.title = (
                    event.title
                )

                model.description = (
                    event.description
                )

                model.actor_person_code = (
                    event.actor_person_code
                )

                model.occurred_at = (
                    event.occurred_at
                )

                model.reference_type = (
                    event.reference_type
                )

                model.reference_code = (
                    event.reference_code
                )

            session.commit()

    def get_by_id(
        self,
        event_id: str,
    ) -> TimelineEvent | None:

        normalized_id = str(
            event_id
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                TimelineEventModel,
                normalized_id,
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )

    def list_by_entity(
        self,
        entity_type: str,
        entity_code: str,
    ) -> list[TimelineEvent]:

        normalized_type = str(
            entity_type
        ).strip().upper()

        normalized_code = str(
            entity_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    TimelineEventModel
                )
                .where(
                    TimelineEventModel.entity_type
                    == normalized_type
                )
                .where(
                    TimelineEventModel.entity_code
                    == normalized_code
                )
                .order_by(
                    TimelineEventModel.occurred_at.desc()
                )
            )

            models = (
                session.execute(
                    statement
                )
                .scalars()
                .all()
            )

            return [
                self._to_entity(model)
                for model in models
            ]

    @staticmethod
    def _to_entity(
        model: TimelineEventModel,
    ) -> TimelineEvent:

        return TimelineEvent(
            event_id=model.event_id,
            entity_type=model.entity_type,
            entity_code=model.entity_code,
            event_type=model.event_type,
            title=model.title,
            description=model.description,
            actor_person_code=(
                model.actor_person_code
            ),
            occurred_at=model.occurred_at,
            reference_type=(
                model.reference_type
            ),
            reference_code=(
                model.reference_code
            ),
        )