from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SparePartItemViewModel:
    code: str
    name: str
    manufacturer: str
    part_number: str
    quantity: float
    position: str
    observations: str
    is_critical: bool


@dataclass(frozen=True, slots=True)
class SparePartsViewModel:
    items: list[SparePartItemViewModel]

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def has_items(self) -> bool:
        return bool(self.items)