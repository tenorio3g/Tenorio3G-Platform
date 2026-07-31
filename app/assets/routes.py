from flask import render_template, request

from . import assets
from app.assets.services.asset_service import AssetService
from app.domains.assets.bootstrap import (
    get_asset_life_sheet,
)

from app.domains.assets.use_cases.get_asset_life_sheet.query import (
    GetAssetLifeSheetQuery,
)

from app.assets.presenters.asset_life_sheet_presenter import (
    AssetLifeSheetPresenter,
)


@assets.route("/activos")
def index():
    """
    Pantalla principal del módulo Assets.
    """

    activos = AssetService.get_assets()

    return render_template(
        "pages/assets_index.html",
        activos=activos,
        termino_busqueda="",
    )


@assets.route("/activo/<string:codigo>")
def asset_detail(codigo: str):
    """
    Muestra la Hoja de Vida del activo.
    """

    result = get_asset_life_sheet.execute(
        GetAssetLifeSheetQuery(
            code=codigo,
        )
    )

    if not result.success:

        return (
            render_template(
                "pages/asset_not_found.html",
                codigo=codigo,
            ),
            404,
        )

    activo = AssetLifeSheetPresenter.present(
        asset=result.asset,
        asset_model=result.asset_model,
    )

    return render_template(
        "pages/asset_detail.html",
        activo=activo,
    )