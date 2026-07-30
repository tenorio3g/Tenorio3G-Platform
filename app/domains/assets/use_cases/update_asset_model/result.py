"""
T3G-ASSET-XXX

UpdateAssetModelResult

Representa el resultado del caso de uso
UpdateAssetModel.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.assets.entities.asset_model import AssetModel


@dataclass(slots=True)
class UpdateAssetModelResult:
    """
    Resultado del caso de uso UpdateAssetModel.
    """

    success: bool
    message: str
    asset_model: AssetModel | None = None