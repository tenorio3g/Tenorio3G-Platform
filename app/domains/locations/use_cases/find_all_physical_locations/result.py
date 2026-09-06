from __future__ import annotations

from dataclasses import dataclass, field

from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)


@dataclass(slots=True)
class FindAllPhysicalLocationsResult:
    success: bool
    message: str
    locations: list[PhysicalLocation] = field(
        default_factory=list
    )
