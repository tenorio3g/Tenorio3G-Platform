# ==========================================================
# T3G-FND-012
#
# Element   : Empty State ViewModel
# Module    : Foundation UI
# Version   : 0.1.0
# Status    : Development
# Sprint    : FND-012
#
# Purpose
# -------
# Contrato de presentación para representar estados
# vacíos dentro de Foundation UI.
#
# ==========================================================

from dataclasses import dataclass


@dataclass(slots=True)
class EmptyStateViewModel:
    """
    Modelo de presentación para un estado vacío.

    Puede reutilizarse en cualquier módulo de
    Tenorio3G Platform.
    """

    icon: str = "📭"

    title: str = "Sin información"

    description: str = (
        "No existen elementos para mostrar."
    )

    action_label: str = ""

    action_url: str = ""

    show_action: bool = False