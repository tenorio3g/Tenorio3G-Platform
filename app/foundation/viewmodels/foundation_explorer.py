# ==========================================================
# T3G-FND-010
#
# Element   : Foundation Explorer ViewModel
# Module    : Foundation UI
# Version   : 0.2.0
# Status    : Development
# Sprint    : FND-012.1
#
# Purpose
# -------
# Contrato completo de presentación para la pantalla
# Foundation Explorer.
#
# ==========================================================

from dataclasses import (
    dataclass,
)

from .empty_state import (
    EmptyStateViewModel,
)
from .explorer_item import (
    ExplorerItemViewModel,
)
from .explorer_summary import (
    ExplorerSummaryViewModel,
)
from .search_box import (
    SearchBoxViewModel,
)


@dataclass(slots=True)
class FoundationExplorerViewModel:
    """
    Representa todos los datos necesarios para renderizar
    la pantalla Foundation Explorer.
    """

    framework_name: str

    framework_version: str

    search_box: SearchBoxViewModel

    summary: ExplorerSummaryViewModel

    empty_state: EmptyStateViewModel | None

    items: tuple[ExplorerItemViewModel, ...]

    @property
    def has_items(self) -> bool:
        """
        Indica si existen elementos visibles.
        """

        return bool(self.items)

    @property
    def item_count(self) -> int:
        """
        Devuelve la cantidad de elementos visibles.
        """

        return len(self.items)

    @property
    def show_empty_state(self) -> bool:
        """
        Indica si debe mostrarse el componente Empty State.
        """

        return (
            not self.has_items
            and self.empty_state is not None
        )