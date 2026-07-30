"""
T3G-ASSET-UC-001

RegisterAssetModel

Caso de uso responsable de registrar un nuevo modelo
de activo dentro del catálogo.
"""

from __future__ import annotations

from app.domains.assets.entities.asset_model import AssetModel
from app.domains.assets.repositories.asset_model_repository import (
    AssetModelRepository,
)

from .command import RegisterAssetModelCommand
from .result import RegisterAssetModelResult


class RegisterAssetModel:
    """
    Caso de uso para registrar un nuevo modelo.
    """

    def __init__(self, repository: AssetModelRepository) -> None:
        self._repository = repository

    def execute(
        self,
        command: RegisterAssetModelCommand,
    ) -> RegisterAssetModelResult:
        """
        Ejecuta el registro de un nuevo modelo.
        """

        if self._repository.exists_by_code(command.code):
            return RegisterAssetModelResult(
                success=False,
                message=f"Ya existe un modelo con el código '{command.code}'."
            )

        asset_model = AssetModel(
            code=command.code,
            name=command.name,
            model_number=command.model_number,
            manufacturer_code=command.manufacturer_code,
            asset_type_code=command.asset_type_code,
            description=command.description,
            specifications=command.specifications,
        )

        self._repository.save(asset_model)

        return RegisterAssetModelResult(
            success=True,
            message="Modelo registrado correctamente.",
            asset_model=asset_model,
        )