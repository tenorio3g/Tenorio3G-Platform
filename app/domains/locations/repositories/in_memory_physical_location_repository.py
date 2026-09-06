from __future__ import annotations

from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)

from .physical_location_repository import (
    PhysicalLocationRepository,
)


class InMemoryPhysicalLocationRepository(
    PhysicalLocationRepository,
):
    """
    Implementacion en memoria del repositorio de ubicaciones.
    """

    def __init__(self) -> None:
        self._locations: dict[
            str,
            PhysicalLocation,
        ] = {}

    def save(
        self,
        location: PhysicalLocation,
    ) -> None:

        self._locations[
            location.code
        ] = location

    def find_by_code(
        self,
        code: str,
    ) -> PhysicalLocation | None:

        clean_code = code.strip()

        return self._locations.get(
            clean_code
        )

    def find_all(
        self,
    ) -> list[PhysicalLocation]:

        return [
            self._locations[code]
            for code in sorted(
                self._locations
            )
        ]

    def update(
        self,
        location: PhysicalLocation,
    ) -> None:

        if location.code not in self._locations:
            raise KeyError(
                location.code
            )

        self._locations[
            location.code
        ] = location
