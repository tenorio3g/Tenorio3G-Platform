from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeleteSparePartCommand:
    asset_code: str
    spare_part_code: str