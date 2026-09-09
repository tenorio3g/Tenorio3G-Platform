from __future__ import annotations

from abc import ABC, abstractmethod

from app.maps.models.map_layer import MapLayer


class MapLayerRepository(ABC):
    """
    Contrato de persistencia para capas del mapa.
    """

    @abstractmethod
    def save(
        self,
        layer: MapLayer,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_code(
        self,
        code: str,
    ) -> MapLayer | None:
        raise NotImplementedError

    @abstractmethod
    def find_all(
        self,
    ) -> list[MapLayer]:
        raise NotImplementedError

    @abstractmethod
    def find_active(
        self,
    ) -> list[MapLayer]:
        raise NotImplementedError
