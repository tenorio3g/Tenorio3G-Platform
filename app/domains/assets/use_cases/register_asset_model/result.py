"""
T3G-ASSET-UC-001

RegisterAssetModelResult

Representa el resultado del caso de uso
RegisterAssetModel.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.assets.entities.asset_model import AssetModel


@dataclass(slots=True)
class RegisterAssetModelResult:
    """
    Resultado del caso de uso RegisterAssetModel.
    """

    success: bool

    message: str

    asset_model: AssetModel | None = None