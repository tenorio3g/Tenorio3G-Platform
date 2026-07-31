from dataclasses import dataclass


@dataclass(slots=True)
class GetAssetLifeSheetQuery:
    code: str