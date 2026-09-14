from sqlalchemy import select

from app.domains.work_orders.activities.holds.entities import (
    ActivityHold,
)

from app.domains.work_orders.activities.holds.models import (
    ActivityHoldModel,
)

from app.domains.work_orders.activities.holds.value_objects import (
    ActivityHoldReason,
)

from .activity_hold_repository import (
    ActivityHoldRepository,
)


class SQLiteActivityHoldRepository(
    ActivityHoldRepository,
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
        hold: ActivityHold,
    ) -> None:

        with self._session_factory() as session:

            if hold.is_active:

                statement = (
                    select(
                        ActivityHoldModel
                    )
                    .where(
                        ActivityHoldModel.activity_code
                        == hold.activity_code
                    )
                    .where(
                        ActivityHoldModel.resumed_at
                        .is_(None)
                    )
                    .where(
                        ActivityHoldModel.code
                        != hold.code
                    )
                )

                existing_active = (
                    session.execute(
                        statement
                    )
                    .scalars()
                    .first()
                )

                if existing_active is not None:
                    raise ValueError(
                        "activity already has active hold"
                    )

            model = session.get(
                ActivityHoldModel,
                hold.code,
            )

            if model is None:

                model = ActivityHoldModel(
                    code=hold.code,
                    activity_code=(
                        hold.activity_code
                    ),
                    reason=hold.reason.value,
                    observations=(
                        hold.observations
                    ),
                    held_at=hold.held_at,
                    held_by_person_code=(
                        hold.held_by_person_code
                    ),
                    resumed_at=(
                        hold.resumed_at
                    ),
                    resumed_by_person_code=(
                        hold.resumed_by_person_code
                    ),
                )

                session.add(
                    model
                )

            else:

                model.activity_code = (
                    hold.activity_code
                )

                model.reason = (
                    hold.reason.value
                )

                model.observations = (
                    hold.observations
                )

                model.held_at = (
                    hold.held_at
                )

                model.held_by_person_code = (
                    hold.held_by_person_code
                )

                model.resumed_at = (
                    hold.resumed_at
                )

                model.resumed_by_person_code = (
                    hold.resumed_by_person_code
                )

            session.commit()


    def get_by_code(
        self,
        code: str,
    ) -> ActivityHold | None:

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                ActivityHoldModel,
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
    ) -> list[ActivityHold]:

        normalized_activity_code = str(
            activity_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    ActivityHoldModel
                )
                .where(
                    ActivityHoldModel.activity_code
                    == normalized_activity_code
                )
                .order_by(
                    ActivityHoldModel.held_at
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
                self._to_entity(
                    model
                )
                for model
                in models
            ]


    def get_active_by_activity(
        self,
        activity_code: str,
    ) -> ActivityHold | None:

        normalized_activity_code = str(
            activity_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    ActivityHoldModel
                )
                .where(
                    ActivityHoldModel.activity_code
                    == normalized_activity_code
                )
                .where(
                    ActivityHoldModel.resumed_at
                    .is_(None)
                )
                .order_by(
                    ActivityHoldModel.held_at.desc()
                )
            )

            model = (
                session.execute(
                    statement
                )
                .scalars()
                .first()
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )


    @staticmethod
    def _to_entity(
        model: ActivityHoldModel,
    ) -> ActivityHold:

        return ActivityHold(
            code=model.code,
            activity_code=(
                model.activity_code
            ),
            reason=ActivityHoldReason(
                model.reason
            ),
            observations=(
                model.observations
            ),
            held_at=model.held_at,
            held_by_person_code=(
                model.held_by_person_code
            ),
            resumed_at=model.resumed_at,
            resumed_by_person_code=(
                model.resumed_by_person_code
            ),
        )
