from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class DailyActivityResult:
    activity_code: str
    title: str
    status: str
    completion_notes: str
    first_started_at: datetime | None
    last_ended_at: datetime | None
    effective_seconds: int


@dataclass(frozen=True)
class DailyWorkOrderResult:
    work_order_code: str
    title: str
    asset_code: str | None
    activities: list[DailyActivityResult]


@dataclass(frozen=True)
class DailyOperationalReportResult:
    report_date: date
    work_orders: list[DailyWorkOrderResult]
    total_work_orders: int
    total_activities: int
    completed_activities: int
    in_progress_activities: int
    on_hold_activities: int
    effective_seconds: int
