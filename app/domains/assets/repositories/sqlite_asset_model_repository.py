from __future__ import annotations

from sqlalchemy import select

from app.domains.assets.entities.asset_model import (
    AssetModel,
)
from app.domains.assets.models import (
    AssetModelRecord,
)

from .asset_model_repository import (
    AssetModelRepository,
)


class SQLiteAssetModelRepository(
    AssetModelRepository,
):

    def __init__(
        self,
        session_factory,
    ) -> None:
        self._session_factory = session_factory

    def save(
        self,
        asset_model: AssetModel,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                AssetModelRecord,
                asset_model.code,
            )

            if model is None:
                model = AssetModelRecord(
                    code=asset_model.code,
                    name=asset_model.name,
                    model_number=asset_model.model_number,
                    asset_type_code=asset_model.asset_type_code,
                    manufacturer_code=asset_model.manufacturer_code,
                    description=asset_model.description,
                    aliases=list(asset_model.aliases),
                    specifications=dict(
                        asset_model.specifications
                    ),
                    is_active=asset_model.is_active,
                    is_obsolete=asset_model.is_obsolete,
                )

                session.add(model)

            else:
                self._copy_to_model(
                    asset_model=asset_model,
                    model=model,
                )

            session.commit()

    def exists_by_code(
        self,
        code: str,
    ) -> bool:

        return self.find_by_code(
            code
        ) is not None

    def find_by_code(
        self,
        code: str,
    ) -> AssetModel | None:

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                AssetModelRecord,
                normalized_code,
            )

            if model is None:
                return None

            return self._to_entity(model)

    def find_all(
        self,
    ) -> list[AssetModel]:

        with self._session_factory() as session:

            statement = select(
                AssetModelRecord
            ).order_by(
                AssetModelRecord.code
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

    def update(
        self,
        asset_model: AssetModel,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                AssetModelRecord,
                asset_model.code,
            )

            if model is None:
                return

            self._copy_to_model(
                asset_model=asset_model,
                model=model,
            )

            session.commit()

    def delete_by_code(
        self,
        code: str,
    ) -> None:

        normalized_code = str(
            code
        ).strip().upper()

        with self._session_factory() as session:

            model = session.get(
                AssetModelRecord,
                normalized_code,
            )

            if model is None:
                return

            session.delete(model)
            session.commit()

    @staticmethod
    def _copy_to_model(
        asset_model: AssetModel,
        model: AssetModelRecord,
    ) -> None:

        model.name = asset_model.name
        model.model_number = asset_model.model_number
        model.asset_type_code = (
            asset_model.asset_type_code
        )
        model.manufacturer_code = (
            asset_model.manufacturer_code
        )
        model.description = asset_model.description
        model.aliases = list(
            asset_model.aliases
        )
        model.specifications = dict(
            asset_model.specifications
        )
        model.is_active = asset_model.is_active
        model.is_obsolete = asset_model.is_obsolete

    @staticmethod
    def _to_entity(
        model: AssetModelRecord,
    ) -> AssetModel:

        return AssetModel(
            code=model.code,
            name=model.name,
            model_number=model.model_number,
            asset_type_code=model.asset_type_code,
            manufacturer_code=model.manufacturer_code,
            description=model.description,
            aliases=tuple(
                model.aliases or []
            ),
            specifications=dict(
                model.specifications or {}
            ),
            is_active=model.is_active,
            is_obsolete=model.is_obsolete,
        )
