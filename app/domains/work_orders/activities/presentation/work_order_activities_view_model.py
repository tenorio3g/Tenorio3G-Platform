from dataclasses import dataclass, field


@dataclass(frozen=True)
class ActivityHoldHistoryItemViewModel:
    code: str
    reason: str
    reason_label: str
    observations: str
    held_at: str
    held_by_person_code: str
    held_by_person_name: str | None
    resumed_at: str | None
    resumed_by_person_code: str | None
    resumed_by_person_name: str | None
    duration_minutes: int | None
    is_active: bool


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
    hold_reason: str | None = None
    hold_reason_label: str | None = None
    hold_observations: str | None = None
    held_at: str | None = None
    held_by_person_code: str | None = None
    held_by_person_name: str | None = None
    hold_history: list[
        ActivityHoldHistoryItemViewModel
    ] = field(
        default_factory=list
    )


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
