from datetime import date

from app.domains.assets.entities.asset_model import AssetModel
from app.domains.assets.repositories.in_memory_asset_model_repository import (
    InMemoryAssetModelRepository,
)
from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
)
from app.domains.locations.entities.physical_location import (
    PhysicalLocation,
)
from app.domains.locations.repositories.in_memory_physical_location_repository import (
    InMemoryPhysicalLocationRepository,
)

from .command import RegisterAssetCommand
from .register_asset import RegisterAsset


def create_location_repository():
    repository = (
        InMemoryPhysicalLocationRepository()
    )

    repository.save(
        PhysicalLocation(
            code="PLANTA_NORTE",
            name="Planta Norte",
            area="PLANTA",
        )
    )

    return repository


def test_should_register_asset_successfully():

    asset_repository = InMemoryAssetRepository()
    asset_model_repository = (
        InMemoryAssetModelRepository()
    )
    location_repository = (
        create_location_repository()
    )

    asset_model = AssetModel(
        code="CHILLER240",
        name="Carrier Chiller",
        model_number="30XA-240",
        manufacturer_code="CARRIER",
        asset_type_code="CHILLER",
        description="Chiller Carrier",
        specifications={
            "voltaje": "480 V",
        },
    )

    asset_model_repository.save(
        asset_model
    )

    command = RegisterAssetCommand(
        code="CH-001",
        name="Chiller Principal",
        asset_model_code="CHILLER240",
        serial_number="SN-987654",
        location_code="PLANTA_NORTE",
        status="OPERATING",
        installation_date=date(
            2025,
            1,
            15,
        ),
    )

    use_case = RegisterAsset(
        asset_repository,
        asset_model_repository,
        location_repository,
    )

    result = use_case.execute(
        command
    )

    assert result.success is True
    assert result.asset is not None
    assert result.asset.code == "CH-001"
    assert (
        result.asset.asset_model_code
        == "CHILLER240"
    )
    assert (
        result.asset.location_code
        == "PLANTA_NORTE"
    )


def test_should_fail_when_asset_code_already_exists():

    asset_repository = InMemoryAssetRepository()
    asset_model_repository = (
        InMemoryAssetModelRepository()
    )
    location_repository = (
        create_location_repository()
    )

    asset_model = AssetModel(
        code="CHILLER240",
        name="Carrier Chiller",
        model_number="30XA-240",
        manufacturer_code="CARRIER",
        asset_type_code="CHILLER",
        description="Chiller Carrier",
        specifications={},
    )

    asset_model_repository.save(
        asset_model
    )

    use_case = RegisterAsset(
        asset_repository,
        asset_model_repository,
        location_repository,
    )

    command = RegisterAssetCommand(
        code="CH-001",
        name="Chiller Principal",
        asset_model_code="CHILLER240",
        serial_number="SN-111",
        location_code="PLANTA_NORTE",
        status="OPERATING",
        installation_date=date.today(),
    )

    use_case.execute(
        command
    )

    result = use_case.execute(
        command
    )

    assert result.success is False
    assert (
        result.message
        == "Ya existe un activo con ese código."
    )


def test_should_fail_when_asset_model_does_not_exist():

    asset_repository = InMemoryAssetRepository()
    asset_model_repository = (
        InMemoryAssetModelRepository()
    )
    location_repository = (
        create_location_repository()
    )

    command = RegisterAssetCommand(
        code="CH-001",
        name="Chiller Principal",
        asset_model_code="MODEL_NOT_FOUND",
        serial_number="SN-111",
        location_code="PLANTA_NORTE",
        status="OPERATING",
        installation_date=date.today(),
    )

    use_case = RegisterAsset(
        asset_repository,
        asset_model_repository,
        location_repository,
    )

    result = use_case.execute(
        command
    )

    assert result.success is False
    assert (
        result.message
        == "No existe el modelo de activo indicado."
    )


def test_should_fail_when_physical_location_does_not_exist():

    asset_repository = InMemoryAssetRepository()
    asset_model_repository = (
        InMemoryAssetModelRepository()
    )
    location_repository = (
        InMemoryPhysicalLocationRepository()
    )

    asset_model_repository.save(
        AssetModel(
            code="CHILLER240",
            name="Carrier Chiller",
            model_number="30XA-240",
            manufacturer_code="CARRIER",
            asset_type_code="CHILLER",
            description="Chiller Carrier",
            specifications={},
        )
    )

    use_case = RegisterAsset(
        asset_repository,
        asset_model_repository,
        location_repository,
    )

    command = RegisterAssetCommand(
        code="CH-001",
        name="Chiller Principal",
        asset_model_code="CHILLER240",
        serial_number="SN-111",
        location_code="LOCATION_NOT_FOUND",
        status="OPERATING",
        installation_date=date.today(),
    )

    result = use_case.execute(
        command
    )

    assert result.success is False
    assert result.asset is None
    assert (
        result.message
        == "No existe la ubicación física indicada."
    )

    assert (
        asset_repository.find_by_code(
            "CH-001"
        )
        is None
    )
