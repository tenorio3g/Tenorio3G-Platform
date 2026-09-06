from __future__ import annotations

from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.entities.asset_model import AssetModel

from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)
from app.domains.assets.repositories.asset_model_repository import (
    AssetModelRepository,
)

from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)


class DemoAssetSeeder:
    """
    Carga informaci?n inicial de demostraci?n para Assets.

    El seeder es idempotente:
    solamente crea registros que todav?a no existen y nunca
    sobrescribe informaci?n persistida previamente.
    """

    @staticmethod
    def load(
        asset_repository: AssetRepository,
        asset_model_repository: AssetModelRepository,
    ) -> None:

        asset_model_code = "TAB-480-01"
        asset_code = "S2-480-ES09-T269"

        if not asset_model_repository.exists_by_code(
            asset_model_code
        ):
            asset_model = AssetModel(
                code=asset_model_code,
                name="Tablero general 480 V",
                model_number="NQOD",
                asset_type_code="ELECTRICAL_PANEL",
                manufacturer_code="SCHNEIDER",
                description=(
                    "Modelo de tablero el?ctrico general "
                    "para distribuci?n en 480 V."
                ),
                specifications={
                    "voltaje": "480 V",
                    "frecuencia": "60 Hz",
                    "fases": "3",
                },
            )

            asset_model_repository.save(
                asset_model
            )

        if asset_repository.find_by_code(
            asset_code
        ) is None:
            asset = Asset(
                code=asset_code,
                name="TABLERO GENERAL ES09",
                asset_model_code=asset_model_code,
                serial_number="SN-ES09-0001",
                location_code="SUBESTACION-NORTE",
                status=AssetStatus.OPERATING,
                installation_date=date(
                    2024,
                    1,
                    15,
                ),
            )

            asset_repository.save(
                asset
            )
