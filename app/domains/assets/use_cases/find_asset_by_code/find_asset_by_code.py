from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)

from .query import FindAssetByCodeQuery
from .result import FindAssetByCodeResult


class FindAssetByCode:
    """
    Caso de uso para obtener un activo por su código.
    """

    def __init__(
        self,
        repository: AssetRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: FindAssetByCodeQuery,
    ) -> FindAssetByCodeResult:

        asset = self._repository.find_by_code(
            query.code
        )

        if asset is None:
            return FindAssetByCodeResult(
                success=False,
                message="No existe un activo con ese código.",
            )

        return FindAssetByCodeResult(
            success=True,
            message="Activo encontrado.",
            asset=asset,
        )