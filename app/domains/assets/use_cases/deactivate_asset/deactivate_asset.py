from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)

from .command import DeactivateAssetCommand
from .result import DeactivateAssetResult


class DeactivateAsset:
    """
    Caso de uso para desactivar un activo.
    """

    def __init__(
        self,
        repository: AssetRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: DeactivateAssetCommand,
    ) -> DeactivateAssetResult:

        asset = self._repository.find_by_code(
            command.code
        )

        if asset is None:
            return DeactivateAssetResult(
                success=False,
                message="No existe un activo con ese código.",
            )

        if asset.is_out_of_service():
            return DeactivateAssetResult(
                success=False,
                message="El activo ya se encuentra desactivado.",
                asset=asset,
            )

        try:
            asset.deactivate(command.reason)

        except ValueError as error:

            return DeactivateAssetResult(
                success=False,
                message=str(error),
                asset=asset,
            )

        self._repository.update(asset)

        return DeactivateAssetResult(
            success=True,
            message="Activo desactivado correctamente.",
            asset=asset,
        )