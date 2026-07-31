from app.assets.presenters import AssetPresenter
from app.domains.assets.bootstrap import repository


def test_present_asset():
    asset = repository.find_all()[0]

    view = AssetPresenter.present(asset)

    assert view.codigo == asset.code
    assert view.nombre == asset.name
    assert view.ubicacion == asset.location_code

    assert view.estado in {
        "Operando",
        "Advertencia",
        "Falla",
        "Fuera de servicio",
    }

    assert view.area is None
    assert view.ultimo_mantenimiento is None
    assert view.proximo_mantenimiento is None
    assert view.salud is None