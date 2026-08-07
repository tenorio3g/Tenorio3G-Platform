from flask import jsonify, redirect, render_template, request, url_for

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

from app.assets.presenters.asset_api_presenter import (
    AssetApiPresenter,
)

from app.domains.assets.technical_data.bootstrap import (
    get_technical_data,
    save_technical_data,
)
from app.domains.assets.technical_data.use_cases.save_technical_data import (
    SaveTechnicalDataCommand,
)
from app.domains.assets.technical_data.use_cases.get_technical_data import (
    GetTechnicalDataQuery,
)


from app.assets.presenters.technical_data_presenter import (
    TechnicalDataPresenter,
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

    technical_result = get_technical_data.execute(
        GetTechnicalDataQuery(
            asset_code=codigo,
        )
    )

    technical_data = None

    if technical_result.success:
        technical_data = TechnicalDataPresenter.present(
            technical_result.technical_data,
        )

    return render_template(
        "pages/asset_detail.html",
        activo=activo,
        technical_data=technical_data,
    )

@assets.get("/assets/api/<string:codigo>")
def asset_api(codigo: str):
    """
    Devuelve la Hoja de Vida del activo en formato JSON.
    """

    result = get_asset_life_sheet.execute(
        GetAssetLifeSheetQuery(
            code=codigo,
        )
    )

    if not result.success:
        return (
            jsonify(
                {
                    "success": False,
                    "message": result.message,
                    "codigo": codigo,
                }
            ),
            404,
        )

    view_model = AssetLifeSheetPresenter.present(
        asset=result.asset,
        asset_model=result.asset_model,
    )

    payload = AssetApiPresenter.present(
        view_model,
    )

    return jsonify(payload)

@assets.route(
    "/activo/<string:codigo>/editar-datos-tecnicos",
    methods=["GET", "POST"],
)
def edit_technical_data(codigo: str):
    """
    Consulta y actualiza los datos técnicos del activo.
    """

    if request.method == "POST":

        result = save_technical_data.execute(
            SaveTechnicalDataCommand(
                asset_code=codigo,
                equipment_type=request.form.get(
                    "equipment_type",
                    "",
                ),
                manufacturer=request.form.get(
                    "manufacturer",
                    "",
                ),
                model=request.form.get(
                    "model",
                    "",
                ),
                serial_number=request.form.get(
                    "serial_number",
                    "",
                ),
                voltage=request.form.get(
                    "voltage",
                    "",
                ),
                phases=request.form.get(
                    "phases",
                    "",
                ),
                frequency=request.form.get(
                    "frequency",
                    "",
                ),
                motor_power=request.form.get(
                    "motor_power",
                    "",
                ),
                observations=request.form.get(
                    "observations",
                    "",
                ),
            )
        )

        if result.success:
            return redirect(
                url_for(
                    "assets.asset_detail",
                    codigo=codigo,
                )
            )

    technical_result = get_technical_data.execute(
        GetTechnicalDataQuery(
            asset_code=codigo,
        )
    )

    technical_data = None

    if technical_result.success:
        technical_data = TechnicalDataPresenter.present(
            technical_result.technical_data,
        )

    return render_template(
        "pages/edit_technical_data.html",
        codigo=codigo,
        technical_data=technical_data,
    )