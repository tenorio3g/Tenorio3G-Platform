from sqlalchemy import select

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
)

from app.domains.assets.preventive_maintenance.models import (
    PreventiveMaintenanceExecutionModel,
)

from .preventive_maintenance_execution_repository import (
    PreventiveMaintenanceExecutionRepository,
)


class SQLitePreventiveMaintenanceExecutionRepository(
    PreventiveMaintenanceExecutionRepository,
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
        execution: PreventiveMaintenanceExecution,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                PreventiveMaintenanceExecutionModel,
                execution.code,
            )

            if model is None:

                model = (
                    PreventiveMaintenanceExecutionModel(
                        code=execution.code,
                        plan_code=execution.plan_code,
                        asset_code=execution.asset_code,
                        performed_by=execution.performed_by,
                        completed_at=execution.completed_at,
                        observations=execution.observations,
                        scheduled_at=execution.scheduled_at,
                    )
                )

                session.add(
                    model
                )

            else:

                model.plan_code = (
                    execution.plan_code
                )

                model.asset_code = (
                    execution.asset_code
                )

                model.performed_by = (
                    execution.performed_by
                )

                model.completed_at = (
                    execution.completed_at
                )

                model.observations = (
                    execution.observations
                )
                model.scheduled_at = (
                    execution.scheduled_at
                )

            session.commit()

    def get_by_code(
        self,
        code: str,
    ) -> PreventiveMaintenanceExecution | None:

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                PreventiveMaintenanceExecutionModel,
                normalized_code,
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )

    def list_by_plan(
        self,
        plan_code: str,
    ) -> list[PreventiveMaintenanceExecution]:

        normalized_plan_code = str(
            plan_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    PreventiveMaintenanceExecutionModel
                )
                .where(
                    PreventiveMaintenanceExecutionModel.plan_code
                    == normalized_plan_code
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

    def list_by_asset(
        self,
        asset_code: str,
    ) -> list[PreventiveMaintenanceExecution]:

        normalized_asset_code = str(
            asset_code
        ).strip().upper()

        with self._session_factory() as session:

            statement = (
                select(
                    PreventiveMaintenanceExecutionModel
                )
                .where(
                    PreventiveMaintenanceExecutionModel.asset_code
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

    @staticmethod
    def _to_entity(
        model: PreventiveMaintenanceExecutionModel,
    ) -> PreventiveMaintenanceExecution:

        return PreventiveMaintenanceExecution(
            code=model.code,
            plan_code=model.plan_code,
            asset_code=model.asset_code,
            performed_by=model.performed_by,
            completed_at=model.completed_at,
            observations=model.observations,
            scheduled_at=model.scheduled_at,
        )