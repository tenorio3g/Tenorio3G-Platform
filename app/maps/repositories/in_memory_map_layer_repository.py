from __future__ import annotations

from app.maps.models.map_layer import MapLayer

from .map_layer_repository import MapLayerRepository


class InMemoryMapLayerRepository(
    MapLayerRepository,
):
    """
    Repositorio en memoria para capas del mapa.

    Util para pruebas y casos de uso sin dependencia
    de base de datos.
    """

    def __init__(self) -> None:
        self._layers: dict[str, MapLayer] = {}

    def save(
        self,
        layer: MapLayer,
    ) -> None:
        self._layers[layer.code] = layer

    def find_by_code(
        self,
        code: str,
    ) -> MapLayer | None:
        clean_code = str(code).strip().lower()

        return self._layers.get(clean_code)

    def find_all(
        self,
    ) -> list[MapLayer]:
        return self._sorted_layers(
            list(self._layers.values())
        )

    def find_active(
        self,
    ) -> list[MapLayer]:
        active_layers = [
            layer
            for layer in self._layers.values()
            if layer.is_active
        ]

        return self._sorted_layers(
            active_layers
        )

    @staticmethod
    def _sorted_layers(
        layers: list[MapLayer],
    ) -> list[MapLayer]:
        return sorted(
            layers,
            key=lambda layer: (
                layer.order,
                layer.name.lower(),
            ),
        )
