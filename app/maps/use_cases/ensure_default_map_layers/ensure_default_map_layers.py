from __future__ import annotations

from app.maps.models.map_layer import MapLayer
from app.maps.repositories.map_layer_repository import (
    MapLayerRepository,
)

from .result import EnsureDefaultMapLayersResult


class EnsureDefaultMapLayers:
    """
    Garantiza que existan las capas base del mapa
    sin sobrescribir configuraciones existentes.
    """

    def __init__(
        self,
        repository: MapLayerRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
    ) -> EnsureDefaultMapLayersResult:
        self._ensure_layer(
            code="electrical",
            name="Electrico",
            order=10,
            is_active=True,
        )

        self._ensure_layer(
            code="hvac",
            name="HVAC",
            order=20,
            is_active=True,
        )

        return EnsureDefaultMapLayersResult(
            success=True,
        )

    def _ensure_layer(
        self,
        code: str,
        name: str,
        order: int,
        is_active: bool,
    ) -> None:
        existing = self._repository.find_by_code(
            code
        )

        if existing is not None:
            return

        self._repository.save(
            MapLayer(
                code=code,
                name=name,
                order=order,
                is_active=is_active,
            )
        )
