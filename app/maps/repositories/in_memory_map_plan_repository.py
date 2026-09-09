from __future__ import annotations

from app.maps.models.map_plan import MapPlan
from app.maps.repositories.map_plan_repository import (
    MapPlanRepository,
)


class InMemoryMapPlanRepository(
    MapPlanRepository
):
    """
    Implementacion en memoria del repositorio
    de planos del mapa.
    """

    def __init__(self) -> None:
        self._plans: dict[str, MapPlan] = {}

    def save(
        self,
        plan: MapPlan,
    ) -> None:
        self._plans[plan.code] = plan

    def find_by_code(
        self,
        code: str,
    ) -> MapPlan | None:
        clean_code = str(code).strip().lower()

        return self._plans.get(
            clean_code
        )

    def find_all(
        self,
    ) -> list[MapPlan]:
        return sorted(
            self._plans.values(),
            key=self._sort_key,
        )

    def find_active(
        self,
    ) -> list[MapPlan]:
        return sorted(
            (
                plan
                for plan in self._plans.values()
                if plan.is_active
            ),
            key=self._sort_key,
        )

    @staticmethod
    def _sort_key(
        plan: MapPlan,
    ) -> tuple[int, str]:
        return (
            plan.order,
            plan.name.lower(),
        )
