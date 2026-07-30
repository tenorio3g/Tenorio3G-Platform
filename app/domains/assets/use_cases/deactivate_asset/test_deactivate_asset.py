from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
)
from app.domains.assets.use_cases.deactivate_asset.command import (
    DeactivateAssetCommand,
)
from app.domains.assets.use_cases.deactivate_asset.deactivate_asset import (
    DeactivateAsset,
)
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)


def create_active_asset() -> Asset:

    return Asset(
        code="CH-001",
        name="Chiller Principal",
        asset_model_code="CHILLER240",
        serial_number="SN-001",
        location_code="PLANTA_NORTE",
        status=AssetStatus.OPERATING,
        installation_date=date(2025, 1, 10),
    )


def test_should_deactivate_asset():

    repository = InMemoryAssetRepository()
    repository.save(create_active_asset())

    use_case = DeactivateAsset(repository)

    result = use_case.execute(
        DeactivateAssetCommand(
            code="CH-001",
            reason="Compresor principal dañado.",
        )
    )

    assert result.success is True
    assert result.asset is not None
    assert result.asset.is_out_of_service()
    assert (
        result.asset.deactivation_reason
        == "Compresor principal dañado."
    )
    assert result.message == "Activo desactivado correctamente."


def test_should_remove_extra_spaces_from_reason():

    repository = InMemoryAssetRepository()
    repository.save(create_active_asset())

    use_case = DeactivateAsset(repository)

    result = use_case.execute(
        DeactivateAssetCommand(
            code="CH-001",
            reason="   Falla eléctrica en el tablero.   ",
        )
    )

    assert result.success is True
    assert result.asset is not None
    assert result.asset.is_out_of_service()
    assert (
        result.asset.deactivation_reason
        == "Falla eléctrica en el tablero."
    )


def test_should_fail_when_reason_is_empty():

    repository = InMemoryAssetRepository()
    repository.save(create_active_asset())

    use_case = DeactivateAsset(repository)

    result = use_case.execute(
        DeactivateAssetCommand(
            code="CH-001",
            reason="     ",
        )
    )

    assert result.success is False
    assert result.asset is not None
    assert result.asset.is_operating()
    assert result.asset.deactivation_reason is None
    assert (
        result.message
        == "El motivo de desactivación es obligatorio."
    )


def test_should_fail_when_asset_is_already_inactive():

    repository = InMemoryAssetRepository()

    asset = create_active_asset()

    asset.deactivate(
        "Equipo enviado a reparación externa."
    )

    repository.save(asset)

    use_case = DeactivateAsset(repository)

    result = use_case.execute(
        DeactivateAssetCommand(
            code="CH-001",
            reason="Otro motivo.",
        )
    )

    assert result.success is False
    assert result.asset is not None
    assert result.asset.is_out_of_service()
    assert (
        result.asset.deactivation_reason
        == "Equipo enviado a reparación externa."
    )
    assert (
        result.message
        == "El activo ya se encuentra desactivado."
    )


def test_should_fail_when_asset_does_not_exist():

    repository = InMemoryAssetRepository()

    use_case = DeactivateAsset(repository)

    result = use_case.execute(
        DeactivateAssetCommand(
            code="UNKNOWN",
            reason="No importa.",
        )
    )

    assert result.success is False
    assert result.asset is None
    assert (
        result.message
        == "No existe un activo con ese código."
    )