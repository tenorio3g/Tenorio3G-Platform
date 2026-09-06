from app.maps.models.map_location import (
    MapLocation,
)
from app.maps.use_cases.move_asset_on_map.command import (
    MoveAssetOnMapCommand,
)
from app.maps.use_cases.move_asset_on_map.move_asset_on_map import (
    MoveAssetOnMap,
)


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


def create_location() -> MapLocation:
    return MapLocation(
        asset_code="ASSET-001",
        name="Tablero General",
        category="tableros",
        x=10.0,
        y=20.0,
    )


def test_should_move_existing_asset_on_map() -> None:
    repository = (
        FakeMapLocationRepository()
    )

    location = create_location()
    repository.save(location)

    use_case = MoveAssetOnMap(
        repository
    )

    result = use_case.execute(
        MoveAssetOnMapCommand(
            asset_code="ASSET-001",
            x=60.0,
            y=70.0,
        )
    )

    assert result.success is True
    assert result.location is not None

    assert result.location.x == 60.0
    assert result.location.y == 70.0

    assert result.location.asset_code == (
        "ASSET-001"
    )
    assert result.location.name == (
        "Tablero General"
    )
    assert result.location.category == (
        "tableros"
    )

    persisted = (
        repository.find_by_asset_code(
            "ASSET-001"
        )
    )

    assert persisted is not None
    assert persisted.x == 60.0
    assert persisted.y == 70.0


def test_should_reject_asset_without_map_location() -> None:
    repository = (
        FakeMapLocationRepository()
    )

    use_case = MoveAssetOnMap(
        repository
    )

    result = use_case.execute(
        MoveAssetOnMapCommand(
            asset_code="UNKNOWN",
            x=50.0,
            y=50.0,
        )
    )

    assert result.success is False
    assert result.location is None
    assert repository.find_all() == []


def test_should_reject_invalid_coordinates() -> None:
    repository = (
        FakeMapLocationRepository()
    )

    location = create_location()
    repository.save(location)

    use_case = MoveAssetOnMap(
        repository
    )

    result = use_case.execute(
        MoveAssetOnMapCommand(
            asset_code="ASSET-001",
            x=101.0,
            y=50.0,
        )
    )

    assert result.success is False
    assert result.location is None

    persisted = (
        repository.find_by_asset_code(
            "ASSET-001"
        )
    )

    assert persisted is not None
    assert persisted.x == 10.0
    assert persisted.y == 20.0
