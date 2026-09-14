from dataclasses import dataclass


@dataclass(frozen=True)
class WorkSessionItemViewModel:
    code: str
    person_code: str
    person_name: str
    started_at: str
    ended_at: str | None
    duration_minutes: int | None
    duration_label: str
    is_active: bool


@dataclass(frozen=True)
class TechnicianWorkSessionSummaryViewModel:
    person_code: str
    person_name: str
    total_minutes: int
    total_duration_label: str
    closed_session_count: int
    has_active_session: bool


@dataclass(frozen=True)
class ActivityWorkSessionSummaryViewModel:
    activity_code: str
    sessions: list[
        WorkSessionItemViewModel
    ]
    technicians: list[
        TechnicianWorkSessionSummaryViewModel
    ]
    total_minutes: int
    total_duration_label: str
    closed_session_count: int
    has_active_session: bool


@dataclass(frozen=True)
class WorkSessionSummaryViewModel:
    by_activity: dict[
        str,
        ActivityWorkSessionSummaryViewModel,
    ]

    @property
    def has_items(
        self,
    ) -> bool:
        return bool(
            self.by_activity
        )