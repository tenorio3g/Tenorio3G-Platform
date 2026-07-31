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
    Carga información de demostración para el dominio Assets.

    Registra modelos de activo y activos físicos relacionados.
    """

    @staticmethod
    def load(
        asset_repository: AssetRepository,
        asset_model_repository: AssetModelRepository,
    ) -> None:
        """
        Carga el catálogo inicial de demostración.
        """

        asset_model = AssetModel(
            code="TAB-480-01",
            name="Tablero general 480 V",
            model_number="NQOD",
            asset_type_code="ELECTRICAL_PANEL",
            manufacturer_code="SCHNEIDER",
            description=(
                "Modelo de tablero eléctrico general "
                "para distribución en 480 V."
            ),
            specifications={
                "voltaje": "480 V",
                "frecuencia": "60 Hz",
                "fases": "3",
            },
        )

        asset = Asset(
            code="S2-480-ES09-T269",
            name="TABLERO GENERAL ES09",
            asset_model_code=asset_model.code,
            serial_number="SN-ES09-0001",
            location_code="SUBESTACION-NORTE",
            status=AssetStatus.OPERATING,
            installation_date=date(2024, 1, 15),
        )

        asset_model_repository.save(
            asset_model,
        )

        asset_repository.save(
            asset,
        )