# ==========================================================
# T3G-FND-006
#
# Element   : Component Metadata
# Module    : Foundation Registry
# Version   : 0.1.0
# Status    : Development
# Sprint    : FND-005.2
#
# Purpose
# -------
# Define el contrato tipado para registrar elementos
# pertenecientes al T3G Framework.
#
# ==========================================================

from dataclasses import dataclass, field

from .enums import RegistryCategory, RegistryStatus





@dataclass(frozen=True)
class ComponentMetadata:
    """
    Representa los metadatos oficiales de un elemento
    registrado dentro del T3G Framework.
    """

    id: str
    name: str
    category: RegistryCategory
    status: RegistryStatus
    owner: str

    description: str | None = None

    version: str | None = None

    since: str | None = None

    template: str | None = None

    stylesheet: str | None = None

    viewmodel: str | None = None

    documentation: str | None = None

    tags: tuple[str, ...] = field(default_factory=tuple)

    depends_on: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        self._validate_required_fields()
        self._validate_types()
        self._validate_metadata()
        self._validate_version_state()
        self._validate_dependencies()

    def _validate_required_fields(self) -> None:
        if not self.id.strip():
            raise ValueError("ComponentMetadata.id no puede estar vacío.")

        if not self.name.strip():
            raise ValueError("ComponentMetadata.name no puede estar vacío.")

        if not self.owner.strip():
            raise ValueError("ComponentMetadata.owner no puede estar vacío.")

    def _validate_version_state(self) -> None:
        if self.status == RegistryStatus.PENDING:
            return

        if self.version is None:
            raise ValueError(
                "Un elemento que no está pendiente debe tener una versión."
            )

        if self.since is None:
            raise ValueError(
                "Un elemento que no está pendiente debe indicar desde qué versión existe."
            )

    def _validate_dependencies(self) -> None:
        if self.id in self.depends_on:
            raise ValueError(
                f"El elemento '{self.id}' no puede depender de sí mismo."
            )

        if len(self.depends_on) != len(set(self.depends_on)):
            raise ValueError(
                f"El elemento '{self.id}' contiene dependencias duplicadas."
            )
        

    
    def _validate_types(self) -> None:
        if not isinstance(self.category, RegistryCategory):
            raise TypeError(
                f"'{self.id}' contiene una categoría inválida: "
                f"{self.category!r}. Debe utilizar RegistryCategory."
            )

        if not isinstance(self.status, RegistryStatus):
            raise TypeError(
                f"'{self.id}' contiene un estado inválido: "
                f"{self.status!r}. Debe utilizar RegistryStatus."
            )

    def _validate_metadata(self) -> None:
        """
        Valida metadatos opcionales.
        """

        if self.tags:

            normalized = {
                tag.lower().strip()
                for tag in self.tags
            }

            if len(normalized) != len(self.tags):
                raise ValueError(
                    f"'{self.id}' contiene tags duplicados."
                )


    @property
    def is_stable(self) -> bool:
        return self.status == RegistryStatus.STABLE

    @property
    def is_pending(self) -> bool:
        return self.status == RegistryStatus.PENDING

    @property
    def has_dependencies(self) -> bool:
        return bool(self.depends_on)