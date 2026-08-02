from __future__ import annotations

from app.maps.repositories.map_location_repository import (
    MapLocationRepository,
)

from .result import FindAllMapLocationsResult


class FindAllMapLocations:
    """
    Caso de uso para obtener todas las ubicaciones registradas.
    """

    def __init__(
        self,
        repository: MapLocationRepository,
    ) -> None:
        self._repository = repository

    def execute(self) -> FindAllMapLocationsResult:
        locations = self._repository.find_all()

        return FindAllMapLocationsResult(
            success=True,
            message="Ubicaciones obtenidas correctamente.",
            locations=locations,
        )