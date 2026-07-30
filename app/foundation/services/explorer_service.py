# ==========================================================
# T3G-FND-011
#
# Element   : Foundation Explorer Service
# Module    : Foundation UI
# Version   : 0.3.0
# Status    : Development
# Sprint    : FND-006.2
#
# Purpose
# -------
# Construye el ViewModel de Foundation Explorer a partir
# del Registry oficial del T3G Framework.
#
# Responsibilities
# ----------------
# - Filtrar los elementos del Registry.
# - Construir los elementos de presentación.
# - Calcular el resumen de los resultados visibles.
# - Construir el componente de búsqueda.
#
# ==========================================================

from typing import Any, Iterable

from app.foundation.registry import (
    RegistryCategory,
    RegistryService,
    RegistryStatus,
)
from app.foundation.viewmodels import (
    EmptyStateViewModel,
    ExplorerItemViewModel,
    ExplorerSummaryViewModel,
    FoundationExplorerViewModel,
    SearchBoxViewModel,
)


class FoundationExplorerService:
    """
    Traduce los metadatos internos del Registry a modelos
    de presentación para Foundation Explorer.
    """

    def __init__(self) -> None:
        self.registry = RegistryService()

    def build(
        self,
        framework_version: str,
        search: str = "",
    ) -> FoundationExplorerViewModel:
        """
        Construye el contrato completo de presentación
        para la pantalla Foundation Explorer.
        """

        normalized_search = search.strip()

        registry_items = self._filter_registry(
            items=self.registry.all,
            search=normalized_search,
        )

        items = self._build_items(
            registry_items=registry_items,
        )

        summary = self._build_summary(
            registry_items=registry_items,
        )

        search_box = self._build_search_box(
            search=normalized_search,
        )

        empty_state = self._build_empty_state(
            registry_items=registry_items,
            search=normalized_search,
        )


        return FoundationExplorerViewModel(
            framework_name="T3G Framework",
            framework_version=framework_version,
            search_box=search_box,
            summary=summary,
            empty_state=empty_state,
            items=items,
        )

    def _filter_registry(
        self,
        items: Iterable[Any],
        search: str,
    ) -> tuple[Any, ...]:
        """
        Filtra los elementos del Registry mediante una
        búsqueda libre sobre sus principales metadatos.
        """

        registry_items = tuple(items)

        if not search:
            return registry_items

        search_term = search.casefold()

        return tuple(
            item
            for item in registry_items
            if self._matches_search(
                item=item,
                search_term=search_term,
            )
        )

    def _matches_search(
        self,
        item: Any,
        search_term: str,
    ) -> bool:
        """
        Indica si un elemento coincide con el término
        de búsqueda recibido.
        """

        searchable_values = (
            item.id,
            item.name,
            self._resolve_value(item.category),
            self._resolve_value(item.status),
            item.owner,
            item.version,
            item.since,
        )

        return any(
            search_term in str(value).casefold()
            for value in searchable_values
            if value is not None
        )

    def _build_items(
        self,
        registry_items: Iterable[Any],
    ) -> tuple[ExplorerItemViewModel, ...]:
        """
        Convierte los elementos internos del Registry
        en modelos de presentación.
        """

        return tuple(
            ExplorerItemViewModel(
                id=item.id,
                name=item.name,
                category=self._resolve_value(
                    item.category,
                ),
                status=self._resolve_value(
                    item.status,
                ),
                owner=item.owner,
                version=item.version,
                since=item.since,
                depends_on=item.depends_on,
            )
            for item in registry_items
        )

    def _build_summary(
        self,
        registry_items: Iterable[Any],
    ) -> ExplorerSummaryViewModel:
        """
        Calcula las estadísticas del conjunto actualmente
        visible en Foundation Explorer.
        """

        items = tuple(registry_items)

        return ExplorerSummaryViewModel(
            total=len(items),
            primitives=self._count_by_category(
                items=items,
                category=RegistryCategory.PRIMITIVE,
            ),
            components=self._count_by_category(
                items=items,
                category=RegistryCategory.COMPONENT,
            ),
            patterns=self._count_by_category(
                items=items,
                category=RegistryCategory.PATTERN,
            ),
            utilities=self._count_by_category(
                items=items,
                category=RegistryCategory.UTILITY,
            ),
            stable=self._count_by_status(
                items=items,
                status=RegistryStatus.STABLE,
            ),
            development=self._count_by_status(
                items=items,
                status=RegistryStatus.DEVELOPMENT,
            ),
            pending=self._count_by_status(
                items=items,
                status=RegistryStatus.PENDING,
            ),
            deprecated=self._count_by_status(
                items=items,
                status=RegistryStatus.DEPRECATED,
            ),
        )

    def _build_search_box(
        self,
        search: str,
    ) -> SearchBoxViewModel:
        """
        Construye el componente de búsqueda utilizado
        por Foundation Explorer.
        """

        return SearchBoxViewModel(
            action="/foundation/explorer",
            name="q",
            placeholder="Buscar componente...",
            value=search,
            button_label="Buscar",
            button_icon="🔎",
            input_icon="🔎",
            aria_label="Buscar componentes de Foundation",
            help_text=(
                "Puede buscar por nombre, identificador, "
                "categoría, estado, responsable o versión."
            ),
        )



    def _build_empty_state(
        self,
        registry_items,
        search: str,
    ) -> EmptyStateViewModel | None:
        """
        Construye el Empty State cuando la búsqueda
        no produce resultados.
        """

        if registry_items:
            return None

        if search:

            return EmptyStateViewModel(
                icon="🔍",
                title="No encontramos componentes",
                description=(
                    f'No existe ningún componente que '
                    f'coincida con "{search}".'
                ),
                action_label="Limpiar búsqueda",
                action_url="/foundation/explorer",
                show_action=True,
            )

        return EmptyStateViewModel(
            icon="📦",
            title="No existen componentes",
            description=(
                "El Registry todavía no contiene "
                "componentes para mostrar."
            ),
        )


    

    @staticmethod
    def _count_by_category(
        items: Iterable[Any],
        category: RegistryCategory,
    ) -> int:
        """
        Cuenta los elementos pertenecientes a una categoría.
        """

        return sum(
            1
            for item in items
            if item.category == category
        )

    @staticmethod
    def _count_by_status(
        items: Iterable[Any],
        status: RegistryStatus,
    ) -> int:
        """
        Cuenta los elementos pertenecientes a un estado.
        """

        return sum(
            1
            for item in items
            if item.status == status
        )

    @staticmethod
    def _resolve_value(value: Any) -> str:
        """
        Obtiene el valor de presentación de un Enum
        o convierte el valor recibido a texto.
        """

        if hasattr(value, "value"):
            return str(value.value)

        return str(value)