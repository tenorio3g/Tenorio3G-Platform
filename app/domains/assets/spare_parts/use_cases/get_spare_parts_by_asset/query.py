from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetSparePartsByAssetQuery:
    asset_code: str