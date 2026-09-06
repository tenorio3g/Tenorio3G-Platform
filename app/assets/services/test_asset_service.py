from app.assets.services.asset_service import AssetService


def test_get_assets():
    assets = AssetService.get_assets()

    asset = next(
        (
            item
            for item in assets
            if item.codigo == "S2-480-ES09-T269"
        ),
        None,
    )

    assert asset is not None
    assert asset.nombre == "TABLERO GENERAL ES09"
