from __future__ import annotations

from abc import ABC, abstractmethod

from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
    SparePart,
)


class SparePartRepository(ABC):
    """
    Contrato de persistencia para refacciones
    y sus relaciones con activos.
    """

    @abstractmethod
    def save_spare_part(
        self,
        spare_part: SparePart,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_spare_part_by_code(
        self,
        code: str,
    ) -> SparePart | None:
        raise NotImplementedError

    @abstractmethod
    def link_to_asset(
        self,
        relation: AssetSparePart,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[AssetSparePart]:
        raise NotImplementedError

    @abstractmethod
    def get_assets_by_spare_part_code(
        self,
        spare_part_code: str,
    ) -> list[AssetSparePart]:
        raise NotImplementedError