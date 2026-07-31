from __future__ import annotations

from app.domains.assets.entities.asset import Asset

from .asset_view_model import AssetViewModel


class AssetPresenter:
    """
    Convierte entidades Asset del dominio en modelos compatibles
    con la interfaz web.
    """

    STATUS_LABELS = {
        "OPERATING": "Operando",
        "ACTIVE": "Operando",
        "WARNING": "Advertencia",
        "FAILURE": "Falla",
        "FAILED": "Falla",
        "OUT_OF_SERVICE": "Fuera de servicio",
        "INACTIVE": "Fuera de servicio",
    }

    @classmethod
    def present(
        cls,
        asset: Asset,
    ) -> AssetViewModel:
        return AssetViewModel(
            codigo=asset.code,
            nombre=asset.name,
            estado=cls._present_status(asset),
            ubicacion=asset.location_code,
            area=None,
            ultimo_mantenimiento=None,
            proximo_mantenimiento=None,
            salud=None,
        )

    @classmethod
    def _present_status(
        cls,
        asset: Asset,
    ) -> str:
        """
        Traduce el estado interno del dominio al texto utilizado
        por la interfaz.
        """

        status_name = asset.status.name

        return cls.STATUS_LABELS.get(
            status_name,
            status_name.replace("_", " ").title(),
        )