import importlib

from app import create_app
from app.maps.models.map_location import (
    MapLocation,
)


def test_should_place_asset_on_map() -> None:
    routes_module = importlib.import_module(
        "app.maps.routes"
    )

    original_use_case = getattr(
        routes_module,
        "place_asset_on_map",
        None,
    )

    captured_command = {}

    class FakeResult:
        success = True
        message = (
            "Activo colocado correctamente en el mapa."
        )
        location = MapLocation(
            asset_code="ASSET-001",
            name="Tablero principal",
            category="tableros",
            x=35.5,
            y=62.0,
            layer_code="hvac",
            plan_code="roof",
        )

    class FakePlaceAssetOnMap:
        def execute(self, command):
            captured_command["command"] = command
            return FakeResult()

    routes_module.place_asset_on_map = (
        FakePlaceAssetOnMap()
    )

    try:
        app = create_app()
        app.config.update(
            TESTING=True,
        )

        with app.test_client() as client:
            response = client.post(
                "/maps/api/locations",
                json={
                    "asset_code": "ASSET-001",
                    "category": "tableros",
                    "x": 35.5,
                    "y": 62.0,
                    "layer_code": "hvac",
                    "plan_code": "roof",
                },
            )
    finally:
        if original_use_case is None:
            delattr(
                routes_module,
                "place_asset_on_map",
            )
        else:
            routes_module.place_asset_on_map = (
                original_use_case
            )

    assert response.status_code == 201

    command = captured_command["command"]

    assert command.asset_code == "ASSET-001"
    assert command.category == "tableros"
    assert command.x == 35.5
    assert command.y == 62.0
    assert command.layer_code == "hvac"
    assert command.plan_code == "roof"

    payload = response.get_json()

    assert payload == {
        "success": True,
        "message": (
            "Activo colocado correctamente en el mapa."
        ),
        "location": {
            "asset_code": "ASSET-001",
            "layer_code": "hvac",
            "plan_code": "roof",
            "name": "Tablero principal",
            "category": "tableros",
            "x": 35.5,
            "y": 62.0,
        },
    }


def test_should_return_bad_request_when_placement_fails():
    routes_module = importlib.import_module(
        "app.maps.routes"
    )

    original_use_case = getattr(
        routes_module,
        "place_asset_on_map",
        None,
    )

    class FakeResult:
        success = False
        message = (
            "El activo ya tiene una posicion "
            "registrada en el mapa."
        )
        location = None

    class FakePlaceAssetOnMap:
        def execute(self, command):
            return FakeResult()

    routes_module.place_asset_on_map = (
        FakePlaceAssetOnMap()
    )

    try:
        app = create_app()
        app.config.update(
            TESTING=True,
        )

        with app.test_client() as client:
            response = client.post(
                "/maps/api/locations",
                json={
                    "asset_code": "ASSET-001",
                    "category": "tableros",
                    "x": 35.5,
                    "y": 62.0,
                },
            )
    finally:
        if original_use_case is None:
            delattr(
                routes_module,
                "place_asset_on_map",
            )
        else:
            routes_module.place_asset_on_map = (
                original_use_case
            )

    assert response.status_code == 400

    assert response.get_json() == {
        "success": False,
        "message": (
            "El activo ya tiene una posicion "
            "registrada en el mapa."
        ),
    }


def test_should_default_to_electrical_layer_when_omitted() -> None:
    routes_module = importlib.import_module(
        "app.maps.routes"
    )

    original_use_case = getattr(
        routes_module,
        "place_asset_on_map",
        None,
    )

    captured_command = {}

    class FakeResult:
        success = True
        message = (
            "Activo colocado correctamente en el mapa."
        )
        location = MapLocation(
            asset_code="ASSET-001",
            name="Tablero principal",
            category="tableros",
            x=35.5,
            y=62.0,
        )

    class FakePlaceAssetOnMap:
        def execute(self, command):
            captured_command["command"] = command
            return FakeResult()

    routes_module.place_asset_on_map = (
        FakePlaceAssetOnMap()
    )

    try:
        app = create_app()
        app.config.update(
            TESTING=True,
        )

        with app.test_client() as client:
            response = client.post(
                "/maps/api/locations",
                json={
                    "asset_code": "ASSET-001",
                    "category": "tableros",
                    "x": 35.5,
                    "y": 62.0,
                },
            )
    finally:
        if original_use_case is None:
            delattr(
                routes_module,
                "place_asset_on_map",
            )
        else:
            routes_module.place_asset_on_map = (
                original_use_case
            )

    assert response.status_code == 201

    command = captured_command["command"]

    assert command.layer_code == "electrical"
    assert command.plan_code == "ground_floor"
