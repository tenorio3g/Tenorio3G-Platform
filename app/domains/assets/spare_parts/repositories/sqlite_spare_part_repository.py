from __future__ import annotations

from sqlalchemy import select

from app.foundation.database import SessionLocal

from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
    SparePart,
)

from app.domains.assets.spare_parts.models import (
    AssetSparePartModel,
    SparePartModel,
)

from app.domains.assets.spare_parts.repositories.spare_part_repository import (
    SparePartRepository,
)


class SQLiteSparePartRepository(
    SparePartRepository,
):
    """
    Implementación SQLite del repositorio de refacciones.
    """

    def __init__(
        self,
        session_factory=SessionLocal,
    ) -> None:
        self._session_factory = session_factory

    def save_spare_part(
        self,
        spare_part: SparePart,
    ) -> None:

        clean_code = spare_part.code.strip()

        with self._session_factory() as session:

            model = session.scalar(
                select(SparePartModel).where(
                    SparePartModel.code == clean_code
                )
            )

            if model is None:
                model = SparePartModel(
                    code=clean_code,
                    name=spare_part.name,
                    manufacturer=spare_part.manufacturer,
                    part_number=spare_part.part_number,
                    unit=spare_part.unit,
                    description=spare_part.description,
                )

                session.add(model)

            else:
                model.name = spare_part.name
                model.manufacturer = spare_part.manufacturer
                model.part_number = spare_part.part_number
                model.unit = spare_part.unit
                model.description = spare_part.description

            session.commit()

    def get_spare_part_by_code(
        self,
        code: str,
    ) -> SparePart | None:

        clean_code = code.strip()

        if not clean_code:
            return None

        with self._session_factory() as session:

            model = session.scalar(
                select(SparePartModel).where(
                    SparePartModel.code == clean_code
                )
            )

            if model is None:
                return None

            return self._spare_part_to_entity(model)

    def link_to_asset(
        self,
        relation: AssetSparePart,
    ) -> None:

        # Aseguramos primero que la refacción exista.
        self.save_spare_part(
            relation.spare_part
        )

        with self._session_factory() as session:

            model = session.scalar(
                select(AssetSparePartModel).where(
                    AssetSparePartModel.asset_code
                    == relation.asset_code,
                    AssetSparePartModel.spare_part_code
                    == relation.spare_part_code,
                )
            )

            if model is None:

                model = AssetSparePartModel(
                    asset_code=relation.asset_code,
                    spare_part_code=relation.spare_part_code,
                    quantity=relation.quantity,
                    position=relation.position,
                    observations=relation.observations,
                    is_critical=relation.is_critical,
                )

                session.add(model)

            else:

                model.quantity = relation.quantity
                model.position = relation.position
                model.observations = relation.observations
                model.is_critical = relation.is_critical

            session.commit()

    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[AssetSparePart]:

        clean_code = asset_code.strip()

        if not clean_code:
            return []

        with self._session_factory() as session:

            relation_models = list(
                session.scalars(
                    select(AssetSparePartModel).where(
                        AssetSparePartModel.asset_code
                        == clean_code
                    )
                ).all()
            )

            results: list[AssetSparePart] = []

            for relation_model in relation_models:

                spare_part_model = session.scalar(
                    select(SparePartModel).where(
                        SparePartModel.code
                        == relation_model.spare_part_code
                    )
                )

                if spare_part_model is None:
                    continue

                results.append(
                    self._relation_to_entity(
                        relation_model,
                        spare_part_model,
                    )
                )

            return results

    def get_assets_by_spare_part_code(
        self,
        spare_part_code: str,
    ) -> list[AssetSparePart]:

        clean_code = spare_part_code.strip()

        if not clean_code:
            return []

        with self._session_factory() as session:

            spare_part_model = session.scalar(
                select(SparePartModel).where(
                    SparePartModel.code == clean_code
                )
            )

            if spare_part_model is None:
                return []

            relation_models = list(
                session.scalars(
                    select(AssetSparePartModel).where(
                        AssetSparePartModel.spare_part_code
                        == clean_code
                    )
                ).all()
            )

            return [
                self._relation_to_entity(
                    relation_model,
                    spare_part_model,
                )
                for relation_model in relation_models
            ]

    @staticmethod
    def _spare_part_to_entity(
        model: SparePartModel,
    ) -> SparePart:

        return SparePart(
            code=model.code,
            name=model.name,
            manufacturer=model.manufacturer,
            part_number=model.part_number,
            unit=model.unit,
            description=model.description,
        )

    @classmethod
    def _relation_to_entity(
        cls,
        relation_model: AssetSparePartModel,
        spare_part_model: SparePartModel,
    ) -> AssetSparePart:

        spare_part = cls._spare_part_to_entity(
            spare_part_model
        )

        return AssetSparePart(
            asset_code=relation_model.asset_code,
            spare_part=spare_part,
            quantity=relation_model.quantity,
            position=relation_model.position,
            observations=relation_model.observations,
            is_critical=relation_model.is_critical,
        )