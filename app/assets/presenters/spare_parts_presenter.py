from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
)

from .spare_parts_view_model import (
    SparePartItemViewModel,
    SparePartsViewModel,
)


class SparePartsPresenter:
    """
    Adapta las relaciones activo-refacción
    para mostrarlas en el expediente técnico.
    """

    @staticmethod
    def present(
        relations: list[AssetSparePart],
    ) -> SparePartsViewModel:

        items = [
            SparePartItemViewModel(
                code=relation.spare_part.code,
                name=relation.spare_part.name,
                manufacturer=(
                    relation.spare_part.manufacturer
                    or "Sin fabricante registrado"
                ),
                part_number=(
                    relation.spare_part.part_number
                    or "Sin número de parte"
                ),
                quantity=relation.quantity,
                position=(
                    relation.position
                    or "Sin posición registrada"
                ),
                observations=(
                    relation.observations
                    or ""
                ),
                is_critical=relation.is_critical,
            )
            for relation in relations
        ]

        return SparePartsViewModel(
            items=items,
        )