"""
T3G-ASSET-UC-003

FindAllAssetModelsResult

Representa el resultado del caso de uso
FindAllAssetModels.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.assets.entities.asset_model import AssetModel


@dataclass(slots=True)
class FindAllAssetModelsResult:
    """
    Resultado del caso de uso FindAllAssetModels.
    """

    success: bool

    message: str

    asset_models: list[AssetModel] = field(default_factory=list)