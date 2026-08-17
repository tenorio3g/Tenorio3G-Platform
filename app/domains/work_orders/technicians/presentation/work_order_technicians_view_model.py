from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrderTechnicianItemViewModel:
    person_code: str
    name: str
    position: str
    assigned_at: str


@dataclass(frozen=True)
class WorkOrderTechniciansViewModel:
    items: list[
        WorkOrderTechnicianItemViewModel
    ]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)