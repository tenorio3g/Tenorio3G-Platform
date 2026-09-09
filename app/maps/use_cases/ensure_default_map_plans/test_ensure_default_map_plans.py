from app.maps.models.map_plan import MapPlan
from app.maps.repositories.in_memory_map_plan_repository import (
    InMemoryMapPlanRepository,
)
from app.maps.use_cases.ensure_default_map_plans import (
    EnsureDefaultMapPlans,
)


def test_should_create_default_plans():
    repository = (
        InMemoryMapPlanRepository()
    )

    use_case = (
        EnsureDefaultMapPlans(
            repository
        )
    )

    result = use_case.execute()

    assert result.success is True

    plans = repository.find_all()

    assert [
        plan.code
        for plan in plans
    ] == [
        "ground_floor",
        "upper_floor",
        "roof",
    ]

    assert plans[0].name == "Planta Baja"
    assert plans[0].order == 10

    assert plans[1].name == "Planta Alta"
    assert plans[1].order == 20

    assert plans[2].name == "Techo"
    assert plans[2].order == 30


def test_should_be_idempotent():
    repository = (
        InMemoryMapPlanRepository()
    )

    use_case = (
        EnsureDefaultMapPlans(
            repository
        )
    )

    use_case.execute()
    use_case.execute()

    plans = repository.find_all()

    assert len(plans) == 3


def test_should_preserve_existing_plan_configuration():
    repository = (
        InMemoryMapPlanRepository()
    )

    repository.save(
        MapPlan(
            code="ground_floor",
            name="PB Modificada",
            order=5,
            is_active=False,
        )
    )

    use_case = (
        EnsureDefaultMapPlans(
            repository
        )
    )

    result = use_case.execute()

    assert result.success is True

    plan = repository.find_by_code(
        "ground_floor"
    )

    assert plan is not None
    assert plan.name == "PB Modificada"
    assert plan.order == 5
    assert plan.is_active is False

    roof = repository.find_by_code(
        "roof"
    )

    assert roof is not None
    assert roof.name == "Techo"
