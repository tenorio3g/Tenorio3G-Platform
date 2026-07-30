# ==========================================================
# T3G-FND-007
#
# Element   : Registry Service
# Module    : Foundation Registry
# Version   : 0.1.0
# Status    : Development
# Sprint    : FND-005.3
#
# ==========================================================

from .components import COMPONENTS
from .enums import RegistryCategory, RegistryStatus
from .metadata import ComponentMetadata
from .primitives import PRIMITIVES


class RegistryService:
    """
    Proporciona operaciones de consulta sobre
    el catálogo oficial del T3G Framework.
    """

    @property
    def all(self) -> tuple[ComponentMetadata, ...]:
        return PRIMITIVES + COMPONENTS

    def get(self, component_id: str) -> ComponentMetadata | None:
        for item in self.all:
            if item.id == component_id:
                return item
        return None

    def exists(self, component_id: str) -> bool:
        return self.get(component_id) is not None

    def by_status(
        self,
        status: RegistryStatus,
    ) -> tuple[ComponentMetadata, ...]:

        return tuple(
            item
            for item in self.all
            if item.status == status
        )

    def by_category(
        self,
        category: RegistryCategory,
    ) -> tuple[ComponentMetadata, ...]:

        return tuple(
            item
            for item in self.all
            if item.category == category
        )

    def dependents_of(
        self,
        component_id: str,
    ) -> tuple[ComponentMetadata, ...]:

        return tuple(
            item
            for item in self.all
            if component_id in item.depends_on
        )
    def dependents_of(
        self,
        component_id: str,
    ) -> tuple[ComponentMetadata, ...]:
        """
        Devuelve los elementos que dependen directamente
        del elemento indicado.
        """

        return tuple(
            item
            for item in self.all
            if component_id in item.depends_on
        )

