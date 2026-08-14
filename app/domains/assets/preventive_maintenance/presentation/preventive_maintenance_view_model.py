from dataclasses import dataclass


@dataclass(frozen=True)
class PreventiveMaintenanceItemViewModel:
    code: str
    title: str
    frequency_days: int
    responsible_person_code: str
    next_due_at: str
    status: str
    is_active: bool


@dataclass(frozen=True)
class PreventiveMaintenanceViewModel:
    items: list[PreventiveMaintenanceItemViewModel]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)