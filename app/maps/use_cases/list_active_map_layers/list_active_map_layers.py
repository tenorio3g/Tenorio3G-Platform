from __future__ import annotations

from app.maps.repositories.map_layer_repository import (
    MapLayerRepository,
)

from .result import ListActiveMapLayersResult


class ListActiveMapLayers:
    """
    Caso de uso para obtener las capas activas
    disponibles en el mapa industrial.
    """

    def __init__(
        self,
        repository: MapLayerRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
    ) -> ListActiveMapLayersResult:
        layers = self._repository.find_active()

        return ListActiveMapLayersResult(
            success=True,
            layers=layers,
        )
