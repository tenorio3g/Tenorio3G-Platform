from __future__ import annotations

from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)
from app.domains.locations.repositories.physical_location_repository import (
    PhysicalLocationRepository,
)

from .command import RegisterPhysicalLocationCommand
from .result import RegisterPhysicalLocationResult


class RegisterPhysicalLocation:
    """
    Caso de uso para registrar una ubicacion fisica.
    """

    def __init__(
        self,
        repository: PhysicalLocationRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: RegisterPhysicalLocationCommand,
    ) -> RegisterPhysicalLocationResult:

        clean_code = command.code.strip()

        existing_location = (
            self._repository.find_by_code(
                clean_code
            )
        )

        if existing_location is not None:
            return RegisterPhysicalLocationResult(
                success=False,
                message=(
                    "Ya existe una ubicacion "
                    "con ese codigo."
                ),
            )

        location = PhysicalLocation(
            code=command.code,
            name=command.name,
            area=command.area,
        )

        self._repository.save(
            location
        )

        return RegisterPhysicalLocationResult(
            success=True,
            message=(
                "Ubicacion registrada "
                "correctamente."
            ),
            location=location,
        )
