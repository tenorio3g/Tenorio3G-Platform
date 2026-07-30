from app.domains.assets.repositories.asset_model_repository import (
    AssetModelRepository,
)

from .command import UpdateAssetModelCommand
from .result import UpdateAssetModelResult


class UpdateAssetModel:
    """
    Caso de uso para actualizar la información editable
    de un modelo de activo existente.
    """

    def __init__(
        self,
        repository: AssetModelRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: UpdateAssetModelCommand,
    ) -> UpdateAssetModelResult:
        asset_model = self._repository.find_by_code(
            command.code
        )

        if asset_model is None:
            return UpdateAssetModelResult(
                success=False,
                message="No existe un modelo con ese código.",
            )

        asset_model.rename(
            command.name
        )

        asset_model.change_description(
            command.description
        )

        asset_model.replace_specifications(
            command.specifications
        )

        self._repository.update(
            asset_model
        )

        return UpdateAssetModelResult(
            success=True,
            message="Modelo actualizado correctamente.",
            asset_model=asset_model,
        )