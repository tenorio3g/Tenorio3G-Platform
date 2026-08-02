from __future__ import annotations

from abc import ABC, abstractmethod

from app.maps.models.map_location import MapLocation


class MapLocationRepository(ABC):
    """
    Contrato de persistencia para ubicaciones del mapa.
    """

    @abstractmethod
    def find_all(self) -> list[MapLocation]:
        raise NotImplementedError

    @abstractmethod
    def find_by_asset_code(
        self,
        asset_code: str,
    ) -> MapLocation | None:
        raise NotImplementedError

    @abstractmethod
    def save(
        self,
        location: MapLocation,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        asset_code: str,
    ) -> None:
        raise NotImplementedError