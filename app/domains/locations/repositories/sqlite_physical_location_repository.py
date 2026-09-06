from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)
from app.domains.locations.models.physical_location_model import (
    PhysicalLocationModel,
)

from .physical_location_repository import (
    PhysicalLocationRepository,
)


class SQLitePhysicalLocationRepository(
    PhysicalLocationRepository,
):

    def __init__(
        self,
        session_factory: sessionmaker,
    ) -> None:
        self._session_factory = session_factory

    def save(
        self,
        location: PhysicalLocation,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                PhysicalLocationModel,
                location.code,
            )

            if model is None:
                model = PhysicalLocationModel(
                    code=location.code,
                    name=location.name,
                    area=location.area,
                    is_active=location.is_active,
                )

                session.add(model)

            else:
                self._copy_to_model(
                    location,
                    model,
                )

            session.commit()

    def find_by_code(
        self,
        code: str,
    ) -> PhysicalLocation | None:

        clean_code = code.strip()

        with self._session_factory() as session:

            model = session.get(
                PhysicalLocationModel,
                clean_code,
            )

            if model is None:
                return None

            return self._to_entity(
                model
            )

    def find_all(
        self,
    ) -> list[PhysicalLocation]:

        with self._session_factory() as session:

            statement = (
                select(
                    PhysicalLocationModel
                )
                .order_by(
                    PhysicalLocationModel.code
                )
            )

            models = session.scalars(
                statement
            ).all()

            return [
                self._to_entity(model)
                for model in models
            ]

    def update(
        self,
        location: PhysicalLocation,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                PhysicalLocationModel,
                location.code,
            )

            if model is None:
                raise KeyError(
                    location.code
                )

            self._copy_to_model(
                location,
                model,
            )

            session.commit()

    @staticmethod
    def _copy_to_model(
        location: PhysicalLocation,
        model: PhysicalLocationModel,
    ) -> None:

        model.name = location.name
        model.area = location.area
        model.is_active = location.is_active

    @staticmethod
    def _to_entity(
        model: PhysicalLocationModel,
    ) -> PhysicalLocation:

        return PhysicalLocation(
            code=model.code,
            name=model.name,
            area=model.area,
            is_active=model.is_active,
        )
