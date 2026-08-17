from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardRecentWorkOrderViewModel:
    code: str
    title: str
    status: str
    priority: str
    asset_code: str
    created_at: str


@dataclass(frozen=True)
class DashboardViewModel:
    total_assets: int
    total_work_orders: int
    active_people: int
    pending_activities: int

    created_work_orders: int
    assigned_work_orders: int
    in_progress_work_orders: int
    on_hold_work_orders: int

    completed_work_orders: int
    closed_work_orders: int
    cancelled_work_orders: int

    recent_work_orders: list[
        DashboardRecentWorkOrderViewModel
    ]