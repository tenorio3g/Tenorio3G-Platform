from __future__ import annotations

from dataclasses import dataclass

from app.maps.models.map_location import (
    MapLocation,
)


@dataclass(frozen=True)
class PlaceAssetOnMapResult:
    success: bool
    message: str
    location: MapLocation | None = None
