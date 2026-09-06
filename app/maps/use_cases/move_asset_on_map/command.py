from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MoveAssetOnMapCommand:
    asset_code: str
    x: float
    y: float
