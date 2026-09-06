from __future__ import annotations

from app.assets.presenters.asset_life_sheet_view_model import (
    AssetLifeSheetViewModel,
)

from app.domains.assets.entities.asset import Asset
from app.domains.assets.entities.asset_model import AssetModel
from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)


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
        physical_location: PhysicalLocation | None = None,
    ) -> AssetLifeSheetViewModel:

        estado = cls.STATUS_LABELS.get(
            asset.status.name,
            asset.status.name,
        )

        ubicacion = asset.location_code
        area = None

        if physical_location is not None:
            ubicacion = physical_location.name
            area = physical_location.area

        return AssetLifeSheetViewModel(
            codigo=asset.code,
            nombre=asset.name,
            estado=estado,
            ubicacion=ubicacion,
            area=area,
            modelo=asset_model.display_name,
            salud=None,
            ultimo_mantenimiento=None,
            proximo_mantenimiento=None,
        )
