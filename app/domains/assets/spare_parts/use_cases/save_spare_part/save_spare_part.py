from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
    SparePart,
)

from app.domains.assets.spare_parts.repositories import (
    SparePartRepository,
)

from .command import SaveSparePartCommand
from .result import SaveSparePartResult


class SaveSparePart:
    """
    Registra o actualiza una refacción
    y la relaciona con un activo.
    """

    def __init__(
        self,
        repository: SparePartRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: SaveSparePartCommand,
    ) -> SaveSparePartResult:

        asset_code = command.asset_code.strip()
        code = command.code.strip()
        name = command.name.strip()

        if not asset_code:
            return SaveSparePartResult(
                success=False,
                message="El código del activo es obligatorio.",
            )

        if not code:
            return SaveSparePartResult(
                success=False,
                message="El código de la refacción es obligatorio.",
            )

        if not name:
            return SaveSparePartResult(
                success=False,
                message="El nombre de la refacción es obligatorio.",
            )

        if command.quantity <= 0:
            return SaveSparePartResult(
                success=False,
                message="La cantidad debe ser mayor que cero.",
            )

        spare_part = SparePart(
            code=code,
            name=name,
            manufacturer=command.manufacturer.strip(),
            part_number=command.part_number.strip(),
            unit=command.unit.strip() or "pieza",
        )

        relation = AssetSparePart(
            asset_code=asset_code,
            spare_part=spare_part,
            quantity=command.quantity,
            position=command.position.strip(),
            observations=command.observations.strip(),
            is_critical=command.is_critical,
        )

        self._repository.save_spare_part(
            spare_part
        )

        self._repository.link_to_asset(
            relation
        )

        return SaveSparePartResult(
            success=True,
            message="Refacción guardada correctamente.",
        )