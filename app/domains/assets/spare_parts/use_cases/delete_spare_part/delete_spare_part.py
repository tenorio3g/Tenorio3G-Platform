from app.domains.assets.spare_parts.repositories import (
    SparePartRepository,
)

from .command import DeleteSparePartCommand
from .result import DeleteSparePartResult


class DeleteSparePart:

    def __init__(
        self,
        repository: SparePartRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: DeleteSparePartCommand,
    ) -> DeleteSparePartResult:

        asset_code = command.asset_code.strip()
        spare_part_code = (
            command.spare_part_code.strip()
        )

        if not asset_code:
            return DeleteSparePartResult(
                success=False,
                message="El código del activo es obligatorio.",
            )

        if not spare_part_code:
            return DeleteSparePartResult(
                success=False,
                message=(
                    "El código de la refacción "
                    "es obligatorio."
                ),
            )

        self._repository.unlink_from_asset(
            asset_code,
            spare_part_code,
        )

        return DeleteSparePartResult(
            success=True,
            message="Refacción eliminada del activo.",
        )