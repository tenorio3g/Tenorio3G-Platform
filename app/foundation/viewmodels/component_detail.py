# ==========================================================
# T3G-FND-012
#
# Element   : Component Detail ViewModel
# Module    : Foundation UI
# Version   : 0.1.0
# Status    : Development
# Sprint    : FND-007.1
#
# Purpose
# -------
# Define el contrato de presentación para la ficha técnica
# individual de un elemento del Registry.
#
# ==========================================================

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ComponentReferenceViewModel:
    """
    Referencia resumida hacia otro elemento del Registry.
    """

    id: str
    name: str
    category: str
    status: str


@dataclass(frozen=True)
class ComponentDetailViewModel:
    """
    Ficha técnica completa de un elemento registrado
    dentro del T3G Framework.
    """

    id: str
    name: str
    category: str
    status: str
    owner: str

    version: str | None = None
    since: str | None = None
    description: str | None = None

    template: str | None = None

    stylesheet: str | None = None

    viewmodel: str | None = None

    documentation: str | None = None

    tags: tuple[str, ...] = field(default_factory=tuple)

    dependencies: tuple[
        ComponentReferenceViewModel,
        ...
    ] = field(default_factory=tuple)

    dependents: tuple[
        ComponentReferenceViewModel,
        ...
    ] = field(default_factory=tuple)

    @property
    def has_dependencies(self) -> bool:
        return bool(self.dependencies)

    @property
    def has_dependents(self) -> bool:
        return bool(self.dependents)