from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
)
from app.domains.assets.use_cases.activate_asset.activate_asset import (
    ActivateAsset,
)
from app.domains.assets.use_cases.activate_asset.command import (
    ActivateAssetCommand,
)
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)


def create_inactive_asset() -> Asset:
    return Asset(
        code="CH-001",
        name="Chiller Principal",
        asset_model_code="CHILLER240",
        serial_number="SN-001",
        location_code="PLANTA_NORTE",
        status=AssetStatus.OUT_OF_SERVICE,
        installation_date=date(2025, 1, 10),
        deactivation_reason="Compresor principal dañado.",
    )


def test_should_activate_asset():

    repository = InMemoryAssetRepository()
    repository.save(create_inactive_asset())

    use_case = ActivateAsset(repository)

    result = use_case.execute(
        ActivateAssetCommand(
            code="CH-001",
        )
    )

    assert result.success is True
    assert result.asset is not None
    assert result.asset.status == AssetStatus.OPERATING
    assert result.asset.deactivation_reason is None
    assert result.message == "Activo activado correctamente."


def test_should_fail_when_asset_is_already_active():

    repository = InMemoryAssetRepository()

    asset = create_inactive_asset()
    asset.activate()
    repository.save(asset)

    use_case = ActivateAsset(repository)

    result = use_case.execute(
        ActivateAssetCommand(
            code="CH-001",
        )
    )

    assert result.success is False
    assert result.asset is not None
    assert result.asset.status == AssetStatus.OPERATING
    assert result.message == "El activo ya se encuentra activo."


def test_should_fail_when_asset_does_not_exist():

    repository = InMemoryAssetRepository()

    use_case = ActivateAsset(repository)

    result = use_case.execute(
        ActivateAssetCommand(
            code="UNKNOWN",
        )
    )

    assert result.success is False
    assert result.asset is None
    assert result.message == "No existe un activo con ese código."