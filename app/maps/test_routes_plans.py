import importlib

from app import create_app
from app.maps.models.map_plan import (
    MapPlan,
)


def test_should_return_active_map_plans() -> None:
    routes_module = importlib.import_module(
        "app.maps.routes"
    )

    original_use_case = getattr(
        routes_module,
        "list_active_map_plans",
        None,
    )

    class FakeResult:
        success = True
        plans = [
            MapPlan(
                code="ground_floor",
                name="Planta Baja",
                order=10,
                is_active=True,
            ),
            MapPlan(
                code="upper_floor",
                name="Planta Alta",
                order=20,
                is_active=True,
            ),
            MapPlan(
                code="roof",
                name="Techo",
                order=30,
                is_active=True,
            ),
        ]

    class FakeListActiveMapPlans:
        def execute(self):
            return FakeResult()

    routes_module.list_active_map_plans = (
        FakeListActiveMapPlans()
    )

    try:
        app = create_app()
        app.config.update(
            TESTING=True,
        )

        with app.test_client() as client:
            response = client.get(
                "/maps/api/plans"
            )
    finally:
        if original_use_case is None:
            delattr(
                routes_module,
                "list_active_map_plans",
            )
        else:
            routes_module.list_active_map_plans = (
                original_use_case
            )

    assert response.status_code == 200

    assert response.get_json() == [
        {
            "code": "ground_floor",
            "name": "Planta Baja",
            "order": 10,
        },
        {
            "code": "upper_floor",
            "name": "Planta Alta",
            "order": 20,
        },
        {
            "code": "roof",
            "name": "Techo",
            "order": 30,
        },
    ]
