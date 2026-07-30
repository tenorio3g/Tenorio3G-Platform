# ==========================================================
# T3G-FND-009
#
# Element   : Registry Intelligence Service
# Module    : Foundation
# Version   : 0.1.0
# Status    : Development
# Sprint    : FND-009.1
#
# Purpose
# -------
# Proporciona consultas avanzadas, filtros y estadísticas
# sobre el Registry del T3G Framework.
#
# ==========================================================

from app.foundation.registry import RegistryService
from app.foundation.registry.enums import (
    RegistryCategory,
    RegistryStatus,
)
from app.foundation.viewmodels import (
    RegistryStatisticsViewModel,
)


class RegistryIntelligenceService:
    """
    Analiza la información contenida en el Registry
    y genera resultados reutilizables para otras capas.
    """

    def __init__(self) -> None:
        self.registry = RegistryService()

    @property
    def items(self) -> tuple:
        """
        Devuelve todos los elementos registrados.
        """

        return self.registry.all

    def by_category(
        self,
        category: RegistryCategory,
    ) -> tuple:
        """
        Devuelve los elementos pertenecientes
        a una categoría específica.
        """

        return tuple(
            item
            for item in self.items
            if item.category == category
        )

    def by_status(
        self,
        status: RegistryStatus,
    ) -> tuple:
        """
        Devuelve los elementos que poseen
        un estado específico.
        """

        return tuple(
            item
            for item in self.items
            if item.status == status
        )

    def by_owner(
        self,
        owner: str,
    ) -> tuple:
        """
        Devuelve los elementos asignados
        a un responsable específico.
        """

        normalized_owner = owner.strip().lower()

        if not normalized_owner:
            return tuple()

        return tuple(
            item
            for item in self.items
            if item.owner.strip().lower() == normalized_owner
        )

    def by_tag(
        self,
        tag: str,
    ) -> tuple:
        """
        Devuelve los elementos que contienen
        una etiqueta específica.
        """

        normalized_tag = tag.strip().lower()

        if not normalized_tag:
            return tuple()

        return tuple(
            item
            for item in self.items
            if normalized_tag in {
                current_tag.strip().lower()
                for current_tag in item.tags
            }
        )



    def search(
        self,
        query: str,
    ) -> tuple:
        """
        Busca elementos por texto dentro de sus campos principales.

        La búsqueda no distingue entre mayúsculas y minúsculas.
        """

        normalized_query = query.strip().lower()

        if not normalized_query:
            return tuple()

        return tuple(
            item
            for item in self.items
            if normalized_query in (item.id or "").lower()
            or normalized_query in (item.name or "").lower()
            or normalized_query in (item.description or "").lower()
            or normalized_query in (item.owner or "").lower()
            or any(
                normalized_query in (tag or "").lower()
                for tag in (item.tags or tuple())
            )
        )



    def sort_by_name(
        self,
        items: tuple | None = None,
    ) -> tuple:
        """
        Ordena elementos alfabéticamente por nombre.
        """

        source = self.items if items is None else items

        return tuple(
            sorted(
                source,
                key=lambda item: item.name.lower(),
            )
        )



    def sort_by_category(
        self,
        items: tuple | None = None,
    ) -> tuple:
        """
        Ordena elementos por categoría y nombre.
        """

        source = self.items if items is None else items

        return tuple(
            sorted(
                source,
                key=lambda item: (
                    item.category.value,
                    item.name.lower(),
                ),
            )
        )


    def sort_by_status(
        self,
        items: tuple | None = None,
    ) -> tuple:
        """
        Ordena elementos por estado y nombre.
        """

        source = self.items if items is None else items

        return tuple(
            sorted(
                source,
                key=lambda item: (
                    item.status.value,
                    item.name.lower(),
                ),
            )
        )









    def primitives(self) -> tuple:
        return self.by_category(
            RegistryCategory.PRIMITIVE
        )

    def components(self) -> tuple:
        return self.by_category(
            RegistryCategory.COMPONENT
        )

    def patterns(self) -> tuple:
        return self.by_category(
            RegistryCategory.PATTERN
        )

    def utilities(self) -> tuple:
        """
        Devuelve los elementos registrados como utilidades.
        """

        return self.by_category(
            RegistryCategory.UTILITY
        )

    def stable(self) -> tuple:
        return self.by_status(
            RegistryStatus.STABLE
        )

    def development(self) -> tuple:
        return self.by_status(
            RegistryStatus.DEVELOPMENT
        )

    def pending(self) -> tuple:
        return self.by_status(
            RegistryStatus.PENDING
        )

    def deprecated(self) -> tuple:
        return self.by_status(
            RegistryStatus.DEPRECATED
        )

    def statistics(
        self,
    ) -> RegistryStatisticsViewModel:
        """
        Construye las estadísticas generales del Registry.
        """

        return RegistryStatisticsViewModel(
            total=len(self.items),

            primitives=len(self.primitives()),
            components=len(self.components()),
            patterns=len(self.patterns()),
            utilities=len(self.utilities()),

            stable=len(self.stable()),
            development=len(self.development()),
            pending=len(self.pending()),
            deprecated=len(self.deprecated()),
        )