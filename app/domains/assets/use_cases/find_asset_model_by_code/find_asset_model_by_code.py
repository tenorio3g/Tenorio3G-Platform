"""
T3G-ASSET-UC-002

FindAssetModelByCode

Caso de uso responsable de buscar un modelo
de activo mediante su código.
"""

from app.domains.assets.repositories.asset_model_repository import (
    AssetModelRepository,
)

from .command import FindAssetModelByCodeCommand
from .result import FindAssetModelByCodeResult


class FindAssetModelByCode:
    """
    Caso de uso para buscar un modelo de activo por código.
    """

    def __init__(self, repository: AssetModelRepository) -> None:
        self._repository = repository

    def execute(
        self,
        command: FindAssetModelByCodeCommand,
    ) -> FindAssetModelByCodeResult:
        """
        Ejecuta la búsqueda de un modelo de activo.
        """

        asset_model = self._repository.find_by_code(command.code)

        if asset_model is None:
            return FindAssetModelByCodeResult(
                success=False,
                message=(
                    f"No se encontró un modelo con el código "
                    f"'{command.code}'."
                ),
            )

        return FindAssetModelByCodeResult(
            success=True,
            message="Modelo encontrado correctamente.",
            asset_model=asset_model,
        )