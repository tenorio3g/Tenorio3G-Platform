"""
T3G-ASSET-UC-XXX

GetAssetLifeSheet

Caso de uso encargado de obtener toda la información
necesaria para mostrar la Hoja de Vida de un activo.
"""

from app.domains.assets.use_cases.find_asset_by_code.find_asset_by_code import (
    FindAssetByCode,
)
from app.domains.assets.use_cases.find_asset_by_code.query import (
    FindAssetByCodeQuery,
)

from app.domains.assets.use_cases.find_asset_model_by_code.find_asset_model_by_code import (
    FindAssetModelByCode,
)
from app.domains.assets.use_cases.find_asset_model_by_code.command import (
    FindAssetModelByCodeCommand,
)

from .query import GetAssetLifeSheetQuery
from .result import GetAssetLifeSheetResult


class GetAssetLifeSheet:
    """
    Caso de uso para obtener la Hoja de Vida
    de un activo.
    """

    def __init__(
        self,
        find_asset_by_code: FindAssetByCode,
        find_asset_model_by_code: FindAssetModelByCode,
    ) -> None:

        self._find_asset_by_code = find_asset_by_code
        self._find_asset_model_by_code = (
            find_asset_model_by_code
        )

    def execute(
        self,
        query: GetAssetLifeSheetQuery,
    ) -> GetAssetLifeSheetResult:
        """
        Obtiene toda la información necesaria
        para mostrar la Hoja de Vida de un activo.
        """

        asset_result = self._find_asset_by_code.execute(
            FindAssetByCodeQuery(
                code=query.code,
            )
        )

        if not asset_result.success:
            return GetAssetLifeSheetResult(
                success=False,
                message=asset_result.message,
            )

        asset_model_result = (
            self._find_asset_model_by_code.execute(
                FindAssetModelByCodeCommand(
                    code=asset_result.asset.asset_model_code,
                )
            )
        )

        if not asset_model_result.success:
            return GetAssetLifeSheetResult(
                success=False,
                message=asset_model_result.message,
                asset=asset_result.asset,
            )

        return GetAssetLifeSheetResult(
            success=True,
            message="Hoja de vida obtenida correctamente.",
            asset=asset_result.asset,
            asset_model=asset_model_result.asset_model,
        )