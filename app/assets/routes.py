from flask import render_template, request

from . import assets
from app.assets.repositories.asset_repository import AssetRepository


repository = AssetRepository()


@assets.route("/activos")
def index():
    """
    Pantalla principal del módulo Assets.
    """

    termino_busqueda = request.args.get(
        "buscar",
        ""
    ).strip()

    if termino_busqueda:
        activos = repository.buscar(termino_busqueda)
    else:
        activos = repository.obtener_todos()

    return render_template(
        "pages/assets_index.html",
        activos=activos,
        termino_busqueda=termino_busqueda,
    )


@assets.route("/activo/<string:codigo>")
def asset_detail(codigo: str):
    """
    Muestra la Hoja de Vida del activo.
    """

    activo = repository.obtener_por_codigo(codigo)

    if activo is None:
        return (
            render_template(
                "pages/asset_not_found.html",
                codigo=codigo,
            ),
            404,
        )

    return render_template(
        "pages/asset_detail.html",
        activo=activo,
    )