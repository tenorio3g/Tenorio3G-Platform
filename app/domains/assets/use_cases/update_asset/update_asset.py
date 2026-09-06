from app.domains.assets.repositories.asset_model_repository import (
    AssetModelRepository,
)
from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)
from app.domains.locations.repositories.physical_location_repository import (
    PhysicalLocationRepository,
)

from .command import UpdateAssetCommand
from .result import UpdateAssetResult


class UpdateAsset:

    def __init__(
        self,
        repository: AssetRepository,
        asset_model_repository: AssetModelRepository,
        location_repository: PhysicalLocationRepository,
    ) -> None:
        self._repository = repository
        self._asset_model_repository = asset_model_repository
        self._location_repository = location_repository

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

        if command.asset_model_code is not None:
            if not self._asset_model_repository.exists_by_code(
                command.asset_model_code
            ):
                return UpdateAssetResult(
                    success=False,
                    message="No existe el modelo de activo indicado.",
                    asset=asset,
                )

        if command.location_code is not None:
            location = self._location_repository.find_by_code(
                command.location_code
            )

            if location is None:
                return UpdateAssetResult(
                    success=False,
                    message="No existe la ubicación física indicada.",
                    asset=asset,
                )

        if command.name is not None:
            asset.rename(command.name)

        if command.asset_model_code is not None:
            asset.change_asset_model(
                command.asset_model_code
            )

        if command.serial_number is not None:
            asset.change_serial_number(
                command.serial_number
            )

        if command.location_code is not None:
            asset.change_location(
                command.location_code
            )

        if command.installation_date is not None:
            asset.change_installation_date(
                command.installation_date
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
