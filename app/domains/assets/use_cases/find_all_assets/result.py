from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.assets.entities.asset import Asset


@dataclass(slots=True)
class FindAllAssetsResult:
    """
    Resultado de la consulta de todos los activos.
    """

    success: bool
    message: str
    assets: list[Asset] = field(default_factory=list)