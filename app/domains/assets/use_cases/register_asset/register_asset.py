from __future__ import annotations

from app.domains.assets.entities.asset import Asset
from app.domains.assets.repositories.asset_model_repository import (
    AssetModelRepository,
)
from app.domains.assets.repositories.asset_repository import (
    AssetRepository,
)
from app.domains.locations.repositories.physical_location_repository import (
    PhysicalLocationRepository,
)

from .command import RegisterAssetCommand
from .result import RegisterAssetResult


class RegisterAsset:
    """
    Caso de uso para registrar un activo fisico.

    Valida:
    - que el codigo del activo no exista;
    - que el modelo asociado exista;
    - que la ubicacion fisica asociada exista.
    """

    def __init__(
        self,
        asset_repository: AssetRepository,
        asset_model_repository: AssetModelRepository,
        location_repository: PhysicalLocationRepository,
    ) -> None:
        self._asset_repository = asset_repository
        self._asset_model_repository = asset_model_repository
        self._location_repository = location_repository

    def execute(
        self,
        command: RegisterAssetCommand,
    ) -> RegisterAssetResult:

        existing_asset = self._asset_repository.find_by_code(
            command.code
        )

        if existing_asset is not None:
            return RegisterAssetResult(
                success=False,
                message=(
                    "Ya existe un activo con ese código."
                ),
            )

        asset_model = self._asset_model_repository.find_by_code(
            command.asset_model_code
        )

        if asset_model is None:
            return RegisterAssetResult(
                success=False,
                message=(
                    "No existe el modelo de activo indicado."
                ),
            )

        physical_location = (
            self._location_repository.find_by_code(
                command.location_code
            )
        )

        if physical_location is None:
            return RegisterAssetResult(
                success=False,
                message=(
                    "No existe la ubicación física indicada."
                ),
            )

        asset = Asset(
            code=command.code.strip(),
            name=command.name.strip(),
            asset_model_code=(
                command.asset_model_code.strip()
            ),
            serial_number=(
                command.serial_number.strip()
            ),
            location_code=(
                physical_location.code
            ),
            status=command.status,
            installation_date=(
                command.installation_date
            ),
        )

        self._asset_repository.save(
            asset
        )

        return RegisterAssetResult(
            success=True,
            message=(
                "Activo registrado correctamente."
            ),
            asset=asset,
        )
