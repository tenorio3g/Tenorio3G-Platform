from __future__ import annotations

from sqlalchemy import select

from app.domains.assets.entities.asset import Asset
from app.domains.assets.models import AssetRecordModel
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)

from .asset_repository import AssetRepository


class SQLiteAssetRepository(AssetRepository):

    def __init__(
        self,
        session_factory,
    ) -> None:
        self._session_factory = session_factory

    def save(
        self,
        asset: Asset,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                AssetRecordModel,
                asset.code,
            )

            if model is None:
                model = AssetRecordModel(
                    code=asset.code,
                    name=asset.name,
                    asset_model_code=asset.asset_model_code,
                    serial_number=asset.serial_number,
                    location_code=asset.location_code,
                    status=asset.status.value,
                    installation_date=asset.installation_date,
                    deactivation_reason=asset.deactivation_reason,
                )

                session.add(model)

            else:
                self._copy_to_model(
                    asset=asset,
                    model=model,
                )

            session.commit()

    def find_by_code(
        self,
        code: str,
    ) -> Asset | None:

        normalized_code = str(
            code
        ).strip()

        with self._session_factory() as session:

            model = session.get(
                AssetRecordModel,
                normalized_code,
            )

            if model is None:
                return None

            return self._to_entity(model)

    def find_all(
        self,
    ) -> list[Asset]:

        with self._session_factory() as session:

            statement = select(
                AssetRecordModel
            ).order_by(
                AssetRecordModel.code
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
        asset: Asset,
    ) -> None:

        with self._session_factory() as session:

            model = session.get(
                AssetRecordModel,
                asset.code,
            )

            if model is None:
                return

            self._copy_to_model(
                asset=asset,
                model=model,
            )

            session.commit()

    @staticmethod
    def _copy_to_model(
        asset: Asset,
        model: AssetRecordModel,
    ) -> None:

        model.name = asset.name
        model.asset_model_code = asset.asset_model_code
        model.serial_number = asset.serial_number
        model.location_code = asset.location_code
        model.status = asset.status.value
        model.installation_date = asset.installation_date
        model.deactivation_reason = (
            asset.deactivation_reason
        )

    @staticmethod
    def _to_entity(
        model: AssetRecordModel,
    ) -> Asset:

        return Asset(
            code=model.code,
            name=model.name,
            asset_model_code=model.asset_model_code,
            serial_number=model.serial_number,
            location_code=model.location_code,
            status=AssetStatus(model.status),
            installation_date=model.installation_date,
            deactivation_reason=model.deactivation_reason,
        )
