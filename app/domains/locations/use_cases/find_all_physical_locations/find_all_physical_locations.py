from __future__ import annotations

from app.domains.locations.repositories.physical_location_repository import (
    PhysicalLocationRepository,
)

from .query import FindAllPhysicalLocationsQuery
from .result import FindAllPhysicalLocationsResult


class FindAllPhysicalLocations:
    """
    Caso de uso para consultar el catalogo completo
    de ubicaciones fisicas.
    """

    def __init__(
        self,
        repository: PhysicalLocationRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: FindAllPhysicalLocationsQuery,
    ) -> FindAllPhysicalLocationsResult:

        locations = self._repository.find_all()

        return FindAllPhysicalLocationsResult(
            success=True,
            message=self._build_message(
                len(locations)
            ),
            locations=locations,
        )

    @staticmethod
    def _build_message(
        count: int,
    ) -> str:

        if count == 0:
            return (
                "No hay ubicaciones registradas."
            )

        if count == 1:
            return (
                "Se encontro 1 ubicacion."
            )

        return (
            f"Se encontraron {count} ubicaciones."
        )
