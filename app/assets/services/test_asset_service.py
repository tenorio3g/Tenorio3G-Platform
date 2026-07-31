from app.assets.services.asset_service import AssetService


def test_get_assets():
    assets = AssetService.get_assets()

    assert len(assets) == 1
    assert assets[0].codigo == "S2-480-ES09-T269"
    assert assets[0].nombre == "TABLERO GENERAL ES09"