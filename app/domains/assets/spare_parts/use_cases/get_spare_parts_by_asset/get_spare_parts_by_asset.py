from app.domains.assets.spare_parts.repositories.spare_part_repository import (
    SparePartRepository,
)

from .query import GetSparePartsByAssetQuery
from .result import GetSparePartsByAssetResult


class GetSparePartsByAsset:
    """
    Obtiene las refacciones asociadas a un activo.
    """

    def __init__(
        self,
        repository: SparePartRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: GetSparePartsByAssetQuery,
    ) -> GetSparePartsByAssetResult:

        asset_code = query.asset_code.strip()

        if not asset_code:
            return GetSparePartsByAssetResult(
                success=False,
                message="El código del activo es obligatorio.",
            )

        spare_parts = self._repository.get_by_asset_code(
            asset_code,
        )

        return GetSparePartsByAssetResult(
            success=True,
            message="Refacciones obtenidas correctamente.",
            spare_parts=spare_parts,
        )