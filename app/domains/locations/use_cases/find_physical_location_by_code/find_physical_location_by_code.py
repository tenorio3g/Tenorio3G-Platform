from __future__ import annotations

from app.domains.locations.repositories.physical_location_repository import (
    PhysicalLocationRepository,
)

from .query import FindPhysicalLocationByCodeQuery
from .result import FindPhysicalLocationByCodeResult


class FindPhysicalLocationByCode:
    """
    Caso de uso para consultar una ubicacion fisica por codigo.
    """

    def __init__(
        self,
        repository: PhysicalLocationRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: FindPhysicalLocationByCodeQuery,
    ) -> FindPhysicalLocationByCodeResult:

        clean_code = query.code.strip()

        location = self._repository.find_by_code(
            clean_code
        )

        if location is None:
            return FindPhysicalLocationByCodeResult(
                success=False,
                message=(
                    "No existe la ubicacion indicada."
                ),
            )

        return FindPhysicalLocationByCodeResult(
            success=True,
            message=(
                "Ubicacion encontrada correctamente."
            ),
            location=location,
        )
