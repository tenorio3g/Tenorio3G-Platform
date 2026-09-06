from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlaceAssetOnMapCommand:
    asset_code: str
    category: str
    x: float
    y: float
