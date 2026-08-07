from __future__ import annotations

from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
    SparePart,
)
from app.domains.assets.spare_parts.repositories.spare_part_repository import (
    SparePartRepository,
)


class InMemorySparePartRepository(
    SparePartRepository,
):
    """
    Implementación en memoria del repositorio de refacciones.

    Se utiliza para pruebas del dominio sin depender de SQLite.
    """

    def __init__(self) -> None:
        self._spare_parts: dict[str, SparePart] = {}
        self._relations: list[AssetSparePart] = []

    def save_spare_part(
        self,
        spare_part: SparePart,
    ) -> None:
        clean_code = spare_part.code.strip()

        self._spare_parts[clean_code] = spare_part

    def get_spare_part_by_code(
        self,
        code: str,
    ) -> SparePart | None:
        clean_code = code.strip()

        return self._spare_parts.get(clean_code)

    def link_to_asset(
        self,
        relation: AssetSparePart,
    ) -> None:
        existing_relation = next(
            (
                item
                for item in self._relations
                if (
                    item.asset_code
                    == relation.asset_code
                    and item.spare_part_code
                    == relation.spare_part_code
                )
            ),
            None,
        )

        if existing_relation is None:
            self._relations.append(relation)
            return

        existing_relation.quantity = relation.quantity
        existing_relation.position = relation.position
        existing_relation.observations = (
            relation.observations
        )
        existing_relation.is_critical = (
            relation.is_critical
        )

    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[AssetSparePart]:
        clean_code = asset_code.strip()

        return [
            relation
            for relation in self._relations
            if relation.asset_code == clean_code
        ]

    def get_assets_by_spare_part_code(
        self,
        spare_part_code: str,
    ) -> list[AssetSparePart]:
        clean_code = spare_part_code.strip()

        return [
            relation
            for relation in self._relations
            if relation.spare_part_code == clean_code
        ]