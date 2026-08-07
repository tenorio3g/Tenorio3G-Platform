from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GetTechnicalDataQuery:
    asset_code: str