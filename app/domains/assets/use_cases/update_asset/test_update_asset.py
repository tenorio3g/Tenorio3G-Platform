from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
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


def test_should_update_asset():

    repository = InMemoryAssetRepository()
    repository.save(create_asset())

    use_case = UpdateAsset(repository)

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

    use_case = UpdateAsset(repository)

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

    use_case = UpdateAsset(repository)

    result = use_case.execute(
        UpdateAssetCommand(
            code="UNKNOWN",
            name="Activo inexistente",
        )
    )

    assert result.success is False
    assert result.asset is None
    assert result.message == "No existe un activo con ese código."