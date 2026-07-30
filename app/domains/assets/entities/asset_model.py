# ==========================================================
# T3G-ASSET-008
#
# Entity  : AssetModel
# Domain  : Assets
# Version : 1.0.0
# Status  : Development
#
# Purpose
# -------
# Representa la ficha técnica maestra de un modelo comercial
# de equipo industrial.
#
# AssetModel conecta:
#
# - AssetType
# - Manufacturer
#
# Ejemplo:
#
# Tipo:        Chiller
# Fabricante:  Carrier
# Modelo:      30XA-120
#
# ==========================================================

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(slots=True)
class AssetModel:
    """
    Representa un modelo comercial dentro del catálogo técnico.

    El modelo contiene información compartida por todas las
    unidades físicas que pertenezcan al mismo producto.

    Ejemplo:

        AssetModel(
            code="CARRIER-30XA-120",
            name="AquaForce 30XA",
            model_number="30XA-120",
            asset_type_code="CHILLER",
            manufacturer_code="CARRIER",
            description="Chiller enfriado por aire.",
            aliases=("30XA", "AquaForce"),
            specifications={
                "voltaje": "480 V",
                "frecuencia": "60 Hz",
                "refrigerante": "R-134a",
            },
        )
    """

    code: str
    name: str
    model_number: str
    asset_type_code: str
    manufacturer_code: str
    description: str = ""
    aliases: tuple[str, ...] = field(default_factory=tuple)
    specifications: dict[str, str] = field(default_factory=dict)
    is_active: bool = True
    is_obsolete: bool = False

    def __post_init__(self) -> None:
        """
        Normaliza y valida el estado inicial de la entidad.
        """

        self.code = self._normalize_code(
            self.code,
            field_name="code",
        )

        self.name = self._normalize_required_text(
            self.name,
            field_name="name",
        )

        self.model_number = self._normalize_required_text(
            self.model_number,
            field_name="model_number",
        )

        self.asset_type_code = self._normalize_code(
            self.asset_type_code,
            field_name="asset_type_code",
        )

        self.manufacturer_code = self._normalize_code(
            self.manufacturer_code,
            field_name="manufacturer_code",
        )

        self.description = self._normalize_optional_text(
            self.description,
            field_name="description",
        )

        self.aliases = self._normalize_aliases(
            self.aliases,
        )

        self.specifications = self._normalize_specifications(
            self.specifications,
        )

    @property
    def display_name(self) -> str:
        """
        Devuelve una representación adecuada para la interfaz.
        """

        return f"{self.manufacturer_code} {self.model_number} - {self.name}"

    @property
    def has_aliases(self) -> bool:
        """
        Indica si el modelo contiene nombres alternativos.
        """

        return bool(self.aliases)

    @property
    def has_specifications(self) -> bool:
        """
        Indica si existen especificaciones técnicas registradas.
        """

        return bool(self.specifications)

    @property
    def is_available_for_new_assets(self) -> bool:
        """
        Indica si el modelo puede asignarse a nuevos activos.

        Un modelo debe estar activo y no estar obsoleto.
        """

        return self.is_active and not self.is_obsolete

    def activate(self) -> None:
        """
        Habilita el modelo dentro del catálogo.
        """

        self.is_active = True

    def deactivate(self) -> None:
        """
        Deshabilita el modelo sin eliminar su información.
        """

        self.is_active = False

    def mark_as_obsolete(self) -> None:
        """
        Marca el modelo como obsoleto o descontinuado.
        """

        self.is_obsolete = True

    def restore_from_obsolete(self) -> None:
        """
        Retira la marca de obsolescencia.
        """

        self.is_obsolete = False

    def rename(self, new_name: str) -> None:
        """
        Cambia el nombre comercial visible.
        """

        self.name = self._normalize_required_text(
            new_name,
            field_name="new_name",
        )

    def change_description(self, description: str) -> None:
        """
        Sustituye la descripción técnica general.
        """

        self.description = self._normalize_optional_text(
            description,
            field_name="description",
        )


    def replace_specifications(
        self,
        specifications: Mapping[str, str],
    ) -> None:
        """
        Sustituye completamente las especificaciones técnicas.
        """

        self.specifications = self._normalize_specifications(
            specifications
        )


    def add_alias(self, alias: str) -> None:
        """
        Agrega un nombre alternativo evitando duplicados.
        """

        normalized_alias = self._normalize_required_text(
            alias,
            field_name="alias",
        )

        comparison_key = normalized_alias.casefold()

        existing_values = {
            self.code.casefold(),
            self.name.casefold(),
            self.model_number.casefold(),
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
        Elimina un alias sin distinguir mayúsculas.
        """

        if not isinstance(alias, str):
            raise TypeError(
                "Alias must be a string."
            )

        comparison_key = alias.strip().casefold()

        if not comparison_key:
            return

        self.aliases = tuple(
            current_alias
            for current_alias in self.aliases
            if current_alias.casefold() != comparison_key
        )

    def set_specification(
        self,
        name: str,
        value: str,
    ) -> None:
        """
        Registra o sustituye una especificación técnica.

        Ejemplo:

            model.set_specification(
                "voltaje",
                "480 V",
            )
        """

        normalized_name = self._normalize_required_text(
            name,
            field_name="specification_name",
        ).casefold()

        normalized_value = self._normalize_required_text(
            value,
            field_name="specification_value",
        )

        self.specifications[normalized_name] = normalized_value

    def remove_specification(self, name: str) -> None:
        """
        Elimina una especificación técnica.
        """

        if not isinstance(name, str):
            raise TypeError(
                "Specification name must be a string."
            )

        normalized_name = name.strip().casefold()

        if not normalized_name:
            return

        self.specifications.pop(
            normalized_name,
            None,
        )

    def get_specification(
        self,
        name: str,
        default: str | None = None,
    ) -> str | None:
        """
        Obtiene una especificación por nombre.
        """

        if not isinstance(name, str):
            raise TypeError(
                "Specification name must be a string."
            )

        normalized_name = name.strip().casefold()

        if not normalized_name:
            return default

        return self.specifications.get(
            normalized_name,
            default,
        )

    def has_specification(self, name: str) -> bool:
        """
        Comprueba si existe una especificación determinada.
        """

        if not isinstance(name, str):
            return False

        normalized_name = name.strip().casefold()

        if not normalized_name:
            return False

        return normalized_name in self.specifications

    def belongs_to_type(self, asset_type_code: str) -> bool:
        """
        Comprueba si el modelo corresponde a un tipo de activo.
        """

        if not isinstance(asset_type_code, str):
            return False

        return (
            self.asset_type_code
            == asset_type_code.strip().upper()
        )

    def is_manufactured_by(
        self,
        manufacturer_code: str,
    ) -> bool:
        """
        Comprueba si pertenece a un fabricante determinado.
        """

        if not isinstance(manufacturer_code, str):
            return False

        return (
            self.manufacturer_code
            == manufacturer_code.strip().upper()
        )

    def matches(self, search_term: str) -> bool:
        """
        Comprueba si un término coincide con los datos del modelo.

        La búsqueda considera:

        - Código interno
        - Nombre comercial
        - Número de modelo
        - Tipo
        - Fabricante
        - Descripción
        - Alias
        - Especificaciones
        """

        if not isinstance(search_term, str):
            return False

        normalized_term = search_term.strip().casefold()

        if not normalized_term:
            return False

        searchable_values = (
            self.code,
            self.name,
            self.model_number,
            self.asset_type_code,
            self.manufacturer_code,
            self.description,
            *self.aliases,
            *self.specifications.keys(),
            *self.specifications.values(),
        )

        return any(
            normalized_term in value.casefold()
            for value in searchable_values
        )

    def same_identity_as(
        self,
        other: "AssetModel",
    ) -> bool:
        """
        Determina si dos objetos representan el mismo modelo.
        """

        if not isinstance(other, AssetModel):
            return False

        return self.code == other.code

    @staticmethod
    def _normalize_code(
        value: str,
        *,
        field_name: str,
    ) -> str:
        """
        Limpia y normaliza un código.
        """

        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        normalized_value = value.strip().upper()

        if not normalized_value:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

        if " " in normalized_value:
            raise ValueError(
                f"{field_name} cannot contain spaces."
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
                f"{field_name} must be a string."
            )

        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(
                f"{field_name} cannot be empty."
            )

        return normalized_value

    @staticmethod
    def _normalize_optional_text(
        value: str,
        *,
        field_name: str,
    ) -> str:
        """
        Limpia un texto opcional.
        """

        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        return value.strip()

    @classmethod
    def _normalize_aliases(
        cls,
        aliases: tuple[str, ...],
    ) -> tuple[str, ...]:
        """
        Limpia alias y elimina duplicados.
        """

        if aliases is None:
            return ()

        normalized_aliases: list[str] = []
        registered_aliases: set[str] = set()

        for alias in aliases:
            normalized_alias = cls._normalize_required_text(
                alias,
                field_name="alias",
            )

            comparison_key = normalized_alias.casefold()

            if comparison_key in registered_aliases:
                continue

            registered_aliases.add(comparison_key)
            normalized_aliases.append(
                normalized_alias,
            )

        return tuple(normalized_aliases)

    @classmethod
    def _normalize_specifications(
        cls,
        specifications: Mapping[str, str],
    ) -> dict[str, str]:
        """
        Limpia las especificaciones técnicas.

        Los nombres se almacenan en minúsculas para evitar
        duplicados como:

        - Voltaje
        - voltaje
        - VOLTAJE
        """

        if specifications is None:
            return {}

        if not isinstance(specifications, Mapping):
            raise TypeError(
                "Specifications must be a mapping."
            )

        normalized_specifications: dict[str, str] = {}

        for name, value in specifications.items():
            normalized_name = cls._normalize_required_text(
                name,
                field_name="specification_name",
            ).casefold()

            normalized_value = cls._normalize_required_text(
                value,
                field_name="specification_value",
            )

            normalized_specifications[
                normalized_name
            ] = normalized_value

        return normalized_specifications