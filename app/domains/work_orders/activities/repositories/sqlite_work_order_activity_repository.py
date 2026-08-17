from sqlalchemy import select

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.models import (
    WorkOrderActivityModel,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)

from .work_order_activity_repository import (
    WorkOrderActivityRepository,
)


class SQLiteWorkOrderActivityRepository(
    WorkOrderActivityRepository,
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
        activity: WorkOrderActivity,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                WorkOrderActivityModel,
                activity.code,
            )

            if model is None:

                model = WorkOrderActivityModel(
                    code=activity.code,
                    work_order_code=(
                        activity.work_order_code
                    ),
                    title=activity.title,
                    description=(
                        activity.description
                    ),
                    responsible_person_code=(
                        activity.responsible_person_code
                    ),
                    status=activity.status.value,
                    estimated_minutes=(
                        activity.estimated_minutes
                    ),
                    started_at=(
                        activity.started_at
                    ),
                    completed_at=(
                        activity.completed_at
                    ),
                )

                session.add(
                    model
                )

            else:

                model.work_order_code = (
                    activity.work_order_code
                )

                model.title = (
                    activity.title
                )

                model.description = (
                    activity.description
                )

                model.responsible_person_code = (
                    activity.responsible_person_code
                )

                model.status = (
                    activity.status.value
                )

                model.estimated_minutes = (
                    activity.estimated_minutes
                )

                model.started_at = (
                    activity.started_at
                )

                model.completed_at = (
                    activity.completed_at
                )

            session.commit()

    def get_by_code(
        self,
        code: str,
    ) -> WorkOrderActivity | None:

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                WorkOrderActivityModel,
                normalized_code,
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderActivity]:

        normalized_work_order_code = str(
            work_order_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    WorkOrderActivityModel
                )
                .where(
                    WorkOrderActivityModel.work_order_code
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

    def delete(
        self,
        code: str,
    ) -> None:

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                WorkOrderActivityModel,
                normalized_code,
            )

            if model is not None:

                session.delete(
                    model
                )

                session.commit()

    @staticmethod
    def _to_entity(
        model: WorkOrderActivityModel,
    ) -> WorkOrderActivity:

        return WorkOrderActivity(
            code=model.code,
            work_order_code=(
                model.work_order_code
            ),
            title=model.title,
            description=model.description,
            responsible_person_code=(
                model.responsible_person_code
            ),
            status=ActivityStatus(
                model.status
            ),
            estimated_minutes=(
                model.estimated_minutes
            ),
            started_at=model.started_at,
            completed_at=model.completed_at,
        )