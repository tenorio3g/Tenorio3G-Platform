from __future__ import annotations

from dataclasses import dataclass, field

from app.maps.models.map_location import MapLocation


@dataclass(slots=True)
class FindAllMapLocationsResult:
    success: bool
    message: str
    locations: list[MapLocation] = field(default_factory=list)