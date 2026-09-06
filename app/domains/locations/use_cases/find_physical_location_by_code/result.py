from __future__ import annotations

from dataclasses import dataclass

from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)


@dataclass(slots=True)
class FindPhysicalLocationByCodeResult:
    success: bool
    message: str
    location: PhysicalLocation | None = None
