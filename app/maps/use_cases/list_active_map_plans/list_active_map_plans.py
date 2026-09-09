from __future__ import annotations

from app.maps.repositories.map_plan_repository import (
    MapPlanRepository,
)

from .result import ListActiveMapPlansResult


class ListActiveMapPlans:
    """
    Caso de uso para obtener los planos activos
    disponibles en el mapa industrial.
    """

    def __init__(
        self,
        repository: MapPlanRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
    ) -> ListActiveMapPlansResult:
        plans = self._repository.find_active()

        return ListActiveMapPlansResult(
            success=True,
            plans=plans,
        )
