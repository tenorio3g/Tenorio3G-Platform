# ==========================================================
# T3G-FND-005
#
# Component : Search Box ViewModel
# Module    : Foundation UI
# Version   : 0.1.0
# Status    : Development
# Sprint    : UI-005
#
# Purpose
# -------
# Define el contrato de presentación utilizado por el
# componente reutilizable Search Box.
#
# Este archivo no contiene lógica de negocio ni depende
# de los dominios Assets, Work Orders, Inventory o Knowledge.
#
# ==========================================================

from dataclasses import dataclass
from typing import Literal, Optional


SearchMethod = Literal["get", "post"]
SearchAutocomplete = Literal["on", "off"]


@dataclass(frozen=True)
class SearchBoxViewModel:
    """
    Contrato de datos del componente Search Box.

    Foundation solamente renderiza esta información.
    Cada dominio es responsable de definir la ruta, el valor
    inicial y el texto apropiado para su contexto.

    Ejemplos de uso:
        Buscar activos
        Buscar órdenes de trabajo
        Buscar materiales
        Buscar artículos de conocimiento
    """

    action: str
    name: str

    placeholder: str = "Buscar..."
    value: str = ""

    field_id: Optional[str] = None

    method: SearchMethod = "get"
    autocomplete: SearchAutocomplete = "off"

    button_label: str = "Buscar"
    button_icon: Optional[str] = "🔎"

    input_icon: Optional[str] = None

    aria_label: Optional[str] = None
    help_text: Optional[str] = None

    autofocus: bool = False
    show_button: bool = True
    disabled: bool = False

    def __post_init__(self) -> None:
        """
        Valida exclusivamente las reglas estructurales del ViewModel.

        Estas validaciones no representan reglas de negocio.
        """

        if not self.action.strip():
            raise ValueError(
                "SearchBoxViewModel.action no puede estar vacío."
            )

        if not self.name.strip():
            raise ValueError(
                "SearchBoxViewModel.name no puede estar vacío."
            )

        if not self.placeholder.strip():
            raise ValueError(
                "SearchBoxViewModel.placeholder no puede estar vacío."
            )

        if self.show_button and not self.button_label.strip():
            raise ValueError(
                "SearchBoxViewModel.button_label no puede estar vacío "
                "cuando show_button es True."
            )

        if self.field_id is not None and not self.field_id.strip():
            raise ValueError(
                "SearchBoxViewModel.field_id no puede contener "
                "una cadena vacía."
            )

        if self.aria_label is not None and not self.aria_label.strip():
            raise ValueError(
                "SearchBoxViewModel.aria_label no puede contener "
                "una cadena vacía."
            )

        if self.help_text is not None and not self.help_text.strip():
            raise ValueError(
                "SearchBoxViewModel.help_text no puede contener "
                "una cadena vacía."
            )

    @property
    def resolved_field_id(self) -> str:
        """
        Devuelve el identificador HTML del campo.

        Cuando `field_id` no fue definido, utiliza el nombre del
        parámetro de búsqueda para mantener un identificador estable.
        """

        return self.field_id or self.name

    @property
    def resolved_aria_label(self) -> str:
        """
        Devuelve una descripción accesible para el campo de búsqueda.
        """

        return self.aria_label or self.placeholder