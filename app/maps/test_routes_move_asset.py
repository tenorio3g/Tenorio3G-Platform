import importlib

from app import create_app
from app.maps.models.map_location import (
    MapLocation,
)


def test_should_move_asset_on_map() -> None:
    routes_module = importlib.import_module(
        "app.maps.routes"
    )

    original_use_case = getattr(
        routes_module,
        "move_asset_on_map",
        None,
    )

    captured_command = {}

    class FakeResult:
        success = True
        message = (
            "Activo reubicado correctamente en el mapa."
        )
        location = MapLocation(
            asset_code="ASSET-001",
            name="Tablero principal",
            category="tableros",
            x=72.4,
            y=18.6,
        )

    class FakeMoveAssetOnMap:
        def execute(self, command):
            captured_command["command"] = command
            return FakeResult()

    routes_module.move_asset_on_map = (
        FakeMoveAssetOnMap()
    )

    try:
        app = create_app()
        app.config.update(
            TESTING=True,
        )

        with app.test_client() as client:
            response = client.patch(
                "/maps/api/locations/ASSET-001",
                json={
                    "x": 72.4,
                    "y": 18.6,
                },
            )
    finally:
        if original_use_case is None:
            delattr(
                routes_module,
                "move_asset_on_map",
            )
        else:
            routes_module.move_asset_on_map = (
                original_use_case
            )

    assert response.status_code == 200

    command = captured_command["command"]

    assert command.asset_code == "ASSET-001"
    assert command.x == 72.4
    assert command.y == 18.6

    assert response.get_json() == {
        "success": True,
        "message": (
            "Activo reubicado correctamente en el mapa."
        ),
        "location": {
            "asset_code": "ASSET-001",
            "layer_code": "electrical",
            "plan_code": "ground_floor",
            "name": "Tablero principal",
            "category": "tableros",
            "x": 72.4,
            "y": 18.6,
        },
    }


def test_should_return_bad_request_when_move_fails():
    routes_module = importlib.import_module(
        "app.maps.routes"
    )

    original_use_case = getattr(
        routes_module,
        "move_asset_on_map",
        None,
    )

    class FakeResult:
        success = False
        message = (
            "El activo no tiene una posicion "
            "registrada en el mapa."
        )
        location = None

    class FakeMoveAssetOnMap:
        def execute(self, command):
            return FakeResult()

    routes_module.move_asset_on_map = (
        FakeMoveAssetOnMap()
    )

    try:
        app = create_app()
        app.config.update(
            TESTING=True,
        )

        with app.test_client() as client:
            response = client.patch(
                "/maps/api/locations/ASSET-404",
                json={
                    "x": 20.0,
                    "y": 30.0,
                },
            )
    finally:
        if original_use_case is None:
            delattr(
                routes_module,
                "move_asset_on_map",
            )
        else:
            routes_module.move_asset_on_map = (
                original_use_case
            )

    assert response.status_code == 400

    assert response.get_json() == {
        "success": False,
        "message": (
            "El activo no tiene una posicion "
            "registrada en el mapa."
        ),
    }
