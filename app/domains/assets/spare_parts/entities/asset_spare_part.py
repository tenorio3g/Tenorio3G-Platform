from __future__ import annotations

from app.domains.assets.spare_parts.entities.spare_part import (
    SparePart,
)


class AssetSparePart:
    """
    Relaciona una refacción con un activo específico.
    """

    def __init__(
        self,
        asset_code: str,
        spare_part: SparePart,
        quantity: float = 1,
        position: str = "",
        observations: str = "",
        is_critical: bool = False,
    ) -> None:
        self.asset_code = asset_code.strip()
        self.spare_part = spare_part
        self.quantity = quantity
        self.position = position.strip()
        self.observations = observations.strip()
        self.is_critical = is_critical

        self._validate()

    def _validate(self) -> None:
        if not self.asset_code:
            raise ValueError(
                "El código del activo es obligatorio."
            )

        if self.quantity <= 0:
            raise ValueError(
                "La cantidad debe ser mayor que cero."
            )

    @property
    def spare_part_code(self) -> str:
        return self.spare_part.code

    def __repr__(self) -> str:
        return (
            "AssetSparePart("
            f"asset_code='{self.asset_code}', "
            f"spare_part_code='{self.spare_part_code}', "
            f"quantity={self.quantity}"
            ")"
        )