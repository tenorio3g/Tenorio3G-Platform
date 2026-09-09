from __future__ import annotations

from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.maps.models.map_plan import MapPlan

from .map_plan_repository import MapPlanRepository


class SQLiteMapPlanRepository(
    MapPlanRepository,
):
    """
    Implementacion SQLite del repositorio de planos del mapa.
    """

    def __init__(
        self,
        session_factory: Callable[[], Session],
    ) -> None:
        self._session_factory = session_factory

    def save(
        self,
        plan: MapPlan,
    ) -> None:
        with self._session_factory() as session:
            existing = session.scalar(
                select(MapPlan).where(
                    MapPlan.code == plan.code
                )
            )

            if existing is None:
                session.add(plan)

            else:
                existing.name = plan.name
                existing.order = plan.order
                existing.is_active = plan.is_active

            session.commit()

    def find_by_code(
        self,
        code: str,
    ) -> MapPlan | None:
        clean_code = str(code).strip().lower()

        with self._session_factory() as session:
            statement = select(
                MapPlan
            ).where(
                MapPlan.code == clean_code
            )

            return session.scalar(statement)

    def find_all(
        self,
    ) -> list[MapPlan]:
        with self._session_factory() as session:
            statement = (
                select(MapPlan)
                .order_by(
                    MapPlan.order,
                    MapPlan.name,
                )
            )

            return list(
                session.scalars(statement).all()
            )

    def find_active(
        self,
    ) -> list[MapPlan]:
        with self._session_factory() as session:
            statement = (
                select(MapPlan)
                .where(
                    MapPlan.is_active.is_(True)
                )
                .order_by(
                    MapPlan.order,
                    MapPlan.name,
                )
            )

            return list(
                session.scalars(statement).all()
            )
