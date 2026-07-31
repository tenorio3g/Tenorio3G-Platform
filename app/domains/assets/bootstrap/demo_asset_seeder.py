from __future__ import annotations

from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)


class DemoAssetSeeder:
    """
    Carga información de demostración en el repositorio.

    Se utiliza únicamente durante el desarrollo mientras no exista
    una base de datos real.
    """

    @staticmethod
    def load(
        repository: AssetRepository,
    ) -> None:
        """
        Carga los activos iniciales.
        """

        repository.save(

            Asset(

                code="S2-480-ES09-T269",

                name="TABLERO GENERAL ES09",

                asset_model_code="TAB-480-01",

                serial_number="SN-ES09-0001",

                location_code="SUBESTACION-NORTE",

                status=AssetStatus.OPERATING,

                installation_date=date(2024, 1, 15),

            )

        )