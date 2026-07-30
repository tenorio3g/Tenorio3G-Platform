from datetime import date

from app.domains.assets.entities.asset import Asset
from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
)
from app.domains.assets.use_cases.find_all_assets.find_all_assets import (
    FindAllAssets,
)
from app.domains.assets.use_cases.find_all_assets.query import (
    FindAllAssetsQuery,
)
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)


def create_asset(
    code: str,
    name: str,
) -> Asset:
    return Asset(
        code=code,
        name=name,
        asset_model_code="CHILLER240",
        serial_number=f"SN-{code}",
        location_code="PLANTA_NORTE",
        status=AssetStatus.OPERATING,
        installation_date=date(2025, 1, 10),
    )


def test_should_return_all_assets():

    repository = InMemoryAssetRepository()

    repository.save(
        create_asset(
            code="CH-001",
            name="Chiller Principal",
        )
    )

    repository.save(
        create_asset(
            code="CH-002",
            name="Chiller Secundario",
        )
    )

    use_case = FindAllAssets(repository)

    result = use_case.execute(
        FindAllAssetsQuery()
    )

    assert result.success is True
    assert len(result.assets) == 2
    assert result.assets[0].code == "CH-001"
    assert result.assets[1].code == "CH-002"
    assert result.message == "Se encontraron 2 activos."


def test_should_return_success_with_empty_list_when_no_assets_exist():

    repository = InMemoryAssetRepository()

    use_case = FindAllAssets(repository)

    result = use_case.execute(
        FindAllAssetsQuery()
    )

    assert result.success is True
    assert result.assets == []
    assert result.message == "No hay activos registrados."


def test_should_return_singular_message_when_one_asset_exists():

    repository = InMemoryAssetRepository()

    repository.save(
        create_asset(
            code="CH-001",
            name="Chiller Principal",
        )
    )

    use_case = FindAllAssets(repository)

    result = use_case.execute(
        FindAllAssetsQuery()
    )

    assert result.success is True
    assert len(result.assets) == 1
    assert result.message == "Se encontró 1 activo."