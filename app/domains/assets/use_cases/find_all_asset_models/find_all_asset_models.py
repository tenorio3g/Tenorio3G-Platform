"""
T3G-ASSET-UC-003

FindAllAssetModels

Caso de uso responsable de obtener todos
los modelos de activos registrados.
"""

from app.domains.assets.repositories.asset_model_repository import (
    AssetModelRepository,
)

from .command import FindAllAssetModelsCommand
from .result import FindAllAssetModelsResult


class FindAllAssetModels:
    """
    Caso de uso para obtener todos los modelos
    de activos registrados.
    """

    def __init__(self, repository: AssetModelRepository) -> None:
        self._repository = repository

    def execute(
        self,
        command: FindAllAssetModelsCommand,
    ) -> FindAllAssetModelsResult:
        """
        Ejecuta la búsqueda de todos los modelos.
        """

        asset_models = self._repository.find_all()

        return FindAllAssetModelsResult(
            success=True,
            message="Modelos obtenidos correctamente.",
            asset_models=asset_models,
        )