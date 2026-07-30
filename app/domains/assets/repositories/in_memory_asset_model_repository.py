"""
T3G-ASSET-REP-002

InMemoryAssetModelRepository

Implementación en memoria del contrato AssetModelRepository.

Se utiliza únicamente para pruebas y desarrollo.
"""

from __future__ import annotations

from app.domains.assets.repositories.asset_model_repository import (
    AssetModelRepository,
)

from app.domains.assets.entities.asset_model import AssetModel


class InMemoryAssetModelRepository(AssetModelRepository):

    def __init__(self) -> None:
        self._models: dict[str, AssetModel] = {}

    def save(self, asset_model: AssetModel) -> None:
        self._models[asset_model.code] = asset_model

    def exists_by_code(self, code: str) -> bool:
        return code in self._models

    def find_by_code(self, code: str) -> AssetModel | None:
        return self._models.get(code)

    def find_all(self) -> list[AssetModel]:
        return list(self._models.values())

    def update(self, asset_model: AssetModel) -> None:
        self._models[asset_model.code] = asset_model

    def delete_by_code(self, code: str) -> None:
        self._models.pop(code, None)