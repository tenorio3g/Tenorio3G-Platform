from __future__ import annotations

from dataclasses import dataclass

from app.maps.models.map_layer import MapLayer


@dataclass(frozen=True)
class ListActiveMapLayersResult:
    success: bool
    layers: list[MapLayer]
