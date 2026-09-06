from __future__ import annotations

from abc import ABC, abstractmethod

from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)


class PhysicalLocationRepository(ABC):
    """
    Contrato de persistencia para ubicaciones fisicas.
    """

    @abstractmethod
    def save(
        self,
        location: PhysicalLocation,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_code(
        self,
        code: str,
    ) -> PhysicalLocation | None:
        raise NotImplementedError

    @abstractmethod
    def find_all(
        self,
    ) -> list[PhysicalLocation]:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        location: PhysicalLocation,
    ) -> None:
        raise NotImplementedError
