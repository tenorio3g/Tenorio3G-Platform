from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)

from .command import ActivateAssetCommand
from .result import ActivateAssetResult


class ActivateAsset:
    """
    Caso de uso para activar un activo.
    """

    def __init__(
        self,
        repository: AssetRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: ActivateAssetCommand,
    ) -> ActivateAssetResult:

        asset = self._repository.find_by_code(
            command.code
        )

        if asset is None:
            return ActivateAssetResult(
                success=False,
                message="No existe un activo con ese código.",
            )

        if asset.is_operating():
            return ActivateAssetResult(
                success=False,
                message="El activo ya se encuentra activo.",
                asset=asset,
            )

        asset.activate()
        self._repository.update(asset)

        return ActivateAssetResult(
            success=True,
            message="Activo activado correctamente.",
            asset=asset,
        )