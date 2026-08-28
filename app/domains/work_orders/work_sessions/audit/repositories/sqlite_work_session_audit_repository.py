from sqlalchemy import (
    select,
)

from app.domains.work_orders.work_sessions.audit.entities import (
    WorkSessionAuditEntry,
)

from app.domains.work_orders.work_sessions.audit.value_objects import (
    WorkSessionAuditEventType,
)

from app.domains.work_orders.work_sessions.models import (
    WorkSessionAuditEntryModel,
)

from .work_session_audit_repository import (
    WorkSessionAuditRepository,
)


class SQLiteWorkSessionAuditRepository(
    WorkSessionAuditRepository,
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
        entry: WorkSessionAuditEntry,
    ) -> None:

        model = WorkSessionAuditEntryModel(
            work_session_code=(
                entry.work_session_code
            ),
            event_type=(
                entry.event_type.value
            ),
            reason=entry.reason,
            actor_person_code=(
                entry.actor_person_code
            ),
            occurred_at=(
                entry.occurred_at
            ),
            previous_started_at=(
                entry.previous_started_at
            ),
            previous_ended_at=(
                entry.previous_ended_at
            ),
            new_started_at=(
                entry.new_started_at
            ),
            new_ended_at=(
                entry.new_ended_at
            ),
        )

        with self._session_factory() as session:

            session.add(
                model
            )

            session.commit()

    def list_by_work_session(
        self,
        work_session_code: str,
    ) -> list[WorkSessionAuditEntry]:

        normalized_work_session_code = (
            self._normalize_code(
                work_session_code
            )
        )

        with self._session_factory() as session:

            statement = (
                select(
                    WorkSessionAuditEntryModel
                )
                .where(
                    WorkSessionAuditEntryModel.work_session_code
                    == normalized_work_session_code
                )
                .order_by(
                    WorkSessionAuditEntryModel.occurred_at
                    .asc(),
                    WorkSessionAuditEntryModel.id
                    .asc(),
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
    def _normalize_code(
        value,
    ) -> str:

        return str(
            value
        ).strip().upper()

    @staticmethod
    def _to_entity(
        model: WorkSessionAuditEntryModel,
    ) -> WorkSessionAuditEntry:

        return WorkSessionAuditEntry(
            work_session_code=(
                model.work_session_code
            ),
            event_type=(
                WorkSessionAuditEventType(
                    model.event_type
                )
            ),
            reason=model.reason,
            actor_person_code=(
                model.actor_person_code
            ),
            occurred_at=(
                model.occurred_at
            ),
            previous_started_at=(
                model.previous_started_at
            ),
            previous_ended_at=(
                model.previous_ended_at
            ),
            new_started_at=(
                model.new_started_at
            ),
            new_ended_at=(
                model.new_ended_at
            ),
        )
