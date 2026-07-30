from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.assets.entities.asset import Asset


@dataclass(slots=True)
class UpdateAssetResult:
    """
    Resultado de la actualización de un activo.
    """

    success: bool
    message: str
    asset: Asset | None = None