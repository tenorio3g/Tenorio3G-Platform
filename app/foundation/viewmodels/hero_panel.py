# ==========================================================
# T3G-FND-004
#
# Component : Hero Panel ViewModel
# Module    : Foundation UI
# Version   : 0.1.0
# Status    : Development
# Sprint    : UI-004
#
# Purpose
# -------
# Define el contrato de presentación utilizado por el
# componente reutilizable Hero Panel.
#
# Este archivo no contiene lógica de negocio ni depende
# de los dominios Assets, Work Orders o Inventory.
#
# ==========================================================

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class HeroPanelDetail:
    """
    Representa un dato descriptivo mostrado dentro del Hero Panel.

    Ejemplos:
        Ubicación: Subestación Norte
        Responsable: Daniel
        Próximo mantenimiento: 18 septiembre 2026
    """

    label: str
    value: str


@dataclass(frozen=True)
class HeroPanelAction:
    """
    Representa una acción disponible dentro del Hero Panel.

    La propiedad `variant` corresponde a una variante visual
    de Foundation Buttons, por ejemplo: primary o secondary.
    """

    label: str
    url: str
    variant: str = "primary"


@dataclass(frozen=True)
class HeroPanelBadge:
    """
    Define el estado visual mostrado mediante Foundation Badge.

    Variantes permitidas actualmente:
        success
        warning
        danger
        info
        neutral
    """

    text: str
    variant: str = "neutral"


@dataclass(frozen=True)
class HeroPanelViewModel:
    """
    Contrato de datos del componente Hero Panel.

    Foundation solamente renderiza esta información.
    La transformación desde una entidad de dominio hacia este
    ViewModel será responsabilidad de cada módulo.
    """

    title: str
    subtitle: Optional[str] = None
    badge: Optional[HeroPanelBadge] = None
    progress: Optional[int] = None
    progress_label: Optional[str] = None
    details: list[HeroPanelDetail] = field(default_factory=list)
    actions: list[HeroPanelAction] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Valida exclusivamente las reglas estructurales del ViewModel.

        Estas validaciones no representan reglas de negocio.
        """

        if not self.title.strip():
            raise ValueError("HeroPanelViewModel.title no puede estar vacío.")

        if self.progress is not None and not 0 <= self.progress <= 100:
            raise ValueError(
                "HeroPanelViewModel.progress debe estar entre 0 y 100."
            )