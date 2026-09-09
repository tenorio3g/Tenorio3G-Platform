from __future__ import annotations

from abc import ABC, abstractmethod

from app.maps.models.map_plan import MapPlan


class MapPlanRepository(ABC):
    """
    Contrato de persistencia para planos fisicos
    del mapa industrial.
    """

    @abstractmethod
    def save(
        self,
        plan: MapPlan,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_code(
        self,
        code: str,
    ) -> MapPlan | None:
        raise NotImplementedError

    @abstractmethod
    def find_all(
        self,
    ) -> list[MapPlan]:
        raise NotImplementedError

    @abstractmethod
    def find_active(
        self,
    ) -> list[MapPlan]:
        raise NotImplementedError
