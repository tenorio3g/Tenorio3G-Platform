from __future__ import annotations

import pytest

from app.maps.models.map_plan import MapPlan


def test_map_plan_should_normalize_its_identity() -> None:
    plan = MapPlan(
        code="  GROUND_FLOOR  ",
        name="  Planta Baja  ",
        order=10,
        is_active=True,
    )

    assert plan.code == "ground_floor"
    assert plan.name == "Planta Baja"
    assert plan.order == 10
    assert plan.is_active is True


def test_map_plan_should_default_order_to_zero() -> None:
    plan = MapPlan(
        code="roof",
        name="Techo",
    )

    assert plan.order == 0


def test_map_plan_should_default_to_active() -> None:
    plan = MapPlan(
        code="roof",
        name="Techo",
    )

    assert plan.is_active is True


@pytest.mark.parametrize(
    ("code", "name"),
    [
        ("", "Planta Baja"),
        ("   ", "Planta Baja"),
        ("ground_floor", ""),
        ("ground_floor", "   "),
    ],
)
def test_map_plan_should_reject_empty_identity(
    code: str,
    name: str,
) -> None:
    with pytest.raises(ValueError):
        MapPlan(
            code=code,
            name=name,
        )


@pytest.mark.parametrize(
    "order",
    [
        -1,
        1.5,
        "10",
        True,
        None,
    ],
)
def test_map_plan_should_reject_invalid_order(
    order,
) -> None:
    with pytest.raises(ValueError):
        MapPlan(
            code="ground_floor",
            name="Planta Baja",
            order=order,
        )


@pytest.mark.parametrize(
    "is_active",
    [
        1,
        0,
        "true",
        None,
    ],
)
def test_map_plan_should_require_boolean_active_state(
    is_active,
) -> None:
    with pytest.raises(ValueError):
        MapPlan(
            code="ground_floor",
            name="Planta Baja",
            is_active=is_active,
        )
