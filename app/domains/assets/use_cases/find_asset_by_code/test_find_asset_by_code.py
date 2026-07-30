from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
)
from app.domains.assets.use_cases.find_asset_by_code.find_asset_by_code import (
    FindAssetByCode,
)
from app.domains.assets.use_cases.find_asset_by_code.query import (
    FindAssetByCodeQuery,
)
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)


def test_should_find_asset_by_code():

    repository = InMemoryAssetRepository()

    asset = Asset(
        code="CH-001",
        name="Chiller Principal",
        asset_model_code="CHILLER240",
        serial_number="SN123456",
        location_code="PLANTA_NORTE",
        status=AssetStatus.OPERATING,
        installation_date=date(2025, 1, 10),
    )

    repository.save(asset)

    use_case = FindAssetByCode(repository)

    result = use_case.execute(
        FindAssetByCodeQuery(
            code="CH-001",
        )
    )

    assert result.success is True
    assert result.asset is not None
    assert result.asset.code == "CH-001"


def test_should_fail_when_asset_does_not_exist():

    repository = InMemoryAssetRepository()

    use_case = FindAssetByCode(repository)

    result = use_case.execute(
        FindAssetByCodeQuery(
            code="UNKNOWN",
        )
    )

    assert result.success is False
    assert result.asset is None
    assert result.message == "No existe un activo con ese código."