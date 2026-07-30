# ==========================================================
# T3G-ASSET-003
#
# Value Object : Asset Code
# Module       : Shared
# Version      : 1.0.0
# Status       : Development
#
# Purpose
# -------
# Representa el identificador único de un activo.
#
# ==========================================================

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssetCode:
    """
    Value Object que representa el código de un activo.
    """

    value: str

    def __post_init__(self):

        value = self.value.strip().upper()

        if not value:
            raise ValueError(
                "Asset code cannot be empty."
            )

        object.__setattr__(
            self,
            "value",
            value,
        )

    def __str__(self) -> str:

        return self.value

    def __repr__(self) -> str:

        return (
            f"AssetCode('{self.value}')"
        )

    @property
    def display(self) -> str:

        return self.value

    @property
    def is_valid(self) -> bool:

        return len(self.value) >= 3