from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SaveSparePartCommand:
    asset_code: str
    code: str
    name: str
    manufacturer: str
    part_number: str
    unit: str
    quantity: float
    position: str
    observations: str
    is_critical: bool