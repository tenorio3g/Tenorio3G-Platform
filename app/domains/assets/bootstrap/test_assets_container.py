from app.domains.assets.bootstrap import (
    get_asset_life_sheet,
    repository,
)

from app.domains.assets.use_cases.get_asset_life_sheet.query import (
    GetAssetLifeSheetQuery,
)


def test_bootstrap_loaded():

    assets = repository.find_all()

    assert len(assets) == 1
    assert assets[0].code == "S2-480-ES09-T269"


def test_container_should_get_asset_life_sheet():

    result = get_asset_life_sheet.execute(
        GetAssetLifeSheetQuery(
            code="S2-480-ES09-T269",
        )
    )

    assert result.success is True
    assert result.asset is not None
    assert result.asset_model is not None