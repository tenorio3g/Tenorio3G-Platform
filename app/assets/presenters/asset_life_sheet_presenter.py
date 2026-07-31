from __future__ import annotations

from app.assets.presenters.asset_life_sheet_view_model import (
    AssetLifeSheetViewModel,
)

from app.domains.assets.entities.asset import Asset
from app.domains.assets.entities.asset_model import AssetModel


class AssetLifeSheetPresenter:
    """
    Convierte entidades del dominio en un ViewModel
    para la Hoja de Vida.
    """

    STATUS_LABELS = {
        "OPERATING": "Operando",
        "OUT_OF_SERVICE": "Fuera de servicio",
    }

    @classmethod
    def present(
        cls,
        asset: Asset,
        asset_model: AssetModel,
    ) -> AssetLifeSheetViewModel:

        estado = cls.STATUS_LABELS.get(
            asset.status.name,
            asset.status.name,
        )

        return AssetLifeSheetViewModel(
            codigo=asset.code,
            nombre=asset.name,
            estado=estado,
            ubicacion=asset.location_code,

            # Temporal
            area="Sin área registrada",

            modelo=asset_model.display_name,

            # Temporal
            salud=100,

            ultimo_mantenimiento=None,
            proximo_mantenimiento=None,
        )