"""
T3G-ASSET-UC-002

FindAssetModelByCodeResult

Representa el resultado del caso de uso
FindAssetModelByCode.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.assets.entities.asset_model import AssetModel


@dataclass(slots=True)
class FindAssetModelByCodeResult:
    """
    Resultado del caso de uso FindAssetModelByCode.
    """

    success: bool

    message: str

    asset_model: AssetModel | None = None