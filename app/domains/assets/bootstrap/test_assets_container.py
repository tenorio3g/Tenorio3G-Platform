from app.domains.assets.bootstrap import repository


def test_bootstrap_loaded():

    assets = repository.find_all()

    assert len(assets) == 1

    assert assets[0].code == "S2-480-ES09-T269"