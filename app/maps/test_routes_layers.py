import importlib

from app import create_app
from app.maps.models.map_layer import (
    MapLayer,
)


def test_should_return_active_map_layers() -> None:
    routes_module = importlib.import_module(
        "app.maps.routes"
    )

    original_use_case = getattr(
        routes_module,
        "list_active_map_layers",
        None,
    )

    class FakeResult:
        success = True
        layers = [
            MapLayer(
                code="electrical",
                name="Electrico",
                order=10,
                is_active=True,
            ),
            MapLayer(
                code="hvac",
                name="HVAC",
                order=20,
                is_active=True,
            ),
        ]

    class FakeListActiveMapLayers:
        def execute(self):
            return FakeResult()

    routes_module.list_active_map_layers = (
        FakeListActiveMapLayers()
    )

    try:
        app = create_app()
        app.config.update(
            TESTING=True,
        )

        with app.test_client() as client:
            response = client.get(
                "/maps/api/layers"
            )
    finally:
        if original_use_case is None:
            delattr(
                routes_module,
                "list_active_map_layers",
            )
        else:
            routes_module.list_active_map_layers = (
                original_use_case
            )

    assert response.status_code == 200

    assert response.get_json() == [
        {
            "code": "electrical",
            "name": "Electrico",
            "order": 10,
        },
        {
            "code": "hvac",
            "name": "HVAC",
            "order": 20,
        },
    ]
