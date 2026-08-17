from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrderSparePartItemViewModel:
    code: str
    name: str
    manufacturer: str
    part_number: str
    unit: str
    quantity: float
    unit_cost: float
    total_cost: float
    used_at: str
    observations: str


@dataclass(frozen=True)
class WorkOrderSparePartsViewModel:
    items: list[
        WorkOrderSparePartItemViewModel
    ]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total_items(self) -> int:
        return len(self.items)

    @property
    def total_cost(self) -> float:
        return sum(
            item.total_cost
            for item in self.items
        )