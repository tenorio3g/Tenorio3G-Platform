from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base
from app.maps.models.map_plan import MapPlan
from app.maps.repositories.sqlite_map_plan_repository import (
    SQLiteMapPlanRepository,
)


def create_repository(tmp_path):
    database_path = (
        tmp_path
        / "map_plans_repository.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    TestSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(
        bind=engine
    )

    repository = (
        SQLiteMapPlanRepository(
            TestSessionLocal
        )
    )

    return repository, engine


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


def test_should_save_and_find_plan_by_code(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        create_plan(
            "ground_floor",
            "Planta Baja",
            10,
        )
    )

    plan = repository.find_by_code(
        "ground_floor"
    )

    assert plan is not None
    assert plan.code == "ground_floor"
    assert plan.name == "Planta Baja"
    assert plan.order == 10
    assert plan.is_active is True

    engine.dispose()


def test_find_by_code_should_normalize_input(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        create_plan(
            "ground_floor",
            "Planta Baja",
            10,
        )
    )

    plan = repository.find_by_code(
        "  GROUND_FLOOR  "
    )

    assert plan is not None
    assert plan.code == "ground_floor"

    engine.dispose()


def test_find_by_code_should_return_none_when_missing(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

    assert (
        repository.find_by_code("missing")
        is None
    )

    engine.dispose()


def test_save_should_update_existing_plan(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        create_plan(
            "roof",
            "Techo",
            30,
            True,
        )
    )

    repository.save(
        create_plan(
            "roof",
            "Azotea",
            40,
            False,
        )
    )

    plans = repository.find_all()

    assert len(plans) == 1
    assert plans[0].name == "Azotea"
    assert plans[0].order == 40
    assert plans[0].is_active is False

    engine.dispose()


def test_find_all_should_order_by_order_then_name(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

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

    plans = repository.find_all()

    assert [
        plan.code
        for plan in plans
    ] == [
        "ground_floor",
        "upper_floor",
        "roof",
    ]

    engine.dispose()


def test_find_active_should_exclude_inactive_plans(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

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
            False,
        )
    )

    repository.save(
        create_plan(
            "roof",
            "Techo",
            30,
            True,
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

    engine.dispose()
