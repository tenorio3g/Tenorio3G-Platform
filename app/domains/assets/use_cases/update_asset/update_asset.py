from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)

from .command import UpdateAssetCommand
from .result import UpdateAssetResult


class UpdateAsset:
    """
    Caso de uso para actualizar la información modificable de un activo.
    """

    def __init__(
        self,
        repository: AssetRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: UpdateAssetCommand,
    ) -> UpdateAssetResult:

        asset = self._repository.find_by_code(
            command.code
        )

        if asset is None:
            return UpdateAssetResult(
                success=False,
                message="No existe un activo con ese código.",
            )

        if command.name is not None:
            asset.rename(command.name)

        if command.serial_number is not None:
            asset.change_serial_number(
                command.serial_number
            )

        if command.location_code is not None:
            asset.change_location(
                command.location_code
            )

        if command.status is not None:
            asset.change_status(
                command.status
            )

        self._repository.update(asset)

        return UpdateAssetResult(
            success=True,
            message="Activo actualizado correctamente.",
            asset=asset,
        )