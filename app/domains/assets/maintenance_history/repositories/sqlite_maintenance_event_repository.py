from sqlalchemy import select

from app.foundation.database import SessionLocal

from app.domains.assets.maintenance_history.entities import (
    MaintenanceEvent,
)

from app.domains.assets.maintenance_history.models import (
    MaintenanceEventModel,
)

from .maintenance_event_repository import (
    MaintenanceEventRepository,
)


class SQLiteMaintenanceEventRepository(
    MaintenanceEventRepository
):

    def __init__(
        self,
        session_factory=SessionLocal,
    ) -> None:
        self._session_factory = session_factory

    def save(
        self,
        event: MaintenanceEvent,
    ) -> MaintenanceEvent:

        with self._session_factory() as session:

            model = session.scalar(
                select(
                    MaintenanceEventModel
                ).where(
                    MaintenanceEventModel.code
                    == event.code
                )
            )

            if model is None:

                model = MaintenanceEventModel(
                    code=event.code,
                    asset_code=event.asset_code,
                    event_type=event.event_type,
                    title=event.title,
                    description=event.description,
                    performed_by=event.performed_by,
                    started_at=event.started_at,
                    completed_at=event.completed_at,
                    observations=event.observations,
                )

                session.add(model)

            else:

                model.asset_code = event.asset_code
                model.event_type = event.event_type
                model.title = event.title
                model.description = event.description
                model.performed_by = event.performed_by
                model.started_at = event.started_at
                model.completed_at = event.completed_at
                model.observations = event.observations

            session.commit()

        return event

    def get_by_code(
        self,
        code: str,
    ) -> MaintenanceEvent | None:

        with self._session_factory() as session:

            model = session.scalar(
                select(
                    MaintenanceEventModel
                ).where(
                    MaintenanceEventModel.code
                    == code
                )
            )

            if model is None:
                return None

            return self._to_entity(model)

    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[MaintenanceEvent]:

        with self._session_factory() as session:

            models = list(
                session.scalars(
                    select(
                        MaintenanceEventModel
                    ).where(
                        MaintenanceEventModel.asset_code
                        == asset_code
                    )
                ).all()
            )

            return [
                self._to_entity(model)
                for model in models
            ]

    def delete(
        self,
        code: str,
    ) -> bool:

        with self._session_factory() as session:

            model = session.scalar(
                select(
                    MaintenanceEventModel
                ).where(
                    MaintenanceEventModel.code
                    == code
                )
            )

            if model is None:
                return False

            session.delete(model)
            session.commit()

            return True

    @staticmethod
    def _to_entity(
        model: MaintenanceEventModel,
    ) -> MaintenanceEvent:

        return MaintenanceEvent(
            code=model.code,
            asset_code=model.asset_code,
            event_type=model.event_type,
            title=model.title,
            description=model.description,
            performed_by=model.performed_by,
            started_at=model.started_at,
            completed_at=model.completed_at,
            observations=model.observations,
        )