from __future__ import annotations

from app.assets.presenters.asset_life_sheet_view_model import (
    AssetLifeSheetViewModel,
)


class AssetApiPresenter:
    """
    Convierte la Hoja de Vida en una respuesta serializable
    para clientes HTTP.
    """

    @staticmethod
    def present(
        asset: AssetLifeSheetViewModel,
    ) -> dict[str, object]:
        return {
            "codigo": asset.codigo,
            "nombre": asset.nombre,
            "estado": asset.estado,
            "ubicacion": asset.ubicacion,
            "area": asset.area,
            "modelo": asset.modelo,
            "salud": asset.salud,
            "ultimo_mantenimiento": asset.ultimo_mantenimiento,
            "proximo_mantenimiento": asset.proximo_mantenimiento,
        }