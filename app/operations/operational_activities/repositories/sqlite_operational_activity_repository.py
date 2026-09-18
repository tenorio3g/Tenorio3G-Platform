from datetime import (
    datetime,
    time,
    timedelta,
)

from sqlalchemy import (
    or_,
    select,
)

from app.operations.operational_activities.entities import (
    OperationalActivity,
    OperationalActivitySource,
)

from app.operations.operational_activities.models import (
    OperationalActivityModel,
)

from .operational_activity_repository import (
    OperationalActivityRepository,
)


class SQLiteOperationalActivityRepository(
    OperationalActivityRepository,
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
        activity: OperationalActivity,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                OperationalActivityModel,
                activity.code,
            )

            if model is None:

                model = OperationalActivityModel(
                    code=activity.code,
                    description=activity.description,
                    started_at=activity.started_at,
                    ended_at=activity.ended_at,
                    result_notes=activity.result_notes,
                    area=activity.area,
                    location_description=(
                        activity.location_description
                    ),
                    asset_code=activity.asset_code,
                    work_order_code=(
                        activity.work_order_code
                    ),
                    source=activity.source.value,
                    created_at=activity.created_at,
                    created_by_person_code=(
                        activity.created_by_person_code
                    ),
                    completed_at=(
                        activity.completed_at
                    ),
                    completed_by_person_code=(
                        activity.completed_by_person_code
                    ),
                )

                session.add(
                    model
                )

            else:

                model.description = (
                    activity.description
                )

                model.started_at = (
                    activity.started_at
                )

                model.ended_at = (
                    activity.ended_at
                )

                model.result_notes = (
                    activity.result_notes
                )

                model.area = activity.area

                model.location_description = (
                    activity.location_description
                )

                model.asset_code = (
                    activity.asset_code
                )

                model.work_order_code = (
                    activity.work_order_code
                )

                model.source = (
                    activity.source.value
                )

                model.created_at = (
                    activity.created_at
                )

                model.created_by_person_code = (
                    activity.created_by_person_code
                )

                model.completed_at = (
                    activity.completed_at
                )

                model.completed_by_person_code = (
                    activity.completed_by_person_code
                )

            session.commit()

    def get_by_code(
        self,
        code: str,
    ) -> OperationalActivity | None:

        normalized_code = (
            self._normalize_code(
                code
            )
        )

        with self._session_factory() as session:

            model = session.get(
                OperationalActivityModel,
                normalized_code,
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )

    def list_all(
        self,
    ) -> list[OperationalActivity]:

        with self._session_factory() as session:

            statement = select(
                OperationalActivityModel
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

    def list_by_date(
        self,
        report_date,
    ) -> list[OperationalActivity]:

        day_start = datetime.combine(
            report_date,
            time.min,
        )

        day_end = (
            day_start
            + timedelta(days=1)
        )

        with self._session_factory() as session:

            statement = (
                select(
                    OperationalActivityModel
                )
                .where(
                    OperationalActivityModel.started_at
                    < day_end,

                    or_(
                        OperationalActivityModel.ended_at
                        .is_(None),

                        OperationalActivityModel.ended_at
                        > day_start,
                    ),
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
        model: OperationalActivityModel,
    ) -> OperationalActivity:

        return OperationalActivity(
            code=model.code,
            description=model.description,
            started_at=model.started_at,
            ended_at=model.ended_at,
            result_notes=model.result_notes,
            area=model.area,
            location_description=(
                model.location_description
            ),
            asset_code=model.asset_code,
            work_order_code=(
                model.work_order_code
            ),
            source=OperationalActivitySource(
                model.source
            ),
            created_at=model.created_at,
            created_by_person_code=(
                model.created_by_person_code
            ),
            completed_at=model.completed_at,
            completed_by_person_code=(
                model.completed_by_person_code
            ),
        )
