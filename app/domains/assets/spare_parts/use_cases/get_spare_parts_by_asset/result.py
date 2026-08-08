from dataclasses import dataclass, field

from app.domains.assets.spare_parts.entities import (
    AssetSparePart,
)


@dataclass(frozen=True, slots=True)
class GetSparePartsByAssetResult:
    success: bool
    message: str
    spare_parts: list[AssetSparePart] = field(
        default_factory=list
    )