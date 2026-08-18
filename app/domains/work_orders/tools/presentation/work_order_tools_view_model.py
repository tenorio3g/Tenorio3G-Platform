from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrderToolItemViewModel:
    usage_id: str
    tool_code: str
    tool_name: str
    quantity: int
    status: str
    status_label: str
    issued_at: str
    returned_at: str | None
    observations: str


@dataclass(frozen=True)
class WorkOrderToolsViewModel:
    items: list[
        WorkOrderToolItemViewModel
    ]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def issued(self) -> int:
        return sum(
            1
            for item in self.items
            if item.status == "ISSUED"
        )

    @property
    def returned(self) -> int:
        return sum(
            1
            for item in self.items
            if item.status == "RETURNED"
        )