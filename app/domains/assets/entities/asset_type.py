# ==========================================================
# T3G-ASSET-005
#
# Entity  : AssetType
# Domain  : Assets
# Version : 1.0.0
# Status  : Development
#
# Purpose
# -------
# Representa un tipo de activo dentro de Tenorio3G.
#
# Un tipo de activo define el conocimiento general compartido
# por varias instancias de equipos, por ejemplo:
#
# - Chiller
# - Tablero
# - Transformador
# - UMA
# - Motor
#
# ==========================================================

from dataclasses import dataclass, field


@dataclass(slots=True)
class AssetType:
    """
    Representa la clasificación funcional de un activo.

    Ejemplo:

        AssetType(
            code="CHILLER",
            name="Chiller",
            category_code="HVAC",
            description="Equipo de producción de agua helada.",
            aliases=("CH", "Enfriador de agua"),
        )
    """

    code: str
    name: str
    category_code: str
    description: str = ""
    aliases: tuple[str, ...] = field(default_factory=tuple)
    is_active: bool = True

    def __post_init__(self) -> None:
        """
        Normaliza y valida los datos iniciales.
        """

        self.code = self._normalize_code(self.code)
        self.name = self._normalize_required_text(
            self.name,
            field_name="name",
        )
        self.category_code = self._normalize_code(
            self.category_code,
        )
        self.description = self.description.strip()
        self.aliases = self._normalize_aliases(self.aliases)

    @property
    def display_name(self) -> str:
        """
        Devuelve una representación corta para la interfaz.
        """

        return f"{self.code} - {self.name}"

    @property
    def has_aliases(self) -> bool:
        """
        Indica si el tipo contiene nombres alternativos.
        """

        return bool(self.aliases)

    def activate(self) -> None:
        """
        Habilita el tipo para utilizarlo en nuevos activos.
        """

        self.is_active = True

    def deactivate(self) -> None:
        """
        Deshabilita el tipo sin eliminar su historial.
        """

        self.is_active = False

    def add_alias(self, alias: str) -> None:
        """
        Agrega un alias evitando valores vacíos y duplicados.
        """

        normalized_alias = self._normalize_required_text(
            alias,
            field_name="alias",
        )

        existing_aliases = {
            current_alias.casefold()
            for current_alias in self.aliases
        }

        if normalized_alias.casefold() in existing_aliases:
            return

        if normalized_alias.casefold() == self.name.casefold():
            return

        self.aliases = (*self.aliases, normalized_alias)

    def remove_alias(self, alias: str) -> None:
        """
        Elimina un alias sin distinguir mayúsculas y minúsculas.
        """

        normalized_alias = alias.strip().casefold()

        self.aliases = tuple(
            current_alias
            for current_alias in self.aliases
            if current_alias.casefold() != normalized_alias
        )

    def matches(self, search_term: str) -> bool:
        """
        Comprueba si un término coincide con el código,
        nombre, descripción o alguno de los alias.
        """

        normalized_term = search_term.strip().casefold()

        if not normalized_term:
            return False

        searchable_values = (
            self.code,
            self.name,
            self.description,
            *self.aliases,
        )

        return any(
            normalized_term in value.casefold()
            for value in searchable_values
        )

    @staticmethod
    def _normalize_code(value: str) -> str:
        """
        Normaliza códigos como ' hvac ' a 'HVAC'.
        """

        normalized_value = value.strip().upper()

        if not normalized_value:
            raise ValueError(
                "Code cannot be empty."
            )

        return normalized_value

    @staticmethod
    def _normalize_required_text(
        value: str,
        *,
        field_name: str,
    ) -> str:
        """
        Limpia y valida un texto obligatorio.
        """

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(
                f"{field_name.capitalize()} cannot be empty."
            )

        return normalized_value

    @classmethod
    def _normalize_aliases(
        cls,
        aliases: tuple[str, ...],
    ) -> tuple[str, ...]:
        """
        Limpia alias, elimina vacíos y evita duplicados.
        """

        normalized_aliases: list[str] = []
        registered_aliases: set[str] = set()

        for alias in aliases:
            normalized_alias = alias.strip()

            if not normalized_alias:
                continue

            comparison_key = normalized_alias.casefold()

            if comparison_key in registered_aliases:
                continue

            registered_aliases.add(comparison_key)
            normalized_aliases.append(normalized_alias)

        return tuple(normalized_aliases)