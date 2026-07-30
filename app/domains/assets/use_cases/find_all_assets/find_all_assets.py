from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)

from .query import FindAllAssetsQuery
from .result import FindAllAssetsResult


class FindAllAssets:
    """
    Caso de uso para obtener todos los activos registrados.
    """

    def __init__(
        self,
        repository: AssetRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: FindAllAssetsQuery,
    ) -> FindAllAssetsResult:
        assets = self._repository.find_all()

        return FindAllAssetsResult(
            success=True,
            message=self._build_message(len(assets)),
            assets=assets,
        )

    @staticmethod
    def _build_message(total_assets: int) -> str:
        if total_assets == 0:
            return "No hay activos registrados."

        if total_assets == 1:
            return "Se encontró 1 activo."

        return f"Se encontraron {total_assets} activos."