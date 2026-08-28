from sqlalchemy import (
    and_,
    or_,
    select,
)

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from app.domains.work_orders.work_sessions.models import (
    WorkSessionModel,
)

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)

from .work_session_repository import (
    WorkSessionRepository,
)


class SQLiteWorkSessionRepository(
    WorkSessionRepository,
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
        work_session: WorkSession,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                WorkSessionModel,
                work_session.code,
            )

            if model is None:

                model = WorkSessionModel(
                    code=work_session.code,
                    work_order_code=(
                        work_session.work_order_code
                    ),
                    activity_code=(
                        work_session.activity_code
                    ),
                    person_code=(
                        work_session.person_code
                    ),
                    started_at=(
                        work_session.started_at
                    ),
                    ended_at=(
                        work_session.ended_at
                    ),
                    source=(
                        work_session.source.value
                    ),
                    created_at=(
                        work_session.created_at
                    ),
                    created_by_person_code=(
                        work_session.created_by_person_code
                    ),
                )

                session.add(
                    model
                )

            else:

                model.work_order_code = (
                    work_session.work_order_code
                )

                model.activity_code = (
                    work_session.activity_code
                )

                model.person_code = (
                    work_session.person_code
                )

                model.started_at = (
                    work_session.started_at
                )

                model.ended_at = (
                    work_session.ended_at
                )

                model.source = (
                    work_session.source.value
                )

                model.created_at = (
                    work_session.created_at
                )

                model.created_by_person_code = (
                    work_session.created_by_person_code
                )

            session.commit()

    def get_by_code(
        self,
        code: str,
    ) -> WorkSession | None:

        normalized_code = (
            self._normalize_code(
                code
            )
        )

        with self._session_factory() as session:

            model = session.get(
                WorkSessionModel,
                normalized_code,
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )

    def list_by_activity(
        self,
        activity_code: str,
    ) -> list[WorkSession]:

        normalized_activity_code = (
            self._normalize_code(
                activity_code
            )
        )

        with self._session_factory() as session:

            statement = (
                select(
                    WorkSessionModel
                )
                .where(
                    WorkSessionModel.activity_code
                    == normalized_activity_code
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

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkSession]:

        normalized_work_order_code = (
            self._normalize_code(
                work_order_code
            )
        )

        with self._session_factory() as session:

            statement = (
                select(
                    WorkSessionModel
                )
                .where(
                    WorkSessionModel.work_order_code
                    == normalized_work_order_code
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

    def list_by_person(
        self,
        person_code: str,
    ) -> list[WorkSession]:

        normalized_person_code = (
            self._normalize_code(
                person_code
            )
        )

        with self._session_factory() as session:

            statement = (
                select(
                    WorkSessionModel
                )
                .where(
                    WorkSessionModel.person_code
                    == normalized_person_code
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

    def has_overlap(
        self,
        person_code: str,
        started_at,
        ended_at,
        exclude_work_session_code: str | None = None,
    ) -> bool:

        normalized_person_code = (
            self._normalize_code(
                person_code
            )
        )

        conditions = [
            WorkSessionModel.person_code
            == normalized_person_code,

            WorkSessionModel.started_at
            < ended_at,

            or_(
                WorkSessionModel.ended_at
                .is_(None),

                WorkSessionModel.ended_at
                > started_at,
            ),
        ]

        if exclude_work_session_code is not None:

            normalized_excluded_code = (
                self._normalize_code(
                    exclude_work_session_code
                )
            )

            conditions.append(
                WorkSessionModel.code
                != normalized_excluded_code
            )

        with self._session_factory() as session:

            statement = (
                select(
                    WorkSessionModel.code
                )
                .where(
                    and_(
                        *conditions
                    )
                )
                .limit(1)
            )

            result = (
                session.execute(
                    statement
                )
                .scalar_one_or_none()
            )

            return result is not None

    def get_active_by_person(
        self,
        person_code: str,
    ) -> WorkSession | None:

        normalized_person_code = (
            self._normalize_code(
                person_code
            )
        )

        with self._session_factory() as session:

            statement = (
                select(
                    WorkSessionModel
                )
                .where(
                    WorkSessionModel.person_code
                    == normalized_person_code,
                    WorkSessionModel.ended_at
                    .is_(None),
                )
                .order_by(
                    WorkSessionModel.started_at
                    .desc()
                )
                .limit(1)
            )

            model = (
                session.execute(
                    statement
                )
                .scalar_one_or_none()
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )

    @staticmethod
    def _normalize_code(
        value,
    ) -> str:

        return str(
            value
        ).strip().upper()

    @staticmethod
    def _to_entity(
        model: WorkSessionModel,
    ) -> WorkSession:

        return WorkSession(
            code=model.code,
            work_order_code=(
                model.work_order_code
            ),
            activity_code=(
                model.activity_code
            ),
            person_code=(
                model.person_code
            ),
            started_at=(
                model.started_at
            ),
            ended_at=(
                model.ended_at
            ),
            source=WorkSessionSource(
                model.source
            ),
            created_at=(
                model.created_at
            ),
            created_by_person_code=(
                model.created_by_person_code
            ),
        )
