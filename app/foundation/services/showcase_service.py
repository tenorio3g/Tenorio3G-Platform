# ==========================================================
# T3G-FND-015
#
# Service   : Foundation Showcase
# Module    : Foundation UI
# Version   : 0.2.0
# Status    : Development
#
# Purpose
# -------
# Construye el ViewModel principal del
# Foundation Showcase.
#
# ==========================================================

from app.foundation.viewmodels import (
    FoundationShowcaseViewModel,
    ShowcaseSectionViewModel,
)


class FoundationShowcaseService:
    """
    Construye el catálogo visual del Foundation.
    """

    def build(self) -> FoundationShowcaseViewModel:

        sections = (

            ShowcaseSectionViewModel(
                title="Hero Panel",
                description="Encabezados principales reutilizables.",
                component_name="hero_panel",
                anchor="hero-panel",
            ),

            ShowcaseSectionViewModel(
                title="Badge",
                description="Indicadores de estado.",
                component_name="badge",
                anchor="badge",
            ),

            ShowcaseSectionViewModel(
                title="Search Box",
                description="Buscador reutilizable.",
                component_name="search_box",
                anchor="search-box",
            ),

            ShowcaseSectionViewModel(
                title="KPI Card",
                description="Indicadores numéricos.",
                component_name="kpi_card",
                anchor="kpi-card",
            ),

            ShowcaseSectionViewModel(
                title="Empty State",
                description="Estados vacíos.",
                component_name="empty_state",
                anchor="empty-state",
            ),

            ShowcaseSectionViewModel(
                title="Alert",
                description="Mensajes reutilizables.",
                component_name="alert",
                anchor="alert",
            ),

        )

        return FoundationShowcaseViewModel(

            title="Foundation Showcase",

            subtitle=(
                "Catálogo oficial de componentes "
                "reutilizables del Foundation."
            ),

            sections=sections,
        )