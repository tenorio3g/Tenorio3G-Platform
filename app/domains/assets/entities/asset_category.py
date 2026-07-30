# ==========================================================
# T3G-ASSET-006
#
# Entity  : AssetCategory
# Domain  : Assets
# Version : 1.0.0
# Status  : Development
#
# Purpose
# -------
# Representa una categoría general dentro del catálogo
# técnico de activos.
#
# Ejemplos:
#
# - HVAC
# - Eléctrico
# - Mecánico
# - Instrumentación
# - Producción
#
# ==========================================================

from dataclasses import dataclass, field


@dataclass(slots=True)
class AssetCategory:
    """
    Representa una familia general de activos.

    Una categoría organiza tipos de activos relacionados.

    Ejemplo:

        AssetCategory(
            code="HVAC",
            name="Climatización y refrigeración",
            description=(
                "Equipos utilizados para climatización, "
                "ventilación y producción de agua helada."
            ),
            aliases=(
                "Climatización",
                "Aire acondicionado",
            ),
        )
    """

    code: str
    name: str
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

        self.description = self.description.strip()

        self.aliases = self._normalize_aliases(
            self.aliases,
        )

    @property
    def display_name(self) -> str:
        """
        Devuelve el nombre que puede mostrarse en la interfaz.
        """

        return f"{self.code} - {self.name}"

    @property
    def has_aliases(self) -> bool:
        """
        Indica si la categoría contiene nombres alternativos.
        """

        return bool(self.aliases)

    def activate(self) -> None:
        """
        Habilita la categoría.
        """

        self.is_active = True

    def deactivate(self) -> None:
        """
        Deshabilita la categoría sin eliminar su historial.
        """

        self.is_active = False

    def rename(self, new_name: str) -> None:
        """
        Modifica el nombre visible de la categoría.
        """

        self.name = self._normalize_required_text(
            new_name,
            field_name="new_name",
        )

    def update_description(self, description: str) -> None:
        """
        Actualiza la descripción de la categoría.
        """

        self.description = description.strip()

    def add_alias(self, alias: str) -> None:
        """
        Agrega un alias evitando valores vacíos y duplicados.
        """

        normalized_alias = self._normalize_required_text(
            alias,
            field_name="alias",
        )

        comparison_key = normalized_alias.casefold()

        existing_values = {
            self.code.casefold(),
            self.name.casefold(),
            *(
                current_alias.casefold()
                for current_alias in self.aliases
            ),
        }

        if comparison_key in existing_values:
            return

        self.aliases = (
            *self.aliases,
            normalized_alias,
        )

    def remove_alias(self, alias: str) -> None:
        """
        Elimina un alias sin distinguir mayúsculas y minúsculas.
        """

        normalized_alias = alias.strip().casefold()

        if not normalized_alias:
            return

        self.aliases = tuple(
            current_alias
            for current_alias in self.aliases
            if current_alias.casefold() != normalized_alias
        )

    def matches(self, search_term: str) -> bool:
        """
        Comprueba si un término coincide con la categoría.

        La búsqueda considera:

        - Código
        - Nombre
        - Descripción
        - Alias
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

    def same_identity_as(
        self,
        other: "AssetCategory",
    ) -> bool:
        """
        Determina si dos categorías representan la misma
        identidad mediante su código.
        """

        if not isinstance(other, AssetCategory):
            return False

        return self.code == other.code

    @staticmethod
    def _normalize_code(value: str) -> str:
        """
        Normaliza un código como ' hvac ' a 'HVAC'.
        """

        if not isinstance(value, str):
            raise TypeError(
                "Code must be a string."
            )

        normalized_value = value.strip().upper()

        if not normalized_value:
            raise ValueError(
                "Code cannot be empty."
            )

        if " " in normalized_value:
            raise ValueError(
                "Code cannot contain spaces."
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

        if not isinstance(value, str):
            raise TypeError(
                f"{field_name.capitalize()} must be a string."
            )

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
        Limpia los alias y elimina duplicados.
        """

        if aliases is None:
            return ()

        normalized_aliases: list[str] = []
        registered_aliases: set[str] = set()

        for alias in aliases:
            if not isinstance(alias, str):
                raise TypeError(
                    "Every alias must be a string."
                )

            normalized_alias = alias.strip()

            if not normalized_alias:
                continue

            comparison_key = normalized_alias.casefold()

            if comparison_key in registered_aliases:
                continue

            registered_aliases.add(comparison_key)
            normalized_aliases.append(
                normalized_alias,
            )

        return tuple(normalized_aliases)