# ==========================================================
# T3G-FND-005
#
# Element   : Components Registry
# Module    : Foundation UI
# Version   : 0.2.0
# Status    : Development
# Sprint    : FND-005.2
#
# Purpose
# -------
# Define el catálogo oficial de componentes compuestos
# disponibles dentro del T3G Framework.
#
# ==========================================================

from .enums import RegistryCategory, RegistryStatus
from .metadata import ComponentMetadata


COMPONENTS = (
    ComponentMetadata(
        id="timeline",
        name="Timeline",
        description=(
            "Componente para representar eventos "
            "cronológicos."
        ),
        category=RegistryCategory.COMPONENT,
        version="1.0.0",
        status=RegistryStatus.STABLE,
        since="0.1.0",
        owner="Foundation",
        depends_on=(
            "panel",
            "badge",
        ),
    ),
    ComponentMetadata(
        id="hero-panel",
        name="Hero Panel",

        description=(
            "Encabezado principal utilizado para mostrar "
            "información resumida de una entidad."
        ),

        category=RegistryCategory.COMPONENT,

        version="0.1.0",

        status=RegistryStatus.DEVELOPMENT,

        since="0.2.0",

        owner="Foundation",

        template="components/foundation/hero_panel.html",

        stylesheet="foundation/hero_panel.css",

        viewmodel="HeroPanelViewModel",

        documentation="docs/foundation/components/hero_panel.md",

        tags=(
            "layout",
            "dashboard",
            "header",
        ),

        depends_on=(
            "panel",
            "badge",
            "progress",
            "button",
        ),
    ),



    ComponentMetadata(
        id="kpi-card",
        name="KPI Card",
        description=(
            "Tarjeta para mostrar indicadores clave."
        ),
        category=RegistryCategory.COMPONENT,
        status=RegistryStatus.PENDING,
        owner="Foundation",
        depends_on=(
            "panel",
        ),
    ),
)