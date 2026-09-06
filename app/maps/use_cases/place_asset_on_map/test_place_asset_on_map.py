from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)
from app.maps.models.map_location import (
    MapLocation,
)
from app.maps.use_cases.place_asset_on_map.command import (
    PlaceAssetOnMapCommand,
)
from app.maps.use_cases.place_asset_on_map.place_asset_on_map import (
    PlaceAssetOnMap,
)


class FakeAssetRepository:
    def __init__(self) -> None:
        self.assets: dict[str, Asset] = {}

    def save(
        self,
        asset: Asset,
    ) -> None:
        self.assets[asset.code] = asset

    def find_by_code(
        self,
        code: str,
    ) -> Asset | None:
        return self.assets.get(code.strip())

    def find_all(
        self,
    ) -> list[Asset]:
        return list(self.assets.values())

    def update(
        self,
        asset: Asset,
    ) -> None:
        self.assets[asset.code] = asset


class FakeMapLocationRepository:
    def __init__(self) -> None:
        self.locations: dict[
            str,
            MapLocation,
        ] = {}

    def find_all(
        self,
    ) -> list[MapLocation]:
        return list(
            self.locations.values()
        )

    def find_by_asset_code(
        self,
        asset_code: str,
    ) -> MapLocation | None:
        return self.locations.get(
            asset_code.strip()
        )

    def save(
        self,
        location: MapLocation,
    ) -> None:
        self.locations[
            location.asset_code
        ] = location

    def delete(
        self,
        asset_code: str,
    ) -> None:
        self.locations.pop(
            asset_code.strip(),
            None,
        )


def create_asset(
    code: str = "ASSET-001",
    name: str = "Tablero General",
) -> Asset:
    return Asset(
        code=code,
        name=name,
        asset_model_code="MODEL-001",
        serial_number="SERIAL-001",
        location_code="PLANTA-01",
        status=AssetStatus.OPERATING,
        installation_date=date(
            2026,
            1,
            1,
        ),
    )


def create_use_case():
    asset_repository = (
        FakeAssetRepository()
    )

    map_repository = (
        FakeMapLocationRepository()
    )

    use_case = PlaceAssetOnMap(
        asset_repository,
        map_repository,
    )

    return (
        use_case,
        asset_repository,
        map_repository,
    )


def test_should_place_existing_asset_on_map() -> None:
    (
        use_case,
        asset_repository,
        map_repository,
    ) = create_use_case()

    asset_repository.save(
        create_asset(
            name="TABLERO GENERAL ES09",
        )
    )

    result = use_case.execute(
        PlaceAssetOnMapCommand(
            asset_code="ASSET-001",
            category="tableros",
            x=52.4,
            y=38.7,
        )
    )

    assert result.success is True
    assert result.location is not None

    assert result.location.asset_code == (
        "ASSET-001"
    )
    assert result.location.name == (
        "TABLERO GENERAL ES09"
    )
    assert result.location.category == (
        "tableros"
    )
    assert result.location.x == 52.4
    assert result.location.y == 38.7

    persisted = (
        map_repository.find_by_asset_code(
            "ASSET-001"
        )
    )

    assert persisted is result.location


def test_should_reject_unknown_asset() -> None:
    (
        use_case,
        _,
        map_repository,
    ) = create_use_case()

    result = use_case.execute(
        PlaceAssetOnMapCommand(
            asset_code="UNKNOWN",
            category="tableros",
            x=50.0,
            y=50.0,
        )
    )

    assert result.success is False
    assert result.location is None
    assert (
        map_repository.find_all()
        == []
    )


def test_should_reject_asset_already_on_map() -> None:
    (
        use_case,
        asset_repository,
        map_repository,
    ) = create_use_case()

    asset = create_asset()
    asset_repository.save(asset)

    map_repository.save(
        MapLocation(
            asset_code=asset.code,
            name=asset.name,
            category="tableros",
            x=10.0,
            y=20.0,
        )
    )

    result = use_case.execute(
        PlaceAssetOnMapCommand(
            asset_code=asset.code,
            category="tableros",
            x=60.0,
            y=70.0,
        )
    )

    assert result.success is False

    persisted = (
        map_repository.find_by_asset_code(
            asset.code
        )
    )

    assert persisted is not None
    assert persisted.x == 10.0
    assert persisted.y == 20.0


def test_should_reject_coordinates_outside_map() -> None:
    (
        use_case,
        asset_repository,
        map_repository,
    ) = create_use_case()

    asset_repository.save(
        create_asset()
    )

    invalid_coordinates = (
        (-0.1, 50.0),
        (100.1, 50.0),
        (50.0, -0.1),
        (50.0, 100.1),
    )

    for x, y in invalid_coordinates:
        result = use_case.execute(
            PlaceAssetOnMapCommand(
                asset_code="ASSET-001",
                category="tableros",
                x=x,
                y=y,
            )
        )

        assert result.success is False
        assert result.location is None

    assert (
        map_repository.find_all()
        == []
    )


def test_should_reject_blank_category() -> None:
    (
        use_case,
        asset_repository,
        map_repository,
    ) = create_use_case()

    asset_repository.save(
        create_asset()
    )

    result = use_case.execute(
        PlaceAssetOnMapCommand(
            asset_code="ASSET-001",
            category="   ",
            x=50.0,
            y=50.0,
        )
    )

    assert result.success is False
    assert result.location is None
    assert (
        map_repository.find_all()
        == []
    )
