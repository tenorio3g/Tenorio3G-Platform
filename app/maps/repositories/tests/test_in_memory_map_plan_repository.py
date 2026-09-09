from __future__ import annotations

from app.maps.models.map_plan import MapPlan
from app.maps.repositories.in_memory_map_plan_repository import (
    InMemoryMapPlanRepository,
)


def create_repository() -> InMemoryMapPlanRepository:
    return InMemoryMapPlanRepository()


def test_repository_should_save_and_find_plan() -> None:
    repository = create_repository()

    plan = MapPlan(
        code="ground_floor",
        name="Planta Baja",
        order=10,
    )

    repository.save(plan)

    found = repository.find_by_code(
        "ground_floor"
    )

    assert found is plan


def test_find_by_code_should_normalize_code() -> None:
    repository = create_repository()

    plan = MapPlan(
        code="ground_floor",
        name="Planta Baja",
    )

    repository.save(plan)

    found = repository.find_by_code(
        "  GROUND_FLOOR  "
    )

    assert found is plan


def test_find_by_code_should_return_none_when_missing() -> None:
    repository = create_repository()

    assert (
        repository.find_by_code("missing")
        is None
    )


def test_save_should_replace_existing_plan() -> None:
    repository = create_repository()

    repository.save(
        MapPlan(
            code="roof",
            name="Techo",
            order=30,
        )
    )

    replacement = MapPlan(
        code="roof",
        name="Azotea",
        order=20,
    )

    repository.save(replacement)

    assert (
        repository.find_by_code("roof")
        is replacement
    )

    assert len(repository.find_all()) == 1


def test_find_all_should_return_sorted_plans() -> None:
    repository = create_repository()

    repository.save(
        MapPlan(
            code="roof",
            name="Techo",
            order=30,
        )
    )

    repository.save(
        MapPlan(
            code="upper_floor",
            name="Planta Alta",
            order=20,
        )
    )

    repository.save(
        MapPlan(
            code="ground_floor",
            name="Planta Baja",
            order=10,
        )
    )

    plans = repository.find_all()

    assert [
        plan.code
        for plan in plans
    ] == [
        "ground_floor",
        "upper_floor",
        "roof",
    ]


def test_find_active_should_exclude_inactive_plans() -> None:
    repository = create_repository()

    repository.save(
        MapPlan(
            code="ground_floor",
            name="Planta Baja",
            order=10,
            is_active=True,
        )
    )

    repository.save(
        MapPlan(
            code="upper_floor",
            name="Planta Alta",
            order=20,
            is_active=False,
        )
    )

    repository.save(
        MapPlan(
            code="roof",
            name="Techo",
            order=30,
            is_active=True,
        )
    )

    plans = repository.find_active()

    assert [
        plan.code
        for plan in plans
    ] == [
        "ground_floor",
        "roof",
    ]
