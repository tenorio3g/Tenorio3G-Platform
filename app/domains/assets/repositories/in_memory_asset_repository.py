from __future__ import annotations

from app.domains.assets.entities.asset import Asset

from .asset_repository import AssetRepository


class InMemoryAssetRepository(AssetRepository):
    """
    Implementación en memoria del repositorio de activos.

    Se utiliza para pruebas y desarrollo sin depender de una
    base de datos.
    """

    def __init__(self) -> None:
        self._assets: dict[str, Asset] = {}

    def save(
        self,
        asset: Asset,
    ) -> None:
        self._assets[asset.code] = asset

    def find_by_code(
        self,
        code: str,
    ) -> Asset | None:
        return self._assets.get(code)

    def find_all(
        self,
    ) -> list[Asset]:
        return list(self._assets.values())

    def update(
        self,
        asset: Asset,
    ) -> None:
        self._assets[asset.code] = asset