from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.entities.asset_model import AssetModel

from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
)
from app.domains.assets.repositories.in_memory_asset_model_repository import (
    InMemoryAssetModelRepository,
)

from app.domains.assets.use_cases.find_asset_by_code.find_asset_by_code import (
    FindAssetByCode,
)
from app.domains.assets.use_cases.find_asset_model_by_code.find_asset_model_by_code import (
    FindAssetModelByCode,
)

from app.domains.assets.use_cases.get_asset_life_sheet.get_asset_life_sheet import (
    GetAssetLifeSheet,
)
from app.domains.assets.use_cases.get_asset_life_sheet.query import (
    GetAssetLifeSheetQuery,
)

from app.domains.assets.value_objects.asset_status import AssetStatus


def test_should_get_asset_life_sheet():

    asset_repository = InMemoryAssetRepository()
    asset_model_repository = InMemoryAssetModelRepository()

    asset_model = AssetModel(
        code="CHILLER240",
        name="Carrier AquaForce",
        model_number="30XA-120",
        asset_type_code="CHILLER",
        manufacturer_code="CARRIER",
    )

    asset = Asset(
        code="CH-001",
        name="Chiller Principal",
        asset_model_code="CHILLER240",
        serial_number="SN123456",
        location_code="PLANTA_NORTE",
        status=AssetStatus.OPERATING,
        installation_date=date(2025, 1, 10),
    )

    asset_model_repository.save(asset_model)
    asset_repository.save(asset)

    find_asset = FindAssetByCode(asset_repository)
    find_asset_model = FindAssetModelByCode(asset_model_repository)

    use_case = GetAssetLifeSheet(
        find_asset,
        find_asset_model,
    )

    result = use_case.execute(
        GetAssetLifeSheetQuery(
            code="CH-001",
        )
    )

    assert result.success is True
    assert result.asset is not None
    assert result.asset_model is not None

    assert result.asset.code == "CH-001"
    assert result.asset_model.code == "CHILLER240"