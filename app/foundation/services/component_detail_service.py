# ==========================================================
# T3G-FND-013
#
# Element   : Component Detail Service
# Module    : Foundation UI
# Version   : 0.1.0
# Status    : Development
# Sprint    : FND-007.1
#
# Purpose
# -------
# Construye la ficha técnica de un elemento del Registry,
# incluyendo dependencias y dependientes directos.
#
# ==========================================================

from app.foundation.registry import RegistryService
from app.foundation.viewmodels import (
    ComponentDetailViewModel,
    ComponentReferenceViewModel,
)


class ComponentDetailService:
    """
    Construye el modelo de presentación utilizado por
    la pantalla de detalle del Foundation Explorer.
    """

    def __init__(self) -> None:
        self.registry = RegistryService()

    def build(
        self,
        component_id: str,
    ) -> ComponentDetailViewModel | None:

        item = self.registry.get(component_id)

        if item is None:
            return None

        dependencies = tuple(
            self._build_reference(dependency)
            for dependency_id in item.depends_on
            if (
                dependency :=
                self.registry.get(dependency_id)
            ) is not None
        )

        dependents = tuple(
            self._build_reference(dependent)
            for dependent in self.registry.dependents_of(
                component_id
            )
        )

        return ComponentDetailViewModel(
            id=item.id,
            name=item.name,
            category=item.category.value,
            status=item.status.value,
            owner=item.owner,
            version=item.version,
            since=item.since,
            dependencies=dependencies,
            dependents=dependents,
            description=item.description,

            template=item.template,

            stylesheet=item.stylesheet,

            viewmodel=item.viewmodel,

            documentation=item.documentation,

            tags=item.tags,
        )

    @staticmethod
    def _build_reference(
        item,
    ) -> ComponentReferenceViewModel:

        return ComponentReferenceViewModel(
            id=item.id,
            name=item.name,
            category=item.category.value,
            status=item.status.value,
        )