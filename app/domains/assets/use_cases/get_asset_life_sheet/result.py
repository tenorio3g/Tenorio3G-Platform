from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.assets.entities.asset import Asset
    from app.domains.assets.entities.asset_model import AssetModel


@dataclass(slots=True)
class GetAssetLifeSheetResult:

    success: bool

    message: str

    asset: "Asset | None" = None

    asset_model: "AssetModel | None" = None