# ==========================================================
# T3G-FND-010
#
# Component : KPI Card ViewModel
# Module    : Foundation UI
# Version   : 0.1.0
# Status    : Development
# Sprint    : FND-010
#
# Purpose
# -------
# Define el contrato de presentación utilizado por el
# componente reutilizable KPI Card.
#
# Este archivo no contiene lógica de negocio ni depende
# de los dominios Assets, Work Orders o Inventory.
#
# ==========================================================

from dataclasses import dataclass
from typing import Optional


KPI_CARD_VARIANTS = {
    "primary",
    "success",
    "warning",
    "danger",
    "info",
    "neutral",
}


@dataclass(frozen=True)
class KpiCardViewModel:
    """
    Contrato de datos del componente KPI Card.

    El componente representa un indicador resumido mediante:

        title:
            Nombre del indicador.

        value:
            Valor principal mostrado.

        subtitle:
            Explicación breve del valor.

        icon:
            Identificador opcional de un icono del Foundation.

        variant:
            Variante visual del componente.
    """

    title: str
    value: str

    subtitle: Optional[str] = None
    icon: Optional[str] = None

    variant: str = "neutral"

    def __post_init__(self) -> None:
        """
        Valida exclusivamente las reglas estructurales
        del ViewModel.
        """

        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError(
                "KpiCardViewModel.title no puede estar vacío."
            )

        if not isinstance(self.value, str) or not self.value.strip():
            raise ValueError(
                "KpiCardViewModel.value no puede estar vacío."
            )

        if self.subtitle is not None and not isinstance(
            self.subtitle,
            str,
        ):
            raise TypeError(
                "KpiCardViewModel.subtitle debe ser texto o None."
            )

        if self.icon is not None and not isinstance(self.icon, str):
            raise TypeError(
                "KpiCardViewModel.icon debe ser texto o None."
            )

        if self.variant not in KPI_CARD_VARIANTS:
            allowed_variants = ", ".join(
                sorted(KPI_CARD_VARIANTS)
            )

            raise ValueError(
                "KpiCardViewModel.variant no es válida. "
                f"Variantes permitidas: {allowed_variants}."
            )