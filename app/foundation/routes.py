# ==========================================================
# T3G-FND-004
#
# Component : Foundation Lab Routes
# Module    : Foundation UI
# Version   : 0.1.0
# Status    : Development
# Sprint    : UI-004
#
# Purpose
# -------
# Proporciona los datos de demostración utilizados por
# Foundation Lab para probar componentes reutilizables.
#
# ==========================================================
from app.foundation.services.showcase_service import (
    FoundationShowcaseService,
)

from app.foundation.services import (
    ComponentDetailService,
    FoundationExplorerService,
)
from flask import (
    Blueprint,
    render_template,
    request,
)

from app.foundation import foundation
from app.foundation.registry import COMPONENTS, PRIMITIVES
from app.foundation.viewmodels import (
    HeroPanelAction,
    HeroPanelBadge,
    HeroPanelDetail,
    HeroPanelViewModel,
)



@foundation.route("/showcase")
def showcase():
    """
    Catálogo visual de componentes Foundation.
    """

    showcase_service = FoundationShowcaseService()

    sections = showcase_service.build()

    return render_template(
        "foundation/showcase.html",
        sections=sections,
    )





@foundation.route("/")
def playground():
    """
    Muestra el laboratorio visual de Foundation UI.

    Esta pantalla permite desarrollar, probar y documentar
    componentes independientes de los dominios de negocio.
    """

    foundation_version = "1.0.0"


    hero = HeroPanelViewModel(
        title="TABLERO GENERAL ES09",
        subtitle="S2-480-ES09-T269",
        badge=HeroPanelBadge(
            text="Operando",
            variant="success",
        ),
        progress=84,
        progress_label="Salud del activo",
        details=[
            HeroPanelDetail(
                label="Área",
                value="Producción",
            ),
            HeroPanelDetail(
                label="Ubicación",
                value="Subestación Norte",
            ),
            HeroPanelDetail(
                label="Último mantenimiento",
                value="18 Junio 2026",
            ),
            HeroPanelDetail(
                label="Próximo mantenimiento",
                value="18 Septiembre 2026",
            ),
        ],
        actions=[
            HeroPanelAction(
                label="Ver detalles",
                url="#",
            ),
        ],
    )


    return render_template(
        "foundation/playground.html",
        foundation_version=foundation_version,
        primitives=PRIMITIVES,
        components=COMPONENTS,
        hero=hero,
    )



@foundation.route("/explorer")
def explorer():
    search = request.args.get(
        "q",
        "",
    ).strip()

    explorer_service = FoundationExplorerService()

    explorer_view = explorer_service.build(
        framework_version="1.0.0",
        search=search,
    )

    return render_template(
        "foundation/explorer.html",
        explorer=explorer_view,
    )
@foundation.route("/explorer/<string:component_id>")
def explorer_detail(component_id: str):

    detail_service = ComponentDetailService()

    component = detail_service.build(component_id)

    if component is None:
        abort(404)

    return render_template(
        "foundation/explorer_detail.html",
        component=component,
    )


@foundation.route("/dashboard")
def dashboard():

    from app.foundation.services import (
        RegistryIntelligenceService,
    )

    intelligence = RegistryIntelligenceService()

    statistics = intelligence.statistics()

    return render_template(
        "foundation/dashboard.html",
        statistics=statistics,
    )