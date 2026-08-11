from dataclasses import dataclass


@dataclass
class MaintenanceEventItemViewModel:
    code: str
    event_type: str
    title: str
    description: str
    performed_by: str
    started_at: str
    completed_at: str
    observations: str
    status: str


@dataclass
class MaintenanceHistoryViewModel:
    items: list[MaintenanceEventItemViewModel]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)