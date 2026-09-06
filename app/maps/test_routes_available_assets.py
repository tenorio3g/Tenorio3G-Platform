import importlib
from datetime import date

from app import create_app
from app.domains.assets.entities.asset import Asset
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)
from app.maps.models.map_location import (
    MapLocation,
)


def create_asset(
    code: str,
    name: str,
) -> Asset:
    return Asset(
        code=code,
        name=name,
        asset_model_code="MODEL-001",
        serial_number=f"SERIAL-{code}",
        location_code="PLANTA-01",
        status=AssetStatus.OPERATING,
        installation_date=date(
            2026,
            1,
            1,
        ),
    )


def test_should_return_only_assets_without_map_location(
    monkeypatch,
) -> None:
    available_asset = create_asset(
        code="ASSET-AVAILABLE",
        name="Activo disponible",
    )

    placed_asset = create_asset(
        code="ASSET-PLACED",
        name="Activo colocado",
    )

    class FakeFindAllAssetsResult:
        success = True
        assets = [
            available_asset,
            placed_asset,
        ]

    class FakeFindAllAssets:
        def execute(self, query):
            return FakeFindAllAssetsResult()

    class FakeFindAllMapLocationsResult:
        success = True
        locations = [
            MapLocation(
                asset_code="ASSET-PLACED",
                name="Activo colocado",
                category="tableros",
                x=50.0,
                y=50.0,
            )
        ]

    class FakeFindAllMapLocations:
        def execute(self):
            return (
                FakeFindAllMapLocationsResult()
            )

    routes_module = importlib.import_module(
        "app.maps.routes"
    )

    monkeypatch.setattr(
        routes_module,
        "find_all_assets",
        FakeFindAllAssets(),
        raising=False,
    )

    monkeypatch.setattr(
        routes_module,
        "find_all_map_locations",
        FakeFindAllMapLocations(),
    )

    app = create_app()
    app.config.update(
        TESTING=True,
    )

    with app.test_client() as client:
        response = client.get(
            "/maps/api/available-assets"
        )

    assert response.status_code == 200

    payload = response.get_json()

    assert payload == [
        {
            "code": "ASSET-AVAILABLE",
            "name": "Activo disponible",
        }
    ]
