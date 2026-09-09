from __future__ import annotations

from dataclasses import dataclass

from app.maps.models.map_plan import MapPlan


@dataclass(frozen=True)
class ListActiveMapPlansResult:
    success: bool
    plans: list[MapPlan]
