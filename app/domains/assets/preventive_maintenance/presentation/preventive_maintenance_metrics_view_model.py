from dataclasses import dataclass


@dataclass(frozen=True)
class PreventiveMaintenanceMetricsViewModel:
    total_plans: int
    active_plans: int
    programmed: int
    due_today: int
    overdue: int
    inactive: int
    executions: int
    on_time_executions: int
    late_executions: int
    compliance_percent: float