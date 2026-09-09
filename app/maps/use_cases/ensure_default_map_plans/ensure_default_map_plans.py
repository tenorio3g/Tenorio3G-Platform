from __future__ import annotations

from app.maps.models.map_plan import MapPlan
from app.maps.repositories.map_plan_repository import (
    MapPlanRepository,
)

from .result import EnsureDefaultMapPlansResult


class EnsureDefaultMapPlans:
    """
    Garantiza que existan los planos base del mapa
    sin sobrescribir configuraciones existentes.
    """

    def __init__(
        self,
        repository: MapPlanRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
    ) -> EnsureDefaultMapPlansResult:
        self._ensure_plan(
            code="ground_floor",
            name="Planta Baja",
            order=10,
            is_active=True,
        )

        self._ensure_plan(
            code="upper_floor",
            name="Planta Alta",
            order=20,
            is_active=True,
        )

        self._ensure_plan(
            code="roof",
            name="Techo",
            order=30,
            is_active=True,
        )

        return EnsureDefaultMapPlansResult(
            success=True,
        )

    def _ensure_plan(
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
            MapPlan(
                code=code,
                name=name,
                order=order,
                is_active=is_active,
            )
        )
