from app.maps.models.map_plan import MapPlan
from app.maps.repositories.in_memory_map_plan_repository import (
    InMemoryMapPlanRepository,
)
from app.maps.use_cases.list_active_map_plans import (
    ListActiveMapPlans,
)


def create_plan(
    code,
    name,
    order,
    is_active=True,
):
    return MapPlan(
        code=code,
        name=name,
        order=order,
        is_active=is_active,
    )


def test_should_return_only_active_plans():
    repository = InMemoryMapPlanRepository()

    repository.save(
        create_plan(
            "ground_floor",
            "Planta Baja",
            10,
            True,
        )
    )

    repository.save(
        create_plan(
            "upper_floor",
            "Planta Alta",
            20,
            True,
        )
    )

    repository.save(
        create_plan(
            "obsolete",
            "Obsoleto",
            30,
            False,
        )
    )

    use_case = ListActiveMapPlans(
        repository
    )

    result = use_case.execute()

    assert result.success is True

    assert [
        plan.code
        for plan in result.plans
    ] == [
        "ground_floor",
        "upper_floor",
    ]


def test_should_return_empty_result_when_no_active_plans():
    repository = InMemoryMapPlanRepository()

    repository.save(
        create_plan(
            "inactive",
            "Inactivo",
            10,
            False,
        )
    )

    use_case = ListActiveMapPlans(
        repository
    )

    result = use_case.execute()

    assert result.success is True
    assert result.plans == []


def test_should_preserve_repository_order():
    repository = InMemoryMapPlanRepository()

    repository.save(
        create_plan(
            "roof",
            "Techo",
            30,
        )
    )

    repository.save(
        create_plan(
            "upper_floor",
            "Planta Alta",
            20,
        )
    )

    repository.save(
        create_plan(
            "ground_floor",
            "Planta Baja",
            10,
        )
    )

    use_case = ListActiveMapPlans(
        repository
    )

    result = use_case.execute()

    assert [
        plan.code
        for plan in result.plans
    ] == [
        "ground_floor",
        "upper_floor",
        "roof",
    ]
