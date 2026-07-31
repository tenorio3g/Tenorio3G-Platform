# ==========================================================
# T3G-ASSET-002
#
# Component : Asset Identity
# Module    : Assets
# Version   : 1.0.0
# Status    : Development
#
# Purpose
# -------
# Representa la identidad de un activo dentro del dominio
# de Tenorio3G.
#
# ==========================================================

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AssetIdentity:
    """
    Información que identifica de manera única un activo.
    """

    code: str

    name: str

    description: str

    serial_number: str

    model: str

    manufacturer: str

    @property
    def display_name(self) -> str:
        """
        Nombre amigable del activo.
        """

        return f"{self.code} - {self.name}"