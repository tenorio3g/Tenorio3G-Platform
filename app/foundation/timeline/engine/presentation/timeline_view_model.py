from dataclasses import dataclass


@dataclass(frozen=True)
class TimelineEventItemViewModel:
    event_id: str
    event_type: str
    title: str
    description: str
    actor_person_code: str
    occurred_at: str
    reference_type: str | None
    reference_code: str | None


@dataclass(frozen=True)
class TimelineViewModel:
    items: list[
        TimelineEventItemViewModel
    ]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)