from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)
from app.maps.models.map_layer import (
    MapLayer,
)
from app.maps.models.map_plan import (
    MapPlan,
)
from app.maps.models.map_location import (
    MapLocation,
)
from app.maps.repositories.in_memory_map_layer_repository import (
    InMemoryMapLayerRepository,
)
from app.maps.repositories.in_memory_map_plan_repository import (
    InMemoryMapPlanRepository,
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

    layer_repository = (
        InMemoryMapLayerRepository()
    )

    layer_repository.save(
        MapLayer(
            code="electrical",
            name="Electrico",
            order=10,
            is_active=True,
        )
    )

    layer_repository.save(
        MapLayer(
            code="hvac",
            name="HVAC",
            order=20,
            is_active=True,
        )
    )

    plan_repository = (
        InMemoryMapPlanRepository()
    )

    plan_repository.save(
        MapPlan(
            code="ground_floor",
            name="Planta Baja",
            order=10,
            is_active=True,
        )
    )

    plan_repository.save(
        MapPlan(
            code="upper_floor",
            name="Planta Alta",
            order=20,
            is_active=True,
        )
    )

    plan_repository.save(
        MapPlan(
            code="roof",
            name="Techo",
            order=30,
            is_active=True,
        )
    )

    use_case = PlaceAssetOnMap(
        asset_repository,
        map_repository,
        layer_repository,
        plan_repository,
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


def test_should_place_asset_in_explicit_layer() -> None:
    (
        use_case,
        asset_repository,
        map_repository,
    ) = create_use_case()

    asset_repository.save(
        create_asset(
            code="CH-001",
            name="Chiller 1",
        )
    )

    result = use_case.execute(
        PlaceAssetOnMapCommand(
            asset_code="CH-001",
            category="chiller",
            x=25.0,
            y=30.0,
            layer_code="hvac",
        )
    )

    assert result.success is True
    assert result.location is not None
    assert result.location.layer_code == "hvac"

    persisted = (
        map_repository.find_by_asset_code(
            "CH-001"
        )
    )

    assert persisted is not None
    assert persisted.layer_code == "hvac"


def test_should_reject_unknown_map_layer() -> None:
    asset_repository = FakeAssetRepository()
    map_repository = FakeMapLocationRepository()
    layer_repository = InMemoryMapLayerRepository()
    plan_repository = InMemoryMapPlanRepository()

    plan_repository.save(
        MapPlan(
            code="ground_floor",
            name="Planta Baja",
            order=10,
            is_active=True,
        )
    )

    layer_repository.save(
        MapLayer(
            code="electrical",
            name="Electrico",
            order=10,
            is_active=True,
        )
    )

    asset_repository.save(
        create_asset(
            code="CH-001",
            name="Chiller 1",
        )
    )

    use_case = PlaceAssetOnMap(
        asset_repository,
        map_repository,
        layer_repository,
        plan_repository,
    )

    result = use_case.execute(
        PlaceAssetOnMapCommand(
            asset_code="CH-001",
            category="chiller",
            x=25.0,
            y=30.0,
            layer_code="hvac",
        )
    )

    assert result.success is False
    assert result.location is None
    assert result.message == (
        "No existe la capa indicada."
    )
    assert map_repository.find_all() == []


def test_should_reject_inactive_map_layer() -> None:
    asset_repository = FakeAssetRepository()
    map_repository = FakeMapLocationRepository()
    layer_repository = InMemoryMapLayerRepository()
    plan_repository = InMemoryMapPlanRepository()

    plan_repository.save(
        MapPlan(
            code="ground_floor",
            name="Planta Baja",
            order=10,
            is_active=True,
        )
    )

    layer_repository.save(
        MapLayer(
            code="hvac",
            name="HVAC",
            order=20,
            is_active=False,
        )
    )

    asset_repository.save(
        create_asset(
            code="CH-001",
            name="Chiller 1",
        )
    )

    use_case = PlaceAssetOnMap(
        asset_repository,
        map_repository,
        layer_repository,
        plan_repository,
    )

    result = use_case.execute(
        PlaceAssetOnMapCommand(
            asset_code="CH-001",
            category="chiller",
            x=25.0,
            y=30.0,
            layer_code="hvac",
        )
    )

    assert result.success is False
    assert result.location is None
    assert result.message == (
        "La capa indicada no esta activa."
    )
    assert map_repository.find_all() == []
def test_should_place_asset_in_explicit_plan() -> None:
    (
        use_case,
        asset_repository,
        map_repository,
    ) = create_use_case()

    asset_repository.save(
        create_asset(
            code="CH-ROOF-001",
            name="Chiller en techo",
        )
    )

    result = use_case.execute(
        PlaceAssetOnMapCommand(
            asset_code="CH-ROOF-001",
            category="chiller",
            x=25.0,
            y=30.0,
            layer_code="hvac",
            plan_code="roof",
        )
    )

    assert result.success is True
    assert result.location is not None
    assert result.location.layer_code == "hvac"
    assert result.location.plan_code == "roof"

    persisted = (
        map_repository.find_by_asset_code(
            "CH-ROOF-001"
        )
    )

    assert persisted is not None
    assert persisted.layer_code == "hvac"
    assert persisted.plan_code == "roof"


def test_should_reject_unknown_map_plan() -> None:
    asset_repository = FakeAssetRepository()
    map_repository = FakeMapLocationRepository()
    layer_repository = InMemoryMapLayerRepository()
    plan_repository = InMemoryMapPlanRepository()

    layer_repository.save(
        MapLayer(
            code="hvac",
            name="HVAC",
            order=20,
            is_active=True,
        )
    )

    plan_repository.save(
        MapPlan(
            code="ground_floor",
            name="Planta Baja",
            order=10,
            is_active=True,
        )
    )

    asset_repository.save(
        create_asset(
            code="CH-001",
            name="Chiller 1",
        )
    )

    use_case = PlaceAssetOnMap(
        asset_repository,
        map_repository,
        layer_repository,
        plan_repository,
    )

    result = use_case.execute(
        PlaceAssetOnMapCommand(
            asset_code="CH-001",
            category="chiller",
            x=25.0,
            y=30.0,
            layer_code="hvac",
            plan_code="roof",
        )
    )

    assert result.success is False
    assert result.location is None
    assert result.message == (
        "No existe el plano indicado."
    )
    assert map_repository.find_all() == []


def test_should_reject_inactive_map_plan() -> None:
    asset_repository = FakeAssetRepository()
    map_repository = FakeMapLocationRepository()
    layer_repository = InMemoryMapLayerRepository()
    plan_repository = InMemoryMapPlanRepository()

    layer_repository.save(
        MapLayer(
            code="hvac",
            name="HVAC",
            order=20,
            is_active=True,
        )
    )

    plan_repository.save(
        MapPlan(
            code="roof",
            name="Techo",
            order=30,
            is_active=False,
        )
    )

    asset_repository.save(
        create_asset(
            code="CH-001",
            name="Chiller 1",
        )
    )

    use_case = PlaceAssetOnMap(
        asset_repository,
        map_repository,
        layer_repository,
        plan_repository,
    )

    result = use_case.execute(
        PlaceAssetOnMapCommand(
            asset_code="CH-001",
            category="chiller",
            x=25.0,
            y=30.0,
            layer_code="hvac",
            plan_code="roof",
        )
    )

    assert result.success is False
    assert result.location is None
    assert result.message == (
        "El plano indicado no esta activo."
    )
    assert map_repository.find_all() == []
