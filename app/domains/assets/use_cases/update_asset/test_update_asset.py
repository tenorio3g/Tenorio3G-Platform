from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.entities.asset_model import AssetModel
from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
)
from app.domains.assets.repositories.in_memory_asset_model_repository import (
    InMemoryAssetModelRepository,
)
from app.domains.assets.use_cases.update_asset.command import (
    UpdateAssetCommand,
)
from app.domains.assets.use_cases.update_asset.update_asset import (
    UpdateAsset,
)
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)
from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)
from app.domains.locations.repositories.in_memory_physical_location_repository import (
    InMemoryPhysicalLocationRepository,
)


def create_asset() -> Asset:
    return Asset(
        code="CH-001",
        name="Chiller Principal",
        asset_model_code="CHILLER240",
        serial_number="SN-ORIGINAL",
        location_code="PLANTA_NORTE",
        status=AssetStatus.OPERATING,
        installation_date=date(2025, 1, 10),
    )


def create_asset_model(
    code: str = "CHILLER480",
) -> AssetModel:
    return AssetModel(
        code=code,
        name="Chiller Test",
        model_number="TEST-480",
        asset_type_code="CHILLER",
        manufacturer_code="TEST",
    )


def create_physical_location(
    code: str = "PLANTA_SUR",
) -> PhysicalLocation:
    return PhysicalLocation(
        code=code,
        name="Planta Sur",
        area="PRODUCCION",
    )


def test_should_update_asset():

    repository = InMemoryAssetRepository()
    repository.save(create_asset())

    model_repository = InMemoryAssetModelRepository()
    model_repository.save(create_asset_model())

    location_repository = InMemoryPhysicalLocationRepository()
    location_repository.save(create_physical_location())

    use_case = UpdateAsset(
        repository,
        model_repository,
        location_repository,
    )

    result = use_case.execute(
        UpdateAssetCommand(
            code="CH-001",
            name="Chiller de Producción",
            serial_number="SN-ACTUALIZADO",
            location_code="PLANTA_SUR",
            status=AssetStatus.MAINTENANCE,
        )
    )

    assert result.success is True
    assert result.asset is not None
    assert result.asset.code == "CH-001"
    assert result.asset.name == "Chiller de Producción"
    assert result.asset.serial_number == "SN-ACTUALIZADO"
    assert result.asset.location_code == "PLANTA_SUR"
    assert result.asset.status == AssetStatus.MAINTENANCE
    assert result.message == "Activo actualizado correctamente."


def test_should_update_only_provided_fields():

    repository = InMemoryAssetRepository()
    repository.save(create_asset())

    model_repository = InMemoryAssetModelRepository()
    model_repository.save(create_asset_model())

    location_repository = InMemoryPhysicalLocationRepository()
    location_repository.save(
        create_physical_location(
            code="ALMACEN_MANTENIMIENTO",
        )
    )

    use_case = UpdateAsset(
        repository,
        model_repository,
        location_repository,
    )

    result = use_case.execute(
        UpdateAssetCommand(
            code="CH-001",
            location_code="ALMACEN_MANTENIMIENTO",
        )
    )

    assert result.success is True
    assert result.asset is not None

    assert result.asset.name == "Chiller Principal"
    assert result.asset.serial_number == "SN-ORIGINAL"
    assert result.asset.location_code == "ALMACEN_MANTENIMIENTO"
    assert result.asset.status == AssetStatus.OPERATING


def test_should_fail_when_asset_does_not_exist():

    repository = InMemoryAssetRepository()

    model_repository = InMemoryAssetModelRepository()
    model_repository.save(create_asset_model())

    location_repository = InMemoryPhysicalLocationRepository()
    location_repository.save(create_physical_location())

    use_case = UpdateAsset(
        repository,
        model_repository,
        location_repository,
    )

    result = use_case.execute(
        UpdateAssetCommand(
            code="UNKNOWN",
            name="Activo inexistente",
        )
    )

    assert result.success is False
    assert result.asset is None
    assert result.message == "No existe un activo con ese código."

def test_should_update_asset_model_and_installation_date():

    repository = InMemoryAssetRepository()
    repository.save(create_asset())

    model_repository = InMemoryAssetModelRepository()
    model_repository.save(create_asset_model())

    location_repository = InMemoryPhysicalLocationRepository()
    location_repository.save(create_physical_location())

    use_case = UpdateAsset(
        repository,
        model_repository,
        location_repository,
    )

    result = use_case.execute(
        UpdateAssetCommand(
            code="CH-001",
            asset_model_code="CHILLER480",
            installation_date=date(2026, 8, 15),
        )
    )

    assert result.success is True
    assert result.asset is not None
    assert result.asset.code == "CH-001"
    assert result.asset.asset_model_code == "CHILLER480"
    assert (
        result.asset.installation_date
        == date(2026, 8, 15)
    )



def test_should_fail_when_new_asset_model_does_not_exist():

    repository = InMemoryAssetRepository()
    repository.save(create_asset())

    model_repository = InMemoryAssetModelRepository()
    model_repository.save(create_asset_model())

    location_repository = InMemoryPhysicalLocationRepository()
    location_repository.save(create_physical_location())

    use_case = UpdateAsset(
        repository,
        model_repository,
        location_repository,
    )

    result = use_case.execute(
        UpdateAssetCommand(
            code="CH-001",
            asset_model_code="MODEL-UNKNOWN",
        )
    )

    assert result.success is False
    assert result.asset is not None
    assert result.asset.asset_model_code == "CHILLER240"
    assert (
        result.message
        == "No existe el modelo de activo indicado."
    )

def test_should_fail_when_new_location_does_not_exist():

    repository = InMemoryAssetRepository()
    repository.save(create_asset())

    model_repository = InMemoryAssetModelRepository()
    model_repository.save(create_asset_model())

    location_repository = InMemoryPhysicalLocationRepository()
    location_repository.save(create_physical_location())

    use_case = UpdateAsset(
        repository,
        model_repository,
        location_repository,
    )

    result = use_case.execute(
        UpdateAssetCommand(
            code="CH-001",
            location_code="LOCATION-UNKNOWN",
        )
    )

    assert result.success is False
    assert result.asset is not None
    assert result.asset.location_code == "PLANTA_NORTE"
    assert (
        result.message
        == "No existe la ubicación física indicada."
    )
