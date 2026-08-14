from sqlalchemy import select

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.models import (
    PreventiveMaintenancePlanModel,
)

from .preventive_maintenance_repository import (
    PreventiveMaintenanceRepository,
)


class SQLitePreventiveMaintenanceRepository(
    PreventiveMaintenanceRepository,
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
        plan: PreventiveMaintenancePlan,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                PreventiveMaintenancePlanModel,
                plan.code,
            )

            if model is None:

                model = (
                    PreventiveMaintenancePlanModel(
                        code=plan.code,
                        asset_code=plan.asset_code,
                        title=plan.title,
                        frequency_days=(
                            plan.frequency_days
                        ),
                        responsible_person_code=(
                            plan.responsible_person_code
                        ),
                        next_due_at=plan.next_due_at,
                        description=(
                            plan.description
                        ),
                        is_active=plan.is_active,
                    )
                )

                session.add(
                    model
                )

            else:

                model.asset_code = (
                    plan.asset_code
                )

                model.title = (
                    plan.title
                )

                model.frequency_days = (
                    plan.frequency_days
                )

                model.responsible_person_code = (
                    plan.responsible_person_code
                )

                model.next_due_at = (
                    plan.next_due_at
                )

                model.description = (
                    plan.description
                )

                model.is_active = (
                    plan.is_active
                )

            session.commit()

    def get_by_code(
        self,
        code: str,
    ) -> PreventiveMaintenancePlan | None:

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                PreventiveMaintenancePlanModel,
                normalized_code,
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )

    def list_by_asset(
        self,
        asset_code: str,
    ) -> list[PreventiveMaintenancePlan]:

        normalized_asset_code = str(
            asset_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    PreventiveMaintenancePlanModel
                )
                .where(
                    PreventiveMaintenancePlanModel.asset_code
                    == normalized_asset_code
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

    def list_all(
        self,
    ) -> list[PreventiveMaintenancePlan]:

        with self._session_factory() as session:

            statement = select(
                PreventiveMaintenancePlanModel
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
                PreventiveMaintenancePlanModel,
                normalized_code,
            )

            if model is not None:

                session.delete(
                    model
                )

                session.commit()

    @staticmethod
    def _to_entity(
        model: PreventiveMaintenancePlanModel,
    ) -> PreventiveMaintenancePlan:

        return PreventiveMaintenancePlan(
            code=model.code,
            asset_code=model.asset_code,
            title=model.title,
            frequency_days=(
                model.frequency_days
            ),
            responsible_person_code=(
                model.responsible_person_code
            ),
            next_due_at=model.next_due_at,
            description=model.description,
            is_active=model.is_active,
        )