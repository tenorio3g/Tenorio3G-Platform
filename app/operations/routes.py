from flask import render_template

from . import operations
from app.operations.services.operations_service import OperationsService


@operations.route("/operaciones")
def index():

    service = OperationsService()

    resumen = service.resumen()
    metricas = service.obtener_metricas()
    ordenes_recientes = service.obtener_ordenes_recientes()
    activos_en_riesgo = service.obtener_activos_en_riesgo()
    tecnicos = service.obtener_tecnicos()

    return render_template(
        "pages/operations_dashboard.html",
        resumen=resumen,
        metricas=metricas,
        ordenes_recientes=ordenes_recientes,
        activos_en_riesgo=activos_en_riesgo,
        tecnicos=tecnicos
    )