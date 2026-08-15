from dataclasses import dataclass


@dataclass(frozen=True)
class PreventiveMaintenanceExecutionItemViewModel:
    code: str
    plan_code: str
    performed_by: str
    scheduled_at: str
    completed_at: str
    status: str
    observations: str


@dataclass(frozen=True)
class PreventiveMaintenanceExecutionsViewModel:
    items: list[
        PreventiveMaintenanceExecutionItemViewModel
    ]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)