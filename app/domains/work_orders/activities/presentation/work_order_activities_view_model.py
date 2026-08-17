from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrderActivityItemViewModel:
    code: str
    title: str
    description: str
    responsible_person_code: str
    responsible_person_name: str
    status: str
    status_label: str
    estimated_minutes: int | None
    actual_minutes: int | None
    started_at: str | None
    completed_at: str | None


@dataclass(frozen=True)
class WorkOrderActivitiesViewModel:
    items: list[
        WorkOrderActivityItemViewModel
    ]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def completed(self) -> int:
        return sum(
            1
            for item in self.items
            if item.status == "COMPLETED"
        )

    @property
    def progress_percent(self) -> int:

        if not self.items:
            return 0

        return round(
            self.completed
            / self.total
            * 100
        )